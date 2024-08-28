# carta.py

class Carta:
    def __init__(self, nome, atk, def_, atks, ex):
        self.nome = nome
        self.atk = atk
        self.def_ = def_
        self.atks = atks
        self.ex = ex

    def __str__(self):
        return f"{self.nome} (ATK: {self.atk}, DEF: {self.def_}, ATKS: {self.atks}, EX: {self.ex})"
