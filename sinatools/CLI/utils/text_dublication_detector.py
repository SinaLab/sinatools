import argparse
from sinatools.utils.text_dublication_detector import removal

def main():
    parser = argparse.ArgumentParser(description='Processes a CSV file of sentences to identify and remove duplicate sentences based on a specified threshold and cosine similarity. It saves the filtered results and the identified duplicates to separate files.')
    
    parser.add_argument('--csv_file', type=str, help='The path to the input CSV file that will be processed.')
    parser.add_argument('--column_name', type=str, help='The name of the column from which duplicates will be removed.')
    parser.add_argument('--final_file_name', type=str, help='The name of the output file that will contain the deduplicated results.')
    parser.add_argument('--deleted_file_name', type=str, help='The name of the output file that will contain the records that were identified as duplicates and removed.')
    parser.add_argument('--similarity_threshold', type=float, default=0.8, help='The similarity threshold for determining duplicates. Records with a similarity score above this value will be considered duplicates (default is 0.8).')

    args = parser.parse_args()

    if args.csv_file is None and args.column_name is None:
        print("Either --csv_file or --column_name argument must be provided.")
        return

    removal(args.csv_file, args.column_name, args.final_file_name, args.deleted_file_name, args.similarity_threshold)
    

if __name__ == '__main__':
    main()

# text_dublication_detector --csv_file "text.csv" --column_name "A" --final_file_name "Final.csv" --deleted_file_name "deleted.csv" --similarity_threshold 0.8