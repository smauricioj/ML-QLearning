# -*- coding: utf-8 -*-

# Autor: Sergio P
# Data: 30/09/2022

# ---------------------------------------------------------------
# IMPORTS

from dataclasses import dataclass
from .Estado import Estado

# ---------------------------------------------------------------
# CLASSES

@dataclass(frozen=True,repr=True,eq=True)
class ParSA:
    ''' Classe que representa um par estado-ação '''

    s: Estado
    ''' Estado, pode ser herdado para implementação específica '''

    a: str
    ''' Ação, uma string representando '''