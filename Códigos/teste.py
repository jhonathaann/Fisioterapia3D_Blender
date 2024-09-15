import bpy
import mathutils

def cortes_horizontais(obj, intervalo_corte=1.0, tamanho_plano=10.0):
    # Verifique se o objeto é do tipo MESH
    if obj.type != 'MESH':
        print("Selecione um objeto do tipo MESH.")
        return
    
    # Aplique as transformações de escala e rotação ao objeto
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    
    # Obtenha a matriz de transformação do objeto
    matriz_transformacao = obj.matrix_world
    
    # Converta os vértices para coordenadas globais e encontre Z min e Z max
    vertices_mundo = [matriz_transformacao @ vert.co for vert in obj.data.vertices]
    min_z = min(vertices_mundo, key=lambda v: v.z).z
    max_z = max(vertices_mundo, key=lambda v: v.z).z
    
    print(f"Coordenada Z mínima: {min_z}")
    print(f"Coordenada Z máxima: {max_z}")
    
    # Entre no modo de edição do objeto
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Adicione planos de corte horizontais ao longo do eixo Z
    z_atual = min_z
    while z_atual <= max_z:
        bpy.ops.mesh.bisect(
            plane_co=(0, 0, z_atual),
            plane_no=(0, 0, 1),
            use_fill=False,
            clear_inner=False,
            clear_outer=False
        )
        z_atual += intervalo_corte
    
    # Atualize a malha
    bpy.ops.mesh.delete(type='FACE')  # Opcional: Remover faces não desejadas
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Adicionar planos de visualização (opcional)
    for z in range(int(min_z), int(max_z)+1, int(intervalo_corte)):
        bpy.ops.mesh.primitive_plane_add(size=tamanho_plano, location=(0, 0, z))
        plano = bpy.context.active_object
        plano.name = f"Plano_Corte_{z:.1f}"
        
        # Alterar a cor dos planos para destacar
        mat = bpy.data.materials.new(name=f"MaterialPlano_{z:.1f}")
        mat.diffuse_color = (1, 0, 0, 0.5)  # Vermelho semi-transparente
        plano.data.materials.append(mat)
    
    print("Cortes horizontais realizados e planos de visualização adicionados.")

# Selecione o objeto no qual deseja realizar os cortes
obj = bpy.context.active_object

# Chame a função para realizar os cortes horizontais
cortes_horizontais(obj, intervalo_corte=1.0, tamanho_plano=10.0)
