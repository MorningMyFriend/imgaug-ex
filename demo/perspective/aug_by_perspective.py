#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import print_function, division
import sys
import os
import cv2
import numpy as np

class Perspective:
    def __init__(self):
        self.transMats = self.loadSampleImgs()


    def loadSampleImgs(self):
        '''
        读取基础图像，矫正为标准图像，得到矩形四个角点坐标 ptSrc
        读取目标效果图像，人为给出角点坐标，或者程序提取出
        每个矩形角点按照[tl tr br bl]顺序存储
        :return: transMats
        '''
        imgdir = 'perspective_imgs'
        baseImg = cv2.imread(os.path.join(imgdir, '0.jpg'))

        ptRaw = np.float32([[319.3,249.3], [1126, 246], [1124, 815.3], [327.6, 819.5]])
        xmin = (ptRaw[0][0] + ptRaw[3][0]) / 2
        xmax = (ptRaw[1][0] + ptRaw[2][0]) / 2
        ymin = (ptRaw[0][1] + ptRaw[1][1]) / 2
        ymax = (ptRaw[2][1] + ptRaw[3][1]) / 2
        ptSrc = np.float32([[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]])

        ptDes = []
        ptDes.append(np.float32([[410.7,242],[1172,338.7],[1050.5,794.4],[383.7, 757.7]]))
        ptDes.append(np.float32([[360, 191.5],[1188,286.7],[1068, 848.5],[356,704]]))
        ptDes.append(np.float32([[308.8,240],[1080.5, 241.5],[1148.7,764],[359.3,883.3]]))
        ptDes.append(np.float32([[358.5,313.5],[1142.2,156.5],[1210.3,858.3],[355.5,854.2]]))
        ptDes.append(np.float32([[298.5,253.8],[1124.7,243.3],[1168.3,856.3],[255.5,853]]))
        ptDes.append(np.float32([[292.7,274.5],[1151.5,268.3],[1091.5,799.8],[362.2,795.5]]))
        ptDes.append(np.float32([[352,215.2],[1161.2,261.5],[1165,809],[365.8,883.6]]))
        ptDes.append(np.float32([[303.3,252],[1177.5,209.5],[1161.8,897.2],[311.5,828.8]]))


        transMats = []
        for pts in ptDes:
            transMat = cv2.getPerspectiveTransform(ptSrc, pts)
            transMats.append(transMat)

        return transMats

    def transform(self, img, pts):
        '''
        增强图像，并且求变换后的点坐标
        :param img: 输入图像
        :param pts: 输入图像上的点
        :return: imgWarped, ptsWarped
        '''

        pts = np.array([pts], dtype=np.float32)

        ptsDes = []
        imgDes = []
        for transMat in self.transMats:
            imgWarped = cv2.warpPerspective(img, transMat, (img.shape[1], img.shape[0]))
            # 要求输入三通道，float32类型 数组
            ptsWarped = cv2.perspectiveTransform(pts, transMat)

            imgDes.append(imgWarped)
            ptsDes.append(ptsWarped[0])

        # for pt in pts[0]:
        #     cv2.circle(img, (pt[0],pt[1]), 3, (0,255,0), 3)
        #
        # for pt in ptsWarped[0]:
        #     cv2.circle(imgWarped, (pt[0],pt[1]), 3, (0, 255, 0), 3)

        # cv2.imshow('img src', img)
        #     cv2.imshow('img warp',imgWarped)
        #     cv2.waitKey(0)
        return imgDes, ptsDes

def main():
    tranformer = Perspective()
    transMats = tranformer.loadSampleImgs()

    for index, mat in enumerate(transMats):
        img = cv2.imread('/home/wurui/图片/test.jpg')
        if img.shape[0]<1 or img.shape[1]<1:
            continue

        pts = np.float32([[300,300],[700,300],[700,700],[300,700]])
        tranformer.transform(img, pts)

if __name__ == '__main__':
    main()
    #
    # augment_times = 3
    # voc_dir = "/home/wurui/Desktop/CarBrandLinconKey/org/"
    # xml_dir = os.path.join(voc_dir, 'xml')
    # img_dir = os.path.join(voc_dir, 'img')
    # res_xml_dir = os.path.join(voc_dir, 'Annotations')
    # res_img_dir = os.path.join(voc_dir, 'JPEGImages')
    #
    # xmls = os.listdir(xml_dir)
    # for xml in xmls:
    #     augment(xml)
    #     # pool = mp.Pool(processes=None)
    #     # pool.map(augment, xmls)
    #     # filter_invalid_xml(res_xml_dir, res_img_dir, '/tmp/xml_filter')
