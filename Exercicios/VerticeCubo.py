'''Modificar vértices de um objeto
Objetivo: Trabalhar com os vértices de uma malha.

Tarefa: Selecionar um vértice de um cubo e movê-lo 1 unidade no eixo X.'''

import bpy
import bmesh

# adicionando o cubo na cena
#bpy.ops.mesh.primitive_cube_add()

# selecionando o cubo na cena
cubo = bpy.data.objects.get("Cubo")

# se o cubo foi selecionado
if cubo:
    # tornando o cubo um objeto ativo (selecionando ele)
    bpy.context.view_layer.objects.active = cubo
    # entrando no modo edicao
    bpy.ops.object.mode_set(mode='EDIT')
    
    # criando uma malha editavel a partir do objeto selecionado
    mesh = bmesh.from_edit_mesh(cubo.data)
    
    # selecionando o primeiro vertice da malha e movendo ele em 1 unidade no eixo x
    vertice = mesh.verts[0]
    vertice.co.x += 1
    
    # atualizando a malha para aplicar as mudanças
    bmesh.update_edit_mesh(cubo.data)
    
    # voltando ao modo de objeto
    bpy.ops.object.mode_set(mode='OBJECT')

else:
    print("objeto nao foi selecionado")
