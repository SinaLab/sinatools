# -*- coding: utf-8 -*-

from nlptools.utils.parser import arStrip
from nlptools.utils.implication import Implication
import argparse

def normalize_word(word: str, ignore_all_diacritics_but_not_shadda: bool=True, ignore_shadda_diacritic: bool=True) -> str:
    """
    Normalize a given Arabic word by removing diacritics and/or shadda diacritic.

    Args:
        word (:obj:`str`): The input text.
        ignore_all_diacritics_but_not_shadda (:obj:`bool`): A boolean flag indicating whether to remove all diacritics except shadda (default is True). 
        ignore_shadda_diacritic (:obj:`bool`): A boolean flag indicating whether to remove shadda diacritic (default is True).

    Returns:
          :obj:`str` Normalized Arabic word.
    """
    if ignore_all_diacritics_but_not_shadda:
        word = arStrip(word, True, True, False, False, False, False)
        
    if ignore_shadda_diacritic:
        word = arStrip(word, False, False, True, False, False, False)
    
    return word

    
def get_preferred_word(word1, word2):
    """
    Returns the preferred word among two given words based on their implication.

    Args:
        word1 (:obj:`str`): The first word.
        word2 (:obj:`str`): The second word.

    Returns:
        :obj:`str`: The preferred word among the two given words.
    
    """
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
    """
    Returns the non-preferred word between the two input words.

    Args:
        word1 (:obj:`str`): The first word.
        word2 (:obj:`str`): The second word.

    Returns:
        :obj:`str`: The non-preferred word. If there is no non-preferred word, The '#' is returned.

    """

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
#@TBD
def get_intersection(list1, list2, ignore_all_diacritics_but_not_shadda=False, ignore_shadda_diacritic=False):
    """
    Get the intersection of two lists after normalization and ignoring diacritics based on input flags.

    Args:
        list1 (:obj:`list`): The first list.
        list2 (:obj:`list`): The second list.
        ignore_all_diacritics_but_not_shadda (:obj:`bool`, optional): A flag to ignore all diacritics except for the shadda. Defaults to False.
        ignore_shadda_diacritic (:obj:`bool`, optional): A flag to ignore the shadda diacritic. Defaults to False.

    Returns:
         :obj:`list`: The intersection of the two lists after normalization and ignoring diacritics.

    """

    # Remove all None and empty values from first list
    list1 = [str(i) for i in list1 if i not in (None, ' ', '')]
    list1 = [str(i.strip()) for i in list1]

    # Remove all None and empty values from second list
    list2 = [str(i) for i in list2 if i not in (None, ' ', '')]
    list2 = [str(i.strip()) for i in list2]

    interection_list = []

    # Add all Common words between the two list1 and list2 to interectionList
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
             


def get_union(list1, list2, ignore_all_diacritics_but_not_shadda, ignore_shadda_diacritic):
    """
    Finds the union of two lists by removing duplicates and normalizing words.

    Args:
        list1 (:obj:`list`): The first list.
        list2 (:obj:`list`): The second list.
        ignore_all_diacritics_but_not_shadda (:obj:`bool`): Whether to ignore all diacritics except shadda or not.
        ignore_shadda_diacritic (:obj:`bool`): Whether to ignore shadda diacritic or not.
   Returns:
         :obj:`list`: The union of the two lists after removing duplicates and normalizing words.
    """

    list1 = [str(i) for i in list1 if i not in (None, ' ', '')]

    list2 = [str(i) for i in list2 if i not in (None, ' ', '')]

    union_list = []

    for list1_word in list1:
        word1 = normalize_word(list1_word, ignore_all_diacritics_but_not_shadda, ignore_shadda_diacritic)
        union_list.append(word1)

    for list2_word in list2:
        word2 = normalize_word(list2_word, ignore_all_diacritics_but_not_shadda, ignore_shadda_diacritic)
        union_list.append(word2)

    i = 0
    while i < len(union_list):
        j = i + 1
        while j < len(union_list):
            non_preferred_word = get_non_preferred_word(union_list[i], union_list[j])
            if (non_preferred_word != "#"):
                union_list.remove(non_preferred_word)
            j = j + 1
        i = i + 1

    return union_list
      


def jaccard_similarity(list1: list, list2: list, ignore_all_diacritics_but_not_shadda: bool, ignore_shadda_diacritic: bool) -> float:
    """
    Calculates the Jaccard similarity coefficient between two lists.

    Args:
        list1 (:obj:`list`): The first list.
        list2 (:obj:`list`): The second list.
        ignore_all_diacritics_but_not_shadda (:obj:`bool`): A flag indicating whether to ignore all diacritics except for shadda.
        ignore_shadda_diacritic (:obj:`bool`): A flag indicating whether to ignore the shadda diacritic.

    Returns:
         :obj:`float`: The Jaccard similarity coefficient between the two lists.
    """
    # Find the intersection between two sets
    intersection_list = get_intersection(list1, list2, ignore_all_diacritics_but_not_shadda, ignore_shadda_diacritic)
    
    # Find the union between two sets
    union_list = get_union(list1, list2, ignore_all_diacritics_but_not_shadda, ignore_shadda_diacritic)
    
    # Calculate the Jaccard similarity coefficient by dividing the length of the intersectionList by the length of the unionList
    return float(len(intersection_list)) / float(len(union_list))
   



def jaccard(delimiter, str1, str2, selection, ignoreAllDiacriticsButNotShadda=True, ignoreShaddaDiacritic=True):
    """
    Compute the Jaccard similarity, union, or intersection of two sets of strings.

    Args:
        delimiter (:obj:`str`): The delimiter used to split the input strings.
        str1 (:obj:`str`): The first input string to compare.
        str2 (:obj:`str`): The second input string to compare.
        selection (:obj:`str`): The desired operation to perform on the two sets of strings. 
                         Must be one of *intersection*, *union*, *jaccardSimilarity*, or *jaccardAll*.
        ignoreAllDiacriticsButNotShadda (:obj:`bool`): If True, ignore all diacritics except for the Shadda diacritic. (Defualt is True)
        ignoreShaddaDiacritic (:obj:`bool`): If True, ignore the Shadda diacritic.(Default is True)

    Returns:
        The Jaccard similarity, union, or intersection of the two sets of strings, 
        depending on the value of the `selection` argument.
    
    Note:
        - If `selection` is *jaccardAll*, a list of the intersection, union, and Jaccard similarity 
        of the two sets of strings will be returned.
        - If an error occurs, the method will return the string "An error has occurred".
          Online tool: https://sina.birzeit.edu/resources/jaccardFunction.html
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
            similarity = jaccard_similarity(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
            return similarity
        elif selection == "jaccardAll":    
            intersection = get_intersection(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
            union = get_union(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
            similarity = jaccard_similarity(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
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
