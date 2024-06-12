from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin, LoginManager, Login_user, Login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, session
import logging
import os


app = Flask(__name__)

#configuração de logs
logging.basicConfig(filename='system.log' , level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

#uso de logging
logging.info('aplicação iniciada')

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = 'static/imagens'
db = SQLAlchemy(app)
migrate = Migrate(app, db)#inicializa Flask-Migrate

#configuração do login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#modelo de usuario

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Modelo de dados
class Anuncio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100),  nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    foto = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"Anuncio('{self.titulo}', '{self.descricao}', '{self.preco}', '{self.foto}')"

# Rotas

@app.route('/register', methods=['GET','POST'])
def register():
    if request.methode == 'POST':
        username = request.form.get['username']
        email = request.form.get['email']
        password = request.form.get['password']

        #verifica se o usuario ja existe
        if Usuario.query.filter_by(username=username).first():
            flash('Username já existe. Por favor, escolha outro.', 'danger')
            return redirect(url_for('register'))
        
        #criar o novo usuario
        novo_usuario = Usuario(username=username, email=email)
        novo_usuario.set_password(password)
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Registro bem-sucedido! Você pode fazer login agora.','sucess')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get['username']
        password = request.form.get['password']

        usuario = Usuario.query.filter_by(username=username).first()

        if usuario is None or not usuario.check_password(password):
            flash('Nome de usuario ou senha incorretos.','danger')
            return redirect(url_for('login'))
        
        login_user(usuario)
        flash('Login bem-sucedido!', 'sucess')
        return redirect(url_for('listar_anuncios'))
    
    return render_template('login.html')

@app.route('/logout')
@Login_required
def logout():
    logout_user()
    flash('Você foi desconectado.','info')
    return redirect(url_for('login'))


@app.route('/')
def index():
    return 'Olá, mundo! Este é o meu clone da OLX.'

@app.route('/anuncios')
def listar_anuncios():
    anuncios = Anuncio.query.all()
    return render_template('anuncios.html', anuncios=anuncios)

@app.route('/test')
def test():
    return 'Teste de rota'

@app.route('/criar_anuncio', methods=['GET', 'POST'])
def criar_anuncio():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        preco = request.form['preco']
        foto = None

        if 'foto' in request.files:
            arquivo = request.files['foto']
            if arquivo.filename != '':
                foto = salvar_imagem(arquivo)

        novo_anuncio = Anuncio(titulo=titulo, descricao=descricao, preco=preco, foto=foto)
        try:
            db.session.add(novo_anuncio)
            db.session.commit()
            logging.info(f'Anuncio criado: {titulo}')
            return redirect(url_for('listar_anuncios'))
        except IntegrityError:
            db.session.rollback()
            alerta = 'Já existe um anúncio com esse título'
            return render_template('criar_anuncio.html', alerta=alerta)

    return render_template('criar_anuncio.html')


@app.route('/editar_anuncio/<int:id>', methods=['GET', 'POST'])
def editar_anuncio(id):
    anuncio = Anuncio.query.get_or_404(id)
    if request.method == 'POST':
        anuncio.titulo = request.form['titulo']
        anuncio.descricao = request.form['descricao']
        anuncio.preco = request.form['preco']
        
        if 'foto' in request.files:
            arquivo = request.files['foto']
            if arquivo.filename != '':
                anuncio.foto = salvar_imagem(arquivo)

        try:
            db.session.commit()
            return redirect(url_for('listar_anuncios'))
        except IntegrityError:
            db.session.rollback()
            alerta = 'Já existe um anúncio com esse título'
            return render_template('editar_anuncio.html', anuncio=anuncio, alerta=alerta)

    return render_template('editar_anuncio.html', anuncio=anuncio)



@app.route('/deletar_anuncio/<int:id>', methods=['POST'])
def deletar_anuncio(id):
    anuncio = Anuncio.query.get_or_404(id)
    db.session.delete(anuncio)
    db.session.commit()
    return redirect(url_for('listar_anuncios'))

@app.route('/gerenciar_anuncios')
def gerenciar_anuncios():
    anuncios = Anuncio.query.all()
    return render_template('gerenciar_anuncios.html', anuncios=anuncios)

@app.route('/ver_logs')
def ver_logs():
    try:
        with open('system.log', 'r') as file:
            conteudo = file.readlines()
        logs = conteudo    
    except FileNotFoundError:
        logs = ["Log file not found."]
    return render_template('logs.html', logs=logs)

@app.route('/controle')
def controle():
    return render_template('controle.html')

if __name__ == '__main__':
    app.run(debug=True)

def salvar_imagem(arquivo):
    nome_arquivo = secure_filename(arquivo.filename)
    caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
    arquivo.save(caminho_arquivo)
    return nome_arquivo

if __name__ == '__main__':
    app.run(debug=True)
