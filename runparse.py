import json
import re
from collections import deque

def opencat(fpath):
  wordf = open(fpath)
  wordset = set(wordf.read().splitlines())
  wordf.close()
  return wordset

def parse():
  nouns = opencat('wordcats/c_nouns.txt')
  verbs = opencat('wordcats/c_verbs.txt')
  adjectives = opencat('wordcats/c_adjectives.txt')
  adverbs = opencat('wordcats/c_adverbs.txt')
  prepositions = opencat('wordcats/c_prepositions.txt')
  conjunctions = opencat('wordcats/c_conjunctions.txt')
  pronouns = opencat('wordcats/c_pronouns.txt')
  allwords = opencat('wordcats/allwords.txt')
  cats = [nouns,verbs,adjectives,adverbs,prepositions,conjunctions,pronouns]
  
  corpusf = open('gutenberg-poetry-v001 (1).ndjson 2')
  corpuslist = corpusf.readlines()
  corpusf.close()

  #return index position in counts for that word class, if not categorised return -1
  def catword(word,cats):
    for i in range(len(cats)):
      if word in cats[i]:
        return i
    return -1
  #longest line: 16, shortest line: 2
  #index 0 is line length 2 (minus 2 from sentence length to get index)
  #(nouns, verbs,adjectives, adverbs, prepositions, conjunctions, pronouns)
  topweight = [[[0,0,0,0,0,0,0] for _ in range(sentlen)] for sentlen in range(2,17)]
  #counrt how many times a word appears
  freqdict = {w:0 for w in allwords}
  #distributions of word class in the 4 spaces around word
  adjdict = {word:[[0,0,0,0,0,0,0] for _ in range(4)] for word in allwords}
  #adjacency constraints (if two words are adjacent in the output they must have been adjacent somewhere in the corpus):
  combdictl = {word:set() for word in allwords}
  combdictr = {word:set() for word in allwords}

  #in first corpus pass create plist which has lists of lines for each text
  pastgid = '19'
  plist = [[]]
  for line in corpuslist:
    jel = json.loads(line)
    if jel['gid'] == pastgid:
      plist[-1].append(jel['s'])
    else:
      plist.append([jel['s']])
    pastgid = jel['gid']

  parseplist = []
  for text in plist:
    parseplist.append([])
    for line in text:
      wordlist = re.split('\W+',line)
      if wordlist[-1] == "":
        wordlist = wordlist[:-1]
      wordlist = [word.lower() for word in wordlist]
      #add to topweight,freqdict:
      ctopw = topweight[len(wordlist)-2]
      for i,word in enumerate(wordlist):
        wordclass = catword(word,cats)
        if wordclass != -1:
          ctopw[i][wordclass] += 1
          freqdict[word] += 1
      #add to adjdict, adjacency constraints:
      if len(wordlist)>2:
        startlist = [catword(word,cats) for word in wordlist[:3]]
        wordwind = deque([-1,-1]+startlist,maxlen = 5)
      else:
        startlist = [catword(word,cats) for word in wordlist[:2]]
        wordwind = deque([-1,-1]+startlist+[-1],maxlen = 5)
      posmap = [0,1,None,2,3]
      for i,word in enumerate(wordlist):
        if word in allwords:
          for pos,adjwordclass in enumerate(wordwind):
            if pos != 2 and adjwordclass != -1:
              dictpos = posmap[pos]
              adjdict[word][dictpos][adjwordclass] += 1
          '''#adjacency left:
          if wordwind[1]!=-1:
            combdictl[word][wordwind[1]].add(wordlist[i-1])
          #adjacency right:
          if wordwind[3]!=-1:
            combdictr[word][wordwind[3]].add(wordlist[i+1])'''
          #due to overlap between word classes contents of combdictl,combdictr are currently not seperated into the classes :(
          #adjacency left:
          if wordwind[1]!=-1:
            combdictl[word].add(wordlist[i-1])
          #adjacency right:
          if wordwind[3]!=-1:
            combdictr[word].add(wordlist[i+1])
        if i+3<len(wordlist):
          wordwind.append(catword(wordlist[i+3],cats))
        else:
          wordwind.append(-1)
  combdictl = {word:list(combdictl[word]) for word in allwords}
  combdictr = {word:list(combdictr[word]) for word in allwords}
  return (topweight,freqdict,adjdict,combdictl,combdictr,cats)