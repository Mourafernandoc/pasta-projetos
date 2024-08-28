# jogo.py

import random
from carta import Carta
from jogador import Jogador

class Jogo:
    def __init__(self, jogador1, jogador2):
        self.jogador1 = jogador1
        self.jogador2 = jogador2
        self.turno = random.choice([jogador1, jogador2])
        self.vencedor = None

    def trocar_turno(self):
        self.turno = self.jogador1 if self.turno == self.jogador2 else self.jogador2

    def iniciar_batalha(self):
        carta_jogador1 = self.jogador1.mao.pop(0)
        carta_jogador2 = self.jogador2.mao.pop(0)
        print(f"{self.jogador1.nome} joga {carta_jogador1}")
        print(f"{self.jogador2.nome} joga {carta_jogador2}")

        resultado = self.comparar_cartas(carta_jogador1, carta_jogador2)
        print(resultado)

        sel.trocar_turno()

    def comparar_cartas(self, carta1, carta2):
        #combate usando atk e def
        if carta1.atk > carta2.def_:
            vencedor = self.jogador1.nome
        elif carta1.atk < carta2.def_:
            vencedor = self.jogador2.nome
        else:
            vencedor = "empate"

        # logica de super ataque(atks)
        if carta1.atks > carta2.atks:
            vencedor = self.jogador1.nome
        elif carta1.atks < carta2.atks:
            vencedor = self.jogador2.nome

        # habilidade especial(ex)
        if carta1.ex:
            print(f"{self.jogador1.nome} usa a habilidade especial!")
            vencedor = self.jogador1.nome

        if carta2.ex:
            print(f"{self.jogador2.nome} usa a habilidade especial!")
            vencedor = self.jogador2.nome

        return f" O {vencedor} vence a batalha!"
        