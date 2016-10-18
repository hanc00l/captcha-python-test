# captcha-python-test

--

受《验证码破解技术四部曲》[https://github.com/nladuo](https://github.com/nladuo) 启发，学习验证码识别的相关技术，包括opencv、tesseract、机器学习算法（kNN和SVM）等，将原作者的算法改为python。

验证码识别的难点在于对图像的干扰的处理，只要能正确去除干扰、分割字符，通过机器学习或人工神经网络，识别率都还能比较高。目前对复杂的验证码的图形处理还有待提高。。。

--
#### 1、相关依赖组件

+ opencv2
+ tesseract、pytesseract
+ numpy
+ libsvm

#### 2、tesseract

![](basic.jpg)

对于简单的验证码，直接使用pytesseract可以识别

#### 3、csdn1

![](csdn1.png)

纯数字、干扰小的验证码，简单进行图片去除背景、二值化和阈值处理后，使用kNN算法识别。

#### 4、csdn2

![](csdn2.png)

字母加数字、背景有干扰、图形字符位置有轻微变形，进行图片去除背景、二值化和阈值处理后，使用kNN算法识别；相比csdn1，主要是进行图形规整化处理后与csdn1区别不大。


#### 5、weibo.cn

![](weibo.cn.png)

背景有严重干扰（包括色斑、干扰线、噪声等）、字符变形类的验证码，识别的关键在于去干扰和提取字符，只要去干扰处理得好，使用足够的测试数据进行SVM（支持向量机）训练，识别率相当的高（>90%）。

