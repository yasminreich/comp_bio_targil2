import random, string, re, math
import Person, Mutations
from Fitness import Fit
from copy import deepcopy
import numpy as np
from multiprocessing import Pool


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

    def __getDevidor(self, percentileNum):
        allFit = []
        for person in self.population:
            allFit.append(person.getFitness())

        arr = np.array(allFit)
        return np.percentile(arr, percentileNum)

    def dispachBestPeople(self, bestPeople):
        newPop = []
        for person in bestPeople:
            # create new copies of the best individual (5% of the new population)
            amount = math.ceil(person.getFitness()/10)
            for i in range(amount):
                newPop.append(deepcopy(self.bestPerson))
        
        return newPop


    def nextGen(self, mutationChance, deathThreshold):

        # Remove individuals with low fitness
        self.__naturalSelection(deathThreshold)
        

        # get the individual with the best fitness and then remove it from the current population
        # self.bestPerson = self.__getBestPerson()

        sortedPeople = sorted(self.population, key=lambda p: p.fitness, reverse=True)[:5]

        self.bestPerson = sortedPeople[0]

        newPopulation = self.dispachBestPeople(sortedPeople)

        
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



        
    
if __name__ == "__main__":
    text = ""
    with open('/Users/chenbistra/Documents/repos/comp_bio_targil2/enc.txt', 'r') as f:
        text = f.read()

    text = re.sub(r"\s+", " ", text)

    popy = Population(60, text)
    # deathTreshold = 5
    breakPoint=93
    generationCounter = 0
    while True:
        generationCounter += 1
        popy.nextGen(mutationChance=0.6, deathThreshold=20)
        print("best person fitness:", float(popy.bestPerson.getFitness()))
        if popy.bestPerson.getFitness() >= breakPoint:
            print(popy.bestPerson.getFitness())
            print(popy.bestPerson.new_dna)
            break
    print(generationCounter)
        



