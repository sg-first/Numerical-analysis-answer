x=[0.4,0.6,0.8,1]
y=[25,23,20,21]

def calu(x,y,startPos=1):
    result=[]
    for i in range(startPos,len(y)):
        r=(y[i-1]-y[i])/(x[i-startPos]-x[i])
        result.append(r)
    while len(result)!=len(y):
        result=[None]+result
    return result

def getFun(xList,coeList):
    def f(x):
        result=0
        for i in range(len(coeList)):
            val=coeList[i]
            for j in range(i):
                val*=(x-xList[j])
            result+=val
        return result
    return f

y1=calu(x,y)
y2=calu(x,y1,2)
y3=calu(x,y2,3)
print(y1)
print(y2)
print(y3)

f=getFun(x,[y[0],y1[1],y2[2],y3[3]])
print(f(0.7))
