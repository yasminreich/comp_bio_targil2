import string
import random
import Person

class Population:
    def __init__(self, population_size, code):
        self.size = population_size
        self.code_dna = code
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
            people.append(Person.Person(self.code_dna, self.generate_encoding_dict(), 0))
        return people
    
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
    