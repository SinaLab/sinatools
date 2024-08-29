import argparse
from sinatools.morphology.ALMA_multi_word import ALMA_multi_word
import json
from sinatools.utils.readfile import read_file

def main():
    parser = argparse.ArgumentParser(description='Multi-Word Analysis using SinaTools')
    
    # Adding arguments for the multi-word input or file containing the multi-word input
    parser.add_argument('--multi_word', type=str, help='Multi-word text to be analyzed')
    parser.add_argument('--file', type=str, help='File containing the multi-word text to be analyzed')

    args = parser.parse_args()

    if args.multi_word is None and args.file is None:
        print("Error: Either --multi_word or --file argument must be provided.")
        return

    # Get the input either from the --multi_word argument or from the file specified in the --file argument
    multi_word_text = args.multi_word if args.multi_word else " ".join(read_file(args.file))

    # Perform multi-word analysis
    results = ALMA_multi_word(multi_word_text)
    
    # Print the results in JSON format
    print(json.dumps(results, ensure_ascii=False, indent=4))

if __name__ == '__main__':
    main()
#alma_multi_word --multi_word "Your multi-word text here"
#alma_multi_word --file "path/to/your/file.txt"
