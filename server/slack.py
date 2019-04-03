from slackclient import SlackClient
from flask import jsonify
from server.moderate import (
    accept,
    reject,
)

SLACK_TOKEN = "xoxb-207397077559-597873676612-sF2fRZ7ehH7CoQE0f5AqAsq2"

def slack_message_actions(request):
    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    # Check to see what the user's selection was and update the message
    selection = form_json["actions"][0]["selected_options"][0]["value"]

    if selection == "APPROVED":
        message_text = "The only winning move is not to play.\nHow about a nice game of chess?"
    elif selection == "REJECTED":
        message_text = ":horse:"

    slack_client = SlackClient(SLACK_TOKEN)
    response = slack_client.api_call(
      "chat.update",
      channel=form_json["channel"]["id"],
      ts=form_json["message_ts"],
      text=message_text,
      attachments=[]
    )

    return jsonify("", 200)

def send_slack_moderation_messages(image_path, _id):
    slack_client = SlackClient(SLACK_TOKEN)

    with open(image_path, "rb") as file_content:
        slack_client.api_call(
            "files.upload",
            channels="#submissions",
            filename="image.png",
            file=file_content,
            title="New Submission"
        )

    blocks = [
    	{
    		"type": "section",
    		"text": {
    			"type": "mrkdwn",
    			"text": "A new image has been submitted, would you like to approve it?"
    		}
    	},
    	{
    		"type": "actions",
    		"block_id": "moderate_images",
    		"elements": [
    			{
                    "type": "button",
                    "action_id": "approve_{}".format(_id),
                    "text": {
                        "type": "plain_text",
                        "text": "Approve"
                    },
                    "confirm": {
                        "title": {
                            "type": "plain_text",
                            "text": "Are you sure?"
                        },
                        "text": {
                            "type": "mrkdwn",
                            "text": "Do you really want to accept this image?"
                        },
                        "confirm": {
                            "type": "plain_text",
                            "text": "Approve"
                        },
                        "deny": {
                            "type": "plain_text",
                            "text": "Cancel"
                        }
                    },
    			},
                {
    				"type": "button",
                    "action_id": "reject_{}".format(_id),
                    "text": {
                        "type": "plain_text",
                        "text": "Reject"
                    },
                    "confirm": {
                        "title": {
                            "type": "plain_text",
                            "text": "Are you sure?"
                        },
                        "text": {
                            "type": "mrkdwn",
                            "text": "Do you really want to reject this image?"
                        },
                        "confirm": {
                            "type": "plain_text",
                            "text": "Reject"
                        },
                        "deny": {
                            "type": "plain_text",
                            "text": "Cancel"
                        }
                    },
    			}
    		]
    	}
    ]

    slack_client.api_call(
        "chat.postMessage",
        channel="#submissions",
        blocks=blocks
    )
