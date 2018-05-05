import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import os.path

##
racine='C:/Users/antoine/Desktop/Polytechnique/Binet/X Finance/Data Sports bet'


#racine='C:/Users/antoine/Desktop/Polytechnique/Binet/X Finance/Sports bet'
#racine="/Users/yassinhamaoui/Desktop/data_sports_bets/"

data=pd.read_csv(open(racine+'test.csv',encoding='utf-8'),index_col=0)

event_winner=data.groupby("event_id").apply(lambda x: np.repeat(x["racer_id"].values,x["win_lose"]))

def strategie(event_id,nCourse=10):
    listRacer=np.array(data.loc["event_id"]["racer_id"])
    for racer in listRacer:
        
    

data=pd.read_csv(open(racine+'/test.csv'),index_col=0)
data=data[data.columns[:7]]
data.index.name='event_id'


##


racerAux=data.groupby('racer_id')

racer=pd.DataFrame(columns=['event_id','win_lose'])

racer['win_lose']=racerAux['win_lose'].apply(lambda x:np.array(x))
racer['event_id']=racerAux.apply(lambda x:np.array(x.index))
 
##

>>>>>>> 0588342e08c76df41d83ccc9b2d06cae855dcb8d

def backTest(strat):
    w=0
    for i in data.groupby(data.index).