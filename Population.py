import random, string
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
    def __naturalSelection(self, deathThreshold):
        for person in self.population:
            if person.getFitness() < deathThreshold:
                self.population.remove(person)
    
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


    def nextGen(self, mutationChance, bestPersonCoverage, deathThreshold, percentileNum):
        # Remove individuals with low fitness
        self.__naturalSelection(deathThreshold)
        newPopulation = []

        # get the individual with the best fitness and then remove it from the current population
        bestPerson = self.__getBestPerson()
        self.population.remove(bestPerson)

        # create new copies of the best individual (5% of the new population)
        bestPersonAmount = int(self.size * bestPersonCoverage)
        for i in range(bestPersonAmount):
            newPopulation.append(deepcopy(bestPerson))
        
        # go through the remaining population and do crossover 
        while True:
            parent1, parent2 = random.sample(self.population, 2)
            child1, child2 = Mutations.crossover(parent1, parent2)
            newPopulation.append(child1)
            if len(newPopulation) == self.size:
                break
            newPopulation.append(child2)
        
        self.population = newPopulation

        devidor = self.__getDevidor(percentileNum)
        for person in self.population:
            if person.getFitness() < devidor and random.random() < 0.2:
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
    popy = Population(100, "abcdefg hijklmnop qrs tuv wx yz")
    popy.nextGen(mutationChance=0.2, bestPersonCoverage=0.05, deathThreshold=20, percentileNum=90)
    
    for i in popy.population:
        Mutations.switchMutation(i)
        print(i.new_dna)
        print(i.fitness)
    


