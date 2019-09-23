# -*- coding:utf-8 -*-
from __future__ import print_function, division
import sys

sys.path.append('../')

from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from lxml import etree
import codecs

import os
import copy


def prettify(elem):
    """
        Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf8')
    root = etree.fromstring(rough_string)
    return etree.tostring(root, pretty_print=True)

def changeBoundingBox(xmldir, targetdir):
    for fxml in os.listdir(xmldir):
        parser = etree.XMLParser(encoding='utf-8')
        xmltree = ElementTree.parse(os.path.join(xmldir, fxml), parser=parser).getroot()
        pascal_voc_tree = copy.deepcopy(xmltree)
        for object_iter in pascal_voc_tree.findall('object'):
            bndbox = object_iter.find('bndbox')
            xmin = bndbox.find('xmin').text
            ymin = bndbox.find('ymin').text
            xmax = bndbox.find('xmax').text
            ymax = bndbox.find('ymax').text

            if int(xmin) > int(xmax):
                xmin, xmax = xmax, xmin
            if int(ymin) > int(ymax):
                ymin, ymax = ymax, ymin

            bndbox.find('xmin').text = xmin
            bndbox.find('xmax').text = xmax
            bndbox.find('ymin').text = ymin
            bndbox.find('ymax').text = ymax

        out_file = codecs.open(os.path.join(targetdir, fxml), 'w', encoding='utf-8')
        prettifyResult = prettify(pascal_voc_tree)
        out_file.write(prettifyResult.decode('utf8'))
        out_file.close()


if __name__ == '__main__':
    xmldir = '/home/wurui/project/imgaug-ex/demo/pascal'
    targetdir = '/home/wurui/project/imgaug-ex/demo/xml'
    changeBoundingBox(xmldir, targetdir)