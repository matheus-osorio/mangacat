import cv2
import numpy as np
import os
import math
from threading import Thread


class Image_Gluer:
    EQUALIZE_FIRST = 0
    EQUALIZE_DURING = 1

    RESIZE_METHOD = 0
    BLACKBAR_METHOD = 1
    WHITEBAR_METHOD = 2
    def __init__(self, imgList, destinyImage, originFolder = './imgs', extension= 'jpg', strategy = 0, method = 0):
        self.list = imgList
        self.destiny = destinyImage
        self.originFolder = originFolder
        self.extension = extension
        self.strategy = strategy
        self.method = 0
    def glue(self):
        print('Starting glue process')
        if self.strategy == self.EQUALIZE_FIRST:
            self.equalizeAllImages()
        
        self.glueImages()
    
    def moutImage(self, name):
        return f'{self.originFolder}/{name}.{self.extension}'

    def equalizeAllImages(self):
        print('Equaling image before gluing')
        maxSize = 0
    
        for img_name in self.list:
            img = cv2.imread(self.moutImage(img_name))
            maxSize = max(maxSize, img.shape[1])
        
        for img_name in self.list:
            name = self.moutImage(img_name)
            print(f'Equalizing {name}')
            img = cv2.imread(name)
            img = self.extendImage(img,(0, maxSize))
            self.saveImage(img, name)
        
    def extendImage(self,image, dimensions):
        shape = image.shape

        if self.method != self.RESIZE_METHOD:
            diff = (dimensions[0] - shape[0], dimensions[1] - shape[1])

            if diff[0] > 0:
                image = self.extendVertically(image, diff[0])
            
            if diff[1] > 0:
                image = self.extendHorizontally(image,diff[1])
        else:
            
            image = self.resizeImage(image, dimensions[1])

        
        return image

    def resizeImage(self, image, height):
        shape = image.shape
        percentage = height / shape[1]
        dimensions = (height, round(shape[0] * percentage))
        return cv2.resize(image, dimensions, interpolation = cv2.INTER_AREA)


    def extendVertically(self, image, diff):
        width = image.shape[1]
        color = [0,0,0]
        if self.method != self.BLACKBAR_METHOD:
            color = [255,255,255]

        before_len = math.ceil(diff/2)
        after_len = math.floor(diff/2)
        line = [color for i in range(width)]

        before = [line for i in range(before_len)]
        after = [line for i in range(after_len)]
        before = np.array(before)
        after = np.array(after)
        if diff == 1:
            return np.concatenate((before,image), axis=0)

        return np.concatenate((before,image,after), axis=0)
    
    def extendHorizontally(self,image,diff):
        height = image.shape[0]
        color = self.filling
        before_len = math.ceil(diff/2)
        after_len = math.floor(diff/2)

        before_line = [color for i in range(before_len)]
        after_line = [color for i in range(after_len)]
        before = np.array([before_line for i in range(height)])
        after = np.array([after_line for i in range(height)])
        if diff == 1:
            return np.concatenate((before,image), axis=1)

        return np.concatenate((before,image,after), axis=1)
    
    def glueImages(self):
        total = None

        for img_name in self.list:
            name = self.moutImage(img_name)
            print(f'Gluing Image: {name}')
            img = cv2.imread(name)
            if not isinstance(total, np.ndarray):
                total = img
                continue
            
            total = self.prepAndGlue(total, img)
        
        self.saveImage(total, self.destiny)
        print(f'Created result Image: {self.destiny}')
    
    def prepAndGlue(self, total, image):
        if self.strategy != self.EQUALIZE_FIRST:
            image = self.extendImage(image, (0, total.shape[1]))
        
        return np.concatenate((total, image), axis=0)
    
    def saveImage(self, image, name):

        cv2.imwrite(name,image)

