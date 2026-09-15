with open("../datos/equipos.txt", "r", encoding="utf-8") as archivo:
    for linea in archivo:
        equipo = linea.strip()
        print(f"Procesando equipo: {equipo}")