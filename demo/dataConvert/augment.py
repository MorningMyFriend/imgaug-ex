# -*- coding:utf-8 -*-
from __future__ import print_function, division
import sys
sys.path.append('../../')

import os
import shutil
import copy

import numpy as np
from scipy import misc
from imgaug import augmenters as iaa
import imgaug as ia

from scipy import ndimage, misc
from skimage import data

import json
from xml.etree import ElementTree
from lxml import etree
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, ElementTree
import codecs

import cv2

# options

NUM_IMG_NEW = 4  # 生成新图像的数量
NUM_ROI_MIN = 1  # 图上至少含有的目标数量，否则跳过

seq = iaa.Sequential([
        # iaa.Crop(px=(0, 16)),  # crop images from each side by 0 to 16px (randomly chosen)
        # iaa.Fliplr(0.5),  # horizontally flip 50% of the images
        # iaa.Flipud(0.5),
        # iaa.Affine(rotate=(90)),
        # iaa.Affine(#scale={"x": (0.5, 2.0), "y": (0.5, 2.0)},
        # scale images to 80-120% of their size, individually per axis
        # translate_px={"x": (-16, 16), "y": (-16, 16)},
        iaa.Affine(scale=(0.8, 1.09)),
        # iaa.AdditiveGaussianNoise(scale = 0.1*100),
        iaa.Affine(rotate=(-3, 3), mode='edge'),
        iaa.Crop(px=(0, 100)),
        # iaa.Affine(shear = 5, mode = 'edge'),
        #     shear=(-30, 30)),
        iaa.Multiply((0.7, 1.3)),  # change brightness of images (50-150% of original value)
        # iaa.ContrastNormalization((0.8, 1.5))
    ])

def parseJson(jsonPath):
    '''
    根据 json 格式不同修改此函数
    :param jsonPath:
    :return:
    '''
    f = open(jsonPath, encoding = 'utf-8')
    root = json.load(f)
    points = root['shapes'][0]['points']
    return points

def writeJson(jsonPath, points):
    points = points.tolist()
    shapes = {'label': 'idcard', 'points': points}
    with open(jsonPath, 'w') as f:
        json.dump(shapes, f)



def augment_json(imgdir, jsondir, saveimgdir, savejsondir):
    imgId = []
    for imgName in os.listdir(imgdir):
        imgId.append(imgName.split('.')[0])

    for jsonFile in os.listdir(jsondir):
        if imgId.__contains__(jsonFile[0:-5]) == False:
            print('json file:', jsonFile, ' has no img')
            continue

        image = cv2.imread(os.path.join(imgdir, jsonFile[0:-5]+'.jpeg'))

        points = parseJson(os.path.join(jsondir, jsonFile))
        keypoints = []
        for point in points:
            keypoints.append(ia.Keypoint(point[0], point[1]))
        keypoints = [ia.KeypointsOnImage(keypoints, shape=image.shape)]

        # enhance
        for i in range(NUM_IMG_NEW):
            seq_det = seq.to_deterministic()
            image_aug = seq_det.augment_image(image)
            keypoints_aug = seq_det.augment_keypoints(keypoints)[0]
            new_points = keypoints_aug.get_coords_array()

            writeJson(os.path.join(savejsondir, jsonFile[0:-5]+'_'+str(i)+'.json'), new_points)




if __name__ == '__main__':
    imgdir = '/home/wurui/Downloads/OcrData/id-card/front'
    jsondir = '/home/wurui/Downloads/OcrData/id-card/json'
    saveimgdir = '../img'
    savejsondir = '../pascal'
    augment_json(imgdir, jsondir, saveimgdir, savejsondir)
