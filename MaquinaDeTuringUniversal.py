# -*- coding: utf-8 -*-

"""
MaquinaDeTuringUniversal.py

"""

DIREITA = True
ESQUERDA = False
BLANK = "B"
TRASH = "#"
LEFT = "11"
RIGHT = "1"

from Fita import Fita

'''
class ErroSimulacao(Exception):

    def __init__(self, mensagem):
        self.mensagem = mensagem
'''

class MaquinaDeTuringUniversal:
    """Recebe string no formato R(M)w e simula M com entrada w.

    Argumentos:
        entrada: 

    Atributos:
        fita1 -- entrada da MTU, com string no formato R(M)w.
        fita2 -- estado atual da simulação. 
        fita3 -- usada na simulação de M com entrada w.
        palavra -- armazena w
    """

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
        self.transicoes = split[1].split("00")    
        headTransicoes = list()  #para verificar o determinismo  
        #for n, transicao in enumerate(self.transicoes):
        for transicao in self.transicoes:
            #verifica se a transicao é uma quintupla
            if len(transicao.split("0")) != 5:
                print("transicao {} com 0 errados".format(n))
            #verifica se tem apenas 1's na transicao
            elementosTransicao = transicao.split("0")
            for elementoTransicao in elementosTransicao:
                for digito in elementoTransicao:
                    if digito != "1":
                        print("elementos da transicoes nao sao apenas 1's")
            #verifica a direção da transicao
            direcao = elementosTransicao[4]
            if len(direcao) != 1 and len(direcao) != 2:
                print("transicao com direcao desconhecida")
        #verifica o determinismo
            headTransicoes.append(elementosTransicao[0] + "0" + elementosTransicao[1])
        if len(set(headTransicoes)) != len(headTransicoes):
            print("maquina nao deterministica")
        #verifica palavra
        self.palavra = split[2]
        letras = self.palavra.split("0")
        for letra in letras:
            if len(letra) > 3 and len(letra) < 1:
                print("Palavra em formato errado")
        #inicializa fitas            
        self.fita1 = Fita("000" + split[1] + "000")
        self.fita2 = Fita("1")
        self.fita3 = Fita(self.palavra)
        self.fita3.mudarTransicao(DIREITA, BLANK)

    def __str__(self):
        """Retorna as três fitas como string."""
        retorno  = "Fita 1: \n" + self.fita1.__str__() + "\n\n" 
        retorno += "Fita 2: \n" +self.fita2.__str__() + "\n\n"
        retorno += "Fita 3: \n" +self.fita3.__str__()
        return retorno

    def estadoAtualMT(self): 
        """Retorna o estado atual da MT simulada"""
        estado = ""
        self.fita2.rebobinar()
        self.fita2.mudarTransicao(DIREITA, BLANK)
        while self.fita2.pegarSimbolo() != BLANK:
            estado += self.fita2.mudarTransicao(DIREITA, self.fita2.pegarSimbolo())
        return estado

    def simboloAtualMT(self):
        """Retorna o simbolo atual da MT simulada"""
        simbolo = ""
        voltar = 0
        while self.fita3.pegarSimbolo() != "0" and self.fita3.pegarSimbolo() != BLANK:
            simbolo += self.fita3.mudarTransicao(DIREITA, self.fita3.pegarSimbolo())
            voltar += 1
        for i in range(voltar):
            self.fita3.mudarTransicao(ESQUERDA, self.fita3.pegarSimbolo())           
        return simbolo

    def simularTransicao(self):
        """Simula uma transição da maquina de Turing."""
        #acha transação
        estadoAtual = self.estadoAtualMT()
        simboloAtual =  self.simboloAtualMT() 
        posicaoTransacao = self.fita1.fita.find("00" + estadoAtual + "0" + simboloAtual + "0") + 2
        #aceita caso não ache a transição
        if posicaoTransacao == 1:
            return True
        #pega a transicao
        self.fita1.rebobinar()
        while self.fita1.cabecote != posicaoTransacao:
            self.fita1.mudarTransicao(DIREITA, self.fita1.pegarSimbolo())
        transicao = ""
        while transicao[-2:] != "00":
            transicao += self.fita1.mudarTransicao(DIREITA, self.fita1.pegarSimbolo())
            posicaoTransacao += 1
        transicao = transicao[:-2]
        elementosTransicao = transicao.split("0")
        #muda MT de estado
        self.fita2.recomecarFita(elementosTransicao[2])
        #Simula fita infinita
        if elementosTransicao[4] == RIGHT:
            cabecote = self.fita3.cabecote
            self.direitaSimboloMT(self.fita3, "0")
            if cabecote == self.fita3.cabecote:
                while self.fita3.pegarSimbolo() != BLANK:
                    self.fita3.mudarTransicao(DIREITA, self.fita3.pegarSimbolo())
                self.fita3.mudarTransicao(DIREITA, "0")
                self.fita3.mudarTransicao(DIREITA, "1")
                self.fita3.mudarTransicao(DIREITA, "1")
                self.fita3.mudarTransicao(DIREITA, "1")
                self.fita3.mudarTransicao(ESQUERDA, self.fita3.pegarSimbolo())
                self.fita3.mudarTransicao(ESQUERDA, self.fita3.pegarSimbolo())
                self.fita3.mudarTransicao(ESQUERDA, self.fita3.pegarSimbolo())
            self.esquerdaSimboloMT(self.fita3, "0")
        #muda Simbolo
        if len(elementosTransicao[1]) > len(elementosTransicao[3]):
            #substitui "1" no "111" fazendo "1##"
            for i in elementosTransicao[2]:
                self.fita3.mudarTransicao(DIREITA, i)
            while self.fita3.pegarSimbolo() != "0":
                self.fita3.mudarTransicao(DIREITA, TRASH)
            #remove os lixos            
            while self.temLixoEsquerda(self.fita3):
                self.removerLixoAEsquerda(self.fita3)
            #cabeça de leitura escrita no mesmo lugar
            self.fita3.mudarTransicao(ESQUERDA, self.fita3.pegarSimbolo())
            while self.fita3.pegarSimbolo() == "1":
                self.fita3.mudarTransicao(ESQUERDA, self.fita3.pegarSimbolo())
            self.fita3.mudarTransicao(DIREITA, self.fita3.pegarSimbolo())
        elif len(elementosTransicao[1]) < len(elementosTransicao[3]):
            #substitui crescendo a fita pra esquerda
            for i in range(len(elementosTransicao[3])):
                if self.fita3.pegarSimbolo() == "0":
                    self.fita3.mudarTransicao(ESQUERDA, self.fita3.pegarSimbolo())
                    self.criarBlankDireita(self.fita3)
                    self.fita3.mudarTransicao(DIREITA, self.fita3.pegarSimbolo())
                self.fita3.mudarTransicao(DIREITA, elementosTransicao[3][i])
            #retorna cabeça de leitura e escrita antes da edição 
            self.fita3.mudarTransicao(DIREITA, self.fita3.pegarSimbolo())
            self.esquerdaSimboloMT(self.fita3, "0")
        #move a cabeça de leitura e escrita
        testeBlank = self.fita3.mudarTransicao(ESQUERDA, self.fita3.pegarSimbolo())
        if testeBlank == BLANK and elementosTransicao[4] == LEFT:
            raise Exception('Mt simlada foi quebrada')
        self.fita3.mudarTransicao(DIREITA, self.fita3.pegarSimbolo())
        if elementosTransicao[4] == LEFT:
            self.esquerdaSimboloMT(self.fita3, "0")
        if elementosTransicao[4] == RIGHT:
            self.direitaSimboloMT(self.fita3, "0")
        #não aceita
        return False
             
    def removerLixoAEsquerda(self, fita):
        """Remove lixos (#) a esquerda."""
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
        """Verifica se existe lixo a esquerda da cabeça d eleitura e escrita da fita"""
        if fita.cabecote == 0:
            return False
        if fita.fita[fita.cabecote-1] == TRASH:
            return True
        else: 
            return False

    def esquerdaSimboloMT(self, fita, separador):
        """Simula move esquerda da MT"""
        fita.mudarTransicao(ESQUERDA, fita.pegarSimbolo())
        if fita.pegarSimbolo() == BLANK:
            fita.mudarTransicao(DIREITA, fita.pegarSimbolo())
        else:    
            fita.mudarTransicao(ESQUERDA, fita.pegarSimbolo())
            while fita.pegarSimbolo() != separador and fita.pegarSimbolo() != BLANK:
                fita.mudarTransicao(ESQUERDA, fita.pegarSimbolo())
            fita.mudarTransicao(DIREITA, fita.pegarSimbolo())

    def direitaSimboloMT(self, fita, separador):
        """Simula move direita da MT"""
        while fita.pegarSimbolo() != separador and fita.pegarSimbolo() != BLANK:
            fita.mudarTransicao(DIREITA, fita.pegarSimbolo())
        if fita.pegarSimbolo() == BLANK:
            fita.mudarTransicao(ESQUERDA, fita.pegarSimbolo())
            self.esquerdaSimboloMT(fita, "0")
        else:
            fita.mudarTransicao(DIREITA, fita.pegarSimbolo())  

    def printBonito(self):
        """ """
        #estado
        estado = -1;
        self.fita2.rebobinar()
        self.fita2.mudarTransicao(DIREITA, self.fita2.pegarSimbolo())
        while self.fita2.pegarSimbolo() != BLANK:
            estado += 1
            self.fita2.mudarTransicao(DIREITA, self.fita2.pegarSimbolo())
        self.fita2.rebobinar()
        print("Estado q{}: ".format(str(estado)))

        #jump e cabecote
        fita = ""
        cabecoteInicial = self.fita3.cabecote
        jump = cabecoteInicial
        while self.fita3.pegarSimbolo() != BLANK:
            simbolo = 0
            while self.fita3.pegarSimbolo() != "0" and self.fita3.pegarSimbolo() != BLANK:
                simbolo += 1
                self.fita3.mudarTransicao(ESQUERDA, self.fita3.pegarSimbolo())
            jump -= simbolo
            if self.fita3.pegarSimbolo() != BLANK:
                self.fita3.mudarTransicao(ESQUERDA, self.fita3.pegarSimbolo())
        for i in range(jump):
            fita += " "
        fita += "v" + "\n"

        # fita
        self.fita3.rebobinar()
        self.fita3.mudarTransicao(DIREITA, self.fita3.pegarSimbolo())
        dicionario = {1:"a", 2:"b", 3:"B"}
        while self.fita3.pegarSimbolo() != BLANK:
            simbolo = 0
            while self.fita3.pegarSimbolo() != "0" and self.fita3.pegarSimbolo() != BLANK:
                simbolo += 1
                self.fita3.mudarTransicao(DIREITA, self.fita3.pegarSimbolo())
            fita += dicionario[simbolo]
            self.fita3.mudarTransicao(DIREITA, self.fita3.pegarSimbolo())
        print(fita)
        self.fita3.cabecote = cabecoteInicial 


def main():     
    """teste inicial"""   
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
    mtu.printBonito()
    print("__________________")
    while not mtu.simularTransicao():
        mtu.printBonito()
        print("__________________")
    print(mtu)


if __name__ == '__main__':
    main()

