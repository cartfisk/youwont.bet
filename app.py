# app.py
import os
import random
from bson import ObjectId
from datetime import datetime
import mimetypes
from pymongo import MongoClient
from flask import (
    Flask,
    request,
    redirect,
    url_for,
    flash,
    render_template,
    session,
    abort,
    jsonify,
    send_file,
)
from werkzeug.utils import secure_filename

from server.slack import (
    send_slack_moderation_messages,
    slack_message_actions,
)
from server.moderate import accept
from server.constants import (
    IMAGE_SUBMISSION_PATHS,
    AUDIO_ARCHIVE_PATH,
)

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


@app.route("/")
def index():
    # TODO: check for cookie and disable site
    return render_template("index.html")


# SLACK INTERACTION ENDPOINTS
@app.route("/v1/slack/message_actions", methods=["POST"])
def message_actions():
    return slack_message_actions(request)


@app.route("/v1/upload", methods=["POST"])
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

    # send_slack_moderation_messages(image_path, _id)
    # TODO: store cookie and block more than 1 submission
    # TODO: don't make accept happen automatically
    accept(_id)
    return jsonify({"message": "success", "download_code": download_code}, 200)


@app.route("/download/<code>", methods=["GET"])
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
        return render_template("invalid.html")

if __name__ == "__main__":

    app.run(host="0.0.0.0")
