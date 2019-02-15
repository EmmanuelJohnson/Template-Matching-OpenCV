import cv2
import numpy as np
import math
import imutils
import glob
import os

DEBUG = False
THRESHOLD = 0.41

#Read the image using opencv
def get_image(path):
    return cv2.imread(path)

#Read the image in gray scale using opencv
def get_image_gray(path):
    return cv2.imread(path,0)

#Show the resulting image
def show_image(name,image):
    cv2.imshow(name,image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#Save the resulting image
def save_image(name,image):
    cv2.imwrite(name,image) 

#Add Gaussian Blur to the given image
def addGaussian(img,size):
    return cv2.GaussianBlur(img, (size, size), 1)

#Add Laplacian Edge Detection to the given image
def addLaplacian(img):
    return cv2.Laplacian(img,cv2.CV_32F)

#Add Sobel Edge Detection to the given image
def addSobel(img,name):
    sobelx = cv2.Sobel(img,cv2.CV_32F,1,0,ksize=3)
    sobely = cv2.Sobel(img,cv2.CV_32F,0,1,ksize=3)
    save_image('sobelx '+name+'.png',sobelx)
    save_image('sobely '+name+'.png',sobely)
    return sobelx, sobely

#Match template with the given image
def match(baseImage,template):
    matched = cv2.matchTemplate(baseImage, template, cv2.TM_CCOEFF_NORMED)
    return matched

def main():
    imageSets = {
        "positives":{
            "path": "input_images/pos_*.jpg",
            "template": "template.png"
        },
        "negatives":{
            "path": "input_images/neg_*.jpg",
            "template": "template.png"
        },
        "bonus_positives_1":{
            "path": "input_images/task3_bonus/t1_*.jpg",
            "template": "input_images/task3_bonus/t1.jpg"
        },
        "bonus_positives_2":{
            "path": "input_images/task3_bonus/t2_*.jpg",
            "template": "input_images/task3_bonus/t2.jpg"
        },
        "bonus_positives_3":{
            "path": "input_images/task3_bonus/t3_*.jpg",
            "template": "input_images/task3_bonus/t3.jpg"
        },
        "bonus_negatives":{
            "path": "input_images/task3_bonus/neg_*.jpg",
            "template": "template.png"
        }
    }

    for iS,iSV in imageSets.items():
        spath = "output_images/"+iS+"_output"
        if not os.path.exists(spath):
                os.makedirs(spath)
        for ip in glob.glob(iSV["path"]):

            tFileName = iSV["template"].split("/")[-1:][0]
            template = get_image_gray(iSV["template"])
            org_tempH, org_tempW = template.shape[0],template.shape[1]

            fileName = ip.split("/")[-1:][0]
            baseCImage = get_image(ip)
            baseImage = get_image_gray(ip)
            lBaseImg = baseImage
            lBaseImg = addGaussian(lBaseImg, 3)
            lBaseImg = addLaplacian(lBaseImg)

            print('__Matching '+fileName+' with '+tFileName+"__")

            if DEBUG:
                save_image(spath+"/lap_"+fileName,lBaseImg)

            optMaxVal,optMaxLoc,optMaxLocEnd = 0,0,0

            scalingFactors = np.linspace(0.6, 1.0, 25)[::-1]
            isDetected = False

            for scale in scalingFactors:
                
                resizedTemplate = template
                resizeAmount = int(resizedTemplate.shape[1] * scale)
                resizedTemplate = imutils.resize(resizedTemplate, width = resizeAmount)

                res_tempH, res_tempW = resizedTemplate.shape[0],resizedTemplate.shape[1]

                gtemplate = addGaussian(resizedTemplate,3)
                ltemplate = addLaplacian(gtemplate)

                result = match(lBaseImg, ltemplate)

                minMaxRes = cv2.minMaxLoc(result)
                maxVal,maxLoc = minMaxRes[1],minMaxRes[3]
                
                if maxVal > optMaxVal:
                    optMaxVal,optMaxLoc = maxVal, maxLoc
                    optMaxLocEnd = (int(optMaxLoc[0]+res_tempW),int(optMaxLoc[1]+res_tempH))
                    isDetected = True
                    if DEBUG:
                        cv2.rectangle(baseCImage, maxLoc, optMaxLocEnd, (0, 0, 255), 1)
            
            if isDetected and maxVal>THRESHOLD:
                print('__Matched Template Location : '+str(optMaxLoc)+" "+str(optMaxLocEnd)+"__")
                center = (int((optMaxLoc[0]+optMaxLocEnd[0])/2),int((optMaxLoc[1]+optMaxLocEnd[1])/2))
                dist = int(int(np.linalg.norm(np.array(optMaxLoc)-np.array(optMaxLocEnd)))/2)
                cv2.circle(baseCImage, center, dist, (255, 0, 0), thickness=2, lineType=8, shift=0)
            save_image(spath+"/output_"+fileName,baseCImage)

if __name__ == '__main__':
    main()