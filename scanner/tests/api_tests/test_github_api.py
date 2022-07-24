"""Tests for GitHub API."""
import pytest
from scanner.api.github import GetGithubGists


class TestGithubApi:
    """Tests for GitHub API."""

    def test_get_gists_for_user_response_equals_200(self):
        """Check for response 202."""
        gists = GetGithubGists("zicdamasta")
        assert gists.get_status_code() == 200

    def test_get_gists_for_wrong_user_response_equals_404(self):
        """Check for response 404 if user does not exist."""
        gists = GetGithubGists("wrong_user")
        assert gists.get_status_code() == 404

    def test_get_gists_response_has_all_needed_parameters(self):
        """Check if needed parameters exists."""
        gists = GetGithubGists("zicdamasta")
        params = ["url", "files", "owner", "html_url", "id"]
        response = gists.response
        for param in params:
            if param not in response.text:
                pytest.fail(
                    f"There is no {param} in get_data (got: {response.text})"
                )

