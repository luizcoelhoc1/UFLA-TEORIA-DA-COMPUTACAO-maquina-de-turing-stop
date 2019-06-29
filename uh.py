# -*- coding: utf-8 -*-

"""
uh.py

Estende a classe MaquinaDeTuringUniversal, incluindo heurísticas para
identificar se a MT para ou entra em loop com uma determinada entrada.
"""

import sys
import itertools
from MaquinaDeTuringUniversal import MaquinaDeTuringUniversal

class MTUcomHeuristicas(MaquinaDeTuringUniversal):
    """Estende a MTU com heurísticas para identificar se ela para ou entra em loop."""

    spinner = itertools.cycle(['-', '/', '|', '\\'])

    # experimental
    def mostrar_progresso(self):
        sys.stdout.write(self.spinner.next())  # write the next character
        sys.stdout.flush()                     # flush stdout buffer (actual character display)
        sys.stdout.write('\b')                 # erase the last written char


    def executar_simulacao(self):
        while not self.simularTransicao():
            self.printBonito()
            #self.mostrar_progresso()
        return True

    def resultado(self):
        """Retorna string informando se a mt simulada para ou entra em loop."""
        status = self.executar_simulacao()
        if status:
            return "A MT simulada aceita w e para."
        else:
            return "A MT entra em loop com a entrada w." 


    def verifica_loop(self, estado):
        numTransEstado = 0
        for transicao in self.transicoes:
            elementosTransicao = transicao.split("0")
            if elementosTransicao[0] == estado:
                numTransEstado += 1
        return numTransEstado == 3

    '''
    def andrew():
        """Detecta loop pela repetição de estados. Ex: (q0 -q1 - q2 - q0) *2"""
        if ((len(self.buffer) != 1) and (self.buffer[0] == self.buffer[len(self.buffer)-1])):
            self.cicloCount += 1
            self.buffer = []
        if ((self.cicloCount == 2) ) :
            raise Exception('Entrou em loop, ciclo detectado')
    '''

    def max_combinacoes(self):
        pass

    def verifica_max_combinacoes(self):
        pass
