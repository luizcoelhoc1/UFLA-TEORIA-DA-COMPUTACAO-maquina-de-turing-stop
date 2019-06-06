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
  
    
    """
    Faz as devidas alterações na fita que uma instrução de transição de uma Maquina de Turing realiza
    """
    def mudarTransicao(self, direcao, simbulo):
    #Quebrar a Fita indo pra ESQUERDA no final da fita
        if self.cabecote == 0 and direcao == ESQUERDA:
            raise Exception('Fita estourada')

    #Simulando Fita Infinita
        if len(self.fita) == (self.cabecote+1) and direcao == DIREITA:
            self.fita += BLANK
        
    #salva simbulo anterior para retorno 
        simbuloAnterior = self.fita[self.cabecote]
        
    #Faz a troca de simbulos
        self.fita = self.fita[:self.cabecote] + simbulo + self.fita[(self.cabecote + 1):] 

    #Move cabecote
        if direcao == DIREITA: 
            self.cabecote += 1
        else: 
            self.cabecote -= 1
        return simbuloAnterior
  
    """
    Retorna o simbulo quo cabeçote está apontando
    """
    def pegarSimbulo (self):
        return self.fita[self.cabecote]

    """
    Zera a fita e coloca uma nova entrada
    """
    def recomecarFita(self, entrada):
        self.fita = BLANK + entrada
        self.cabecote = 0
        
    """
    Função de escritura da fita
    """
    def __str__(self):
        icon = "v"
        retorno = ""
        for i in range(self.cabecote):
            retorno += " "
        retorno += icon + "\n"
        return retorno + self.fita + BLANK

    """
    Volta o cabeçote ao começo da fita sem alterar nenhum simbulo 
    """
    def rebobinar(self):
        if self.fita[0] != BLANK:
            raise Exception('Fita estourada')
        self.cabecote = 0        


        
        
        
