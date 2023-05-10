
FREQ2_REGEX = "^(\d*\.\d+|\d+)\t(\w\w)$"
import re
class Fit:

    def __init__(self, pathToDict, pathTofreq2) -> None:
        self.dictWords = list(set(self.__generateDictionary(pathToDict)))
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
        for i in range(len(word) - 1):
            score += self.freq2[word[i:i+2]]
        
        return score *10000/count
        

    def generateScore(self, sentence: str) -> None:
        total = 0
        words = sentence.split(" ")
        for word in words:
            total += self.__getWordScore(word)

        return total/len(words)