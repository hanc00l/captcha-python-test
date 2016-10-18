#!/usr/bin/env python
# encoding: utf-8
import cv2

img = cv2.imread('m.jpg')
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
