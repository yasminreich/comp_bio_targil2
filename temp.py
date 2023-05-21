import Populationp
import Mutations
import string

if __name__ == "__main__":
    popy = Populationp.Population(2, "xaac cbz")
    print(list(popy.population[0].encoding_dict.values()))
    print(list(popy.population[1].encoding_dict.values()))
    child1, child2 = Mutations.crossover(popy.population[0], popy.population[1])
    print(child1.getEncodingDict().values())
    print(child1.encoding_dict.values())
    print(child2.getEncodingDict().values())
    print(child2.encoding_dict.values())
