import coloredlogs
import logging
import sys
import unittest

coloredlogs.install()

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

from api_user.tests.user_test import UserTests

if __name__ == "__main__":
    unittest.main()