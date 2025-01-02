import bpy
import bmesh
import mathutils

def corte_na_horizontal(obj):
    # verifique se o objeto é do tipo MESH
    if obj.type != 'MESH':
        print("Selecione um objeto do tipo MESH.")
        return
    
    # obtenha a bounding box do objeto e a matriz de transformação do mundo
    bb = obj.bound_box
    matriz_transformacao = obj.matrix_world
    
    # converta os cantos da bounding box para coordenadas globais
    bbw = [matriz_transformacao @ mathutils.Vector(corner) for corner in bb]
    
    # calcule o valor médio de Y na bounding box
    min_z = (min(corner.z for corner in bbw) + max(corner.z for corner in bbw)) / 2
    print("Mid Y:", min_z)
    
    # entre no modo de edição
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    
    # Use o bmesh para manipulação de malha
    bm = bmesh.from_edit_mesh(obj.data)
    
    vertices_removidos = [v for v in bm.verts if (matriz_transformacao @ v.co).z > min_z]
    
    bmesh.ops.delete(bm, geom=vertices_removidos, context='VERTS')
    
    # atualize a malha
    bmesh.update_edit_mesh(obj.data)
    
    # volte ao modo de objeto
    bpy.ops.object.mode_set(mode='OBJECT')

# selecione o objeto para o qual deseja aplicar o corte
obj = bpy.context.active_object

# aplique o corte na malha
corte_na_horizontal(obj)