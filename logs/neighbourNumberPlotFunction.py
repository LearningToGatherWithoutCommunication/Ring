# Plot the minimum and maximum number of neighbours. 
import matplotlib.pyplot as plt

from curves import *
def plotNumberOfNeighbour(infos,minNumberOfNeighbour,maxNumberOfNeighbour):
 
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

    plt.plot(smoothCurve(minNumberOfNeighbour))
    plt.plot(smoothCurve(maxNumberOfNeighbour))
    plt.plot(smoothCurve([minSizeOfGroup for i in range(100)]))
    plt.xlabel('Time in fractions of learning phase')
    plt.ylabel('Maximum and minimum number of neighbors among agents')
    plt.title('Existence of group during learning phase')
    plt.show()
    return
