# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 19:55:38 2019

@author: luizc
"""


DIREITA = True
ESQUERDA = False
BLANK = "B"



class Fita:
    def __init__(self, entrada):
        self.recomecarFita(entrada)
  
    def mudarTransicao(self, direcao, simbulo):
    #Quebrar a Fita indo pra ESQUERDA no final da fita
        if self.cabecote == 0 and direcao == ESQUERDA:
            raise Exception('Fita estourada')

    #Simulando Fita Infinita
        if len(self.fita) == self.cabecote and direcao == DIREITA:
            self.fita += BLANK

    #Faz a troca de simbulos
        self.fita[self.cabecote] = simbulo

    #Move cabecote
        if direcao == DIREITA: 
            self.cabecote += 1
        else: 
            self.cabecote -= 1
        return 0
  
    def pegarSimbulo (self):
        return self.fita[self.cabecote]

    def recomecarFita(self, entrada):
        self.fita = BLANK + entrada
        self.cabecote = 0
        
    def __str__(self):
        return self.fita
        
        
        
        
        