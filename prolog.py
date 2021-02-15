from random import randrange
import kanren as k

"""
Imposta le sedi nella base di conoscenza ed il loro stato
Input:
    headquarters: insieme di sedi
    kb: base di conoscenza
"""
def setHeadquarters(headquarters, relation):
    for headquarter in headquarters:
        i = randrange(3)
        if i == 1:
            k.fact(relation, headquarter.lower(), "active", "full")
        elif i == 2:
            k.fact(relation, headquarter.lower(), "active", "free")
        elif i == 0:
            k.fact(relation, headquarter.lower(), "notactive", "full")

"""
Inizializza la base di conoscenza e la restituisce
Input:
    headquarters: insieme di sedi
Output:
    kb: base di conoscenza
"""
def createKB(headquarters):
    hq = k.Relation()
    setHeadquarters(headquarters, hq)
    return hq

def listOfActiveHqs(relation):
    q = k.var()
    return k.run(0, q, relation(q, "active", "free"))

def listOfNotActiveHqs(relation):
    q = k.var()
    return k.run(0, q, relation(q, "notactive", "full"))
