import csv

busqueda = input("Introduce el nombre del equipo: ")

encontrado = False

with open("../datos/inventario.csv", "r", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)

    for equipo in lector:
        if equipo["nombre"] == busqueda:
            print()
            print("Equipo encontrado")
            print("-----------------")
            print(f"Nombre: {equipo['nombre']}")
            print(f"IP: {equipo['ip']}")
            print(f"Sistema: {equipo['sistema']}")
            print(f"Ubicación: {equipo['ubicacion']}")

            encontrado = True
            break

if not encontrado:
    print("El equipo no existe en el inventario.")