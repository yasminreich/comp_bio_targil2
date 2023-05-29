import re
from PopulationLamark import Population
import csv
import Fitness

if __name__ == "__main__":
    temp = 0.8
    filename = "lamark_{}.csv".format(temp)
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['population_size', 'motation_chance', "n_opt", 'death_treshold', 'generation_num','calls_to_fit', 'best_fit'])
    text = ""
    with open('enc.txt', 'r') as f:
        text = f.read()
    text = re.sub(r"\s+", " ", text)
    population_size_values = [40, 60, 80, 100]
    mutation_chance_values = [0.2, 0.4, 0.6, 0.8]
    death_threshold_values = [temp]
    local_ops = [5,7,10]
    # fit = Fitness.Fit("dict.txt", "Letter2_Freq.txt", "CalculatedWords.json")
    for p in population_size_values:
         for m in mutation_chance_values:
              for d in death_threshold_values:
                for l in local_ops:
                    for i in range(1):
                        popy = Population(p, text)
                        convergenceMax = 10
                        convergenceCount = 0
                        generationCounter = 0
                        lastBestFit = 0
                        while convergenceCount < convergenceMax:
                            generationCounter += 1
                            popy.nextGen(mutationChance=m, deathThreshold=d, localOpositions=l)
                            print("best person fitness:", float(popy.bestPerson.fitness))
                            if popy.bestPerson.fitness == lastBestFit:
                                convergenceCount += 1
                            else:
                                convergenceCount = 0
                            lastBestFit = popy.bestPerson.fitness
                        with open(filename, mode='a', newline='') as csvfile:
                                    writer = csv.writer(csvfile)
                                    writer.writerow([p, m, l, d, generationCounter, popy.fitness.fitnessCallCount, popy.bestPerson.fitness])
                        # popy.fitness.calcWordsToJson()