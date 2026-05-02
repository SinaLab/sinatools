"""
About:
------

The sentence_tokenizer command tokenizes text into sentences using the
SinaTools utility. It can split at dots, question marks, exclamation marks,
and new lines.

Usage:
------
Run sentence_tokenizer --help to show this usage information.

.. code-block:: none

    Usage:
        sentence_tokenizer --text=TEXT [options]
        sentence_tokenizer --file=FILE [options]

.. code-block:: none

    Options:
      --text TEXT
            Text to be tokenized into sentences.
      --file FILE
            File containing the text to be tokenized into sentences
      --dot
            Tokenize at dots.
      --new_line
            Tokenize at new lines.
      --question_mark
            Tokenize at question marks.
      --exclamation_mark
            Tokenize at exclamation marks.

Examples:
---------

.. code-block:: none

  sentence_tokenizer --text "Your text here." --dot --question_mark
  sentence_tokenizer --file "path/to/file.txt" --dot --question_mark

"""
import argparse

from sinatools.utils.tokenizer import sentence_tokenizer
from sinatools.utils.readfile import read_file


def main():
    parser = argparse.ArgumentParser(
        description='Sentence Tokenization using SinaTools'
    )

    # Adding arguments for the text, file, and tokenization options
    parser.add_argument(
        '--text',
        type=str,
        help='Text to be tokenized into sentences',
    )
    parser.add_argument(
        '--file',
        type=str,
        help='File containing the text to be tokenized into sentences',
    )
    parser.add_argument('--dot', action='store_true', help='Tokenize at dots')
    parser.add_argument(
        '--new_line',
        action='store_true',
        help='Tokenize at new lines',
    )
    parser.add_argument(
        '--question_mark',
        action='store_true',
        help='Tokenize at question marks',
    )
    parser.add_argument(
        '--exclamation_mark',
        action='store_true',
        help='Tokenize at exclamation marks',
    )

    args = parser.parse_args()

    # Check if either text or file is provided
    if args.text is None and args.file is None:
        print("Either --text or --file argument must be provided.")
        return

    text_content = args.text if args.text else " ".join(read_file(args.file))

    # Perform sentence tokenization
    sentences = sentence_tokenizer(
        text_content,
        dot=args.dot,
        new_line=args.new_line,
        question_mark=args.question_mark,
        exclamation_mark=args.exclamation_mark,
    )

    # Print each sentence in a new line
    for sentence in sentences:
        print(sentence)


if __name__ == '__main__':
    main()
