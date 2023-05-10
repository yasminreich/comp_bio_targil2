
class Person:
    def __init__(self, original_dna, encoding_dict, num_generations):
        self.original_dna = original_dna
        self.encoding_dict = encoding_dict
        self.num_generations = num_generations
        self.new_dna = self.get_new_dna()
        self.fitness = 0
    
    def get_new_dna(self):
        new_string = ""
        for x in self.original_dna:
            new_string += self.encoding_dict[x]
        return new_string
    