import bpy

# parametros do cilindro
raio = 1.0     # raio da base do cilindro
altura = 2.0   # altura do cilindro
vertices = 32  # numero de vertices para a base circular
localizacao = (0,0,0)  # localizacao do cilindro no espcaço

# criando o cilindro
bpy.ops.mesh.primitive_cylinder_add(
    radius = raio,
    depth = altura,
    vertices = vertices,
    location = localizacao

)


