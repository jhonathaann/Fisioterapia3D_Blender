import bpy

# função para redimensionar um objeto
def scale_object(obj, scale_factor):
    # ferifique se o objeto é do tipo MESH
    if obj.type != 'MESH':
        print("Selecione um objeto do tipo MESH.")
        return
    
    # aplique a escala ao objeto
    obj.scale *= scale_factor
    
    # atualize a cena para aplicar a transformação
    bpy.context.view_layer.update()

# selecione o objeto para o qual deseja redimensionar a escala
obj = bpy.context.active_object

# Defina o fator de escala (por exemplo, 0.5 para diminuir pela metade)
scale_factor = 0.5

# redimensione o objeto
scale_object(obj, scale_factor)
