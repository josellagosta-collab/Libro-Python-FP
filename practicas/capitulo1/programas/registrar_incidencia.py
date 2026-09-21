nombre_equipo = input("Nombre del equipo: ")
descripcion = input("Descripción de la incidencia: ")

with open("../datos/incidencias.txt", "a", encoding="utf-8") as archivo:
    archivo.write(f"{nombre_equipo} - {descripcion}\n")

print("Incidencia registrada correctamente.")
