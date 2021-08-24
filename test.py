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
from api_daily_price.tests.daily_tests import DailyTests

if __name__ == "__main__":
    unittest.main()