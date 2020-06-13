import numpy as np

def getLU(A):
    shape=A.shape
    L=np.zeros(shape)
    U=np.zeros(shape)
    r,_=shape

    for i in range(r):
        U[0,i]=A[0,i]
    for i in range(r):
        L[i,0]=A[i,0]/U[0,0]

    for i in range(1,r):
        for j in range(r):
            if j < i:
                U[i, j] = 0
            else:
                sum=0
                for k in range(i):
                    sum+=L[i,k]*U[k,j]
                U[i,j]=A[i,j]-sum
        for j in range(r):
            if i==j:
                L[j,i]=1
            elif j < i: # 注意这里i和j是反的
                L[j,i]=0
            else:
                sum=0
                for k in range(i): # 求的是j i
                    sum+=L[j,k]*U[k,i]
                L[j,i]=(A[j,i]-sum)/U[i,i]

    return L,U

A=[[4,2,0,0],[1,4,1,0],[0,1,4,1],[0,0,2,4]]
A=np.array(A)
L,U=getLU(A)
print(L)
print(U)

def getY(L,b): # 使用行向量
    r=b.shape[0]
    y=np.zeros(b.shape)
    y[0]=b[0]
    for i in range(1,r):
        y[i]=b[i]
        for j in range(i):
            y[i]-=L[i,j]*y[j]
    return y

b=[-1,0,0,0]
b=np.array(b)
y=getY(L,b)
print(y)


def getX(U,b):
    r = b.shape[0]
    y = np.zeros(b.shape)
    y[r-1] = b[r-1] / U[r-1,r-1]
    for i in range(r-2, -1, -1): # 最后一行完事了，从倒数第二行开始
        y[i] = b[i]
        for j in range(r-1, i, -1): # 从最后一个往前减，i不减，直接除
            y[i] -= U[i, j] * y[j]
        y[i] /= U[i, i]
    return y

x=getX(U,y)
print(x)