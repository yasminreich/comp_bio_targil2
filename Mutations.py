import Person, random
import string
def switchMutation(person: Person) -> None:
    keys = list(person.getEncodingDict().keys())
    key1, key2 = random.sample(keys, 2)
    person.getEncodingDict()[key1], person.getEncodingDict()[key2] = person.getEncodingDict()[key2], person.getEncodingDict()[key1]
    person.new_dna = person.get_new_dna()
    person.calculateFitness()

def replace_duplicate_letters(child):
    # Create a set to keep track of previously seen letters
    seen_letters = set()
     # Replace duplicate letters in child
    replaced_child = []
    for char in child:
        if char in seen_letters:
            #insert null if letter allready appeared
            replaced_child.append(None)
        else:
            replaced_child.append(char)
            seen_letters.add(char)
    #now we put the missing letters in the new child
    alphabet = string.ascii_lowercase
    none_indices = [i for i in range(len(replaced_child)) if replaced_child[i] == None]
    remaining_letters = [letter for letter in alphabet if letter not in replaced_child]
    for index in none_indices:
        replaced_child = replaced_child[:index] + [random.choice(remaining_letters)] + replaced_child[index+1:]
    return replaced_child

def crossover(person1, person2):
    parent1 = list(person1.encoding_dict.values())
    parent2 = list(person2.encoding_dict.values())
    random_cut = random.randint(1, len(parent1)-1)
    # Perform crossover
    child1_list = parent1[:random_cut] + parent2[random_cut:]
    child2_list = parent2[:random_cut] + parent1[random_cut:]
    #replace duplicate charecters
    child1_list = replace_duplicate_letters(child1_list)
    child2_list = replace_duplicate_letters(child2_list)
    alphabet = string.ascii_lowercase
    child1_dict = dict(zip(alphabet, child1_list))
    child2_dict = dict(zip(alphabet, child2_list))
    child1 = Person.Person(parent1.original_dna, child1_dict, parent1.num_generations + 1, parent1.fitnessFunc)
    child2 = Person.Person(parent1.original_dna, child2_dict, parent1.num_generations + 1, parent1.fitnessFunc)
    return child1, child2

