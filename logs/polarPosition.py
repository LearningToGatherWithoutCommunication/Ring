#Plot trajectories of the agent in different ways.
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter
from curves import *

def plotPolarPos(infos,posHistoryA,posHistoryL):
 
    [
            runDuration,
            popSize,
            ringSize,
            decreasePoint,
            decreaseValue,
            learnersNumber,
            adultsNumber,
            reward,
            penalty,
            minSizeOfGroup,
            minimumDistanceToBeInGroup,
            pointToStopExploration,
            cycleLength
            ] = infos

    #From a number vector a_i gives the vector b were b_i is the rank of a_i in a in decreasing order
    def rankDecreasing(valueList):
        indexList = [(valueList[i],i) for i in range(len(valueList))]
        indexList.sort(key = itemgetter(1), reverse = True)
        return [b for (a,b) in indexList]

    def probaDistributionToDiscreteDistribution(probaDist,numberOfRepresentant):
        totalSum = sum (probaDist)
        discreteDistribution = [math.floor(i /totalSum * numberOfRepresentant) for i in probaDist]
        decimalPart = [probaDist[i] - discreteDistribution[i] for i in range(len(probaDist))]
        rankDecimal = rankDecreasing(decimalPart) 
        remainingRepresentant = numberOfRepresentant - sum(discreteDistribution)
        for i in range(remainingRepresentant):
            discreteDistribution[rankDecimal[i]] += 1
        return discreteDistribution
    #Polar transformation of a list. Takes a list of positions x and returns t*exp(2i*pi*x).
    #MaxVal is to compute the phase : phi = value/maxVal where value is an element of the list and maxVal is the larger element. val is to increase a bit the radius (less than 1) in order to separate points at equal time but from different sources
    def toPolar(list,maxVal,val):
        res=[]
        for (t,i) in enumerate(list):
            r = t + 1 + val
            x = r * math.cos(i/maxVal * 2 * math.pi)
            y = r * math.sin(i/maxVal * 2 * math.pi)
            res.append((x,y))
        return res
    #compute the barycenter of on a ring
    def barycenter(list,ringSize):
        p1 = [ i for i in list if i < ringSize/2]
        p2 = [ i for i in list if i > ringSize/2]
        if p1 !=[]:
            b1,w1 = sum(p1) / len(p1),len(p1)
        else :
            b1,w1 = 0,0
        if p2 != []:
            b2,w2 = sum(p2) / len(p2),len(p2)
        else :
            b2,w2 = 0,0
        tempBar1 = (b1 * w1 + b2 * w2) / (2 * len(list))
        tempBar2 = (b1 * w1 + (ringSize - b2) * w1) / (2 *len(list))
        if w1 > 0:
            d1 = min((tempBar1 - b1) % ringSize,(b1 - tempBar1) % ringSize)
            d2 = min((tempBar2 - b1) % ringSize,(b1 - tempBar2) % ringSize)
            if d1 < d2:
                return tempBar1
            else :
                return tempBar2
        else :
            d1 = min((tempBar1 - b2) % ringSize,(b2 - tempBar1) % ringSize)
            d2 = min((tempBar2 - b2) % ringSize,(b2 - tempBar2) % ringSize)
            if d1 < d2:
                return tempBar1
            else :
                return tempBar2

    def densityToColor(d):
        if d >= 8:
            return 'k'
        elif d >= 1:
            return 'white'
        else:
            return 'm'

    def densityToSize(d):
        if d >= 1:
            return d**2+3
        elif d > 0:
            return 20 
        else:
            return 0

    maxPlot = min(runDuration, int(cycleLength) * 1 )
    colors = [i for i in 'bgrcmyk']
    #Polar transformation in order to keep the ring topology : position is phase and time is radius
    polarPlot = False
    #Classic trajectories, centered around barycenter
    classicPlot = False
    #Density of agents at each position.
    densityPlot = True
    #Raw trajectories, often crossing the figures due to ring topology (n->0 is almost vertical)
    rawPlot = False

#Plotting at different points of the position history
########################################################################
#                            StartPlot                                 #
########################################################################

    plotRangeMin = 0
    plotRangeMax = maxPlot - 1
    if polarPlot:
        for f in range(adultsNumber):
            pos = (posHistoryL[f][plotRangeMin : plotRangeMax ])
            polar = toPolar(pos,ringSize,f/20)
            x = np.array([a for (a,b) in polar])
            y = np.array([b for (a,b) in polar])
            color = colors[f%len(colors)]
            plt.scatter(x,y, c = color, cmap=plt.cm.gist_earth)
        for f in range(learnersNumber):
            pos = (posHistoryL[f][plotRangeMin : plotRangeMax ])
            polar = toPolar(pos,ringSize,f/20)
            x = np.array([a for (a,b) in polar])
            y = np.array([b for (a,b) in polar])
            color = colors[f%len(colors)]
            plt.scatter(x,y, c = color, cmap=plt.cm.gist_earth)

        for i in range(len(x)):
            circle=plt.Circle((0,0),i+2,fill = False)
            plt.gcf().gca().add_artist(circle) 
    
        plt.title('Position of agents for the '+str(maxPlot)+' first steps in polar transformation.')
        plt.show()
    if classicPlot:
        bar=[]
        bar = [barycenter([posHistoryL[f][i] for f in range(learnersNumber)],ringSize) for i in range(plotRangeMin,plotRangeMax)]

        for f in range(learnersNumber):
            pos = (posHistoryL[f][plotRangeMin : plotRangeMax ])
            plt.plot([(x-bar[t]+ringSize/2) % ringSize for t,x in enumerate(pos)])

        plt.xlabel('Time in iterations')
        plt.ylabel('Position of the agents on the ring')
        plt.title('Position of agents for the '+str(maxPlot)+' first steps')
        plt.show()

    if densityPlot:
        state = [[0 for i in range(ringSize)] for i in range(plotRangeMin,plotRangeMax)]
        for t in range(plotRangeMin,plotRangeMax):
            for f in range(learnersNumber):
                y = posHistoryL[f][t]
                state[t-plotRangeMin][y] += 1
            for f in range(adultsNumber):
                y = posHistoryA[f][t]
                state[t-plotRangeMin][y] += 1
            stateNormalized = probaDistributionToDiscreteDistribution(state[t-plotRangeMin],10)
            neighbour = [[stateNormalized[y-2] + stateNormalized[y-1] + stateNormalized[y] if stateNormalized[y-1]>0 else 0  for y in range(ringSize)] for t in range(plotRangeMax-plotRangeMin)]
            size = [densityToSize(d) for d in neighbour[t-plotRangeMin]]
            color = [densityToColor(d) for d in neighbour[t-plotRangeMin]]
            y = [y for y,d in enumerate(neighbour[t-plotRangeMin])]
            x = [t -plotRangeMin for i in range(ringSize)]
            plt.scatter(x,y,s = size,c=color)
        plt.xlabel('Time in iterations')
        plt.ylabel('Position on the ring')
        plt.title('Number of neighbors for each position for the '+str(maxPlot)+' first steps.')
        plt.show()

    if rawPlot:
        for f in range(adultsNumber):
            plt.plot(posHistoryA[f][plotRangeMin : plotRangeMax ])
        for f in range(learnersNumber):
            plt.plot(posHistoryL[f][plotRangeMin : plotRangeMax ])
        plt.xlabel('Time in iterations')
        plt.ylabel('Position of the agents on the ring')
        plt.title('Position of agents for the '+str(maxPlot)+' first steps')
        plt.show()

########################################################################
#                            MidPlot                                   #
########################################################################
    plotRangeMin = math.floor(runDuration/2) 
    plotRangeMax = math.floor(runDuration/2)+ maxPlot - 1

    if polarPlot:
        for f in range(adultsNumber):
            pos = (posHistoryL[f][plotRangeMin : plotRangeMax ])
            polar = toPolar(pos,ringSize,f/20)
            x = np.array([a for (a,b) in polar])
            y = np.array([b for (a,b) in polar])
            color = colors[f%len(colors)]
            plt.scatter(x,y, c = color, cmap=plt.cm.gist_earth)
        for f in range(learnersNumber):
            pos = (posHistoryL[f][plotRangeMin : plotRangeMax ])
            polar = toPolar(pos,ringSize,f/20)
            x = np.array([a for (a,b) in polar])
            y = np.array([b for (a,b) in polar])
            color = colors[f%len(colors)]
            plt.scatter(x,y, c = color, cmap=plt.cm.gist_earth)

        for i in range(len(x)):
            circle=plt.Circle((0,0),i+2,fill = False)
            plt.gcf().gca().add_artist(circle) 
    
        plt.title('Position of agents for '+str(maxPlot)+' intermediate steps in polar transformation.')
        plt.show()

    if classicPlot:
        bar=[]
        bar = [barycenter([posHistoryL[f][i] for f in range(learnersNumber)],ringSize) for i in range(plotRangeMin,plotRangeMax)]

        for f in range(learnersNumber):
            pos = (posHistoryL[f][plotRangeMin : plotRangeMax ])
            plt.plot([(x-bar[t]+ringSize/2) % ringSize for t,x in enumerate(pos)])

        plt.xlabel('Time in iterations')
        plt.ylabel('Position of the agents on the ring')
        plt.title('Position of agents for the '+str(maxPlot)+' intermediate steps')
        plt.show()

    if densityPlot:
        state = [[0 for i in range(ringSize)] for i in range(plotRangeMin,plotRangeMax)]
        for t in range(plotRangeMin,plotRangeMax):
            for f in range(learnersNumber):
                y = posHistoryL[f][t]
                state[t-plotRangeMin][y] += 1
            for f in range(adultsNumber):
                y = posHistoryA[f][t]
                state[t-plotRangeMin][y] += 1
            stateNormalized = probaDistributionToDiscreteDistribution(state[t-plotRangeMin],10)
            neighbour = [[stateNormalized[y-2] + stateNormalized[y-1] + stateNormalized[y] if stateNormalized[y-1]>0 else 0  for y in range(ringSize)] for t in range(plotRangeMax-plotRangeMin)]
            size = [densityToSize(d) for d in neighbour[t-plotRangeMin]]
            color = [densityToColor(d) for d in neighbour[t-plotRangeMin]]
            y = [y for y,d in enumerate(neighbour[t-plotRangeMin])]
            x = [t-plotRangeMin  for i in range(ringSize)]
            plt.scatter(x,y,s = size,c=color)
        
        plt.xlabel('Time in iterations')
        plt.ylabel('Position on the ring')
        plt.title('Number of neighbors for each position for '+str(maxPlot)+' intermediate steps.')
        plt.show()

    if rawPlot:
        for f in range(adultsNumber):
            plt.plot(posHistoryA[f][plotRangeMin : plotRangeMax ])
        for f in range(learnersNumber):
            plt.plot(posHistoryL[f][plotRangeMin : plotRangeMax ])
        plt.xlabel('Time in iterations')
        plt.ylabel('Position of the agents on the ring')
        plt.title('Position of agents for the '+str(maxPlot)+' first steps')
        plt.show()

########################################################################
#                           EndPlot                                    #
########################################################################
    plotRangeMin = runDuration - maxPlot 
    plotRangeMax = runDuration - 1

    if polarPlot:
        for f in range(adultsNumber):
            pos = (posHistoryL[f][plotRangeMin : plotRangeMax ])
            polar = toPolar(pos,ringSize,f/20)
            x = np.array([a for (a,b) in polar])
            y = np.array([b for (a,b) in polar])
            color = colors[f%len(colors)]
            plt.scatter(x,y, c = color, cmap=plt.cm.gist_earth)
        for f in range(learnersNumber):
            pos = (posHistoryL[f][plotRangeMin : plotRangeMax ])
            polar = toPolar(pos,ringSize,f/20)
            x = np.array([a for (a,b) in polar])
            y = np.array([b for (a,b) in polar])
            color = colors[f%len(colors)]
            plt.scatter(x,y, c = color, cmap=plt.cm.gist_earth)

        for i in range(len(x)):
            circle=plt.Circle((0,0),i+2,fill = False)
            plt.gcf().gca().add_artist(circle) 
    
        plt.title('Position of agents for the '+str(maxPlot)+' last steps in polar transformation.')
        plt.show()

    if classicPlot:
        bar=[]
        bar = [barycenter([posHistoryL[f][i] for f in range(learnersNumber)],ringSize) for i in range(plotRangeMin,plotRangeMax)]
        for f in range(learnersNumber):
            pos = (posHistoryL[f][plotRangeMin : plotRangeMax ])
            plt.plot([(x-bar[t]+ringSize/2) % ringSize for t,x in enumerate(pos)])

        plt.xlabel('Time in iterations')
        plt.ylabel('Position of the agents on the ring')
        plt.title('Position of agents for the '+str(maxPlot)+' last steps')
        plt.show()

    if densityPlot:
        state = [[0 for i in range(ringSize)] for i in range(plotRangeMin,plotRangeMax)]
        for t in range(plotRangeMin,plotRangeMax):
            for f in range(learnersNumber):
                y = posHistoryL[f][t]
                state[t-plotRangeMin][y] += 1
            for f in range(adultsNumber):
                y = posHistoryA[f][t]
                state[t-plotRangeMin][y] += 1
            stateNormalized = probaDistributionToDiscreteDistribution(state[t-plotRangeMin],10)
            neighbour = [[stateNormalized[y-2] + stateNormalized[y-1] + stateNormalized[y] for y in range(ringSize)] for t in range(plotRangeMax-plotRangeMin)]
            neighbour = [[stateNormalized[y-2] + stateNormalized[y-1] + stateNormalized[y] if stateNormalized[y-1]>0 else 0  for y in range(ringSize)] for t in range(plotRangeMax-plotRangeMin)]
            size = [densityToSize(d) for d in neighbour[t-plotRangeMin]]
            color = [densityToColor(d) for d in neighbour[t-plotRangeMin]]
            y = [y for y,d in enumerate(neighbour[t-plotRangeMin])]
            x = [t-plotRangeMin for i in range(ringSize)]
            plt.scatter(x,y,s = size,c=color)
        plt.xlabel('Time in iterations')
        plt.ylabel('Position on the ring')
        plt.title('Number of neighbors for each position for the '+str(maxPlot)+' last steps.')
        plt.show()

    if rawPlot:
        for f in range(adultsNumber):
            plt.plot(posHistoryA[f][plotRangeMin : plotRangeMax ])
        for f in range(learnersNumber):
            plt.plot(posHistoryL[f][plotRangeMin : plotRangeMax ])
        plt.xlabel('Time in iterations')
        plt.ylabel('Position of the agents on the ring')
        plt.title('Position of agents for the '+str(maxPlot)+' last steps')
        plt.show()

    return
