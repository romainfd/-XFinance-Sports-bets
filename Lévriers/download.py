import requests
import datetime

dataType = 'place'
debut = datetime.datetime(2012, 9, 20)
end = debut.today()

def dateToString(date):
	return zeroIfOneDigit(date.day)+zeroIfOneDigit(date.month)+str(date.year);

def zeroIfOneDigit(int):
	if (int < 10):
		return "0"+str(int)
	return str(int)

d = debut
data = requests.get('http://www.betfairpromo.com/betfairsp/prices/dwbfgreyhound'+dataType+""+dateToString(d)+'.csv')
print(data.text)
d = debut
with open("output.csv") as file:
	while (d < end):
		data = requests.get('http://www.betfairpromo.com/betfairsp/prices/dwbfgreyhound'+dataType+""+dateToString(d)+'.csv')
		if data.status_code == 200:
			print(dateToString(d))
			#print(data.text)
		d = d + datetime.timedelta(1)