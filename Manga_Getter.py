import requests
from bs4 import BeautifulSoup as BS

class Manga_Getter:
    def __init__(self,manga):
        self.manga = manga

    def makeSQLReady(self,text):
        return text.replace("'", "''")

    def getChapters(self):
        nodes = self.page.findAll('a', {'class': 'chapter-name text-nowrap'})
        chapters = [{'name': self.makeSQLReady(node.text), 'href': node['href']} for node in nodes]
        chapters = chapters[::-1]
        return chapters
    
    def getTitle(self):
        parentNode = self.page.find('div', {'class': 'story-info-right'})
        title = parentNode.find('h1')
        return self.makeSQLReady(title.text)
    
    def getImage(self):
        return self.page.find('span', {'class': 'info-image'}).find('img', {'class': 'img-loading'})['src']

    def getInfos(self):
        parentNode = self.page.find('table', {'class': 'variations-tableInfo'})
        body = parentNode.find('tbody')
        lines = body.findAll('tr')
        lines = [line.find('td', {'class': 'table-value'}) for line in lines]
        obj = {
            'alternative': [self.makeSQLReady(text) for text in lines[0].find('h2').text.split(';')],
            'author': [self.makeSQLReady(a.text) for a in lines[1].findAll('a')],
            'status': self.makeSQLReady(lines[2].text),
            'genres': [self.makeSQLReady(a.text) for a in lines[3].findAll('a')]
        }
        
        
        return obj

    def getDescription(self):
        description = self.page.find('div', {'id': 'panel-story-info-description'}).text.replace('\nDescription :\n', '')
        return self.makeSQLReady(description)

    def mangakalot(self):
        res = requests.get(self.manga)
        parsed = BS(res.text, features="html.parser")
        self.page = parsed
        return {
            'title': self.getTitle(),
            'image': self.getImage(),
            'chapters': self.getChapters(),
            'infos': self.getInfos(),
            'description': self.getDescription()
        }

