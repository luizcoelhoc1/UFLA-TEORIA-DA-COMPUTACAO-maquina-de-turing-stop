# -*- coding: utf-8 -*-

"""
Created on Mon Jun  3 19:54:48 2019

@author: luizc
"""
DIREITA = True
ESQUERDA = False
BLANK = "B"
TRASH = "#"

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
            elementosTransicao = transacao.split("0")
            for elementoTransicao in elementosTransicao:
                for digito in elementoTransicao:
                    if digito != "1":
                        print("elementos da transicoes nao sao apenas 1's")

            #verifica a direção da transacao
            direcao = elementosTransicao[4]
            if len(direcao) != 1 and len(direcao) != 2:
                print("transacao com direcao desconhecida")

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
                
        self.fita1 = Fita("000" + split[1] + "000")
        self.fita2 = Fita("1")
        self.fita3 = Fita(palavra)
        self.fita3.mudarTransicao(DIREITA, BLANK)

    def __str__(self):
        retorno  = "Fita 1: \n" + self.fita1.__str__() + "\n\n" 
        retorno += "Fita 2: \n" +self.fita2.__str__() + "\n\n"
        retorno += "Fita 3: \n" +self.fita3.__str__()
        return retorno

    def rodarTransicao(self):
        
        #achar estado
        estado = ""
        self.fita2.rebobinar()
        self.fita2.mudarTransicao(DIREITA, BLANK)
        while self.fita2.pegarSimbolo() != BLANK:
            estado += self.fita2.mudarTransicao(DIREITA, self.fita2.pegarSimbolo())
        
        #achar simbulo
        simbulo = ""
        voltar = 0
        while self.fita3.pegarSimbolo() != "0":
            simbulo += self.fita3.mudarTransicao(DIREITA, self.fita3.pegarSimbolo())
            voltar += 1
        for i in range(voltar):
            self.fita3.mudarTransicao(ESQUERDA, self.fita3.pegarSimbolo())            
        
        posicaoTransacao = self.fita1.fita.find("00" + estado + "0" +simbulo + "0") + 2
        """
        if posicaoTransacao == -1:
            return True"""
            
        #pega a transacao
        self.fita1.rebobinar()
        while self.fita1.cabecote != posicaoTransacao:
            self.fita1.mudarTransicao(DIREITA, self.fita1.pegarSimbolo())
        transacao = ""
        while transacao[-2:] != "00":
            transacao += self.fita1.mudarTransicao(DIREITA, self.fita1.pegarSimbolo())
            posicaoTransacao += 1
        transacao = transacao[:-2]
        
        
        elementosTransacao = transacao.split("0")
        print(elementosTransacao[2])
        self.fita2.recomecarFita(elementosTransacao[2])
        
        if len(elementosTransacao[1]) > len(elementosTransacao[3]):
            i = 0
            while elementosTransacao[2][i:] != "":
                self.fita3.mudarTransicao(DIREITA, elementosTransacao[2][i])
            
            
        if len(elementosTransacao[1]) > len(elementosTransacao[3]):
            for i in elementosTransacao[2]:
                self.fita3.mudarTransicao(DIREITA, i)
            while fita3.pegarSimbolo() != "0":
                self.fita3.mudarTransicao(DIREITA, TRASH)
            
            while temLixoEsquerda(self.fita3):
                removerLixoAEsquerda(self.fita3)
            
            self.fita3.mudarTransicao(ESQUERDA, self.fita3.pegarSimbolo())
            while self.fita3.pegarSimbolo() == "1":
                self.fita3.mudarTransicao(ESQUERDA, self.fita3.pegarSimbolo())
            self.fita3.mudarTransicao(DIREITA, self.fita3.pegarSimbolo())
        elif len(elementosTransacao[1]) < len(elementosTransacao[3]):
            print()
            
            
            
            
        print(self.fita3) 
            
        
        """
        
        while self.fita1.cabecote != posicaoTransacao
        print(self.fita1.fita.find(transacao))
        """
       
        transicao = estado + "0" + self.fita2.pegarSimbolo()
        #self.fita1..find(transacao)
        print(self)
        print("\n__________________\n")
        

    def removerLixoAEsquerda(self, fita):
        inicio = fita.cabecote
    
        while fita.pegarSimbolo() != BLANK:
            if fita.pegarSimbolo() == "0":
                fita.mudarTransicao(ESQUERDA, TRASH)
                fita.mudarTransicao(DIREITA, "0")
                fita.mudarTransicao(DIREITA, TRASH)
            if fita.pegarSimbolo() == "1":
                fita.mudarTransicao(ESQUERDA, TRASH)
                fita.mudarTransicao(DIREITA, "1")
                fita.mudarTransicao(DIREITA, TRASH)
    
        fita.mudarTransicao(ESQUERDA, BLANK)
        fita.mudarTransicao(ESQUERDA, BLANK)
        fita.rebobinar()
        
        while fita.cabecote != inicio:
            fita.mudarTransicao(DIREITA, fita.pegarSimbolo() )
        fita.mudarTransicao(ESQUERDA, fita.pegarSimbolo())
        
    def temLixoEsquerda(self, fita):
        if fita.cabecote == 0:
            return False
        if fita.fita[fita.cabecote-1] == TRASH:
            return True
        else: 
            return False



   


    
#import re
#p = re.compile("^000 \b(1+01+01+01+01+00)\b 0 \b(1|l1)0\b* + 000$")
#print(re.search(p, "000101110110111010011010111010100110110111101101001110110111011010011101110111110111011001111010111101010011110111011111011101100011101011011011000"))
mc = "000"
mc += "1011101101110100"
mc += "11010111010100"
mc += "11011011110110100"
mc += "11101101110110100"
mc += "1110111011111011101100"
mc += "11110101111010100"
mc += "111101110111110111011"
mc += "000"
mc += "11101011011011"
mc += "000"

mtu = MaquinaDeTuringUniversal(mc)
mtu.rodarTransicao()
