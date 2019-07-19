import json
from slackclient import SlackClient
from flask import jsonify
import requests
import multiprocessing
import os

from server.moderate import accept, reject

SLACK_TOKEN = os.environ["YOUWONT_SLACK_TOKEN"]

def handle_message_action(form_json):
    response_url = form_json["response_url"]
    # Check to see what the user's selection was and update the message
    action_id = form_json["actions"][0]["action_id"].split("_")
    selection = action_id[0]
    submission_id = action_id[1]

    if selection == "approve":
        message_text = "Photo Approved :camera_with_flash:"
        attachment_text = "This photo will appear on youwont.bet in a moment."
        p = multiprocessing.Process(target=accept, args=(submission_id,))
        p.start()
    elif selection == "reject":
        message_text = "Photo Rejected :no_entry:"
        attachment_text = "This photo has been rejected but is still available in the `assets/images/submissions/rejected` folder."
        p = multiprocessing.Process(target=reject, args=(submission_id,))
        p.start()

    response_body = {
        "text": message_text,
        "attachments": [
            {
                "text": attachment_text
            }
        ],
        "response_type": "in_channel"
    }
    response = requests.post(response_url, json=response_body)
    return response

def slack_message_actions(request):
    # Parse the request payload
    form_json = json.loads(request.form["payload"])
    p = multiprocessing.Process(target=handle_message_action, args=(form_json,))
    p.start()
    return jsonify("", 200)




def send_slack_moderation_messages(image_path, _id):
    slack_client = SlackClient(SLACK_TOKEN)

    with open(image_path, "rb") as file_content:
        slack_client.api_call(
            "files.upload",
            channels="#submissions",
            filename="image.png",
            file=file_content,
            title="New Submission",
        )

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "A new image has been submitted, would you like to approve it?",
            },
        },
        {
            "type": "actions",
            "block_id": "moderate_images",
            "elements": [
                {
                    "type": "button",
                    "action_id": "approve_{}".format(_id),
                    "text": {"type": "plain_text", "text": "Approve"},
                    "confirm": {
                        "title": {"type": "plain_text", "text": "Are you sure?"},
                        "text": {
                            "type": "mrkdwn",
                            "text": "Do you really want to accept this image?",
                        },
                        "confirm": {"type": "plain_text", "text": "Approve"},
                        "deny": {"type": "plain_text", "text": "Cancel"},
                    },
                },
                {
                    "type": "button",
                    "action_id": "reject_{}".format(_id),
                    "text": {"type": "plain_text", "text": "Reject"},
                    "confirm": {
                        "title": {"type": "plain_text", "text": "Are you sure?"},
                        "text": {
                            "type": "mrkdwn",
                            "text": "Do you really want to reject this image?",
                        },
                        "confirm": {"type": "plain_text", "text": "Reject"},
                        "deny": {"type": "plain_text", "text": "Cancel"},
                    },
                },
            ],
        },
    ]

    slack_client.api_call("chat.postMessage", channel="#submissions", blocks=blocks)
