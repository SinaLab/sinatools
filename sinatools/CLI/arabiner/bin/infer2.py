import os
import csv
from sinatools.utils.sentence_tokenizer import sent_tokenize
from sinatools.morphology.tokenizers_words import simple_word_tokenize
import pandas as pd

"""
CSV NER Tagging Tool

Usage:
------
Run the script with the following command:

arabi_ner2  input.csv --text-columns "TextColumn1,TextColumn2" --additional-columns "Column3,Column4" --output-csv output.csv
"""

import argparse
import pandas as pd
from sinatools.utils.sentence_tokenizer import sent_tokenize
from sinatools.morphology.tokenizers_words import simple_word_tokenize
from sinatools.arabiner.bin.infer import ner

def infer(sentence):
    output = ner(sentence)
    return [word[1] for word in output]


def corpus_tokenizer(input_csv, output_csv, text_column, additional_columns, row_id, global_sentence_id):
    print(input_csv, output_csv, text_column, additional_columns)
    row_id = row_id - 1
    global_sentence_id = global_sentence_id - 1
    fieldnames = ['Row_ID', 'Docs_Sentence_Word_ID', 'Global Sentence ID', 'Sentence ID', 'Sentence', 'Word Position', 'Word', 'Ner tags']
    for additional_column in additional_columns:
        fieldnames.append(additional_column)

    with open(output_csv, 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        df = pd.read_csv(input_csv)
        for index, row in df.iterrows():            
            sentences = sent_tokenize(row[text_column], dot=True, new_line=True, question_mark=False, exclamation_mark=False)
            for sentence_id, sentence in enumerate(sentences, start=1):
                words = simple_word_tokenize(sentence)
                global_sentence_id += 1

                tags = infer(sentence) 
                for word_position, word in enumerate(words, start=1):
                    row_id += 1
                    doc_sentence_filename = input_csv.split(".csv")[0]
                    docs_sentence_word_id = f"{doc_sentence_filename}_{global_sentence_id}_{sentence_id}_{word_position}"
                    output_dic = {'Row_ID': row_id, 'Docs_Sentence_Word_ID': docs_sentence_word_id, 'Global Sentence ID': global_sentence_id, 'Sentence ID': sentence_id, 
                                  'Sentence': sentence, 'Word Position': word_position, 'Word': word, 'Ner tags':tags[word_position-1]}
                    for additional_column in additional_columns:
                        output_dic[additional_column] = row[additional_column]

                    writer.writerow(output_dic)                                                                                                                                                                                                                                          

def main():
    parser = argparse.ArgumentParser(description="CSV NER Tagging Tool")
    parser.add_argument("--input_csv", help="Path to the input CSV file")
    parser.add_argument("--text_column", required=True,
                        help="Column index in the CSV file to apply NER tagging")
    parser.add_argument("--additional_columns", nargs='*', default=[],
                        help="Additional column indexes to retain in the output seperated by , ")
    parser.add_argument("--output_csv", default="output.csv",
                        help="Path to the output CSV file")
    parser.add_argument("--row_id", default="1",
                    help="Row id to starts with")
    parser.add_argument("--global_sentence_id", default="1",
                    help="global_sentence_id to starts with")

    args = parser.parse_args()
    corpus_tokenizer(args.input_csv, args.output_csv, args.text_column, args.additional_columns, int(args.row_id), int(args.global_sentence_id))


if __name__ == "__main__":
    main()



