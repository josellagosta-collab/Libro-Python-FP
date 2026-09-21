import csv

with open("../datos/inventario.csv", "r", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)

    for equipo in lector:
        print(f"Nombre: {equipo['nombre']}")
        print(f"IP: {equipo['ip']}")
        print(f"Sistema: {equipo['sistema']}")
        print(f"Ubicación: {equipo['ubicacion']}")
        print("-------------------------")