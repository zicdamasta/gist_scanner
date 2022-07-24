"""Simple integration tests for the scanner module."""
import os


import pytest
from scanner.scan_users import scan_users


class TestIntegration:
    """Integration test"""

    def test_scan_user_and_check_output_file(self):
        """Runs the scanner and checks if the output file is created."""
        user_list = ["zicdamasta"]
        scan_users(user_list, hours_interval=0, minutes_interval=0)
        # check that ../output/zicdamasta.txt exists
        assert os.path.exists("output/user/zicdamasta.txt")

