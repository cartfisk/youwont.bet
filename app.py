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
)
from werkzeug.utils import secure_filename
import multiprocessing

from server.constants import (
    IMAGE_SUBMISSION_PATHS,
    AUDIO_ARCHIVE_PATH,
)
from server.slack import (
    send_slack_moderation_messages,
    slack_message_actions,
)

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


# SLACK INTERACTION ENDPOINTS
@app.route("/api/v1/slack/message_actions", methods=["POST"])
def message_actions():
    return slack_message_actions(request)


@app.route("/api/v1/upload", methods=["POST"])
def handle_incoming_photo():
    image = request.files.get("file")
    mongo = MongoClient(os.environ["DB"])
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


@app.route("/api/v1/download/<code>", methods=["GET"])
def download_album(code):
    mongo = MongoClient(os.environ["DB"])
    download_codes = mongo["youwont"]["download_codes"]
    code_doc = download_codes.find_one({"_id": ObjectId(code)})
    is_valid = False
    if code_doc is not None:
        is_valid = code_doc.get("valid", False)
    if is_valid:
        return send_file(
            AUDIO_ARCHIVE_PATH,
            attachment_filename="pace-yourself.zip",
            as_attachment=True,
            mimetype="application/zip"
        )
    else:
        return jsonify({"message": "invalid download code"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0")
