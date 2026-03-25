import unittest
from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parent))
from exercise_1 import word_frequency  # noqa: E402


class TestWordFrequency(unittest.TestCase):
    def test_lowercases_words(self) -> None:
        self.assertEqual(word_frequency("Python python PYTHON")["python"], 3)

    def test_ignores_punctuation(self) -> None:
        result = word_frequency("hi, hi! hi? (hi)")
        self.assertEqual(result["hi"], 4)

    def test_handles_newlines(self) -> None:
        result = word_frequency("a\na\na")
        self.assertEqual(result["a"], 3)

    def test_splits_on_hyphen(self) -> None:
        result = word_frequency("data-driven data-driven")
        self.assertEqual(result["data"], 2)
        self.assertEqual(result["driven"], 2)

    def test_empty_string(self) -> None:
        self.assertEqual(word_frequency(""), {})


if __name__ == "__main__":
    unittest.main()

