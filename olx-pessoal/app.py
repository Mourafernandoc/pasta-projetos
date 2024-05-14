from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Olá, mundo! Este é o meu clone da OLX.'

if __name__ == '__main__':
    app.run(debug=True)


from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #caminho para o banco de dados
db = SQLAlchemy(app)

class Anuncio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    foto = db.Column(db.String(20), nullable=False, default='default.jpg') #arquivo da foto

    def __repr__(self):
        return f"Anuncio ('{self.titulo}' , '{self.descricao}' , '{self.preco}' , '{self.foto}')"