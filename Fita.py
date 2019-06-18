"""
@author: luizc
"""

DIREITA = True
ESQUERDA = False
BLANK = "B"

class Fita:
    '''Simula a fita de uma MT'''

    def __init__(self, entrada):
        self.recomecarFita(entrada)
  
    def mudarTransicao(self, direcao, simbolo):
    '''Faz alterações na fita'''    
        # Quebrar a Fita indo pra ESQUERDA no final da fita
        if self.cabecote == 0 and direcao == ESQUERDA:
            raise Exception('Fita estouradaa')
        # Simulando Fita Infinita
        if len(self.fita) == (self.cabecote+1) and direcao == DIREITA:
            self.fita += BLANK  
        # Salva simbolo anterior para retorno 
        simboloAnterior = self.fita[self.cabecote]
        # Faz a troca de simbolos
        self.fita = self.fita[:self.cabecote] + simbolo + self.fita[(self.cabecote + 1):] 
        # Move cabecote
        if direcao == DIREITA: 
            self.cabecote += 1
        else: 
            self.cabecote -= 1
        return simboloAnterior


    def pegarSimbolo (self):
    '''Retorna o simbolo quo cabeçote está apontando'''
        return self.fita[self.cabecote]


    def recomecarFita(self, entrada):
    '''Zera a fita e coloca uma nova entrada'''
        self.fita = BLANK + entrada
        self.cabecote = 0
        
 
    def __str__(self):
    '''Função de escritura da fita'''
        icon = "v"
        retorno = ""
        for i in range(self.cabecote):
            retorno += " "
        retorno += icon + "\n"
        return retorno + self.fita + BLANK


    def rebobinar(self):
    '''Volta o cabeçote ao começo da fita sem alterar nenhum símbolo'''
        if self.fita[0] != BLANK:
            raise Exception('Fita estourada')
        self.cabecote = 0        


        
        
        
