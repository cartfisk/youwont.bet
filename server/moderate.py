import os
import shutil
from pymongo import MongoClient
from bson import ObjectId
import redis
from rq import Queue
from flask import current_app

from server.constants import IMAGE_SUBMISSION_PATHS
from server.images import update_master_image


def get_submission(_id):
    mongo = MongoClient(current_app.config["DB"])
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
    mongo = MongoClient(current_app.config["DB"])
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


def queued_accept(_id):
    result = moderate(_id, "ACCEPTED")
    if result.get("success", False):
        update_master_image(result["file"], result["submission"]["position"])
        return True
    else:
        return False


def queued_reject(_id):
    moderate(_id, "REJECTED")
    return True

def queue(task, args):
    redis_url = current_app.config['REDIS_URL']
    redis_connection = redis.from_url(redis_url)
    q = Queue(connection=redis_connection)
    q.enqueue(task, args)

def accept(_id):
    queue(queued_accept, _id)

def reject(_id):
    queue(queued_reject, _id)
