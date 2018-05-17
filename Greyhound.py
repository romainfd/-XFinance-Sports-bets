import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import os.path
import Greyhounds.download as dnld
import time
import datetime

## PARAMETRES GLOBAUX
minRacersNb = 2 # nb of racer min to bet
dataPath = "Greyhounds/Output/"
factorLastRace = 1
tempFactor = 1
## /PARAMETRES

## CHOIX AUTOMATIQUE DE LA RACINE
racines = {
    'C:\\Users\\Romain Fouilland\\Documents\\Romain\\Travail\\Polytechnique\\Binets\\X Finance\\Horse racing': "C:/Users/Romain Fouilland/Documents/Romain/Travail/Polytechnique/Binets/X Finance/Horse racing/",
    'C:\\Users\\antoine':'C:/Users/antoine/Desktop/Polytechnique/Binet/X Finance/Sports bet/',
    'Users\\yassin': "/Users/yassinhamaoui/Desktop/data_sports_bets/" #a finir de remplir
}
racine = racines[os.getcwd()]
## /RACINE

## PARAMETERS BUILDING
# win or place ?
dataType = 'place'
# start and end dates (year, month, day)
debut = datetime.datetime(2018, 1, 1)
# fin = debut.today()
fin = datetime.datetime(2018, 4, 1)
## /PARAMETERS

# Télécharge les données voulues
def openData(dataType, debut, fin):
    # if the file already exists we do not download it again
    if (os.path.isfile(racine+dataPath+"output_"+dataType+"_"+debut.strftime("%d%m%Y")+"_"+fin.strftime("%d%m%Y")+".csv")):
        print("File already exists. Using existing data.")
        return racine+dataPath+"output_"+dataType+"_"+debut.strftime("%d%m%Y")+"_"+fin.strftime("%d%m%Y")+".csv"
    return dnld.getData(racine+dataPath, dataType, debut, fin)

# Traitement des données
    # enleve les entiers . et espace
def formatName(name):
    nameInit = name
    for i in range(len(nameInit)):
        if (ord(name[0]) >= 65 and ord(name[0]) <= 90):
            # on est bien sur une majuscule
            index = name.find("(")
            if (index >= 0):
                name = name[:index]
                if (name[-1] == " "):
                    name = name[:-1]
            return name.lower()
        # sinon, on supprime une lettre
        name = name[1:]
    # Commence TJS par une maj => on sort jamais du for
    print("Erreur sur le nom de cheval : "+nameInit)
    return nameInit

data=pd.read_csv(open(openData(dataType, debut, fin),encoding='utf-8'),index_col=0)
data=data[data.columns[:7]]
data.index.name='event_id'
data['win_lose']=data['win_lose'].fillna(0).astype(int)
data['racer_name'] = data['racer_name'].apply(lambda x: formatName(x))
print("Données chargées")

##
courses=pd.DataFrame(columns=['date', 'winners', 'racers'])
courses['date'] = data.groupby("event_id").apply(lambda x: x["date"].iloc[0])
courses['racers'] = data.groupby("event_id").apply(lambda x: np.array(x["racer_name"]))
courses['winners'] = data.groupby("event_id").apply(lambda x: np.repeat(x["racer_name"].values, x["win_lose"]))

racerAux=data.groupby('racer_name')
racer=pd.DataFrame(columns=['event_id','win_lose', 'date'])
racer['win_lose']=racerAux['win_lose'].apply(lambda x:np.array(x))
racer['event_id']=racerAux.apply(lambda x:np.array(x.index))
racer['date']=racerAux.apply(lambda x: np.array(x['date']))
print("Données triées")

## traitement de la date
def dateFromStr(dateStr):
    return datetime.datetime(int(dateStr[6:10]), int(dateStr[3:5]), int(dateStr[0:2]), int(dateStr[11:13]), int(dateStr[14:16]))

##
def strategie(event_id,nCourse=10):
    try:
        listRacer=courses['racers'].loc[event_id]
    except TypeError:
        listRacer=[courses['racers'].loc[event_id]]
    maxPerf=0
    bestRacer=listRacer[0]
    for racerName in listRacer:
        # On récupere les courses (et les résultats) faites par le racer
        coursesRacer=racer.loc[racerName]["event_id"]
        resultats=racer.loc[racerName]["win_lose"]
        # on se place à la course que l'on veut prédire (on apprend qu'avant)
        indexCourse=np.where(coursesRacer == event_id)[0][0]
        # comme les index sont croissants, on récupère directement le bon nb de courses dispos avant avec indexCourse
        nbCoursesUtilisables = min(indexCourse, nCourse)
        if (nbCoursesUtilisables == 0):
            continue
        # Calcul du score du racer
        #dateNow = dateFromStr(courses['date'].loc[event_id]) # date de la course étudiée
        #coursesDates = racer.loc[racerName]["date"][indexCourse - nbCoursesUtilisables:indexCourse] # date des courses précédentes
        #fonc = lambda date: 1/((dateNow - dateFromStr(date)).days+(dateNow - dateFromStr(date)).seconds/24*60*60) # pondérations pour chaque course prop. à proximité temporelle
        #ponde = np.array([fonc(x) for x in coursesDates])
        # vecteur de pondération
        ponde = np.arange(1, nbCoursesUtilisables + 1)**tempFactor
        # normalisation
        #print(ponde)
        ponde = ponde/np.sum(ponde)
        performance = np.dot(resultats[indexCourse - nbCoursesUtilisables:indexCourse], ponde) # nul si aucune course avant
        if (resultats[indexCourse - 1] == 1):
            performance *= factorLastRace
        if (performance>maxPerf):
            maxPerf=performance
            bestRacer=racerName
    return bestRacer

def backTest(strat):
    w=0
    nbBets = 0
    # set pour ne traiter qu'une fois chaque liste
    for i in courses.index:
        if courses.loc[i].size >= minRacersNb:
            # on parie sur cette course
            nbBets += 1
            if strat(i) in courses['winners'].loc[i]:
                # notre levrier est dans les gagnants
                w+=1
    return w/nbBets
##

t0 = time.time()
print(backTest(strategie))
print(time.time() - t0)
