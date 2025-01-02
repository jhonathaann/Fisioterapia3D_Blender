import bpy
import math

# selecionando o objeto e salvando as suas info em uma variavel
obj = bpy.context.object

if obj and obj.type == 'MESH':
    # acessando a malha do objeto
    mesh = obj.data
    
    quant_vertices = len(obj.data.vertices)

    coord_x = []
    coord_y = []
    coord_z = []
    
    for vert in mesh.vertices:
        
        coord_x.append(vert.co.x) # salvando as coord de x
        coord_y.append(vert.co.y) # salvando as coord de y
        coord_z.append(vert.co.z) # salvando as coord de z
    
    perimetro = 0 
    for i in range(quant_vertices-1):
        
        # pegando as coord de um ponto
        x1,y1,z1 = coord_x[i], coord_y[i], coord_z[i]
        
        # pegando as coord do ponto seguinte
        x2,y2,z2 = coord_x[i+1], coord_y[i+1], coord_z[i+1]
        
        perimetro += math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    
    print(f"perimetro do objeto {obj.name} : {perimetro}")
else:
    print("nao foi selecionando um objeto do tipo MESH")
