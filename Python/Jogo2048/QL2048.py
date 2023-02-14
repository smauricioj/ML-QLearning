# -*- coding: utf-8 -*-

# Autor: Sergio P
# Data: 16/09/2022

# ---------------------------------------------------------------
# IMPORTS

from pathlib import Path
from random import choice
from math import log2, factorial
import pickle
import matplotlib.pyplot as plt

from QL import QLearning
from . import Estado2048
 
# ---------------------------------------------------------------
# CLASSES
        
class QL2048:
    ''' Executa o algoritmo de Q-Learning no jogo 2048 '''

    n_episodios: int
    ''' Nº de episodios do algoritmo '''

    objetivo: int
    ''' Qual valor objetivo a aprendizagem quer definir '''

    q_size: int
    ''' Qual tamanho previsto da tabela Q '''

    def __init__(self, conf: dict):
        self.conf = conf
        self.acoes = ['cima','baixo','direita','esquerda']
        self.ql = None
        self.n_episodios = 30_000
        self.objetivo = 128
        self.arff_examples = []

    def iniciaQL(self, file_name: None | Path = None):
        if file_name:
            self.ql = QLearning.carregarQ(self.conf['result_dir']/file_name)
            self.acoes = self.ql.acoes
        else:
            self.ql = QLearning(self.acoes)

            # Hiper parâmetros
            self.ql.epsilon = 0.95 # Exploração no começo
            self.ql.epsilonDec = (1.0/self.n_episodios)/100
            # self.ql.epsilonDec = 0 # sem decaimento
            self.ql.epsilonMin = 0.5 # Meio a meio no final

            self.ql.alpha = 0.75 # Taxa de aprendizagem alta
            self.ql.alphaDec = (1.0/self.n_episodios)/1000
            # self.ql.alphaDec = 0 # sem decaimento

            # Tamanho previsto para tabela Q

            def beta(o,n):
                return (factorial(int(log2(o))))/(factorial(int(log2(o))-n))

            def q_size(o,n):
                return (2**(4*(n+1)))*(3**n)*(beta(o,n))

            n = Estado2048.EstadoReduzido.n_ranks
            assert(log2(self.objetivo)-n >= 0)

            self.ql.q_size = len(self.acoes)*q_size(self.objetivo, n)

    def novoEstado(self, mat):
        '''
        Cria um novo estado
        Função usada pra testar tipos de estados diferentes
        '''
        # return Estado2048.EstadoJogo(mat)
        return Estado2048.EstadoReduzido(mat)

    def testaEstado(self):
        '''
            Método usado para testar os estados durante produção
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        '''

        i = self.novoEstado(mat=[
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,4],
            [0,0,0,4]
        ])
        j = self.novoEstado(mat=[
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,4],
            [0,0,0,8]            
        ])
        print(*i.mat,sep='\n')
        print(i)

        print(*j.mat,sep='\n')
        print(j)
        print('-'*20)
        print(j.recompensa(i,'baixo'))
        print('-'*20)

    def testaJogo(self,
                  pausado: bool = False,
                  arff: bool = False,
                  arff_reduzido: bool = True):
        ''' Testa a tabela Q para tentar vencer o jogo '''

        # Estado inicial aleatório
        i = self.novoEstado(mat=None)
        a = None

        # Contador de tentativas falhas
        conta_tentativas = 0

        while True:
            # Pausado é para ver o jogo acontecendo
            if pausado:    
                print(f'Ação: {a}')            
                print(*i.mat,sep='\n')
                print(i)
                x = input('c: ')
                if x == 'n':
                    exit()

            # Escolhe a melhor ação possível
            if conta_tentativas < 2:
                if arff:
                    rand_choice = False
                a = self.ql.argmaxQ(i)
            else:
                if arff:
                    rand_choice = True
                a = choice(self.ql.acoes)

            # Simula a ação
            j = i.simularAcao(a)

            # Define se adiciona uma nova célula
            if i.mat == j.mat:
                # Se o estado não mudou, só continua
                c = True
                conta_tentativas += 1
            else:
                # Se o estado mudou, adiciona
                c = j.continua()
                conta_tentativas = 0

            # Se j é terminal ou não conseguiu adicionar célula, termina
            if j.terminal(self.objetivo) or not c:
                return j.vitoria(self.objetivo)
            else:
                # Salva o exemplo de atuação para arquivo arff
                if arff and not rand_choice:
                    s = i.s
                    if arff_reduzido:
                        line = ''
                    else:
                        line = f"'{s[0]}','{s[1]}','{s[2]}','{s[3]}',"
                    for rank in range(4,7):
                        if s[rank][0] != 0:
                            for e in range(5):
                                line += f"'{s[rank][e]}',"
                        else:
                            line += "?,?,?,?,?,"
                    line += f"'{a}'\n"
                    self.arff_examples.append(line)
                i = j

    def geraArff(self,
                 file_name: None | str = None,
                 reduzido: bool = True):
        '''
        Gera um arquivo .arff com exemplos da aplicação
        da tabela Q no jogo 2048
        '''
        if not file_name:
            file_name = f'q_o_{self.objetivo}_reduzido_{reduzido}.arff'

        with open(self.conf['result_dir']/file_name, 'w') as file:
            file.write("@relation decisao-jogo\n")

            if not reduzido:
                file.write("@attribute flush-cima {'True','False'}\n")
                file.write("@attribute flush-baixo {'True','False'}\n")
                file.write("@attribute flush-esquerda {'True','False'}\n")
                file.write("@attribute flush-direita {'True','False'}\n")

            for rank in range(1,4):
                file.write(f"@attribute rank-{rank}-valor ")
                # Editar para objetivo!
                file.write("{'2','4','8','16','32','64','128'}\n")
                file.write(f"@attribute rank-{rank}-quadrante {{'1','2','3','4'}}\n")
                file.write(f"@attribute rank-{rank}-distancia {{'0','1','2'}}\n")
                file.write(f"@attribute rank-{rank}-vertical {{'True','False'}}\n")
                file.write(f"@attribute rank-{rank}-horizontal {{'True','False'}}\n")

            file.write("@attribute decisao {'cima','baixo','esquerda','direita'}\n")
            file.write("@data\n")

            for _ in range(2000):
                self.testaJogo(
                    pausado=False,
                    arff=True,
                    arff_reduzido=reduzido
                )
                for line in self.arff_examples:
                    file.write(line)
                self.arff_examples.clear()

    def executa(self):
        ''' Executa o QLearning '''

        # Verifica se QL está instanciado
        if isinstance(self.ql, type(None)):
            raise ValueError('QL não instanciado')

        # Estado inicial do jogo é aleatório '''
        i = self.novoEstado(mat=None)
        j = None
        a = None
        r = None

        # Contadores
        episodio = 0

        # Plots
        x, y = [], []

        while episodio <= self.n_episodios:
            # Escolhe uma ação
            a = self.ql.acaoExploraçãoGreedy(i)

            # Define o próximo estado
            j = i.simularAcao(a)

            # Procura recompensa
            r = j.recompensa(i, a)

            # Atualiza tabela
            self.ql.atualizaQ(i, a, j, r)

            # Se ouve mudança na situação de jogo
            c = True
            if i.mat != j.mat:
                # Tenta adicionar uma nova peça
                c = j.continua()

            # Se terminou o jogo
            if j.terminal(self.objetivo) or not c:
                if episodio % 1_000 == 0:
                    # Meta-dados
                    print(f'\nEpisódio: {episodio}; {self.ql}')
                    if episodio != 0:
                        self.ql.salvarQ(self.conf['result_dir'])

                elif episodio % 1_00 == 0:
                    # Tenta um jogo
                    print('\tResultado: (', end='', flush=True)
                    if self.testaJogo():
                        print('+)')
                    else:
                        print('-)')

                if episodio % 100 == 0:
                    # Plots
                    x.append(episodio)
                    y.append(self.ql.tamanhoTabelaQ)

                # Começa um novo episódio
                episodio += 1
                i = self.novoEstado(mat=None)
            else:
                # Continua
                i = j

        # Plot final
        plt.plot(x, y, label=f'o={self.objetivo}')

