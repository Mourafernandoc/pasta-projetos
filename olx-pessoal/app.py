from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = 'static/imagens'
db = SQLAlchemy(app)

# Modelo de dados
class Anuncio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), unique=True, nullable=False)
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

@app.route('/criar_anuncio', methods=['GET' , 'POST'])
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
        db.session.add(novo_anuncio)
        db.session.commit()

        return redirect(url_for('listar_anuncios'))
    
    return render_template('criar_anuncio.html')

def salvar_imagem(arquivo):
    nome_arquivo = secure_filename(arquivo.filename)
    caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
    arquivo.save(caminho_arquivo)
    return nome_arquivo

if __name__ == '__main__':
    app.run(debug=True)
