#deterministic markov chains on the %deltas in price
import json
from pprint import pprint
from datetime import datetime
import numpy as np 
from collections import defaultdict
from numpy import dot
from numpy.linalg import norm
import matplotlib.pyplot as plt

#needed to use because of issues with scipy install
def getCosSim(a, b):
	return dot(a, b)/(norm(a)*norm(b))

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
mostRecentPrice = 4171.09

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
weekVectors = list(getStates(stateDeltaList, 10))

# pprint(stateDict)
# pprint(stateDeltaList)
#pprint(stateDeltaList)
pprint("----------------------------------")
#print(weekVectors)

currentState = [-7, -2, 6, 4, -3, 2, 4, -4, -1, 3]

runningMax = 0;
runningPrediction = 0;
for pastState in weekVectors:
	#print(currentState)
	#print(pastState)
	#print(getCosSim(pastState[0], currentState))
	if(abs(getCosSim(pastState[0], currentState))>runningMax):

		runningMax=abs(getCosSim(pastState[0], currentState))
		runningPrediction = pastState[1]
	#	print(runningPrediction)	
#	print(abs(np.corrcoef(pastState[0], currentState)[0][1]))


def getPrediction(corpus, currentState):
	runningMax = 0
	runningPrediction = 0
	for corpusState in corpus:
		if(abs(getCosSim(corpusState[0], currentState))>runningMax and corpusState[1]<100):
			runningMax = abs(getCosSim(corpusState[0], currentState))
			runningPrediction = corpusState[1]
	return runningPrediction

print(getPrediction(weekVectors, currentState))
currentState.append(runningPrediction)



for x in range(1,100):
	currentState.append(getPrediction(weekVectors, currentState[x:]))

for i in range(0, len(currentState)):
	currentState[i] = (currentState[i]/100)*mostRecentPrice + mostRecentPrice
	mostRecentPrice = currentState[i]
print(currentState)
plt.plot(currentState)
plt.show()
#keeps going for number of desired predictions
# for i in range(0,6):
# print(runningPrediction)
# currentState.append(runningPrediction)
# plt.plot(currentState)
# plt.show()
#attempt #1, each "word" is 7 days (arbitrary period, assume some level of periodicity because of week, maybe will do fft later). 
#Similarity (correlation coeff) between 2 vectors is a weight, set boundary similarity for considered "equality" current goal is just to be able to guess direction accurately

