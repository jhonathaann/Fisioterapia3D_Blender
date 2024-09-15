import bpy
import mathutils

def cortes_horizontais(obj, intervalo_corte=1.0, tamanho_plano=10.0):
    # verificando se o objeto selecionado é do tipo MESH
    if obj.type != "MESH":
        print("Selecione um objeto do tipo MESH.")
        return
    
    # aplicando as transformaçoes de escala e rotaçao ao objeto
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # obtendo a matriz de transformacao do objeto
    matriz_transformacao = obj.matrix_world

    # convertendo os vertices para coordenadas globais e encontrando z min e Z max
    vertices_mundo = [matriz_transformacao @ vert.cor for vert in obj.data.vertices]
    min_z = min(vertices_mundo, key=lambda v: v.z).z
    max_z = max(vertices_mundo, key=lambda v: v.z).z

    # entrando no modo ediçao do objeto
    bpy.context.view_layer.objects.ative = obj
    bpy.ops.object.mode_set(mode='EDIT')

    # adicionando os planos de corte horizontais ao longo de eixo Z
    # e que estao compreendidos na altura do objeto
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
    
    # atualizando a malha
    bpy.ops.mesh.delete(type='FACE')
    bpy.ops.object.mode_set(mode='OBJECT')

    # adicionando os planos para visualizacao
    for z in range(int(min_z), int(max_z)+1, int(intervalo_corte)):
        bpy.ops.mesh.primitive_plane_add(size=tamanho_plano, location=(0,0,z))
        plano = bpy.context.active_object
        plano.name = f"Plano_Corte_{z:.1f}"

        # alterando a cor dos planos
        mat = bpy.data.materials.new(name=f"MaterialPlano_{z:.1f}")
        mat.diffuse_color=(1,0,0,0.5) # vermelho semi-transparente
        plano.data.materials.append(mat)


# selecionando o objeto no qual sera realizado os cortes
obj = bpy.context.active_object

cortes_horizontais(obj, intervalo_corte=1.0, tamanho_plano=10.0)
