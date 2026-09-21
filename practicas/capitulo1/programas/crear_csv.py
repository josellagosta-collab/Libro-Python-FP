import csv

with open("../datos/nuevo_inventario.csv", "w", encoding="utf-8", newline="") as archivo:
    escritor = csv.writer(archivo)

    escritor.writerow(["nombre", "ip", "sistema", "ubicacion"])
    escritor.writerow(["PC-AULA-01", "192.168.1.101", "Windows 11", "Aula 1"])
    escritor.writerow(["SERVIDOR-01", "192.168.1.10", "Ubuntu Server", "CPD"])

print("Archivo CSV creado correctamente.")r