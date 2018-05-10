import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import os.path
from Greyhounds.download import *

racine = "C:/Users/Romain Fouilland/Documents/Romain/Travail/Polytechnique/Binets/X Finance/Horse racing/"
#racine='C:/Users/antoine/Desktop/Polytechnique/Binet/X Finance/Data Sports bet/'
#racine="/Users/yassinhamaoui/Desktop/data_sports_bets/"

## PARAMETERS BUILDING
# win or place ?
dataType = 'place'
# start and end dates (year, month, day)
debut = datetime.datetime(2018, 5, 2)
fin = datetime.datetime(2018, 5, 5)
## /PARAMETERS

# Télécharge les données voulues
def openData(dataType, debut, fin):
    # if the file already exists we do not download it again
    # if (os.path.isfile(racine+"Greyhounds/Output/output_"+dataType+"_"+dateToString(debut)+"_"+dateToString(fin)+".csv")):
    #     print("File already exists. Using existing data.")
    #     return racine+"Greyhounds/Output/output_"+dataType+"_"+dateToString(debut)+"_"+dateToString(fin)+".csv"
    return getData(racine+"Greyhounds/", dataType, debut, fin)

data=pd.read_csv(open(openData(dataType, debut, fin),encoding='utf-8'),index_col=0)
data=data[data.columns[:7]]
data.index.name='event_id'

##
eventWinner=data.groupby("event_id").apply(lambda x: np.repeat(x["racer_id"].values,x["win_lose"]))

##
racerAux=data.groupby('racer_id')
racer=pd.DataFrame(columns=['event_id','win_lose'])
racer['win_lose']=racerAux['win_lose'].apply(lambda x:np.array(x))
racer['event_id']=racerAux.apply(lambda x:np.array(x.index))
 
##
def strategie(event_id,nCourse=10):
    try:
        listRacer=list(np.array(data.loc[event_id]["racer_id"]))
    except TypeError:
        listRacer=[data.loc[event_id]["racer_id"]]
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

print(backTest(strategie))