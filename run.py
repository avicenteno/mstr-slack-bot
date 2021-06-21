import logging
import sys
import getopt

logging.basicConfig(level=logging.DEBUG)

import os

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

import constants as c

# Install the Slack app and get xoxb- token in advance
#app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])
app = AsyncApp(token=c.SLACK_BOT_TOKEN)


@app.command("/hello-socket-mode")
async def hello_command(ack, body):
    user_id = body["user_id"]
    await ack(f"Hi <@{user_id}>!")


@app.event("app_mention")
async def event_test(event, say):
    await say(f"Hi there, <@{event['user']}>!")

async def publish_reports(channel, report_url, file_path):
    
    #await app.client.files_upload(
    #    channels=channel,
    #    initial_comment=f"For more details: {report_url}",
    #    file=file_path
    #)

    await app.client.chat_postMessage(
        channel=channel,
        text='text',
        blocks= [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": ":newspaper:  Paper Company Newsletter  :newspaper:"
			}
		},
		{
			"type": "context",
			"elements": [
				{
					"text": "*November 12, 2019*  |  Sales Team Announcements",
					"type": "mrkdwn"
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": " :loud_sound: *IN CASE YOU MISSED IT* :loud_sound:"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Replay our screening of *Threat Level Midnight* and pick up a copy of the DVD to give to your customers at the front desk."
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Watch Now",
					"emoji": True
				}
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":calendar: |   *PENDING REPORTS*  | :calendar: "
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "`11/20-11/22` *Beet the Competition* _ annual retreat at Schrute Farms_"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "RSVP",
					"emoji": True
				}
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "`12/01` *Toby's Going Away Party* at _Benihana_"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Learn More",
					"emoji": True
				}
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "`11/13` :pretzel: *Pretzel Day* :pretzel: at _Scranton Office_"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "RSVP",
					"emoji": True
				}
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":calendar: |   *AVAILABLE REPORTS*  | :calendar: "
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "`10/21` *Conference Room Meeting*"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Watch Recording",
					"emoji": True
				}
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*FOR YOUR INFORMATION*"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "MicroStrategy Links \n\n https://microstrategy.prod.gaikai.com/MicroStrategy/servlet/mstrWeb \n\n https://microstrategy.prod.gaikai.com/MicroStrategyLibrary/app",
				"verbatim": False
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Please join me in welcoming our 3 *new hires* to the Paper Company family! \n\n *Robert California*, CEO \n\n *Ryan Howard*, Temp \n\n *Erin Hannon*, Receptionist "
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": ":pushpin: Do you have something to include in the daily report? Here's *how to submit content*."
				}
			]
		}
	    ]
    )


async def main(argv):
  
    #User input
    try:
      opts, args = getopt.getopt(argv,"hc:m:f:",["msg=","file="])
    except getopt.GetoptError:
        print('-c <channel> -m <message> -f <file>')
        return 0
    for opt, arg in opts:
        if opt == '-h':
            print('-u <url> -f <file>')
            return 0
        elif opt in ("-c", "--channel"):
            channel = arg
        elif opt in ("-m", "--msg"):
            message = arg
        elif opt in ("-f", "--file"):
            file_path = arg

    await publish_reports(channel,message, file_path)


    #handler = AsyncSocketModeHandler(app, c.SLACK_APP_TOKEN)
    #await handler.start_async()



if __name__ == "__main__":
    import asyncio
    print("Process Running....")
    asyncio.run(main(sys.argv[1:]))
