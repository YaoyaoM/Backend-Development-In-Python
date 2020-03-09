from flask_sqlalchemy import SQLAlchemy

db1 = SQLAlchemy()

class Post(db1.Model):
    __tablename__= 'post'
    id=db1.Column(db1.Integer, primary_key=True)
    text=db1.Column(db1.String, nullable=False)
    username=db1.Column(db1.String, nullable=False)
    comments = db1.relationship('Comment', cascade= 'delete')

    def __init__(self, **kwargs):
        self.text = kwargs.get('text', '')
        self.username = kwargs.get('username', '')
    
    def serialize(self):
        return {
            'id': self.id,
            'score': 0,
            'text': self.text,
            'username': self.username
        }

class Comment(db1.Model):
    __tablename__= 'comment'
    id=db1.Column(db1.Integer, primary_key=True)
    text = db1.Column(db1.String, nullable=False)
    username=db1.Column(db1.String, nullable=False)
    post_id=db1.Column(db1.Integer, db1.ForeignKey('post.id'), nullable=False)

    def __init__(self, **kwargs):
        self.text = kwargs.get('text', '')
        self.username = kwargs.get('username', '')
        self.post_id=kwargs.get('post_id')
    
    def serialize(self):
        return {
            'id': self.id,
            'score': 0,
            'text': self.text,
            'username': self.username
        }

