from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    avatar_url = db.Column(db.String(1000), default='/static/avatar.png')
    favoritos = db.relationship('FavoriteAnime', backref='user', lazy=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class FavoriteAnime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150))
    imagen = db.Column(db.String(1000))
    reseña = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    usuario = db.relationship('User', backref='animes_favoritos')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    usuario = db.relationship('User', backref='posts', overlaps="user,posts")



