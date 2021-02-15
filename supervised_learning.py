import pandas as pd
import pickle as p
import os.path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score

"""
Recupera il dataset dal path
Input:
    path: path del file in cui si trova il dataset
Output:
    Il dataset
"""
def recoverDataset(path):
    return pd.read_csv(path)

"""
Recupera dal dataset tutti i valori per le feature di input
Input:
    dataset: il dataset
Output:
    X: I valori per le feature di input, a cui è stato anche applicato un OrdinalEncoder
    per gestire le feature ordinali
    enc: Ordinal Encoder utilizzato nel preprocessing di X
"""
def splitX(dataset):
    X = dataset.drop("class", axis = 1)
    enc = OrdinalEncoder(categories = [["low", "med", "high", "vhigh"], ["low", "med", "high", "vhigh"], ["2", "3", "4", "5more"], ["2", "4", "more"], ["small", "med", "big"], ["low", "med", "high"]])
    X = enc.fit_transform(X[["buying", "maint", "doors", "persons", "lug_boot", "safety"]])
    return (X, enc)

"""
Recupera dal dataset tutti i valori per le feature obiettivo
Input:
    dataset: il dataset
Output:
    y: I valori per le feature obiettivo, a cui è stato anche applicato un LabelEconder
    per tradurre i valori di tipo Stringa in Interi
    le: Label Encoder utilizzato nel preprocessing di y
"""
def splity(dataset):
    y = dataset["class"]
    le = LabelEncoder()
    y = le.fit_transform(y)
    return (y, le)

"""
Restituisce le medie dei punteggi della K-Fold Cross Validation (con k = 10) per 3 classificatori diversi, ovvero
Logistic Regression (massimo numero di iterate = 2000), Support Vector Machines e Random Forest Classifier (numero di alberi di default = 100)
Input:
    X: insieme dei valori per le feature di input
    y: insieme dei valori per le feature obiettivo
    metric: stringa che specifica il tipo di punteggio restituito dalla Cross Validation ('balanced_accuracy', 'neg_mean_absolute_error', ecc.)
Output:
    scoreList: dizionario con chiave una stringa che specifica il classificatore e come valore la media del punteggio della Cross Validation 
"""
def getKFoldScores(X, y, metric):
    scoreList = dict()
    scoreList["Logistic Regression"] = cross_val_score(LogisticRegression(max_iter = 2000), X, y, cv = 10, scoring = metric).mean()
    scoreList["Support Vector Machines"] = cross_val_score(SVC(), X, y, cv = 10, scoring = metric).mean()
    scoreList["Random Forest Classifier"] = cross_val_score(RandomForestClassifier(), X, y, cv = 10, scoring = metric).mean()
    return scoreList

"""
Restituisce il classification report (contenente varie informazioni come Precision, Recall, ecc.) per la predizione ottenuta
dal classificatore Logistic Regression (massimo numero di iterate = 2000) su train e test set, oppure il risultato
di classificazioni effettuate su istanze caricate da file testuale
Input:
    X: insieme dei valori per le feature di input
    y: insieme dei valori per le feature obiettivo
    testsize: specifica la grandezza dello split dei dati di test rispetto a quelli di training
    labelEncoder: label encoder usato precedentemente per il preprocessing
    ordinalEncoder: ordinal encoder usato precedentemente per il preprocessing
    i: valore intero per scegliere se restituire il classification report (i = 0) o classificare delle istanze da file (i = 1)
    path: path del file in cui si trovano le istanze da classificare
Output:
    Classification Report sul test set oppure classi predette su istanze da file
"""
def logisticRegressionPred(X, y, testsize, labelEncoder, ordinalEncoder, i, path):
    lr = None
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = testsize, random_state = 42)
    if not os.path.isfile("./utilities/logisticRegressionModel"):
        lr = LogisticRegression(max_iter = 2000)
        lr.fit(X_train, y_train)
        with open("./utilities/logisticRegressionModel", "wb") as f:
            p.dump(lr, f)
    else:
        with open("./utilities/logisticRegressionModel", "rb") as f:
            lr = p.load(f)
    if i == 0:
        pred_lr = lr.predict(X_test)
        return classification_report(y_test, pred_lr)
    elif i == 1:
        query = list()
        with open(path, "r") as f:
            queryList = [line.strip().split(",") for line in f if line and line[0].isalpha()]
        for queryText in queryList:
            query.append(queryText)
        query = ordinalEncoder.transform(query)
        prediction = lr.predict(query)
        prediction = labelEncoder.inverse_transform(prediction)
        return prediction

"""
Restituisce il classification report (contenente varie informazioni come Precision, Recall, ecc.) per la predizione ottenuta
dal classificatore Support Vector Machines su train e test set, oppure il risultato
di classificazioni effettuate su istanze caricate da file testuale
Input:
    X: insieme dei valori per le feature di input
    y: insieme dei valori per le feature obiettivo
    testsize: specifica la grandezza dello split dei dati di test rispetto a quelli di training
    labelEncoder: label encoder usato precedentemente per il preprocessing
    ordinalEncoder: ordinal encoder usato precedentemente per il preprocessing
    i: valore intero per scegliere se restituire il classification report (i = 0) o classificare delle istanze da file (i = 1)
    path: path del file in cui si trovano le istanze da classificare
Output:
    Classification Report sul test set oppure classi predette su istanze da file
"""
def supportVectorMachinesPred(X, y, testsize, labelEncoder, ordinalEncoder, i, path):
    svm = None
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = testsize, random_state = 42)
    if not os.path.isfile("./utilities/supportVectorMachinesModel"):
        svm = SVC()
        svm.fit(X_train, y_train)
        with open("./utilities/supportVectorMachinesModel", "wb") as f:
            p.dump(svm, f)
    else:
        with open("./utilities/supportVectorMachinesModel", "rb") as f:
            svm = p.load(f)
    if i == 0:
        pred_svm = svm.predict(X_test)
        return classification_report(y_test, pred_svm)
    elif i == 1:
        query = list()
        with open(path, "r") as f:
            queryList = [line.strip().split(",") for line in f if line and line[0].isalpha()]
        for queryText in queryList:
            query.append(queryText)
        query = ordinalEncoder.transform(query)
        prediction = svm.predict(query)
        prediction = labelEncoder.inverse_transform(prediction)
        return prediction

"""
Restituisce il classification report (contenente varie informazioni come Precision, Recall, ecc.) per la predizione ottenuta
dal classificatore Random Forest Classifier (numero di alberi di default = 100) su train e test set, oppure il risultato
di classificazioni effettuate su istanze caricate da file testuale
Input:
    X: insieme dei valori per le feature di input
    y: insieme dei valori per le feature obiettivo
    testsize: specifica la grandezza dello split dei dati di test rispetto a quelli di training
    labelEncoder: label encoder usato precedentemente per il preprocessing
    ordinalEncoder: ordinal encoder usato precedentemente per il preprocessing
    i: valore intero per scegliere se restituire il classification report (i = 0) o classificare delle istanze da file (i = 1)
    path: path del file in cui si trovano le istanze da classificare
Output:
    Classification Report sul test set oppure classi predette su istanze da file
"""
def randomForestClassifierPred(X, y, testsize, labelEncoder, ordinalEncoder, i, path):
    rfc = None
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = testsize, random_state = 42)
    if not os.path.isfile("./utilities/randomForestClassifierModel"):
        rfc = RandomForestClassifier()
        rfc.fit(X_train, y_train)
        with open("./utilities/randomForestClassifierModel", "wb") as f:
            p.dump(rfc, f)
    else:
        with open("./utilities/randomForestClassifierModel", "rb") as f:
            rfc = p.load(f)
    if i == 0:
        pred_rfc = rfc.predict(X_test)
        return classification_report(y_test, pred_rfc)
    elif i == 1:
        query = list()
        with open(path, "r") as f:
            queryList = [line.strip().split(",") for line in f if line and line[0].isalpha()]
        for queryText in queryList:
            query.append(queryText)
        query = ordinalEncoder.transform(query)    
        prediction = rfc.predict(query)
        prediction = labelEncoder.inverse_transform(prediction)
        return prediction