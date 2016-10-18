#!/usr/bin/env python
# encoding: utf-8

from PIL import Image
import pytesseract
import cv2

def get_code(filename):
    temp_code_filename = '/tmp/tmp_code.jpg'
    img = cv2.imread(filename)
    ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    cv2.imwrite(temp_code_filename,img)
    img_code = Image.open(temp_code_filename)
    code = pytesseract.image_to_string(img_code)
    return code

def main():
    print get_code('test1.jpg')
    print get_code('test2.jpg')
    print get_code('test3.jpg')
    print get_code('1.png')
    print get_code('2.png')
    print get_code('3.png')
    print get_code('4.png')
    print get_code('5.png')
    

if __name__ == '__main__':
    main()
