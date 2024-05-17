from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError

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
