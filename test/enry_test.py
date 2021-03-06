import unittest

from info_processing.code_processing.enry_processor import get_language

from pathlib2 import Path


class EnryTest(unittest.TestCase):
    def test_get_language(self):
        path = str(Path(f"{Path().cwd}/enry_test.py"))
        path_to_file = str(Path(f"{Path().cwd}/test_files/qwerty.java"))
        self.assertEqual("python", get_language(path))
        self.assertEqual("java", get_language(path_to_file))


if __name__ == '__main__':
    unittest.main()
