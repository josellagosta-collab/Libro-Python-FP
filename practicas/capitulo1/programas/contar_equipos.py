contador = 0

with open("../datos/equipos.txt", "r", encoding="utf-8") as archivo:
    for linea in archivo:
        equipo = linea.strip()

        if equipo:
            contador += 1

print(f"Número de equipos: {contador}")