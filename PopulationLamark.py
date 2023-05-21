import random, string, re, math
import Person, Mutations
from Fitness import Fit
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
    def __naturalSelection(self, percent):

        # devidor = self.__getDevidor(percentileNum)
        temp = []
        people_to_remove = int(self.size * percent)
        temp = self.population[:self.size - people_to_remove]
        self.population = temp


    def dispachBestPeople(self, bestPeople):


        newPop = []
        for person in bestPeople:
            # create new copies of the best individual (5% of the new population)
            percent = person.getFitness()/10
            amount = math.ceil((60/100)*percent)
            for i in range(amount):
                newPop.append(self.bestPerson.deepcopy())
        
        return newPop


    def nextGen(self, mutationChance, deathThreshold, localOpositions):
        self.population = sorted(self.population, key=lambda p: p.fitness, reverse=True)
        # Remove individuals with low fitness
        self.__naturalSelection(deathThreshold)
        

        # get the individual with the best fitness and then remove it from the current population
        # self.bestPerson = self.__getBestPerson()

        
        self.bestPerson = self.population[0]


        newPopulation = self.dispachBestPeople(self.population[:5])

        
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
        
        for person in self.population:
            newPerson = person.deepcopy()
            for i in range(localOpositions):
                Mutations.switchMutation(newPerson)
            
            if newPerson.fitness > person.fitness:
                person.fitness = newPerson.fitness
                person.new_dna = newPerson.new_dna
                person.encoding_dict = newPerson.encoding_dict
     
    
if __name__ == "__main__":
    text = ""
    with open('/Users/chenbistra/Documents/repos/comp_bio_targil2/enc.txt', 'r') as f:
        text = f.read()

    text = re.sub(r"\s+", " ", text)

    popy = Population(60, text)
    # deathTreshold = 5
    # breakPoint=93
    convergenceMax = 10
    convergenceCount = 0
    generationCounter = 0
    lastBestFit = 0
    while convergenceCount < convergenceMax:
        generationCounter += 1
        popy.nextGen(mutationChance=0.6, deathThreshold=0.2, localOpositions=5)
        print("best person fitness:", float(popy.bestPerson.fitness))
        if popy.bestPerson.fitness == lastBestFit:
            convergenceCount += 1
        else:
            convergenceCount = 0
        lastBestFit = popy.bestPerson.fitness

        # if popy.bestPerson.getFitness() >= breakPoint:
        #     print(popy.bestPerson.getFitness())
        #     print(popy.bestPerson.new_dna)
        #     break
    print(popy.bestPerson.new_dna)
    print("number of generations:", generationCounter)
    print("number of calls to fit:", popy.fitness.fitnessCallCount)
    
        



