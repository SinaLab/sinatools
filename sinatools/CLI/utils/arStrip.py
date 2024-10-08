"""

About:
------
The arStrip command offers functionality to strip various elements from Arabic text using the SinaTools' `arStrip` utility. It provides flexibility to selectively strip diacritics, small diacritics, shaddah, digits, alif, and special characters.

Usage:
------
Below is the usage information that can be generated by running arStrip --help.

.. code-block:: none

    Usage:
        arStrip --text=TEXT [OPTIONS]
        arStrip --file "path/to/your/file.txt" [OPTIONS]

.. code-block:: none

    Options:
      --text TEXT
            The Arabic text that needs to be stripped.

      --file FILE
            File containing text to be stripped.

      --diacs BOOL [default=True]
            Indicates whether to strip diacritics.

      --small_diacs BOOL [default=True]
            Indicates whether to strip small diacritics.

      --shaddah BOOL [default=True]
            Indicates whether to strip shaddah.

      --digit BOOL [default=True]
            Indicates whether to strip digits.

      --alif BOOL [default=True]
            Indicates whether to strip alif.

      --special_chars BOOL [default=True]
            Indicates whether to strip special characters.

Examples:
---------
.. code-block:: none

    arStrip --text "مُختَبَر سينا لحوسبة اللغة!" --diacs=True --small_diacs=False --shaddah=True --digit=False --alif=False --special_chars=False    
    arStrip --file "path/to/your/file.txt" --diacs=True --small_diacs=False --shaddah=True --digit=False --alif=False --special_chars=False

"""

import argparse
from sinatools.utils.parser import arStrip
from sinatools.utils.readfile import read_file

def main():                             
    parser = argparse.ArgumentParser(description='Arabic text stripping tool using SinaTools')
    
    parser.add_argument('--text', type=str, help='Text to be stripped')
    parser.add_argument('--file', type=str, help='File containing text to be stripped')
    parser.add_argument('--diacs', type=bool, default=True, help='Whether to strip diacritics')
    parser.add_argument('--small_diacs', type=bool, default=True, help='Whether to strip small diacritics')
    parser.add_argument('--shaddah', type=bool, default=True, help='Whether to strip shaddah')
    parser.add_argument('--digit', type=bool, default=True, help='Whether to strip digits')
    parser.add_argument('--alif', type=bool, default=True, help='Whether to strip alif')
    parser.add_argument('--special_chars', type=bool, default=True, help='Whether to strip special characters')

    args = parser.parse_args()

    if args.file:
        text_content = read_file(args.file)
    elif args.text:
        text_content = args.text
    else:
        print("Either --text or --file argument must be provided.")
        return

    stripped_text = arStrip(text_content, diacs=args.diacs, small_diacs=args.small_diacs, 
                            shaddah=args.shaddah, digit=args.digit, alif=args.alif, special_chars=args.special_chars)
    
    print(stripped_text)

if __name__ == '__main__':
    main()

#arStrip --text "example text" --diacs=True
#arStrip --file "path/to/your/file.txt" --diacs=True