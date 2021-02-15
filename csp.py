import constraint as c
import numpy as np
from random import randrange

"""
Trasforma la soluzione dal tipo dizionario in una matrice (6x3)
Input:
    solution: dizionario con le variabili come chiavi e come valori il valore dal dominio per la soluzione
Output:
    Matrice (6x3) con i valori dalla soluzione del Constraint Satisfaction Problem
"""
def turnToMatrix(solution):
    matrix = np.zeros((6,3))
    for variable in solution.keys():
        matrix[int(variable[1])][int(variable[2])] = solution[variable]
    return matrix

"""
Crea il Constraint Satisfaction Problem che riguarda la creazione di una matrice (6x3)
che deve soddisfare un insieme di vincoli (specificati nella documentazione)
Il dominio delle variabili è di tipo float in un intervallo che aumenta di 0.025 da 0 a 1.0
Output:
    Il Constraint Satisfaction Problem con le variabili e i vincoli
"""
def createCSP():
    problem = c.Problem()
    domain = [0.0, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3, 0.325, 0.35, 0.375, 0.4, 0.425, 0.45, 0.475, 0.5, 0.525, 0.55, 0.575, 0.6, 0.625, 0.65, 0.675, 0.7, 0.725, 0.75, 0.775, 0.8, 0.825, 0.85, 0.875, 0.9, 0.925, 0.95, 0.975, 1.0]
    problem.addVariable("x00", domain)
    problem.addVariable("x01", domain)
    problem.addVariable("x02", domain)
    problem.addVariable("x10", domain)
    problem.addVariable("x11", domain)
    problem.addVariable("x12", domain)
    problem.addVariable("x20", domain)
    problem.addVariable("x21", domain)
    problem.addVariable("x22", domain)
    problem.addVariable("x30", domain)
    problem.addVariable("x31", domain)
    problem.addVariable("x32", domain)
    problem.addVariable("x40", domain)
    problem.addVariable("x41", domain)
    problem.addVariable("x42", domain)
    problem.addVariable("x50", domain)
    problem.addVariable("x51", domain)
    problem.addVariable("x52", domain)
    
    problem.addConstraint(lambda a, b, c: a + b + c == 1.0, ("x00", "x01", "x02"))
    problem.addConstraint(lambda a, b, c: a + b + c == 1.0, ("x10", "x11", "x12"))
    problem.addConstraint(lambda a, b, c: a + b + c == 1.0, ("x20", "x21", "x22"))
    problem.addConstraint(lambda a, b, c: a + b + c == 1.0, ("x30", "x31", "x32"))
    problem.addConstraint(lambda a, b, c: a + b + c == 1.0, ("x40", "x41", "x42"))
    problem.addConstraint(lambda a, b, c: a + b + c == 1.0, ("x50", "x51", "x52"))
    
    problem.addConstraint(lambda a, b: a > b, ("x00", "x01"))
    problem.addConstraint(lambda a, b: a > b, ("x01", "x02"))
    problem.addConstraint(lambda a, b: a > b, ("x20", "x21"))
    problem.addConstraint(lambda a, b: a > b, ("x21", "x22"))
    problem.addConstraint(lambda a, b: a > b, ("x40", "x41"))
    problem.addConstraint(lambda a, b: a > b, ("x41", "x42"))
    
    problem.addConstraint(lambda a, b: a < b, ("x10", "x11"))
    problem.addConstraint(lambda a, b: a < b, ("x11", "x12"))
    problem.addConstraint(lambda a, b: a < b, ("x30", "x31"))
    problem.addConstraint(lambda a, b: a < b, ("x31", "x32"))
    problem.addConstraint(lambda a, b: a < b, ("x50", "x51"))
    problem.addConstraint(lambda a, b: a < b, ("x51", "x52"))
    
    problem.addConstraint(lambda a, b: a > b, ("x00", "x20"))
    problem.addConstraint(lambda a, b: abs(a - b) <= 0.1 , ("x01", "x21"))
    problem.addConstraint(lambda a, b: a < b, ("x02", "x22"))
    problem.addConstraint(lambda a, b: a > b, ("x20", "x40"))
    problem.addConstraint(lambda a, b: abs(a - b) <= 0.1 , ("x21", "x41"))
    problem.addConstraint(lambda a, b: a < b, ("x22", "x42"))
    
    problem.addConstraint(lambda a, b: a > b, ("x10", "x30"))
    problem.addConstraint(lambda a, b: abs(a - b) <= 0.1 , ("x11", "x31"))
    problem.addConstraint(lambda a, b: a < b, ("x12", "x32"))
    problem.addConstraint(lambda a, b: a > b, ("x30", "x50"))
    problem.addConstraint(lambda a, b: abs(a - b) <= 0.1 , ("x31", "x51"))
    problem.addConstraint(lambda a, b: a < b, ("x32", "x52"))
    
    problem.addConstraint(lambda a, b: abs(a - b) >= 0.8, ("x00", "x02"))
    problem.addConstraint(lambda a, b: abs(a - b) <= 0.5, ("x10", "x12"))
    problem.addConstraint(lambda a, b: abs(a - b) <= 0.3, ("x20", "x22"))
    problem.addConstraint(lambda a, b: abs(a - b) <= 0.3, ("x30", "x32"))
    problem.addConstraint(lambda a, b: abs(a - b) <= 0.5, ("x40", "x42"))
    problem.addConstraint(lambda a, b: abs(a - b) >= 0.8, ("x50", "x52"))
    
    return problem

"""
Salva la matrice contenente i valori ottenuti dalla risoluzione del CSP in un file
Input:
    matrix: matrice contenente i valori Float
"""
def saveMatrix(matrix):
    np.savetxt("./utilities/probabilities.txt", matrix, fmt = "%.3f")

"""
Risolve un Constraint Satisfaction Problem ottenendo tutte le possibili soluzioni e ne
seleziona una casualmente
Input:
    problem: Constraint Satisfaction Problem
    rand: numero massimo di soluzioni per il problema
Output:
    Soluzione casuale del problema trasformata in una matrice (6x3) con il metodo turnToMatrix
"""
def solveProblemRand(problem, rand):
    solutionIter = problem.getSolutionIter()
    solutionIndex = randrange(rand)
    finalSolution = None
    i = 0
    
    for solution in solutionIter:
        if i == solutionIndex:
            finalSolution = solution
            break
        i = i + 1
    
    return turnToMatrix(finalSolution)