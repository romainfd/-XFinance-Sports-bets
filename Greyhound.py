import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
##

#racine='C:/Users/antoine/Desktop/Polytechnique/Binet/X Finance/Sports bet'
#racine="/Users/yassinhamaoui/Desktop/data_sports_bets/"

data=pd.read_csv(open(racine+'test.csv',encoding='utf-8'),index_col=0)

event_winner=data.groupby("event_id").apply(lambda x: np.repeat(x["racer_id"].values,x["win_lose"]))

def strategie(event_id,nCourse=10):
    listRacer=np.array(data.loc["event_id"]["racer_id"])
    for racer in listRacer:
        

    


#df=data.groupby('EVENT_ID')

