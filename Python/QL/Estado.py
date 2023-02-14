# -*- coding: utf-8 -*-

# Autor: Sergio P
# Data: 30/09/2022

# ---------------------------------------------------------------
# IMPORTS

from dataclasses import dataclass

# ---------------------------------------------------------------
# CLASSES

@dataclass(eq=True)
class Estado:
    ''' Classe para herança e garantir hash '''

    def __hash__(self):
        ''' Necessário sobrescrever '''
        return 0