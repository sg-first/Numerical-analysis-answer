import cv2
import numpy as np
import math

# 不同值时可以用来逼近不同的样条函数
a = -1/2

# 样条函数
def S(x):
    if (abs(x) >= 0) & (abs(x) <= 1):
        return (a+2) * (abs(x) ** 3) - (a + 3) * (abs(x) ** 2) + 1
    elif (abs(x) > 1) & (abs(x) <= 2):
        return a * (abs(x) ** 3) - (5 * a) * (abs(x) ** 2) + (8 * a) * abs(x) - 4 * a
    return 0

# 填充2像素边界，避免在对边界处理时越界
def padding(img,H,W,C):
    zimg = np.zeros((H+4,W+4,C))
    zimg[2:H+2,2:W+2,:C] = img
    # Pad the first/last two col and row
    zimg[2:H+2,0:2,:C]=img[:,0:1,:C]
    zimg[H+2:H+4,2:W+2,:]=img[H-1:H,:,:]
    zimg[2:H+2,W+2:W+4,:]=img[:,W-1:W,:]
    zimg[0:2,2:W+2,:C]=img[0:1,:,:C]
    # Pad the missing eight points
    zimg[0:2,0:2,:C]=img[0,0,:C]
    zimg[H+2:H+4,0:2,:C]=img[H-1,0,:C]
    zimg[H+2:H+4,W+2:W+4,:C]=img[H-1,W-1,:C]
    zimg[0:2,W+2:W+4,:C]=img[0,W-1,:C]
    return zimg

# 双三次插值
def bicubic(img, ratio):
    H,W,C = img.shape # 宽、高、通道数

    img = padding(img,H,W,C)
    # Create new image
    dH = math.floor(H*ratio)
    dW = math.floor(W*ratio)
    dst = np.zeros((dH, dW, 3)) # 放大后图像

    h = 1/ratio

    for c in range(C):
        for j in range(dH):
            for i in range(dW): # 遍历新图像中的每个像素
                print(c,j,i)
                x, y = i * h + 2 , j * h + 2 # 算要处理的中心像素（+2是因为扩了2像素边界，有一个偏置）

                # 周围的像素和中间像素差多少（用于带入样条函数）
                x1 = 1 + x - math.floor(x)
                x2 = x - math.floor(x)
                x3 = math.floor(x) + 1 - x
                x4 = math.floor(x) + 2 - x

                y1 = 1 + y - math.floor(y)
                y2 = y - math.floor(y)
                y3 = math.floor(y) + 1 - y
                y4 = math.floor(y) + 2 - y

                mat_l = np.matrix([[S(x1), S(x2), S(x3), S(x4)]]) # 求横向权重
                # 使用周围16个像素的值
                mat_m = np.matrix([[img[int(y-y1),int(x-x1),c],img[int(y-y2),int(x-x1),c],img[int(y+y3),int(x-x1),c],img[int(y+y4),int(x-x1),c]],
                                   [img[int(y-y1),int(x-x2),c],img[int(y-y2),int(x-x2),c],img[int(y+y3),int(x-x2),c],img[int(y+y4),int(x-x2),c]],
                                   [img[int(y-y1),int(x+x3),c],img[int(y-y2),int(x+x3),c],img[int(y+y3),int(x+x3),c],img[int(y+y4),int(x+x3),c]],
                                   [img[int(y-y1),int(x+x4),c],img[int(y-y2),int(x+x4),c],img[int(y+y3),int(x+x4),c],img[int(y+y4),int(x+x4),c]]])
                mat_r = np.matrix([[S(y1)], [S(y2)], [S(y3)], [S(y4)]]) # 求纵向权重
                dst[j, i, c] = np.dot(np.dot(mat_l, mat_m),mat_r)
    return dst


img = cv2.imread('zhaoxin.png')

# Scale ratio
ratio = 2

dst = bicubic(img, ratio)
cv2.imwrite('bigzhaoxin.png', dst)
