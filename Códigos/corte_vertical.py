import bpy
import bmesh
import mathutils

def corte_na_vertical(obj):
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
    min_y = (min(corner.y for corner in bbw) + max(corner.y for corner in bbw)) / 2
    print("Mid Y:", min_y)
    
    # entre no modo de edição
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    
    # Use o bmesh para manipulação de malha
    bm = bmesh.from_edit_mesh(obj.data)
    
    # itere sobre os vértices e remova os que estão acima do meio da bounding box em Y
    # estando acima do y, nos ficamos com a parte de traz do modelo
    # OBS: essa logica funcionou em alguns modelos (ou seja, ficou apenas a parte das costas do modelo)
    # mas em alguns outros modelos não funcionou muito bem
    vertices_removidos = [v for v in bm.verts if (matriz_transformacao @ v.co).y > min_y]
    
    bmesh.ops.delete(bm, geom=vertices_removidos, context='VERTS')
    
    # atualize a malha
    bmesh.update_edit_mesh(obj.data)
    
    # volte ao modo de objeto
    bpy.ops.object.mode_set(mode='OBJECT')

# selecione o objeto para o qual deseja aplicar o corte
obj = bpy.context.active_object

# aplique o corte na malha
corte_na_vertical(obj)
