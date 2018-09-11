# -*- coding=utf-8 -*-
import os
import shutil
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree,Element

#'''https://www.jianshu.com/p/bcef2ff6ffaa'''

def renameLabel():
    xmldir = '/home/wurui/gitREPO/ocr-nameplates-cuizhou/data/result/cnnInput/xml'
    savedir = '/media/wurui/WorkSpace/OCR/CarBrandData/lincon/CarBrandLiconKey2/xml'
    for xmlname in os.listdir(xmldir):
        tree = ET.parse(os.path.join(xmldir, xmlname))
        root = tree.getroot()
        obj_nodes = root.findall('object')
        # if len(obj_nodes)>0:
        #     tree.write(os.path.join(savedir, xmlname))
        for obj_node in obj_nodes:
            name_node = obj_node.find('name')
            # print('names=',name_node.text)
            if name_node.text == 'm':
                print(xmlname)
        # tree.write(os.path.join(savedir, xmlname))


def xmlStatisticLabelNum():
    xmldir = '/media/cuizhou/6087-6554/cuizhou/xml'

    dictLabelNum = {}
    for xmlfile in os.listdir(xmldir):
        tree = ET.parse(os.path.join(xmldir, xmlfile))
        root = tree.getroot()
        obj_nodes = root.findall('object')
        for obj_node in obj_nodes:
            name_node = obj_node.find('name')
            label = name_node.text
            if dictLabelNum.keys().__contains__(label):
                dictLabelNum[label] += 1
            else:
                dictLabelNum[label] = 1

    print(dictLabelNum)

    classes_name_txt = 'classes_name.txt'
    f = open(classes_name_txt, 'w')
    rareKey = []
    sorted(dictLabelNum.items(), key=lambda x:x[1], reverse=True)
    for key,item in dictLabelNum.items():
        # f.writelines(str(key)+'\n')
        f.writelines(str(key)+','+str(item)+'\n')
        if(item<8):
            rareKey.append(key)
    f.close()
    print(rareKey)


def selectRareLabelXml():
    rareLabel = ['bread']
    xmldir = '/media/cuizhou/6087-6554/cuizhou/xml'
    savedir = '/media/cuizhou/6087-6554/cuizhou/xml-bread'

    for xmlfile in os.listdir(xmldir):
        tree = ET.parse(os.path.join(xmldir, xmlfile))
        root = tree.getroot()
        obj_nodes = root.findall('object')

        for obj_node in obj_nodes:
            name_node = obj_node.find('name')
            label = name_node.text
            if rareLabel.__contains__(label):
                print(xmlfile)
                shutil.move(os.path.join(xmldir, xmlfile), os.path.join(savedir, xmlfile))
                break




if __name__ == '__main__':
    # renameLabel()
    xmlStatisticLabelNum()
    # selectRareLabelXml()
