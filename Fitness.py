import re, math, os, json
import numpy as np
from Levenshtein import distance

class Fit:
    def __init__(self, pathToDict, pathToFreq2, pathToCalcWords):
        self.dictWords = self.__generateDictionary(pathToDict)
        self.freq2 = self.__generate2Freq(pathToFreq2)
        self.fitnessCallCount = 0
        self.pathToCalcWords = pathToCalcWords
        self.__getCalcWords()
        

    def __getCalcWords(self):
        if os.path.exists(self.pathToCalcWords):
            with open(self.pathToCalcWords) as json_file:
                self.calculatedWords = json.load(json_file)
                
        else: 
            self.calculatedWords = {}
        

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

    def getWordScore(self, word):
        if word in self.calculatedWords:
            return self.calculatedWords[word]
        levDistance = 0
        wordLen = len(word)
        if wordLen in self.dictWords:
            if word in self.dictWords[wordLen]:
                self.calculatedWords.setdefault(word, 100)
                return 100
            else:
                # levDistance = min([distance(word, dict_word) for dict_word in self.dictWords[wordLen]])
                levDistance = min(distance(word, dict_word) for dict_word in self.dictWords[wordLen])
                if levDistance <= math.floor(wordLen/2):
                    score = (1 - levDistance / len(word))*100
                    self.calculatedWords.setdefault(word, score)
                    return score
        
        count = len(word) - 1
        if count == 0:
            return 0
        

        # subwords = [word[i:i+2] for i in range(count)]
        subwords = (word[i:i+2] for i in range(count))
        valid_subwords = [subword for subword in subwords if all(symbol not in subword for symbol in (",", ".", ";"))]
        scores = np.array([self.freq2.get(subword, 1e-6) for subword in valid_subwords])
        score = np.sum(scores) * 1000
        self.calculatedWords.setdefault(word, score / count)
        return score / count

    def generateScore(self, individual):
        self.fitnessCallCount += 1
        words = individual.split()
        scores = np.array([self.getWordScore(word) for word in words])
        return np.mean(scores)

    def calcWordsToJson(self):

        with open(self.pathToCalcWords, "w") as outfile:
            json.dump(self.calculatedWords, outfile)
        print("len dict:", len(self.calculatedWords))
