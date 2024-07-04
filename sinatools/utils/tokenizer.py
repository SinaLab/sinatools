import os
import csv
from sinatools.utils.tokenizers_words import simple_word_tokenize

def remove_empty_values(sentences):
    return [value for value in sentences if value != '']


def sentence_tokenizer(text, dot=True, new_line=True, question_mark=True, exclamation_mark=True):
    """
    This method tokenizes a text into a set of sentences based on the selected separators, including the dot, new line, question mark, and exclamation mark.

    Args:
        text (:obj:`str`): Arabic text to be tokenized.
        dot (:obj:`str`): flag to split text based on Dot (default is True).
        new_line (:obj:`str`): flag to split text based on new_line (default is True).
        question_mark (:obj:`str`): flag to split text based on question_mark (default is True).
        exclamation_mark (:obj:`str`): flag to split text based on exclamation_mark (default is True).

    Returns:
        :obj:`list`: list of sentences.

    **Example:**

    .. highlight:: python
    .. code-block:: python

        from sinatools.utils import tokenizer
        sentences = tokenizer.sentence_tokenizer("مختبر سينا لحوسبة اللغة والذكاء الإصطناعي. في جامعة بيرزيت.", dot=True, new_line=True, question_mark=True, exclamation_mark=True)
        print(sentences)

        #output
        ['مختبر سينا لحوسبة اللغة والذكاء الإصطناعي.', 'في جامعة بيرزيت.']
    """
    separators = []
    split_text = [text]
    if new_line==True:
        separators.append('\n')
    if dot==True:
        separators.append('.')
    if question_mark==True:
        separators.append('?')
        separators.append('؟')
    if exclamation_mark==True:
        separators.append('!')
    
    for sep in separators:
        new_split_text = []
        for part in split_text:
            tokens = part.split(sep)
            tokens_with_separator = [token + sep for token in tokens[:-1]]
            tokens_with_separator.append(tokens[-1].strip())
            new_split_text.extend(tokens_with_separator)
        split_text = new_split_text
    
    split_text = remove_empty_values(split_text)    
    return split_text

def corpus_tokenizer(dir_path, output_csv, row_id = 1, global_sentence_id = 1):
    """
    This method receives a directory and tokenizes all files within the input directory, as well as all files within subdirectories within the main directory. The results are then stored in a CSV file.

    Args:
        dir_path (:obj:`str`): The path of the directory containing multiple Arabic txt files.
        output_csv (:obj:`str`): The name of the output CSV file, which will be generated in the current directory where this function is used.
        row_id (:obj:`int`): Specifies the row_id you wish to start with; the default value is 1.
        global_sentence_id (:obj:`int`): Specifies the global_sentence_id you wish to start with; the default value is 1.

    Returns:
        csv file (:obj:`str`): The CSV file contains the following fields: 
            * Row_ID (primary key, unique for all records in outputfile)
            * Docs_Sentence_Word_ID (DirectoryName_FileName_GlobalSentenceID_SentenceID_WordPosition)
            * GlobalSentenceID (Integer, a unique identifier for each sentence in the entire file)
            * SentenceID (Integer, a unique identifier for each file within the CSV file)
            * Sentence (Generated text that forms a sentence)
            * Word Position (Integer, the position of each word within the sentence)
            * Word (Each row contains a word from the generated sentence).

    **Example:**

    .. highlight:: python
    .. code-block:: python

        from sinatools.utils import tokenizer
        output = tokenizer.corpus_tokenizer(dir_path="History", output_csv="ouputFile.csv", row_id = 1, global_sentence_id = 1)

        #output
        # csv file called: ouputFile.csv 
        # For example, if the 'History' directory contains 2 files named 'h1.txt' and 'h2.txt'. 
        # The output file will contain: 
        # Row_ID, Docs_Sentence_Word_ID, Global Sentence ID, Sentence ID, Sentence, Word Position, Word
        # 1,History_h1_1_1_1,1,1,الطيور الضارة ومكافحتها,1,الطيور
        # 2,History_h1_1_1_2,1,1,الطيور الضارة ومكافحتها,2,الضارة
        # 3,History_h1_1_1_3,1,1,الطيور الضارة ومكافحتها,3,ومكافحتها
        # 4,History_h2_2_1_1,1,1,بشكل عام,1,بشكل
        # 5,History_h2_2_1_2,1,1,بشكل عام,2,عام
    """    
    row_id = row_id - 1
    global_sentence_id = global_sentence_id - 1
    with open(output_csv, 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['Row_ID', 'Docs_Sentence_Word_ID', 'Global Sentence ID', 'Sentence ID', 'Sentence', 'Word Position', 'Word']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding="utf-8") as f:
                        content = f.read()
                        sentences = sentence_tokenizer(content, dot=True, new_line=True, question_mark=False, exclamation_mark=False)
                        for sentence_id, sentence in enumerate(sentences, start=1):
                            words = simple_word_tokenize(sentence)
                            global_sentence_id += 1
                            for word_pos, word in enumerate(words, start=1):
                                row_id += 1
                                dir_name = os.path.basename(root)
                                doc_sentence_filename = file.split(".txt")[0]
                                docs_sentence_word_id = f"{dir_name}_{doc_sentence_filename}_{global_sentence_id}_{sentence_id}_{word_pos}"
                                writer.writerow({'Row_ID': row_id,
                                                 'Docs_Sentence_Word_ID': docs_sentence_word_id,
                                                 'Global Sentence ID': global_sentence_id,
                                                 'Sentence ID': sentence_id,
                                                 'Sentence': sentence,
                                                 'Word Position': word_pos,
                                                 'Word': word})
