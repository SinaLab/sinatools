"""
About:
------
The remove_punctuation command performs delete punctuation marks from the input text.

Usage:
------
Below is the usage information that can be generated by running remove_punctuation --help.

.. code-block:: none

    Usage:
        remove_punctuation --text=TEXT
        remove_punctuation --file "path/to/your/file.txt"

Examples:
---------
.. code-block:: none

    remove_punctuation --text "te%s@t...!!?"    
    remove_punctuation --file "path/to/your/file.txt"
"""

import argparse
from sinatools.utils.parser import remove_punctuation
#from sinatools.utils.parser import read_file
#from sinatools.utils.parser import write_file


def main():
    parser = argparse.ArgumentParser(description='remove punctuation marks from the text')

    parser.add_argument('--text',required=True,help="input text")
   # parser.add_argument('myFile', type=argparse.FileType('r'),help='Input file csv')
    args = parser.parse_args()
    result = remove_punctuation(args.text)
 
    print(result)
    if __name__ == '__main__':
        main()

