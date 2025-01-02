import bpy


radius = 1.0        # raio
vertices = 32       # vertices (quanto maior, mais suave sera a circunferencia)
location = (0, 0, 0)  # localizacao dela
rotation = (0, 0, 0)  # rotacao dela

# Cria a circunferência
bpy.ops.mesh.primitive_circle_add(
    vertices=vertices,
    radius=radius,
    location=location,
    rotation=rotation
)

print("circunferencia criada com sucesso!")
