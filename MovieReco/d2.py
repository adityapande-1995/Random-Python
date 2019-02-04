#!python3
import pandas as pd
from collections import defaultdict
from math import sqrt

def load_dataset():
    df = pd.read_csv("ml-latest-small/ratings.csv", nrows=1030)
    r,c = df.shape
    data = defaultdict(dict)
    for i in range(r):
        data[ df.iloc[i,:]['userId'] ][ df.iloc[i,:]['movieId'] ] = df.iloc[i,:]['rating']
    return data


def sim_distance(prefs,person1,person2): # Euclidean distance based score between 2 people
    common = [pow(prefs[person1][item]-prefs[person2][item],2) for item in prefs[person1] if item in prefs[person2]]
    if len(common) == 0:
        return 0
    else:
        return 1/(1 + sum(common))

def sim_pearson(prefs, p1,p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    
    n = len(si)
    if n == 0: return 0
    
    sum1 = sum([ prefs[p1][it] for it in si])
    sum2 = sum([ prefs[p2][it] for it in si])
    sum1Sq = sum([ pow(prefs[p1][it],2) for it in si])
    sum2Sq = sum([ pow(prefs[p2][it],2) for it in si])
    pSum = sum([ prefs[p1][it]*prefs[p2][it] for it in si ])

    # Calculate pearson score
    num = pSum - (sum1*sum2/n)
    den = sqrt((sum1Sq - pow(sum1,2)/n)*(sum2Sq - pow(sum2,2)/n))
    if den == 0: return 0
    return num/den

def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs,person,other),other) for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

def getRecos(prefs, person, similarity=sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs: # Iterate over critics
        if other == person: continue
        sim = similarity(prefs, person, other)

        if sim <= 0: continue
        for item in prefs[other]: # Iterate over a critics ratings
            if item not in prefs[person] or prefs[person][item] == 0: # If original persona hasnt rated it or rated it zero
                totals.setdefault(item,0)
                totals[item] += prefs[other][item]*sim
                simSums.setdefault(item,0)
                simSums[item] += sim

    rankings = [(total/simSums[item], item) for item,total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings

def transformPrefs(prefs): # Invert mapping from crtitic:movie (rating) to movie:critic (rating)
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})

            # Flip item and person
            result[item][person] = prefs[person][item]
    return result
