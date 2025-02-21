from fastapi import FastAPI, Request,HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import pytz
import os
from dotenv import load_dotenv
import re
from dateparser import parse


app = FastAPI()

origins =[
    'https://ping.telex.im',
    'https://telex.im',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
ALL_TIMEZONES = list(pytz.all_timezones)
IMAGE_PATH='img/logo.png'

class TimeConversionRequest(BaseModel):
    message: str
    class Setting(BaseModel):
        label: str
        type: str
        default: str
        required: bool

    settings: list[Setting]
    channel_id: str

class TimeConversionResponse(BaseModel):
    converted_time: str
@app.get('/')
def gethome():
    return {"status":"running"}


@app.get('/app-logo')
async def get_logo():
    if os.path.exists(IMAGE_PATH):
        return FileResponse(IMAGE_PATH, media_type='image/png')
    return {'error':'image not found'}


@app.get('/integration-json')
def get_integration_json(request:Request):
    BASE_URL = str(request.base_url).rstrip("/")
    integration_json = {
  "data": {
    "date": {
      "created_at": "2025-02-20",
      "updated_at": "2025-02-20"
    },
    "descriptions": {
      "app_description": "This modifier automatically detects time mentions in messages and converts them to the recipient’s local time zone. It helps users avoid confusion when scheduling meetings, events, or deadlines across different time zones.",
      "app_logo": f'{BASE_URL}/app-logo',
      "app_name": "Smart Timezone Converter",
      "app_url": BASE_URL,
      "background_color": "#fff"
    },
    "integration_category": "Task Automation",
    "integration_type": "modifier",
    "is_active": False,
    # "output": [
    #   {
    #     "label": "output_channel_1",
    #     "value": True
    #   },
    #   {
    #     "label": "output_channel_2",
    #     "value": false
    #   }
    # ],

    "key_features": [
      'The integration scans messages for any explicit time mentions ("Sunday February 23, 2025 10:34 AM UTC").',
      "The day e.g (sunday, monday is optional)",
      "The date sent must be specified ONLY in UTC as the converted time is UTC-based conversion",
      "It modifies the message by appending the converted time in the recipient’s local time zone."
    ],
    # "permissions": {
    #   "monitoring_user": {
    #     "always_online": True,
    #     "display_name": "Performance Monitor"
    #   }
    # },
    "settings": [
      {
        "label": "Timezones",
        "type": "dropdown",
        "options": ALL_TIMEZONES,
        "description":"user will select their timezone with this",
        "required": True,
        "default": "Africa/lagos",
      }
    ],
    "target_url":f'{BASE_URL}/convert-time'
  }
}
    return integration_json

# import re
# import pytz
# from datetime import datetime, timezone
# from dateutil.parser import parse
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List, Dict, Any

# app = FastAPI()

# # Define the request body model
# class Setting(BaseModel):
#     label: str
#     type: str
#     default: str
#     required: bool

# class TimeConversionRequest(BaseModel):
#     message: str
#     settings: List[Setting]
#     channel_id: str


def process_time_conversion(request: TimeConversionRequest):
    """
    Process the request body and convert the detected time to the user's timezone.
    """
    try:
        # Validate message type
        if not isinstance(request.message, str):
            return {"error": "Invalid message type. It must be a string."}

        # Regex pattern to detect datetime
        pattern = r'(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)?,?\s*' \
                  r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s' \
                  r'\d{1,2},\s\d{4}\s\d{1,2}:\d{2}\s?(?:AM|PM)(?:\s[A-Z]{2,4})?'

        match = re.search(pattern, request.message)
        if not match:
            return {"error": "The message does not contain a valid date."}

        # Parse the matched date string
        date_time = parse(match.group())

        # Extract user timezone
        if not request.settings or not request.settings[0].type:
            return {"error": "User timezone setting is missing."}

        user_timezone = request.settings[0].default

        # Validate timezone
        if user_timezone not in pytz.all_timezones:
            return {"error": f"Invalid timezone: {user_timezone}"}

        # Convert to UTC and then to user timezone
        utc_time = date_time.replace(tzinfo=timezone.utc)
        user_time = utc_time.astimezone(pytz.timezone(user_timezone)).strftime("%A, %B %d, %Y %I:%M %p %Z")

        # Replace in message
        to_replace_date = f'{date_time.strftime("%A, %B %d, %Y %I:%M %p %Z")} ({user_time})'
        returned_message = re.sub(pattern, to_replace_date, request.message)

        return {"message": returned_message}
    except Exception as e:
        return {"error": str(e), 'status': 'failed'}


@app.post("/convert-time")
async def convert_time(request: TimeConversionRequest):
    result = process_time_conversion(request)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result



# @app.post("/convert-time")
# async def convert_time(request:TimeConversionRequest):

#     try:
#         if type(request.message) != str:
#             return {"error": "Invalid message type"}
#         # Parse the input time
#         pattern = r'(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)?,?\s*?(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}\s\d{1,2}:\d{2}\s?(?:AM|PM)(?:\s[A-Z]{2,4})?'

#         match = re.search(pattern, request.message)
#         if not match:
#             return {"error": "The message does not contain any date"}
#         date_time = parse(match.group())
#         user_timezone = request.settings[0].type
#         utc_time = date_time.replace(tzinfo=timezone.utc)
#         user_time = utc_time.astimezone(pytz.timezone(user_timezone)).strftime("%A, %B %d, %Y %I:%M %p %Z")
#         to_replace_date = f'{date_time} ({user_time})'
#         returned_message = re.sub(pattern,to_replace_date,request.message)
         
#         return {"message": returned_message}
#     except Exception as e:
#         return {"error": str(e),'status':'cant tell'}

