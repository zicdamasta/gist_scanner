"""Connectors for GitHub API."""
import requests
import json
import os
import logging

from requests import Response

logger = logging.getLogger(__name__)

API_KEY = os.environ.get('GITHUB_API_KEY', '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')
API_URL = "https://api.github.com"


class GetGithubGists:
    """Simple get request to GitHub API."""

    def __init__(self, username, since=""):
        """Init connector."""
        self.username = username
        self.parameters = {"since": since}
        self.headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {API_KEY}"}
        self.response = self.get_response()

    def get_response(self) -> Response:
        """Get response for request."""
        logger.info(f"Getting gists for {self.username}")
        return requests.get(f"{API_URL}/users/{self.username}/gists", params=self.parameters, headers=self.headers)

    def get_status_code(self) -> int:
        """Get response's status code."""
        return self.response.status_code

    def get_json(self) -> dict:
        """Convert response to dict."""
        return json.loads(self.response.text)
