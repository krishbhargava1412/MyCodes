import unittest
from PIL import Image
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from util import read_license_plate, license_complies_format, format_license

class TestReadLicensePlate(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
