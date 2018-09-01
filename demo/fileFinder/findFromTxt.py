import os
import shutil

def findImgFromTxtList():
    fromdir = '/media/wurui/WorkSpace/OCR/CarBrandData/binli/JPEGImages'
    savedir = "/media/wurui/WorkSpace/OCR/CarBrandData/binli/testImg-3"
    f = open("imgName.txt")
    while(1):
      line = f.readline();

      # line = name.jpg
      # imgname = line[:-1]
      # print imgname.split('/')[-1]
      # newimg = os.path.join(savedir,imgname.split('/')[-1])
      # print imgname

      # line = name
      imgName = line.split('\n')[0]
      print(imgName)
      imgname = os.path.join(fromdir, imgName+'.jpg')
      newimg = os.path.join(savedir, imgName+'.jpg')
      # if os.path.exists(imgname)==False:
      #     continue
      shutil.copy(imgname,newimg)
      if line==None:
        break

def findImgFromTxtdir():
    txtdir = '/home/wurui/CLionProjects/SHbank2.0/data/result/20180520/false-result/none'
    imgsavedir = "/home/wurui/CLionProjects/SHbank2.0/data/img/20180520/false-none"
    count=0
    for txtfile in os.listdir(txtdir):
        count+=1
        f = open(os.path.join(txtdir, txtfile))
        line = f.readline()
        line = line.split(' ')[0]
        imgname = line
        imgname=imgname.strip(' ')
        print(imgname.split('/')[-1])
        newimg = os.path.join(imgsavedir, str(count)+'.jpg')
        print(imgname)
        shutil.copy(imgname, newimg)
        if line == None:
            break

def rename():
    imgdir = '/home/wurui/Desktop/dz/value'

    index = 38;
    for img in os.listdir(imgdir):
        oldname = os.path.join(imgdir, img)
        newname = os.path.join(imgdir, img[0:-4]+'.jpg')
        os.rename(oldname, newname)
        index+=1
        print(index)

def findSameFile():
    xml1 = '/home/wurui/gitREPO/ocr-nameplates-cuizhou/img/audi/制造年月'
    xml2 = '/home/wurui/gitREPO/ocr-nameplates-cuizhou/img/audi/整车型号'
    xml3 = '/home/wurui/gitREPO/ocr-nameplates-cuizhou/data/cnnInputEnhance/xml'
    xml4 = '/home/wurui/gitREPO/ocr-nameplates-cuizhou/data/cnnInputEnhance/xml-rare'
    img = '/media/wurui/WorkSpace/OCR/CarBrandData/汽车名牌/audi596-2'
    savedir = '/home/wurui/Desktop/audi/select'
    files1 = []
    common = []
    # [files1.append(f[0:-4]) for f in os.listdir(xml1)]
    [files1.append(f[0:-4]) for f in os.listdir(xml2)]
    # [files1.append(f[0:-4]) for f in os.listdir(xml3)]
    # [files1.append(f[0:-4]) for f in os.listdir(xml4)]
    count=0
    for f in os.listdir(img):
        if files1.__contains__(f[0:-4])==True:
            # if count%3==1:
            shutil.copy(os.path.join(img,f), os.path.join(savedir,f))
            count+=1
            print(f,' ',count)


def selectFiles():
    # findImgFromTxtdir()
    # rename()
    dir = '/home/wurui/dl_rpository/pytorch-CycleGAN-and-pix2pix-master/datasets/idcard/A/imga'
    fromdir = '/media/wurui/WorkSpace/OCR/CarBrandData/dazhong/train-key/dg-rare'
    # xml = '/media/wurui/WorkSpace/OCR/CarBrandData/lincon/Annotations'
    saveimg = '/home/wurui/dl_rpository/pytorch-CycleGAN-and-pix2pix-master/datasets/idcard/A/val'
    # savexml = '/media/wurui/WorkSpace/OCR/CarBrandData/lincon/CarBrandLiconKey2/xml1'
    count=0
    for f in os.listdir(dir):
        count+=1
        if(count%12!=6):
            continue
        # shutil.move(os.path.join(dir, f), os.path.join(saveimg, f))
        shutil.move(os.path.join(dir,f), os.path.join(saveimg, f))
        print(f)



def mergeImages():
    dir1 = '/media/wurui/WorkSpace/OCR/CarBrandData/binli/bl41'
    dir2 = '/media/wurui/WorkSpace/OCR/CarBrandData/binli/bl50'
    dir3 = '/media/wurui/WorkSpace/OCR/CarBrandData/binli/bl92'
    dir4 = '/media/wurui/WorkSpace/OCR/CarBrandData/binli/bl115'
    savedir = '/media/wurui/WorkSpace/OCR/CarBrandData/binli/JPEGImages'
    dirs = [dir1, dir2, dir3, dir4]
    fileNames = []
    for dir in dirs:
        for f in os.listdir(dir):
            if fileNames.__contains__(f[0:-4]):
                shutil.copy(os.path.join(dir, f), os.path.join(savedir, 'A'+f[0:-4]+'.jpg'))
            else:
                shutil.copy(os.path.join(dir, f), os.path.join(savedir, f[0:-4] + '.jpg'))
            print(f)


def rename():
    dir = '/media/wurui/WorkSpace/OCR/CarBrandData/汽车名牌/audi596-v'
    count = 108
    for f in os.listdir(dir):
        os.rename(os.path.join(dir,f), os.path.join(dir, str(count)+'.jpg'))
        count += 1

def movefiles():
    root = '/media/wurui/WorkSpace/OCR/CarBrandData/audi/ad415'
    save = '/media/wurui/WorkSpace/OCR/CarBrandData/audi/img1'

    for path, dirs, files in os.walk(root):
        for name in files:
            old = os.path.join(path, name)
            shutil.copy(old, os.path.join(save,name))
            print(old)

if __name__ == '__main__':
    # findImgFromTxtList()
    # selectFiles()
    # rename()
    # movefiles()
    findSameFile()
    # mergeImages()