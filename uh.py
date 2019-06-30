# -*- coding: utf-8 -*-

"""
uh.py

Estende a classe MaquinaDeTuringUniversal, incluindo heurísticas para
identificar se a MT para ou entra em loop com uma determinada entrada.
"""


import sys
import itertools
from MaquinaDeTuringUniversal import MaquinaDeTuringUniversal, DIREITA

class MTUcomHeuristicas(MaquinaDeTuringUniversal):
    """Estende a MTU com heurísticas para identificar se ela para ou entra em loop."""

    def executar_simulacao(self):
        # seta e verifica os estados criticos
        #self.verifica_TransicoesCriticas()
        # verifica se existem loop para todos simbolos em alguma transicao
        q_erro = self.verifica_qerro()
        # verifica se o número de iterações ultrapassa o numero maximo de combinações 
        max_combinacoes = self.calcula_max_combinacoes()
        iteracoes = 0
        # executa a simulação
        while not self.simularTransicao():
            #if self.verifica_TransicaoAtualIsCritica():
            #    return False
            if self.estadoAtualMT() == q_erro:
                return False
            iteracoes += 1
            if iteracoes >= max_combinacoes:
                return False
            #self.printBonito()
        return True

    def resultado(self):
        """Retorna string informando se a mt simulada para ou entra em loop."""
        status = self.executar_simulacao()
        if status:
            return "A MT simulada aceita w e para.\n"
        else:
            return "A MT entra em loop com a entrada w.\n"

    def verifica_qerro(self):
        NUM_SIMBOLOS = 3
        num_transicoes_estado = {}
        for transicao in self.transicoes:
            elementos = transicao.split("0")
            if elementos[0] == elementos[2]:
                if elementos[0] in num_transicoes_estado:
                    num_transicoes_estado[elementos[0]] += 1
                else:
                    num_transicoes_estado[elementos[0]] = 1
        for estado, num_transicoes in num_transicoes_estado.items():
            #print('TRANSICOES POR ESTADO:', estado, num_transicoes)
            if num_transicoes >= NUM_SIMBOLOS:
                return estado

    def calcula_max_combinacoes(self):
        num_transicoes_mt = len(self.transicoes)
        #print(num_transicoes_mt)
        tam_palavra = len(self.palavra.split('0'))
        #print(tam_palavra)
        num_simbolos = 3
        _max = num_transicoes_mt * tam_palavra * (num_simbolos ** tam_palavra)
        return _max


    def verifica_TransicoesCriticas(self):
        """X0Z0Y0Z011
           Y0K0X0K01"""
        self.transicoesCriticas = list()
        transicoes = self.fita1.fita.split("00")
        for transicao in self.transicoes:
            print(transicao)
            elementosTransicao = transicao.split("0")
            if elementosTransicao[1] == elementosTransicao[3]: #verifica se nao muda simbolo na primeira transição
                for transicao2 in self.transicoes:
                    elementosTransicao2 = transicao2.split("0")
                    isCritico = elementosTransicao2[1] == elementosTransicao2[3]               #verifica se nao muda o simbolo na segunda transição
                    isCritico = isCritico and elementosTransicao[0] == elementosTransicao2[2]  #verifica se verifica se a primeira esta apontando pra segunda
                    isCritico = isCritico and elementosTransicao[2] == elementosTransicao2[0]  #verifica se verifica se a segunda esta apontando pra primeira
                    isCritico = isCritico and elementosTransicao[4] != elementosTransicao2[4] #direita esquerda ou esquerda direita
                    if isCritico:
                        self.transicoesCriticas.append(transicao)
    
    def verifica_TransicaoAtualIsCritica(self):
        estadoAtual = self.estadoAtualMT()
        simboloAtual =  self.simboloAtualMT() 
        posicaoTransacao = self.fita1.fita.find("00" + estadoAtual + "0" + simboloAtual + "0") + 2

        while self.fita1.cabecote != posicaoTransacao:
            self.fita1.mudarTransicao(DIREITA, self.fita1.pegarSimbolo())
        transacao = ""
        while transacao[-2:] != "00":
            transacao += self.fita1.mudarTransicao(DIREITA, self.fita1.pegarSimbolo())
            posicaoTransacao += 1
        transacao = transacao[:-2]
        for tc in self.transicoesCriticas:
            if tc == transacao:
                return True
        return False

    
