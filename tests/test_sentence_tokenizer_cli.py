import io
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from sinatools.CLI.utils import sentence_tokenizer


class SentenceTokenizerCliTest(unittest.TestCase):
    def test_text_argument_is_not_split_into_characters(self):
        argv = [
            "sentence_tokenizer",
            "--text",
            "One. Two?",
            "--dot",
            "--question_mark",
        ]

        stdout = io.StringIO()
        with patch.object(sys, "argv", argv):
            with redirect_stdout(stdout):
                sentence_tokenizer.main()

        self.assertEqual(stdout.getvalue().splitlines(), ["One.", "Two?"])


if __name__ == "__main__":
    unittest.main()
