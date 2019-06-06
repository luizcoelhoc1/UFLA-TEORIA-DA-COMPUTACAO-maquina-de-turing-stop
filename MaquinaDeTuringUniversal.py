# -*- coding: utf-8 -*-

"""
Created on Mon Jun  3 19:54:48 2019

@author: luizc
"""
DIREITA = True
ESQUERDA = False
BLANK = "B"

from Fita import Fita



class MaquinaDeTuringUniversal:
    def __init__(self, entrada):
        contador = 0
        #verifica inicio começado com 000
        if entrada[0:3] != "000":
            print("comeco errado")
            
        #verifica termino começado com 000
        if entrada[-3:] != "000":
            print("final errado")

        #verifica separadores 000
        split = entrada.split("000")
        if len(split) != 4:
            print("nao possui apenas 3 separadores 000")

        #verifica transações corretas
        transacoes = split[1].split("00")    
        headTransicoes = list()  #para verificar o determinismo  
        for transacao in transacoes:
            
            #verifica se a transicao é uma quintupla
            if len(transacao.split("0")) != 5:
                print("transacao com 0 errados")
                
            #verifica se tem apenas 1's na transicao
            elementosTransicao = transicao.split("0")
            for elementoTransicao in elementosTransicao:
                for digito in elementoTransicao:
                    if digito != 1:
                        print("elementos da transições nao são apenas 1's")

            #verifica a direção da transacao
            direcao = elementosTransicao[4]
            if len(direcao) != 1 or len(direcao) != 2:
                print("transacao com direção desconhecida")

        #verifica o determinismo
            headTransicoes.append(elementosTransicao[0] + "0" + elementosTransicao[1])
        if len(set(headTransicoes)) != len(headTransicoes):
            print("maquina nao deterministica")

        #verifica palavra
        palavra = split[2]
        letras = palavra.split("0")
        for letra in letras:
            if len(letra) > 3 and len(letra) < 1:
                print("Palavra em formato errado")
                
        self.fita1 = Fita(transacoes)
        self.fita2 = Fita("1")
        self.fita3 = Fita(palavra)

    def __str__(self):
        retorno  = self.fita1.__str__() + "\n"
        retorno += self.fita2.__str__() + "\n"
        retorno += self.fita3.__str__()
        return retorno

import re
p = re.compile("^000 \b(1+01+01+01+01+00)\b 0 \b(1|l1)0\b* + 000$")
print(re.search(p, "000101110110111010011010111010100110110111101101001110110111011010011101110111110111011001111010111101010011110111011111011101100011101011011011000"))

oi = "000101011011101001010111010100110110111101101001110110111011010011101110111110111011001111010111101010011110111011111011101100011101011011011000"

transacoes = oi.split("000")[1].split("00")
headTransicoes = list()
for transicao in transacoes:
    print(transicao)
    elementosTransicao = transicao.split("0")
    
print(len(headTransicoes))
print(len(set(headTransicoes)))
    
