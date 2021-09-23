import cv2
import numpy as np
import os
from threading import Thread


class Image_Gluer:
    def __init__(self,maxValue, directory = '/', extension = 'jpg', jumpSize = 30, maxThreads = 2, useThreads = True):
        self.maxValue = maxValue
        self.directory = directory
        self.extension = extension
        self.maxThreads = maxThreads
        self.jumpSize = jumpSize
        self.useThreads = useThreads
    
    def glue(self):
        self.spreadIntoParts()
        if self.useThreads:
            self.glueWithThreads()
        else:
            self.glueImage()
    
    def spreadIntoParts(self):
        portions = []
        order = []
        maxValue = self.maxValue
        jumpSize = self.jumpSize
        for i in enumerate(range(0,maxValue, jumpSize)):
            value = []
            name = f'./parts/part{i[0]+1}.png'
            for j in range(i[1], min(i[1]+jumpSize, maxValue)):
                img_name = f'{self.directory}{j}.{self.extension}'
                value.append(img_name)
            obj = {
                'name':name,
                'range': value
            }
            portions.append(obj)  
            order.append(name)    

        self.portions = portions
        self.order = order  
    
    def glueWithThreads(self):
        threads = []
        for i in range(self.maxThreads):
            t = Thread(target=self.glueImage)
            threads.append(t)
            t.start()
        
        for thread in threads:
            t.join()
    
    def glueImage(self):
        while len(self.portions) > 0:
            portion = self.portions[0]
            self.portions = self.portions[1:]
            self.loopThroughImages(portion)
            
    def loopThroughImages(self,portion):
        finalImg = None
        for img_name in portion['range']:
            img = cv2.imread(img_name)
            if not isinstance(finalImg, np.ndarray):
                finalImg = img
            else:
                finalImg = self.glueParts(finalImg,img)
            del img
        cv2.imwrite(portion['name'], finalImg)
        del finalImg
    
    def glueParts(self, finalImg, part):
        if not isinstance(part, np.ndarray):
            return finalImg
        final_length = finalImg.shape[1]
        part_length = part.shape[1]
        diff = final_length - part_length
        if diff > 0:
            part = self.incrementImage(part, diff)
        elif diff < 0:
            finalImg = self.incrementImage(finalImg, -diff)
        
        return np.concatenate((finalImg, part), axis=0)
    
    def incrementImage(self, img, size):
        if size % 2 != 0:
            before = (size + 1)/2
            after = (size -1)/2
        else:
            before = size/2
            after = before
        before = [[0,0,0] for i in range(int(before))]
        after = [[0,0,0] for i in range(int(after))]

        before = np.array(before)
        after = np.array(after)
        lines = []
        for line in img:
            if size > 1:
                newLine = np.concatenate((before,line,after))
            else:
                newLine = np.concatenate((before,line))
            lines.append(newLine)
        return np.array(lines)        
