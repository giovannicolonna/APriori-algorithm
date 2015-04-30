__author__ = 'gio'
from itertools import combinations
import time
import random
from collections import defaultdict



def compare():
    #i should check that randomized algorithm does not return itemsets not in the original algorithm result
    #Reads the file and return it like a set
    fRandomized= "outputRandomizedWithoutFP.dat"  #Randomize Alg Results
    fSimple= "outputNonRandomized.dat"  #aPriori Alg Results
    set1 = toSet(fSimple)
    set2 = toSet(fRandomized)

    for elem in set2:  #for each element in the randomize Results
        if elem not in set1:  #if is not in the aPriori Results
            print elem
            print 'Check on correctness of results: NOT PASSED'
            exit()

    print 'Check on correctness of results (if results of apriori randomized without FP are the contained in normal apriori): PASSED'


def toSet(file):
    result = set()
    f = open(file,'r')
    for line in f:
        tempString = ''
        for elem in line.split(): #for each basket
            tempString = tempString + str(elem) + ' '
        result.add(tempString)

    f.close()

    return result

##NON RANDOMIZED A-PRIORI, RANDOMIZED IS BELOW

print ("- - - SIMPLE APRIORI ALGORITHM EXECUTION - - -")

THRESHOLD = 500   #500 for retail.dat, 500.000 for webdocs
PROBABILITY = 0.1   #0.1 for retail.dat, 0.0001 for webdocs
INPUT = "retail.dat"   #select between retail.dat and webdocs.dat
START = time.time()

currentDict = {}
resDict = {}
filterset = {}

f = open(INPUT,"r")
output = open("outputNonRandomized.dat","w")
#first iteration, i set up singles elements
for line in f:
    for item in line.split():
        if item not in currentDict:
            currentDict[item]=1
        else:
            currentDict[item]=currentDict[item]+1
#I filter results
count = 0
toadd = []
for item in currentDict:
    if currentDict[item]>=THRESHOLD:
        resDict[item]=currentDict[item]
        output.write(item+"\n")
        toadd.append(item)
        count = count + 1
        #now resDict contains single items over threshold
filterset[1]=toadd

print "[Non-randomized apriori] " + str(count) + " frequent itemsets of size: 1"
currentDict = {}
count = 0

#n-ples analisys

k=2
while True:

    f = open(INPUT,"r")
    for line in f:
        #I read the line, which is a basket
        basket = line.split()
        filteredBasket = []

        #I filter the values of the basket according on what is already in result itemsets dictionary
        for elem in basket:
            if elem in filterset[k-1]:
                filteredBasket.append(elem)

        #now i perform combinations of k and add to the current dictionary result
        for nple in combinations(filteredBasket,k):
            if nple not in currentDict:
                currentDict[nple]=1
            else:
                currentDict[nple]=currentDict[nple]+1

    #I filter results, I compute the over-threshold list
    toadd = []
    for item in currentDict:
        if currentDict[item]>=THRESHOLD:
            resDict[item]=currentDict[item]

            #i write tuple values
            for elem in sorted(item):
                toadd.append(elem)
                output.write(str(elem)+" ")

            output.write("\n")
            count = count + 1
            #now resDict contains only nples over threshold
    filterset[k]=toadd
    print "[Non-randomized apriori] " + str(count) + " frequent itemsets of size: "+str(k)
    if count == 0:
        break
    currentDict = {}
    count = 0
    k=k+1




END = time.time()
print ("Total time elapsed, non-randomized a-priori: " + str(END-START)+"\n\n")
f.close()
output.close()


# ---------- END OF NON RANDOMIZED, NOW WE WILL PERFORM RANDOMIZED ANALISYS
#
#
#
#


#2 steps: one analysis with tpr and one with 0.9tpr

print "- - - RANDOMIZED APRIORI ALGORITHM EXECUTION - - -\n"
MAX_K = 0
step = 1
while step<3: #two steps
    START = time.time()

    if step==1:
        #STEP ONE, WITHOUT FALSE NEGATIVE REDUCTION
        print "STEP 1: original threshold t * p\n"
        RAND_THRESHOLD = float(float(THRESHOLD)*PROBABILITY)
    else:
        #STEP TWO: FALSE NEGATIVES REDUCTION
        print "STEP 2: false negatives reduction, 0.9 * p * t\n"
        RAND_THRESHOLD = float(float(THRESHOLD)*PROBABILITY)*0.9


    dataset = defaultdict(int)
    f = open(INPUT,"r")
    output2 = open("outputRandomized.dat","w")

    index=0
    for line in f:
        p = random.random()
        if p<=PROBABILITY:
            #temp.write(line)
            currbasket = []
            for elem in line.split():
                currbasket.append(elem)
            dataset[index]=currbasket
            index=index+1


    currentDict = {}
    randResDict = {}
    filterset = {}

    #first iteration, i set up singles elements
    for line in dataset:
        for item in dataset[line]:
            if item not in currentDict:
                currentDict[item]=1
            else:
                currentDict[item]=currentDict[item]+1
    #I filter results
    count = 0
    toadd = []
    for item in currentDict:
        if currentDict[item]>=RAND_THRESHOLD:
            randResDict[item]=currentDict[item]
            output2.write(item+"\n")
            toadd.append(item)
            count = count + 1
            #now resDict contains single items over threshold
    print "[Randomized apriori] " + str(count) + " frequent itemsets of size: 1"
    filterset[1]=toadd
    currentDict = {}
    count = 0

    #n-ples analisys

    k=2
    while True:

        #temp = open("temp.dat","r")
        for line in dataset:
            #I read the line, which is a basket
            basket = dataset[line]
            filteredBasket = []

            #I filter the values of the basket according on what is already in result itemsets dictionary (which contains already)
            #n-ples over the threshold
            for elem in basket:
                if elem in filterset[k-1]:
                    filteredBasket.append(elem)

            #now i perform combinations of k and add to the current dictionary result
            for nple in combinations(filteredBasket,k):
                if nple not in currentDict:
                    currentDict[nple]=1
                else:
                    currentDict[nple]=currentDict[nple]+1


        #I filter results, I compute the over-threshold list
        toadd = []
        for item in currentDict:
            if currentDict[item]>=RAND_THRESHOLD:
                #if i'm above the threshold, i put the nple in resdict
                randResDict[item]=currentDict[item]
                #i write tuple values
                for elem in item:
                    output2.write(str(elem)+" ")
                    toadd.append(elem)
                output2.write("\n")
                count = count + 1
                #now resDict contains only nples over threshold
        filterset[k]=toadd
        print "[Randomized apriori] " + str(count) + " frequent itemsets of size: "+str(k)
        if count == 0:
            MAX_K = k
            break


        currentDict = {}
        count = 0

        k=k+1



    print "\n"

    output2.close()


    print "False-positives elimination:"


    #FALSE POSITIVE: frequent in the sample but not in the whole
    #FALSE NEGATIVE: frequent in the whole but not in the sample

    falsepositivescount = 0  #conta il numero di falsi positivi
    falsenegativescount = 0  #conta il numero di falsi negativi
    falsepositive = []  #array che conterra' i falsi positivi per eliminarli dal risultato

    fpDict = {} #dizionario degli itemsets letti da file per la verifica dei FP

    randomMatrix = {} #mappa che contiene i risultati del random divisi per lunghezza

    for res in randResDict:
        if isinstance(res,tuple):
            if len(res) not in randomMatrix:
                randomMatrix[len(res)]=set()
                randomMatrix[len(res)].add(res)
            else:
                for elem in res:
                    randomMatrix[len(res)].add(elem)
        else:
            if 1 not in randomMatrix:
                randomMatrix[1] = set()
                randomMatrix[1].add(res)
            else:
                randomMatrix[1].add(res)





    f = open(INPUT,"r")
    z = 0
    for line in f:
        #if z%5000 == 0:
         #   print z
        z += 1
        #I read the line, which is a basket
        basket = set(line.split())

        for k in range(1,MAX_K):
            toCombine = basket.intersection(randomMatrix[k])

            #now i perform combinations of k and add to the current dictionary result
            comblist = combinations(toCombine,k)
            for nple in comblist:
                if nple not in fpDict:
                    fpDict[nple]=1
                else:
                    fpDict[nple]=fpDict[nple]+1

    f.close()

    finalResult = {}

    for item in fpDict:
        if fpDict[item]>=THRESHOLD:
            finalResult[item] = fpDict[item]

    print "Apriori randomized without FP contains: "+str(len(finalResult))+" elements:"

    #print of results without fp
    toPrint = defaultdict(int)
    for elem in finalResult:
        if not isinstance(elem,tuple):
            toPrint[1] += 1
        else:
            toPrint[len(elem)] += 1

    for k in range(1,len(toPrint)+1):
        print "[Randomized apriori without FP] "+str(toPrint[k])+" elements of size: " + str(k)

    output3 = open("outputRandomizedWithoutFP.dat","w")

    for element in finalResult:
        if isinstance(element,tuple):
            for item in sorted(element):
                output3.write(item+" ")
            output3.write("\n")
        else:
            output3.write(element+"\n")

    output3.close()


    f1 = open("outputNonRandomized.dat","r")
    f2 = open("outputRandomizedWithoutFP.dat","r")
    lengthf1 = 0
    lengthf2 = 0
    for line in f1:
        lengthf1 += 1
    f1.close()
    for line in f2:
        lengthf2 += 1
    f2.close()
    falsenegativescount = lengthf1 - lengthf2
    print str(falsenegativescount)+" false negatives have been detected.\n"


    END = time.time()
    if step==1:
        print ("Total time elapsed, randomized a-priori (with false positive elimination): " + str(END-START)+"\n")
    else:
        print ("Total time elapsed, randomized a-priori (with FP elimination AND FN reduction): "+str(END-START)+"\n")
    step = step+1

compare()   #I PERFORM THE CORRECTNESS OF RESULTS, method is on head of this file


