from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Olá, mundo! Este é o meu clone da OLX.'

if __name__ == '__main__':
    app.run(debug=True)
    