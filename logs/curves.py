#Computes a smoothed curve by averaging subsets of length windowsSize of the curve given. 

import math

def smoothCurve(curve,windowsSize = -1):
    #If no paramater given, reduce the curve to 1000 points
    if windowsSize == -1:
        windowsSize = math.ceil(len(curve) /1000)
    if curve == []:
        return []
    res=[]
    for j in range(math.ceil(len(curve)/windowsSize)):
        res.append(0)
        k = 0
        for i in range(windowsSize):
            if i+j*windowsSize < len(curve): 
                k = k + 1
                res[j] = res[j] + curve[i+j * windowsSize]
            else :
                break
        if k==0:
            res[j] = 0
        else:
            res[j] =res[j] / k
    return res
