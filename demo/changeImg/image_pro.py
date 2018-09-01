import os
import cv2
import numpy as np
from voc_and_textbox.tool_scripts.pascal_voc_io import *

def  shift(image, x, y):
    M = np.float32([1,0,x], [0,1,y])
    shiftImg = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    return shiftImg

def rotate(image, angle, center=None, scale=1.0):
    (h, w) = image.shape[:2]
    if center is None:
        center = (w/2, h/2)
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotateImg = cv2.warpAffine(image, M, (w, h))
    return rotateImg

def cropImgFromXml(imgdir, xmldir, savedir):
    for fname in os.listdir(xmldir):
        xml = os.path.join(xmldir, fname)

        imgname = os.path.join(imgdir, os.path.splitext(fname)[0] + '.jpg')
        img = cv2.imread(imgname)
        if img.shape[0]<1 or img.shape[1]<1:
            print('img none:', imgname)
            continue

        reader = PascalVocReader(xml)

        shapes = reader.getShapes()
        polygons = [shape[1] for shape in shapes]

        # polygons.size = 1
        for id,polygon in enumerate(polygons):
            imgRoi = img[polygon[0][1]-20:polygon[2][1]+20, polygon[0][0]-20:polygon[2][0]+20]
            cv2.imwrite(os.path.join(savedir, os.path.splitext(fname)[0] + '.jpg'), imgRoi)


if __name__ == '__main__':
    imgdir = '/media/wurui/WorkSpace/OCR/CarBrandData/汽车名牌/奥迪596铭牌照2'
    # xmldir = '/media/wurui/WorkSpace/windows_v1.2/data/xml'
    savedir = '/media/wurui/WorkSpace/OCR/CarBrandData/汽车名牌/audi596-v'
    # cropImgFromXml(imgdir, xmldir, savedir)

    # resize rotate img
    for f in os.listdir(imgdir):
        img = cv2.imread(os.path.join(imgdir,f))
        # if img.shape[1] < img.shape[0]:
        img = rotate(img, 180)
        # img = cv2.resize(img, (img.shape[1]/3, img.shape[0]/3), img)
        # cv2.imshow('img', img)
        cv2.imwrite(os.path.join(savedir,f), img)

    # crop img
    # for f in os.listdir(imgdir):
        # old = os.path.join(imgdir,f)
        # new = old[0: -4]+'.jpg'
        # os.rename(old, new)
        # img = cv2.imread(os.path.join(imgdir, f))
        #
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
        # cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel, img, iterations=2)
        # cv2.imshow("",img)
        # cv2.waitKey(0)

        # # cv2.imshow("",img)
        # # cv2.waitKey(0)
        # img = np.zeros(img.shape, dtype = np.uint8)
        # # cv2.imshow("", img)
        # # cv2.waitKey(0)
        # # img = img[0:(int)(img.shape[0]*0.65), 0:(int)(img.shape[1]*0.8)]
        # img = cv2.resize(img, (img.shape[1]/2, img.shape[0]/2), img,interpolation=cv2.INTER_CUBIC)
        # cv2.imwrite(os.path.join(savedir,f), img)
        print(f)
