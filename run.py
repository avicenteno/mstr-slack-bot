import logging
import sys
import getopt

logging.basicConfig(level=logging.DEBUG)

import os
import json

from pathlib import Path
from dotenv import load_dotenv

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

import constants as c

#Get environment constants
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


# Install the Slack app and get xoxb- token in advance
app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])

@app.command("/hello-socket-mode")
async def hello_command(ack, body):
    user_id = body["user_id"]
    await ack(f"Hi <@{user_id}>!")


@app.event("app_mention")
async def event_test(event, say):
    await say(f"Hi there, <@{event['user']}>!")

async def upload_file(channel):
	response = await app.client.files_upload(
        channels=channel,
        initial_comment="My initial comment",
        file=os.environ["FILE_TO_UPLOAD"]
    )
	return response

async def publish_reports(channel, json_string):

	response = await asyncio.wait_for(app.client.files_upload(
        channels=channel,
        initial_comment="My initial comment",
        file="data/fiole.xlsx"
    ), 120.0)
	
	channel_id = list(response['file']['shares']['public'].keys())[0]
	print(channel_id)
	ts = response['file']['shares']['public'][channel_id][0]['ts']

	print(ts)

	await app.client.chat_update(
        channel=channel_id,
        text='text',
		ts=ts,
        blocks= json_string['blocks']
    )

async def update_chat(channel, json_string,result):
    
	ts = result['file']['shares']['public'][channel][0]['ts']

	await app.client.chat_update(
        channel=channel,
        text='text',
		ts=ts,
        blocks= json_string['blocks']
    )

async def postMessage(channel,json_string):
	await app.client.chat_postMessage(
        channel=channel,
        text='text',
        blocks= json_string['blocks']
    )
	
async def main(argv):

	try:
		opts, args = getopt.getopt(argv,"hc:m:",["channel=","msg="])
	except getopt.GetoptError:
		print('-c <channel> -m <message file>')
		return 0
    	
	for opt, arg in opts:
		if opt == '-h':
			print('-c <channel> -m <message file>')
			return 0
		elif opt in ("-c", "--channel"):
			channel = arg
		elif opt in ("-m", "--msg"):
			message_file = arg
		

	# Open the slack message file
	with open(message_file) as file:
		# Load its content and make a new dictionary
		slack_message = json.load(file)


	#await update_chat(channel, slack_message, result)
	#await publish_reports(channel, slack_message)
	await postMessage(channel, slack_message)
	#handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    #await handler.start_async()

if __name__ == "__main__":
    import asyncio
    print("Process Running....")
    asyncio.run(main(sys.argv[1:]))
