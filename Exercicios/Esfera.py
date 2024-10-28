'''Escalar uma esfera

Objetivo: Praticar a escala de objetos.

Tarefa: Adicione uma esfera e redimensione-a para o dobro do tamanho no eixo X.'''

import bpy

# adicionando uma esfera na cena
# bpy.ops.mesh.primitive_uv_sphere_add(location=(2, 0, 0))
bpy.ops.mesh.primitive_uv_sphere_add()

# selecionando o obejto criado
esfera = bpy.context.active_object

# redimencionando-a para o dobro do tamanho no eixo x
esfera.scale.x *= 2
