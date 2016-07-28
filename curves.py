import math

def smoothCurve(curve,windowsSize = -1):
#If no paramater given, reduce the curve to 1000 points
    if windowsSize == -1:
        windowsSize = math.ceil(len(curve) /1000)
    if curve == []:
        return []
    y = []
    x = []
    for j in range(math.ceil(len(curve)/windowsSize)):
        x.append(j * windowsSize)
        y.append(0)
        k = 0
        for i in range(windowsSize):
            if i+j*windowsSize < len(curve): 
                k = k + 1
                y[j] += curve[i+j * windowsSize]
            else :
                break
        if k==0:
            y[j] = 0
        else:
            y[j] =y[j] / k
    return x,y,windowsSize
