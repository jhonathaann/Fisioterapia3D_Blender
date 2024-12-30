'''1. Adicionar um cubo e movê-lo no eixo Z

Objetivo: Ensinar como criar e manipular objetos básicos.

Tarefa: Usando Python, adicione um cubo na cena e mova-o 2 unidades no eixo Z.'''

import bpy
from pathlib import Path

csvpath = Path(__file__).parent / 'include' / 'cubo_teste.obj'

cubo = csvpath
print(cubo)


