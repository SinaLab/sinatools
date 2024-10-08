"""
About:
------
The jaccard tool computes the Jaccard similarity between two sets of strings. The Jaccard similarity is the size of the intersection divided by the size of the union of the sample sets. It provides a measure of similarity between two sets.

Usage:
------
Below is the usage information that can be generated by running jaccard_similarity --help.

.. code-block:: none

    Usage:
        jaccard_similarity --list1="WORD1, WORD2"  --list2="WORD1,WORD2" --delimiter="DELIMITER"  --selection="SELECTION"  [OPTIONS]
        
        jaccard_similarity --file1=File1 --file2=File2 --delimiter="DELIMITER"  --selection="SELECTION"  [OPTIONS]

.. code-block:: none

    Options:
      --list1 WORD1 WORD2 ...
            First list of strings (delimiter-separated).
      --list2 WORD1 WORD2 ...
            Second list of strings (delimiter-separated).
      --file1
            First file containing the first set of words
      --file2      
            Second file containing the second set of words
      --delimiter 
            Denote the bounds between regions in a text
      --selection
            Selecting the Jaccard function type, which can be one of the following options: 'jaccardAll', 'intersection', 'union', or 'similarity'.
      --ignoreAllDiacriticsButNotShadda 
            If this option is selected, the comparison will be between two lists after ignoring all diacritics from the lists but keeping the shadda.
      --ignoreShaddaDiacritic        
            If this option is selected, the comparison will be between two lists after ignoring diacritics (shadda) from lists of strings.

Examples:
---------

.. code-block:: none

      jaccard_similarity --list1 "word1,word2"  --list2 "word1, word2" --delimiter ","  --selection "jaccardAll" --ignoreAllDiacriticsButNotShadda --ignoreShaddaDiacritic  
      
      jaccard_similarity --file1 "path/to/your/file1.txt"  --file2 "path/to/your/file2.txt" --delimiter ","  --selection "jaccardAll" --ignoreAllDiacriticsButNotShadda --ignoreShaddaDiacritic  

"""

import argparse
from sinatools.utils.similarity import get_jaccard
from sinatools.utils.readfile import read_file


def main():
    parser = argparse.ArgumentParser(description='Compute Jaccard similarity between two sets of strings')
    
    # Adding optional arguments for the two sets and the files
    parser.add_argument('--delimiter', type=str, help='denote the bounds between regions in a text')
    parser.add_argument('--list1', type=str, help='First string (delimiter-separated)')
    parser.add_argument('--list2', type=str, help='Second string (delimiter-separated)')
    parser.add_argument('--file1', type=str, help='File containing the first set of words')
    parser.add_argument('--file2', type=str, help='File containing the second set of words')
    parser.add_argument('--selection', type=str, help='selecting jaccard function type')
    parser.add_argument('--ignoreAllDiacriticsButNotShadda', action='store_true', help='Ignore all diacritics but not shadda')
    parser.add_argument('--ignoreShaddaDiacritic', action='store_true', help='Ignore shadda diacritic')
    
 
    args = parser.parse_args()

    if args.file1 and args.file2:
        set1 = " ".join(read_file(args.file1))
        set2 = " ".join(read_file(args.file2))
    elif args.list1 is not None and args.list2 is not None:
        set1 = args.list1
        set2 = args.list2
    else:
        print("Either --file1 and --file2 arguments or both --set1 and --set2 arguments must be provided.")
        return

    similarity = get_jaccard(args.delimiter, set1, set2, args.selection, args.ignoreAllDiacriticsButNotShadda, args.ignoreShaddaDiacritic)
    
    print("Jaccard Result:", similarity)

if __name__ == '__main__':
    main()

# jaccard_similarity --list1 "word1,word2"  --list2 "word1, word2" --delimiter ","  --selection "jaccardAll" --ignoreAllDiacriticsButNotShadda --ignoreShaddaDiacritic  
# jaccard_similarity --file1 "path/to/your/file1.txt" --file2 "path/to/your/file2.txt" --delimiter ","  --selection "jaccardAll" --ignoreAllDiacriticsButNotShadda --ignoreShaddaDiacritic  