from sinatools.utils.parser import arStrip
from . import five_grams_dict, four_grams_dict  , three_grams_dict , two_grams_dict

def ALMA_multi_word(multi_word, n):
    undiac_multi_word = arStrip(multi_word, True, True, True, False, True, False)  # diacs , smallDiacs , shaddah ,  digit , alif , specialChars
    result_word = []
    if n == 2:
        if undiac_multi_word in two_grams_dict.keys():
            result_word = two_grams_dict[undiac_multi_word]                    
    elif n == 3:
        if undiac_multi_word in three_grams_dict.keys():
            result_word = three_grams_dict[undiac_multi_word]                    
    elif n == 4:
        if undiac_multi_word in four_grams_dict.keys():
            result_word = four_grams_dict[undiac_multi_word]                    
    else:    
     if undiac_multi_word in five_grams_dict.keys():
         result_word = five_grams_dict[undiac_multi_word]            
    
    my_json = {}
    output_list = []
    my_json['multi_word_lemma'] = multi_word
    my_json['undiac_multi_word_lemma'] = multi_word
    ids = []
    if result_word != []:
        my_json['POS'] = result_word[0][1] #POS
        for result in result_word: 
           ids.append(result[3])
        my_json['ids'] = ids
        output_list.append(my_json)    
    return output_list  