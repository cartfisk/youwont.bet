# app.py
import os
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
)
from werkzeug.utils import secure_filename

from slackclient import SlackClient
from server.slack import (
    SLACK_TOKEN,
    send_slack_moderation_messages,
    slack_message_options,
    slack_message_actions,
)
from server.moderate import accept
from server.constants import IMAGE_SUBMISSION_PATHS

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route("/")
def index():
    return render_template("index.html")

# SLACK INTERACTION ENDPOINTS
@app.route("/v1/slack/message_options", methods=["POST"])
def message_options():
    return slack_message_options(request)


@app.route("/v1/slack/message_actions", methods=["POST"])
def message_actions():
    return slack_message_actions(request)

@app.route("/v1/upload", methods=["POST"])
def handle_incoming_photo():
    image = request.files.get("file")
    mongo = MongoClient(os.environ["DB"])
    submissions = mongo["youwont"]["submissions"]

    extension = mimetypes.guess_extension(image.mimetype)
    filename = "image_{0:05d}{1}".format(position, extension)
    image_path = os.path.join(IMAGE_SUBMISSION_PATHS["PENDING"], secure_filename(filename))
    image.save(image_path)

    mongo_result = submissions.insert_one({
        "filename": filename,
        "added": datetime.now(),
        "status": "PENDING",
    })

    _id = str(mongo_result.inserted_id)



    # send_slack_moderation_messages(image_path)

    accept(_id)

    return jsonify({"message": "success"}, 200)

if __name__ == '__main__':

    app.run(host='0.0.0.0')
