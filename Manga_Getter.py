import requests
from bs4 import BeautifulSoup as BS

class Manga_Getter:
    def __init__(self,manga):
        self.manga = manga
    
    def mangakalot(self):
        res = requests.get(self.manga)
        parsed = BS(res.text, features="html.parser")
        nodes = parsed.findAll('a', {'class': 'chapter-name text-nowrap'})
        chapters = [{'name': node.text, 'href': node['href']} for node in nodes]
        chapters = chapters[::-1]
        return chapters

