''' Rotacionar um objeto em torno do eixo Y

Objetivo: Introduzir rotação de objetos.

Tarefa: Rotacione o cubo criado no exercício anterior em 45 graus no eixo Y.'''

import bpy

# selecionar o objeto pelo nome
cubo = bpy.data.objects.get("Cubo")

# verificando se o objeto foi selecionado
if cubo:
    # tornando o cubo um objeto ativo
    bpy.context.view_layer.objects.active = cubo
    cubo.select_set(True)

    # rotacionando o cubo em 45° graus no eixo y
    cubo.rotation_euler[1] += 0.7854
else:
    print("Cubo nao encontrado")