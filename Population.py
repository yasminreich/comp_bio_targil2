import random, string, re
import Person, Mutations
from Fitness import Fit
from copy import deepcopy
import numpy as np

class Population:
    def __init__(self, population_size, code):
        self.size = population_size
        self.code_dna = code
        self.fitness = Fit("dict.txt", "Letter2_Freq.txt")
        self.population = self.create_initial_population()


    def generate_encoding_dict(self):
        # Get all lowercase letters from the alphabet
        lowercase_letters = string.ascii_lowercase

        # Shuffle the letters randomly
        shuffled_letters = random.sample(lowercase_letters, len(lowercase_letters))

        # Create a dictionary that maps each letter to its shuffled counterpart
        encoding_dict = {}
        for i, letter in enumerate(lowercase_letters):
            encoding_dict[letter] = shuffled_letters[i]

        return encoding_dict


    def create_initial_population(self):
        people = []
        #create a population in size of random permutations
        for x in range(self.size):
            people.append(Person.Person(self.code_dna, self.generate_encoding_dict(), 0, self.fitness))
        return people
    
    # remove individuals with low fitness
    def __naturalSelection(self, percentileNum):

        devidor = self.__getDevidor(percentileNum)
        temp = []

        for person in self.population:
            if person.getFitness() > devidor:
                temp.append(person)
        
        self.population = temp
        

    def __getBestPerson(self):
        bestPerson = self.population[0]
        for person in self.population[1:]:
            if person.getFitness() > bestPerson.getFitness():
                bestPerson = person
        
        return bestPerson

    def __getDevidor(self, percentileNum):
        allFit = []
        for person in self.population:
            allFit.append(person.getFitness())

        arr = np.array(allFit)
        return np.percentile(arr, percentileNum)


    def nextGen(self, mutationChance, bestPersonCoverage, deathThreshold):

        # Remove individuals with low fitness
        self.__naturalSelection(deathThreshold)
        newPopulation = []

        # get the individual with the best fitness and then remove it from the current population
        self.bestPerson = self.__getBestPerson()
        # if bestPerson.getFitness() >= breakPoint:
        #     print(bestPerson.new_dna)
        #     print(bestPerson.getFitness())
        #     break
        # self.population.remove(self.bestPerson)

        # create new copies of the best individual (5% of the new population)
        bestPersonAmount = int(self.size * bestPersonCoverage)
        for i in range(bestPersonAmount):
            newPopulation.append(deepcopy(self.bestPerson))
        
        # go through the remaining population and do crossover 
        while True:
            parent1, parent2 = random.sample(self.population, 2)
            child1, child2 = Mutations.crossover(parent1, parent2)
            newPopulation.append(child1)
            if len(newPopulation) == self.size:
                break
            newPopulation.append(child2)
            if len(newPopulation) == self.size:
                break
        
        self.population = newPopulation

        
        for person in self.population:
            # if person.getFitness() < devidor and random.random() < mutationChance:
            if random.random() < mutationChance:
                Mutations.switchMutation(person)
    
def generate_encoding_dict():
        # Get all lowercase letters from the alphabet
        lowercase_letters = string.ascii_lowercase

        # Shuffle the letters randomly
        shuffled_letters = random.sample(lowercase_letters, len(lowercase_letters))

        # Create a dictionary that maps each letter to its shuffled counterpart
        encoding_dict = {}
        for i, letter in enumerate(lowercase_letters):
            encoding_dict[letter] = shuffled_letters[i]

        return encoding_dict

if __name__ == "__main__":
    text = ""
    # text = "enudcdx ef xjfxuysvciyl mcqeucknecfd, evj mczzcinlecjq jdifndejujm fd evj evjfua fz mjqijde wcev pfmczciyecfd yuj xuyrj jdfnxv. yll evj cdmcrcmnylq fz evj qypj qsjicjq, ydm yll evj qsjicjq fz evj qypj xjdnq, fu jrjd vcxvju xufns, pnqe vyrj mjqijdmjm zufp ifppfd syujdeq; ydm evjujzfuj, cd vfwjrju mcqeyde ydm cqflyejm syueq fz evj wfulm evja yuj dfw zfndm, evja pnqe cd evj ifnuqj fz qniijqqcrj xjdjuyecfdq vyrj syqqjm zufp qfpj fdj syue ef evj fevjuq. wj yuj fzejd wvflla ndyklj jrjd ef ifdhjienuj vfw evcq ifnlm vyrj kjjd jzzjiejm. aje, yq wj vyrj ujyqfd ef kjlcjrj evye qfpj qsjicjq vyrj ujeycdjm evj qypj qsjiczci zfup zfu rjua lfdx sjucfmq, jdfupfnqla lfdx yq pjyqnujm ka ajyuq, eff pniv qeujqq fnxve dfe ef kj lycm fd evj fiiyqcfdyl wcmj mczznqcfd fz evj qypj qsjicjq; zfu mnucdx rjua lfdx sjucfmq fz ecpj evjuj wcll ylwyaq kj y xffm ivydij zfu wcmj pcxuyecfd ka pyda pjydq. y kufojd fu cdejuunsejm uydxj pya fzejd kj yiifndejm zfu ka evj jbecdiecfd fz evj qsjicjq cd evj cdejupjmcyej ujxcfdq. ce iyddfe kj mjdcjm evye wj yuj yq aje rjua cxdfuyde fz evj znll jbejde fz evj ryucfnq ilcpyeyl ydm xjfxuysvciyl ivydxjq wvciv vyrj yzzjiejm evj jyuev mnucdx pfmjud sjucfmq; ydm qniv ivydxjq wcll fkrcfnqla vyrj xujyela zyiclceyejm pcxuyecfd. yq yd jbypslj, c vyrj yeejpsejm ef qvfw vfw sfejde vyq kjjd evj cdzlnjdij fz evj xlyicyl sjucfm fd evj mcqeucknecfd kfev fz evj qypj ydm fz ujsujqjdeyecrj qsjicjq evufnxvfne evj wfulm. wj yuj yq aje sufzfndmla cxdfuyde fz evj pyda fiiyqcfdyl pjydq fz euydqsfue. wcev ujqsjie ef mcqecdie qsjicjq fz evj qypj xjdnq cdvykcecdx rjua mcqeyde ydm cqflyejm ujxcfdq, yq evj sufijqq fz pfmczciyecfd vyq djijqqyucla kjjd qlfw, yll evj pjydq fz pcxuyecfd wcll vyrj kjjd sfqqcklj mnucdx y rjua lfdx sjucfm; ydm ifdqjtnjdela evj mczzcinlea fz evj wcmj mczznqcfd fz qsjicjq fz evj qypj xjdnq cq cd qfpj mjxujj ljqqjdjm."
    with open('/Users/chenbistra/Documents/repos/comp_bio_targil2/enc.txt', 'r') as f:
        text = f.read()

    text = "enudcdx ef xjfxuysvciyl mcqeucknecfd, evj mczzcinlecjq jdifndejujm fd evj evjfua fz mjqijde wcev pfmczciyecfd yuj xuyrj jdfnxv. yll evj cdmcrcmnylq fz evj qypj qsjicjq, ydm yll evj qsjicjq fz evj qypj xjdnq, fu jrjd vcxvju xufns, pnqe vyrj mjqijdmjm zufp ifppfd syujdeq; ydm evjujzfuj, cd vfwjrju mcqeyde ydm cqflyejm syueq fz evj wfulm evja yuj dfw zfndm, evja pnqe cd evj ifnuqj fz qniijqqcrj xjdjuyecfdq vyrj syqqjm zufp qfpj fdj syue ef evj fevjuq. wj yuj fzejd wvflla ndyklj jrjd ef ifdhjienuj vfw evcq ifnlm vyrj kjjd jzzjiejm. aje, yq wj vyrj ujyqfd ef kjlcjrj evye qfpj qsjicjq vyrj ujeycdjm evj qypj qsjiczci zfup zfu rjua lfdx sjucfmq, jdfupfnqla lfdx yq pjyqnujm ka ajyuq, eff pniv qeujqq fnxve dfe ef kj lycm fd evj fiiyqcfdyl wcmj mczznqcfd fz evj qypj qsjicjq; zfu mnucdx rjua lfdx sjucfmq fz ecpj evjuj wcll ylwyaq kj y xffm ivydij zfu wcmj pcxuyecfd ka pyda pjydq. y kufojd fu cdejuunsejm uydxj pya fzejd kj yiifndejm zfu ka evj jbecdiecfd fz evj qsjicjq cd evj cdejupjmcyej ujxcfdq. ce iyddfe kj mjdcjm evye wj yuj yq aje rjua cxdfuyde fz evj znll jbejde fz evj ryucfnq ilcpyeyl ydm xjfxuysvciyl ivydxjq wvciv vyrj yzzjiejm evj jyuev mnucdx pfmjud sjucfmq; ydm qniv ivydxjq wcll fkrcfnqla vyrj xujyela zyiclceyejm pcxuyecfd. yq yd jbypslj, c vyrj yeejpsejm ef qvfw vfw sfejde vyq kjjd evj cdzlnjdij fz evj xlyicyl sjucfm fd evj mcqeucknecfd kfev fz evj qypj ydm fz ujsujqjdeyecrj qsjicjq evufnxvfne evj wfulm. wj yuj yq aje sufzfndmla cxdfuyde fz evj pyda fiiyqcfdyl pjydq fz euydqsfue. wcev ujqsjie ef mcqecdie qsjicjq fz evj qypj xjdnq cdvykcecdx rjua mcqeyde ydm cqflyejm ujxcfdq, yq evj sufijqq fz pfmczciyecfd vyq djijqqyucla kjjd qlfw, yll evj pjydq fz pcxuyecfd wcll vyrj kjjd sfqqcklj mnucdx y rjua lfdx sjucfm; ydm ifdqjtnjdela evj mczzcinlea fz evj wcmj mczznqcfd fz qsjicjq fz evj qypj xjdnq cq cd qfpj mjxujj ljqqjdjm."
    text = re.sub(r"\s+", " ", text)

    popy = Population(100, text)
    # deathTreshold = 5
    breakPoint=70
    while True:
        popy.nextGen(mutationChance=0.4, bestPersonCoverage=0.05, deathThreshold=20)
        print("best person fitness:", float(popy.bestPerson.getFitness()))
        if popy.bestPerson.getFitness() >= breakPoint:
            print(popy.bestPerson.getFitness())
            print(popy.bestPerson.new_dna)
            break
        # deathTreshold = popy.bestPerson.getFitness() * 0.1



    # for i in popy.population:
    #     Mutations.switchMutation(i)
    #     print(i.new_dna)
    #     print(i.fitness)
    


