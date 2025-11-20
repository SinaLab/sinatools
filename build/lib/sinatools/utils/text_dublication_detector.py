
import pandas as pd
import re
import math
from collections import Counter
from sinatools.utils.parser import arStrip
from sinatools.utils.parser import remove_punctuation

def validator(sentence, max_tokens=500):
    tokens = len(sentence.split())
    if tokens > max_tokens:
        return f"Invalid: Sentence has {tokens} tokens, which exceeds the maximum allowed ({max_tokens})."
    else:
        return "Valid"


def removal(csv_file, columnName, finalFileName, deletedFileName, similarityThreshold=0.8):
    """
    This method is designed to identify dublicate text in a given corpora/text. It processes a CSV file of sentences to identify and remove duplicate sentences based on a specified threshold. We used cosine similarity to measure similarity between words and sentences. The method saves the filtered results and the identified duplicates to separate files.
    
    Args:
        csv_file (:obj:`str`) – The CSV file contains Arabic text that needs to be cleaned.
        column_name (:obj:`str`) – This is the name of the column containing the text that needs to be checked for duplicate removal.
        final_file_name (:obj:`str`) – This is the name of the CSV file that will contain the data after duplicate removal.        
        deleted_file_name (:obj:`str`) – This is the name of the file that will contain all the duplicate records that are deleted.        
        similarity_threshold (:obj:`float`) – This is a floating-point number. The default value is 0.8, indicating the percentage of similarity that the function should use when deleting duplicates from the text column.    
    
    Returns:
        csv files.
    
    **Example:**
    
    .. highlight:: python
    .. code-block:: python
    
        from sinatools.utils.text_dublication_detector import removal
        removal("/path/to/csv/file1", "sentences", "/path/to/final/file", "/path/to/deleted/file", 0.8)
    """

    # Read CSV file
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        return "Error: CSV file not found."

    # Check if the specified column exists
    if columnName not in df.columns:
        return f"Error: Column '{columnName}' does not exist in the CSV file."

    # Create an empty DataFrame to store the final results
    finalDf = pd.DataFrame(columns=df.columns)

    # Create temporary DataFrames for deleted sentences
    deletedSentencesDf = pd.DataFrame(columns=df.columns)

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        currentSentence = str(row[columnName])

        # Call the validator function for each sentence
        #validationResult = validator(currentSentence)
        validationResult = "Valid"

        if validationResult == "Valid":
            # Check cosine similarity with all sentences in the final DataFrame
            isDuplicate = False
            DublicatedRow = ""
            for _, finalRow in finalDf.iterrows():
                finalSentence = str(finalRow[columnName])
                currentSentence = remove_punctuation(arStrip(currentSentence, diacs = False, smallDiacs = False, shaddah = False,  digit = True, alif = False, specialChars = True))
                finalSentence = remove_punctuation(arStrip(finalSentence, diacs = False, smallDiacs = False, shaddah = False,  digit = True, alif = False, specialChars = True))
                if currentSentence != "" and finalSentence != "":
                   similarity = calculateCosineSimilarity(currentSentence, finalSentence)

                   if similarity >= similarityThreshold:
                       isDuplicate = True
                       DublicatedRow = finalSentence
                       print("DublicatedRow : ", DublicatedRow)
                       break

            if not isDuplicate:
                # If not a duplicate, add the sentence to the final DataFrame
                finalDf = finalDf.append(row, ignore_index=True)
            else:
                # If a duplicate, add the sentence to the deleted sentences DataFrame
                #deletedSentencesDf = deletedSentencesDf.append(row, ignore_index=True)
                deletedSentencesDf = deletedSentencesDf.append({**row, 'Dublicated': DublicatedRow}, ignore_index=True)
        else:
            # If validation fails, return the error message
            return validationResult

    # Save the final results to CSV files
    finalDf.to_csv(finalFileName, index=False)
    deletedSentencesDf.to_csv(deletedFileName, index=False)


def calculateCosineSimilarity(sentence1, sentence2):
    vector1 = textToVector(sentence1)
    vector2 = textToVector(sentence2)
    cosine = getCosine(vector1, vector2)
    
    return cosine


def getCosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def textToVector(text):
    WORD = re.compile(r"\w+")
    words = WORD.findall(text)
    return Counter(words)


# columnName = "Message"
# csvFile = "Arabic-Oct7-Feb12.csv"
# similarityThreshold = 0.8 
# finalFileName = "Arabic-Oct7-Feb12FINAL.csv" 
# deletedFileName = "Arabic-Oct7-Feb12DeletedSent.csv"

# result = removal(csvFile, columnName, finalFileName, deletedFileName, similarityThreshold)
# print(result)
