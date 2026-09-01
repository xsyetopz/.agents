import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from example_core import greeting


class GreetingTest(unittest.TestCase):
    def test_trims_name(self):
        self.assertEqual("Hello, editor.", greeting(" editor "))


if __name__ == "__main__":
    unittest.main()
