import re
import os
from PopulationRegular import Population
import csv

if __name__ == "__main__":
    temp = 0.8
    with open("regular_{}.csv".format(temp), mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['population_size', 'motation_chance', 'death_treshold', 'generation_num','calls_to_fit', 'best_fit'])
    text = ""
    with open('enc.txt', 'r') as f:
        text = f.read()
    text = re.sub(r"\s+", " ", text)
    population_size_values = [40, 60, 80, 100, 150]
    mutation_chance_values = [0.2, 0.4, 0.6, 0.8]
    death_threshold_values = [temp]
    for p in population_size_values:
         for m in mutation_chance_values:
              for d in death_threshold_values:
                for i in range(10):
                    popy = Population(p, text)
                    convergenceMax = 10
                    convergenceCount = 0
                    generationCounter = 0
                    lastBestFit = 0
                    while convergenceCount < convergenceMax:
                        generationCounter += 1
                        popy.nextGen(mutationChance=m, deathThreshold=d)
                        if popy.bestPerson.fitness == lastBestFit:
                            convergenceCount += 1
                        else:
                            convergenceCount = 0
                        lastBestFit = popy.bestPerson.fitness
                    with open("regular_{}.csv".format(temp), mode='a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow([p, m, d, generationCounter, popy.fitness.fitnessCallCount, popy.bestPerson.fitness])
                    # popy.fitness.calcWordsToJson()