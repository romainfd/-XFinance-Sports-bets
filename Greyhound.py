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
tempFactor = 0.5
offsetDays = 365*5+30*4
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
debut = datetime.datetime(2013, 1, 1)
# fin = debut.today()
fin = datetime.datetime(2018, 5, 1)
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
    return nameInit[3:]

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
def strategie(event_id,nCourse=1000):
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
        if (courses.loc[i].size >= minRacersNb and (dateFromStr(courses.loc[i]['date']) - debut).days >= offsetDays):
            # on parie sur cette course
            nbBets += 1
            if strat(i) in courses['winners'].loc[i]:
                # notre levrier est dans les gagnants
                w+=1
    if nbBets == 0:
        return 0
    return w/nbBets
##

# t0 = time.time()
# print(backTest(strategie)*100)
# print(time.time() - t0)

#factors = [0.10, 0.20, 0.30, 0.40, 0.47, 0.485, 0.49, 0.495, 0.5, 0.505, 0.51, 0.515, 0.53, 0.6, 0.7, 0.8, 0.9, 1];
#results = []
#for i in range(len(factors)):
#    tempFactor = factors[i]
#    results.append(backTest(strategie))
#    print("Pour le tempFactor = {}, après {:.2f}s, on a obtenu une prévision de {}".format(factors[i], time.time() - t0, results[i]))
#    t0 = time.time()
#plt.plot(factors, results)
#plt.show()
#print(results)
#
#factors = [1.1, 1.2, 1.3, 1.4, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.5, 4, 4.5, 5]
#results = []
#for i in range(len(factors)):
#    tempFactor = factors[i]
#    results.append(backTest(strategie))
#    print("Pour le tempFactor = {}, après {:.2f}s, on a obtenu une prévision de {}".format(factors[i], time.time() - t0, results[i]))
#    t0 = time.time()
#plt.plot(factors, results)
#plt.show()
#print(results)
#
#factors= [7.5, 10, 12.5, 15, 20]
#results = []
#for i in range(len(factors)):
#    tempFactor = factors[i]
#    results.append(backTest(strategie))
#    print("Pour le tempFactor = {}, après {:.2f}s, on a obtenu une prévision de {}".format(factors[i], time.time() - t0, results[i]))
#    t0 = time.time()
#    
#plt.plot(factors, results)
#plt.show()
#print(results)

## Nb de course par lévriers
# print('step 1 : Nb de course par lévriers')
# 
# NbCourseGreyhound=racer['win_lose'].apply(lambda x : len(x)) # Nb de courses par racer
# 
# plt.figure()
# 
# plt.hist(NbCourseGreyhound,bins=np.arange(max(NbCourseGreyhound)+1)-0.5)
# 
# plt.title('Histogramme du nombre de courses effectuées par lévrier')
# plt.xlabel('Nombre de courses')
# plt.ylabel('Nombre de lévriers')
# plt.xlim(0,max(NbCourseGreyhound)+1)
# 
# consec=1 # paramètre du nombre de victoires consécutives
# 
# def filterVict(results,consecutive=consec): # fonction filtre nombre de victoires consécutives
#     t=0
#     for i in results:
#         if (i==1):
#             t+=1
#             if (t==consecutive):
#                 return True
#         else:
#             t=0
#     return False
# 
# filterWinLose=racer['win_lose'].apply(lambda x: filterVict(x,consec)) # filtre nombre de victoires consécutives
# 
# winners=racer.loc[filterWinLose] # tableau des winners
# losers=racer.loc[~filterWinLose] # tableau des losers
# 
# #nombre de courses courues par les winners/losers
# NbCourseWinners=winners['win_lose'].apply(lambda x : len(x)) 
# NbCourseLosers=losers['win_lose'].apply(lambda x : len(x))
# 
# # Affichage
# plt.figure()
# 
# plt.hist([NbCourseLosers,NbCourseWinners],bins=np.arange(max(NbCourseWinners)+1)-0.5,stacked=False,color=['r','b'],label=['Losers','Winners'])
# 
# plt.title('Histogramme du nombre de courses effectuées par lévrier')
# plt.xlabel('Nombre de courses')
# plt.ylabel('Nombre de lévriers')
# plt.legend()
# plt.xlim(0,max(NbCourseWinners)+1)
# 
# def auxRankVict(results,consecutive=consec): # fonction qui renvoie le rend de la première série de 'consecutive' victoires consécutives
#     t=0
#     rank=0
#     for i in results:
#         rank+=1
#         if (i==1):
#             t+=1
#             if (t==consecutive):
#                 return rank-consecutive+1
#         else:
#             t=0
#     return 0
# 
# rankVictories=winners['win_lose'].apply(lambda x: auxRankVict(x,consec)) # tableau du rang ddes premières victoires consécutives
# 
# # Affichage
# plt.figure()
# 
# plt.hist(rankVictories,bins=np.arange(max(rankVictories)+1)-0.5)
# 
# plt.title('Histogramme des rangs de la première série de {} victoire(s) consécutive(s)'.format(consec))
# plt.xlabel('Rang de la première série de {} victoire(s) consécutive(s)'.format(consec))
# plt.ylabel('Nombre de lévriers')
# 
# plt.show()
# 
# print('Nombre de racers : {}'.format(racer.index.size))
# print('Nombre de winners : {}'.format(winners.index.size))
# print('Nombre de cources : {}'.format(np.sum(NbCourseGreyhound)))

## Statistique longévité des racers
# print('step 2 : Statistique longévité des racers')
# 
# def filterlongevity(l): # fonction qui renvoie la différence en jour des dates de la dernière et de la première course
#     return(dateFromStr(l[-1])-dateFromStr(l[0])).days
# 
# longevities=racer['date'].apply(lambda x: filterlongevity(x)) # tableau des qui renvoie la longévité des racers
# 
# # longévité des winners/losers
# longevityWinners=longevities[filterWinLose]
# longevitiesLosers=longevities[~filterWinLose]
# 
# # Affichage
# plt.figure()
# 
# plt.hist([longevitiesLosers,longevityWinners],bins=np.arange(0,max(longevityWinners)+1,10)-0.5,stacked=False,color=['r','b'],label=['Losers','Winners'], normed=True)
# 
# plt.title('Durée de la période d\'activité des lévriers')
# plt.xlabel('Nb de jours')
# plt.ylabel('Pourcentage du nombre total de lévriers')
# plt.legend()
# plt.xlim(-1,max(longevityWinners)+1)
# 
# plt.figure()
# 
# 
# plt.hist([longevitiesLosers,longevityWinners],bins=np.arange(1,max(longevityWinners)+1,10)-0.5,stacked=False,color=['r','b'],label=['Losers','Winners'], normed=True)
# 
# plt.title('Durée de la période d\'activité des lévriers (si plus d\'une course)')
# plt.xlabel('Nb de jours')
# plt.ylabel('Pourcentage du nombre total de lévriers')
# plt.legend()
# plt.xlim(-1,max(longevityWinners)+1)
# 
# plt.show()


## Statistique sur les nouveaux racers
print('step 3 : Statistique sur les nouveaux racers')

NewRacerCourse=pd.DataFrame(columns=['New racer','Winner is new'],index=courses.index) # tableau donnant  pour chaque course le nombre de racer et de winner dont c'est la première course

for i in courses.index:
    s=0
    for r in courses['racers'].loc[i]:
        ind=racer['event_id'].loc[r][0]
        if(ind==i):
            s+=1
    NewRacerCourse['New racer'].loc[i]=s
    s=0
    for r in courses['winners'].loc[i]:
        ind=racer['event_id'].loc[r][0]
        if(ind==i):
            s+=1
    NewRacerCourse['Winner is new'].loc[i]=s

#Affichage
plt.figure()

plt.hist(NewRacerCourse['New racer'],bins=np.arange(max(NewRacerCourse['New racer']))-0.5,normed=True)


plt.title('Histogramme du nombre de nouveaux racers par course')
plt.xlabel('Nb de nouveaux racers')
plt.ylabel('Pourcentage de courses')
plt.xlim(-1,max(NewRacerCourse['New racer'])+1)

plt.figure()

plt.hist(NewRacerCourse['Winner is new'],bins=np.arange(max(NewRacerCourse['Winner is new']))-0.5,normed=True)


plt.title('Histogramme du nombre de winners sur leur 1ère course')
plt.xlabel('Nb de winners sur leur 1ère course')
plt.ylabel('Pourcentage de courses')
plt.xlim(-1,max(NewRacerCourse['Winner is new'])+1)

plt.show()

## Vérifier la croissance des dates dans le tableau racer
def CheckDate(l):
    if (len(l)<2):
        return True
    for i in range(len(l)-1):
        if((dateFromStr(l[i+1])-dateFromStr(l[i])).days+(dateFromStr(l[i+1])-dateFromStr(l[i])).seconds<=0):
            return False
    return True

print(racer.loc[~racer['date'].apply(lambda x: patternCheckDate(x))])
