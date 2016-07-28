from loadLogs import *
from positionPlotFunction import *
from computableMetrics import *
from firstTimeInGroupPlotFunction import *
from neighbourNumberPlotFunction import *
from sys import argv
from boxplot import *
if len(argv) > 1:
    script, filename = argv
else:
    filename='logsLoc'

logsLocFile = open(filename)
logsFileNameList = logsLocFile.read().splitlines()
logsLocFile.close()
for logsFileName in logsFileNameList:
    infos,sumSquaredDistanceHist,firstTimeInGroupHist,maxNumberOfNeighbour,minNumberOfNeighbour,posHistoryA,posHistoryL = load(logsFileName)

    plotFirstTimeInGroup(infos,firstTimeInGroupHist)

    plotNumberOfNeighbour(infos,minNumberOfNeighbour,maxNumberOfNeighbour)
   
    plotPos(infos,posHistoryA,posHistoryL)
    
#    boxPlot(infos,firstTimeInGroupHist,minNumberOfNeighbour,maxNumberOfNeighbour)

#    plotMetrics(infos,posHistoryA,posHistoryL)

