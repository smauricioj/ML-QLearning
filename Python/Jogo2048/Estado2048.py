# -*- coding: utf-8 -*-

# Autor: Sergio P
# Data: 20/09/2022

# Baseado em: geeksforgeeks.org/2048-game-in-python/

# ---------------------------------------------------------------
# IMPORTS

from hashlib import sha1
from sys import byteorder
from math import log2
from random import randint
import numpy as np

from QL import Estado

# ---------------------------------------------------------------
# FUNÇÕES


def new_mat() -> list:
    ''' Inicializa a matriz de celulas do jogo '''

    # Matriz é 4 vetores de 4 elementos, todos 0
    mat = [[0 for _ in range(4)] for _ in range(4)]

    # Adiciona célula inicial
    add_cell(mat)
    return mat


def contains(mat, cell) -> bool:
    ''' Retorna se a matriz contém cell '''
    return any([any([c == cell for c in r]) for r in mat])


def add_cell(mat) -> bool:
    ''' Adiciona uma célula em local aleatório '''

    # Verifica se pode adicionar
    if contains(mat, 0):
        # Escolhe uma célula aleatória vazia
        while True:
            i = randint(0, 3)
            j = randint(0, 3)
            if mat[i][j] == 0:
                break

        # Atualiza o valor da célula com 2 ou 4
        mat[i][j] = 2 * randint(1, 2)
        return True
    else:
        return False


def next_step(mat, max_cell) -> int:
    '''
    Define qual próximo passo do jogo

    Retornos:
    +1 : vitória
     0 : continua
    -1 : derrota
    '''

    if contains(mat, max_cell):
        # Se contém max_cell, é vitória
        return 1

    if contains(mat, 0):
        # Se contém pelo menos 1 célula vazia, continua
        return 0

    for i in range(4):
        for j in range(4):
            # Se dá pra juntar células, continua
            # (deve ter algum jeito melhor de descrever isso)
            if i != 3 and j != 3:
                if mat[i][j] == mat[i+1][j] or mat[i][j] == mat[i][j+1]:
                    return 0
            if i == 3 and j != 3:
                if mat[i][j] == mat[i][j+1]:
                    return 0
            if i != 3 and j == 3:
                if mat[i][j] == mat[i+1][j]:
                    return 0

    # Condição de derrota
    return -1


def olha_esquerda(m, i, j):
    ''' Olha para esquerda da célula i,j e procura valor igual '''
    if j > 0:
        for other_j in range(j-1, -1, -1):
            if m[i][other_j] == 0:
                continue
            elif m[i][other_j] == m[i][j]:
                return True
            else:
                return False
        return False
    else:
        return False


def olha_direita(m, i, j):
    ''' Olha para direita da célula i,j e procura valor igual '''
    if j < 3:
        for other_j in range(j+1, 4):
            if m[i][other_j] == 0:
                continue
            elif m[i][other_j] == m[i][j]:
                return True
            else:
                return False
        return False
    else:
        return False


def olha_cima(m, i, j):
    ''' Olha para cima da célula i,j e procura valor igual '''
    if i > 0:
        for other_i in range(i-1, -1, -1):
            if m[other_i][j] == 0:
                continue
            elif m[other_i][j] == m[i][j]:
                return True
            else:
                return False
        return False
    else:
        return False


def olha_baixo(m, i, j):
    ''' Olha para baixo da célula i,j e procura valor igual '''
    if i < 3:
        for other_i in range(i+1, 4):
            if m[other_i][j] == 0:
                continue
            elif m[other_i][j] == m[i][j]:
                return True
            else:
                return False
        return False
    else:
        return False


def merge(mat) -> list:
    ''' Junta as célular iguais nas linhas para esquerda '''

    # Percorre as linhas
    for i in range(4):
        # Percorre as colunas, menos a última-
        for j in range(3):

            # Condições para juntar:
            # ser igual a próxima na linha
            # e não ser vazia
            if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:

                # Duplica a célula e zera a próxima
                mat[i][j] = mat[i][j] * 2
                mat[i][j + 1] = 0

    return mat


def compress(mat) -> list:
    ''' Comprime as células para a esquerda '''
    return [
        (lambda l: l + [0]*(4-len(l)))([c for c in r if c != 0])
        for r in mat
    ]


def reverse(mat) -> list:
    ''' Inverte a matriz, linha a linha '''
    return [r[::-1] for r in mat]


def transpose(mat) -> list:
    ''' Transpõe a matriz, invertendo linhas e colunas '''
    return [list(r) for r in list(zip(*mat))]


def move_left(mat) -> list:
    ''' Movimento para a esquerda '''
    return compress(merge(compress(mat)))


def move_right(mat) -> list:
    ''' Movimento para a direita '''
    return reverse(move_left(reverse(mat)))


def move_up(mat) -> list:
    ''' Movimento para cima '''
    return transpose(move_left(transpose(mat)))


def move_down(mat) -> list:
    ''' Movimento para baixo '''
    return transpose(move_right(transpose(mat)))

# ---------------------------------------------------------------
# CLASSES


class EstadoJogo(Estado):
    ''' Estado do jogo para Q-Learning '''

    mat: list[list]
    ''' Matriz com valores de 0 a 2048 '''

    pont: int
    ''' Pontuação do jogo '''

    v_max: int
    ''' Maior valor na matriz '''

    def __init__(self, mat: None | list[list]):
        super(EstadoJogo, self).__init__()
        if mat is None:
            self.mat = new_mat()
        else:
            # Iniciando estado com uma matriz definida
            assert(len(mat) == 4)
            assert(all([len(r) == 4 for r in mat]))
            self.mat = mat

        self.pont = sum([sum(r) for r in self.mat])
        self.v_max = max([max(r) for r in self.mat])
        self.s = None

    def __hash__(self):
        return int.from_bytes(
            sha1(np.array(self.mat).tobytes()).digest(),
            byteorder
        )

    def __eq__(self, outro):
        return isinstance(outro, type(self)) and self.mat == outro.mat

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        batch = '\n'
        for r in self.mat:
            batch += f'{r}\n'
        return batch

    def _novoEstado(self,
                    mat: None | list[list]) -> Estado:
        return EstadoJogo(mat=mat)

    def recompensa(self,
                   outro: Estado,
                   acao: str) -> int:
        '''
        Retorna a recompensa por atingir o estado atual a partir de outro
        '''
        return next_step(self.mat, 2048)

    # Daqui pra baixo é fixo

    def terminal(self,
                 max_cell: int) -> bool:
        ''' Retorna se o estado do jogo é terminal ou não '''
        return next_step(self.mat, max_cell) != 0

    def vitoria(self,
                max_cell: int) -> bool:
        ''' Retorna se o estado do jogo é vitória ou não '''
        return contains(self.mat, max_cell)

    def continua(self) -> bool:
        ''' Próximo passo do jogo '''
        return add_cell(self.mat)

    def simularAcao(self,
                    acao: str) -> Estado:
        nova_mat = self.mat
        if acao == 'cima':
            nova_mat = move_up(self.mat)
        elif acao == 'baixo':
            nova_mat = move_down(self.mat)
        elif acao == 'direita':
            nova_mat = move_right(self.mat)
        elif acao == 'esquerda':
            nova_mat = move_left(self.mat)
        return self._novoEstado(mat=nova_mat)


class EstadoReduzido(EstadoJogo):
    ''' Estado reduzido para Q-Learning '''

    s: tuple
    '''
    Tupla com elementos
        0 flush_cima:bool     = Se as peças estão todas acima
        1 flush_baixo:bool    =               ^^        abaixo
        2 flush_esquerda:bool =               ^^        a esquerda
        3 flush_direita:bool  =               ^^        a direita
        3+n rank_n:tuple      = Tupla com informações da peça no rank n
            0 valor:int       = Valor da peça
            1 quad:int        = Quadrante
            2 dist:int        = Distância manhatan do canto
            3 vert:bool       = Se pode juntar com movimento vertical
            4 horz:bool       = Se pode juntar com movimento horizontal
    '''

    n_ranks: int = 3
    ''' Número de ranks incluído na tupla de estados '''

    def __init__(self, mat: None | list[list]):
        super(EstadoReduzido, self).__init__(mat)

        # Matrix do numpy é melhor pra lidar com essas coisas
        matrix = np.asmatrix(self.mat)

        # Quadrantes da matrix
        quads = [
            M for S in np.split(matrix, 2, axis=0)
              for M in np.split(S, 2, axis=1)
        ]

        # Procura os maiores elementos
        flat = matrix.flatten()
        flat.sort()
        uniques = np.unique(flat, axis=1)[0,1:]
        rks = []

        # Para cada elemento no rank
        for rank in range(1,min(self.n_ranks,len(uniques))+1):
            # Valor do elemento
            valor = uniques[-rank]

            # Posição do elemento na matriz
            idx = np.unravel_index(
                np.argmax(matrix.flatten()==valor),
                matrix.shape
            )

            # Define quadrante e distância
            if idx[0] < 2:
                if idx[1] < 2:
                    # Primeiro quadrante
                    quad = 1
                    if idx == (0, 0):
                        dist = 0
                    elif idx == (1, 1):
                        dist = 2
                    else:
                        dist = 1
                else:
                    # Segundo quadrante
                    quad = 2
                    if idx == (0, 3):
                        dist = 0
                    elif idx == (1, 2):
                        dist = 2
                    else:
                        dist = 1
            else:
                if idx[1] < 2:
                    # Terceiro quadrante
                    quad = 3
                    if idx == (3, 0):
                        dist = 0
                    elif idx == (2, 1):
                        dist = 2
                    else:
                        dist = 1
                else:
                    # Quarto quadrante
                    quad = 4
                    if idx == (3, 3):
                        dist = 0
                    elif idx == (2, 2):
                        dist = 2
                    else:
                        dist = 1

            # Tupla com valores desejados
            i, j = idx
            rk = (
                valor,
                quad,
                dist,
                olha_cima(self.mat, i, j) or olha_baixo(self.mat, i, j),
                olha_direita(self.mat, i, j) or olha_esquerda(self.mat, i, j)
            )
            rks.append(rk)

        # Se tem menos elementos do que o tamanho do rank
        if len(rks) < self.n_ranks:
            for _ in range(self.n_ranks-len(rks)):
                # Preenche com dummies
                rk = (0,0,0,False,False)
                rks.append(rk)

        # Construção da tupla de estado
        self.s = (
            (self.mat == move_up(self.mat)),
            (self.mat == move_down(self.mat)),
            (self.mat == move_left(self.mat)),
            (self.mat == move_right(self.mat)),
            *rks
        )

    def __hash__(self):
        return hash(self.s)

    def __eq__(self, outro: Estado):
        return isinstance(outro, type(self)) and self.s == outro.s

    def __str__(self):
        return str(self.s)

    def _novoEstado(self,
                    mat: None | list[list]):
        return EstadoReduzido(mat=mat)

    def recompensa(self,
                   outro: Estado,
                   acao: str) -> float:
        '''
        Retorna a recompensa por atingir
            self
        a partir de
            outro

        (outro) -r-> (self)
        '''
        assert(isinstance(outro, type(self)))

        # Movimento não evolutivo
        acoes = ['cima', 'baixo', 'esquerda', 'direita']
        for n in range(len(acoes)):
            if outro.s[n] and acao == acoes[n]:
                # Punição por movimento não evolutivo
                return -log2(self.s[4][0])

        # Recompensa positiva!
        recom = 0

        # Para cada rank
        for rank in range(4, 4+self.n_ranks):
            # Somente calcula quando a peça n é vazia
            if self.s[rank][0] != 0:
                # Valor máximo
                if self.s[rank][0] > outro.s[rank][0]:
                    recom += log2(self.s[rank][0])

                # Distância manhattan
                if (self.s[rank][1] == outro.s[rank][1] and
                    self.s[rank][2] < outro.s[rank][2]):
                    recom += 2

                # Posicionamento das peças
                if ((self.s[rank][3] and not outro.s[rank][3]) or
                    (self.s[rank][4] and not outro.s[rank][4])):
                    recom += 1

        # Caso padrão
        return recom
