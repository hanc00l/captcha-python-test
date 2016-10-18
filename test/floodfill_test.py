#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np

# 读入图像
filename = 'floodfill.png'
im = cv2.imread(filename)
# 转换颜色空间
rgbIm = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

# 获取图像尺寸
h, w = im.shape[:2]
print im.shape
# 泛洪填充
diff = (8, 8, 8)
mask = np.zeros((h+2, w+2), np.uint8)
#cv2.floodFill(image, mask, seedPoint, newVal[, loDiff[, upDiff[, flags]]]) → retval, rect¶
#ret1,ret2 = cv2.floodFill(im, mask, (10, 10), (255, 255, 0), diff, diff)
#print mask[h/2]
ret1,rect = cv2.floodFill(im, mask, (200, 300), (255, 255, 0), diff, diff)
#print mask[h/2]
print ret1
print rect

# 在OpenCV窗口中显示泛洪填充后的结果
cv2.imshow('flood fill', im)
# 显示被填充的区域
x1 = rect[0]
y1 = rect[1]
x2 = x1 + rect[2]
y2 = y1 +rect[3]
im2 = im[y1:y2,x1:x2]
cv2.imshow('new',im2)
#
cv2.waitKey()
cv2.destroyAllWindows()
