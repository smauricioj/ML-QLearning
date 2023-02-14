# -*- coding: utf-8 -*-

# Autor: Sergio P
# Data: 16/09/2022

# ---------------------------------------------------------------
# IMPORTS

from dataclasses import dataclass
from random import random, choice
from math import inf
from pandas import DataFrame
import pickle

from .Estado import Estado
from .ParSA import ParSA

# ---------------------------------------------------------------
# CLASSES

class QLearning(dict):
    ''' Classe para implementação do algorítimo de QLearning '''

    acoes: list[str]
    ''' Lista de ações possíveis no ambiente de aprendizagem '''

    gamma: float = 0.2
    ''' Fator de desconto '''

    alpha: float = 0.9
    ''' Taxa de aprendizagem '''

    alphaDec: float = 0.00005
    ''' Decrescimento linear do alpha '''

    epsilon: float = 0.5
    ''' Divisão de exploração/exploitação '''

    epsilonDec: float = 0.0001
    ''' Decrescimento linear do episilon '''

    epsilonMin: float = 0.01
    ''' Epsilon mínimo '''

    padraoQ: float = 0
    ''' Valor padrão de q quando o par s,a é desconhecido '''

    q_size: int = 1
    ''' Tamanho máximo previsto da tabela Q '''

    def __init__(self, acoes: list[str]):
        ''' Inicializa o processo com uma lista de ações não vazia'''
        assert(len(acoes) > 0)
        self.acoes = acoes

    def __repr__(self):
        return str(self)

    def __str__(self):
        line = ''
        line += f'Epsilon: {self.epsilon:.5f}; '
        line += f'Alpha: {self.alpha:.5f}; '
        if self.q_size != 1:
            line += f'QRatio: {len(self)/self.q_size:.5f}'
        else:
            line += f'QSize: {len(self)}'
        return line

    @property
    def tamanhoTabelaQ(self):
        if self.q_size != 1:
            return len(self)/self.q_size
        else:
            return len(self)
    

    def getQ(self, p: ParSA):
        ''' Retorna o valor da tabela q para um par estado-acao '''
        if p in self:
            return self[p]
        else:
            return self.padraoQ

    def maxQ(self, s: Estado):
        ''' Retorna o maior valor de Q para as ações no estado s '''
        return max([self.getQ(ParSA(s,a)) for a in self.acoes])

    def argmaxQ(self, s: Estado):
        ''' Retorna a ação que possui o maior valor Q na tabela para o estado s '''

        # Arg acumula as ações possíveis para retorno
        arg = list()
        maximum = -inf
        for a in self.acoes:
            # Procura o valor q da ação a
            q = self.getQ(ParSA(s,a))

            # Guarda todas as ações a que são iguais ao maximum
            if q >= maximum:
                if q > maximum:
                    maximum = q
                    arg = list()
                arg.append(a)

        if len(arg) == 0:
            # Se nenhuma é a melhor, retorna uma escolha aleatória
            return choice(self.acoes)
        else:
            # Se alguma é a melhor, retorna uma escolha dentre essas
            return choice(arg)

    def atualizaQ(self, s: Estado, a: str, new_s: Estado, r: float):
        ''' Atualiza a tabela q com a experiência do agente '''

        # Se alpha é maior que o mínimo, decresce
        if self.alpha > 0.01:
            self.alpha -= self.alphaDec

        # Procura valor atual na tabela
        par = ParSA(s,a)
        q = self.getQ(par)

        # Equação de bellman
        q = q + self.alpha * (r + (self.gamma * self.maxQ(new_s) - q ))
        
        # Atualiza a tabela
        self[par] = q

    def acaoExploraçãoGreedy(self, s: Estado):
        ''' Retorna a ação ideal para exploração do estado s '''
        
        # Se epsilon é maior que o mínimo, decresce
        if self.epsilon > self.epsilonMin:
            self.epsilon -= self.epsilonDec

        # Divisão de exploração / exploitação
        if random() < self.epsilon:
            return choice(self.acoes) # Exploração
        else:
            return self.argmaxQ(s) # Exploitação

    def salvarQ(self, path):
        ''' Salva um arquivo da tabela q '''
        with open(path/'q.bin', 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def carregarQ(cls, path):
        ''' Inicia uma tabela q já salva em disco '''
        with open(path, 'rb') as file:
            return pickle.load(file)



