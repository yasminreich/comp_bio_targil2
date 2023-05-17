import re
import numpy as np

FREQ2_REGEX = r"^(\d*\.\d+|\d+)\t(\w\w)$"

class Fit:
    def __init__(self, pathToDict, pathTofreq2):
        self.dictWords = set(self.__generateDictionary(pathToDict))
        self.freq2 = self.__generate2Freq(pathTofreq2)

    def __generateDictionary(self, pathToDictionary):
        with open(pathToDictionary, "r") as f:
            return {word.lower() for word in f.read().split("\n")}

    def __generate2Freq(self, pathTofreq2):
        returnDict = {}
        with open(pathTofreq2, "r") as f:
            for line in f:
                match = re.match(FREQ2_REGEX, line)
                if match:
                    returnDict[match.group(2).lower()] = float(match.group(1))
        return returnDict

    def __getWordScore(self, word):
        if word.lower() in self.dictWords:
            return 100

        score = 0
        count = len(word) - 1

        if count == 0:
            return 100 if word in {"a", "i"} else 0

        subwords = [word[i:i+2] for i in range(count)]
        valid_subwords = [subword for subword in subwords if all(symbol not in subword for symbol in (",", ".", ";"))]
        scores = np.array([self.freq2.get(subword, 0) for subword in valid_subwords])
        score = np.sum(scores) * 1000

        return score / count

    def generateScore(self, sentence):
        words = sentence.split()
        scores = np.array([self.__getWordScore(word) for word in words])
        return np.mean(scores)
