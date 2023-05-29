import os
from re import sub
from PopulationRegular import Population as popReg
from PopulationDarwin import Population as popDar
from PopulationLamark import Population as popLam
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox

def runRegular(populationSize, encodedText, convergenceMax, mutationChance, deathThreshold, progressText):
    popy = popReg(populationSize, encodedText)
    convergenceCount = 0
    generationCounter = 0
    lastBestFit = 0
    graph = {}
    while convergenceCount < convergenceMax:
        generationCounter += 1
        popy.nextGen(mutationChance=mutationChance, deathThreshold=deathThreshold)
        # print("best person fitness:", float(popy.bestPerson.fitness))
        if popy.bestPerson.fitness == lastBestFit:
            convergenceCount += 1
        else:
            convergenceCount = 0
        lastBestFit = popy.bestPerson.fitness
        graph[generationCounter] = lastBestFit
        progressText.update()
        progressText.insert(END, f"Generation: {generationCounter}, Best Fitness: {lastBestFit}\n")
        progressText.see(END)

    return graph, popy.bestPerson


def runDarwin(populationSize, encodedText, convergenceMax, mutationChance, deathThreshold, localOpositions, progressText):
    popy = popDar(populationSize, encodedText)
    convergenceCount = 0
    generationCounter = 0
    lastBestFit = 0
    graph = {}
    while convergenceCount < convergenceMax:
        generationCounter += 1
        popy.nextGen(mutationChance=mutationChance, deathThreshold=deathThreshold, localOpositions=localOpositions)
        # print("best person fitness:", float(popy.bestPerson.fitness))
        if popy.bestPerson.fitness == lastBestFit:
            convergenceCount += 1
        else:
            convergenceCount = 0
        lastBestFit = popy.bestPerson.fitness
        graph[generationCounter] = lastBestFit
        progressText.update()
        progressText.insert(END, f"Generation: {generationCounter}, Best Fitness: {lastBestFit}\n")
        progressText.see(END)

    return graph, popy.bestPerson


def runLamark(populationSize, encodedText, convergenceMax, mutationChance, deathThreshold, localOpositions, progressText):
    popy = popLam(populationSize, encodedText)
    convergenceCount = 0
    generationCounter = 0
    lastBestFit = 0
    graph = {}
    while convergenceCount < convergenceMax:
        generationCounter += 1
        popy.nextGen(mutationChance=mutationChance, deathThreshold=deathThreshold, localOpositions=localOpositions)
        # print("best person fitness:", float(popy.bestPerson.fitness))
        if popy.bestPerson.fitness == lastBestFit:
            convergenceCount += 1
        else:
            convergenceCount = 0
        lastBestFit = popy.bestPerson.fitness
        graph[generationCounter] = lastBestFit
        progressText.update()
        progressText.insert(END, f"Generation: {generationCounter}, Best Fitness: {lastBestFit}\n")
        progressText.see(END)

    return graph, popy.bestPerson


def getEncodedText(encodedFilePath):
    text = ""
    with open(encodedFilePath, 'r') as f:
        text = f.read()

    text = sub(r"\s+", " ", text)
    return text

def update_progress_text(text):
    progressText.insert(END, text + '\n')
    progressText.see(END)  # Scroll to the end

def run_algorithm(populationSize, mutationChance, deathThreshold, geneticType, encodedFilePath, localOpositions=None):
    
    convergenceMax = 10

    encodedText = getEncodedText(encodedFilePath)

    if geneticType == "Regular":
        graph, bestPerson = runRegular(populationSize, encodedText, convergenceMax, mutationChance, deathThreshold, progressText)
    elif geneticType == "Darwin":
        graph, bestPerson = runDarwin(populationSize, encodedText, convergenceMax, mutationChance, deathThreshold, localOpositions, progressText)
    elif geneticType == "Lamark":
        graph, bestPerson = runLamark(populationSize, encodedText, convergenceMax, mutationChance, deathThreshold, localOpositions, progressText)

    with open("plain.txt", 'w') as file:
        file.write(bestPerson.new_dna)
    with open("perm.txt", 'w') as file:
        for key, value in bestPerson.getEncodingDict().items():
            file.write(f"{key} {value}\n")

    x_values = list(graph.keys())
    y_values = list(graph.values())

    plt.plot(x_values, y_values)
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.title('Best Fitness Per Generation')
    plt.show()

    openButton = Button(window, text="Open Files", command=open_files, font=font)
    openButton.pack()

def open_files():
    os.system("notepad.exe perm.txt")
    os.system("notepad.exe plain.txt")

def start_algorithm():
    populationSize = populationSizeEntry.get()
    mutationChance = mutationChanceEntry.get()
    deathThreshold = deathThresholdEntry.get()
    geneticType = geneticTypeVar.get()
    encodedFilePath = encodedFilePathEntry.get()

    if geneticType == "Darwin" or geneticType == "Lamark":
        localOpositions = localOpositionsEntry.get()
    else:
        localOpositions = None

    try:
        populationSize = int(populationSize)
        mutationChance = float(mutationChance)
        deathThreshold = float(deathThreshold)
        localOpositions = int(localOpositions) if localOpositions is not None else None
        progressText.delete('1.0', END)

        run_algorithm(populationSize, mutationChance, deathThreshold, geneticType, encodedFilePath, localOpositions)
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")

def update_local_oppositions_entry():
    if geneticTypeVar.get() == "Darwin" or geneticTypeVar.get() == "Lamark":
        localOpositionsLabel.pack()
        localOpositionsEntry.pack()
    else:
        localOpositionsLabel.pack_forget()
        localOpositionsEntry.pack_forget()

# Create the main window
window = Tk()
window.title("Genetic Algorithm")

font = ('Arial', 12)

encodedFilePathLabel = Label(window, text="Encoded File Path:", font=font)
encodedFilePathLabel.pack()
encodedFilePathEntry = Entry(window, font=font)
encodedFilePathEntry.pack()

# Create the input labels and entry fields
populationSizeLabel = Label(window, text="Population Size:", font=font)
populationSizeLabel.pack()
populationSizeEntry = Entry(window, font=font)
populationSizeEntry.pack()

mutationChanceLabel = Label(window, text="Mutation Chance:", font=font)
mutationChanceLabel.pack()
mutationChanceEntry = Entry(window, font=font)
mutationChanceEntry.pack()

deathThresholdLabel = Label(window, text="Death Threshold:", font=font)
deathThresholdLabel.pack()
deathThresholdEntry = Entry(window, font=font)
deathThresholdEntry.pack()

geneticTypeLabel = Label(window, text="Genetic Algorithm Type:", font=font)
geneticTypeLabel.pack()
geneticTypeVar = StringVar()
geneticTypeVar.set("Regular")
geneticTypeEntry = OptionMenu(window, geneticTypeVar, "Regular", "Darwin", "Lamark", command=update_local_oppositions_entry)
geneticTypeEntry.pack()

localOpositionsLabel = Label(window, text="Number of Local Opposions:", font=font)
localOpositionsLabel.pack()
localOpositionsEntry = Entry(window, font=font)
localOpositionsEntry.pack()

progressLabel = Label(window, text="Progress:", font=font)
progressLabel.pack()
progressText = Text(window, height=10, width=50, font=font)
progressText.pack()

startButton = Button(window, text="Start", command=start_algorithm, font=font)
startButton.pack()

# Start the GUI event loop
window.mainloop()
