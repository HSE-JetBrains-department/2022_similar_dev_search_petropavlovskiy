import unittest

from pathlib2 import Path

from src.code_processing.enry_processor import get_language


class EnryTest(unittest.TestCase):
    def test_get_language(self):
        path = str(Path(f"{Path().cwd}/enry_test.py"))
        self.assertEqual("python", get_language(path))
        print()


if __name__ == '__main__':
    unittest.main()
