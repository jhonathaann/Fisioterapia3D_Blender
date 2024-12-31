import bpy

objeto = bpy.data.objects.get('B370')

if objeto:
    
    bpy.context.view_layer.objects.active = objeto
    objeto.select_set(True)
    
    objeto.location = (0,0,0)
    
else:
    
    print("Objeto nao encontrado")