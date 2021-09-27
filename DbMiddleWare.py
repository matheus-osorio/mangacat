import psycopg2
from env import env

conn = psycopg2.connect(
    host = env['host'],
    database = env['database'],
    user = env['user'],
    password = env['password'],
    options = env['options']
)

cursor = conn.cursor()

class DbMiddleware:
    def __init__(self):
        pass
    def query(self,query):
        print(query)
        cursor.execute(query)
        return self
    
    def fetch(self):
        return cursor.fetchall()
    
    def commit(self):
        conn.commit()

    def insertManga(self,image, description, url):
        query = f''' 
        insert into manga (image, description, url)
        values (
            '{image}',
            '{description}',
            '{url}'
        )
        on conflict do nothing
        returning "id"
        '''
        return self.query(query)

    def insertAuthor(self, name):
        query = f''' 
        insert into author ("name")
            values (
            '{name}'
            )
            on conflict do nothing

            returning "id"
        '''
        return self.query(query)

    def insertMangaAuthor(self, mangaId,authorId):
        query = f''' 
        insert into author_x_manga (mangaId, authorId)
        values (
            {mangaId},
            {authorId}
        )
        '''
        print(query)
        return self.query(query)

    def insertGenre(self, genre):
        query = f'''
        insert into genre(genre)
        values 
        ('{genre}')
        on conflict do nothing
        returning "id"
        '''
        return self.query(query)
    
    def insertMangaGenre(self, mangaId, genreId):
        query = f'''
        insert into manga_x_genre(mangaId, genreId)
        values
        (
        {mangaId},
        {genreId}
        )
        '''
        return self.query(query)

    def insertTitle(self,title,mangaId,main):
        query = f'''
        insert into title(title, main, mangaId)
        values (
        '{title}',
        {main},
        {mangaId}
        )

        on conflict do nothing
        '''
        return self.query(query)

    def insertChapters(self, name, url, mangaId):
        query = f''' 
        insert into chapters (chapterName, url, mangaId)
        values (
        '{name}',
        '{url}',
        {mangaId}
        )
        on conflict do nothing
        returning "id"
        '''
        return self.query(query)

    def getManga(self, params):
        query = f''' 
        select * from manga
        {'where' if params != {} else ''}
        {f"url = '{params['url']}'" if 'url' in params else ''}
        {f"name = '{params['name']}'" if 'name' in params else ''}
        {f"id = '{params['id']}'" if 'id' in params else ''}
        '''
        return self.query(query)
    
    def getAuthor(self, params):
        query = f'''
        select * from author
        {'where' if params != {} else ''}
        {f"name = '{params['name']}'" if 'name' in params else ''}
        '''

        return self.query(query)

    def getGenre(self, params):
        query = f'''
        select * from genre
        {'where' if params != {} else ''}
        {f"genre = '{params['genre']}'" if 'genre' in params else ''}
        '''
        return self.query(query)
    
    
