from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
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

if __name__ == '__main__':
    app.run(debug=True)
