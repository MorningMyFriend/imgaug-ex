# -*- coding=utf-8 -*-
import os
import shutil
import cv2

import xml.etree.ElementTree as ET


def getClassesAndMkdir(xmldir, savedir):
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

    classes_name_txt = os.path.join(savedir,'classes_name.txt')
    f = open(classes_name_txt, 'w')

    for key, item in dictLabelNum.items():
        f.writelines(str(key) + '\n')
        # f.writelines(str(key)+','+str(item)+'\n')

    f.close()


def main(imgdir, xmldir, savedir):
    # create classes_name.txt and mkdir for images
    getClassesAndMkdir(xmldir, savedir)

    # txt file: subimgpath label
    trainTxt = open(os.path.join(savedir, 'train.txt'), 'w')

    # crop subimgs from xmls
    imgNames = []
    for img in os.listdir(imgdir):
        imgNames.append(img[0:-4])


    for xmlfile in os.listdir(xmldir):
        name = xmlfile[0:-4]
        if imgNames.__contains__(name) == False:
            print("Warnning!!! ",name," not exist in ", imgdir)
            continue
        #image
        image = cv2.imread(os.path.join(imgdir, name+'.jpg'))
        if image.shape[0]==0 or image.shape[1]==0:
            print('image read null:', name)
            continue

        # parse xml
        tree = ET.parse(os.path.join(xmldir, xmlfile))
        root = tree.getroot()

        obj_nodes = root.findall('object')
        for id,obj_node in enumerate(obj_nodes):
            # label name
            name_node = obj_node.find('name')
            label = name_node.text
            # rect
            rect_node = obj_node.find('bndbox')
            xmin = max(0, int(rect_node.find('xmin').text))
            ymin = max(0, int(rect_node.find('ymin').text))
            xmax = min(image.shape[1], int(rect_node.find('xmax').text))
            ymax = min(image.shape[1], int(rect_node.find('ymax').text))
            # subimg
            subimg = image[ymin:ymax, xmin:xmax]
            # save subimg
            if os.path.exists(os.path.join(savedir, label)) == False:
                os.makedirs(os.path.join(savedir, label))
            subimgName = os.path.join(savedir, label, name + '-'+str(id)+'.jpg')
            cv2.imwrite(subimgName, subimg)
            # add to train.txt list
            trainTxt.write(subimgName+' '+label+'\n')

    trainTxt.close()
    return

if __name__ == '__main__':
    imgdir = '/home/wurui/Downloads/ZT/img'
    xmldir = '/home/wurui/Downloads/ZT/xml'
    savedir = '/home/wurui/Downloads/ZT/traindata'

    main(imgdir, xmldir, savedir)