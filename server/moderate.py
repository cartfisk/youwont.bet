import os, shutil
from pymongo import MongoClient
from flask import jsonify

from server.constants import IMAGE_SUBMISSION_PATHS
from server.images import update_master_image
from server.files import delete_directory_contents, copy_directory

def get_submission(_id):
    mongo = MongoClient(os.environ["DB"])
    submissions = mongo["youwont"]["submissions"]
    return submissions.find_one({
        "_id": _id
    })

def handle_file(filename, status):
    pending_path = os.path.join(IMAGE_SUBMISSION_PATHS["PENDING"], filename)
    new_path = os.path.join(IMAGE_SUBMISSION_PATHS[status], filename)
    shutil.move(pending_path, new_path)
    return new_path

def moderate(_id, status):
    submission = get_submission(_id)
    last_accepted_cursor = submissions.find({"position": {"$exists": True}}).sort([('position', -1)]).limit(1)
    position = 0
    if last_accepted_cursor.count() > 0:
        position = last_accepted_cursor.next()["position"] + 1

    if submission is not None:
        update = {"status": status}
        if status == "ACCEPTED":
            update["position"] = position
        mongo = MongoClient(os.environ["DB"])
        submissions = mongo["youwont"]["submissions"]
        submissions.update_one({"_id": _id}, update)
    else:
        return {"success": False, "error": "Can't find that submission."}
    filename = submission["filename"]
    path = handle_file(filename, status)
    return {"success": True, "submission": submission, "file": path}

def accept(_id):
    result = moderate(_id, "ACCEPTED")
    if result.get("success", False):
        update_master_image(result["file"], result["submission"]["position"])

    else:
        return jsonify({"message": "Can't find that submission..."}, 500)

def reject(_id):
    moderate("REJECTED")
    return True