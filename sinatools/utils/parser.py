import re 
import argparse

def arStrip(text , diacs=True , small_diacs=True , shaddah=True , digit=True, alif=True , special_chars=True ):
    
    """
    This method allows one to optionally remove (Arabic diacritics, small diacritics, shaddah, Latin and Arabic digits, unify alif, remove special characters, extra spaces, underscore and Arabic tatwelah) from the input text.

    Args:
        text (:obj:`str`): Arabic text to be processed.
        diacs (:obj:`bool`): flag to remove these 7 Arabic diacretics [ ٍ ِ ْ ٌ ُ َ ً] (default is True).
        small_diacs (:obj:`bool`): flag to remove all Quranic annotation signs from this range [06D6-06ED] in addition to small alif. (default is True).
        shaddah (:obj:`bool`): flag to remove shaddah (default is True).
        digit (:obj:`bool`): flag to remove Latin and Arabic digits (default is True).
        alif (:obj:`bool`): flag to unify alif. Replace [ٱ أ إ آ] into [ا] (default is True).
        special_chars (:obj:`bool`): flag to remove these special characters [?؟!@#$%] (default is True).

    Returns:
        :obj:`str`: stripped text.

    **Example:**

    .. highlight:: python
    .. code-block:: python

        from sinatools.utils import parser
        output = parser.arStrip('2023الجو جميلُ')
        print(output)

        # output
        الجو جميل

        output =parser.arStrip('أَلَمۡ یَأۡنِ لِلَّذِینَ ءَامَنُوۤا۟ أَن تَخۡشَعَ قُلُوبُهُمۡ لِذِكۡرِ ٱللَّهِ وَمَا نَزَلَ مِنَ ٱلۡحَقِّ وَلَا یَكُونُوا۟ كَٱلَّذِینَ أُوتُوا۟ ٱلۡكِتَـٰبَ مِن قَبۡلُ فَطَالَ عَلَیۡهِمُ ٱلۡأَمَدُ فَقَسَتۡ قُلُوبُهُمۡۖ وَكَثِیر مِّنۡهُمۡ فَـسِقُونَ', True, True, True, True, False, False )
        print(output)
        #output
        ألم یأن للذین ءامنوا أن تخشع قلوبهم لذكر ٱلله وما نزل من ٱلحق ولا یكونوا كٱلذین أوتوا ٱلكتب من قبل فطال علیهم ٱلأمد فقست قلوبهم وكثیر منهم فسقون
    """
    try:
        if text: # if the input string is not empty do the following
            #print("in if")
            if diacs == True :
                text = re.sub(r'[\u064B-\u0650]+', '',text) # Remove all Arabic diacretics [ ًٌٍَُِْ]
                text = re.sub(r'[\u0652]+', '',text) # Remove SUKUN
            if shaddah == True:
                text = re.sub(r'[\u0651]+', '',text) # Remove shddah
            if small_diacs == True:
                text = re.sub(r'[\u06D6-\u06ED]+', '',text) # Remove all small Quranic annotation signs
            if digit == True:
                text = re.sub('[0-9]+', ' ',text) # Remove English digits
                text = re.sub('[٠-٩]+', ' ',text)# Remove Arabic digits
            
            if alif == True:                             # Unify alif with hamzah: 
                text = re.sub('ٱ', 'ا',text);
                text = re.sub('أ', 'ا',text);
                text = re.sub('إ', 'ا',text);
                text = re.sub('آ', 'ا',text);
            if special_chars == True:
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
    Removes these arabic and english punctuation marks from the text [! " # $ % & ' ( ) * + , - . / : ; > = < ? @ [ \ ] ^ _ ` { | } ~ ، ؛ ؞ ؟ ـ ٓ ٬ ٪ ٫ ٭ ۔].
    
    Args:
      text (:obj:`str`): The input text.
    
    Returns:
       :obj:`str`

    **Example:**

    .. highlight:: python
    .. code-block:: python
    
        from sinatools.utils import parser
        return parser.remove_punctuation("te!@#،$%%؟st")

        #output
        test

        output= parser.remove_punctuation(" {يَا أَيُّهَا الَّذِينَ آمَنُوا لِيَسْتَأْذِنْكُمُ ....}")
        print(output)

        #output
        يَا أَيُّهَا الَّذِينَ آمَنُوا لِيَسْتَأْذِنْكُمُ  

    """
    output_string = text
    try:
        if text:
            punctuation_marks = [r'[\u0021-\u002F]+', r'[U+060C]+', r'[\u003A-\u0040]+',
                                 r'[\u005B-\u0060]+', r'[\u007B-\u007E]+', r'[\u060C]+',
                                 r'[\u061B]+', r'[\u061E]+', r'[\u061F]+', r'[\u0640]+',
                                 r'[\u0653]+', r'[\u065C]+', r'[\u066C]+', r'[\u066A]+',
                                 r'["}"]+', r'["{"]+']
            for punctuation in punctuation_marks:
                output_string = re.sub(punctuation, '', output_string)
    except:
        return text
    return output_string

def remove_latin(text):
    """
    This method removes all Latin letters from the input text.

    Parameters:
        text (:obj:`str`): The input text.
    Returns:
        :obj:`str`
    **Example:**

    .. highlight:: python
    .. code-block:: python

        from sinatools.utils import parser
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
                 
