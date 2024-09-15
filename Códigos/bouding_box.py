import bpy
import mathutils

# função para visualizar a bouding box de um objeto
def create_bounding_box(obj):

    # verifique se o objeto é do tipo MESH
    if obj.type != 'MESH':
        print("Selecione um objeto do tipo MESH.")
        return
    
    # Obtenha a bounding box do objeto e a matriz de transformação do mundo
    bb = obj.bound_box
    matrix_world = obj.matrix_world
    
    # converta os cantos da bounding box para coordenadas globais
    bbw = [matrix_world @ mathutils.Vector(corner) for corner in bb]
    
    # Crie uma nova malha para a bounding box
    bb_mesh = bpy.data.meshes.new(name="BoundingBox")
    bb_object = bpy.data.objects.new("BoundingBox", bb_mesh)
    bpy.context.collection.objects.link(bb_object)
    
    # defina os vértices e arestas da bounding box
    verts = [v[:] for v in bbw]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # base inferior
        (4, 5), (5, 6), (6, 7), (7, 4),  # topo superior
        (0, 4), (1, 5), (2, 6), (3, 7)   # arestas verticais
    ]
    faces = []
    
    # crie a malha
    bb_mesh.from_pydata(verts, edges, faces)
    bb_mesh.update()
    

# selecione o objeto para o qual deseja visualizar a bounding box
obj = bpy.context.active_object

# crie e visualize a bounding box
create_bounding_box(obj)
