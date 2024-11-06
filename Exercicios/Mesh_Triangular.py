# give python access to blender's functionality
import bpy

# extend python's math functionality
import math

# create variables used in the loop
radius_step = 0.1
current_radius = 0.1
number_triangles = 50

for i in range(number_triangles):

    # add a triangle mesh into the scene
    current_radius = current_radius + radius_step;  # raio atual
    bpy.ops.mesh.primitive_circle_add(vertices=3, radius=current_radius)


    # get a reference to the currently active object
    triangle_mesh = bpy.context.active_object

    # rotate mesh about the x-axis
    #triangle_mesh.rotation_euler.x = math.radians(-90)
    graus = -90
    radianos = math.radians(graus)
    triangle_mesh.rotation_euler.x = radianos

    # convert mesh into a curve (convertendo a malha para uma curva)
    bpy.ops.object.convert(target='CURVE')

    # add a bevel to curve
    #bpy.context.object.data.bevel_depth = 0.12
    #bpy.context.object.data.bevel_resolution = 16
    triangle_mesh.data.bevel_depth = 0.05
    triangle_mesh.data.bevel_resolution = 16

    # shade smooth (suavizando a sombra)
    bpy.ops.object.shade_smooth()