#deterministic markov chains on the %deltas in price
import json
from pprint import pprint
from datetime import datetime

#load quandl data
with open('btc.json') as data_file:    
    data = json.load(data_file)


#create list of tuples (date, % diff from previous state)
stateDateTimeDict = {}
stateList = []
stateDeltaList = []

for price in reversed(data["dataset"]["data"]):
	datetime = datetime.strptime(price[0], '%Y-%m-%d') 
	exchangeRate = price[4]
	stateDateTimeDict.update({datetime:exchangeRate}) #this probably won't be used because we don't care about dates currently

for price in reversed(data["dataset"]["data"]):
	if(price[4]==0):
		price[4] += .1
	stateList.append(price[4])

for i in range(1, len(stateList)):
	stateDeltaList.append(round(((stateList[i]-stateList[i-1])/stateList[i-1] * 100)))

# pprint(stateDict)
# pprint(stateDeltaList)
pprint(stateDeltaList)