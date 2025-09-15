from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    avatar_url = db.Column(db.String(500), default='/static/avatar.png')

    animes_favoritos = db.relationship(
        'FavoriteAnime',
        backref='usuario',
        lazy=True,
        overlaps="user,favoritos"
    )

    posts = db.relationship(
        'Post',
        backref='usuario',
        lazy=True,
        overlaps="user,posts"
    )

    def get_id(self):
        return str(self.id)


class FavoriteAnime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150))
    imagen = db.Column(db.String(1000))
    reseña = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    usuario = db.relationship(
        'User',
        backref='animes_favoritos',
        overlaps="user,favoritos"
    )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    usuario = db.relationship(
        'User',
        backref='posts',
        overlaps="user,posts"
    )
