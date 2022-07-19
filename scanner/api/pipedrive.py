"""Connector for Popedrive API."""
import requests
import json
import os
import logging

from requests import Response

logger = logging.getLogger(__name__)

API_KEY = os.environ.get('PIPEDRIVE_API_KEY', 'eaf6cb3dec1ade10fc81ec9ad70175a9925bdaec')
API_URL = "https://api.pipedrive.com/v1"


def generate_body(due_date, due_time, subject, public_description, activity_type, busy_flag, done):
    """Generate body for request."""
    return {
        "due_date": due_date,
        "due_time": due_time,
        "public_description": public_description,
        "subject": subject,
        "type": activity_type,
        "busy_flag": busy_flag,
        "done": done
    }


class PostPipedriveActivity:
    """Simple connector superclass."""

    def __init__(self, due_date, due_time, subject, public_description, activity_type="Task", busy_flag=False, done=0):
        """Init connector."""
        self.body = generate_body(due_date, due_time, subject, public_description, activity_type, busy_flag, done)
        self.parameters = {"api_token": API_KEY}
        self.post_response = self.post_activity()

    def post_activity(self) -> Response:
        """Get response for request."""
        logger.info(f"Posting activity: {self.body}")
        return requests.post(f"{API_URL}/activities", params=self.parameters, json=self.body)

    def get_status_code(self) -> int:
        """Get response's status code."""
        return self.post_response.status_code

    def get_json(self) -> dict:
        """Convert response to dict."""
        return json.loads(self.post_response.text)
