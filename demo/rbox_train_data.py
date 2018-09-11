#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import print_function, division
import sys

sys.path.append('../')

import os
import numpy as np
import cv2

IMG_EX = '.jpg'
LABEL_EX = '.rbox'


class RBOX:
    def __init__(self, params):
        if len(params) == 5:
            # 根据中心点/宽高/角度 初始化rbox
            [self.x0, self.y0, self.w, self.h, self.ang] = params
            # if self.ang>=180:
            #     self.ang = self.ang%180
            # 计算角点
            self.GetCorners()
        elif len(params) == 4:
            # 根据角点 初始化rbox
            [self.p1, self.p2, self.p3, self.p4] = params

    def GetCorners(self):
        # 已知中心宽高角度，求角点
        c1 = [-self.w / 2, -self.h / 2]
        c2 = [self.w / 2, -self.h / 2]
        c3 = [self.w / 2, self.h / 2]
        c4 = [-self.w / 2, self.h / 2]
        pts = np.array([c1, c2, c3, c4], dtype=np.float32)
        pts = np.array([pts])
        # 旋转角度，正直表示逆时针旋转
        m = cv2.getRotationMatrix2D((0, 0), self.ang, 1)
        m1 = np.array([[0, 0, 1]])
        m = np.r_[m, m1]
        [self.p1, self.p2, self.p3, self.p4] = cv2.perspectiveTransform(pts, m)[0]
        self.p1[0] += self.x0
        self.p2[0] += self.x0
        self.p3[0] += self.x0
        self.p4[0] += self.x0
        self.p1[1] += self.y0
        self.p2[1] += self.y0
        self.p3[1] += self.y0
        self.p4[1] += self.y0
        return

    def GetCenterAngle(self):
        # 已知角点，求中心宽高角度
        self.x0 = (self.p1[0] + self.p2[0] + self.p3[0] + self.p4[0]) / 4
        self.y0 = (self.p1[1] + self.p2[1] + self.p3[1] + self.p4[1]) / 4
        return

    def Draw(self, image):
        corners = [((int)(self.p1[0]), (int)(self.p1[1])), ((int)(self.p2[0]), (int)(self.p2[1])),
                   ((int)(self.p3[0]), (int)(self.p3[1])), ((int)(self.p4[0]), (int)(self.p4[1]))]
        for i, pt in enumerate(corners):
            cv2.circle(image, pt, 3, (0, 255, 0), 2)
            cv2.line(image, corners[i], corners[(i + 1) % 4], (0, 255, 0), 2)

        px = self.x0 + self.w / 2 * np.cos(self.ang / 180 * np.pi)
        py = self.y0 - self.w / 2 * np.sin(self.ang / 180 * np.pi)
        cv2.circle(image, ((int)(self.x0), (int)(self.y0)), 3, (0, 0, 255), 2)
        cv2.line(image, ((int)(self.x0), (int)(self.y0)), ((int)(px), (int)(py)), (0, 255, 0), 2)
        return image


def OutToFile(rboxes, rboxfile_path):
    f = open(rboxfile_path, 'w')
    for rbox in rboxes:
        f.writelines(
            str(rbox.x0) + ' ' + str(rbox.y0) + ' ' + str(rbox.w) + ' ' + str(rbox.h) + ' 1 ' + str(rbox.ang) + '\n')
    f.close()

def ReadRboxFile(rootdir):
    for img in os.listdir(rootdir):
        if img[-4:] == IMG_EX:
            label = os.path.join(rootdir, img + LABEL_EX)
            if os.path.exists(label):
                image = cv2.imread(os.path.join(rootdir, img))
                if image.shape[0] < 1 or image.shape[1] < 1:
                    print('image size 0')
                    continue

                # 读取标签文件
                f = open(label, 'r')
                while True:
                    try:
                        line = f.readline()
                        line = line.strip('\n')
                        [x, y, w, h, cls, ang] = line.split(' ')
                        x = (float)(x)
                        y = (float)(y)
                        w = (float)(w)
                        h = (float)(h)
                        ang = (float)(ang)

                        print('x:{} y:{} w:{} h:{} ang:{}'.format(x, y, w, h, ang))

                    except:
                        break

def GetRboxesFromFile(label_path):
    # 读取标签文件
    rboxes = []
    f = open(label_path, 'r')
    while True:
        try:
            line = f.readline()
            line = line.strip('\n')
            [x, y, w, h, cls, ang] = line.split(' ')
            x = (float)(x)
            y = (float)(y)
            w = (float)(w)
            h = (float)(h)
            ang = (float)(ang)

            print('x:{} y:{} w:{} h:{} ang:{}'.format(x, y, w, h, ang))

            # 画 rbox
            params = [x, y, w, h, ang]
            rboxes.append(RBOX(params))
        except:
            break
    return rboxes


def check_display(rootdir):
    '''
    rootdir: 图片和标签放在同级目录
    标签文件格式：中心点坐标 x y，box宽高w h，类别（前景1 背景0），角度 [0,360)
    显示图片和标签效果，显示坐标和方向
    检查角度是否在[0,180）, 不是则修正
    '''
    for img in os.listdir(rootdir):
        if img[-4:] == IMG_EX:
            label = os.path.join(rootdir, img + LABEL_EX)
            if os.path.exists(label):
                image = cv2.imread(os.path.join(rootdir, img))
                if image.shape[0] < 1 or image.shape[1] < 1:
                    print('image size 0')
                    continue

                # 读取标签文件
                rboxes = GetRboxesFromFile(label)
                for rbox in rboxes:
                    image = rbox.Draw(image)
                    if rbox.ang<0 or rbox.ang>=360:
                        print('image: {}   angle:{}'.format(img, rbox.ang))
                cv2.imshow('boxes', image)
                cv2.waitKey(0)


def augment_rotate(angle, rboxes, image, imgName, savedir):
    m = cv2.getRotationMatrix2D((image.shape[1] / 2, image.shape[0] / 2), angle, 1)

    # new image
    rotate_image = cv2.warpAffine(image, m, (image.shape[1], image.shape[0]))

    # new rbox
    pts = []
    for rbox in rboxes:
        pts.append([rbox.x0, rbox.y0])
    pts = np.array([pts], dtype=np.float32)
    # pts = np.array([pts])

    m1 = np.array([[0,0,1]])
    m = np.r_[m,m1]
    rotate_pts = cv2.perspectiveTransform(pts, m)[0]
    for i, rbox in enumerate(rboxes):
        [rbox.x0, rbox.y0] = rotate_pts[i]
        rbox.ang += angle
        rbox.ang = rbox.ang%360
        rbox.GetCorners()
    #     rbox.Draw(rotate_image)
    # cv2.imshow('org', image)
    # cv2.imshow('rotate', rotate_image)
    # cv2.waitKey(0)

    # write to file
    new_img_name = os.path.join(savedir, imgName[0:-4]+'_rotate_'+str(angle)+'.jpg')
    cv2.imwrite(new_img_name, rotate_image)
    OutToFile(rboxes, new_img_name+'.rbox')
    print('save: ',new_img_name+'\n')

def augment():
    rootdir = '/home/cuizhou/Desktop/bread-resize'
    savedir = '/home/cuizhou/Desktop/180'
    for img in os.listdir(rootdir):
        if img[-4:] == IMG_EX:
            label = os.path.join(rootdir, img + LABEL_EX)
            if os.path.exists(label):
                image = cv2.imread(os.path.join(rootdir, img))
                if image.shape[0] < 1 or image.shape[1] < 1:
                    print('image size 0')
                    continue

                # 读取rbox标签文件
                rboxes = GetRboxesFromFile(label)

                # 旋转增强
                augment_rotate(270, rboxes, image, img, savedir)
                # augment_rotate(180, rboxes, image, img, savedir)
                # augment_rotate(270, rboxes, image, img, savedir)
                # augment_rotate(90, rboxes, image, img, savedir)

    return

def trainval():
    rootdir = '/home/cuizhou/Repositories/DRBox-master/data/Bread/train_data'
    tarinval_path = '/home/cuizhou/Repositories/DRBox-master/data/Bread/trainval.txt'
    f = open(tarinval_path, 'w')
    for img in os.listdir(rootdir):
        if img[-4:] == IMG_EX:
            label = os.path.join(rootdir, img + LABEL_EX)
            if os.path.exists(label):
                f.writelines(img+' ' +img+LABEL_EX+'\n')
    f.close()

def resizeImgToCnnInput(rootdir):
    for img in os.listdir(rootdir):
        try:
            image = cv2.imread(os.path.join(rootdir, img))
            bkg = np.zeros((700,700,3), dtype=np.uint8)
            bkg[110:590, 30:670] = image
            cv2.imwrite(os.path.join(rootdir, img), bkg)
        except:
            continue

def drawDetectResult(rootdir):
    image = cv2.imread('/home/cuizhou/Desktop/test/401.jpg')
    ratio_w = image.shape[1] / 300.0
    ratio_h = image.shape[0] / 300.0
    for fil in os.listdir(rootdir):
        if fil[-6:] == '.score':
            f = open(os.path.join(rootdir, fil), 'r')
            while True:
                try:
                    line = f.readline()
                    line = line.strip('\n')
                    [x, y, w, h, cls, ang, score] = line.split(' ')
                    x = (float)(x)
                    y = (float)(y)
                    w = (float)(w) # *ratio_w
                    h = (float)(h) # *ratio_h
                    ang = (float)(ang)
                    score = (float)(score)

                    print('x:{} y:{} w:{} h:{} ang:{} score:{}'.format(x, y, w, h, ang, score))

                    # 画 rbox
                    if(score>0.9):
                        params = [x, y, w, h, ang]
                        rbox = RBOX(params)
                        rbox.Draw(image)
                except:
                    break
            cv2.imshow('result', image)
            cv2.waitKey(0)



if __name__ == '__main__':
    rootdir = '/home/cuizhou/Desktop/rbox-bread'#'/home/cuizhou/Repositories/DRBox-master/data/Airplane/train_data'
    # ReadRboxFile('/home/cuizhou/Repositories/DRBox-master/data/Airplane/train_data')
    # check_display(rootdir)
    # augment()
    # trainval()
    # resizeImgToCnnInput('/home/cuizhou/Desktop/test')
    drawDetectResult('/home/cuizhou/Repositories/DRBox-master/examples/rbox/deploy/Airplane')

