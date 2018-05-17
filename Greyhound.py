import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import os.path
import Greyhounds.download as dnld


##
racine = "C:/Users/Romain Fouilland/Documents/Romain/Travail/Polytechnique/Binets/X Finance/Horse racing/"
#racine='C:/Users/antoine/Desktop/Polytechnique/Binet/X Finance/Data Sports bet/'
#racine="/Users/yassinhamaoui/Desktop/data_sports_bets/"

dataPath = "Greyhounds/Output/"
## PARAMETERS BUILDING
# win or place ?
dataType = 'place'
# start and end dates (year, month, day)
debut = dnld.datetime.datetime(2018, 1, 1)
# fin = debut.today()
fin = dnld.datetime.datetime(2018, 4, 1)
## /PARAMETERS

# Télécharge les données voulues
def openData(dataType, debut, fin):
    # if the file already exists we do not download it again
    if (os.path.isfile(racine+dataPath+"/output_"+dataType+"_"+dnld.dateToString(debut)+"_"+dnld.dateToString(fin)+".csv")):
        print("File already exists. Using existing data.")
        return racine+"Greyhounds/Output/output_"+dataType+"_"+dnld.dateToString(debut)+"_"+dnld.dateToString(fin)+".csv"
    return dnld.getData(racine+dataPath, dataType, debut, fin)

data=pd.read_csv(open(openData(dataType, debut, fin),encoding='utf-8'),index_col=0)
data=data[data.columns[:7]]
data.index.name='event_id'
data['win_lose']=data['win_lose'].fillna(0).astype(int)
data['racer_name'] = data['racer_name'].apply(lambda x: x[3:])
print("Donnéees chargées")

##
eventWinner=data.groupby("event_id").apply(lambda x: np.repeat(x["racer_name"].values, x["win_lose"]))

racerAux=data.groupby('racer_name')
racer=pd.DataFrame(columns=['event_id','win_lose'])
racer['win_lose']=racerAux['win_lose'].apply(lambda x:np.array(x))
racer['event_id']=racerAux.apply(lambda x:np.array(x.index))
 
print("Données triées")
##
def strategie(event_id,nCourse=10):
    try:
        listRacer=list(np.array(data.loc[event_id]["racer_name"]))
    except TypeError:
        listRacer=[data.loc[event_id]["racer_name"]]
    maxPerf=0
    bestRacer=listRacer[0]
    for racerID in listRacer:
        courses=list(racer.loc[racerID]["event_id"])
        indexCourse=courses.index(event_id)
        resultats=list(racer.loc[racerID]["win_lose"])
        compteur=1
        performance=0
        while (indexCourse-compteur>=0 and compteur<=nCourse) :
            performance+=resultats[indexCourse-compteur]
            compteur+=1
        if (performance>maxPerf):
            maxPerf=performance
            bestRacer=racerID
    return bestRacer

def backTest(strat):
    w=0
    s=set(data.index)
    for i in s:
        if strat(i) in eventWinner.loc[i]:
            w+=1
    return w/len(s)
##♦


print(backTest(strategie))
