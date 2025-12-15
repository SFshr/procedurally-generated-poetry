import random
import math

def wfc(combdictl,combdictr,counter,wordconstraintlist):
  #collapse a minimum entropy position
  entropylist = entlist(counter)
  linelen = len(wordconstraintlist)
  leastindexes = minentropy(entropylist)
  chosensentindex = random.choice(leastindexes)
  chosenconstraints = wordconstraintlist[chosensentindex]
  chosenweights = counter[chosensentindex]
  #choose wordclass, word:
  potclassindexes = []
  potclassweights = []
  for classindex,potclass in enumerate(chosenconstraints):
    if potclass:
      potclassindexes.append(classindex)
      potclassweights.append(sum(chosenweights[classindex]))
  chosenclassindex = random.choices(potclassindexes,potclassweights)[0]
  chosenwordindex = random.choices(range(len(chosenconstraints[chosenclassindex])),chosenweights[chosenclassindex])[0]
  collapsedword = chosenconstraints[chosenclassindex][chosenwordindex]
  newchosenconstraints = [[] for _ in range(len(chosenconstraints))]
  newchosenconstraints[chosenclassindex] = [collapsedword]
  wordconstraintlist[chosensentindex] = newchosenconstraints
  
  #propogate collapse using adjacency conditions
  #propogating left:
  prevconstraints = newchosenconstraints
  for i in range(chosensentindex-1,-1,-1):
    if entropylist[i] == 0:
      break
    currentconstraints = wordconstraintlist[i]
    targetconstraints = set()
    for prevwordclass in prevconstraints:
      for prevword in prevwordclass:
        targetconstraints.update(combdictl[prevword])
    newconstraints = []
    for constraintclass in currentconstraints:
      newconstraints.append([c for c in constraintclass if c in targetconstraints])
    if currentconstraints == newconstraints:
      break
    wordconstraintlist[i] = newconstraints
    prevconstraints = newconstraints
  
  #propogating right:
  prevconstraints = newchosenconstraints
  for i in range(chosensentindex+1,linelen):
    if entropylist[i] == 0:
      break
    currentconstraints = wordconstraintlist[i]
    targetconstraints = set()
    for prevwordclass in prevconstraints:
      for prevword in prevwordclass:
        targetconstraints.update(combdictr[prevword])
    newconstraints = []
    for constraintclass in currentconstraints:
      newconstraints.append([c for c in constraintclass if c in targetconstraints])
    if currentconstraints == newconstraints:
      break
    wordconstraintlist[i] = newconstraints
    prevconstraints = newconstraints
  return wordconstraintlist
    
#returns list of minimum nonzero entropy
def minentropy(entropylist):
  minentropy = 10
  minindex = []
  for i,entropy in enumerate(entropylist):
    if entropy != 0 and entropy < minentropy:
      minentropy = entropy
      minindex = [i]
    elif entropy == minentropy:
      minindex.append(i)
  return minindex

def entlist(counter):
  #flatten counter, get sum of weights:
  entroplist = []
  for wordcount in counter:
    classcounter=[]
    for classcount in wordcount:
      classcounter += classcount
    entroplist.append(entropy(classcounter))
  return entroplist

#measure of how constrained each position in word list is
def entropy(weightlist):
  weightsum = 0
  logweightsum = 0
  for cfreq in weightlist:
    if cfreq > 0:
      logfreq = math.log(cfreq,2)
      weightsum += cfreq
      logweightsum += cfreq*logfreq
  return math.log(weightsum,2) - (logweightsum/weightsum)
  
