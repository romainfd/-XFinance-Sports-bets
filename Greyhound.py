import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import os.path

##
#racine='C:/Users/antoine/Desktop/Polytechnique/Binet/X Finance/Data Sports bet/'
#racine="/Users/yassinhamaoui/Desktop/data_sports_bets/"

data=pd.read_csv(open(racine+'test.csv',encoding='utf-8'),index_col=0)
data=data[data.columns[:7]]
data.index.name='event_id'

##
event_winner=data.groupby("event_id").apply(lambda x: np.repeat(x["racer_id"].values,x["win_lose"]))

##
racerAux=data.groupby('racer_id')
racer=pd.DataFrame(columns=['event_id','win_lose'])
racer['win_lose']=racerAux['win_lose'].apply(lambda x:np.array(x))
racer['event_id']=racerAux.apply(lambda x:np.array(x.index))
 
##
def strategie(event_id,nCourse=10):
    #traiter le cas ou c'est un seul où 0 élement
    listRacer=np.array(data.loc[event_id]["racer_id"])
    maxPerf=0
    bestRacer=listRacer[0]
    for racerID in listRacer:
        #traiter le cas ou c'est un seul où 0 élement
        courses=list(racer.loc[racerID]["event_id"])
        indexCourse=courses.index(event_id)
        #traiter le cas ou c'est un seul où 0 élement
        resultats=list(racer.loc[racerID]["win_lose"])
        compteur=1
        performance=0
        while (indexCourse-compteur>=0 and compteur<=10) :
            performance+=resultats[indexCourse-Compteur]
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
    return w/s