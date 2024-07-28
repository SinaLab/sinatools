import json
from sinatools.wsd import settings 
from sinatools.wsd.wsd import normalizearabert
from sinatools.wsd.wsd import GlossPredictor
from sinatools.utils.parser import arStrip
from sinatools.utils.tokenizers_words import simple_word_tokenize
from sinatools.morphology.ALMA_multi_word import ALMA_multi_word
from sinatools.morphology.morph_analyzer import analyze
from sinatools.ner.entity_extractor import extract
from . import glosses_dic


def distill_entities(entities):
    list_output = list()

    temp_entities = sortTags(entities)

    temp_list = list()

    temp_list.append(["", "", 0, 0])
    word_position = 0

    for entity in temp_entities:
        counter_tag = 0
        for tag in str(entity[1]).split():
            if counter_tag >= len(temp_list):
                temp_list.append(["", "", 0, 0])

            if "O" == tag and word_position != 0:
                for j in range(0, len(temp_list)):
                    if temp_list[j][1] != "":
                        list_output.append([temp_list[j][0].strip(), temp_list[j][1], temp_list[j][2], temp_list[j][3]])
                        temp_list[j][0] = ""
                        temp_list[j][1] = ""
                        temp_list[j][2] = word_position
                        temp_list[j][3] = word_position
            elif "O" != tag and len(tag.split("-")) == 2 and tag.split("-")[0] == "B":
                if temp_list[counter_tag][1] != "":
                    list_output.append([temp_list[counter_tag][0].strip(), temp_list[counter_tag][1], temp_list[counter_tag][2], temp_list[counter_tag][3]])
                temp_list[counter_tag][0] = str(entity[0]) + " "
                temp_list[counter_tag][1] = str(tag).split("-")[1]
                temp_list[counter_tag][2] = word_position
                temp_list[counter_tag][3] = word_position

            elif "O" != tag and len(tag.split("-")) == 2 and tag.split("-")[0] == "I" and word_position != 0:
                for j in range(counter_tag,len(temp_list)):
                    if temp_list[j][1] == tag[2:] and temp_list[j][3] != word_position:
                        temp_list[j][0] += str(entity[0]) + " "
                        temp_list[j][3] += 1
                        break
                    else:
                        if temp_list[j][1] != "":
                            list_output.append([temp_list[j][0].strip(), temp_list[j][1], temp_list[j][2], temp_list[j][3]])
                            temp_list[j][0] = ""
                            temp_list[j][1] = ""
                            temp_list[j][2] = word_position
                            temp_list[j][3] = word_position
            counter_tag += 1
        word_position += 1
    for j in range(0, len(temp_list)):
        if temp_list[j][1] != "":
            list_output.append([temp_list[j][0].strip(), temp_list[j][1], temp_list[j][2], temp_list[j][3]])
    return sorted(list_output, key=lambda x: (x[2]))


def sortTags(entities):
    temp_entities = entities
    temp_counter = 0
    for entity in temp_entities:
        tags = entity[1].split()
        for tag in tags:
            if temp_counter != 0:
                if "I-" == tag[0:2]:
                    counter_of_this_tag = 0
                    counter_of_previous_tag = 0
                    for word in tags:
                        if tag.split("-")[1] in word:
                            counter_of_this_tag+=1
                    for word in temp_entities[temp_counter-1][1].split():
                        if tag.split("-")[1] in word:
                            counter_of_previous_tag+=1
                    if counter_of_previous_tag > counter_of_this_tag:
                        tags.append("I-"+tag.split("-")[1])
        tags.sort()
        tags.reverse()
        if temp_counter != 0:
            this_tags = tags
            previous_tags = temp_entities[temp_counter - 1][1].split()
            sorted_tags = list()

            if "O" not in this_tags and "O" not in previous_tags:
                index = 0
                for i in previous_tags:
                    j = 0
                    while this_tags and j < len(this_tags):
                        if this_tags[j][0:2] == "I-" and this_tags[j][2:] == i[2:]:
                            sorted_tags.insert(index, this_tags.pop(j))
                            break
                        elif this_tags[j][0:2] == "B-":
                            break
                        j += 1
                    index += 1
            sorted_tags += this_tags
            tags = sorted_tags
        str_tag = " "
        str_tag = str_tag.join(tags)
        str_tag = str_tag.strip()
        temp_entities[temp_counter][1] = str_tag
        temp_counter += 1
    return temp_entities

def delete_form_list(position, word_lemma):
    tmp_word_lemma = [] 
    output = []
    for wordLemma in word_lemma:
        if position == int(wordLemma[2]): 
           word = wordLemma[0]
           gloss = wordLemma[1]
           position = int(wordLemma[3]) 
           concept_count = int(wordLemma[4]) 
           undiac_multi_word_lemma = wordLemma[5]
           multi_word_lemma = wordLemma[6]
           output.append([word, gloss, concept_count, undiac_multi_word_lemma, multi_word_lemma])
        elif position < int(wordLemma[2]): 
           tmp_word_lemma.append(wordLemma)
    return tmp_word_lemma, output, position

def find_two_word_lemma(input_sentence):
    i = 0
    output = []
    length = len(input_sentence)
    while i < length - 1:
        two_grams = input_sentence[i] +" "+ input_sentence[i + 1] 
        data = ALMA_multi_word(two_grams, 2)
        try :
            glosses_list = []   
            concept_count = 0
            ids = data[0]["ids"]
            for concepts in ids:
               glosses_list.append(json.loads(concepts))
            concept_count = concept_count + data[0]["POS"]
            found_2Word_lemma = [two_grams, glosses_list, i, i + 1, concept_count, data[0]['undiac_multi_word_lemma'], data[0]['multi_word_lemma']]
            output.append(found_2Word_lemma) 
            i = i + 1    
        except:
            i = i + 1 
    return output


def find_three_word_lemma(input_sentence):
    i = 0
    output = []
    length = len(input_sentence)
    while i < length - 2:
        three_grams = input_sentence[i] +" "+ input_sentence[i + 1] + " "+ input_sentence[i + 2]
        data = ALMA_multi_word(three_grams, 3)
        try:
           glosses_list = []   
           concept_count = 0
           ids = data[0]["ids"]
           for concepts in ids:
              glosses_list.append(json.loads(concepts))
           concept_count = concept_count + data[0]["POS"]
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
      data = ALMA_multi_word(four_grams, 4)
      try:
         glosses_list = []   
         concept_count = 0
         ids = data[0]["ids"]
         for concepts in ids:
            glosses_list.append(json.loads(concepts))
         concept_count = concept_count + data[0]["POS"] 
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
      data = ALMA_multi_word(five_grams, 5)
      try:
         glosses_list = []   
         concept_count = 0
         ids = data[0]["ids"]
         for concepts in ids:
            glosses_list.append(json.loads(concepts))
         concept_count = concept_count + data[0]["POS"]
         found_5Word_lemma = [five_grams, glosses_list, i, i + 4, concept_count, data[0]['undiac_multi_word_lemma'], data[0]['multi_word_lemma']]
         output.append(found_5Word_lemma) 
         i = i + 1    
      except:  
         i = i + 1 
   return output

def jsons_to_list_of_lists(json_list):
    return [[d['token'], d['tags']] for d in json_list]
    
def find_named_entities(string):
   found_entities = []
   
   ner_entites = extract(string)
   list_of_entites = jsons_to_list_of_lists(ner_entites)
   entites = distill_entities(list_of_entites)
   
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

   data = analyze(word, language ='MSA', task ='full', flag="1")
   Diac_lemma = ""
   pos = ""
   Undiac_lemma = ""
   glosses = []
   Diac_lemma = data[0]["lemma"]
   pos = data[0]["pos"]
   Undiac_lemma = arStrip(Diac_lemma, True, True, True, True, True, False) # Remove diacs , smallDiacs , shaddah ,  digit , alif , specialChars
   ids = [] 
#    glosses_list = []   
   concept_count = 0
   lemma_id = data[0]["lemma_id"]

   if lemma_id in glosses_dic.keys(): 
      value = glosses_dic[lemma_id]
      glosses= json.loads(value[1])
    #   glosses_list.append(json.loads(value[1]))
      concept_count = concept_count + value[0]
   
   return word, Undiac_lemma, Diac_lemma, pos , concept_count, glosses

def disambiguate_glosses_using_SALMA(glosses, Diac_lemma, Undiac_lemma, word, sentence):
   word = normalizearabert(word)
   glosses_dictionary = {}
   if glosses != None:
      for gloss in glosses:
         glosses_dictionary.update({gloss['concept_id'] : gloss['gloss']})
      concept_id, gloss = GlossPredictor(Diac_lemma, Undiac_lemma,word,sentence,glosses_dictionary)

      my_json = {}    
      my_json['Concept_id'] = concept_id
    #   my_json['Gloss'] = gloss
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


def find_glosses(input_sentence, two_word_lemma, three_word_lemma,four_word_lemma, five_word_lemma, ner):
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
            # my_json['concept_count'] = output_from_ner[1][0][2]
            my_json['concept_count'] = '*'
            my_json['glosses'] = output_from_ner[1][0][1]
            my_json['Diac_lemma'] = output_from_ner[1][0][4]
            my_json['Undiac_lemma'] = output_from_ner[1][0][3] 
            output_list.append(my_json)
            # print("output list: ", output_list)
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
    #   my_json['Gloss'] = glosses['gloss']
      my_json['Concept_id'] = glosses['concept_id']
      my_json['Diac_lemma'] = word['Diac_lemma']
      my_json['Undiac_lemma'] = word['Undiac_lemma']
      return my_json
   elif concept_count == '*':
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

   output_list = find_glosses(input_sentence, two_word_lemma, three_word_lemma, four_word_lemma, five_word_lemma, ner)
   results = []
   for word in output_list:
      results.append(disambiguate_glosses_main(word, sentence))
   return results


def disambiguate(sentence):
    """
    This method disambiguate words within a sentence.

    Args:
        sentence (:obj:`str`): The Arabic text to be disambiguated, it should be limited to less than 500 characters.

    Returns:
        :obj:`list`: The JSON output includes a list of words, with each word having a gloss if it exists or a lemma if no gloss is found.

    **Example:**

    .. highlight:: python
    .. code-block:: python

        from sinatools.wsd.disambiguator import disambiguate
        result = disambiguate("مختبر سينا لحوسبة اللغة والذكاء الإصطناعي. في جامعة بيرزيت.")
        print(result)

        #output
         [
             {
                 "Concept_id": "303019218",
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
                 "Concept_id": "334000099",
                 "Diac_lemma": جامِعَة بيرزَيت,
                 "Undiac_lemma": "جامعة بيرزيت"
             }
         ]
    """      
    if len(sentence) > 500:
       content = ["Input is too long"]
       return content
    else: 
       results = WSD(sentence)
       return results 