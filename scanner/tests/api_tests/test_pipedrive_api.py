"""Tests for Pipedrive API."""
import pytest
from scanner.api.pipedrive import PostPipedriveActivity


class TestGithubApi:
    """Tests for Pipedrive API."""

    def test_post_activity_response_equals_201(self):
        """Check for response 201."""
        activity = PostPipedriveActivity("2020-01-01", "12:00", "Test", "Test", "Task", False, 0)
        assert activity.get_status_code() == 201
