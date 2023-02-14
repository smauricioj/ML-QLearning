# -*- coding: utf-8 -*-

# Autor: Sergio P
# Data: 

# ---------------------------------------------------------------
# IMPORTS

from json import load
from pathlib import Path
import matplotlib.pyplot as plt

import Jogo2048

# ---------------------------------------------------------------
# MAIN

def main():
    # Dicionário de configurações
    with open(Path.cwd()/'conf.json',
              encoding='utf-8') as conf_file:
        conf = load(conf_file)

    # Diretórios
    conf['main_dir'] = Path.cwd().parent
    conf['result_dir'] = conf['main_dir']/'Resultados'

    # Instâncias
    ql = Jogo2048.QL2048(conf)
    # Teste de estados, usado em produção
    # ql.testaEstado()

    # Aprendizagem
    # ql.objetivo = 64
    # ql.iniciaQL()
    # ql.executa()

    # Aprendizagem Plots
    # for o in [2**x for x in range(4,10)]:
    #     ql = Jogo2048.QL2048(conf)
    #     ql.objetivo = o
    #     ql.iniciaQL()
    #     # print(ql.ql.q_size)
    #     ql.executa()
    # plt.xlabel('Episódios')
    # plt.ylabel('Tamanho Q')
    # plt.legend()
    # plt.grid()
    # plt.show()

    # Teste de jogos
    # ql.iniciaQL(file_name='q.bin')
    # c_vitorias = 0
    # for _ in range(2000):
    #     if ql.testaJogo():
    #         c_vitorias += 1
    # print(c_vitorias)

    # Geração de arquivo arff
    # ql.iniciaQL(file_name='q.bin')
    # ql.geraArff(reduzido=True)
    # ql.geraArff(reduzido=False)

if __name__ == '__main__':
    main()