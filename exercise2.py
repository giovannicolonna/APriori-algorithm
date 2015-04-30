__author__ = 'gio'

import random
import time
from itertools import combinations

START = time.time()
trialnumber = 0
resultsingles = [] #collect results for single values
resultcouples = [] #collect results for couples

#i create a set with all the possible couples of [1,2000] for statistical analisys
allThePossibleCouples = []
temp=[]
for i in range(1,2001):
    temp.append(i)
for elem in combinations(temp,2):
    allThePossibleCouples.append(elem)

while trialnumber<10:
    print "TEST NUMBER "+str(trialnumber)
    mapsOfInteger = {}

    #creation of integers dictionary
    for i in range(1,2001):
        mapsOfInteger[i]=0

    setOfCouples = {}

    mapOfFrequents = {}


    #creation of random dataset

    dataset = {}
    for i in range(1,100000+1):
        currentBasket = set()
        for elem in range(1,2001):
            #aggiungiamo elem con probabilita' 1/200 = 0.005
            guard = random.random()
            if guard<=0.005:
                currentBasket.add(elem)
        dataset[i] = currentBasket
        #set up the couple map, i use a couple as a key, and count them later
        for couple in combinations(currentBasket,2):
            setOfCouples[couple]=0

    for elem in dataset.values():
        for id in elem:
            mapsOfInteger[id]=mapsOfInteger[id]+1

    #count elemns which are over the expected value + 10% = 550
    print "- Counting single items appearing over the expected value + 10%"
    counting = 0
    avgvalue = 0.0
    for id in mapsOfInteger:
        howmany = mapsOfInteger[id]
        if howmany>550:
            counting = counting+1
            avgvalue=avgvalue+howmany
        mapOfFrequents[id] = howmany

    print "Total single items: "+str(counting)
    resultsingles.append(float(counting))
    print "Average: "+str(float(avgvalue/counting))

    #count couples which are more frequent than 5 times 2,5, (at least 13 times)
    print "\n"
    print "- Counting couples which are more frequent than 5 times the EV"
    countfreqcouples = 0
    for i in range(1,100000+1):
        for couple in combinations(dataset[i],2):
            setOfCouples[couple]=setOfCouples[couple]+1

    for elem in setOfCouples:
            if setOfCouples[elem]>12:
                countfreqcouples=countfreqcouples+1
                print "Couple: "+str(elem)+" appears: "+str(setOfCouples[elem])+" times."
                mapOfFrequents[elem] = setOfCouples[elem]
    print "There are in this test "+str(countfreqcouples)+" most-frequent couples"

    resultcouples.append(float(countfreqcouples))
    if countfreqcouples>0:
        #CALCULATE INTERESTINGNESS OF CURRENT FREQUENT COUPLES
        interestingnesses = []
        for couple in mapOfFrequents:
            if isinstance(couple,tuple):
                A = couple[0]
                B = couple[1]
                supAandB = mapOfFrequents[couple]
                supA = mapOfFrequents[couple[0]]
                supB = mapOfFrequents[B]
                m = 100000
                intAtoB = float(float(supAandB)/float(supA) - float(supB)/float(m))
                intBtoA = float(float(supAandB)/float(supB) - float(supA)/float(m))
                interestingnesses.append(intAtoB)
                interestingnesses.append(intBtoA)
        avgInt = float(sum(interestingnesses))/len(interestingnesses)
        print "Average interestingness of these frequent couples is: " + str(avgInt)
        print "\n"
    trialnumber=trialnumber+1
END = time.time()
print "FINAL RESULTS: average number of single elements above EV+10%: "+str((float(sum(resultsingles)))/10)
print "Average number of couples above 5 times the EV: "+str((float(sum(resultcouples)))/10)
print "Total time of testing:" + str(END - START)