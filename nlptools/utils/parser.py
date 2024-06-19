import re 
import argparse

def arStrip(text , diacs=True , smallDiacs=True , shaddah=True , digit=True, alif=True , specialChars=True ):
    
    """
    This method removes Arabic diacritics, small diacritcs, shaddah, Latin and Arabic digits, and unify alif.
    And remove special characters, spaces, underscore and Arabic tatwelah from the input text.

    Args:
        text (:obj:`str`): Arabic text to be processed.
        diacs (:obj:`bool`): flag to remove Arabic diacretics [ ًٌٍَُِْ] (default is True).
        smallDiacs (:obj:`bool`): flag to remove small diacretics (default is True).
        shaddah (:obj:`bool`): flag to remove shaddah (default is True).
        digit (:obj:`bool`): flag to remove Latin and Arabic digits (default is True).
        alif (:obj:`bool`): flag to unify alif (default is True).
        specialChars (:obj:`bool`): flag to remove special characters (default is True).

    Returns:
        :obj:`str`: stripped text.

    **Example:**

    .. highlight:: python
    .. code-block:: python

        from nlptools.utils import parser
        processed_text =parser.arStrip('2023الجو جميلُ')
        print(processed_text)

        #putput
        الجو جميل

        name =parser.arStrip('أَلَمۡ یَأۡنِ لِلَّذِینَ ءَامَنُوۤا۟ أَن تَخۡشَعَ قُلُوبُهُمۡ لِذِكۡرِ ٱللَّهِ وَمَا نَزَلَ مِنَ ٱلۡحَقِّ وَلَا یَكُونُوا۟ كَٱلَّذِینَ أُوتُوا۟ ٱلۡكِتَـٰبَ مِن قَبۡلُ فَطَالَ عَلَیۡهِمُ ٱلۡأَمَدُ فَقَسَتۡ قُلُوبُهُمۡۖ وَكَثِیر مِّنۡهُمۡ فَـسِقُونَ' , True , True , True ,  True , True , True )
        print(name)
        #putput
        الم یان للذین ءامنوا ان تخشع قلوبهم لذكر الله وما نزل من الحق ولا یكونوا كالذین اوتوا الكتٰب من قبل فطال علیهم الامد فقست قلوبهم وكثیر منهم فسقون


    """
    try:
        if text: # if the input string is not empty do the following
            #print("in if")
            if diacs == True :
                text = re.sub(r'[\u064B-\u0650]+', '',text) # Remove all Arabic diacretics [ ًٌٍَُِْ]
                text = re.sub(r'[\u0652]+', '',text) # Remove SUKUN
            if shaddah == True:
                text = re.sub(r'[\u0651]+', '',text) # Remove shddah
            if smallDiacs == True:
                text = re.sub(r'[\u06D6-\u06ED]+', '',text) # Remove all small Quranic annotation signs
            if digit == True:
                text = re.sub('[0-9]+', ' ',text) # Remove English digits
                text = re.sub('[٠-٩]+', ' ',text)# Remove Arabic digits
            
            if alif == True:                             # Unify alif with hamzah: 
                text = re.sub('ٱ', 'ا',text);
                text = re.sub('أ', 'ا',text);
                text = re.sub('إ', 'ا',text);
                text = re.sub('آ', 'ا',text);
            if specialChars == True:
                text = re.sub('[?؟!@#$%-]+' , '' , text) # Remove some of special chars 

            text = re.sub('[\\s]+'," ",text) # Remove all spaces
            text = text.replace("_" , '') #Remove underscore
            text = text.replace("ـ" , '') # Remove Arabic tatwelah
            text = text.strip() # Trim input string
    except:
        return text
    return text
    
def remove_punctuation(text):
    """
    Removes punctuation marks from the text.
    
    Args:
      text (:obj:`str`): The input text.
    
    Returns:
      :obj:`str`: The output text without punctuation marks.

    **Example:**

    .. highlight:: python
    .. code-block:: python
    
        from nlptools.utils import parser
        return parser.remove_punctuation("te!@#،$%%؟st")

        #output
        test

        output= parser.remove_punctuation(" {يَا أَيُّهَا الَّذِينَ آمَنُوا لِيَسْتَأْذِنْكُمُ ....}")
        print(output)

        #output
        يَا أَيُّهَا الَّذِينَ آمَنُوا لِيَسْتَأْذِنْكُمُ  

    """
    try:
        if text:
            punctuation_marks = [r'[\u0021-\u002F]+', r'[U+060C]+', r'[\u003A-\u0040]+',
                                 r'[\u005B-\u0060]+', r'[\u007B-\u007E]+', r'[\u060C]+',
                                 r'[\u061B]+', r'[\u061E]+', r'[\u061F]+', r'[\u0640]+',
                                 r'[\u0653]+', r'[\u065C]+', r'[\u066C]+', r'[\u066A]+',
                                 r'["}"]+', r'["{"]+']
            outputString = text
            for punctuation in punctuation_marks:
                outputString = re.sub(punctuation, '', outputString)
    except:
        return text
    return outputString

def remove_latin(text):
    """
    This method removes all Latin characters from the input text.

    Args:
        text (:obj:`str`): The input text.

    Returns:
         outputString (:obj:`str`): The text without Latin characters.
    Note:
        If an error occurs during processing, the original text is returned.
    **Example:**

    .. highlight:: python
    .. code-block:: python

        from nlptools.utils import parser
        return parser.remove_latin("miojkdujhvaj1546545spkdpoqfoiehwv nWEQFGWERHERTJETAWIKUYFC")
    
        #output
        1546545  

        output = parser.remove_latin("أصل المسمى «تخطيط موارد المؤسسة» هو تعريب لمسمى التخطيط باللغة الإنجليزية Enterprise Resource Planning")
        print(output)

        #output
        أصل المسمى «تخطيط موارد المؤسسة» هو تعريب لمسمى التخطيط باللغة الإنجليزية      
    """
    try:
        if text:
            text = re.sub('[a-zA-Z]+', ' ', text)
    except:
        return text
    return text
                 