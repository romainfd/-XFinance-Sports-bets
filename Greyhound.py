import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import os.path
##
racine='C:/Users/antoine/Desktop/Polytechnique/Binet/X Finance/Data Sports bet'

data=pd.read_csv(open(racine+'/test.csv'),index_col=0)
data=data[data.columns[:7]]
data.index.name='event_id'


##


racerAux=data.groupby('racer_id')

racer=pd.DataFrame(columns=['event_id','win_lose'])

racer['win_lose']=racerAux['win_lose'].apply(lambda x:np.array(x))
racer['event_id']=racerAux.apply(lambda x:np.array(x.index))
 
##


def backTest(strat):
    w=0
    for i in data.groupby(data.index).