#Plot the time to create a group
import matplotlib.pyplot as plt
from curves import *
import statistics as stat
def plotFirstTimeInGroup(infos,firstTimeInGroup):
 
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

    x,y,w = smoothCurve(firstTimeInGroup)
    plt.plot([t/1000 for t in x],y,'k^')
    plt.xlabel('Time in thousands of cycles')
    plt.ylabel('Time to create the first group')
    plt.title('Time for group creation.') 
    plt.xlim(0,(runDuration+10)/(1000*cycleLength))
    plt.ylim(0,cycleLength)
    plt.tight_layout()
    print('Average is {0:.1f} steps, median is {1:.1f} steps and std is {2:.1f}.'.format(stat.mean(firstTimeInGroup),stat.median(firstTimeInGroup),stat.pstdev(firstTimeInGroup)))
    print('Each point is an average over '+str(w)+' cycles.')
    plt.show()
    return
