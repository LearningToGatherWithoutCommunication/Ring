#Plot the time to create a group
import matplotlib.pyplot as plt
from curves import *
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

    plt.plot(smoothCurve(firstTimeInGroup))
    plt.xlabel('Time in fractions of learning phase')
    plt.ylabel('Time for the first group to be created')
    plt.title('Time for group creation during the learning phase')
    plt.show()
    return
