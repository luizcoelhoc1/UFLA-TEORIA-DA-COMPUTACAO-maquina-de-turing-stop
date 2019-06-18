"""
@author: luizc
"""

from Fita import Fita

DIREITA = True
ESQUERDA = False
BLANK = "B"
TRASH = "#"
LEFT = "11"
RIGHT = "1"


class MaquinaDeTuringUniversal:
    '''Simula uma MT universal'''

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
        #inicializa fitas            
        self.fita1 = Fita("000" + split[1] + "000")
        self.fita2 = Fita("1")
        self.fita3 = Fita(palavra)
        self.fita3.mudarTransicao(DIREITA, BLANK)


    def __str__(self):
    '''Retorna as três fitas no print do objeto'''
        retorno  = "Fita 1: \n" + self.fita1.__str__() + "\n\n" 
        retorno += "Fita 2: \n" +self.fita2.__str__() + "\n\n"
        retorno += "Fita 3: \n" +self.fita3.__str__()
        return retorno


    def estadoAtualMT(self): 
    '''Retorna o estado atual da MT simulada'''
        estado = ""
        self.fita2.rebobinar()
        self.fita2.mudarTransicao(DIREITA, BLANK)
        while self.fita2.pegarSimbolo() != BLANK:
            estado += self.fita2.mudarTransicao(DIREITA, self.fita2.pegarSimbolo())
        return estado


    def simboloAtualMT(self):
    '''Retorna o símbolo atual da MT simulada'''
        simbolo = ""
        voltar = 0
        while self.fita3.pegarSimbolo() != "0":
            simbolo += self.fita3.mudarTransicao(DIREITA, self.fita3.pegarSimbolo())
            voltar += 1
        for i in range(voltar):
            self.fita3.mudarTransicao(ESQUERDA, self.fita3.pegarSimbolo())           
        return simbolo


    def rodarTransicao(self):
    '''Simula uma transição da maquina de turing'''
        #acha transação
        posicaoTransacao = self.fita1.fita.find("00" + self.estadoAtualMT() + "0" + self.simboloAtualMT() + "0") + 2
        #aceita caso não ache a transição
        if posicaoTransacao == 1:
            return True
        #pega a transicao
        self.fita1.rebobinar()
        while self.fita1.cabecote != posicaoTransacao:
            self.fita1.mudarTransicao(DIREITA, self.fita1.pegarSimbolo())
        transacao = ""
        while transacao[-2:] != "00":
            transacao += self.fita1.mudarTransicao(DIREITA, self.fita1.pegarSimbolo())
            posicaoTransacao += 1
        transacao = transacao[:-2]
        elementosTransacao = transacao.split("0")
        #muda MT de estado
        self.fita2.recomecarFita(elementosTransacao[2])
        #muda Simbolo
        if len(elementosTransacao[1]) > len(elementosTransacao[3]):
            #substitui "1" no "111" fazendo "1##"
            for i in elementosTransacao[2]:
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
        elif len(elementosTransacao[1]) < len(elementosTransacao[3]):
            #substitui crescendo a fita pra esquerda
            for i in range(len(elementosTransacao[3])):
                if self.fita3.pegarSimbolo() == "0":
                    self.fita3.mudarTransicao(ESQUERDA, self.fita3.pegarSimbolo())
                    self.criarBlankDireita(self.fita3)
                    self.fita3.mudarTransicao(DIREITA, self.fita3.pegarSimbolo())
                self.fita3.mudarTransicao(DIREITA, elementosTransacao[3][i])
            #retorna cabeça de leitura e escrita antes da edição 
            self.fita3.mudarTransicao(DIREITA, self.fita3.pegarSimbolo())
            self.esquerdaSimboloMT(self.fita3, "0")
        #move a cabeça de leitura e escrita
        testeBlank = self.fita3.mudarTransicao(ESQUERDA, self.fita3.pegarSimbolo())
        if testeBlank == BLANK and elementosTransacao[4] == LEFT:
            raise Exception('Mt simlada foi quebrada')
        self.fita3.mudarTransicao(DIREITA, self.fita3.pegarSimbolo())
        if elementosTransacao[4] == LEFT:
            self.esquerdaSimboloMT(self.fita3, "0")
        if elementosTransacao[4] == RIGHT:
            self.direitaSimboloMT(self.fita3, "0")
        #não aceita
        return False
        

    def removerLixoAEsquerda(self, fita):
    '''Remove lixos a esquerda. Ex.: 11######ǐ111001 -> 111111001'''
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
    '''Verifica se existe lixo a esquerda da cabeça d eleitura e escrita da fita.'''
        if fita.cabecote == 0:
            return False
        if fita.fita[fita.cabecote-1] == TRASH:
            return True
        else: 
            return False


    def esquerdaSimboloMT(self, fita, separador):
    '''Simula move esquerda da MT'''
        fita.mudarTransicao(ESQUERDA, fita.pegarSimbolo())
        if fita.pegarSimbolo() == BLANK:
            fita.mudarTransicao(DIREITA, fita.pegarSimbolo())
        else:    
            fita.mudarTransicao(ESQUERDA, fita.pegarSimbolo())
            while fita.pegarSimbolo() != separador and fita.pegarSimbolo() != BLANK:
                fita.mudarTransicao(ESQUERDA, fita.pegarSimbolo())
            fita.mudarTransicao(DIREITA, fita.pegarSimbolo())


    def direitaSimboloMT(self, fita, separador):
    '''Simula move direita da MT'''
        while fita.pegarSimbolo() != separador and fita.pegarSimbolo() != BLANK:
            fita.mudarTransicao(DIREITA, fita.pegarSimbolo())
        if fita.pegarSimbolo() == BLANK:
            fita.mudarTransicao(ESQUERDA, fita.pegarSimbolo())
            esquerdaSimboloMT(fita, "0")
        else:
            fita.mudarTransicao(DIREITA, fita.pegarSimbolo())  


def main:
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
    mtu.rodarTransicao()    


if __name__ == '__main__':
    main()



#import re
#p = re.compile("^000 \b(1+01+01+01+01+00)\b 0 \b(1|l1)0\b* + 000$")
#print(re.search(p, "000101110110111010011010111010100110110111101101001110110111011010011101110111110111011001111010111101010011110111011111011101100011101011011011000"))

"""
def criarBlankDireita(fita):
    #grava primeiro simbolo e ponto de partida
    simboloAntigo = fita.mudarTransicao(DIREITA, TRASH)
    
    #vai ate o final da fita
    while fita.pegarSimbolo() != BLANK: 
        fita.mudarTransicao(DIREITA, fita.pegarSimbolo())
    fita.mudarTransicao(ESQUERDA, fita.pegarSimbolo())
    
    #volta dando swap até onde estava
    while fita.pegarSimbolo() != TRASH:
        simbolo = fita.mudarTransicao(DIREITA, fita.pegarSimbolo())
        fita.mudarTransicao(ESQUERDA, simbolo)
        fita.mudarTransicao(ESQUERDA, BLANK)
    
    #volta o Simbolo de começo e volta a cabeça de leitura e escrita
    fita.mudarTransicao(DIREITA, simboloAntigo)
    fita.mudarTransicao(ESQUERDA, fita.pegarSimbolo())


fita3 = Fita("1011011011011")
elementosTransacao = ["1", "11", "11", "11111111111111111", "1"]
fita3.mudarTransicao(DIREITA, fita3.pegarSimbolo())

def esquerdaSimboloMT(fita, separador):
    fita.mudarTransicao(ESQUERDA, fita.pegarSimbolo())
    if fita.pegarSimbolo() == BLANK:
        fita.mudarTransicao(DIREITA, fita.pegarSimbolo())
    else:    
        fita.mudarTransicao(ESQUERDA, fita.pegarSimbolo())
        while fita.pegarSimbolo() != separador and fita.pegarSimbolo() != BLANK:
            fita.mudarTransicao(ESQUERDA, fita.pegarSimbolo())
        fita.mudarTransicao(DIREITA, fita.pegarSimbolo())
        
def direitaSimboloMT(fita, separador):
    while fita.pegarSimbolo() != separador and fita.pegarSimbolo() != BLANK:
        fita.mudarTransicao(DIREITA, fita.pegarSimbolo())
    if fita.pegarSimbolo() == BLANK:
        fita.mudarTransicao(ESQUERDA, fita.pegarSimbolo())
        esquerdaSimboloMT(fita, "0")
    else:
        fita.mudarTransicao(DIREITA, fita.pegarSimbolo())  


#substitui o simbolo da MT pelo novo simbolo que indica a transicao
for i in range(len(elementosTransacao[3])):
    if fita3.pegarSimbolo() == "0":
        fita3.mudarTransicao(ESQUERDA, fita3.pegarSimbolo())
        criarBlankDireita(fita3)
        fita3.mudarTransicao(DIREITA, fita3.pegarSimbolo())
    fita3.mudarTransicao(DIREITA, elementosTransacao[3][i])

#retorna cabeça de leitura
fita3.mudarTransicao(DIREITA, fita3.pegarSimbolo())
esquerdaSimboloMT(fita3, "0")


testeBlank = fita3.mudarTransicao(ESQUERDA, fita3.pegarSimbolo())
if testeBlank == BLANK and elementosTransacao[4] == LEFT:
    raise Exception('Mt simlada foi quebrada')
fita3.mudarTransicao(DIREITA, fita3.pegarSimbolo())

if elementosTransacao[4] == LEFT:
    esquerdaSimboloMT(fita3, "0")
if elementosTransacao[4] == RIGHT:
    direitaSimboloMT(fita3, "0")
print(fita3)
"""
