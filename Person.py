
from copy import deepcopy
class Person:
    def __init__(self, original_dna, encoding_dict, num_generations, fitnessFunc, fitness=None, new_dna = None):
        self.original_dna = original_dna
        self.encoding_dict = encoding_dict
        self.num_generations = num_generations
        self.fitnessFunc = fitnessFunc
        if new_dna == None:
            self.new_dna = self.get_new_dna()
        else:
            self.new_dna = new_dna

        if fitness == None:
            self.calculateFitness()
        else:
            self.fitness = fitness

        
    #generate the new dna from the coded one using the dictionary
    def get_new_dna(self):
        spaceDict = {' ': ' ', '\n ': '\n', ',': ',', '.': '.', ';': ';'}
        temp_dict = {**self.encoding_dict, **spaceDict}
        new_string = ""
        for x in self.original_dna:
            new_string += temp_dict[x]
        return new_string

    def calculateFitness(self):
        self.fitness = self.fitnessFunc.generateScore(self.new_dna)
    
    # def changeEncodingDict(self, newDict: dict) -> None:
    #     self.encoding_dict = newDict
    
    def getEncodingDict(self) -> dict:
        return self.encoding_dict
    
    def getFitness(self):
        return self.fitness

    def deepcopy(self):
        encoding_dict = deepcopy(self.encoding_dict)
        newPerson = Person(self.original_dna, encoding_dict, self.num_generations, self.fitnessFunc, self.fitness, self.new_dna)
        return newPerson
    