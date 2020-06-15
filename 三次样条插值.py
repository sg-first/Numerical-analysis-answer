import numpy as np

def caluH(x):
    result=[]
    for i in range(1,len(x)):
        result.append(x[i]-x[i-1])
    return result

def caluL(H):
    result=[]
    for i in range(len(H)-1):
        val=H[i]/(H[i]+H[i+1])
        result.append(val)
    return result

def caluDiff(x, y, startPos=1):
    result=[]
    for i in range(startPos,len(y)):
        r=(y[i-1]-y[i])/(x[i-startPos]-x[i])
        result.append(r)
    while len(result)!=len(y):
        result=[None]+result
    return result

def caluG(h,y1):
    h=[0]+h+[0]
    result=[]
    for i in range(1,len(y1)):
        if not y1[i] is None:
            gi=(y1[i]-y1[i-1])/(h[i]+h[i-1])
            gi*=6
            result.append(gi)
        else:
            result.append(None)
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

def setEndPos(y1,y_1,y_2):
    y1[0] = y_1
    y1.append(y_2)
    return y1

def caluA(H):
    size=len(H)+1
    A=np.zeros((size,size))
    l=caluL(H)
    m=[1-i for i in l]
    A[0, 0] = 2
    A[0, 1] = 1
    A[size - 1, size - 2] = 1
    A[size - 1, size - 1] = 2

    startPos=0
    for i in range(1,size-1):
        A[i,startPos]=l[startPos]
        A[i,startPos+1]=2
        A[i,startPos+2]=m[startPos]
        startPos+=1
    '''
    A=[[2,1,0,0,0],
       [l[0],2,m[0],0,0],
       [0,l[1],2,m[1],0],
       [0,0,l[2],2,m[2]],
       [0,0,0,1,2]]
    '''
    return A

def genFunSeg(x,y,M,h,i):
    h=[0]+h
    hi=h[i]
    hi26=hi**2/6
    c1=M[i-1]/(6*hi)
    c2=M[i]/(6*hi)
    c3=y[i-1]-hi26*M[i-1]
    c3/=hi
    c4=y[i]-hi26*M[i]
    c4/=hi
    def fun(rx):
        return c1*(x[i]-rx)**3+c2*(rx-x[i-1])**3+ \
               c3*(x[i]-rx)+c4*(rx-x[i-1])
    return fun

def genFun(x,y,M,H):
    allFun=[]
    for i in range(1,len(x)):
        allFun.append(genFunSeg(x,y,M,H,i))

    def fun(rx):
        for i in range(1,len(x)):
            if rx>=x[i-1] and rx<x[i]:
                return allFun[i-1](rx)
        return 0

    return fun

def doFun(f,xList):
    yList=[]
    for i in xList:
        yList.append(f(i))
    return np.array(yList)

# 得到函数
def cubic(x,y):
    y_1 = 0
    y_2 = 0
    y1 = caluDiff(x, y)
    # 端点一阶导数值
    y1 = setEndPos(y1, y_1, y_2)
    # y2=caluDiff(x, y1, 2)
    H = caluH(x)
    G = caluG(H, y1)
    GT = np.array(G).T
    # 计算M
    A = caluA(H)
    Ai = np.linalg.inv(A)
    M = np.dot(Ai, GT)
    f=genFun(x,y,M,H)
    return f
