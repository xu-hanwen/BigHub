import os
import cv2
from settings import *

def splitimage(src,rownum,colnum,dstpath):

    img=cv2.imread(src)
    w,h=img.shape[0],img.shape[1] #图片大小
    if rownum<=h and colnum<=w:
        print('开始处理图片切割，请稍候-')
        s=os.path.split(src)
        if dstpath=='':#没有输入路径
            dstpath=s[0]#使用源图片所在目录s[0]
        fn=s[1].split('.')#s[1]是源图片文件名
        basename=fn[0]#主文件名
        ext=fn[-1]#扩展名
        num=1
        rowheight = h//rownum
        colwidth = w//colnum
        for r in range(rownum):
            for c in range(colnum):
                ROI = img[r*rowheight:(r+1)*rowheight,c*colwidth:(c+1)*colwidth]
                # cv2.imshow('roi',ROI)
                # cv2.waitKey()
                cv2.imwrite(os.path.join(dstpath,basename+''+str(num)+'.'+ext),ROI)
                num=num+1
        num -= 1
        print('图片切割完毕，共生成%s张小图片。'% num)
    else:
        print('不合法的行列切割参数！')

def image(src,dstpath=''):

    src = src
    dstpath=dstpath
    img_cv2 = cv2.imread(src)
    img_cv2 = cv2.resize(img_cv2,(320,320))
    cv2.imwrite("image/image.jpeg",img_cv2)
    # cv2.imshow("img_cv2",img_cv2)
    # cv2.waitKey()
    src = "image/image.jpeg"
    if(dstpath=='')or os.path.exists(dstpath):
        row,col=BOARDWIDTH,BOARDHEIGHT
        if row>0 and col>0:
            splitimage(src,row,col,dstpath)
        else:
            print('无效的行列切割参数！')
    else:
        print('图片输出目录%s不存在！'%dstpath)




