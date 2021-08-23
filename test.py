import coloredlogs
import logging
import sys
import unittest

from api_user.tests.user_tests import UserTests

coloredlogs.install()

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

if __name__ == "__main__":
    unittest.main()