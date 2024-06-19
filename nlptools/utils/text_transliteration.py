from collections import deque

# This is a mapping dictionery of Arabic letters to BW 
# dictionery contains: key -> Unicode to Arabic, value -> BW chars
# It includes all BW mappings in addition to other special characters
#  that are used in the SAMA database but not part of the BW character set such as numbers and Qur'anic diacritics
ar2bw_map = {
    '\u0621' : '\'' , # ء
    '\u0622' : '|' , # آ
    '\u0623' : '>' , # أ
    '\u0624' : '&' , # ؤ
    '\u0625' : '<' , # إ
    '\u0626' : '}' , # ئ
    '\u0627' : 'A' , # ا
    '\u0628' : 'b' , # ب
    '\u0629' : 'p' , # ة
    '\u062A' : 't' , # ت
    '\u062B' : 'v' , # ث
    '\u062C' : 'j' , # ج
    '\u062D' : 'H' , # ح
    '\u062E' : 'x' , # خ
    '\u062F' : 'd' , # د
    '\u0630' : '*' , # ذ
    '\u0631' : 'r' , # ر
    '\u0632' : 'z' , # ز
    '\u0633' : 's' , # س
    '\u0634' : '$' , # ش
    '\u0635' : 'S' , # ص
    '\u0636' : 'D' , # ض
    '\u0637' : 'T' , # ط
    '\u0638' : 'Z' , # ظ
    '\u0639' : 'E' , # ع
    '\u063A' : 'g' , # غ
    '\u0020' : ' ' , #Space is replaced by space 
    '\u0640' : '_' , #ـ
    '\u0641' : 'f' , # ف
    '\u0642' : 'q' , # ق
    '\u0643' : 'k' , # ك
    '\u0644' : 'l' , # ل
    '\u0645' : 'm' , # م
    '\u0646' : 'n' , # ن
    '\u0647' : 'h' , # ه
    '\u0648' : 'w' , # و
    '\u0649' : 'Y' , # ى
    '\u064A' : 'y' , # ي
    '\u064B' : 'F' , # TANWEEN FATH ً
    '\u064C' : 'N' , #TANWEEN DHAM ٌ
    '\u064D' : 'K' , #TANWEE KASR ٍ
    '\u064E' : 'a' , #FATHA َ
    '\u064F' : 'u' , #DHAMMA ُ
    '\u0650' : 'i' , #KASRA ِ
    '\u0651' : '~' , # SHADDAH ّ
    '\u0652' : 'o' , #SUKON ْ
    '\u0670' : '`' , # SHORT ALEF (dagger alif) ٰ
    '\u0671' : '{' , #AL WITH HAMZA QATE'/WASEL MARK ٱ
    '\u067E' : 'P' , # پ 
    '\u0686' : 'J' , # چ 
    '\u06A4' : 'V' , # ڤ 
    '\u06AF' : 'G' , # گ 
    '\u06EA' : '-' , # ۪ Not BW standerd
    '\u0654' : '#' , # ٔ     Not BW standerd
    '\u06DC ' : ':' , # short sen ۜ  Not BW standerd  
    '\u06E0' : '"' , # small circle ۟  ,Not BW standerd
    '\u06E2' : '[' , # short meem ۢ  , Not BW standerd
    '\u06E3 ' : ';' , #small sen below letter  ۣ  , Not BW standerd
    '\u06E5 ' : ',' , # samall wa ۥ  , Not BW standerd
    '\u06E6' : '.' , # ۦ   Not BW standerd
    '\u06E8 ' : '!' , # small noon ۨ  Not BW standerd
    '\u06EA' : '-' , # special qura'nic arabic ( littel circule underneath), is not part of standerd BW , not in Buckwalter ۪  Not BW standerd
    '\u06EC' : '%' , # small solid circle ۬  Not BW standerd
    '\u06ED ' : ']',  # small meem ۭ  Not BW standerd
    '0' : '0' , #
    '1' : '1' , #
    '2' : '2' , #
    '3' : '3' , #
    '4' : '4' , #
    '5' : '5' , #
    '6' : '6' , #
    '7' : '7' , #
    '8' : '8' , #
    '9' : '9'  #
}

# This is a mapping dictionery of BW  letters to  Arabic
# It includes all Arabic mappings in addition to other special characters
#  that are used in the SAMA database but not part of the Arabic character set such as numbers and Qur'anic diacritics
bw2ar_map = {
    '\'' : '\u0621' , # ء
    '|' : '\u0622' , # آ
    '>' : '\u0623' , # أ
    '&' : '\u0624' , # ؤ
    '<' : '\u0625' , # إ
    '}' : '\u0626' , # ئ
    'A' : '\u0627' , # ا
    'b' : '\u0628' , # ب
    'p' : '\u0629' , # ة
    't' : '\u062A' , # ت
    'v' : '\u062B' , # ث
    'j' : '\u062C' , # ج
    'H' : '\u062D' , # ح
    'x' : '\u062E' , # خ
    'd' : '\u062F' , # د
    '*' : '\u0630' , # ذ
    'r' : '\u0631' , # ر
    'z' : '\u0632' , # ز
    's' : '\u0633' , # س
    '$' : '\u0634' , # ش
    'S' : '\u0635' , # ص
    'D' : '\u0636' , # ض
    'T' : '\u0637' , # ط
    'Z' : '\u0638' , # ظ
    'E' : '\u0639' , # ع
    'g' : '\u063A' , # غ
    ' ' : '\u0020' , #Space is replaced by space 
    '_' : ' ' , #ـ    This is Temporary
    # '_' : '\u0640' , #ـ
    'f' : '\u0641' , # ف
    'q' : '\u0642' , # ق
    'k' : '\u0643' , # ك
    'l' : '\u0644' , # ل
    'm' : '\u0645' , # م
    'n' : '\u0646' , # ن
    'h' : '\u0647' , # ه
    'w' : '\u0648' , # و
    'Y' : '\u0649' , # ى
    'y' : '\u064A' , # ي
    'F' : '\u064B' , # TANWEEN FATH  ً
    'N' : '\u064C' , #TANWEEN DHAM  ٌ
    'K' : '\u064D' , #TANWEE KASR  ٍ
    'a' : '\u064E' , #FATHA  َ
    'u' : '\u064F' , #DHAMMA  ُ
    'i' : '\u0650' , #KASRA  ِ
    '~' : '\u0651' , # SHADDAH  ّ
    'o' : '\u0652' , #SUKON  ْ
    '`' : '\u0670' , # SHORT ALEF (dagger alif) ٰ
    '{' : '\u0671' , #AL WITH HAMZA QATE'/WASEL MARK ٱ
    'P' : '\u067E' , # پ 
    'J' : '\u0686' , # چ 
    'V' : '\u06A4' , # ڤ 
    'G' : '\u06AF' , # گ 
    '-' : '\u06EA' , # ۪ Not BW standerd
    '#' : '\u0654' , # ٔ  ARABIC HAMZA ABOVE   Not BW standerd
    ':' : '\u06DC ' , # short sen ۜ  Not BW standerd  
    '"' : '\u06E0' , # small circle ۟  ,Not BW standerd
    '[' : '\u06E2' , # short meem ۢ  , Not BW standerd
    ';' : '\u06E3 ' , #small sen below letter  ۣ  , Not BW standerd
    ',' : '\u06E5 ' , # samall wa ۥ  , Not BW standerd
    '.' : '\u06E6' , # ۦ   Not BW standerd
    '!' : '\u06E8 ' , # small noon ۨ  Not BW standerd
    '-' : '\u06EA' , # special qura'nic arabic ( littel circule underneath), is not part of standerd BW , not in Buckwalter ۪  Not BW standerd
    '%' : '\u06EC' , # small solid circle ۬  Not BW standerd
    ']' : '\u06ED ',  # small meem ۭ  Not BW standerd
    '0' : '0' , #
    '1' : '1' , #
    '2' : '2' , #
    '3' : '3' , #
    '4' : '4' , #
    '5' : '5' , #
    '6' : '6' , #
    '7' : '7' , #
    '8' : '8' , #
    '9' : '9'  #
}
# A transliterate Function to transliterate Arabic letters and vice versa
#It takes a text and the schema as input and return 2-values: the transliteration and a flag of whether all chars are transliterated or not
def perform_transliteration(text , schema ):
    """
    This method takes a text and a schema as input and returns a tuple of two values: the transliteration of the text based on the given schema and a flag indicating whether all characters in the text were transliterated or not.

    Args:
        text (:obj:`str`): The input text to be transliterated.
        schema (:obj:`str`): The transliteration schema to be used. Should be either `bw2ar` to transliterate Buckwalter-encoded Arabic text to Arabic script, or `ar2bw` to transliterate Arabic script to Buckwalter-encoded Arabic text.

    Returns:
        :obj:`tuple`: A tuple of two values:
        - The transliterated text based on the given schema.
        - A boolean flag indicating whether all characters in the input text were successfully transliterated or not.

    **Example:**

    .. highlight:: python
    .. code-block:: python

        from nlptools.utils import text_transliteration

        print(text_transliteration.perform_transliteration("مُحَمَدٌ نَـشِيْطٌـ1"  , "ar2bw"))
        print(text_transliteration.perform_transliteration("muHamadN"  , "bw2ar"))
        print(text_transliteration.perform_transliteration("شَنُعُ۪ـ1"  , "ar2bw"))
        print(text_transliteration.perform_transliteration("$aw~aH_2"  , "bw2ar"))

        #output
        ('muHamadN na_$iyoTN_1', True)
        ('مُحَمَدٌ', True)
        ('$anuE-u_1', True)
        ('شَوَّح 2', True)
    """
    # to map BW into Arabic  
    if schema == "bw2ar":
        transliterated_text = deque() #Empty deque list
        
        is_all_mapped = True
        for char in text:
            # lockup every charecters in the dictionary, if not found return the original char 
            char_value = bw2ar_map.get(char)
   
            if char_value is None:
                is_all_mapped = False  # False if one cjars is not in map
                transliterated_text.append(char)
            else:
                transliterated_text.append(char_value)

        return ''.join(transliterated_text)  , is_all_mapped
    # to map Arabic into BW
    elif schema == "ar2bw":

        transliterated_text = deque()
   
        is_all_mapped = True
        for char in text:
            # lockup evry charecters in the dictionary, if not found return the original char 
            char_value = ar2bw_map.get(char)
          
            if char_value is None:
                is_all_mapped = False   # False if one cjars is not in map
                transliterated_text.append(char)
            else:
                transliterated_text.append(char_value)

        return ''.join(transliterated_text)  , is_all_mapped

    else:
        raise ValueError("Schema must be either 'bw2ar' or 'ar2bw'.")
