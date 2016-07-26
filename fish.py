################################################
#                 Dependencies                 #
################################################

import math
import random
from operator import itemgetter
#To date the end of the learning phase
import time
#To write logs
import pickle 

################################################
#                 Useful values                #
################################################
#Initialize random seed for random number generator
random.seed()

#number of representants for fishes in sectors
numberOfRepresentant = 10

#Initialize id for fishes
fishId = 0


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

#Global ID generator
def newID():
    global fishId
    newId=fishId
    fishId = fishId + 1
    return newId

#Defining the different relative sectors and returns a vector where each positionhas a corresponding sector.
def sectorInit(self) :

#limits of sectors :
    lim1 = self.criticalSize + 1 #strict limit, lim1 in the first index to be outside sector 1
    lim2 = 3 * self.criticalSize + 1 + math.ceil((self.ringSize - 13)/5)
    lim3 = 5 * self.criticalSize + 1 + math.ceil((self.ringSize - 13)/3)
    limInf = math.ceil(self.ringSize/2) + 1  

    sectors = ['far' for i in range(self.ringSize)] #by default a position is in 'far' sector

#Checking that the limits are not larger than the ring
    if lim1 > limInf :
        lim1 = limInf
    if lim2 > limInf :
        lim2 = limInf
    if lim3 > limInf :
        lim3 = limInf

#Assigning the correct sector to each position, starting by the farther sectors
    for i in range(lim2, lim3):
        sectors[i]='farLeft'
        sectors[-i]='farRight'
    for i in range(lim1 ,lim2):
        sectors[i]='nearLeft'
        sectors[-i]='nearRight'
    for i in range(lim1):
        sectors[i] = 'central'
        sectors[-i] = 'central'
    
    return sectors

#Returns a dict indexed by the names of the sectors and containing positions corresponding to the key sector as a value
def sectorInit2(self):
    sectors = {}

#Sizes of sectors :
    centralSectorSize = self.criticalSize * 2 + 1
    sectorsProportions = [0.16,0.21,0.26]
    [nearSectorSize,farSectorSize,unknownSectorSize] = probaistributionToDiscreteDistribution(sectorsDistribution,self.ringSize - centralSectorSize)
    sectors['central'] = []
    sectors['nearLeft'] = []
    sectors['nearRight'] = []
    sectors['farLeft'] = []
    sectors['farRight'] = []
    sectors['unknown'] = []
    i = - math.floor(centralSectorSize/2)
    for j in range(centralSectorSize):
        sectors['central'].append(i % self.ringSize)
        i += 1
    for j in range(nearSectorSize):
        sectors['nearLeft'].append(i)
        i += 1
    for j in range(farSectorSize):
        sectors['farLeft'].append(i)
        i += 1
    for j in range(unknownSectorSize):
        sectors['unknown'].append(i)
        i += 1
    for j in range(farSectorSize):
        sectors['farRight'].append(i)
        i += 1
    for j in range(nearSectorSize):
        sectors['nearRight'].append(i)
        i += 1
    print(sectors)
    return sectors

#Returns the sector in which is a fish relatively to the agent.
def getSector(self,fish):
    relativePos = (fish.pos - self.pos) % self.ringSize
    return self.sectors[relativePos]

def getSector2(self,fish):
    relativePos = (fish.pos - self.pos) % self.ringSize
    for sector,sectorPos in self.sectors.items():
        if relativePos in sectorPos:
            return sector

#Return the state of the environment as the agent sees it.
def getState(self):
    fishDistribution = [0 for i in self.sectorList]
    state = [0 for i in self.sectorList]
    popSize = len(self.vision)

#Ccounting the fishes and storing their position
    for fish in self.vision:
        fishSector = getSector(self,fish)
        fishDistribution[self.sectorList.index(fishSector)] += 1
    state = probaDistributionToDiscreteDistribution([i/popSize for i in fishDistribution],numberOfRepresentant)

    if sum(state) >  numberOfRepresentant:
        print('Error in selection of representants')
    return tuple(state)

#Function that given a stat returns the action to do.
def policy(self): 
    s = self.currentState
    r = random.random()

# taking one action at random to explore
    if r < self.exploreRate :
        self.nextAction = random.choice([k for k in self.actions.keys()])

# chosing the action that maximizes the reward.
    else :
# nothing is known about this state, initializing it at 0.
        if not (s in self.Q.keys()):  
            #self.Q[s] = {action : 0 for action in self.actions.keys()}
            self.nextAction = random.choice([a for a in self.actions.keys()])
            return

#Computing highest value action

        maxVal,maxAction = max((value,key) for key,value in self.Q[s].items())
        minVal,minAction = min((value,key) for key,value in self.Q[s].items())

        possibleActions = [key for key in self.Q[s].keys()]

#all known actions are equivalent, choosing randomly
        if maxVal == minVal:
            self.nextAction = random.choice(possibleActions)
        else :
            self.nextAction = maxAction

def updateLearning(self,date):

#Updating the state
    #The agent is not yet initialized
    if self.currentState == None:
        self.currentState = self.getState(self)
        return 
    self.lastState = self.currentState
    self.currentState = self.getState(self)
    self.posHistory.append(self.pos)
    self.timeSinceReward = self.timeSinceReward + 1

#Updating eligibility trace. 
#Storing an eligibility value in a dict to prevent eligibility trace to get too long. Each value is sum(lambda^-k) where k is the time at which the state was visited. When clearing it, multiplying by lambda^n give the correct value to it, making fresher action more rewarded and older ones more discounted.
    oldEligibility = self.eligibilityTrace.get(self.lastState,{}).get(self.lastAction,0)
    newEligibility = oldEligibility + self.discountFactor ** (-self.timeSinceReward)
    if self.lastState in self.eligibilityTrace.keys():
        self.eligibilityTrace[self.lastState][self.lastAction] = newEligibility 
    else :
        self.eligibilityTrace[self.lastState] = {self.lastAction : newEligibility}

#Updating learning parameters
    if self.exploreRateMutable:
        self.exploreRate = self.alpha / (self.alpha + self.age)
    if self.learningRateMutable:
        self.learningRate = self.alpha  / (2*self.alpha + 3*self.age)

    self.age = self.age + 1
    reward = self.rewards(self)
    self.lastReward = reward
    
#Updating Q
    if reward == 0 or self.learningRate == 0:
        return
    else:
        expectedCumulativeReward = 0

        #unloading eligibility trace
        for state,vTemp in self.eligibilityTrace.items():

            for action,value in vTemp.items():

                oldQValue = self.Q.get(state,{}).get(action,0)
                eligibility = value * (self.discountFactor) ** (self.timeSinceReward)
                newQValue = (1-self.learningRate * eligibility) * oldQValue + self.learningRate * eligibility * (reward + self.discountFactor * expectedCumulativeReward)
                #initializing unknown states
                if not (state in self.Q.keys()):
                    self.Q[state] = {action : 0 for action in self.actions.keys()}
                #updating Q
                self.Q[state][action] = newQValue

        #reseting eligibility trace
        self.eligibilityTrace.clear()
        self.timeSinceReward = 0

#Define the reward associated to each state
def rewards(penalty = -2, reward = 10, minSizeOfGroup = 3):
    def rewardFunction(self):
        state = self.currentState
        central = state[self.sectorList.index('central')]
        near = state[self.sectorList.index('nearLeft')] + state[self.sectorList.index('nearRight')]
        far = state[self.sectorList.index('farLeft')] + state[self.sectorList.index('farRight')]
        unknown = state[self.sectorList.index('far')]
        if central >= minSizeOfGroup: 
            return reward
        elif central < 2:
            return penalty
        else :
            return 0
    return rewardFunction

class Fish:
#Initialization
    def __init__(self,
                idFish,
                ringSize,
                rewards = rewards,
                vision=[],
                previousKnowledge = {},
                pos = 0,
                learningRate = 1,
                exploreRate = 1,
                criticalSize = 1,
                alpha = 1,
                getState = getState,
                policy = policy,
                update = updateLearning,
                ):

        self.idFish = idFish
        self.ringSize = ringSize
        self.criticalSize = criticalSize
        self.Q = previousKnowledge.copy()
        self.pos = pos
        self.vision = vision
        self.learningRate = learningRate
        self.exploreRate = exploreRate
        self.alpha = alpha
        self.discountFactor = 0.95
        self.speed = 1 
        self.rewards = rewards
        self.age = 0
        self.lastAction = None
        self.nextAction = None
        self.lastState = None
        self.currentState = None
        self.lastReward = 0
        self.getState = getState
        self.sectors = sectorInit(self)
        self.sectorList = [] 
        self.numberOfRepresentant = numberOfRepresentant
        
#Defining the format of state representation, here its the sectors in order i for increasing positions on the ring
        for j in self.sectors:
            if not j in self.sectorList:
                self.sectorList.append(j)

        self.policy = policy
        self.update = update
        self.states = []
        self.eligibilityTrace = {}
        self.posHistory = []
        self.timeSinceReward = 0
        self.exploreRateMutable = True
        self.learningRateMutable = True
        self.joinGroupDate = 0 
        self.timeInGroup = 0

        def goLeft(self):
            self.pos = (self.pos + self.speed)% self.ringSize
            return

        def goRight(self):
            self.pos = (self.pos - self.speed)% self.ringSize
            return

        def dontMove(self):
            return

        self.actions={'left' : goLeft,'right' : goRight, 'dontMove' : dontMove}

    def distance(self,fish):
        return min((self.pos - fish. pos) % self.ringSize ,(fish.pos - self. pos) % self.ringSize)

    def act(self) :
        self.lastAction = self.nextAction
        self.actions[self.nextAction](self)
        self.nextAction = None

    def genLogs(self,path):
        title = 'Fish'+ str(self.idFish)
        logFile = open(path + title +'.log','wb')
        infos = '' 
        infos = infos + 'age:' + str(self.age) + '\n'
        pickle.dump(infos,logFile,2)
        pickle.dump(self.Q,logFile,2)
        pickle.dump(self.posHistory,logFile,2)
        logFile.close()
        return

    def __str__(self):
        return str(self.pos)

    def __repr__(self):
        return str(self.idFish)

    def __eq__(self,fish):
        return self.idFish == fish.idFish

    def __ne__(self,fish):
        return self.idFish != fish.idFish

    def __lt__(self,fish):
        return self.idFish < fish.idFish
