# Plot the minimum and maximum number of neighbours. 
import matplotlib.pyplot as plt
import statistics as stat
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

    x,y,w = smoothCurve([minSizeOfGroup for i in range(runDuration)])
    plt.plot([t/(1000*cycleLength) for t in x],[10 * n for n in y],'r--')

    x,y,w = smoothCurve(minNumberOfNeighbour)
    data = [10*n for n in y]
    print('Average is {0:.1f}\%, median is {1:.1f}\% and std is {2:.1f}\% for min neighbor.'.format(stat.mean(data),stat.median(data),stat.pstdev(data)))
    plt.plot([t/(1000*cycleLength) for t in x],[10 * n for n in y],'w^')

    x,y,w = smoothCurve(maxNumberOfNeighbour)
    data = [10*n for n in y]
    print('Average is {0:.1f}\%, median is {1:.1f}\% and std is {2:.1f}\% for max neighbor.'.format(stat.mean(data),stat.median(data),stat.pstdev(data)))
    plt.plot([t/(1000*cycleLength) for t in x],[10 * n for n in y],'ks')

    plt.xlabel('Time in thousands of cycles')
    plt.ylabel('Maximum and minimum number of neighbors among agents')
    plt.title('Existence of group.')
    plt.xlim(0,(runDuration+10)/(1000*cycleLength))
    plt.ylim(0,100)
    plt.tight_layout()
    print('Each point is an average over '+str(w)+' iterations.')
    plt.show()
    return
