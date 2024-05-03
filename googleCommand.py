import os
import json
import google.auth
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.assistant.library import Assistant
from google.assistant.library.event import EventType

# Path to the JSON key file downloaded during setup
KEY_FILE = '\\googleKey\\KEY.json'

def send_command(command):
    # Load the credentials from the JSON key file
    credentials = Credentials.from_service_account_file(KEY_FILE)
    scoped_credentials = credentials.with_scopes(
        ['https://www.googleapis.com/auth/assistant-sdk-prototype']
    )

    with Assistant(scoped_credentials, 'your_device_id') as assistant:
        assistant.send_text_query(command)

# Example commands
turn_on_light_command = "Turn on the light"
turn_off_light_command = "Turn off the light"

# Send command to turn on the light
send_command(turn_on_light_command)

# Send command to turn off the light
send_command(turn_off_light_command)
