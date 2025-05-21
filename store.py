
class Post:
    def __init__(self, id,public_url, photo_url, body,date ,page,title,):
        self.id = id
        self.photo_url = photo_url
        self.body = body
        self.date=date
        self.page=page
        self.title = title 
        self.public_url= public_url

class PostStore:
    def __init__(self):
        self.posts = []

    def add(self, post):
        self.posts.append(post)

    def get_all(self):
        return self.posts[::-1]

        