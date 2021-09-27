from DbMiddleWare import DbMiddleware

from Orchestrator import Orchestrator

class Middleware:
    def __init__(self):
        self.orch = Orchestrator()
        self.db = DbMiddleware()

    def getMangaInfos(self, params):
        return self.db.getManga(params).fetch()
    
    def newManga(self, url):
        obj = self.getChapterList(url)
        mangaId = self.db.insertManga(obj['image'], obj['description'], url).fetch()
        
        if len(mangaId) == 0:
            mangaId = self.db.getManga({'url': url}).fetch() 
        
        mangaId = mangaId[0][0]

        for author in obj['infos']['author']:
            authorId = self.db.insertAuthor(author).fetch()
            if len(authorId) == 0:
                authorId = self.db.getAuthor({'name': author}).fetch()
            authorId = authorId[0][0]
            self.db.insertMangaAuthor(mangaId, authorId)
        
        for gender in obj['infos']['genres']:
            genreId = self.db.insertGenre(gender).fetch()

            if len(genreId) == 0:
                genreId = self.db.getGenre({'genre': gender}).fetch()
            
            genreId = genreId[0][0]

            self.db.insertMangaGenre(mangaId,genreId)
    
        self.db.insertTitle(obj['title'], mangaId, 'true')

        for title in obj['infos']['alternative']:
            self.db.insertTitle(title,mangaId,'false')
        
        for chapter in obj['chapters']:
            self.db.insertChapters(chapter['name'], chapter['href'], mangaId)
        
        self.db.commit()

    def prepImageName(self,name):
        remove = [':',',']
        for char in remove:
            name = name.replace(char, '')

        while '  ' in name:
            name = name.replace('  ',' ')
        
        replace = [
            [' ','_']
        ]
        
        for char in replace:
            name = name.replace(char[0],char[1])
        
        return name

    def getChapterList(self,url):
        return self.orch.getChapter(url)

    def parseChapter(self,chapter, name = 'result'):
        self.orch.getManga(chapter, name)



mid = Middleware()




