# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 19:54:48 2019

@author: luizc
"""

DIREITA = True
ESQUERDA = False
BLANK = "B"

from Fita import Fita

"""Apenas testando como seria uma MT mesmo"""
class MaquinaDeTuring:
    def __init__(self, listaTransicoes, entrada):
        if len(listaTransicoes) == 0:
            self.listaTransicoes = list()
        else: 
            self.listaTransicoes = listaTransicoes
        self.fita = Fita(entrada)

    def configurarFitaInicial(self, entrada):
        return entrada[2]

    def __str__(self):
        return self.fita.__str__()
