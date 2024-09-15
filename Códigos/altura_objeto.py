import bpy
import mathutils

def demarcar_alturas(obj, tamaho_esfera):
    # verificando se o objeto é do tipo MESH
    if obj.type != "MESH":
        print("Selecione um objeto do tipo MESH")
        return
    
    # obtendo a matriz de transformaçao do objeto
    matriz_transformacao = obj.matriz_world

    # percorrendo os vertices e converntendo para coordenadas globais
    vertices_mundo = [matriz_transformacao @ vert.co for vert in obj.data.vertices]

    # encontrando as coordenadas maximas e minimas no eixo z
    min_z = min(vertices_mundo, key=lambda v: v.z)
    max_z = max(vertices_mundo, key=lambda v: v.z)
    
    #print(f"Coordenada mais baixa (Z min): {min_z}")
    #print(f"Coordenada mais alta (Z max): {max_z}")

    # adicionando esferas no objeto para visualizar as coordenadas
    bpy.ops.mesh.primitive_uv_sphere_add(radius=tamaho_esfera, local=min_z)
    esfera_min = bpy.context.active_object
    esfera_min.name = "Esfera_Mais_Baixa"


    bpy.ops.mesh.primitive_uv_sphere_add(radius=tamaho_esfera, local=max_z)
    esfera_max = bpy.context.active_object
    esfera_max.name = "Esfera_Mais_Alta"

     # Alterar a cor das esferas para destacar
    mat_min = bpy.data.materials.new(name="MaterialMin")
    mat_min.diffuse_color = (0, 0, 1, 1)  # Azul para o ponto mais baixo
    esfera_min.data.materials.append(mat_min)
    
    mat_max = bpy.data.materials.new(name="MaterialMax")
    mat_max.diffuse_color = (1, 0, 0, 1)  # Vermelho para o ponto mais alto
    esfera_max.data.materials.append(mat_max)
    
    #print("Esferas adicionadas para marcar a coordenada mais baixa e mais alta.")

# selecionando o objeto
obj = bpy.context.active_object

demarcar_alturas(obj, tamaho_esfera=0.5)
