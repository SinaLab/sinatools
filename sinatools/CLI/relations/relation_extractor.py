"""
About:
------
The relation_extractor command is designed to extract events and their corresponding arguments (agents, locations, and dates) within a text using the SinaTools relation_extractor API.

Usage:
------
Below is the usage information that can be generated by running relation_extractor --help.

.. code-block:: none

    relation_extractor --text=TEXT [OPTIONS]
    relation_extractor --file=FILE [OPTIONS]

Options:
--------

.. code-block:: none

  --text TEXT
        The text from which events need to be extracted.

  --file FILE
        File containing the text from which events need to be extracted.

Examples:
---------

.. code-block:: none

  relation_extractor --text "Your Arabic text here"
  relation_extractor --file "path/to/your/file.txt"

"""

import argparse
from sinatools.relations.relation_extractor import event_argument_relation_extraction
from sinatools.utils.readfile import read_file

def main():
    parser = argparse.ArgumentParser(description='Relation Extraction using SinaTools')
      
    parser.add_argument('--text', type=str, help='The text from which events need to be extracted.')
    parser.add_argument('--file', type=str, help='File containing the text from which events need to be extracted.')

    args = parser.parse_args()

    if args.text is None and args.file is None:
        print("Error: Either --text or --file argument must be provided.")
        return

    input_text = args.text if args.text else " ".join(read_file(args.file))

    results = event_argument_relation_extraction(input_text)

    for result in results:
        print(result)

if __name__ == '__main__':
    main()
