# -*- coding: utf-8 -*-

from sinatools.utils.parser import arStrip
from sinatools.utils.word_compare import Implication
import argparse

def normalize_word(word: str, ignore_all_diacritics_but_not_shadda: bool=True, ignore_shadda_diacritic: bool=True) -> str:
    if ignore_all_diacritics_but_not_shadda:
        word = arStrip(word, True, True, False, False, False, False)
        
    if ignore_shadda_diacritic:
        word = arStrip(word, False, False, True, False, False, False)
    
    return word

    
def get_preferred_word(word1, word2):
    implication = Implication(word1, word2)
    
    direction = implication.get_direction()
    
    if direction in (0, 2):
        return word1
       
    elif direction == 1:
        return word2
       
    elif direction == 3:
        if not word1.endswith("َ") and not word1.endswith("ُ"):
            return word2
        return word1
     
    
def get_non_preferred_word(word1, word2):

    implication = Implication(word1, word2)
    if implication.get_distance() < 15:
        direction = implication.get_direction()
        if direction == 0 or direction == 1:
            return word1
        elif direction == 2:
            return word2
        elif direction == 3:
            if not word1.endswith("َ") and not word1.endswith("ُ"):
                return word1
            return word2
    return "#"

def get_intersection(list1, list2, ignore_all_diacritics_but_not_shadda=False, ignore_shadda_diacritic=False):
    """
    Computes the intersection of two sets of Arabic words, considering the differences in their diacritization. The method provides two options for handling diacritics: (i) ignore all diacritics except for shadda, and (ii) ignore the shadda diacritic as well. You can try the demo online.
    
    Args:
        list1 (:obj:`list`): The first list.
        list2 (:obj:`bool`): The second list.
        ignore_all_diacratics_but_not_shadda (:obj:`bool`, optional) – A flag to ignore all diacratics except for the shadda. Defaults to False.
        ignore_shadda_diacritic (:obj:`bool`, optional) – A flag to ignore the shadda diacritic. Defaults to False. 
    
    Returns:
        :obj:`list`: The intersection of the two lists, ignores diacritics if flags are true.
    
    **Example:**
    
    .. highlight:: python
    .. code-block:: python
    
        from sinatools.utils.similarity import get_intersection
        list1 = ["كتب","فَعل","فَعَلَ"]
        list2 = ["كتب","فَعّل"]
        print(get_intersection(list1, list2, False, True))
        #output: ["كتب" ,"فعل"]        
    """
    list1 = [str(i) for i in list1 if i not in (None, ' ', '')]
    list1 = [str(i.strip()) for i in list1]

    list2 = [str(i) for i in list2 if i not in (None, ' ', '')]
    list2 = [str(i.strip()) for i in list2]

    interection_list = []

    for list1_word in list1:
        for list2_word in list2:
            word1 = normalize_word(list1_word, ignore_all_diacritics_but_not_shadda, ignore_shadda_diacritic)
            word2 = normalize_word(list2_word, ignore_all_diacritics_but_not_shadda, ignore_shadda_diacritic)

            implication = Implication(word1, word2)
            if implication.get_direction() >= 0 and implication.get_distance() < 15:
                interection_list.append(get_preferred_word(word1, word2))

    i = 0
    while i < len(interection_list):
        j = i + 1
        while j < len(interection_list):
            non_preferred_word = get_non_preferred_word(interection_list[i], interection_list[j])
            if non_preferred_word != "#":
                interection_list.remove(non_preferred_word)
            j += 1
        i += 1

    return interection_list
             


# def get_union(list1, list2, ignore_all_diacritics_but_not_shadda, ignore_shadda_diacritic):
#     """
#     Computes the union of two sets of Arabic words, considering the differences in their diacritization. The method provides two options for handling diacritics: (i) ignore all diacritics except for shadda, and (ii) ignore the shadda diacritic as well. You can try the demo online.
    
#     Args:
#         list1 (:obj:`list`): The first list.
#         list2 (:obj:`bool`): The second list.
#         ignore_all_diacratics_but_not_shadda (:obj:`bool`, optional) – A flag to ignore all diacratics except for the shadda. Defaults to False.
#         ignore_shadda_diacritic (:obj:`bool`, optional) – A flag to ignore the shadda diacritic. Defaults to False. 
    
#     Returns:
#         :obj:`list`: The union of the two lists, ignoring diacritics if flags are true.
    
#     **Example:**
    
#     .. highlight:: python
#     .. code-block:: python
    
#         from sinatools.utils.similarity import get_union
#         list1 = ["كتب","فَعل","فَعَلَ"]
#         list2 = ["كتب","فَعّل"]
#         print(get_union(list1, list2, False, True))
#         #output: ["كتب" ,"فَعل" ,"فَعَلَ"]
#     """
#     list1 = [str(i) for i in list1 if i not in (None, ' ', '')]

#     list2 = [str(i) for i in list2 if i not in (None, ' ', '')]

#     union_list = []

#     for list1_word in list1:
#         word1 = normalize_word(list1_word, ignore_all_diacritics_but_not_shadda, ignore_shadda_diacritic)
#         union_list.append(word1)

#     for list2_word in list2:
#         word2 = normalize_word(list2_word, ignore_all_diacritics_but_not_shadda, ignore_shadda_diacritic)
#         union_list.append(word2)

#     i = 0
#     while i < len(union_list):
#         j = i + 1
#         while j < len(union_list):
#             non_preferred_word = get_non_preferred_word(union_list[i], union_list[j])
#             if (non_preferred_word != "#"):
#                 union_list.remove(non_preferred_word)
#             j = j + 1
#         i = i + 1

#     return union_list
def get_union(list1, list2, ignore_all_diacritics_but_not_shadda, ignore_shadda_diacritic):
  
    
    list1 = [str(i) for i in list1 if i not in (None, ' ', '')]
    list2 = [str(i) for i in list2 if i not in (None, ' ', '')]

    
    union_list = []

    # Normalize and add words from list1
    for list1_word in list1:
        word1 = normalize_word(list1_word, ignore_all_diacritics_but_not_shadda, ignore_shadda_diacritic)
        if word1 not in union_list:  
            union_list.append(word1)

    # Normalize and add words from list2
    for list2_word in list2:
        word2 = normalize_word(list2_word, ignore_all_diacritics_but_not_shadda, ignore_shadda_diacritic)
        if word2 not in union_list:  
            union_list.append(word2)

    
    i = 0
    while i < len(union_list):
        j = i + 1
        while j < len(union_list):
            non_preferred_word = get_non_preferred_word(union_list[i], union_list[j])
            if non_preferred_word != "#":
                union_list.remove(non_preferred_word)
                j -= 1  
            j += 1
        i += 1

    return union_list




def get_jaccard_similarity(list1: list, list2: list, ignore_all_diacritics_but_not_shadda: bool, ignore_shadda_diacritic: bool) -> float:
    """
    Calculates the Jaccard similarity coefficient between two lists of Arabic words, considering the differences in their diacritization. The method provides two options for handling diacritics: (i) ignore all diacritics except for shadda, and (ii) ignore the shadda diacritic as well. You can try the demo online.
    
    Args:
        list1 (:obj:`list`): The first list.
        list2 (:obj:`bool`): The second list.
        ignore_all_diacratics_but_not_shadda (:obj:`bool`, optional) – A flag to ignore all diacratics except for the shadda. Defaults to False.
        ignore_shadda_diacritic (:obj:`bool`, optional) – A flag to ignore the shadda diacritic. Defaults to False. 
    
    Returns:
        :obj:`float`: The Jaccard similarity coefficient between the two lists, ignoring diacritics if flags are true.
    
    **Example:**
    
    .. highlight:: python
    .. code-block:: python
    
        from sinatools.utils.similarity import get_jaccard_similarity
        list1 = ["كتب","فَعل","فَعَلَ"]
        list2 = ["كتب","فَعّل"]
        print(get_jaccard_similarity(list1, list2, True, True))
        #output: 0.67
    """

    intersection_list = get_intersection(list1, list2, ignore_all_diacritics_but_not_shadda, ignore_shadda_diacritic)
    
    union_list = get_union(list1, list2, ignore_all_diacritics_but_not_shadda, ignore_shadda_diacritic)
    
    return float(len(intersection_list)) / float(len(union_list))

def get_jaccard(delimiter, selection, str1, str2, ignoreAllDiacriticsButNotShadda=True, ignoreShaddaDiacritic=True):
    """
    Calculates and returns the Jaccard similarity values (union, intersection, or Jaccard similarity) between two lists of Arabic words, considering the differences in their diacritization. The method provides two options for handling diacritics: (i) ignore all diacritics except for shadda, and (ii) ignore the shadda diacritic as well. You can try the demo online.
    
    Args:
        delimiter (:obj:`str`): The delimiter used to split the input strings.
        str1 (:obj:`str`): The first input string to compare.
        str1 (:obj:`str`): The second input string to compare.
        selection (:obj:`str`) – The desired operation to perform on the two sets of strings. Must be one of intersection, union, jaccardSimilarity, or jaccardAll.
        ignore_all_diacratics_but_not_shadda (:obj:`bool`) – If True, ignore all diacratics except for the Shadda diacritic. (Default is True)
        ignore_shadda_diacritic (:obj:`bool`) – If True, ignore the Shadda diacritic.(Default is True)
    
    Returns:
        Three values (Jaccard similarity, union, or intersection) between the two lists of Arabic words depending on the parameter selection.
    
    **Example:**
    
    .. highlight:: python
    .. code-block:: python
    
        from sinatools.utils.similarity import get_jaccard
        str1 = "فَعَلَ | فَعل"
        str2 = "فَعّل"
        print(get_jaccard("|", "jaccardAll", str1, str2, True, True))
        #output: ['intersection:', ['فعل'], 'union:', ['فعل', 'فعل'], 'similarity:', 0.5]
    """
    try:
        list1 = str1.split(delimiter)
        list2 = str2.split(delimiter)

        if selection == "intersection":
            intersection = get_intersection(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
            return intersection
        elif selection == "union":
            union = get_union(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
            return union
        elif selection == "jaccardSimilarity":      
            similarity = get_jaccard_similarity(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
            return similarity
        elif selection == "jaccardAll":    
            intersection = get_intersection(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
            union = get_union(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
            similarity = get_jaccard_similarity(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
            output_list = ["intersection:", intersection, "union:", union, "similarity:", similarity]
            return output_list
        else:
            return 'Invalid selection option'

    except AttributeError as ae:
        print(f"Attribute error occurred: {str(ae)}")
        return 'Invalid input type'
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return 'An error has occurred'
