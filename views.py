# app.py
import os
from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient
from flask import (
    Flask,
    request,
    redirect,
    url_for,
    flash,
    session,
    abort,
    jsonify,
    send_file,
    current_app,
    Blueprint,
)
from werkzeug.utils import secure_filename
import multiprocessing

from server.constants import (
    IMAGE_SUBMISSION_PATHS,
    # AUDIO_ARCHIVE_PATH,
)
from server.slack import (
    send_slack_moderation_messages,
    slack_message_actions,
)

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

api = Blueprint('api', __name__, url_prefix='/api/v1')


# SLACK INTERACTION ENDPOINTS
@api.route("/slack/message_actions", methods=["POST"])
def message_actions():
    return slack_message_actions(request)

@api.route("/upload", methods=["POST"])
def handle_incoming_photo():
    image = request.files.get("file")
    mongo = MongoClient(current_app.config["DB"])
    submissions = mongo["youwont"]["submissions"]
    download_codes = mongo["youwont"]["download_codes"]
    extension = image.filename.split(".")[-1]
    ts = datetime.now().timestamp()
    filename = "image_{}.{}".format(ts, extension)
    image_path = os.path.join(IMAGE_SUBMISSION_PATHS["PENDING"], secure_filename(filename))
    image.save(image_path)

    mongo_result = submissions.insert_one({
        "filename": filename,
        "added": datetime.now(),
        "status": "PENDING",
    })

    download_code_result = download_codes.insert_one({
        "valid": True
    })

    download_code = str(download_code_result.inserted_id)
    _id = mongo_result.inserted_id

    p = multiprocessing.Process(target=send_slack_moderation_messages, args=(image_path, _id,))
    p.start()

    return jsonify({"message": "success", "download_code": download_code})
