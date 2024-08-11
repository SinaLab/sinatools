import re
from sinatools.utils.tokenizers_words import simple_word_tokenize
from sinatools.utils.parser import arStrip
from sinatools.utils.charsets import AR_CHARSET, AR_DIAC_CHARSET
from sinatools.DataDownload.downloader import get_appdatadir
from . import dictionary

_IS_AR_RE = re.compile(u'^[' + re.escape(u''.join(AR_CHARSET)) + u']+$')

def find_solution(token, language, flag):    
    if token in dictionary.keys():
        resulted_solutions = [] 
        solutions = dictionary[token]
        if flag == '1':
           solutions = [solutions[0]]
        for solution in solutions:
            # token, freq, lemma, lemma_id, root, pos
            resulted_solutions.append([token, solution[0], solution[1], solution[2], solution[3], solution[4]])
        return resulted_solutions
    else:
        return []



def analyze(text, language ='MSA', task ='full', flag="1"):
   """
    This method processes an input text and returns morphological analysis for each token within the text, based on the specified language, task, and flag. You can try the demo online. See article for more details
    
        * If the task is lemmatization, the morphological solution includes only the lemma_id, lemma, token, and token frequency.
        * If the task is pos, the morphological solution includes only the part-of-speech, token, and token frequency.
        * If the task is root, the morphological solution includes only the root, token, and token frequency.
        * If the task is full, the morphological solution includes the lemma_id, lemma, part-of-speech, root, token, and token frequency.    
     
    Parameters:
        text (:obj:`str`): The Arabic text to be morphologically analyzed.
        language (:obj:`str`): Currently, only Modern Standard Arabic (MSA) is supported.
        task (:obj:`str`): The task to filter the results by. Options are [lemmatization, pos, root, full]. The default task if not specified is `full`.
        flag (:obj:`str`):  The flag to filter the returned results. If the flag is `1`, the solution with the highest frequency will be returned. If the flag is `*`, all solutions will be returned, ordered descendingly, with the highest frequency solution first. The default flag if not specified is `1`.
         
    Returns:
        list (:obj:`list`): A list of JSON objects, where each JSON could be contains:
            token: The token from the original text.
            lemma: The lemma of the token (Lemmas from the Qabas lexicon).
            lemma_id: The id of the lemma (qabas lemma ids).
            pos: The part-of-speech of the token (see Qabas POS tags).
            root: The root of the token (qabas roots).
            frequency: The frequency of the token (see section 3 in article).        

    **Example:**

     .. highlight:: python
     .. code-block:: python
     
        from sinatools.morphology.morph_analyzer import analyze
    
        #Return the morpological solution for each token in this text
        #Example: task = full 
        analyze('ذهب الولد الى المدرسة')

        [{ 
            "token": "ذهب",
            "lemma": "ذَهَبَ",
            "lemma_id": "202001617",
            "root": "ذ ه ب",
            "pos": "فعل ماضي",
            "frequency": "82202"
          },{ 
            "token": "الولد",
            "lemma": "وَلَدٌ",
            "lemma_id": "202003092",
            "root": "و ل د",
            "pos": "اسم",
            "frequency": "19066"
          },{ 
            "token": "إلى",
            "lemma": "إِلَى",
            "lemma_id": "202000856",
            "root": "إ ل ى",
            "pos": "حرف جر",
            "frequency": "7367507"
          },{ 
            "token": "المدرسة",
            "lemma": "مَدْرَسَةٌ",
            "lemma_id": "202002620",
            "root": "د ر س",
            "pos": "اسم",
            "frequency": "145285"
        }]

   """

   output_list = []

   tokens = simple_word_tokenize(text)

   for token in tokens:
         result_token = []
         token = arStrip(token , False , True , False , False , False , False) 
         token = re.sub('[ٱ]','ﺍ',token)
         # token, freq, lemma, lemma_id, root, pos
         solution = [token, 0, token+"_0", 0, token, ""]

         if token.isdigit():
            solution[5] = "digit" #pos

         elif not _is_ar(token):
            solution[5] = "Foreign" #pos

         else:
            result_token = find_solution(token,language,flag)
            
            if result_token == []:
               token_without_al = re.sub(r'^[ﻝ]','',re.sub(r'^[ﺍ]','',token))
               if len(token_without_al) > 5  :
                  result_token = find_solution(token_without_al, language, flag)

            if result_token == []:
              # try with replace ﻩ with ﺓ
               result_token = find_solution(re.sub(r'[ﻩ]$','ﺓ',token), language, flag)
               

            if result_token == []:
               # try with unify Alef
               word_with_unify_alef = arStrip(token , False , False , False , False , True , False) # Unify Alef
               result_token = find_solution(word_with_unify_alef, language, flag)
            
            if result_token == []:
               # try with remove diac
               word_undiac = arStrip(token , True , False , True , True , False , False) # remove diacs, shaddah ,  digit
               result_token = find_solution(word_undiac, language, flag)

            if result_token == []:
               # try with remove diac and unify alef
               word_undiac = arStrip(token , True , True , True , False, True , False) # diacs , smallDiacs , shaddah ,  alif
               result_token = find_solution(word_undiac, language, flag)

         if result_token != []:
               output_list += result_token
         else:
            output_list += [solution]
        
   return filter_results(output_list, task)


def filter_results(data, task):
    filtered_data = []
    # token, freq, lemma, lemma_id, root, pos
    if task == 'lemmatization':
        filtered_data = [{'token': item[0], 'lemma': item[2], 'lemma_id': item[3], 'frequency': item[1]} for item in data]
    elif task == 'pos':
        filtered_data = [{'token': item[0], 'pos': item[5], 'frequency': item[1]} for item in data]
    elif task == 'root':
        filtered_data = [{'token': item[0], 'root': item[4], 'frequency': item[1]} for item in data]
    else:
        filtered_data = [{'token': item[0], 'lemma': item[2], 'lemma_id': item[3], 'root': item[4], 'pos':item[5], 'frequency': item[1]} for item in data]
    
    return filtered_data


def _is_ar(word):
    return _IS_AR_RE.match(word) is not None       
        

  
  
  
    
    
    
    
    
