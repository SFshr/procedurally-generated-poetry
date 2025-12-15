import random
from collections import deque

def reweight_markov(adjdict,topweight,wordconstraintlist,gamma,glob_freq,startpoint,markov_jumps,feedback = False):
    lensen = len(wordconstraintlist)
    #generate counter filled with 0s with the same shape as wordconstraintlist
    prevqueue = deque(maxlen = 10)
    counter = []
    for constraint in wordconstraintlist:
        counter.append([[0]*len(cat) for cat in constraint])
    currstate = startpoint
    for _ in range(markov_jumps):
        i,j,k = currstate
        #print(currstate)
        if currstate in prevqueue and feedback:
            counter[i][j][k] = counter[i][j][k] + 5
        else:
            counter[i][j][k] = counter[i][j][k] + 1
        currword = wordconstraintlist[i][j][k]
        if feedback:
            prevqueue.appendleft(currstate)
        adjweight = adjdict[currword]
        #choose index in adjweight to visit with uniform prob, making sure it is within sentence
        lb,ub = 0,3
        if i < 2:
            lb = 2 - i
        if i > lensen-3:
            ub = lensen - i
        relindex = random.randint(lb,ub)
        nexti = [-2,-1,1,2][relindex] + i
        #choose what class of word to select, ensuring chosen class has words in it:
        compweights = []
        allowedj = []
        for classindex,(top, local) in enumerate(zip(topweight[nexti],adjweight[relindex])):
            nweight = gamma*top + (1-gamma)*local
            if wordconstraintlist[nexti][classindex]:
                compweights.append(nweight)
                allowedj.append(classindex)
        
        if all(x == 0 for x in compweights):
            nextj = random.choice(allowedj)
        else:
            nextj = random.choices(allowedj,compweights)[0]
        #choose word in this class using glob_freq 
        classchoice = wordconstraintlist[nexti][nextj]
        classchoiceweights = [glob_freq[c] for c in classchoice]
        nextk = random.choices(range(len(classchoice)),classchoiceweights)[0]
        currstate = (nexti,nextj,nextk)
    return counter

#DEBUGGING:
def fakeweight():
    partitions = [0] + sorted([random.uniform(0,1) for _ in range(6)]) + [1]
    weights = []
    for i in range(7):
        weights.append(partitions[i+1]-partitions[i])
    return weights

#compare two seperate runs to check convergence
def delta(r1,r2):
    diff = []
    for pairword in zip(r1,r2):
        diff.append([])
        for pairtype in zip(*pairword):
            difftype = [c1-c2 for c1,c2 in zip(*pairtype)]
            diff[-1].append(difftype)
    return diff

#get percentage diff
def deltaper(r1,r2):
    diff = []
    for pairword in zip(r1,r2):
        diff.append([])
        for pairtype in zip(*pairword):
            difftype = [abs(c1-c2)/sorted([c1,c2])[0] for c1,c2 in zip(*pairtype)]
            diff[-1].append(difftype)
    return diff

#check difference between numbers to make sure it does something
def maxcomp(r1):
    flattened = []
    for word in r1:
        for wordtype in word:
            flattened += wordtype
    av = sum(flattened)/len(flattened)
    return (max(flattened)-min(flattened))/av