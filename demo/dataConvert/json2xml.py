#coding=utf-8
import os
import shutil
import json
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, ElementTree


def parseJson(jsonPath):
    f = open(jsonPath, encoding = 'utf-8')
    root = json.load(f)
    imgName = root['imagePath']
    points = root['shapes']['points']
    return imgName, points


def genVocXml(filename, bndbox):
    annotation = Element('annotation')

    # unnessesury info
    folder = SubElement(annotation, 'folder')
    folder.text = '1'
    file = SubElement(annotation, 'filename')
    file.text = filename
    path = SubElement(annotation, 'path')
    path.text = filename
    source = SubElement(annotation, 'source')
    database = SubElement(source, 'database')
    database.text = 'Unknown'
    size = SubElement(annotation, 'size')
    width = SubElement(size, 'width')
    width.text = '2400'
    height= SubElement(size, 'height')
    height.text = '1200'
    depth = SubElement(size, 'depth')
    depth.text = '3'
    segmented = SubElement(annotation, 'segmented')
    segmented.text = '0'

    obj = SubElement(annotation, 'object')
    name = SubElement(obj, 'name')
    name.text = 'idcard'
    pose = SubElement(obj, 'pose')
    pose.text = 'Unspecified'
    truncated = SubElement(obj, 'truncated')
    truncated.text = '0'
    difficult = SubElement(obj, 'difficult')
    difficult.text = '0'

    box = SubElement(object, 'bndbox')
    xmin = SubElement(box, 'xmin')
    # xmin.text = bndbox[]
    ymin = SubElement(box, 'ymin')
    xmax = SubElement(box, 'xmax')
    ymax = SubElement(box, 'ymax')




def convert(jsonDir, saveDir):
    for jsonfile in os.listdir(jsonDir):
        imgName, Points = parseJson(os.path.join(jsonDir, jsonfile))



if __name__ == '__main__':
    jsonDir = '/home/wurui/Downloads/OcrData/id-card/json'
    saveDir = '/home/wurui/Downloads/OcrData/id-card/xml'