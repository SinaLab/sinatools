
#  The Imply algorithm takes two words as input and produces the matching tuple defined by (Words Matching).
#  The matching between two words is defined as a tuple:
#  <w1, w2, implication direction, distance, conflicts, verdict, preferredWord> .

from nlptools.utils.parser import arStrip
class Implication:
    """
    The implication class computes whether the two Arabic words are the same or not, regardless of how they are diacritized. The output also contains implication direction, distance, number of conflicts, and other outputs. 
    Argd:
        :obj:`str' word1: input text
        :obj:`str' word2: input text

    """
    # Diacritic Pair Distance Map
    distanceTable = [
    [0, 0, 1, 1, 1, 1, 1, 1, 15, 16, 16, 16, 0, 0, 0, 0 ],
    [0, 0, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 0, 0, 0, 0],
    [1, 101, 0, 101, 101, 101, 101, 101, 101, 101, 101, 101, 0, 0, 0, 0],
    [1, 101, 101, 0, 101, 101, 101, 101, 101, 101, 101, 101, 0, 0, 0, 0],
    [1, 101, 101, 101, 0, 101, 101, 101, 101, 101, 101, 101, 0, 0, 0, 0],
    [1, 101, 101, 101, 101, 0, 101, 101, 101, 101, 101, 101, 0, 0, 0, 0],
    [1, 101, 101, 101, 101, 101, 0, 101, 101, 101, 101, 101, 0, 0, 0, 0],
    [1, 101, 101, 101, 101, 101, 101, 0, 101, 101, 101, 101, 0, 0, 0, 0],
    [15, 101, 101, 101, 101, 101, 101, 101, 0, 1, 1, 1, 0, 0, 0, 0],
    [16, 101, 101, 101, 101, 101, 101, 101, 1, 0, 101, 101, 0, 0, 0, 0],
    [16, 101, 101, 101, 101, 101, 101, 101, 1, 101, 0, 101, 0, 0, 0, 0],
    [16, 101, 101, 101, 101, 101, 101, 101, 1, 101, 101, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 100, 100],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 100, 0, 100],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 100, 100, 0]
    ]

    # Implication direction  Map
    directionTable =[
    [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [2, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0],
    [2, -1, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0],
    [2, -1, -1, 3, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0],
    [2, -1, -1, -1, 3, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0],
    [2, -1, -1, -1, -1, 3, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0],
    [2, -1, -1, -1, -1, -1, 3, -1, -1, -1, -1, -1, 0, 0, 0, 0],
    [2, -1, -1, -1, -1, -1, -1, 3, -1, -1, -1, -1, 0, 0, 0, 0],
    [2, -1, -1, -1, -1, -1, -1, -1, 3, 1, 1, 1, 0, 0, 0, 0],
    [2, -1, -1, -1, -1, -1, -1, -1, 2, 3, -1, -1, 0, 0, 0, 0],
    [2, -1, -1, -1, -1, -1, -1, -1, 2, -1, 3, -1, 0, 0, 0, 0],
    [2, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, -1, -1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, -1, 3, -1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, -1, -1, 3]
    ]

    word1 , word2 = "" , "" # two words to be compared
    conflictFlags =  [False for i in range(5)] 
    verdict = "null"    # verdict:  takes one of the values: “compatible”, or “incompatible”
    word1Undiac = ""    # word1 without diacritics 
    word2Undiac = ""    # word2 without diacritics 
    word1Diacritics = [] # Diacritics array of the first word
    word2Diacritics = [] # Diacritics array of the second word
    direction = -2147483648 # direction: is a number denoting the relationship between the two words, the defult value is given a low integer, arbitrarry value
    distance = -2147483648 # distance: denotes the overall similarity of the diacritization between the two words, which we compute based on the distance map; the defult value is given a low integer, arbitrarry value
    conflicts = -2147483648 # conflict: denotes the number of conflicting diacritics between the two words, the defult value is given a low integer, arbitrarry value
    lettersDirection = [] # implication direction between diacritics 

    def __init__(self , inputWord1 ,  inputWord2):
        
        #check if inputWord1 or inputWord2 is empty, then return the values below
        if ( (not inputWord1) and (inputWord2) ) or  ( ( inputWord1) and (not inputWord2) ):
            self.verdict = "Incompatible"
            self.direction = -3 # the two words have different letters
            self.distance = 3000
            self.conflicts = 0
            return

        self.conflictFlags =  [False for i in range(5)] # reset conflictFlags array to Fales
        self.word1 = Implication.normalize_alef(inputWord1) # unify alif 
        self.word2 = Implication.normalize_alef(inputWord2) # unify alif 

        if ( self.word1 ==  self.word2): # If w1 == w2 returns the values bellow 
            self.verdict = "Compatible"
            self.direction = 3 #  Both letters have exactly the same diacritics 
            self.distance = 0
            self.conflicts = 0
            return
        else: # If w1 and w2 are noot exact match
            try:
                self.lettersDirection = []
                # build diacritics array for each word 
                self.word1Diacritics = Implication.get_diacritics_array(self.word1)
                self.word2Diacritics = Implication.get_diacritics_array(self.word2)

                 # defined lettersDirection array with size of word1Diacritics and fill it by zeros
                for x in range(0 , len(self.word1Diacritics) + 1): 
                    self.lettersDirection.append(0)
            except :
                # In case of errors returns the values below 
                self.verdict = "Incompatible"
                self.direction = -3 # the two words have different letters
                self.distance = 3000
                self.conflicts = 0
                return

            # check if diacritics in both words for some of syntax errors then return Incompatible
            if (  Implication.diacritics_syntax_error_in(self.word1Diacritics) == False and  Implication.diacritics_syntax_error_in(self.word2Diacritics) == False) : 
                # If no syntax error found:
                self.word1Undiac = arStrip(self.word1, diacs=False, shaddah=False)
                self.word2Undiac = arStrip(self.word2, diacs=False, shaddah=False)
                # return compatible if each word is one and same letter regardless of diacritics on this letter
                if (len(self.word1Undiac) == 1 and len(self.word2Undiac) == 1 and self.word1Undiac == self.word2Undiac): 
                        self.verdict = "Compatible"
                        self.direction = 3  #  Both letters have exactly the same diacritics 
                        self.distance = 0
                        self.conflicts = 0
                else : # If words are more than letter or deffirent letter then calculate the impication
                    self.lettersDirection[0] = 3 
                    self.calculate_words_implication()
                
            else : # If found syntax error in diacitics in word1 or word2 then return these:
                self.verdict = "Incompatible"
                self.direction = -3 # the two words have different letters
                self.distance = 3000
                self.conflicts = 0
            
    def get_non_preferred_word(self, word1, word2):
        """
        This method returns the non-preferred word from two given words.

        Args:
            :obj:`str' word1: The first word.
            :obj:`str' word2: The second word.

        Returns:
            :obj:`str': The non-preferred word.

        Raises:
            None
        """
        # this function talkes 2-words and retuen preferredWord 
        word1 = word1.strip()
        word2 = word2.strip()
        if (word1 != None and  word1 ) :
            if (word2 != None and word2) :
                preferredWord = ""
                preferredWord = Implication.getPreferredWord(word1, word2)
                if word1== preferredWord:
                    return word2
                else:
                    return word1
            else :
                return word1
        
        else :
            if word2 != None and word2:
                return word2 
            else:
                return None
    


    def get_preferred_word( self , word1,   word2) :
        """
        This method returns the preferred word from two given words.

        Args:
            :obj:`str' word1: The first word.
            :obj:`str' word2: The second word.

        Returns:
            :obj:`str': The preferred word.

        Raises:
            None
        """        
        word1 = word1.strip()
        word2 = word2.strip()
        if ( word1 != None and word1) :
            if (word2 != None and word2) :
                implication =  Implication(word1, word2) 
                direction = implication.get_distance()
                if (direction < 15) :
                    if ( ( direction == 0 ) or
                       (direction == 2 ) ):
                        return word1
                    elif direction == 1 :
                        return word2
                    elif direction == 3 :
                        if ( ( not word1.endswith("َ") ) and ( not word1.endswith("ُ") ) ) : 
                            return word2
                        return word1

                return ""
            else :
                return word1
        
        else :
            if word2 != None and (not word2):
                return  word2
            else:
                return None
            
    def normalize_alef(word):
        """
        This method normalizes the alif (ألف) character in the given word.

        Args:
            word (:obj:`str`): The input word to be normalized.

        Returns:
            :obj:`str`: The normalized word with alif characters modified.

        **Example:**

        .. highlight:: python
        .. code-block:: python

            from nlptools.utils.implication import Implication

            word = Implication.normalize_alef("ًى")  # Returns "ىً"
            word = Implication.normalize_alef("ًا")  # Returns "اً"
            word = Implication.normalize_alef("ٱلكتاب")  # Returns "الكتاب"
        """
        # If the tanween is before the alif, then it is placed after it,
        # because in the Arabic language this word is similar
        if word.endswith("ًى"):
            word = word[:len(word) - 2] + "ىً"

        if word.endswith("ًا"):
            word = word[:len(word) - 2] + "اً"
        # Replace Alif-dhamma with Alif
        if word.startswith("ٱ"):
            word = "ا" + word[1:]
        return word


    def diacritics_syntax_error_in( diacriticsArray ) :
        """
        This method checks if the diacritics in a given array are incorrect.

        Args:
            diacritics_array (:obj:`list`): A list of diacritics to be checked.

        Returns:
            :obj:`bool`: True if there is a syntax error in the diacritics, False otherwise.

        **Example:**

        .. highlight:: python
        .. code-block:: python

            from nlptools.utils.implication import Implication 

            diacritics = ["َ", "ُ", "ِ", "ّ"]
            has_error = Implication.diacritics_syntax_error_in(diacritics)  # Returns False

            diacritics = ["َ", "ُ", "ِ", "ٓ"]
            has_error = Implication.diacritics_syntax_error_in(diacritics)  # Returns True
        """
        # This funcion return True when the diacritics is incorreclty 
        try:
            # check last letter diacritic
            if ( Implication.wrong_end_diacritic(diacriticsArray[ len(diacriticsArray) - 1]) ) : 
                return True
            else :
                # check All letters diacritic except the last letter diacritic
                for i in range(0 , len(diacriticsArray) - 1 ) :
                    if (Implication.wrong_middle_iacritic(diacriticsArray[i])) :
                        return True 
                return False
            
        except :
            return False
        

    def wrong_end_diacritic(diac):
        """
        This method checks if the given diacritic is a wrong end diacritic.

        Args:
            diac (:obj:`int`): The diacritic value to be checked.

        Returns:
            :obj:`bool`: True if the diacritic is one of the follwoing number (85:SHADDAH WITH FATHATAN, 86:SHADDAH WITH KASRTA, 87:SHADDAH WITH DHAMTAN), False if diacritic is greator than or equal0 and diacritic is less than or equal 11.

        **Example:**

        .. highlight:: python
        .. code-block:: python

            from nlptools.utils.implication import Implication 

            diacritic = 0
            is_wrong_end = Implication.wrong_end_diacritic(diacritic)  # Returns False

            diacritic = 85
            is_wrong_end = Implication.wrong_end_diacritic(diacritic)  # Returns True
        """
        # 0 > No Diacritics , 1 > SUKUN, 2 > FATHA, 3 > KASRA, 4 > DAMMA, 5 > FATHATAN, 6 > KASRATAN,
        #  7 > DAMMATAN, 8 > SHADDA, 9 > SHADDA with FATHA, 10 > SHADDA with KASRA, 11 > SHADDA with DAMMA
        if (diac >= 0 and diac <= 11) :
            return False
        else :
            # 85 - 86 - 87: SHADDAH WITH FATHATAN,SHADDAH WITH KASRTA, SHADDAH WITH DHAMTAN
            return diac < 85 or diac > 87
        
    def wrong_middle_iacritic( diac) :

        if (diac >= 0 and diac <= 4) :
            return False
        else :
            return diac < 8 or diac > 15
            
    
    def calculate_words_implication(self):
        """
        This method calculates the implication between two words, and updates the verdict, direction, distance, and conflicts attributes of the object based on the implication between the words.

        Returns:
            None

        **Example:**

        .. highlight:: python
        .. code-block:: python

            from nlptools.utils.implication import Implication

            implication = Implication(word1, word2)
            implication.calculate_words_implication()
            # Access the updated attributes
            verdict = implication.verdict
            direction = implication.direction
            distance = implication.distance
            conflicts = implication.conflicts
        """

        self.verdict = "Incompatible"
        self.direction = -2 
        self.distance = 1000
        if (Implication.equal_words(self) == False): # If both words are not thge same return these values 
            if ((len(self.word1Undiac) == 0 and len(self.word2Undiac) == 0)):
                if (self.word1 == self.word2): 
                    self.conflicts = 0
                    self.distance = 0
                    self.direction = 3 
                else:
                    self.conflicts = 1
                    self.distance = 1000
                    self.direction = -2 
                
            else:
                self.conflicts = max(len(self.word1Undiac), len(self.word2Undiac))
            
        else:
            if (Implication.calculate_letters_implication(self)):
                self.direction = Implication.calculate_direction(self)
                if (self.direction == -1) :
                    self.distance = 101
                else:
                    self.verdict = "Compatible"
                
            else:
                self.direction = -3 # the two words have different letters
                self.distance = 3000
                self.conflicts = 0

    def equal_words( self ) :
        """
        This method updates the word1Undiac and word2Undiac attributes by removing the first letter, and returns True if the words are equal, False otherwise. 

        Returns:
            :obj:`bool`: True if the words are equal, False otherwise.

        **Example:**

        .. highlight:: python
        .. code-block:: python

            from nlptools.utils.implication Implication

            implication = Implication(word1, word2)
            result = implication.equal_words()
            if result:
                print("The words are equal")
            else:
                print("The words are not equal")
        """
       # check if the tow words are the same taking into account the alif as the first letter 
        word1FirstLetter = self.word1Undiac[0 : 1] # First letter in word1 
        word2FirstLetter = self.word2Undiac[0 : 1] # First letter in word2 
        self.word1Undiac =  self.word1Undiac[1 : ] # all word1 letters without diacritics except first letter 
        self.word2Undiac =  self.word2Undiac[1 : ] # all word2 letters without diacritics except first letter 
        
        # If both words withot first letter are not equal return false, otherwise continue 
        if ( self.word1Undiac != self.word2Undiac):
            return False

        # If the first letter in both words the same and (the other letters are the same) then return true, otherwise continue  
        if word1FirstLetter == word2FirstLetter :
            return True

        # check if first letter is any alif (the other letters are the same) then return below values 
        if (word1FirstLetter != "ا" or word2FirstLetter != "آ" and word2FirstLetter != "أ" and word2FirstLetter != "إ") :
            if ((word1FirstLetter == "آ" or word1FirstLetter == "أ" or word1FirstLetter == "إ") and word2FirstLetter == "ا") :
                self.lettersDirection[0] = 2 # w2 implies w1
                self.conflictFlags[3] = True
                return True
            else:
                return False
        else:
            self.lettersDirection[0] = 1 # w1 implies w2
            self.conflictFlags[2] = True
            return True
        
        return False

       
    def calculate_letters_implication(self) :
        """
        This method updates the lettersDirection, conflictFlags, and distance attributes based on the directionTable and distanceTable values for each pair of diacritics. It returns True after the calculation is completed.

        Returns:
            :obj:`bool`: True indicating the calculation is completed.

        **Example:**

        .. highlight:: python
        .. code-block:: python

            from nlptools.utils.implication import Implication

            implication = Implication(word1, word2)
            result = implication.calculate_letters_implication()
            if result:
                print("Letters implication calculation completed")
        """
        self.distance = 0
        word1Diac = 0
        word2Diac = 0
  
        for i in range ( 0 , len(self.word1Diacritics) - 1) :
            word1Diac = self.word1Diacritics[i];
            word2Diac = self.word2Diacritics[i];

            self.lettersDirection[i + 1] = self.directionTable[word1Diac][word2Diac];
            self.conflictFlags[self.lettersDirection[i + 1] + 1] = True;
            self.distance = self.distance + self.distanceTable[word1Diac][word2Diac];

               
        word1Diac = int( self.word1Diacritics[len(self.word1Diacritics) - 1] ) # last letter diacritics to word1
        word2Diac = int( self.word2Diacritics[len(self.word1Diacritics) - 1] ) # last letter diacritics to word2
        # 8: expresses the presence of shaddah
        if (word1Diac == 8 or word2Diac == 8) :
            self.lettersDirection[len(self.lettersDirection) - 1] = self.directionTable[word1Diac][word2Diac]
            self.conflictFlags[self.lettersDirection[len(self.lettersDirection) - 1] + 1] = True
            self.distance = self.distance + self.distanceTable[word1Diac][word2Diac]
        return True

        
    def calculate_direction(self ): 
        """
        This method calculates the direction of compatibility based on a conflict flags.

        Returns:
            :obj:`int`: The direction of compatibility:
               -1: Incompatible-diacritics
                0: Compatible-imply each other
                1: Compatible-w1 implies w2
                2: Compatible-w2 implies w1
                3: Compatible-exactly equal
                -2147483648: Default value for an invalid direction
        """
        self.conflicts = 0
        if (self.conflictFlags[0] == True): 
            return -1 # Incompatible-diacritics
        
        if (self.conflictFlags[2] == True and self.conflictFlags[3] == True ):
            return 0 # Compatible-imply each other
        
        if (self.conflictFlags[2] == True and self.conflictFlags[3] == False ):
            return 1 # Compatible-w1 implies w2
        
        if (self.conflictFlags[2] == False and self.conflictFlags[3] == True ):
            return 2 # Compatible-w2 implies w1
        
        if (self.conflictFlags[4]):
            return 3 # Compatible-exactly equal
        return -2147483648



    def get_diacritics_array(word): 
        """
        This method converts diacritics in a word to digits and returns the array of diacritics.

        Args:
            word (:obj:`str`): The word with diacritics.

        Returns:
            :obj:`list`: The array of diacritics converted to digits.

        Raises:
            Exception: If the first character of the word is a digit.

        **Example:**

        .. highlight:: python
        .. code-block:: python

            from nlptools.utils.implication import Implication
            word = "مُرَحَّبًا"
            diacritics = Implication.calculate_direction(word)
            print(diacritics)
            Output: [4, 3, 8, 5, 0]
        """ 
        # Replace diacritics by digits 
        word = word.replace(" ", "") #Space
        word = word.replace("ْ", "1") #SUKUN  
        word = word.replace("َ", "2") #FATHA
        word = word.replace("ِ", "3") #KASRA
        word = word.replace("ُ", "4") #DAMMA
        word = word.replace("ً", "5") #FATHATAN
        word = word.replace("ٍ", "6") #KASRATAN
        word = word.replace("ٌ", "7") #DAMMATAN
        word = word.replace("ّ", "8") #SHADDA
        word = word.replace("11", "100") #SUKUN with SUKUN
        word = word.replace("12", "100") #SUKUN with FATHA
        word = word.replace("13", "100") #SUKUN with KASRA
        word = word.replace("14", "100") #SUKUN with DAMMA
        word = word.replace("15", "100") #SUKUN with FATHATAN
        word = word.replace("82", "9") #SHADDA with FATHA
        word = word.replace("83", "10") #SHADDA with KASRA
        word = word.replace("84", "11") #SHADDA with DAMMA
          # Standardization Alif
        word = word[0 : 1].replace("ا", "ا12,") + word[1: ] 
        word = word[0 : 1].replace("أ", "ا13,") + word[1: ] 
        word = word[0 : 1].replace("إ", "ا14,") + word[1: ] 
        word = word[0 : 1].replace("آ", "ا15,") + word[1: ] 
        if word[0:1].isdigit(): # Because a word should not begin with a diacritics 
            raise Exception("Sorry, First char is digit")
        else:
            # word = re.sub(r'[\u0600-\u06FF]' , ",",word) # replace all chars with ,
            for x in word: 
                if ( ( x.isalpha() or not x.isdigit() ) and x != ',' ): # If char is not digit then replace it by , 
                    word = word.replace(x , ",")
            # word = word.replace("\\D", ",")
            word = word[0 : len(word) - 1] + word[ len(word ) - 1].replace(",", ",,") # last letter does not have diacritic problem
           
            while ( ",," in word ):
                word = word.replace(",,", ",0,") # No-DIACRITIC 
            
            word = word[1 : len(word) ] # Ignore the first letter diacritic 
            diacritics = []
            diacritics = word.split(",") # diacritics is array of diacritics
            if '' in diacritics: # Remove empty index if exist
                diacritics.remove('')
            var3 = diacritics[len(diacritics) - 1] # last letter diacritic


            # SHADDA with FATHA,SHADDA with KASRA,SHADDA with DAMMA,SHADDAH WITH FATHATAN,SHADDAH WITH KASRTA, SHADDAH WITH DHAMTAN
            if var3 == "8" or var3 == "9" or var3 == "10" or var3 == "11" or var3 == "85" or var3 == "86" or var3 == "87":
                diacritics[len(diacritics )- 1] = "8"
                     # SUKUN , FATHA , KASRA , DAMMA , FATHATAN , KASRATAN , DAMMATAN 
            elif var3 == "1" or var3 == "2" or var3 == "3" or var3 == "4" or var3 == "5" or var3 == "6" or var3 == "7":
                diacritics[len(diacritics )- 1] = "0"
        
        strDiacritics = []
        strDiacritics = diacritics
        
        # Convert string array digits to integer digits array 
        for x in range(0 , len(strDiacritics) ):
            diacritics[x] = int(strDiacritics[x])
        return diacritics
    
    # def removeDiacritics( word ): # remove all diacritics from Arabic word
    #     word = word.replace(" ", "")
    #     word = word.replace("ْ", "") #SUKUN
    #     word = word.replace("َ", "") #FATHA
    #     word = word.replace("ِ", "") #KASRA
    #     word = word.replace("ُ", "") #DAMMA
    #     word = word.replace("ً", "") #FATHATAN
    #     word = word.replace("ٍ", "") #KASRATAN
    #     word = word.replace("ٌ", "") #DAMMATAN
    #     word = word.replace("ّ", "") #SHADDA
    #     return word

    def get_letters_array(word):
        """
        This method returns the array of letters from a given word.

        Args:
            word (:obj:`str`): The word from which to extract the letters.

        Returns:
            obj:`list`: The array of letters.

        **Example:**

        .. highlight:: python
        .. code-block:: python

            from nlptools.utils.implication import Implication
            word = "مرحبا"
            letters = get_letters_array(word)
            print(letters)
            Output: ['م', 'ر', 'ح', 'ب', 'ا']
        """
        word = arStrip(word, diacs=False, shaddah=False)
        return list(word)

    def get_verdict(self ): 
        return self.verdict


    def get_direction(self): 
        return self.direction


    def get_distance(self) :
        return self.distance


    def get_conflicts(self) :
        return self.conflicts


    def get_word1(self) :
        return self.word1


    def get_word2(self) :
        return self.word2 

    def get_result(self):
        """
        This method returns the result of the comparison between two words.

        Returns:
            :obj:`str`: The result of the comparison. Can be *Same* or *Different*.

        **Example:**

        .. highlight:: python
        .. code-block:: python

            from nlptools.utils.implication import Implication
            w1 = "hello"
            w2 = "hell"
            implication = Implication(w1, w2)
            result = implication.get_result()
            print(result)
            Output: "Same"
        """
        if Implication.get_direction(self) >= 0 and Implication.get_distance(self) < 15:
            self.result = "Same"
        else:
            self.result = "Different"
        return self.result

    def toString(self) :
        return self.word1 + "\t" + self.word2 + "\t" + str(self.verdict) + "\t" + str(self.direction) + "\t" + str(self.distance) + "\t"+ str(self.conflicts)
