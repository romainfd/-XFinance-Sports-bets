import requests
import datetime

dataType = 'win'
debut = datetime.datetime(2013, 1, 1)
fin = debut.today()

def dateToString(date):
	return zeroIfOneDigit(date.day)+zeroIfOneDigit(date.month)+str(date.year);

def zeroIfOneDigit(int):
	if (int < 10):
		return "0"+str(int)
	return str(int)

d = debut
with open("output_"+dataType+"_"+dateToString(debut)+"_"+dateToString(fin)+".csv", "w", encoding='utf-8') as file:
	file.write("event_id,place,event_name,date,racer_id,racer_name,win_lose,BSP,PPWAP,MORNINGWAP,PPMAX,PPMIN,IPMAX,IPMIN,MORNINGTRADEDVOL,PPTRADEDVOL,IPTRADEDVOL\n")
	while (d < fin):
		data = requests.get('http://www.betfairpromo.com/betfairsp/prices/dwbfgreyhound'+dataType+""+dateToString(d)+'.csv')
		if data.status_code == 200:
			tab = data.text[163:]
			file.write(tab)
			print(dateToString(d)+ " done.")
		d = d + datetime.timedelta(1)
	print("Done.")

