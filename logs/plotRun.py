#Displays plots of desired data. Default displayed data is position, time to form group and number of neighbours.
from loadLogs import *
from positionPlotFunction import *
from computableMetrics import *
from firstTimeInGroupPlotFunction import *
from neighbourNumberPlotFunction import *
from sys import argv
from boxplot import *
#Specifiying default path to the data to plot. 
defaultPath = ''

if len(argv) > 1:
    script = argv[0]
    logsFileNameList = argv[1:len(argv)]
    print(logsFileNameList)
    print(len(argv))

elif defaultPath != '':
    logsFileNameList = [defaultPath]

else:
    print("missing one argument, Usage : 'python3 plotRun.py fileToPlotName'")
    logsFileNameList = []

for logsFileName in logsFileNameList:
    infos,sumSquaredDistanceHist,firstTimeInGroupHist,maxNumberOfNeighbour,minNumberOfNeighbour,posHistoryA,posHistoryL = load(logsFileName)

    plotFirstTimeInGroup(infos,firstTimeInGroupHist)

    plotNumberOfNeighbour(infos,minNumberOfNeighbour,maxNumberOfNeighbour)
   
    plotPos(infos,posHistoryA,posHistoryL)
    
#    plotMetrics(infos,posHistoryA,posHistoryL)

