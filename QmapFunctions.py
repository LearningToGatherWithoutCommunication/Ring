import math

def euclideanDistance(Q1,Q2):
    d = 0
    for (state,temp) in Q1.items():
        for (a,v) in temp.items():
            if state in Q2.keys():
                if a in Q2[state].keys():
                    d = d + (Q2[state][a] - v)**2
                else:
                    d = d + v**2
            else:
                d = d + v**2

    for (state,temp) in Q2.items():
        for (a,v) in temp.items():
            if not (state in Q1.keys()):
                d = d + v**2
            else:
                if not(a in Q1[state].keys()):
                    d = d + v**2
    return math.sqrt(d)

def discreteDistance(Q1,Q2):
    d = 0
    for (state,actionDict) in Q1.items():
            if state in Q2.keys():
                m1 = max([(v,a) for (a,v) in Q1[state].items()])[1]
                m2 = max([(v,a) for (a,v) in Q2[state].items()])[1]
                if m2 != m1:
                    d = d + 1 
            else:
                d = d + 1
    for (state,actionDict) in Q2.items():
        if not(state in Q1.keys()):
            d = d + 1
    return d

def distanceMatrix(listQmap,distance):
    matrixDistance=[]
    for Q in listQmap:
        distances = []
        for Q2 in listQmap:
            distances.append(distance(Q,Q2))
        matrixDistance.append(distances)
    return matrixDistance
