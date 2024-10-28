'''1. Adicionar um cubo e movê-lo no eixo Z

Objetivo: Ensinar como criar e manipular objetos básicos.

Tarefa: Usando Python, adicione um cubo na cena e mova-o 2 unidades no eixo Z.'''

import bpy

# adicionando o objeto na cena
bpy.ops.mesh.primitive_cube_add()

# selecionando o objeto criado
cubo = bpy.context.active_object

# andando com o obejto no eixo z
cubo.location.z += 2