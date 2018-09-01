import cv2
import os
import numpy as np

imgdir = '/home/wurui/Desktop/trainImg/TrainData_OCR_Namplate_DZ/VOCdevkit2007/VOC2007/img'
resultdir = '/home/wurui/Desktop/trainImg/TrainData_OCR_Namplate_DZ/VOCdevkit2007/VOC2007/imgFill'

rois = [[207, 68, 832, 95],
        [730, 224, 304, 130],
        [290, 410, 260, 93],
        [101, 241, 182, 94],
        [839, 412, 158, 91],
        [32, 158, 750, 95],
        [100, 330, 201, 90],
        [111, 490, 301, 94]]

def fillAreaNotRoi():
    for img in os.listdir(imgdir):
        image = cv2.imread(os.path.join(imgdir,img))
        imgFill = np.zeros((image.shape[0], image.shape[1],3), np.uint8)
        for roi in rois:
            imgFill[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]] = image[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]

        # cv2.imshow('', imgFill)
        # cv2.waitKey(0)
        cv2.imwrite(os.path.join(resultdir,img), imgFill)
    print 'ok'

if __name__ == '__main__':
    fillAreaNotRoi()