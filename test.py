import unittest
import coloredlogs
import logging
import sys
from cashier_user.tests.user_tests import Usertests
from cashier_product.tests.product_tests import Producttests


coloredlogs.install()

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    unittest.main()