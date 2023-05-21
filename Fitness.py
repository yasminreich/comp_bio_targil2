import re, math
import numpy as np
from Levenshtein import distance

class Fit:
    def __init__(self, pathToDict, pathToFreq2):
        self.dictWords = self.__generateDictionary(pathToDict)
        self.freq2 = self.__generate2Freq(pathToFreq2)
        self.fitnessCallCount = 0

    def __generateDictionary(self, pathToDictionary):
        dictWords = {}
        with open(pathToDictionary, "r") as f:
            words = f.read().split("\n")
            for word in words:
                wordLen = len(word)
                dictWords.setdefault(wordLen, []).append(word)
        return dictWords

    def __generate2Freq(self, pathToFreq2):
        returnDict = {}
        with open(pathToFreq2, "r") as f:
            for line in f:
                match = re.match(r"^(\d*\.\d+|\d+)\t(\w\w)$", line)
                if match:
                    combination = match.group(2).lower()
                    probability = float(match.group(1))
                    returnDict[combination] = probability
        return returnDict



    def __getWordScore(self, word):
        levDistance = 0
        wordLen = len(word)
        if wordLen in self.dictWords:
            if word in self.dictWords[wordLen]:
                return 100
            else:
                levDistance = min([distance(word, dict_word) for dict_word in self.dictWords[wordLen]])
                if levDistance <= math.floor(wordLen/2):
                    return (1 - levDistance / len(word))*100
        
        count = len(word) - 1
        if count == 0:
            return 0
        

        subwords = [word[i:i+2] for i in range(count)]
        valid_subwords = [subword for subword in subwords if all(symbol not in subword for symbol in (",", ".", ";"))]
        scores = np.array([self.freq2.get(subword, 1e-6) for subword in valid_subwords])
        score = np.sum(scores) * 1000

        return score / count


    def generateScore(self, individual):
        self.fitnessCallCount += 1
        words = individual.split()
        scores = np.array([self.__getWordScore(word) for word in words])
        return np.mean(scores)
