import bpy
import math

###  assumindo que esse cilindro tem uma base circular ###

# salvando as info do cilindro em uma variavel
cilindro = bpy.data.objects.get('Cylinder')

if cilindro:

    # coletando as dimensoes do cilindro
    dimensoes = cilindro.dimensions

    raio = dimensoes[0]/2  # raio esta no eixo x
    altura = dimensoes[2]  # altura esta no eixo z

    area_base = 2 * math.pi * (raio * raio)
    areal_lateral = 2 * math.pi * raio * altura  # area do retanuglo, que eh a parte lateral do cilindro

    print(f"area total do cilindro {area_base+areal_lateral}")

else:
    print("Cilindro NAO encontrado")
