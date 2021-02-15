from edge_node import Edge as e
from edge_node import Node as n
"""
Classe grafo non orientato, non necessita di creare nodi o archi esterni, esegue controlli in maniera automatica. 

Il metodo addEdge oltre che aggiungere automaticamente gli archi crea anche
uno o entrambi i nodi, se essi non esistono già nel grafo.

Il metodo addNode risulta utile solo se si hanno nodi isolati. 

Essendo sia gli archi che i nodi privati e incapsulati, i parametri dei metodi saranno
semplicemente i valori contenuti nel nodo, ad esempio se abbiamo un nodo con valore la stringa "pizza", sarà sufficiente
chiamare il metodo getNode("pizza") per ottenere l'oggetto nuovo, oppure removeNode("pizza") per eliminarlo dal grafo.

Il metodo removeNode elimina in automatico anche tutti gli archi del nodo specificato in input.

Essendo un grafo non orientato i metodi relativi agli archi hanno controlli in più:
Per il metodo addEdge() gli archi (1,2) e (2,1) sono lo stesso arco, se viene aggiunto il primo, non sarà necessario
aggiungere il secondo

Se fosse inserito un arco del tipo (1,2) sarebbe possibile eliminarlo tramite removeEdge in uno dei seguenti modi: removeEdge(1,2) OR removeEdge(2,1)

I metodi get ritornano i relativi oggetti e non i valori dei nodi
Se si volesse ottenere il valore di un nodo o di un arco, sarebbe necessario usare i relativi metodi delle loro classi
"""
class GraphNo:
    
    def __init__(self):
        self._edges = []
        self._nodes =  []
    
    def getNodes(self):
        return self._nodes
    
    def getEdges(self):
        return self._edges
    
    def getNodesElements(self):
        nodes = []
        for node in self._nodes:
                nodes.append(node.__str__())
        return nodes

    def getEdgesElements(self):
        edges = []
        for edge in self._edges:
                edges.append("(" + edge.__str__() + ")")
        return edges
    
    def addNode(self, value):
        if not self._containsNode(value):      
            self._nodes.append(n(value))
        else:
           print(f"Il nodo {value} è gia presente")
    
    
    def removeNode(self, value):
        node = self.getNode(value)
        for edge in reversed(self._edges):
            if node is edge.getFirstNode() or node is edge.getSecondNode():
                self.removeEdge(edge.getFirstElem(), edge.getSecondElem())
                    
        self.nodes.remove(node)
    
    def getNode(self, value):
        if self._containsNode(value):
            for node in self._nodes:
                if value == node.getElem():
                    return node
        else:
            print(f"Il nodo {value} non è presente nel grafo")
   
    def _containsNode(self, value):
        existing = False
        for node in self._nodes:
            if node.getElem() == value:
                existing = True
                break
        return existing
    
    def addEdge(self, value1, value2, weight):
        if not self._containsEdge(value1, value2):
            if (not self._containsNode(value1)) and (not self._containsNode(value2)):
                node1 = n(value1)
                node2 = n(value2)
                self._nodes.append(node1)
                self._nodes.append(node2)
                self._edges.append(e(node1, node2, weight))
            elif not self._containsNode(value1):
                node2 = self.getNode(value2)
                node1 = n(value1)
                self._nodes.append(node1)
                self._edges.append(e(node1, node2, weight))
            elif not self._containsNode(value2):
                node1 = self.getNode(value1)
                node2 = n(value2)
                self._nodes.append(node2)
                self._edges.append(e(node1, node2, weight))
            else:
                node1 = self.getNode(value1)
                node2 = self.getNode(value2)
                self._edges.append(e(node1, node2, weight))
        else:
           print(f"L'arco {value1, value2} è gia presente")
                
    def getEdge(self, value1, value2):
        if self._containsEdge(value1, value2):
            for edge in self._edges:
                if (edge.getFirstElem() == value1 and edge.getSecondElem() == value2) or (edge.getFirstElem() == value2 and edge.getSecondElem() == value1):
                    return edge
        else:
             print(f"L'arco {value1, value2} non è presente nel grafo")
    
    def removeEdge(self, value1, value2):
        edge = self.getEdge(value1, value2)
        self._edges.remove(edge)
                
    def _containsEdge(self, value1, value2):
        existing = False
        if value1 is not value2:
            if self._containsNode(value1) and self._containsNode(value2):
                for edge in self._edges:
                    if (edge.getFirstElem() == value1 and edge.getSecondElem() == value2) or (edge.getFirstElem() == value2 and edge.getSecondElem() == value1):
                        existing = True
                        break
        return existing

    def setWeight(self, value1, value2, weight):
        if self._containsEdge(value1, value2):
            edge = self.getEdge(value1, value2)
            edge.setWeight(weight)
            
    def getWeight(self, value1, value2):
        if self._containsEdge(value1, value2):
            for edge in self._edges:
                if (edge.getFirstElem() == value1 and edge.getSecondElem() == value2) or (edge.getFirstElem() == value2 and edge.getSecondElem() == value1):
                    return edge.getWeight()
    
    def _getAdjacentNodes(self, node):
        adjacentNodes = set()
        if self._containsNode(node.getElem()):
            for edge in self._edges:
                if node is edge.getFirstNode():
                    adjacentNodes.add(edge.getSecondNode())
                elif node is edge.getSecondNode():
                        adjacentNodes.add(edge.getFirstNode())
        return adjacentNodes
    
    def getEdgesForNode(self, value):
        edges = set()
        node = self.getNode(value)
        for edge in self._edges:
            if node is edge.getFirstNode() or node is edge.getSecondNode():
                edges.add(edge)
        return edges

    def setDinamicWeights(self):
        for edge in self._edges:
            edge.getWeight().calculateTime()
