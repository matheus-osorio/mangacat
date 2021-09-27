from Manga_Getter import Manga_Getter
from Chapter_Getter import Chapter_Getter
from Image_Getter import Image_Getter
from Image_Gluer import Image_Gluer
from threading import Thread
import time
import os

url = 'https://manganato.com/manga-kq961851'

class Orchestrator:
    def __init__(self, threadMax = 5):
        self.threadMax = threadMax

    def getChapter(self, url):
        MG = Manga_Getter(url)
        return MG.mangakalot()
        
    def wipeDirectory(self,dir):
        os.system(f'rm -r {dir}/*')

    def moveFiles(self,origin,destiny):
        os.system(f'mv {origin}/* {destiny}')

    def getManga(self,url, name='result'):
        self.wipeDirectory('./imgs')
        self.wipeDirectory('./parts')
        CG = Chapter_Getter(url)
        imgs = CG.mangakalot()
        calls = []
        for img in enumerate(imgs):
            def call(name, url):  
                def img_call():
                    IG = Image_Getter(url, str(name), './imgs/')
                    IG.mangakalot()
                return img_call
            calls.append(call(img[0], img[1]))
        
        self.calls = calls
        self.makeCalls(self.callImages)
        self.callImageGluer(name)
        self.moveFiles('./parts', './chapters')


    def makeCalls(self, func):
        threads = []
        for i in range(self.threadMax):
            t = Thread(target=func)
            t.start()
            threads.append(t)
        
        for thread in threads:
            thread.join()
    

    def callImages(self):
        while len(self.calls) > 0:
            call = self.calls[0]
            self.calls = self.calls[1:]
            call()

    def callImageGluer(self, name):
        imgFolderSize = len(os.listdir('./imgs/'))
        imgList = []
        for i in range(imgFolderSize):
            imgList.append(str(i))
        
        imglu = Image_Gluer(imgList, f'./parts/{name}.png')

        imglu.glue()
        