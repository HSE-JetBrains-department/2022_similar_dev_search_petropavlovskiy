import unittest

from code_processing.enry_processor import get_language

from pathlib2 import Path


class EnryTest(unittest.TestCase):
    def test_get_language(self):
        path = str(Path(f"{Path().cwd}/enry_test.py"))
        self.assertEqual("python", get_language(path))
        print()


if __name__ == '__main__':
    unittest.main()
