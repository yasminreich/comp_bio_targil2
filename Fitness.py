import re, math
import numpy as np
from Levenshtein import distance

class Fit:
    def __init__(self, pathToDict, pathToFreq2):
        self.dictWords = self.__generateDictionary(pathToDict)
        self.freq2 = self.__generate2Freq(pathToFreq2)

    def __generateDictionary(self, pathToDictionary):
        dictWords = {}
        with open(pathToDictionary, "r") as f:
            for word in f.read().split("\n"):
                wordLen = len(word)
                if not wordLen in dictWords.keys():
                    dictWords[wordLen] = [word]
                else:
                    dictWords[wordLen].append(word)
                    
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
        words = individual.split()
        scores = np.array([self.__getWordScore(word) for word in words])
        return np.mean(scores)

# fit = Fit("dict.txt", "Letter2_Freq.txt")
# print(fit.generateScore("enudcdx ef xjfxuysvciyl mcqeucknecfd, evj mczzcinlecjq jdifndejujm fd evj evjfua fz mjqijde wcev pfmczciyecfd yuj xuyrj jdfnxv. yll evj cdmcrcmnylq fz evj qypj qsjicjq, ydm yll evj qsjicjq fz evj qypj xjdnq, fu jrjd vcxvju xufns, pnqe vyrj mjqijdmjm zufp ifppfd syujdeq; ydm evjujzfuj, cd vfwjrju mcqeyde ydm cqflyejm syueq fz evj wfulm evja yuj dfw zfndm, evja pnqe cd evj ifnuqj fz qniijqqcrj xjdjuyecfdq vyrj syqqjm zufp qfpj fdj syue ef evj fevjuq. wj yuj fzejd wvflla ndyklj jrjd ef ifdhjienuj vfw evcq ifnlm vyrj kjjd jzzjiejm. aje, yq wj vyrj ujyqfd ef kjlcjrj evye qfpj qsjicjq vyrj ujeycdjm evj qypj qsjiczci zfup zfu rjua lfdx sjucfmq, jdfupfnqla lfdx yq pjyqnujm ka ajyuq, eff pniv qeujqq fnxve dfe ef kj lycm fd evj fiiyqcfdyl wcmj mczznqcfd fz evj qypj qsjicjq; zfu mnucdx rjua lfdx sjucfmq fz ecpj evjuj wcll ylwyaq kj y xffm ivydij zfu wcmj pcxuyecfd ka pyda pjydq. y kufojd fu cdejuunsejm uydxj pya fzejd kj yiifndejm zfu ka evj jbecdiecfd fz evj qsjicjq cd evj cdejupjmcyej ujxcfdq. ce iyddfe kj mjdcjm evye wj yuj yq aje rjua cxdfuyde fz evj znll jbejde fz evj ryucfnq ilcpyeyl ydm xjfxuysvciyl ivydxjq wvciv vyrj yzzjiejm evj jyuev mnucdx pfmjud sjucfmq; ydm qniv ivydxjq wcll fkrcfnqla vyrj xujyela zyiclceyejm pcxuyecfd. yq yd jbypslj, c vyrj yeejpsejm ef qvfw vfw sfejde vyq kjjd evj cdzlnjdij fz evj xlyicyl sjucfm fd evj mcqeucknecfd kfev fz evj qypj ydm fz ujsujqjdeyecrj qsjicjq evufnxvfne evj wfulm. wj yuj yq aje sufzfndmla cxdfuyde fz evj pyda fiiyqcfdyl pjydq fz euydqsfue. wcev ujqsjie ef mcqecdie qsjicjq fz evj qypj xjdnq cdvykcecdx rjua mcqeyde ydm cqflyejm ujxcfdq, yq evj sufijqq fz pfmczciyecfd vyq djijqqyucla kjjd qlfw, yll evj pjydq fz pcxuyecfd wcll vyrj kjjd sfqqcklj mnucdx y rjua lfdx sjucfm; ydm ifdqjtnjdela evj mczzcinlea fz evj wcmj mczznqcfd fz qsjicjq fz evj qypj xjdnq cq cd qfpj mjxujj ljqqjdjm."))
# print(fit.generateScore("ability aqqqe"))