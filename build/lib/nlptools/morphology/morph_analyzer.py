
from . import dictionary
import re
from sinatools.morphology.tokenizers_words import simple_word_tokenize
from sinatools.utils.parser import arStrip
from sinatools.morphology.charsets import AR_CHARSET, AR_DIAC_CHARSET

_IS_AR_RE = re.compile(u'^[' + re.escape(u''.join(AR_CHARSET)) + u']+$')
def find_solution(token, language, task):
    """
    Given a token, this method finds the morphological solution lemma and/or pos based on a spesific language and task.
          
    Args:
        token (:obj:`str`): The Arabic token to be morphologcaly analyzed.
        language (:obj:`str`): In the current version, `MSA` is only supported. 
        task (:obj:`str`): The task to filter the results by [lemmatizer, pos, full]. The defualt task if not specified is `full`.

    Returns:
        list (:obj:`list`): A list of [token, lemma, pos], where:
           token: the original input token
           lemma: the lemma of the token 
           pos: the part-of-speech of the token 
    Note:
        If no sloution is found for this token, an empty list is returned.
    """
    
    if token in dictionary.keys():
        resulted_solutions = [] 
        solutions = dictionary[token]
        for solution in solutions:
            resulted_solutions.append([token, solution[0], solution[1], solution[3]])
        return resulted_solutions
    else:
        return []

def analyze(text, language ='MSA', task ='full'):
   """
    This method takes a text as input and returns a morphological solution for each token in this text, Based on the input language and task, such that,
    if:
        the task is lemmatizer, then the morphological soltuion is only the lemma.
        the task is pos, then the morphological soltuion is only the pos.
        the task is full, the the morphological soltuion is both the lemma and the pos.
     
    Args:
        token (:obj:`str`): The Arabic token to be morphologcaly analyzed.
        language (:obj:`str`): In the current version, `MSA` is only supported. 
        task (:obj:`str`): The task to filter the results by [lemmatizer, pos, full]. The defualt task if not specified is `full`.
         
    Returns:
        list (:obj:`list`): A list of [token, lemma, pos], based on the spesified task, where:
           token: the original input token
           lemma: the lemma of the token 
           pos: the part-of-speech of the token 

    **Example:**

     .. highlight:: python
     .. code-block:: python
     
          from sinatools.morphology import morph_analyzer
     
          #Return the morpological solution for each token in this text
          #Example: task = full 
          morph_analyzer.analyze('ذهب الولد الى المدرسة')
           
           [['ذهب', 'ذَهَبَ۪ 1', 'فعل'],
           ['الولد', 'وَلَد 1', 'اسم'],
           ['الى', 'إِلَى 1', 'كلمة وظيفية'],
           ['المدرسة', 'مَدْرَسَة 1', 'اسم']]

           #Exampel: task = pos
           morph_analyzer.analyze('ذهب الولد الى المدرسة',task='pos')
           #the output
           [['ذهب', 'فعل'], ['الولد', 'اسم'], ['الى', 'كلمة وظيفية'], ['المدرسة', 'اسم']]

           #Exampel: task = lemmatizer
           morph_analyzer.analyze('طار العصور فوق الشجرة', task='lemmatizer')
           #the output
           [['طار', 'طارِ۪ 1'],
            ['العصور', 'عَصْر 1'],
            ['فوق', 'فَوْق 1'],
            ['الشجرة', 'شَجَرَة 1']]
     """
 
   #@check if the init does not load data correctly, call load_alma inside
   output_list = []

   tokens = simple_word_tokenize(text)

   for token in tokens:
         result_token =[]
         token = arStrip(token , False , True , False , False , False , False) 
         token = re.sub('[ٱ]','ﺍ',token)
         solution=[token, token+"_0","",0]

         if token.isdigit():
            solution[2] = "digit" #pos

         elif not _is_ar(token):
            solution[2] = "Foreign" #pos

        #  elif re.match("^[a-zA-Z]*$", token): 
        #     solution[2] = "Foreign" #pos

         else:
            result_token = find_solution(token,language, task)
            
            if result_token == []:
               token_without_al = re.sub(r'^[ﻝ]','',re.sub(r'^[ﺍ]','',token))
               if len(token_without_al) > 5  :
                  result_token = find_solution(token_without_al, language, task)

            if result_token == []:
              # try with replace ﻩ with ﺓ
               result_token = find_solution(re.sub(r'[ﻩ]$','ﺓ',token), language, task)
               

            if result_token == []:
               # try with unify Alef
               word_with_unify_alef = arStrip(token , False , False , False , False , True , False) # Unify Alef
               result_token = find_solution(word_with_unify_alef, language, task)
            
            if result_token == []:
               # try with remove diac
               word_undiac = arStrip(token , True , False , True , True , False , False) # remove diacs, shaddah ,  digit
               result_token = find_solution(word_undiac, language, task)

            if result_token == []:
               # try with remove diac and unify alef
               word_undiac = arStrip(token , True , True , True , False, True , False) # diacs , smallDiacs , shaddah ,  alif
               result_token = find_solution(word_undiac, language, task)

         if result_token != []:
               output_list.append(result_token)
         else:
            # if no solution is found
            output_list.append([solution])
        
   return filter_results(task, output_list)


def filter_results(task, lst):
    if task == 'lemmatizer':
        return remove_items_by_index(lst, [2])
    elif task == 'pos':
        return remove_items_by_index(lst, [1])
    else: 
        return lst


def remove_items_by_index(lst, index_list):
    if len(lst) > 0:
       for inner_list in lst[0]:
          for index in sorted(index_list, reverse=True):
              if len(inner_list) > index:
                 inner_list.pop(index)
    return lst


def _is_ar(word):
    return _IS_AR_RE.match(word) is not None       
        

  
  
  
    
    
    
    
    
