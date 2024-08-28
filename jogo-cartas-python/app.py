# app.py (revisado)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from jogo import Jogo
from jogador import Jogador
from carta import Carta
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
socketio = SocketIO(app)

# Criar jogadores e cartas para o exemplo
jogador1 = Jogador("Jogador 1")
jogador2 = Jogador("Jogador 2")

jogador1.definir_oponente(jogador2)
jogador2.definir_oponente(jogador1)

# Adicionar cartas ao deck de cada jogador
for i in range(10):
    jogador1.adicionar_carta_ao_deck(Carta(f"Carta {i+1}", random.randint(1, 10), random.randint(1, 10), random.randint(1, 10), False))
    jogador2.adicionar_carta_ao_deck(Carta(f"Carta {i+11}", random.randint(1, 10), random.randint(1, 10), random.randint(1, 10), False))

# Comprar as cartas iniciais para os jogadores
for _ in range(5):
    jogador1.comprar_carta()
    jogador2.comprar_carta()

jogo = Jogo(jogador1, jogador2)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('cartas_iniciais', {'cartas': {
        'jogador1': [str(c) for c in jogo.jogador1.mao],
        'jogador2': [str(c) for c in jogo.jogador2.mao]
    }})

@socketio.on('iniciar_batalha')
def handle_battle(data):
    try:
        carta_nome = data.get('carta')
        if not carta_nome:
            raise ValueError("Nenhuma carta selecionada")

        print('Carta recebida:', carta_nome)

        # Buscar a carta selecionada na mão do jogador do turno atual
        carta_selecionada = next((c for c in jogo.turno.mao if str(c) == carta_nome), None)
        if not carta_selecionada:
            raise ValueError(f"Carta '{carta_nome}' não encontrada na mão do jogador {jogo.turno.nome}")

        # Remover a carta selecionada da mão do jogador atual
        jogo.turno.mao.remove(carta_selecionada)

        # Selecionar a carta do oponente (primeira carta da mão como exemplo)
        carta_adversario = jogo.turno.oponente().mao.pop(0)

        print(f"{jogo.turno.nome} joga {carta_selecionada}")
        print(f"Oponente joga {carta_adversario}")

        resultado = jogo.comparar_cartas(carta_selecionada, carta_adversario)

        # Emitir o resultado da batalha e as cartas restantes
        emit('resultado_batalha', {'resultado': resultado, 'cartas': {
            'jogador1': [str(c) for c in jogo.jogador1.mao],
            'jogador2': [str(c) for c in jogo.jogador2.mao]
        }})
    except Exception as e:
        print(f"Erro ao iniciar batalha: {e}")
        emit('erro', {'mensagem': str(e)})

@socketio.on('reiniciar_batalha')
def handle_restart():
    print("Reiniciando batalha...")
    # Recarregar as cartas iniciais ou redefinir o jogo como necessário
    for _ in range(5):
        jogo.jogador1.comprar_carta()
        jogo.jogador2.comprar_carta()
    emit('cartas_iniciais', {'cartas': {
        'jogador1': [str(c) for c in jogo.jogador1.mao],
        'jogador2': [str(c) for c in jogo.jogador2.mao]
    }})

if __name__ == '__main__':
    socketio.run(app, debug=True)
