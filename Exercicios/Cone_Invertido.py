import bpy

# adicionando um cone
bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=1,depth=2,location=(0,0,0))

# selecionando o cone
cone = bpy.context.object

# redimensionando a base
bpy.ops.transform.resize(value=(2,2,1))

# rotaciona o cone em 180graus no eixo z
bpy.ops.transform.rotate(value=3.1459, orient_axis='Z')

