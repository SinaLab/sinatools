from nlptools.morphology import settings 
from nlptools.utils.parser import arStrip
import json


def ALMA_multi_word(multi_word):
    undiac_multi_word = arStrip(multi_word, True, True, True, False, True, False)  # diacs , smallDiacs , shaddah ,  digit , alif , specialChars
    result_word = []
    if undiac_multi_word in settings.div_dic.keys():
        result_word = settings.div_dic[undiac_multi_word]
    
    my_json = {}
    glosses_list = []
    output_list = []
    concept_count = 0
    my_json['multi_word_lemma'] = multi_word
    my_json['undiac_multi_word_lemma'] = multi_word
    ids = []
    if result_word != []:
        #my_json['concept_count'] = result_word[0][1] #concept_count
        #my_json['POS'] = result_word[0][2] #POS
        my_json['POS'] = result_word[0][1] #POS

        for result in result_word: 
           ids.append(result[3])
           #if lemma_id in settings.glosses_dic.keys(): 
           #   value = settings.glosses_dic[lemma_id]
           #   glosses_list.append(json.loads(value[1]))
           #   concept_count = concept_count + value[0]
        my_json['ids'] = ids
        #my_json['concept_count'] = concept_count
        #my_json['glosses'] = glosses_list   
        output_list.append(my_json)    
    return output_list  