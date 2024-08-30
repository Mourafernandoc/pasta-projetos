# app.py (com logs de depuração adicionados)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from jogo import Jogo
from jogador import Jogador
from carta import Carta
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
socketio = SocketIO(app)

# Criar jogadores e instância do jogo
jogador1 = Jogador("Jogador 1")
jogador2 = Jogador("Jogador 2")
jogador1.definir_oponente(jogador2)
jogador2.definir_oponente(jogador1)
jogo = Jogo(jogador1, jogador2)

# Função para iniciar o jogo
def iniciar_jogo():
    jogador1.mao = []
    jogador2.mao = []
    jogador1.deck = []
    jogador2.deck = []
    
    # Adicionar cartas ao deck de cada jogador
    for i in range(10):
        jogador1.adicionar_carta_ao_deck(Carta(f"Carta {i+1}", random.randint(1, 10), random.randint(1, 10), random.randint(1, 10), False))
        jogador2.adicionar_carta_ao_deck(Carta(f"Carta {i+11}", random.randint(1, 10), random.randint(1, 10), random.randint(1, 10), False))
    
    # Comprar cartas iniciais para ambos os jogadores
    for _ in range(5):
        jogador1.comprar_carta()
        jogador2.comprar_carta()

    jogo.resetar_placar()
    
    # Logs de depuração
    print("Jogo iniciado!")
    print(f"Jogador 1 mão: {[str(c) for c in jogador1.mao]}")
    print(f"Jogador 2 mão: {[str(c) for c in jogador2.mao]}")

# Inicializar o jogo no início
iniciar_jogo()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("Novo cliente conectado. Enviando cartas iniciais...")
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
        
        # O jogador 1 sempre inicia
        carta_selecionada = next((c for c in jogador1.mao if str(c) == carta_nome), None)
        if not carta_selecionada:
            raise ValueError(f"Carta '{carta_nome}' não encontrada na mão do jogador {jogador1.nome}")

        # Retira a carta selecionada da mão do jogador 1
        jogador1.mao.remove(carta_selecionada)

        # O jogador 2 responde com a primeira carta de sua própria mão
        if not jogador2.mao:
            raise ValueError(f"Oponente {jogador2.nome} está sem cartas na mão.")
        
        carta_adversario = jogador2.mao.pop(0)

        resultado = jogo.comparar_cartas(carta_selecionada, carta_adversario)

        vencedor = None
        if "Jogador 1" in resultado:
            vencedor = "Jogador 1"
            jogo.pontos_jogador1 += 1
        elif "Jogador 2" in resultado:
            vencedor = "Jogador 2"
            jogo.pontos_jogador2 += 1

        # Verificar se todas as cartas foram usadas
        if not jogador1.mao and not jogador2.mao:
            if jogo.pontos_jogador1 > jogo.pontos_jogador2:
                vencedor_final = "Jogador 1 venceu a batalha final!"
            elif jogo.pontos_jogador2 > jogo.pontos_jogador1:
                vencedor_final = "Jogador 2 venceu a batalha final!"
            else:
                vencedor_final = "A batalha final terminou empatada!"
            
            emit('fim_batalha', {'mensagem': vencedor_final})
        else:
            # Atualiza a interface para remover cartas usadas
            emit('resultado_batalha', {
                'resultado': resultado,
                'carta1': str(carta_selecionada),
                'carta2': str(carta_adversario),
                'vencedor': vencedor,
                'cartas': {
                    'jogador1': [str(c) for c in jogador1.mao],
                    'jogador2': [str(c) for c in jogador2.mao]
                },
                'placar': {
                    'jogador1': jogo.pontos_jogador1,
                    'jogador2': jogo.pontos_jogador2
                }
            })
    except Exception as e:
        print(f"Erro ao iniciar batalha: {e}")
        emit('erro', {'mensagem': str(e)})





#(verificacao adicional)
@socketio.on('reiniciar_batalha')
def handle_restart():
    print("Reiniciando batalha...")
    iniciar_jogo()  # Reinicia o jogo e distribui cartas novamente
    emit('cartas_iniciais', {'cartas': {
        'jogador1': [str(c) for c in jogo.jogador1.mao],
        'jogador2': [str(c) for c in jogo.jogador2.mao]
    }})

if __name__ == '__main__':
    socketio.run(app, debug=True)
