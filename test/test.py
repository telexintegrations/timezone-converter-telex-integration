import pytest
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timezone
import pytz
import re
from dateparser import parse

# Import the FastAPI app
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

# Base URL for testing
BASE_URL = "http://localhost:8000"

# Fixture to create a test client
@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    return TestClient(app)

# Test the root endpoint
def test_get_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"status": "running"}

# Test the app-logo endpoint
def test_get_logo(client):
    response = client.get('/app-logo')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'image/png'

# Test the integration-json endpoint
def test_get_integration_json(client):
    response = client.get('/integration-json')
    assert response.status_code == 200
    integration_json = response.json()
    assert integration_json['data']['descriptions']['app_name'] == "Smart Timezone Converter"

# Test the convert-time endpoint with valid input
def test_convert_time_valid(client):
    request_data = {
        "message": "Sunday February 23, 2025 10:34 AM UTC",
        "settings": [
            {
                "label": "Timezones",
                "type": "dropdown",
                "default": "Africa/Lagos",
                "required": True
            }
        ],
        "channel_id": "test_channel"
    }
    response = client.post('/convert-time', json=request_data)
    assert response.status_code == 200
    result = response.json()
    assert 'message' in result
    assert 'Sunday, February 23, 2025 10:34 AM UTC (Sunday, February 23, 2025 11:34 AM WAT)' == result['message']

# Test the convert-time endpoint with invalid input (missing timezone)
def test_convert_time_invalid_missing_timezone(client):
    request_data = {
        "message": "Sunday February 23, 2025 10:34 AM UTC",
        "settings": [],
        "channel_id": "test_channel"
    }
    response = client.post('/convert-time', json=request_data)
    assert response.status_code == 400
    assert 'error' in response.json()['detail']
    assert response.json()['detail']['error'] == "User timezone setting is missing."

# Test the convert-time endpoint with invalid input (invalid timezone)
def test_convert_time_invalid_timezone(client):
    request_data = {
        "message": "Sunday February 23, 2025 10:34 AM UTC",
        "settings": [
            {
                "label": "Timezones",
                "type": "dropdown",
                "default": "Invalid/Timezone",
                "required": True
            }
        ],
        "channel_id": "test_channel"
    }
    response = client.post('/convert-time', json=request_data)
    assert response.status_code == 400
    assert 'error' in response.json()['detail']
    assert response.json()['detail']['error'] == "Invalid timezone: Invalid/Timezone"

# Test the convert-time endpoint with invalid input (no date in message)
def test_convert_time_invalid_no_date(client):
    request_data = {
        "message": "This is a test message without a date.",
        "settings": [
            {
                "label": "Timezones",
                "type": "dropdown",
                "default": "Africa/Lagos",
                "required": True
            }
        ],
        "channel_id": "test_channel"
    }
    response = client.post('/convert-time', json=request_data)
    assert response.status_code == 400
    assert 'error' in response.json()['detail']
    assert response.json()['detail']['error'] == "The message does not contain a valid date."

# Test the convert-time endpoint with invalid input (invalid message type)
# def test_convert_time_invalid_message_type(client):
#     request_data = {
#         "message": 12345,  # Invalid type, should be string
#         "settings": [
#             {
#                 "label": "Timezones",
#                 "type": "dropdown",
#                 "default": "Africa/Lagos",
#                 "required": True
#             }
#         ],
#         "channel_id": "test_channel"
#     }
#     response = client.post('/convert-time', json=request_data)
#     assert response.status_code == 400
#     assert 'error' in response.json()['detail']
#     assert response.json()['detail']['error'] == "Invalid message type. It must be a string."