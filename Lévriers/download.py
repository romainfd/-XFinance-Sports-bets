import requests
import datetime


## TEST LOCAL
# win or place ?
dataType = 'win'
# start and end dates (year, month, day)
debut = datetime.datetime(2018, 5, 1)
fin = debut.today()
## /PARAMETERS

# formats a date to DDMMYYYY : date.strftime("%Y%m%d") would have worked as well
def dateToString(date):
	return zeroIfOneDigit(date.day)+zeroIfOneDigit(date.month)+str(date.year);

# formats an integer to a string *II (ex: 9 -> 09, 11->11, 104->104)
def zeroIfOneDigit(int):
	if (int < 10):
		return "0"+str(int)
	return str(int)

# Core of the program
# Downloads the data from betfair for every day between start and end dates (if available)
# Stores the data of each (minus the row of column names) in a gloabl csv file in a folder outside of the git repo (called Data Horse Racing and at the same level)
def getData(dataType, debut, fin):
	d = debut
	cpt = 0
	with open("output/output_"+dataType+"_"+dateToString(debut)+"_"+dateToString(fin)+".csv", "w", encoding='utf-8') as file:
		file.write("event_id,place,event_name,date,racer_id,racer_name,win_lose,BSP,PPWAP,MORNINGWAP,PPMAX,PPMIN,IPMAX,IPMIN,MORNINGTRADEDVOL,PPTRADEDVOL,IPTRADEDVOL\n")
		while (d < fin):
			data = requests.get('http://www.betfairpromo.com/betfairsp/prices/dwbfgreyhound'+dataType+""+dateToString(d)+'.csv')
			if data.status_code == 200:
				tab = data.text[163:]
				file.write(tab)
				cpt += 1
				print(dateToString(d)+ " done.")
			d = d + datetime.timedelta(1)
		print("Done: {} data-days have been downloaded between the dates of {} and {}".format(cpt, debut.strftime("%d-%m-%y"), fin.strftime("%d-%m-%y")))
	return "Lévriers/output/output_"+dataType+"_"+dateToString(debut)+"_"+dateToString(fin)+".csv"

getData(dataType, debut, fin)
