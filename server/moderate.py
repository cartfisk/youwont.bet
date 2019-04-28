import os
import shutil
from pymongo import MongoClient
from bson import ObjectId

from server.constants import IMAGE_SUBMISSION_PATHS
from server.images import update_master_image


def get_submission(_id):
    mongo = MongoClient(os.environ["DB"])
    submissions = mongo["youwont"]["submissions"]
    return submissions.find_one({"_id": _id})


def handle_file(filename, status):
    pending_path = os.path.join(IMAGE_SUBMISSION_PATHS["PENDING"], filename)
    new_path = os.path.join(IMAGE_SUBMISSION_PATHS[status], filename)
    shutil.move(pending_path, new_path)
    return new_path


def moderate(string_id, status):
    _id = ObjectId(string_id)
    submission = get_submission(_id)
    mongo = MongoClient(os.environ["DB"])
    submissions = mongo["youwont"]["submissions"]
    last_accepted_cursor = (
        submissions.find({"position": {"$exists": True}})
        .sort([("position", -1)])
        .limit(1)
    )
    position = 0
    if last_accepted_cursor.count() > 0:
        position = last_accepted_cursor.next()["position"] + 1

    if submission is not None:
        update = {"status": status}
        if status == "ACCEPTED":
            update["position"] = position
        submissions.update_one({"_id": _id}, {"$set": update})

    else:
        return {"success": False, "error": "Can't find that submission."}
    filename = submission["filename"]
    path = handle_file(filename, status)
    submission["position"] = position
    return {"success": True, "submission": submission, "file": path}


def accept(_id):
    result = moderate(_id, "ACCEPTED")
    if result.get("success", False):
        update_master_image(result["file"], result["submission"]["position"])
        return True
    else:
        return False


def reject(_id):
    moderate(_id, "REJECTED")
    return True
