import numpy as np

class Node:

    def __init__(self, elem):
        self._elem = elem
    
    def getElem(self):
        return self._elem
    
    def __str__(self):
        return str(self._elem)
    
    def __repr__(self):
        return str(self)
    
class Edge:
    
    def __init__(self, node1, node2, weight):
        self._firstNode = node1
        self._secondNode = node2
        self._weight = weight

    def getValues(self):
        return self._firstNode.getElem(), self._secondNode.getElem(), self._weight.getTime()
    
    def getFirstElem(self):
        return self._firstNode.getElem()
    
    def getSecondElem(self):
        return self._secondNode.getElem()
    
    def getWeight(self):
        return self._weight
    
    def getEdgeNodes(self):
        return self._firstNode, self._secondNode
    
    def getFirstNode(self):
        return self._firstNode
    
    def getSecondNode(self):
        return self._secondNode
   
    def __str__(self):
        return self._firstNode.__str__() + ", "  + self._secondNode.__str__()

"""
Rappresenta il peso degli archi del grafo in virtù dello specifico dominio di applicazione,
tenendo conto della tipologia della strada, distanza fra i nodi (in Km), limite di velocità
medio. Queste informazioni sono utilizzate per il calcolo dinamico del tempo necessario per 
percorrere la strada (vengono considerati anche altri fattori come il numero di vetture sulla strada).
"""
class Weight:
    
    def __init__(self, max_speed, distance, size):
        self._max_speed = max_speed
        self._distance = distance
        self._size = size
        self._time = 0
    
    def setAdditionalTime(self):
        n_vehicles = 0
        incidence = 0
        
        if self._size.lower() == "big":
            while n_vehicles < 100 or n_vehicles > 300:
                n_vehicles = np.random.normal(180, 50)
            incidence = (60 * (n_vehicles - 100)) / 200
       
        if self._size.lower() == "medium":
            while n_vehicles < 50 or n_vehicles > 150:
                n_vehicles = np.random.normal(99, 22)
            incidence = (40 * (n_vehicles - 50)) / 100
            
        if self._size.lower() == "small":
            while n_vehicles < 10 or n_vehicles > 30:
                n_vehicles = np.random.normal(22, 8)
            incidence = n_vehicles - 10
        
        return(incidence) 
    
    def calculateTime(self):
        self._time = (self._distance / self._max_speed) * 60 + self.setAdditionalTime()
        
    def getStandardTime(self):
        return (self._distance / self._max_speed) * 60

    def getTime(self):
        return self._time
    
    def getSize(self):
        return self._size
    
    