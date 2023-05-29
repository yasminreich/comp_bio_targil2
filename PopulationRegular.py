import random, string, re, math
import Person, Mutations
from Fitness import Fit
import numpy as np
from multiprocessing import Pool
import matplotlib.pyplot as plt



class Population:
    def __init__(self, population_size, code):
        self.size = population_size
        self.code_dna = code
        self.fitness = Fit("dict.txt", "Letter2_Freq.txt", "CalculatedWords.json")
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
            percent = person.fitness/10
            amount = math.ceil((self.size/100)*percent)
            for i in range(amount):
                newPop.append(self.bestPerson.deepcopy())
        
        return newPop


    def nextGen(self, mutationChance, deathThreshold):
        self.population = sorted(self.population, key=lambda p: p.fitness, reverse=True)
        # Remove individuals with low fitness
        self.__naturalSelection(deathThreshold)

        
        self.bestPerson = self.population[0]


        newPopulation = self.dispachBestPeople(self.population[:5])

        popForCros = []
        # create vector of people for the crossover
        for person in self.population:
            for _ in range(int(person.fitness)):
                popForCros.append(person.deepcopy())

        
        # go through the remaining population and do crossover 
        while True:
            parent1, parent2 = random.sample(popForCros, 2)
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

    popy = Population(40, text)
    # deathTreshold = 5
    # breakPoint=93
    convergenceMax = 10
    convergenceCount = 0
    generationCounter = 0
    lastBestFit = 0
    graph = {}
    while convergenceCount < convergenceMax:
        generationCounter += 1
        popy.nextGen(mutationChance=0.4, deathThreshold=0.8)
        print("best person fitness:", float(popy.bestPerson.fitness))
        if popy.bestPerson.fitness == lastBestFit:
            convergenceCount += 1
        else:
            convergenceCount = 0
        lastBestFit = popy.bestPerson.fitness
        graph[generationCounter] = lastBestFit


    with open("plain.txt", 'w') as file:
        file.write(popy.bestPerson.new_dna)
    with open("perm.txt", 'w') as file:
        for key, value in popy.bestPerson.getEncodingDict().items():
            file.write(f"{key} {value}\n")
    
    print(generationCounter)
    print(popy.fitness.fitnessCallCount)
    print(popy.bestPerson.new_dna)

    x_values = list(graph.keys())
    y_values = list(graph.values())

    plt.plot(x_values, y_values)
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.title('Best Fitness Per Generation')
    plt.show()
        



