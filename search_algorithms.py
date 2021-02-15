from edge_node import Weight as w
from not_oriented_graph import GraphNo as g
from queue import PriorityQueue
from copy import deepcopy
import pickle as p

"""
Gestisce tutti i metodi e le variabili per la ricerca su grafo IDA*
"""
class IDAstar:
    
    _hit = False # variabile di controllo per l'IDA*
    _f_values = set() # insieme contenente i valori di f() per cui l'IDA* ha superato il bound
    _goal = 0 
    _heuristics_dictionary = {}
    
    def setDictionary(dictionary):
        IDAstar._heuristics_dictionary = dictionary
        
    def getDictionary():
        return IDAstar._heuristics_dictionary
        
    def _setGoal(node):
        IDAstar._goal = node
        
    def getGoal():
        return IDAstar._goal
    
     
    def _checkGoal(node):
        if node is IDAstar._goal:
            return True
        else:
            return False
     
    """
    Restituisce il valore euristico associato ad un percorso da un nodo al goal
    Input:
        node: nodo del grafo per il quale si calcola l'euristica
    Output: valore euristico del percorso
    """
    def _h(node):
       for headquarters in IDAstar._heuristics_dictionary.keys():
           if node.getElem() in headquarters and IDAstar._goal.getElem() in headquarters:
               return float(IDAstar._heuristics_dictionary[headquarters])
    """
    Restituisce il costo totale del cammino considerando il peso di ogni arco e la funzione euristica
    associata all'ultimo nodo del percorso per avere una stima totale
    F(n) = cost(n) + h(n)
    Input:
        G: grafo
        path: percorso su cui si calcola F
    Output:
        valore di F
    """        
    def _f(G, path):
        cost = 0
        for i in range(0, len(path) - 1):
            cost = cost + G.getWeight(path[i].getElem(), path[i + 1].getElem()).getTime()
        cost = cost + IDAstar._h(path[-1])
        return cost
    
    """
    Restituisce il valore f minore per il quale il depth bounded search è fallito 
    """
    def _getMinFValue():
        minimum = IDAstar._f_values.pop()
        for value in IDAstar._f_values:
            if value < minimum:
                minimum = value
        return minimum
    
    """
    Effettua la ricerca IDA* partendo da un nodo iniziale per raggiungere un nodo goal
    Input:
        G: grafo
        s: nodo di partenza
        goal: nodo obiettivo
    Output:
        Percorso ottimale dal nodo di partenza al nodo obiettivo, altrimenti None
    """
    def IDAstar_search(G, s, goal):
        G.setDinamicWeights()
        IDAstar._setGoal(G.getNode(goal))
        IDAstar._hit = False
        s = G.getNode(s)
        start = [s] # imposta il cammino iniziale con il solo nodo di start
        bound = IDAstar._f(G, start) # imposta il bound iniziale all'f(n) del nodo iniziale s
        while not IDAstar._hit:
            result = IDAstar._depth_bounded_search(G, s, goal, [s], bound)
            if isinstance(result, list) and IDAstar._checkGoal(result[-1]): # se è stato trovato un cammino con ultimo nodo goal esso viene restituito
                IDAstar._f_values.clear()
                return result
            if len(IDAstar._f_values) > 0:
                bound = IDAstar._getMinFValue() # recupera il valore di f(n) minore per cui depth_bounded_search è fallito
                IDAstar._f_values.clear() # cancella i vecchi valori ora non piu' utili
                IDAstar._hit = False # riporta hit a false per una nuova iterazione
            else:
                return None
    
    """
    Ricerca di tipo dfs richiamata nell'IDA* per la ricerca di un percorso
    Input:
        G: grafo
        s: nodo di partenza
        goal: nodo obiettivo
        path: percorso locale che si sta esplorando
        bound: valore massimo di F(n) per un percorso (F(n) = cost(n) + h(n))
    Output:
        Restituisce il percorso se trova una soluzione, altrimenti fallisce
        e in caso abbia superato il bound preimpostato segnala l'avvenimento e
        mantiene il valore di F(n) di quel percorso
    """
    def _depth_bounded_search(G, s, goal, path, bound):
        if bound >= IDAstar._f(G, path): # non espande cammini con f(n) superiore al bound
            for node in G._getAdjacentNodes(path[-1]): # nodi adiacenti all'ultimo del cammino
                if node not in path: # cycle pruning
                    pathToCheck = path
                    pathToCheck.append(node) # espande il cammino con un nodo adiacente
                    result = IDAstar._depth_bounded_search(G, s , goal, pathToCheck, bound) # chiamata ricorsiva
                    if isinstance(result, list) and IDAstar._checkGoal(result[-1]): # se viene trovato un cammino con ultimo nodo goal esso viene restituito
                        return result
                    pathToCheck.remove(path[-1]) # riporta il cammino allo stato originale per espanderlo nuovamente
        elif IDAstar._checkGoal(path[-1]): 
            return path
        elif len(G._getAdjacentNodes(path[-1])) > 0: # segnala che l'algoritmo è terminato perchè ha raggiunto il bound
            IDAstar._hit = True
            IDAstar._f_values.add(IDAstar._f(G,path)) # essendo terminato a causa del bound salva il valore di f(n) per il quale è terminato

"""
Gestisce tutti i metodi per la ricerca su grafo Lowest-Cost-First Search
"""
class LowestCostFirstSearch:
    
    """
    Effettua la ricerca Lowest-Cost-First
    Input:
        G: grafo sul quale si effettua la ricerca
        s: nodo di partenza
        goal: nodo obiettivo
    Output:
        Restituisce il percorso di costo minimo dal nodo di partenza a quello obiettivo,
        oppure None nel caso in cui non sia trovato alcun percorso risolutivo
    """
    def search(G, s, goal):
        frontier = PriorityQueue()
        frontier.put((0, 0, [s]))
        closedList = set()
        i = 0
        while not frontier.empty():
            path = frontier.get()[2]
            if path[-1] == goal:
                return (path, format(LowestCostFirstSearch._pathCost(G, path), ".2f"))
            if path[-1] in closedList:
                closedList.remove(path[-1])
            for edge in G.getEdges():
                if edge.getFirstElem() == path[-1] and edge.getSecondNode() not in closedList:
                    newPath = deepcopy(path)
                    newPath.append(edge.getSecondElem())
                    closedList.add(edge.getSecondElem())
                    i = i + 1
                    frontier.put((LowestCostFirstSearch._pathCost(G, newPath), i, newPath))
                elif edge.getSecondElem() == path[-1] and edge.getFirstNode() not in closedList:
                    newPath = deepcopy(path)
                    newPath.append(edge.getFirstElem())
                    closedList.add(edge.getFirstElem())
                    i = i + 1
                    frontier.put((LowestCostFirstSearch._pathCost(G, newPath), i, newPath))
        return None
    
    """
    Calcola il costo di un percorso considerando gli archi usati per raggiungerlo
    (si suppone esista un solo arco che porti da un nodo ad un altro)
    Input:
        G: grafo dal quale si recuperano gli archi ed i loro pesi
        path: percorso del quale si vuole calcolare il costo
    Output:
        Costo totale del percorso
    """
    def _pathCost(G, path):
        cost = 0
        if len(path) > 1:
            for i in range(0, len(path) - 1):
                for edge in G.getEdges():
                    if edge.getFirstElem() == path[i] and edge.getSecondElem() == path[i+1]:
                        cost = cost + edge.getWeight().getStandardTime()
                    elif edge.getSecondElem() == path[i] and edge.getFirstElem() == path[i+1]:
                        cost = cost + edge.getWeight().getStandardTime()
        return cost

def createGraph():
    graph = g()
    graph.addEdge("Gioia del Colle", "Bari", w(90, 38, "Big")) 
    graph.addEdge("Gioia del Colle", "Taranto", w(90, 50, "Big"))
    graph.addEdge("Bari", "Molfetta", w(90, 35, "Big"))
    graph.addEdge("Taranto", "Brindisi", w(110, 70, "Big"))
    graph.addEdge("Taranto", "Lecce", w(100, 104, "Big"))
    graph.addEdge("Brindisi", "Lecce", w(100, 39,  "Medium"))
    graph.addEdge("Foggia", "Barletta", w(100, 75, "Big"))
    graph.addEdge("Barletta", "Andria", w(80, 15, "Small"))
    graph.addEdge("Barletta", "Trani", w(70, 12, "Small"))
    graph.addEdge("Trani", "Molfetta", w(80, 22, "Medium"))
    graph.addEdge("Andria", "Bari", w(90, 58, "Big"))
    graph.addEdge("Andria", "Trani", w(70, 14, "Small"))
    graph.addEdge("Bari", "Castellana Grotte", w(80, 46, "Medium"))
    graph.addEdge("Castellana Grotte", "Brindisi", w(100, 85, "Big"))
    graph.addEdge("Castellana Grotte", "Gioia del Colle", w(70, 25, "Medium"))
    return graph

"""
Salva il dizionario che mantiene i valori euristici usati nella ricerca su grafo IDA* e li ottiene
mediante Lowest-Cost-First Search sullo stesso grafo
Input:
    graph: grafo su cui viene eseguita la lowest-cost-first search
"""
def createHeuristicDictionary(graph):
    headquarters = graph.getNodesElements()
    headquartersCopy = deepcopy(headquarters)
    results = dict()
    for headquarter in headquarters:
        headquartersCopy.remove(headquarter)
        for h in headquartersCopy:
            path = (headquarter, h)
            results[path] = LowestCostFirstSearch.search(graph, headquarter, h)[1]
    with open("./utilities/map", "wb") as file:
        p.dump(results, file)
        
def loadHeuristicDictionary():
    with open("./utilities/map", "rb") as file:
        return p.load(file)