import requests
from bs4 import BeautifulSoup as BS


class Chapter_Getter:
    def __init__(self, chapter, threadMax = 5):
        self.chapter = chapter
        self.threadMax = threadMax
    
    def mangakalot(self):
        res = requests.get(self.chapter)
        if res.status_code != 200:
            return False
        html = BS(res.text, features="html.parser")
        imgs = html.find('div', {'class': 'container-chapter-reader'}).findAll('img')
        imgs = [img['src'] for img in imgs]
        return imgs

