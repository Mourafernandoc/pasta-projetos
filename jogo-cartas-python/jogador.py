# jogador.py

class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.deck = []
        self.mao = []

    def adicionar_carta_ao_deck(self, carta):
        self.deck.append(carta)

    def comprar_carta(self):
        if self.deck:
            carta = self.deck.pop(0)
            self.mao.append(carta)
            return carta
        return None
    def definir_oponente(self, oponente):
        self.oponente_jogador = oponente

    def oponente(self):
        return self.oponente_jogador

    def __str__(self):
        return f"{self.nome} (Cartas na mão: {len(self.mao)}, Cartas no deck: {len(self.deck)})"
