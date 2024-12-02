'''a ideia é, dado um cubo na cena, criar um plano com que intersecte este cubo, de
modo que no ponto de intersecao seja criado uma esfera'''


import bpy
import bmesh
from mathutils import Vector

# funcao que cria um plano
def criando_plano(location=(0, 0, 0), size=2.0):
    bpy.ops.mesh.primitive_plane_add(size=size, location=location)
    plano = bpy.context.object
    plano.name = "plano"
    return plano

# funcao para adicionar uma esfera na posicao especifica
def add_sphere(location, radius=0.1):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)

# obtendo o cubo na cena
cubo = bpy.data.objects.get("cubo")
if not cubo:
    print("Erro")

# criando o plano
plano = criando_plano(location=(0, 0, 1))

# tornando o cubo editavel
bpy.context.view_layer.objects.active = cubo
bpy.ops.object.mode_set(mode='EDIT')

# criando uma bmesh para o cubo
bm = bmesh.from_edit_mesh(cubo.data)

# adicionando uma nova geometria para a interseco com o plano
plane_normal = plano.matrix_world.to_quaternion() @ Vector((0, 0, 1))
plane_point = plano.matrix_world.translation

geom, intersections = bmesh.ops.bisect_plane(
    bm,
    geom=bm.verts[:] + bm.edges[:] + bm.faces[:],
    plane_co=plane_point,
    plane_no=plane_normal,
    use_snap_center=True,
)

# saindo do modo edicao para aplicar as alteracoes
bmesh.update_edit_mesh(cubo.data)
bpy.ops.object.mode_set(mode='OBJECT')

# adicionando as esferas nas posicoes de intercçao
for vert in intersections:
    if isinstance(vert, bmesh.types.BMVert):
        add_sphere(location=cubo.matrix_world @ vert.co)
