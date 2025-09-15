from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.models import User, db, FavoriteAnime, Post # Asegúrate de importar db desde models.py
from app.auth import auth
from flask_login import login_required, current_user
from app.utils import buscar_anime

app = Flask(__name__)

# Configuración de la app
app.config['SECRET_KEY'] = 'anime-secret-key'
import os
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')


# Inicializar extensiones
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


# Cargar usuario para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registrar blueprint de autenticación
app.register_blueprint(auth)

# Ruta principal
from flask_login import current_user

@app.route("/")
def home():
    return render_template("home.html", user=current_user)

@app.route("/init/<clave>")
def init_db(clave):
    if clave != "tu_clave_secreta":
        return "⛔ Clave incorrecta", 403
    db.create_all()
    return "✅ Base de datos creada correctamente."


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    resultado = None
    if request.method == "POST":
        nombre_anime = request.form.get("anime")
        resultado = buscar_anime(nombre_anime)
    return render_template("profile.html", user=current_user, resultado=resultado)

@app.route("/add_favorite", methods=["POST"])
@login_required
def add_favorite():
    titulo = request.form.get("titulo")
    imagen = request.form.get("imagen")
    reseña = request.form.get("reseña")

    nuevo_favorito = FavoriteAnime(
        titulo=titulo,
        imagen=imagen,
        reseña=reseña,
        user_id=current_user.id
    )
    db.session.add(nuevo_favorito)
    db.session.commit()

    return redirect(url_for("profile"))


@app.route("/delete_favorite/<int:id>", methods=["POST"])
@login_required
def delete_favorite(id):
    favorito = FavoriteAnime.query.get_or_404(id)
    if favorito.user_id == current_user.id:
        db.session.delete(favorito)
        db.session.commit()
    return redirect(url_for("profile"))

@app.route("/edit_favorite/<int:id>", methods=["GET", "POST"])
@login_required
def edit_favorite(id):
    favorito = FavoriteAnime.query.get_or_404(id)
    if favorito.user_id != current_user.id:
        return redirect(url_for("profile"))

    if request.method == "POST":
        favorito.reseña = request.form.get("reseña")
        db.session.commit()
        return redirect(url_for("profile"))

    return render_template("edit_favorite.html", favorito=favorito)

@app.route("/feed", methods=["GET", "POST"])
@login_required
def feed():
    if request.method == "POST":
        contenido = request.form.get("contenido")
        if contenido:
            nuevo_post = Post(contenido=contenido, user_id=current_user.id)
            db.session.add(nuevo_post)
            db.session.commit()
            return redirect(url_for("feed"))

    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("feed.html", posts=posts)

@app.route("/buscar", methods=["GET", "POST"])
@login_required
def buscar():
    resultado = None
    if request.method == "POST":
        nombre_anime = request.form.get("anime")
        resultado = buscar_anime(nombre_anime)
    return render_template("buscar.html", resultado=resultado)

@app.route("/usuario/<int:id>")
@login_required
def ver_usuario(id):
    usuario = User.query.get_or_404(id)
    return render_template("ver_usuario.html", usuario=usuario)



