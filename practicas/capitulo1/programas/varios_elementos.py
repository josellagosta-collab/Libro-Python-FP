equipos = [
    "PC-AULA-01",
    "PC-AULA-02",
    "PC-AULA-03",
    "SERVIDOR-01",
    "ROUTER-01"
]

with open("../datos/inventario.txt", "w", encoding="utf-8") as archivo:
    for equipo in equipos:
        archivo.write(equipo + "\n")

print("Inventario generado correctamente.")