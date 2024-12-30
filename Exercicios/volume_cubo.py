import bpy

# salvando as informacoes do cubo em uma variavel
cubo = bpy.data.objects.get('Cube')

if cubo:

    # coletando as dimensoes do objeto
    dimensoes = cubo.dimensions
    # dimensoes = [tamanho em x, tamanho em y, tamanho em z]

    volume = dimensoes[0] *  dimensoes[1] * dimensoes[2]

    print(f"Volume do cubo {volume}")

else:
    print("cubo nao encontrado")