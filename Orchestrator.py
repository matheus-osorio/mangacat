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

    def getManga(self,url):
        MG = Manga_Getter(url)
        chapters = MG.mangakalot()
        last_chapter = chapters[-1]['href']
        if not self.isNewEpisode(last_chapter):
            return
        
        CG = Chapter_Getter(last_chapter)
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
        self.callImageGluer()
        

    def isNewEpisode(self,chapter):
        return True


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

    def callImageGluer(self, params = {'jumpSize': 10}):

        size = len(os.listdir('imgs'))
        imglu = Image_Gluer(size,directory='./imgs/',  **params)
        imglu.glue()
        parts = len(os.listdir('parts'))
        os.system('rm ./imgs/*')
        if parts > 1:
            
            for part in range(1,parts + 1):
                os.system(f'mv ./parts/part{part}.png ./imgs/{part-1}.png')

            self.callImageGluer({'jumpSize': 2, 'extension': 'png', 'useThreads': False})


        
        


orc = Orchestrator()
orc.getManga(url)