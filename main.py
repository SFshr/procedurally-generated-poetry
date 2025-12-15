from runparse import parse
from collapse import wfc
from markovrun import reweight_markov
import os

#check if wfc needs to be run again
def gencomplete(wordconstraintlist):
    for wordcon in wordconstraintlist:
        if not wordposition_collapsed(wordcon):
            return False
    return True

#check if a word position has only one word
def wordposition_collapsed(wordconstraint):
    populatedclasscount = 0
    for classcon in wordconstraint:
        if len(classcon)>1:
            return False
        elif len(classcon)==1:
            populatedclasscount += 1
    if populatedclasscount > 1:
        return False
    return True

#prints current progress - top weighted 2 words from each word class
def waveoutput(wordconstraintlist,counter):
    for weightedwordconstraint in zip(wordconstraintlist,counter):
        if wordposition_collapsed(weightedwordconstraint[0]):
            for wordclass in weightedwordconstraint[0]:
                if wordclass:
                    print('\033[92m'+wordclass[0]+'\033[0m')
        else:
            printlist = []
            for wordclass,classweights in zip(*weightedwordconstraint):
                weightedwordclass = list(zip(wordclass,classweights))
                sortedwordclass = sorted(weightedwordclass,key = lambda x: x[1],reverse = True)
                if len(sortedwordclass)>2:
                    classprint = [w[0] for w in sortedwordclass[:2]]
                    classprint[-1]+f' +{len(sortedwordclass)-2}'
                elif not sortedwordclass:
                    classprint = ['...']
                else:
                    classprint = [w[0] for w in sortedwordclass]
                printlist.append(','.join(classprint))
            print(' | '.join(printlist))

#create deep copy of cats to initialise wordconstraintlist
def copycats(cats):
    newcats = []
    for cat in cats:
        newcats.append([c for c in cat])
    return newcats

#generate sentence
def gen(senlen,features,markov_jumps,gamma_func = lambda x:0,debug_prints = False):
    topweight,freqdict,adjdict,combdictl,combdictr,cats = features
    wordconstraintlist = [copycats(cats) for _ in range(senlen)]
    collapsecount = 0
    while not gencomplete(wordconstraintlist):
        #start random walk on existing coordinate
        for classindex,wordclass in enumerate(wordconstraintlist[0]):
            if wordclass:
                startpoint = (0,classindex,0)
                break
        gamma = gamma_func(collapsecount)
        counter = reweight_markov(adjdict,topweight[senlen-2],wordconstraintlist,gamma,freqdict,startpoint,markov_jumps)
        if debug_prints:
            os.system('clear')
            waveoutput(wordconstraintlist,counter)
        wordconstraintlist = wfc(combdictl,combdictr,counter,wordconstraintlist)
        collapsecount += 1
    finishedsen = []
    for wordcon in wordconstraintlist:
        for classcon in wordcon:
            if classcon:
                finishedsen+=classcon
    return finishedsen

#function of how much of the sentence that has been decided that returns how much to favour global word class distribution over local in markov chain weights
def gamma_lindec(collapsecount):
    gamma = 1 + collapsecount*-0.25
    #range has to be between 0 and 1
    if gamma<0:
        gamma = 0
    return gamma

#generation interface
def main():
    print('parsing texts...')
    features = parse()
    markov_jumps = 4000
    stop = False
    while not stop:
        senlen = int(input(f'sentence length (slow for more than 7): '))
        gensen = gen(senlen,features,markov_jumps,debug_prints = True) #gamma_func = gamma_lindec
        os.system('clear')
        for w in gensen:
            print('\033[92m'+w+'\033[0m')
        genmore = None
        while genmore not in ['Y','n']:
            genmore = input('generate another? [Y/n]: ')
        if genmore == 'n':
            stop = True

if __name__ == '__main__':
    main()