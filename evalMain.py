import re
import os
from PopulationRegular import Population
import csv

if __name__ == "__main__":
    with open("regular.csv", mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['population_size', 'motation_chance', 'death_treshold', 'generation_num', "best_fit"])
    text = ""
    with open('enc.txt', 'r') as f:
        text = f.read()
    text = re.sub(r"\s+", " ", text)
    population_size_values = [40, 60, 80, 100]
    mutation_chance_values = [0.2, 0.4, 0.6]
    death_threshold_values = [10, 20, 60]
    for p in population_size_values:
         for m in mutation_chance_values:
              for d in death_threshold_values:
                for i in range(10):
                    popy = Population(p, text)
                    # deathTreshold = 5
                    # breakPoint=93
                    convergenceMax = 10
                    convergenceCount = 0
                    generationCounter = 0
                    lastBestFit = 0
                    while convergenceCount < convergenceMax:
                        generationCounter += 1
                        popy.nextGen(mutationChance=m, deathThreshold=d)
                        print("best person fitness:", float(popy.bestPerson.fitness))
                        if popy.bestPerson.fitness == lastBestFit:
                            convergenceCount += 1
                        else:
                            convergenceCount = 0
                        lastBestFit = popy.bestPerson.fitness
                    with open("regular.csv", mode='a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow([p, m, d, generationCounter, popy.bestPerson.fitness])