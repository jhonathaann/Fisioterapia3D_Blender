import bpy
import mathutils

# Selecionar o cubo
cubo = bpy.context.object

# obtendo a matriz de transformacao do objeto
matriz_transformacao = cubo.matrix_world

# percorrendo os vertices e convertendo p
vertices_mundo = [matriz_transformacao @ vert.co for vert in cubo.data.vertices]


max_z = max(vertices_mundo, key=lambda v: v.z)
min_z = min(vertices_mundo, key=lambda v: v.z)

min_aux = min_z[2]

while min_aux < max_z[2]:
    
    # criando o plano
    bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, min_aux))

    # selecionando o plano
    plano = bpy.context.object

    # Escalar o plano para cobrir o cubo
    plano.scale = (2, 2, 1)  # Ajuste conforme o tamanho do cubo

    # posicionando o plano no meio do cubo
    plano.location = (
    cubo.location.x + min_aux,
    cubo.location.y + min_aux,
    cubo.location.z + min_aux
    )
    
    min_aux += 0.5
    




