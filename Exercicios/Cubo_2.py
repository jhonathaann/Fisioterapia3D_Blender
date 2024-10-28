'''Manipulando um objeto ja criado, sem criar um objeto novo toda vez'''

import bpy

# selecionando o obejto pelo nome
cubo = bpy.data.objects.get("Cubo")

# verificando se o cubo existe
if cubo:
    # tornando o cubo um objeto ativo (ou seja, selecioando ele)
    bpy.context.view_layer.objects.active = cubo
    cubo.select_set(True)

    # movendo o cubo para uma nova coordenada
    cubo.location.x += 2
    cubo.location.y += 2
    cubo.location.z += 2

else:
    print("O cubo nao foi encontrado")   