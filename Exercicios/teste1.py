import bpy

# Caminho do arquivo OBJ
caminho_obj = r"C:/Users/jhona/OneDrive/Faculdade/PET/Fisioterapia 3D - Blander/Exercicios/include/cubo_teste.obj"

# Importar o arquivo OBJ
bpy.ops.import_scene.obj(filepath=caminho_obj)

# Obter o objeto importado
objeto_importado = bpy.context.selected_objects[0]  # O primeiro objeto importado será o selecionado
print(f"Objeto importado: {objeto_importado.name}")

# Manipular o objeto (exemplo: mover o objeto)
objeto_importado.location = (2.0, 3.0, 0.0)

# Salvar o arquivo Blender após a manipulação
bpy.ops.wm.save_as_mainfile(filepath=r"C:/Users/jhona/OneDrive/Faculdade/PET/Fisioterapia 3D - Blander/Exercicios/include/cena_atualizada.blend")

