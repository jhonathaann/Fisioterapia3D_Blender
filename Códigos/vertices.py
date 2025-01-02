import bpy

# selecionando o objeto e salvando as suas info em uma variavel
obj = bpy.context.object

if obj and obj.type == 'MESH':
    # acessando a malha do objeto
    mesh = obj.data
    
    quant_vertices = len(obj.data.vertices)

    print(f"o objeto {obj.name} possui {quant_vertices} vertices")
    
    print(f"vertices do objeto '{obj.name}':")
    for vert in mesh.vertices:
        print(f"vertice {vert.index}: {vert.co}")
else:
    print("nao foi selecionando um objeto do tipo MESH")
