import tkinter as tk
import supervised_learning as sl
import bayesian_network as bn
import csp as csp
import search_algorithms as g
import prolog as pro
import os.path

"""
Gestisce tutti i metodi e le variabili per il Supervised Learning
"""
class Learning():
    
    _X = None
    _y = None
    _enc = None
    _le = None
    
    def initDataset(path):
        dataset = sl.recoverDataset(path)
        Learning._X, Learning._enc = sl.splitX(dataset)
        Learning._y, Learning._le = sl.splity(dataset)
        
    """
    Restituisce la media dei punteggi della K-Fold Cross Validation per i 3 classificatori usati (Logistic Regression, Support Vector Machines e Random Forest Classifier)
    Input:
        metric: specifica il tipo di metrica da utilizzare
    Output:
        dizionario che contiene i valori restituiti dalla Cross Validation oppure un messaggio di errore nel caso il dataset non fosse stato inizializzato
    """
    def getKFoldScores(metric):
        if Learning._X is not None and Learning._y is not None:
            scores = sl.getKFoldScores(Learning._X, Learning._y, metric)
            return scores
        else:
            return "Dataset wasn't loaded correctly"
    """
    Restituisce il classification report per un classificatore o le predizioni su
    instanze non classificate da file fra tre opzioni (Logistic Regression, Support Vector Machines e Random Forest Classifier)
    Input:
        option: valore tra 1 e 3 per specificare il classificatore da utilizzare
        testsize: valore di tipo Float tra 0 e 1 che specifica la grandezza del test set rispetto al training
        i: valore intero per scegliere se restituire il classification report o classificare delle istanze da file
    Output:
        Classification Report del classificatore selezionato oppure classi corrispondenti
        alle istanze nel file oppure messaggio di errore nel caso di nessuna selezione
    """
    def getPredForClassifier(option, testsize, i):
        path = "./utilities/classification.txt"
        if option == 1:
            return sl.logisticRegressionPred(Learning._X, Learning._y, testsize, Learning._le, Learning._enc, i, path)
        elif option == 2:
            return sl.supportVectorMachinesPred(Learning._X, Learning._y, testsize, Learning._le, Learning._enc, i, path)
        elif option == 3:
            return sl.randomForestClassifierPred(Learning._X, Learning._y, testsize, Learning._le, Learning._enc, i, path)
        else:
            return "Option wasn't selected correctly"

"""
Gestisce tutti i metodi e le variabili per la Bayesian Network
"""
class BayesianNet():
    
    _network = None
    
    def initNetwork(probabilities):
       BayesianNet._network = bn.createBN(probabilities)
       
    def deleteNetwork():
        BayesianNet._network = None
       
    """
    Restituisce la predizione e la sua probabilità nella Bayesian Network
    Input:
        args: lista contente da 1 a 2 elementi
             (1 nel caso in cui sia specificato solo il grado di qualità della macchina, 2 nel caso in cui sia anche specificato se essa debba essere usata per lavoro)
        option: valore booleano per specificare se siano dati 1 o 2 elementi in input
    Output:
        Predizione completa delle osservazioni mancanti per ogni evento in ogni possibile lasso di tempo
        (ovvero short term, medium term e long term) e probabilità che essi accadano
    """
    def getCompletePrediction(args, option):
       completePrediction = dict()
       prediction = None
       timeRanges = set()
       timeRanges.add("short term")
       timeRanges.add("medium term")
       timeRanges.add("long term")
       for timeRange in timeRanges:
           if option:
               prediction = bn.getPrediction(BayesianNet._network, args[1], None, args[0], timeRange)
           else:
               prediction = bn.getPrediction(BayesianNet._network, None, None, args[0], timeRange)
           completePrediction[str(prediction[0])] = bn.getProbability(BayesianNet._network, prediction)
       return completePrediction
   
"""
Gestisce tutti i metodi e le variabili per il Constraint Satisfaction Problem
"""
class CSPprob():
    
    _csp = None
    
    def initCSP():
        CSPprob._csp = csp.createCSP()
    
    """
    Salva una nuova matrice su file contenente nuovi valori di probabilità per la Bayesian Network
    """
    def newProbability():
        csp.saveMatrix(csp.solveProblemRand(CSPprob._csp, 972))

"""
Gestisce tutti i metodi e le variabili per la ricerca su grafo
"""        
class GraphSearch():
    
    _graph = None
    
    def initGraph():
        GraphSearch._graph = g.createGraph()
        
    def getHeadquarters():
        return GraphSearch._graph.getNodesElements()
    
    def idastarSearch(start, destination):
        if len(g.IDAstar.getDictionary()) == 0:
            g.IDAstar.setDictionary(GraphSearch.getHeuristicsDictionary())
        return g.IDAstar.IDAstar_search(GraphSearch._graph, start, destination)
    
    """
    Carica da file la funzione euristica necessaria per la ricerca IDA*
    """
    def getHeuristicsDictionary():
        return g.loadHeuristicDictionary()
        
    def computeHeuristicsDictionary():
        g.createHeuristicDictionary(GraphSearch._graph)

"""
Gestisce tutti i metodi e le variabili riguardanti la Base di Conoscenza
"""
class PrologKB():
    
    _relation = None
    
    def initKb():
        PrologKB._relation = pro.createKB(GraphSearch.getHeadquarters())
        
    def getActiveHqs():
        return pro.listOfActiveHqs(PrologKB._relation)
    
    def getNotActiveHqs():
        return pro.listOfNotActiveHqs(PrologKB._relation)
    
"""
Gestisce la creazione dell'interfaccia grafica
"""
class MainApplication(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self._parent = parent
        frame = tk.Frame(self._parent, bg = "#288cff")
        frame.pack(anchor = tk.N, fill= tk.BOTH, expand = True, side = tk.LEFT)
        text = tk.Text(frame)
        text.place(relx = 0.05, rely = 0.05, relwidth = 0.6, relheight = 0.72)
        text.insert(tk.INSERT,"Welcome")
        text.config(state = tk.DISABLED)
        scrollbarText = tk.Scrollbar(text, orient = tk.VERTICAL, command = text.yview)
        scrollbarText.pack(side=tk.RIGHT, fill=tk.Y)
        radioMetricChoice = tk.StringVar()
        rBAccur = tk.Radiobutton(frame, text = "Balanced Accuracy                  ", variable = radioMetricChoice, value = "balanced_accuracy")
        rBAccur.place(relx = 0.53, rely = 0.85)
        rNMS = tk.Radiobutton(frame, text = "Negative Mean Squared Error", variable = radioMetricChoice, value = "neg_mean_squared_error")
        rNMS.place(relx = 0.53, rely = 0.89)
        radioChoiceClassif = tk.IntVar()
        rLogistic = tk.Radiobutton(frame, text = "Logistic Regression           ", variable = radioChoiceClassif, value = 1)
        rLogistic.place(relx = 0.05, rely = 0.80)
        rSVM = tk.Radiobutton(frame, text = "Support Vector Machines", variable = radioChoiceClassif, value = 2)
        rSVM.place(relx = 0.05, rely = 0.84)
        rRFC = tk.Radiobutton(frame, text = "Random Forest Classifier ", variable = radioChoiceClassif, value = 3)
        rRFC.place(relx = 0.05, rely = 0.88)
        lKFold = tk.Label(frame, text = "K-Fold Cross Validation (k = 10)", bg = "#ffffff")
        lKFold.place(relx = 0.4, rely = 0.80)
        rAction = tk.IntVar()
        rActionFile = tk.Radiobutton(frame, text = "Classify from File      ", variable = rAction, value = 1)
        rActionFile.place(relx = 0.2, rely = 0.8)
        rActionReport = tk.Radiobutton(frame, text = "Classification Report", variable = rAction, value = 0)
        rActionReport.place(relx = 0.2, rely = 0.84)
        buttonClassifier = tk.Button(frame, text = "Classify", command = lambda : buttonPred(text, radioChoiceClassif.get(), rAction.get()))
        buttonClassifier.place(relx = 0.08, rely = 0.92, relwidth = 0.05, relheight = 0.05)
        buttonFold = tk.Button(frame, text = "K-Fold", command = lambda : buttonKFold(text, radioMetricChoice.get()))
        buttonFold.place(relx = 0.415, rely = 0.84, relwidth = 0.1, relheight = 0.1)
        radioChoiceCarClass = tk.StringVar()
        rAcc = tk.Radiobutton(frame, text = "Acceptable", variable = radioChoiceCarClass, value = "acc")
        rAcc.place(relx = 0.7, rely = 0.1)
        rGood = tk.Radiobutton(frame, text = "Good          ", variable = radioChoiceCarClass, value = "good")
        rGood.place(relx = 0.7, rely = 0.14)
        rVGood = tk.Radiobutton(frame, text = "Very Good ", variable = radioChoiceCarClass, value = "vgood")
        rVGood.place(relx = 0.7, rely = 0.18)
        radioChoiceWork = tk.StringVar()
        rWork = tk.Radiobutton(frame, text = "Car used for Work       ", variable = radioChoiceWork, value = "yes")
        rWork.place(relx = 0.8, rely = 0.1)
        rNotWork = tk.Radiobutton(frame, text = "Car not used for Work", variable = radioChoiceWork, value = "no")
        rNotWork.place(relx = 0.8, rely = 0.14)
        rUndefined = tk.Radiobutton(frame, text = "Undefined                    ", variable = radioChoiceWork, value = "undefined")
        rUndefined.place(relx = 0.8, rely = 0.18)
        buttonPrediction = tk.Button(frame, text = "Predict", command = lambda : buttonBN(text, radioChoiceCarClass.get(), radioChoiceWork.get()))
        buttonPrediction.place(relx = 0.70, rely = 0.24, relwidth = 0.08, relheight = 0.08)
        buttonProbabilities = tk.Button(frame, text = "Reset Probabilities", command = lambda : buttonProb(text))
        buttonProbabilities.place(relx = 0.80, rely = 0.24, relwidth = 0.08, relheight = 0.08)
        buttonRefresh = tk.Button(frame, text = "Refresh", command = lambda : refresh(text))
        buttonRefresh.place(relx = 0.61, rely = 0.01)
        lbStart = tk.Listbox(frame, selectmode = tk.SINGLE, exportselection = False)
        lbDestination = tk.Listbox(frame, selectmode = tk.SINGLE, exportselection = False)
        lbStart.place(relx = 0.7, rely = 0.5, relwidth = 0.1, relheight = 0.2)
        lbDestination.place(relx = 0.81, rely = 0.5, relwidth = 0.1, relheight = 0.2)
        scrollbarStart = tk.Scrollbar(lbStart, orient = tk.VERTICAL, command = lbStart.yview)
        scrollbarDestination = tk.Scrollbar(lbDestination, orient = tk.VERTICAL, command = lbDestination.yview)
        scrollbarStart.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbarDestination.pack(side=tk.RIGHT, fill=tk.Y)
        initListBoxes(lbStart, lbDestination)
        button = tk.Button(frame, text = "Search", command = lambda : buttonResearch(text, lbStart, lbDestination)) 
        button.place(relx = 0.75, rely = 0.76, relwidth = 0.1, relheight = 0.1)
        startFilter = tk.StringVar()
        startFilter.trace(tk.W, lambda name, index, mode, startFilter = startFilter: getText(startFilter, lbStart)) 
        startTextArea = tk.Entry(frame, textvariable = startFilter)
        startTextArea.place(relx = 0.7, rely = 0.7, relwidth = 0.1, relheight = 0.05)
        destinationFilter = tk.StringVar()
        destinationFilter.trace(tk.W, lambda name, index, mode, destinationFilter = destinationFilter: getText(destinationFilter, lbDestination)) 
        destinationTextArea = tk.Entry(frame, textvariable = destinationFilter)
        destinationTextArea.place(relx = 0.81, rely = 0.7, relwidth = 0.1, relheight = 0.05)
        kbButton = tk.Button(frame, text = "Refresh KB", command = lambda : buttonKb(text, lbStart, lbDestination)) 
        kbButton.place(relx = 0.925, rely = 0.45)
        lBayesian = tk.Label(frame, text = "Bayesian Network", bg = "#ffffff")
        lBayesian.place(relx = 0.75, rely = 0.05)
        lSearch = tk.Label(frame, text = "Search Path", bg = "#ffffff")
        lSearch.place(relx = 0.7775, rely = 0.4)
        lStart = tk.Label(frame, text = "Start", bg = "#ffffff")
        lStart.place(relx = 0.7, rely = 0.45, relwidth = 0.1)
        lDestination = tk.Label(frame, text = "Destination", bg = "#ffffff")
        lDestination.place(relx = 0.81, rely = 0.45, relwidth = 0.1)
"""
Usato per prendere testo in maniera automatica
"""
def getText(text, lb):
    lb.delete(0, tk.END)
    nameList = list(GraphSearch.getHeadquarters())
    nameList.sort()
    toFind = text.get()
    for headquarter in nameList:
        if headquarter.lower().find(toFind) != -1 or headquarter.lower().find(toFind.lower()) != -1:
            lb.insert(tk.END, headquarter)
        elif text.get() == "":
            lb.insert(tk.END, headquarter)
 
"""
Inizializza gli oggetti Listbox di tkinter con le sedi da inserirvi
Input:
    lbStart: listbox delle sedi di partenza dalla libreria tkinter
    lbDestination: listbox delle sedi di destinazione dalla libreria tkinter
"""
def initListBoxes(lbStart, lbDestination):
    lbStart.delete(0, tk.END)
    lbDestination.delete(0, tk.END)
    nameList = list(GraphSearch.getHeadquarters())
    nameList.sort()
    activeNameList = list(PrologKB.getActiveHqs())
    notActiveNameList = list(PrologKB.getNotActiveHqs())
    for name in nameList:
        if name.upper() in map(str.upper, activeNameList):
            lbDestination.insert(tk.END, name)
        if name.upper() not in map(str.upper, notActiveNameList):
            lbStart.insert(tk.END, name)

"""
Ricrea la Base di Conoscenza relativa allo stato delle varie sedi
Input:
    textArea: oggetto Text dalla libreria tkinter
    lbStart: listbox delle sedi di partenza dalla libreria tkinter
    lbDestination: listbox delle sedi di destinazione dalla libreria tkinter
"""
def buttonKb(textArea, lbStart, lbDestination):
    textArea.config(state = tk.NORMAL)
    textArea.insert(tk.INSERT, "\n")
    textArea.insert(tk.INSERT, "Kb updated")
    PrologKB.initKb()
    initListBoxes(lbStart, lbDestination)
    textArea.see(tk.END)
    textArea.config(state = tk.DISABLED)   
        
"""
Stampa su textArea i valori medi della K-Fold Cross Validation (k = 10) per 3 classificatori (Logistic Regression, Support Vector Machines, Random Forest Classifier)
oppure un messaggio di errore se non è stata scelta (attraverso dei radio button) la metrica con la quale restituire i risultati
Input:
    textArea: oggetto Text dalla libreria tkinter
    metric: stringa per specificare la metrica da usare ('balanced_accuracy' oppure 'neg_mean_squared_error')
"""
def buttonKFold(textArea, metric):
    if len(metric) != 0:
        scores = Learning.getKFoldScores(metric)
        textArea.config(state = tk.NORMAL)
        textArea.insert(tk.INSERT, "\n")
        textArea.insert(tk.INSERT, "--------------------------------------------------------------\n")
        for classifier in scores.keys():
            textArea.insert(tk.INSERT, classifier + ": ")
            textArea.insert(tk.INSERT, scores[classifier])
            textArea.insert(tk.INSERT, "\n")
        textArea.insert(tk.INSERT, "--------------------------------------------------------------")
        textArea.see(tk.END)
        textArea.config(state = tk.DISABLED)
    else:
        textArea.config(state = tk.NORMAL)
        textArea.insert(tk.INSERT, "\n")
        textArea.insert(tk.INSERT, "Choose a metric\n")
        textArea.see(tk.END)
        textArea.config(state = tk.DISABLED)

"""
Stampa su textArea il classification report per un classificatore scelto attraverso dei radio button, altrimenti
restituisce un messaggio di errore in caso non sia stato selezionato un classificatore
Input:
    textArea: oggetto Text dalla libreria tkinter
    option: valore tra 1 e 3 per specificare il classificatore (Logistic Regression, Support Vector Machines, Random Forest Classifier)
    action: valore tra 0 e 1 che specifica se si voglia ottenere il classification report di un classificatore (valore 0)
            oppure se si vogliano effettuare predizioni su un file contenente dati (valore 1)
"""    
def buttonPred(textArea, option, action):
    if option is not None:
        textArea.config(state = tk.NORMAL)
        textArea.insert(tk.INSERT, "\n")
        textArea.insert(tk.INSERT, "--------------------------------------------------------------\n")
        if option == 1 and action == 0:
            textArea.insert(tk.INSERT, "Logistic Regression Table: \n")
        elif option == 2 and action == 0:
            textArea.insert(tk.INSERT, "Support Vector Machines Table: \n")
        elif option == 3 and action == 0:
            textArea.insert(tk.INSERT, "Random Forest Classifier Table: \n")
        elif option == 1 and action == 1:
            textArea.insert(tk.INSERT, "Logistic Regression Prediction: \n")
        elif option == 2 and action == 1:
            textArea.insert(tk.INSERT, "Support Vector Machines Prediction: \n")
        elif option == 3 and action == 1:
            textArea.insert(tk.INSERT, "Random Forest Classifier Prediction: \n")
        if action == 1:
            resultList = Learning.getPredForClassifier(option, 0.2, action)
            for result in resultList:
                textArea.insert(tk.INSERT, result + "\n")
        elif action == 0:
            textArea.insert(tk.INSERT, Learning.getPredForClassifier(option, 0.2, action) + "\n")
        textArea.insert(tk.INSERT, "--------------------------------------------------------------")
        textArea.see(tk.END)
        textArea.config(state = tk.DISABLED)
    else:
        textArea.config(state = tk.NORMAL)
        textArea.insert(tk.INSERT, "\n")
        textArea.insert(tk.INSERT, "Pick the choices\n")
        textArea.see(tk.END)
        textArea.config(state = tk.DISABLED)

"""
Ricrea la matrice contenente i valori di probabilità per la Bayesian Network e ne crea una nuova
per sostituirli
Input:
    textArea: oggetto Text dalla libreria tkinter
"""
def buttonProb(textArea):
        textArea.config(state = tk.NORMAL)
        textArea.insert(tk.INSERT, "\n")
        textArea.insert(tk.INSERT, "--------------------------------------------------------------\n")
        textArea.insert(tk.INSERT, "Creating probability scheme\n")
        textArea.config(state = tk.DISABLED)
        CSPprob.newProbability()
        textArea.config(state = tk.NORMAL)
        textArea.insert(tk.INSERT, "Probability scheme created; importing it into the BN\n")
        textArea.config(state = tk.DISABLED)
        probabilities = bn.seekMatrix("./utilities/probabilities.txt")
        BayesianNet.deleteNetwork()
        BayesianNet.initNetwork(probabilities)
        textArea.config(state = tk.NORMAL)
        textArea.insert(tk.INSERT, "Task Completed\n")
        textArea.insert(tk.INSERT, probabilities)
        textArea.insert(tk.INSERT, "\n")
        textArea.insert(tk.INSERT, "--------------------------------------------------------------")
        textArea.see(tk.END)
        textArea.config(state = tk.DISABLED)
 
"""
Stampa su textArea la predizione e la probabilità ottenute, attraverso la Bayesian Network, da dei valori specificati nei radio button;
se non sono definiti abbastanza valori (in particolare non è definito il grado di qualità dell'auto)
restituisce un messaggio che richiede di selezionare le scelte
Input:
    textArea: oggetto Text dalla libreria tkinter
    optionClass: valore del radio button per la scelta del grado di qualità dell'auto
    optionWork: valore del radio button per specificare se l'autovettura venga usata o meno per lavoro
"""
def buttonBN(textArea, optionClass, optionWork):
    args = list()
    if len(optionClass) != 0 and len(optionWork) != 0 and optionWork != "undefined":
        args.append(optionClass)
        args.append(optionWork)
        textArea.config(state = tk.NORMAL)
        textArea.insert(tk.INSERT, "\n")
        completePrediction = BayesianNet.getCompletePrediction(args, True)
        for prediction in completePrediction.keys():
            textArea.insert(tk.INSERT, prediction + ": ")
            textArea.insert(tk.INSERT, completePrediction[prediction])
            textArea.insert(tk.INSERT, "\n")
        textArea.insert(tk.INSERT, "\n")
        textArea.see(tk.END)
        textArea.config(state = tk.DISABLED)
    elif len(optionClass) != 0 and len(optionWork) != 0:
        args.append(optionClass)
        textArea.config(state = tk.NORMAL)
        textArea.insert(tk.INSERT, "\n")
        completePrediction = BayesianNet.getCompletePrediction(args, False)
        for prediction in completePrediction.keys():
            textArea.insert(tk.INSERT, prediction + ": ")
            textArea.insert(tk.INSERT, completePrediction[prediction])
            textArea.insert(tk.INSERT, "\n")
        textArea.insert(tk.INSERT, "\n")
        textArea.see(tk.END)
        textArea.config(state = tk.DISABLED)
    else:
        textArea.config(state = tk.NORMAL)
        textArea.insert(tk.INSERT, "\n")
        textArea.insert(tk.INSERT, "Pick the choices\n")
        textArea.see(tk.END)
        textArea.config(state = tk.DISABLED)

"""
Stampa su textArea il percorso migliore da un nodo di partenza ad uno obiettivo, selezionati attraverso
dei listbox
Input:
    textArea: oggetto Text dalla libreria tkinter
    optionStart: stringa che specifica la sede di partenza
    optionDestination: stringa che specifica la sede di arrivo
"""        
def buttonResearch(textArea, optionStart, optionDestination):
    selectionStart = optionStart.curselection()
    selectionDestination = optionDestination.curselection()
    if len(selectionStart) != 0 and len(selectionDestination) != 0:
        start = optionStart.get(selectionStart[0])
        destination = optionDestination.get(selectionDestination[0])
        if start == destination:
            textArea.config(state = tk.NORMAL)
            textArea.insert(tk.INSERT, "\n--------------------------------------------------------------\n")
            textArea.insert(tk.INSERT, "Cannot compute same location\n")
            textArea.insert(tk.INSERT, "--------------------------------------------------------------")
            textArea.config(state = tk.DISABLED)
        else:
            textArea.config(state = tk.NORMAL)
            textArea.insert(tk.INSERT, "\n--------------------------------------------------------------\n")
            textArea.insert(tk.INSERT, GraphSearch.idastarSearch(start, destination))
            textArea.insert(tk.INSERT, "\n--------------------------------------------------------------")
            textArea.config(state = tk.DISABLED)
    else:
        textArea.config(state = tk.NORMAL)
        textArea.insert(tk.INSERT, "\n--------------------------------------------------------------\n")
        textArea.insert(tk.INSERT, "Pick the choices\n")
        textArea.insert(tk.INSERT, "--------------------------------------------------------------")
        textArea.config(state = tk.DISABLED)
    textArea.see(tk.END)
        

"""
Cancella tutti i contenuti di un'area di testo
Input:
    textArea: oggetto Text dalla libreria tkinter
"""
def refresh(textArea):
    textArea.config(state = tk.NORMAL)
    textArea.delete("1.0", tk.END)
    textArea.config(state = tk.DISABLED)
        
if __name__ == "__main__":
    root = tk.Tk()
    Learning.initDataset("./dataset/dataset.csv")
    GraphSearch.initGraph()
    if not os.path.isfile("./utilities/map"):
        GraphSearch.computeHeuristicsDictionary()
    CSPprob.initCSP()
    if not os.path.isfile("./utilities/probabilities.txt"):
        CSPprob.newProbability()
    probabilities = bn.seekMatrix("./utilities/probabilities.txt")
    BayesianNet.initNetwork(probabilities)
    PrologKB.initKb()
    root.title("Icon Project")
    root.geometry("1280x720")
    root.resizable(0, 0)
    MainApplication(root).pack(side = "top", fill = "both", expand = True)
    root.mainloop()