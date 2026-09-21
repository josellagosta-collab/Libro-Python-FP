equipo = "SERVIDOR-01"
direccion_ip = "192.168.1.10"
estado = "ACTIVO"

with open("../datos/estado_equipo.txt", "w", encoding="utf-8") as archivo:
    archivo.write(f"Equipo: {equipo}\n")
    archivo.write(f"Dirección IP: {direccion_ip}\n")
    archivo.write(f"Estado: {estado}\n")

print("Información guardada correctamente.")