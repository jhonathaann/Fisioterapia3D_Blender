''' Objetivo: Trabalhar com combinações de objetos.
Tarefa: Adicione um cubo e uma esfera, 
alinhe a esfera sobre o cubo e combine os dois objetos em um só.'''

import bpy

# adicionando o cubo
bpy.ops.mesh.primitive_cube_add(size=2, location=(0,0,0))
cubo = bpy.context.object # acessando o obejto cubo

# adicionando uma esfera
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0,0,1.5))
esfera = bpy.context.object  # acessando o objeto esfera

# selecionando ambos os objetos
bpy.ops.object.select_all(action='DESELECT')
cubo.select_set(True)
esfera.select_set(True)
bpy.context.view_layer.objects.active = cubo

# juntando os dois obejtos
bpy.ops.object.join()
