
class Person:
    def __init__(self, original_dna, encoding_dict, num_generations, fitness):
        self.original_dna = original_dna
        self.encoding_dict = encoding_dict
        self.num_generations = num_generations
        self.new_dna = self.__get_new_dna()
        self.fitness = fitness.generateScore(self.new_dna)
    
    #generate the new dna from the coded one using the dictionary
    def __get_new_dna(self):
        spaceDict = {' ': ' ', '\n ': '\n', ',': ',', '.': '.', ';': ';'}
        temp_dict = {**self.encoding_dict, **spaceDict}
        new_string = ""
        for x in self.original_dna:
            new_string += temp_dict[x]
        return new_string
    
    # def changeEncodingDict(self, newDict: dict) -> None:
    #     self.encoding_dict = newDict
    
    def getEncodingDict(self) -> dict:
        return self.encoding_dict
    