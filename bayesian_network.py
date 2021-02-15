import pomegranate as pg
import numpy as np

"""
Costruisce una Rete Bayesiana (la struttura può essere vista nella documentazione)
Input:
    probabilities: matrice contenente le probabilità associate per l'ultimo nodo della rete
    riguardante la probabilità che un'auto di una certa classe (acc, good, vgood) si rompa in un determinato
    periodo (short term, medium term, long term) a seconda di quanto essa venga utilizzata (frequently, notfrequently)
Output:
    model: La Rete Bayesiana
"""
def createBN(probabilities):
    """
    Distribuzione di probabilità che si riferisce alla necessità dell'uso dell'auto per questioni lavorative
    """
    carForWork = pg.DiscreteDistribution({"yes": 0.6, "no": 0.4 })
    """
    Tabella di probabilità condizionata che si riferisce alla frequenza d'uso dell'auto, in relazione all'uso lavorativo
    """
    usage = pg.ConditionalProbabilityTable(
            [["yes", "frequently", 0.8],
             ["yes", "notfrequently", 0.2],
             ["no", "frequently", 0.3],
             ["no", "notfrequently", 0.7]], [carForWork])
    """
    Distribuzione di probabilità che si riferisce al possibile grado di qualità dell'auto
    """
    carClass = pg.DiscreteDistribution({"acc": 0.74, "good": 0.13, "vgood": 0.13 })
    
    """
    Tabella di probabilità condizionata che si riferisce al periodo in cui un'auto di una determinata classe,
    usata con una determinata frequenza, possa rompersi
    """
    carBreak = pg.ConditionalProbabilityTable(
            [["acc", "frequently", "short term", probabilities[0][0]],
             ["acc", "notfrequently", "short term", probabilities[1][0]],
             ["good", "frequently", "short term", probabilities[2][0]],
             ["good", "notfrequently", "short term", probabilities[3][0]],
             ["vgood", "frequently", "short term", probabilities[4][0]],
             ["vgood", "notfrequently", "short term", probabilities[5][0]],
             ["acc", "frequently", "medium term", probabilities[0][1]],
             ["acc", "notfrequently", "medium term", probabilities[1][1]],
             ["good", "frequently", "medium term", probabilities[2][1]],
             ["good", "notfrequently", "medium term", probabilities[3][1]],
             ["vgood", "frequently", "medium term", probabilities[4][1]],
             ["vgood", "notfrequently", "medium term", probabilities[5][1]],
             ["acc", "frequently", "long term", probabilities[0][2]],
             ["acc", "notfrequently", "long term", probabilities[1][2]],
             ["good", "frequently", "long term", probabilities[2][2]],
             ["good", "notfrequently", "long term", probabilities[3][2]],
             ["vgood", "frequently", "long term", probabilities[4][2]],
             ["vgood", "notfrequently", "long term", probabilities[5][2]]], [carClass, usage])
    
    s1 = pg.Node(carForWork, name = "Car For Work")
    s2 = pg.Node(usage, name = "Car Usage")
    s3 = pg.Node(carClass, name = "Car Class")
    s4 = pg.Node(carBreak, name = "Car Breaks")
    
    model = pg.BayesianNetwork("Probability for a Car to Break")
    model.add_states(s1, s2, s3, s4)
    model.add_edge(s1, s2)
    model.add_edge(s2, s4)
    model.add_edge(s3, s4)
    model.bake()
    return model

"""
Fornisce una predizione dalla Rete Bayesiana fornendo le osservazioni sui dati
Utile in caso di dati mancanti (None), quindi di osservazioni incomplete, per ottenere una
predizione su quali essi siano (rispetto alla probabilità)
Input:
    model: Rete Bayesiana su cui si effettua la predizione
    arg1: Valore che fa riferimento all'utilizzo dell'auto in un contesto lavorativo (yes/no) 
    arg2: Valore che fa riferimento a quanto frequentemente l'auto venga utilizzata,
          considerando anche se venga usata o meno nel contesto lavorativo (frequently/notfrequently)
    arg3: Valore che fa riferimento al grado di qualità dell'auto (acc, good, vgood) [acc = acceptable; v = very]
    arg4: Valore che fa riferimento al periodo in cui l'auto potrebbe rompersi (short term, medium term, long term)
Output:
    Array di 4 dimensioni, ad esempio nella forma: ["yes", "frequently", "acc", "short term"]
"""
def getPrediction(model, arg1, arg2, arg3, arg4):
    return model.predict([[arg1, arg2, arg3, arg4]])

"""
Fornisce la probabilità che una certa predizione di una Rete Bayesiana avvenga
Input:
    model: Rete Bayesiana su cui vengono effettuati i calcoli
    predict: Predizione sulla Rete Bayesiana
Output:
    Probabilità che la data predizione avvenga; i calcoli vengono fatti sfruttando le probabilità nella Rete Bayesiana
"""
def getProbability(model, predict):
    return model.probability(predict)

"""
Recupera da file i valori di probabilità per il nodo della Rete Bayesiana "Probability for a Car to Break"
Input:
    filename: path del file in cui è stata salvata la matrice (6x3) contenente i valori
Output:
    La matrice recuperata dal file
"""
def seekMatrix(filename):
    probabilities = np.loadtxt(filename, usecols = range(3))
    return probabilities
