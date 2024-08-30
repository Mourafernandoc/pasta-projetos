# jogo.py (atualizado)

import random
from carta import Carta
from jogador import Jogador

class Jogo:
    def __init__(self, jogador1, jogador2):
        self.jogador1 = jogador1
        self.jogador2 = jogador2
        self.turno = random.choice([jogador1, jogador2])
        self.pontos_jogador1 = 0
        self.pontos_jogador2 = 0

    def resetar_placar(self):
        self.pontos_jogador1 = 0
        self.pontos_jogador2 = 0

    def trocar_turno(self):
        self.turno = self.jogador1 if self.turno == self.jogador2 else self.jogador2

    def comparar_cartas(self, carta1, carta2):
        if carta1.atk > carta2.def_:
            vencedor = self.jogador1.nome
        elif carta1.atk < carta2.def_:
            vencedor = self.jogador2.nome
        else:
            vencedor = "Empate"

        if carta1.atks > carta2.atks:
            vencedor = self.jogador1.nome
        elif carta1.atks < carta2.atks:
            vencedor = self.jogador2.nome

        if carta1.ex:
            vencedor = self.jogador1.nome

        if carta2.ex:
            vencedor = self.jogador2.nome

        return f"O vencedor é: {vencedor}"
