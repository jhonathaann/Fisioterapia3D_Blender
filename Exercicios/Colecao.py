'''Criar uma coleção e mover objetos para ela

Objetivo: Organizar a cena com coleções.

Tarefa: Crie uma nova coleção e mova o cubo e a esfera para dentro dela.'''

import bpy

# adicionando um cubo na tela
bpy.ops.mesh.primitive_cube_add()

# selecionando o cubo
cubo = bpy.context.active_object

# adicioando uma esfera na tela
bpy.ops.mesh.primitive_uv_sphere_add(location=(3, 0, 0))

# selecionando o obejto criado
esfera = bpy.context.active_object

# criando uma nova colecao
nova_colecao = bpy.data.collections.new("MinhaColecao")
bpy.context.scene.collection.children.link(nova_colecao)

# encontrando o cubo e a esfera na cena
cubo = bpy.data.objects.get("Cubo")
esfera = bpy.data.objects.get("Esfera UV")

# adicioando o cubo na nova colecao
nova_colecao.objects.link(cubo)
# adicioando o cubo na nova colecao
nova_colecao.objects.link(esfera)

# apagando os objetos da colecao antiga
bpy.context.scene.collection.objects.unlink(cubo)
bpy.context.scene.collection.objects.unlink(esfera)

