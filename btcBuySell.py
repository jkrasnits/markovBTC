#deterministic markov chains on the %deltas in price
import json
from pprint import pprint
from datetime import datetime
import numpy as np 
from collections import defaultdict


def getStates(l, period):
    for i in range(0, len(l)-period-period):
        yield (l[i:(i+period)],l[i+period])

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
		price[4] = 1
	stateList.append(price[4])

for i in range(1, len(stateList)):
	stateDeltaList.append(round(((stateList[i]-stateList[i-1])/stateList[i-1] * 100)))

# turn data into vectors of length 7
weekVectors = list(getStates(stateDeltaList, 7))

# pprint(stateDict)
# pprint(stateDeltaList)
pprint(stateDeltaList)
pprint("----------------------------------")
print(weekVectors)

currentState = [1, 4, 1, 3, 6, 4, 3]

runningMax = 0;
runningPrediction = 0;
for pastState in weekVectors:
	print(currentState)
	print(pastState)
	if(abs(np.corrcoef(pastState[0], currentState)[0][1])>runningMax):
		runningMax=abs(np.corrcoef(pastState[0], currentState)[0][1])
		runningPrediction = pastState[1]
	print(runningPrediction)	
	print(abs(np.corrcoef(pastState[0], currentState)[0][1]))

print(runningPrediction)

#attempt #1, each "word" is 7 days (arbitrary period, assume some level of periodicity because of week, maybe will do fft later). 
#Similarity (correlation coeff) between 2 vectors is a weight, set boundary similarity for considered "equality" current goal is just to be able to guess direction accurately

