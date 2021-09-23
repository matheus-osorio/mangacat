import requests
import shutil

class Image_Getter:
    def __init__(self, img, name, directory = '/', extension = 'jpg'):
        self.img = img
        self.name = name
        self.directory = directory
        self.extension = extension
    
    def mangakalot(self):
        headers = {
            'referer': 'https://readmanganato.com/'
        }
        res = requests.get(self.img, headers=headers, stream=True)
        if res.status_code != 200:
            return False
        filename = f'{self.directory}{self.name}.{self.extension}'
        with open(filename,'wb') as img:
            shutil.copyfileobj(res.raw, img)
