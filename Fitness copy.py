
FREQ2_REGEX = "^(\d*\.\d+|\d+)\t(\w\w)$"
import re
class Fit:

    def __init__(self, pathToDict, pathTofreq2) -> None:
        self.dictWords = set(self.__generateDictionary(pathToDict))
        self.freq2 = self.__generate2Freq(pathTofreq2)

    def __generateDictionary(self, pathToDictionary: str) -> list:

        with open(pathToDictionary, "r") as f:
            return f.read().split("\n")

    def __generate2Freq(self, pathTofreq2: str) -> dict:
        returnDict = {}
        with open(pathTofreq2, "r") as f:
            for line in f:

                match = re.match(FREQ2_REGEX, line)
                if match:
                    returnDict[match.group(2).lower()] = float(match.group(1))
                
        return returnDict


    def __getWordScore(self, word: str) -> int:

        if word.lower() in self.dictWords:
            return 100
        score = 0
        count = len(word) - 1

        if count == 0:
            if word == "a" or word == "i":
                return 100
            else:
                return 0 

        for i in range(count):

            subword = word[i:i+2]
            if not "," in subword and not "." in subword and not ";" in subword:
                score += self.freq2[subword]*1000
        
        return score/count
        

    def generateScore(self, sentence: str) -> None:

        total = 0
        word_count = 0
        current_word = ""
        for char in sentence:
            if char == " ":
                if current_word:
                    total += self.__getWordScore(current_word)
                    word_count += 1
                    current_word = ""
            else:
                current_word += char
        
        if current_word:
            total += self.__getWordScore(current_word)
            word_count += 1
        
        return total / word_count 


