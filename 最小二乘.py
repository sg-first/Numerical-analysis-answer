x=[-2,-1,0,1,2]
y=[0,1,2,1,0]

sx=0
sx2=0
sx3=0
sx4=0
sy=0
sxy=0
sx2y=0

n=len(x)

for i in range(n):
    sx+=x[i]
    sx2+=x[i]**2
    sx3+=x[i]**3
    sx4+=x[i]**4
    sy+=y[i]
    sxy+=x[i]*y[i]
    sx2y+=(x[i]**2)*y[i]

A=[[n,sx,sx2],
   [sx,sx2,sx3],
   [sx2,sx3,sx4]]

B=[sy,sxy,sx2y]

import numpy as np
A=np.array(A)
B=np.array(B)

result=np.linalg.solve(A,B)

print(sx,sx2,sx3,sx4,sy,sxy,sx2y)
print(result)