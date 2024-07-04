import json
from sinatools.salma import settings 
from sinatools.salma.wsd import normalizearabert
from sinatools.salma.wsd import GlossPredictor
from sinatools.utils.parser import arStrip
from sinatools.utils.tokenizers_words import simple_word_tokenize
from sinatools.morphology.ALMA_multi_word import ALMA_multi_word
from sinatools.morphology.morph_analyzer import analyze
#from sinatools.ner.entity_extractor import ner

def delete_form_list(position, word_lemma):
    #"""
    #Remove specific elements from the word_lemma list based on the given position.
    #
    #Parameters:
    #position (int): The current position in the input sentence.
    #word_lemma (list): List of word lemma details.
    #
    #Returns:
    #list: Updated word_lemma list with the specific elements removed.
    #list: The list of removed elements.
    #int: The new position in the input sentence.
    #"""
    tmp_word_lemma = [] 
    output = []
    for wordLemma in word_lemma:
        if position == int(wordLemma[2]): # start 
           word = wordLemma[0]
           gloss = wordLemma[1]
           position = int(wordLemma[3]) 
           concept_count = int(wordLemma[4]) 
           undiac_multi_word_lemma = wordLemma[5]
           multi_word_lemma = wordLemma[6]
           output.append([word, gloss, concept_count, undiac_multi_word_lemma, multi_word_lemma])# word
        elif position < int(wordLemma[2]): 
           tmp_word_lemma.append(wordLemma)
    return tmp_word_lemma, output, position

def find_two_word_lemma(input_sentence):
    #"""
    #Find two-word lemmas in the input sentence using the ALMA_multi_word function.
    #
    #Parameters:
    #input_sentence (list): Tokenized input sentence.
    #
    #Returns:
    #list: List of details of found two-word lemmas.
    #"""
    i = 0
    output = []
    length = len(input_sentence)
    while i < length - 1:
        two_grams = input_sentence[i] +" "+ input_sentence[i + 1] 
        data = ALMA_multi_word(two_grams)
        try :
            glosses_list = []   
            concept_count = 0
            ids = data[0]["ids"]
            for lemma_id in ids:
               if lemma_id in settings.glosses_dic.keys(): 
                  value = settings.glosses_dic[lemma_id]
                  glosses_list.append(json.loads(value[1]))
                  concept_count = concept_count + value[0]
            
            # found two_grams
            #found_2Word_lemma = [two_grams,data[0]['glosses'], i, i + 1,data[0]['concept_count'], data[0]['undiac_multi_word_lemma'], data[0]['multi_word_lemma']]
            found_2Word_lemma = [two_grams, glosses_list, i, i + 1, concept_count, data[0]['undiac_multi_word_lemma'], data[0]['multi_word_lemma']]
            output.append(found_2Word_lemma) 
            i = i + 1    
        except: # no record found on this multi_lema
            i = i + 1 
    return output


def find_three_word_lemma(input_sentence):
    i = 0
    output = []
    length = len(input_sentence)
    while i < length - 2:
        three_grams = input_sentence[i] +" "+ input_sentence[i + 1] + " "+ input_sentence[i + 2]
        data = ALMA_multi_word(three_grams)
        try:
           glosses_list = []   
           concept_count = 0
           ids = data[0]["ids"]
           for lemma_id in ids:
              if lemma_id in settings.glosses_dic.keys(): 
                 value = settings.glosses_dic[lemma_id]
                 glosses_list.append(json.loads(value[1]))
                 concept_count = concept_count + value[0]
                 
           #found_3Word_lemma = [three_grams, data[0]['glosses'], i, i + 2,data[0]['concept_count'], data[0]['undiac_multi_word_lemma'], data[0]['multi_word_lemma']]
           found_3Word_lemma = [three_grams, glosses_list, i, i + 2, concept_count, data[0]['undiac_multi_word_lemma'], data[0]['multi_word_lemma']]
           output.append(found_3Word_lemma) 
           i = i + 1    
        except:  
           i = i + 1 
    return output

def find_four_word_lemma(input_sentence):
   i = 0
   output = []
   length = len(input_sentence)
   while i < length - 3:
      four_grams = input_sentence[i] +" "+ input_sentence[i + 1] + " "+ input_sentence[i + 2] + " "+ input_sentence[i + 3]
      data = ALMA_multi_word(four_grams)
      try:
         glosses_list = []   
         concept_count = 0
         ids = data[0]["ids"]
         for lemma_id in ids:
            if lemma_id in settings.glosses_dic.keys(): 
               value = settings.glosses_dic[lemma_id]
               glosses_list.append(json.loads(value[1]))
               concept_count = concept_count + value[0]
         #found_4Word_lemma = [four_grams, data[0]['glosses'], i, i + 3,data[0]['concept_count'], data[0]['undiac_multi_word_lemma'], data[0]['multi_word_lemma']]
         found_4Word_lemma = [four_grams, glosses_list, i, i + 3, concept_count, data[0]['undiac_multi_word_lemma'], data[0]['multi_word_lemma']]
         output.append(found_4Word_lemma) 
         i = i + 1    
      except:  
         i = i + 1 
   return output


def find_five_word_lemma(input_sentence):
   i = 0
   output = []
   length = len(input_sentence)
   while i < length - 4:
      five_grams = input_sentence[i] +" "+ input_sentence[i + 1] + " "+ input_sentence[i + 2] + " "+ input_sentence[i + 3] + " "+ input_sentence[i + 4]
      data = ALMA_multi_word(five_grams)
      try:
         glosses_list = []   
         concept_count = 0
         ids = data[0]["ids"]
         for lemma_id in ids:
            if lemma_id in settings.glosses_dic.keys(): 
               value = settings.glosses_dic[lemma_id]
               glosses_list.append(json.loads(value[1]))
               concept_count = concept_count + value[0]
         #found_5Word_lemma = [five_grams, data[0]['glosses'], i, i + 4,data[0]['concept_count'], data[0]['undiac_multi_word_lemma'], data[0]['multi_word_lemma']]
         found_5Word_lemma = [five_grams, glosses_list, i, i + 4, concept_count, data[0]['undiac_multi_word_lemma'], data[0]['multi_word_lemma']]
         output.append(found_5Word_lemma) 
         i = i + 1    
      except:  
         i = i + 1 
   return output

def find_named_entities(string):
   #"""
   # Find named entities in the input string using a NER tool.
   # 
   # Parameters:
   # string (str): Input string.
   # 
   # Returns:
   # list: List of details of found named entities.
   # """
   found_entities = []
   #entites = ner(string, "4")
   entites = []
   tag_gloss = {
      "PERS": "اسم شخص",
      "ORG": "اسم مؤسسة",
      #"NORP": "مجموعة من الناس", 
      #"OCC": "منصب/مسمى وظيفي",
      "LOC": "اسم منطقة جغرافية",
      "FAC": "اسم لمَعلَم",
      #"EVENT": "حدث",
      "DATE": "فترة زمنية تدل على تاريخ",
      "UNIT": "وحدة قياس",
      "CURR": "عملة",
      "GPE": "اسم بلد، له حدود إدارية/جيوسياسية",
      "TIME": "فترة زمنية تدل على الوقت",
      "CARDINAL": "عدد يدل على معدود",
      "ORDINAL": "رقم، لا يدل على معدود",
      "PERCENT": "نسبة مئوية",
      "QUANTITY": "كمية",
      "MONEY": "مبلغ مالي",
      "LANGUAGE": "اسم للغة طبيعية",
      "PRODUCT": "اسم منتج",
      "LAW": "قانون"
   }

   for entity in entites:
      gloss_ner = ""
      if entity[1] in tag_gloss.keys():
         gloss_ner = tag_gloss[entity[1]]  

      if gloss_ner != "":
         gloss = [{'concept_id': '', 'resource_id': '', 'resource_name': '', 'gloss': gloss_ner}]   
         entity = [entity[0],gloss,int(entity[2]), int(entity[3]),1,arStrip(entity[0],True,True,True,False,True,False),entity[0]]   
         found_entities.append(entity)
   return found_entities   


def find_glosses_using_ALMA(word):

   data = analyze(word)
   Diac_lemma = ""
   pos = ""
   Undiac_lemma = ""
   glosses = []
   Diac_lemma = data[0][1]
   pos = data[0][2]
   Undiac_lemma = arStrip(Diac_lemma, True, True, True, True, True, False) # Remove diacs , smallDiacs , shaddah ,  digit , alif , specialChars
   #"""
   # Find glosses for the given word using the ALMA tool.
   # 
   # Parameters:
   # word (str): Input word.
   # 
   # Returns:
   # tuple: Details of the word including glosses, lemmas, and POS.
   # """
   ids = [] 
   glosses_list = []   
   concept_count = 0
   for line in data:
      lemma_id = line[3]
      ids.append(lemma_id)

   for lemma_id in ids:
      if lemma_id in settings.glosses_dic.keys(): 
         value = settings.glosses_dic[lemma_id]
         glosses_list.append(json.loads(value[1]))
         concept_count = concept_count + value[0]

   #glosses = data[0][4]
   #concept_count = data[0][3]
   return word, Undiac_lemma, Diac_lemma, pos , concept_count, glosses
   
def disambiguate_glosses_using_SALMA(glosses, Diac_lemma, Undiac_lemma, word, sentence):
   #"""
   # Disambiguate glosses using the SALMA tool.
   # 
   # Parameters:
   # glosses (list): List of glosses.
   # Diac_lemma (str): Diacritic lemma of the word.
   # Undiac_lemma (str): Undiacritic lemma of the word.
   # word (str): The word being analyzed.
   # sentence (str): The sentence containing the word.
   # 
   # Returns:
   # dict: Disambiguated gloss details.
   # """
   word = normalizearabert(word)
   glosses_dictionary = {}
   if glosses != None:
      for gloss in glosses:
         glosses_dictionary.update({gloss['concept_id'] : gloss['gloss']})
      concept_id, gloss = GlossPredictor(Diac_lemma, Undiac_lemma,word,sentence,glosses_dictionary)

      my_json = {}    
      my_json['Concept_id'] = concept_id
      my_json['Gloss'] = gloss
      my_json['word'] = word
      my_json['Undiac_lemma'] = Undiac_lemma
      my_json['Diac_lemma'] = Diac_lemma
      return my_json
   else:
      my_json = {}    
      my_json['word'] = word
      my_json['Undiac_lemma'] = Undiac_lemma
      my_json['Diac_lemma'] = Diac_lemma
      return my_json


def find_glosses(input_sentence, three_word_lemma, two_word_lemma, four_word_lemma, five_word_lemma, ner):
      output_list = []
      position = 0
      while position < len(input_sentence):    
         flag = "False"
         output_from5word = delete_form_list(position, five_word_lemma)
         five_word_lemma = output_from5word[0]
         if output_from5word[1] != []: # output
            position = output_from5word[2]  
            flag = "True"
            my_json = {}    
            my_json['word'] = output_from5word[1][0][0]
            my_json['concept_count'] = output_from5word[1][0][2]
            my_json['glosses'] = output_from5word[1][0][1]
            my_json['Diac_lemma'] = output_from5word[1][0][4]
            my_json['Undiac_lemma'] = output_from5word[1][0][3]
            output_list.append(my_json)
            position = position + 1                



         output_from4word = delete_form_list(position, four_word_lemma)
         four_word_lemma = output_from4word[0]
         if output_from4word[1] != []: # output
            position = output_from4word[2]  
            flag = "True"
            my_json = {}    
            my_json['word'] = output_from4word[1][0][0]
            my_json['concept_count'] = output_from4word[1][0][2]
            my_json['glosses'] = output_from4word[1][0][1]
            my_json['Diac_lemma'] = output_from4word[1][0][4]
            my_json['Undiac_lemma'] = output_from4word[1][0][3]
            output_list.append(my_json)
            position = position + 1                
         
         output_from3word = delete_form_list(position, three_word_lemma)
         three_word_lemma = output_from3word[0]
         if output_from3word[1] != []: # output
            position = output_from3word[2]  
            flag = "True"
            my_json = {}    
            my_json['word'] = output_from3word[1][0][0]
            my_json['concept_count'] = output_from3word[1][0][2]
            my_json['glosses'] = output_from3word[1][0][1]
            my_json['Diac_lemma'] = output_from3word[1][0][4]
            my_json['Undiac_lemma'] = output_from3word[1][0][3]
            output_list.append(my_json)
            position = position + 1                



         output_from2Word = delete_form_list(position, two_word_lemma)
         two_word_lemma = output_from2Word[0] 
         if output_from2Word[1] != []:  
            position = output_from2Word[2]
            flag = "True"
            my_json = {}    
            word = output_from2Word[1][0][0]
            my_json['word'] = word
            my_json['concept_count'] = output_from2Word[1][0][2]
            my_json['glosses'] = output_from2Word[1][0][1]
            my_json['Diac_lemma'] = output_from2Word[1][0][4]
            my_json['Undiac_lemma'] = output_from2Word[1][0][3] 
            output_list.append(my_json)
            position = position + 1                 
               


         output_from_ner = delete_form_list(position, ner)
         ner = output_from_ner[0] 
         if output_from_ner[1] != []:  
            position = output_from_ner[2]
            flag = "True"
            my_json = {}    
            word = output_from_ner[1][0][0]
            my_json['word'] = word
            my_json['concept_count'] = output_from_ner[1][0][2]
            my_json['glosses'] = output_from_ner[1][0][1]
            my_json['Diac_lemma'] = output_from_ner[1][0][4]
            my_json['Undiac_lemma'] = output_from_ner[1][0][3] 
            output_list.append(my_json)
            position = position + 1                             
         
         if flag == "False": # Not found in ner or in multi_word_dictionary, ASK ALMA 
            word = input_sentence[position]
            word, Undiac_lemma, Diac_lemma, pos , concept_count, glosses = find_glosses_using_ALMA(word)   
            my_json = {}    
            my_json['word'] = word
            my_json['concept_count'] = concept_count
            my_json['glosses'] = glosses
            my_json['Diac_lemma'] = Diac_lemma
            my_json['Undiac_lemma'] = Undiac_lemma
            output_list.append(my_json)
            position = position + 1  
      return output_list                    

def disambiguate_glosses_main(word, sentence):
   concept_count = word['concept_count']
   if concept_count == 0:
      my_json = {}    
      my_json['word'] = word['word']
      my_json['Diac_lemma'] = word['Diac_lemma']
      my_json['Undiac_lemma'] = word['Undiac_lemma']
      return my_json
   elif concept_count == 1:
      my_json = {}    
      my_json['word'] = word['word']
      glosses = word['glosses'][0]
      my_json['Gloss'] = glosses['gloss']
      my_json['Concept_id'] = glosses['concept_id']
      my_json['Diac_lemma'] = word['Diac_lemma']
      my_json['Undiac_lemma'] = word['Undiac_lemma']
      return my_json
   else:   
      input_word = word['word']
      concept_count = word['concept_count']
      glosses = word['glosses']
      Diac_lemma = word['Diac_lemma']
      Undiac_lemma = word['Undiac_lemma']
      return disambiguate_glosses_using_SALMA(glosses, Diac_lemma, Undiac_lemma, input_word, sentence)

def WSD(sentence):
   
   input_sentence = simple_word_tokenize(sentence)
   
   five_word_lemma = find_five_word_lemma(input_sentence)
   
   four_word_lemma = find_four_word_lemma(input_sentence)
   
   three_word_lemma = find_three_word_lemma(input_sentence)
   
   two_word_lemma = find_two_word_lemma(input_sentence)
   
   ner = find_named_entities(" ".join(input_sentence))

   output_list = find_glosses(input_sentence, three_word_lemma, two_word_lemma, four_word_lemma, five_word_lemma, ner)
   
   results = []
   for word in output_list:
      results.append(disambiguate_glosses_main(word, sentence))
   return results


def SALMA(sentence):
    """
    This method disambiguate words within a sentence.

    Args:
        sentence (:obj:`str`): The Arabic text to be disambiguated, it should be limited to less than 500 characters.

    Returns:
        :obj:`list`: The JSON output includes a list of words, with each word having a gloss if it exists or a lemma if no gloss is found.

    **Example:**

    .. highlight:: python
    .. code-block:: python

        from sinatools.salma.views import SALMA
        JSON = SALMA("مختبر سينا لحوسبة اللغة والذكاء الإصطناعي. في جامعة بيرزيت.")
        print(JSON["resp"])

        #output
         [
             {
                 "Concept_id": "303019218",
                 "Gloss": "ذهَب إلى عملِه:- قصَده، توجَّه إليه \"ذهَب إلى الجامعة/ بيروت - اذهَب إلى أبيك والتمس منه الصفح - ذهَب إلى قول فلان أخذ به - <اذْهَبْ إِلَى فِرْعَوْنَ إِنَّهُ طَغَى> طه/ 24 \". ذهَب رأسًا إليه",
                 "word": "ذهبت",
                 "Undiac_lemma": "ذهب",
                 "Diac_lemma": "ذَهَبَ۪ 1"
             },
             {
                 "word": "إلى",
                 "Diac_lemma": إِلَى 1,
                 "Undiac_lemma": "الى"
             },
             {
                 "word": "جامعة بيرزيت",
                 "Gloss": جامعة فلسطينية تقع في بلدة بيرزيت، قرب مدينة رام الله، ويعود تاريخها إلى عام 1924 عندما تأسست كمدرسة ابتدائية ثم أصبحت جامعة عام 1975,
                 "Concept_id": "334000099",
                 "Diac_lemma": جامِعَة بيرزَيت,
                 "Undiac_lemma": "جامعة بيرزيت"
             }
         ]
    """      
    if len(sentence) > 500:
       content = {"statusText":"Input is too long","statusCode":-7}
       return content
    else: 
       results = WSD(sentence)
       return {"resp": results, "statusText":"OK","statusCode":0}