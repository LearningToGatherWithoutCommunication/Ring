################################################
#                 Dependencies                 #
################################################
#import fish class
from fish import *
#to copy Qmaps
import copy
import math
#To date the end of the learning phase
import time
#To write logs
import pickle
#To readQmaps and compare them
from QmapFunctions import *

from sys import argv
import os
import shutil

################################################
#                 Parameters                   #
################################################
if len(argv) > 1:
    script, pathToConf = argv
else:
    [script] = argv
    pathToConf = 'parameters.conf'
try:
#opening and parsing conf file
    paramFile = open(pathToConf,'r')
    paramLines = paramFile.readlines()
    paramFile.close()
    param = {i.split('=')[0].replace(' ','') : i.split('=')[1].replace(' ','').replace('\n','') 
            for i in paramLines if ((i[0] !='#') and (i[0] != '\n'))}
    learnersNumber = int(param['learnersNumber'])
    adultsNumber = int(param['adultsNumber'])
    popSize = learnersNumber + adultsNumber
    ringSize = int(param['ringSize'])
    #At the begining of a cycle, positions are reset
    cycleLengthInRingSize = int(param['cycleLengthInRingSize'])

    runDurationInCycles = int(param['runDurationInCycles'])
    #reward for being in the group
    reward = int(param['reward'])

    #penalty for begin alone in the central sector
    penalty = int(param['penalty'])

    #Minimum number of individuals in the group
    minSizeOfGroup = int(param['minSizeOfGroup'])

    minimumDistanceToBeInGroup = int(param['minimumDistanceToBeInGroup'])

    # Setting the parameters for explore rate evolution in alpha / (alpha + n). 
    # Fraction of the run at which exploreRate is decreaseValue
    fixedLearning = bool(param['fixedLearning'])
    fixedExploration = bool(param['fixedExploration'])
    learningRate = float(param['learningRate'])
    exploreRate = float(param['exploreRate'])
    decreasePoint = float(param['decreasePoint'])
    decreaseValue = float(param['decreaseValue'])


    # Fraction of the simulation at which there is no longer exploration and behaviour is tested.
    pointToStopExploration = float(param['pointToStopExploration'])
    pathToLogs = param['pathToLogs'].replace("'",'')
    pathToQMapsList = param['pathToQMapsList'].replace("'",'')
except (ValueError,KeyError): 
    print('No parameters file, using default parameters')
    learnersNumber = 10
    adultsNumber = 0 
    popSize = learnersNumber + adultsNumber
    ringSize = 13 
    #Duration of a cycle in ringSize. At the begining of a cycle, positions are reset. 
    cycleLengthInRingSize = 5 
    #Duration of the run in cycleLength
    runDurationInCycles = 25

    #reward for being in the group
    reward = 100

    #penalty for begin alone in the central sector
    penalty = -5 

    #Minimum number of individuals in the group
    minSizeOfGroup = math.floor(10 * 0.8)

    minimumDistanceToBeInGroup = 1

    # Setting the parameters for explore rate evolution in alpha / (alpha + n). 
    # Fraction of the run at which exploreRate is decreaseValue
    decreasePoint = 0.5 
    decreaseValue = 0.5 
    fixedLearning = True 
    fixedExploration = True
    learningRate = 0.1
    exploreRate = 0.1

    # Fraction of the simulation at which there is no longer exploration and behaviour is tested.
    pointToStopExploration = 0.9
    #Path where to write the logs
    pathToLogs = 'logs/' 
    pathToQMapsList = 'logs/QMaps/' 

################################################
#                 Useful values                #
################################################
cycleLength =  cycleLengthInRingSize * ringSize
runDuration = runDurationInCycles * cycleLength
stepToStopExploration = pointToStopExploration * runDuration
alpha = decreaseValue * runDuration * decreasePoint / (1 - decreaseValue)

#Reset position of the fishes and the cycle informations
def reset(pop,date,cycleLength):
    random.shuffle(pop)
    for f in pop:
        f.eligibility = {}
        f.timeSinceReward = 0
        f.lastState = None
        f.joinGroupDate = cycleLength
        f.timeInGroup = 0
        #f.pos = (pop.index(f) * math.ceil(f.ringSize / len(pop)) + round(2*random.random()-1) ) % f.ringSize
        f.pos = random.randint(0,ringSize-1)
        f.currentState = f.getState(f)
    return

#Load Qmap from a fish file
def getKnowledgeFromFish(FishName):
    fish = open(FishName,'rb')
    infos = pickle.load(fish)
    Q = pickle.load(fish)
    posHistory = pickle.load(fish)
    fish.close()
    return Q

#From a number vector a_i gives the vector b were b_i is the rank of a_i in a in decreasing order
def rankDecreasing(valueList):
    indexList = [(valueList[i],i) for i in range(len(valueList))]
    indexList.sort(key = itemgetter(1), reverse = True)
    return [b for (a,b) in indexList]

def probaDistributionToDiscreteDistribution(probaDist,numberOfRepresentant):
    discreteDistribution = [math.floor(i * numberOfRepresentant) for i in probaDist]
    decimalPart = [probaDist[i] - discreteDistribution[i] for i in range(len(probaDist))]
    rankDecimal = rankDecreasing(decimalPart) 
    remainingRepresentant = numberOfRepresentant - sum(discreteDistribution)
    for i in range(remainingRepresentant):
        discreteDistribution[rankDecimal[i]] += 1
    return discreteDistribution

################################################
#            Variables Initialization          #
################################################

pop = []
adults = []
learners = []

#metrics
sumSquaredDistanceHist = []
maxNumberOfNeighbourHist = []
minNumberOfNeighbourHist = []
firstTimeInGroupHist = []
firstTimeInGroup = cycleLength;

#Get a Qmap list from a list of fish files
try:
    fishNamesFile = open(pathToQMapsList+'QMaps','r')
    fishNamesList = fishNamesFile.read().split('\n')
    listQmap = [getKnowledgeFromFish(pathToQMapsList+fishName) for fishName in fishNamesList if fishName != '']
except FileNotFoundError:
    if (adultsNumber > 0):
        print('No adults found')
    listQmap = [{}]

#Initializing adults
for i in range(adultsNumber):
    adults.append(Fish(idFish = newID(),
                       ringSize = ringSize,
                       rewards = rewards(penalty,reward,minSizeOfGroup = minSizeOfGroup),
                       alpha = alpha,
                       criticalSize = minimumDistanceToBeInGroup,
                       ))

#Initializing learners 
for i in range(learnersNumber):
    learners.append(Fish(idFish = newID(),
                        ringSize = ringSize,
                        rewards = rewards(penalty,reward, minSizeOfGroup = minSizeOfGroup),
                        alpha = alpha,
                        criticalSize = minimumDistanceToBeInGroup,
                        ))
pop = adults + learners

#Initializing position a vision (i.e. the other agents that are seen by the agent)
for f in pop :
    f.pos = (pop.index(f) * math.ceil(f.ringSize / len(pop)) + round(2*random.random()-1) ) % f.ringSize
    f.vision = pop
    if fixedLearning:
        f.learningRateMutable = False
        f.learningRate = learningRate
    if fixedLearning:
        f.exploreRateMutable = False
        f.exploreRate = exploreRate
#flagging variable learning rate with a specific value for initial learnig rate
if not fixedLearning:
    learningRate = 1

#Giving already filled Qmaps for adults
for f in adults:
    if len(listQmap) >= len(adults):
        f.Q = listQmap[adults.index(f)].copy()
    else:
        f.Q = random.choice(listQmap).copy()
    f.learningRateMutable = False
    f.learningRate = 0.0
    f.exploreRateMutable = False
    f.exploreRate = 0.0
#   f.policy = deterministicPolicy

################################################
#            Main Loop                         #
################################################

for t in range(runDuration):
    #Begining of a cycle.
    if t % cycleLength == 0 and t > 0:
        firstTimeInGroupHist.append(firstTimeInGroup)
        firstTimeInGroup = cycleLength;
        reset(pop,t,cycleLength)

    #Updating the state of the agents in the neww environment.
    for f in pop :
        f.update(f,t)

    #After a point the fishes are no longer exploring.
    if t > stepToStopExploration:
        f.exploreRateMutable = False
        f.learningRateMutable = False
        f.exploreRate = 0.1
        f.learningRate = 0

    #Deciding next action according to policy.
    for f in pop :
        f.policy(f)

    #Performing next action.
    for f in pop :
        f.act()

    #Computing Metrics
    fishPositionOnRing = [f.pos for f in pop]
    fishRepartitionOnRing = [0 for k in range(ringSize)]
    for j in fishPositionOnRing:
        fishRepartitionOnRing[j] += 1
    fishRepartitionOnRing = probaDistributionToDiscreteDistribution([i/popSize for i in fishRepartitionOnRing],pop[0].numberOfRepresentant)
    #sum of squared distances
    sumSquaredDistance = sum([sum([fishRepartitionOnRing[k] * fishRepartitionOnRing[j] * min((k-j)%ringSize,(j-k)%ringSize)**2 for k in range(ringSize) if fishRepartitionOnRing[k] > 0]) for j in range(ringSize) if fishRepartitionOnRing[j] > 0]) /2
    sumSquaredDistanceHist.append(sumSquaredDistanceHist)

    #Size of groups
    numberOfNeighbour = [fishRepartitionOnRing[i - 2] + fishRepartitionOnRing[i - 1] + fishRepartitionOnRing[i] if fishRepartitionOnRing[i-1] > 0  else 0 for i in range(ringSize)]
    maxNumberOfNeighbour = max(numberOfNeighbour)
    minNumberOfNeighbour = min([i for i in numberOfNeighbour if i > 0])
    maxNumberOfNeighbourHist.append(maxNumberOfNeighbour)
    minNumberOfNeighbourHist.append(minNumberOfNeighbour)

    #Time before the first group
    if (maxNumberOfNeighbour > minSizeOfGroup) and (t % cycleLength < firstTimeInGroup):
        firstTimeInGroup = t % cycleLength

################################################
#                 After Run process            #
################################################

print([len(f.Q) for f in adults])
print(distanceMatrix([f.Q for f in pop],discreteDistance))

#Computing the average number of rewards
#Generating file name and unique ID
date = time.time()
idFile = math.ceil((date - math.ceil(date))*1000000) % 1000
timeNow = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())


#Generating logs for the whole learning phase
#Creating folder to store files
pathToFile = pathToLogs + str(idFile) + '_D' + str(runDurationInCycles) + '_P' + str(popSize) + '_S'+ str(ringSize) + '_L' + str(learningRate) + '-' + timeNow+'/'
os.makedirs(pathToFile, exist_ok = True)
#Keeping a copy of source code that generated the logs
shutil.copyfile(script,pathToFile+script)
shutil.copyfile('fish.py',pathToFile+'fish.py')

logRun = open(pathToFile+'run.log','wb')

#Learning phase parameters stored
infos = 'runDuration:' + str(runDuration) + '\n'
infos = infos +'popSize:' + str(popSize) + '\n' 
infos = infos + 'ringSize:' + str(ringSize) + '\n' 
infos = infos + 'decreasePoint:' + str(decreasePoint) + '\n'
infos = infos + 'decreaseValue:' + str(decreaseValue) + '\n'
infos = infos + 'fixedLearning:' + str(fixedLearning) + '\n'
infos = infos + 'fixedExploration:' + str(fixedExploration) + '\n'
infos = infos + 'learningRate:' + str(learningRate) + '\n'
infos = infos + 'exploreRate:' + str(exploreRate) + '\n'
infos = infos + 'learnersNumber:' + str(learnersNumber) + '\n'
infos = infos + 'adultsNumber:' + str(adultsNumber) + '\n'
infos = infos + 'reward:' + str(reward) + '\n'
infos = infos + 'penalty:' + str(penalty) + '\n'
infos = infos + 'minSizeOfGroup:' + str(minSizeOfGroup) + '\n'
infos = infos + 'minimumDistanceToBeInGroup:' + str(minimumDistanceToBeInGroup) + '\n'
infos = infos + 'pointToStopExploration:' + str(pointToStopExploration) + '\n'
infos = infos + 'cycleLength:' + str(cycleLength) + '\n'

#Writing Data
pickle.dump(infos,logRun,2)
pickle.dump(sumSquaredDistanceHist,logRun,2)
pickle.dump(firstTimeInGroupHist,logRun,2)
pickle.dump(maxNumberOfNeighbourHist,logRun,2)
pickle.dump(minNumberOfNeighbourHist,logRun,2)


for f in adults:
    pickle.dump(f.posHistory,logRun,2)
for f in learners:
    pickle.dump(f.posHistory,logRun,2)

logRun.close()

#Generating fishes logs
for f in pop:
    f.genLogs(pathToFile)
