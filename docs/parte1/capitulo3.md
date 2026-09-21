# Automatización de tareas repetitivas

## 1. Introducción

En los capítulos anteriores hemos aprendido dos grupos de herramientas fundamentales para la administración de sistemas.

En el **capítulo 1** aprendimos a trabajar con:

```text
Archivos
Directorios
CSV
os
pathlib
```

En el **capítulo 2** aprendimos a utilizar:

```text
subprocess
hostname
ipconfig
ping
systeminfo
PowerShell
```

Ahora vamos a combinar estos conocimientos para conseguir uno de los principales objetivos del scripting:

> **Automatizar tareas repetitivas.**

Un administrador puede necesitar realizar una misma operación sobre muchos equipos, archivos o directorios.

Por ejemplo:

```text
Comprobar 1 equipo
Comprobar 2 equipos
Comprobar 3 equipos
...
Comprobar 30 equipos
```

Podríamos realizar las comprobaciones manualmente, pero sería lento y propenso a errores.

Python permite transformar ese trabajo en:

```text
Lista de equipos
       ↓
      Python
       ↓
 repetir automáticamente
       ↓
 ejecutar operación
       ↓
 guardar resultados
```

Este será el objetivo principal del capítulo.

---

## 2. ¿Qué significa automatizar?

Automatizar consiste en conseguir que un programa realice de forma automática una tarea que normalmente tendríamos que repetir manualmente.

Supongamos que queremos comprobar tres equipos.

Manualmente podríamos ejecutar:

```powershell
ping 192.168.1.10
ping 192.168.1.11
ping 192.168.1.12
```

Si tenemos 50 equipos, tendríamos que escribir 50 comandos.

Python puede hacerlo utilizando una lista y un bucle.

Por ejemplo:

```python
equipos = [
    "192.168.1.10",
    "192.168.1.11",
    "192.168.1.12"
]

for equipo in equipos:
    print(equipo)
```

Resultado:

```text
192.168.1.10
192.168.1.11
192.168.1.12
```

El bucle:

```python
for equipo in equipos:
```

hace que Python repita automáticamente las instrucciones para cada elemento de la lista.

Este mecanismo será una de las bases de la automatización.

---

### De una tarea manual a una tarea automática

Podemos representar el proceso de esta forma:

```text
TAREA MANUAL

ping equipo1
ping equipo2
ping equipo3
ping equipo4
...
```

frente a:

```text
AUTOMATIZACIÓN

lista de equipos
      ↓
   bucle for
      ↓
     ping
      ↓
resultado de cada equipo
```

La ventaja aumenta cuanto mayor es el número de elementos que debemos procesar.

!!! example "Ejemplo"

    Imagina que administramos un aula con 30 ordenadores.

    Comprobar manualmente todos los equipos supondría ejecutar 30 veces el comando `ping`.

    Con Python podemos escribir el código una sola vez y dejar que el programa realice las 30 comprobaciones.

---

## 3. Preparar las prácticas del capítulo

Dentro de nuestra carpeta:

```text
practicas/
```

crea:

```text
capitulo3/
```

Dentro crea:

```text
datos/
programas/
resultados/
```

La estructura será:

```text
practicas/
├── capitulo1/
├── capitulo2/
│
└── capitulo3/
    ├── datos/
    ├── programas/
    └── resultados/
```

Durante este capítulo utilizaremos:

```text
datos
```

para almacenar la información de entrada.

```text
programas
```

para nuestros scripts Python.

Y:

```text
resultados
```

para los informes generados automáticamente.

---

## 4. Automatizar una prueba de conectividad

Vamos a recuperar lo aprendido en el capítulo anterior.

Podíamos comprobar un equipo mediante:

```python
import subprocess

resultado = subprocess.run(
    ["ping", "-n", "2", "127.0.0.1"],
    capture_output=True,
    text=True
)

if resultado.returncode == 0:
    print("RESPONDE")
else:
    print("NO RESPONDE")
```

Ahora queremos realizar la misma operación sobre varios equipos.

Dentro de:

```text
practicas/capitulo3/programas/
```

crea:

```text
comprobar_varios_equipos.py
```

Escribe:

```python
import subprocess


equipos = [
    "127.0.0.1",
    "192.168.1.1",
    "8.8.8.8"
]


for equipo in equipos:

    resultado = subprocess.run(
        ["ping", "-n", "2", equipo],
        capture_output=True,
        text=True
    )

    if resultado.returncode == 0:
        print(f"{equipo}: RESPONDE")
    else:
        print(f"{equipo}: NO RESPONDE")
```

Ejecuta:

```powershell
python comprobar_varios_equipos.py
```

Obtendrás un resultado parecido a:

```text
127.0.0.1: RESPONDE
192.168.1.1: RESPONDE
8.8.8.8: RESPONDE
```

Los resultados dependerán de tu red.

Acabamos de automatizar nuestra primera tarea.

---

### Analizar el programa

Tenemos una lista:

```python
equipos = [
    "127.0.0.1",
    "192.168.1.1",
    "8.8.8.8"
]
```

El bucle:

```python
for equipo in equipos:
```

selecciona cada dirección sucesivamente.

En la primera iteración:

```text
equipo = 127.0.0.1
```

En la segunda:

```text
equipo = 192.168.1.1
```

En la tercera:

```text
equipo = 8.8.8.8
```

Y en cada iteración ejecutamos:

```python
subprocess.run(
    ["ping", "-n", "2", equipo]
)
```

Por tanto:

```text
LISTA
 │
 ├── 127.0.0.1
 │       ↓
 │      ping
 │
 ├── 192.168.1.1
 │       ↓
 │      ping
 │
 └── 8.8.8.8
         ↓
        ping
```

No importa demasiado si tenemos 3, 10 o 100 direcciones.

El código encargado de comprobar cada equipo es el mismo.

---

## 5. Crear una función reutilizable

Podemos mejorar el programa separando la operación de comprobación en una función.

Crea:

```text
comprobar_con_funcion.py
```

Escribe:

```python
import subprocess


def comprobar_equipo(equipo):

    resultado = subprocess.run(
        ["ping", "-n", "2", equipo],
        capture_output=True,
        text=True
    )

    if resultado.returncode == 0:
        return True

    return False


equipos = [
    "127.0.0.1",
    "192.168.1.1",
    "8.8.8.8"
]


for equipo in equipos:

    if comprobar_equipo(equipo):
        print(f"{equipo}: RESPONDE")
    else:
        print(f"{equipo}: NO RESPONDE")
```

Ahora tenemos claramente separadas dos responsabilidades.

La función:

```python
comprobar_equipo()
```

realiza la prueba.

El bucle:

```python
for equipo in equipos:
```

decide sobre qué equipos debemos realizarla.

Podemos representarlo así:

```text
        equipos
           │
           ▼
        bucle for
           │
           ▼
 comprobar_equipo()
           │
      ┌────┴────┐
      ▼         ▼
     True      False
      │         │
      ▼         ▼
  RESPONDE   NO RESPONDE
```

Esta separación hará que nuestros programas sean más fáciles de ampliar.

---

## 6. Contar los resultados

Un administrador probablemente no quiera únicamente ver una larga lista de resultados.

También puede interesarle obtener un resumen.

Vamos a contar:

```text
Equipos comprobados
Equipos que responden
Equipos que no responden
```

Crea:

```text
resumen_conectividad.py
```

Escribe:

```python
import subprocess


def comprobar_equipo(equipo):

    resultado = subprocess.run(
        ["ping", "-n", "2", equipo],
        capture_output=True,
        text=True
    )

    return resultado.returncode == 0


equipos = [
    "127.0.0.1",
    "192.168.1.1",
    "8.8.8.8"
]


responden = 0
no_responden = 0


for equipo in equipos:

    if comprobar_equipo(equipo):

        print(f"{equipo}: RESPONDE")
        responden += 1

    else:

        print(f"{equipo}: NO RESPONDE")
        no_responden += 1


print()
print("RESUMEN")
print("=======")

print(f"Equipos comprobados: {len(equipos)}")
print(f"Responden: {responden}")
print(f"No responden: {no_responden}")
```

El resultado podría ser:

```text
127.0.0.1: RESPONDE
192.168.1.1: RESPONDE
8.8.8.8: RESPONDE

RESUMEN
=======
Equipos comprobados: 3
Responden: 3
No responden: 0
```

Ahora nuestro script no solo ejecuta tareas repetitivas.

También **resume automáticamente los resultados**.

---

### Simplificar una función booleana

Observa esta versión:

```python
def comprobar_equipo(equipo):

    resultado = subprocess.run(
        ["ping", "-n", "2", equipo],
        capture_output=True,
        text=True
    )

    return resultado.returncode == 0
```

La expresión:

```python
resultado.returncode == 0
```

ya produce:

```text
True
```

o:

```text
False
```

Por tanto, no necesitamos escribir:

```python
if resultado.returncode == 0:
    return True
else:
    return False
```

Podemos devolver directamente el resultado de la comparación.

---

## 7. Añadir control de errores

Nuestro programa todavía tiene un problema.

¿Qué ocurre si:

```text
ping
```

no puede ejecutarse o tarda demasiado?

Podemos recuperar las técnicas estudiadas en el capítulo 2.

Modifica la función:

```python
def comprobar_equipo(equipo):

    try:

        resultado = subprocess.run(
            ["ping", "-n", "2", equipo],
            capture_output=True,
            text=True,
            timeout=10
        )

        return resultado.returncode == 0

    except FileNotFoundError:

        print("ERROR: no se encuentra el comando ping.")
        return False

    except subprocess.TimeoutExpired:

        print(f"ERROR: tiempo agotado para {equipo}.")
        return False
```

Nuestro proceso es ahora más robusto:

```text
EQUIPO
  │
  ▼
PING
  │
  ├── responde ─────────→ True
  │
  ├── no responde ──────→ False
  │
  ├── timeout ──────────→ False
  │
  └── comando no existe → False
```

!!! tip "Automatización robusta"

    Cuando automatizamos una tarea muchas veces, controlar los errores es especialmente importante.

    Un fallo en un único elemento no debería provocar necesariamente que se detenga todo el proceso.

---

## 8. Práctica propuesta: comprobar un aula

Supongamos que tenemos un aula con equipos cuyas direcciones son:

```text
192.168.1.101
192.168.1.102
192.168.1.103
192.168.1.104
192.168.1.105
```

Crea:

```text
comprobar_aula.py
```

El programa debe:

1. Guardar las direcciones en una lista.
2. Recorrerlas mediante `for`.
3. Ejecutar `ping`.
4. Mostrar `RESPONDE` o `NO RESPONDE`.
5. Contar los resultados.
6. Mostrar un resumen final.

El resultado deberá tener una estructura similar a:

```text
COMPROBACIÓN DEL AULA
=====================

192.168.1.101    RESPONDE
192.168.1.102    RESPONDE
192.168.1.103    NO RESPONDE
192.168.1.104    RESPONDE
192.168.1.105    NO RESPONDE

RESUMEN
=======

Equipos comprobados: 5
Responden: 3
No responden: 2
```

Los resultados reales dependerán de la red utilizada.

!!! example "Ampliación"

    Añade control de errores y un:

    ```python
    timeout=10
    ```

    para evitar que una comprobación pueda mantener el programa bloqueado demasiado tiempo.

---

## 9. El siguiente problema: ¿dónde almacenamos los equipos?

Nuestro programa funciona, pero tenemos las direcciones escritas directamente dentro del código:

```python
equipos = [
    "192.168.1.101",
    "192.168.1.102",
    "192.168.1.103",
    "192.168.1.104",
    "192.168.1.105"
]
```

Esto presenta un problema.

Si queremos cambiar los equipos tendremos que modificar el programa.

En administración es preferible separar:

```text
PROGRAMA
```

de:

```text
DATOS
```

Podemos almacenar las direcciones en un archivo:

```text
equipos.txt
```

o utilizar un inventario:

```text
inventario.csv
```

De esta forma:

```text
      equipos.txt
           │
           ▼
         Python
           │
           ▼
      bucle automático
           │
           ▼
          ping
           │
           ▼
       resultados
```

Esto nos permitirá modificar el listado de equipos **sin tocar el código Python**.

Será el siguiente paso del capítulo.

---

## Resumen

En esta primera parte del capítulo hemos comenzado a automatizar tareas repetitivas.

Hemos combinado:

```text
listas
  +
bucles
  +
funciones
  +
subprocess
  +
control de errores
```

para realizar automáticamente una misma operación sobre varios equipos.

El patrón fundamental es:

```text
        DATOS
          │
          ▼
        BUCLE
          │
          ▼
        FUNCIÓN
          │
          ▼
        ACCIÓN
          │
          ▼
       RESULTADO
```

Este patrón aparece continuamente en los scripts de administración.

En la siguiente parte eliminaremos las listas escritas directamente dentro del programa y aprenderemos a **cargar automáticamente los equipos desde archivos TXT y CSV**, combinando los conocimientos de los capítulos 1 y 2.

---

## 10. Separar los datos del programa

En los ejemplos anteriores utilizábamos una lista escrita directamente en el programa:

```python
equipos = [
    "192.168.1.101",
    "192.168.1.102",
    "192.168.1.103",
    "192.168.1.104",
    "192.168.1.105"
]
```

El programa funciona, pero presenta un inconveniente importante.

Si queremos añadir o eliminar un equipo debemos modificar el código Python.

En administración de sistemas resulta mucho más práctico separar:

```text
DATOS
```

de:

```text
PROGRAMA
```

Por ejemplo:

```text
equipos.txt
     │
     ▼
   Python
     │
     ▼
procesamiento
```

De esta forma podemos modificar los equipos sin cambiar el programa.

---

### Crear el archivo de equipos

Dentro de:

```text
practicas/capitulo3/datos/
```

crea:

```text
equipos.txt
```

Introduce:

```text
127.0.0.1
192.168.1.1
8.8.8.8
```

Cada línea contiene una dirección que queremos comprobar.

Nuestra estructura será:

```text
capitulo3/
├── datos/
│   └── equipos.txt
│
├── programas/
│
└── resultados/
```

---

## 11. Leer automáticamente la lista de equipos

Vamos a crear un programa que lea el archivo.

Dentro de:

```text
practicas/capitulo3/programas/
```

crea:

```text
leer_equipos.py
```

Escribe:

```python
from pathlib import Path


DIRECTORIO_PROGRAMA = Path(__file__).resolve().parent
DIRECTORIO_CAPITULO = DIRECTORIO_PROGRAMA.parent

ARCHIVO_EQUIPOS = (
    DIRECTORIO_CAPITULO
    / "datos"
    / "equipos.txt"
)


with open(
    ARCHIVO_EQUIPOS,
    "r",
    encoding="utf-8"
) as archivo:

    for linea in archivo:

        equipo = linea.strip()

        if equipo:
            print(equipo)
```

Ejecuta:

```powershell
python leer_equipos.py
```

Obtendremos:

```text
127.0.0.1
192.168.1.1
8.8.8.8
```

Observa que utilizamos:

```python
linea.strip()
```

para eliminar saltos de línea y posibles espacios.

También comprobamos:

```python
if equipo:
```

para ignorar líneas vacías.

---

### Ventaja de utilizar un archivo externo

Ahora podemos modificar:

```text
equipos.txt
```

sin modificar:

```text
leer_equipos.py
```

Por ejemplo:

```text
127.0.0.1
192.168.1.1
192.168.1.20
192.168.1.21
192.168.1.22
8.8.8.8
```

El programa procesará automáticamente el nuevo contenido.

Estamos separando claramente:

```text
CONFIGURACIÓN / DATOS
        │
        ▼
    equipos.txt

        +

      PROGRAMA
        │
        ▼
   script Python
```

Este principio será muy importante en programas más grandes.

---

## 12. Cargar los equipos en una lista

También podemos leer el archivo y almacenar sus datos en una lista.

Crea:

```text
cargar_equipos.py
```

Escribe:

```python
from pathlib import Path


DIRECTORIO_PROGRAMA = Path(__file__).resolve().parent
DIRECTORIO_CAPITULO = DIRECTORIO_PROGRAMA.parent

ARCHIVO_EQUIPOS = (
    DIRECTORIO_CAPITULO
    / "datos"
    / "equipos.txt"
)


equipos = []


with open(
    ARCHIVO_EQUIPOS,
    "r",
    encoding="utf-8"
) as archivo:

    for linea in archivo:

        equipo = linea.strip()

        if equipo:
            equipos.append(equipo)


print(equipos)
```

La salida será similar a:

```text
['127.0.0.1', '192.168.1.1', '8.8.8.8']
```

Ahora tenemos los datos del archivo almacenados en:

```python
equipos
```

y podemos recorrerlos:

```python
for equipo in equipos:
    print(equipo)
```

El proceso es:

```text
equipos.txt
     │
     ▼
 lectura
     │
     ▼
   lista
     │
     ▼
 bucle for
```

---

## 13. Automatizar `ping` desde un archivo

Ahora vamos a unir:

```text
archivo
+
bucle
+
subprocess
```

Crea:

```text
ping_desde_archivo.py
```

Escribe:

```python
import subprocess
from pathlib import Path


DIRECTORIO_PROGRAMA = Path(__file__).resolve().parent
DIRECTORIO_CAPITULO = DIRECTORIO_PROGRAMA.parent

ARCHIVO_EQUIPOS = (
    DIRECTORIO_CAPITULO
    / "datos"
    / "equipos.txt"
)


with open(
    ARCHIVO_EQUIPOS,
    "r",
    encoding="utf-8"
) as archivo:

    for linea in archivo:

        equipo = linea.strip()

        if not equipo:
            continue

        resultado = subprocess.run(
            [
                "ping",
                "-n",
                "2",
                equipo
            ],
            capture_output=True,
            text=True
        )

        if resultado.returncode == 0:
            print(f"{equipo}: RESPONDE")
        else:
            print(f"{equipo}: NO RESPONDE")
```

Ejecuta:

```powershell
python ping_desde_archivo.py
```

Obtendremos un resultado parecido a:

```text
127.0.0.1: RESPONDE
192.168.1.1: RESPONDE
8.8.8.8: RESPONDE
```

Los resultados dependerán de la red.

---

### Utilizar `continue`

En el programa aparece:

```python
if not equipo:
    continue
```

Si encontramos una línea vacía:

```python
equipo = ""
```

la instrucción:

```python
continue
```

hace que Python pase directamente a la siguiente iteración del bucle.

Por tanto:

```text
línea
  │
  ▼
¿está vacía?
  │
 ┌┴───────────┐
 │            │
Sí            No
 │            │
 ▼            ▼
continue     ping
 │
 ▼
siguiente línea
```

Esto evita intentar ejecutar:

```powershell
ping
```

sin una dirección.

---

## 14. Crear una función para cargar equipos

Podemos mejorar nuestro programa creando una función específica.

```python
def cargar_equipos(archivo_equipos):

    equipos = []

    with open(
        archivo_equipos,
        "r",
        encoding="utf-8"
    ) as archivo:

        for linea in archivo:

            equipo = linea.strip()

            if equipo:
                equipos.append(equipo)

    return equipos
```

Ahora podemos utilizar:

```python
equipos = cargar_equipos(
    ARCHIVO_EQUIPOS
)
```

Esto separa las diferentes responsabilidades del programa:

```text
cargar_equipos()
       ↓
obtiene los datos

comprobar_equipo()
       ↓
realiza el ping

programa principal
       ↓
coordina las operaciones
```

Esta organización facilita mucho la lectura del código.

---

## 15. Combinar funciones y archivos

Crea:

```text
comprobar_inventario_txt.py
```

Escribe:

```python
import subprocess
from pathlib import Path


DIRECTORIO_PROGRAMA = Path(__file__).resolve().parent
DIRECTORIO_CAPITULO = DIRECTORIO_PROGRAMA.parent

ARCHIVO_EQUIPOS = (
    DIRECTORIO_CAPITULO
    / "datos"
    / "equipos.txt"
)


def cargar_equipos(archivo_equipos):

    equipos = []

    with open(
        archivo_equipos,
        "r",
        encoding="utf-8"
    ) as archivo:

        for linea in archivo:

            equipo = linea.strip()

            if equipo:
                equipos.append(equipo)

    return equipos


def comprobar_equipo(equipo):

    try:

        resultado = subprocess.run(
            [
                "ping",
                "-n",
                "2",
                equipo
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        return resultado.returncode == 0

    except FileNotFoundError:

        print(
            "ERROR: no se encuentra "
            "el comando ping."
        )

        return False

    except subprocess.TimeoutExpired:

        print(
            f"ERROR: tiempo agotado "
            f"para {equipo}."
        )

        return False


equipos = cargar_equipos(
    ARCHIVO_EQUIPOS
)


for equipo in equipos:

    if comprobar_equipo(equipo):
        print(f"{equipo}: RESPONDE")
    else:
        print(f"{equipo}: NO RESPONDE")
```

Nuestro programa tiene ahora dos funciones claramente diferenciadas:

```text
cargar_equipos()
       │
       ▼
     lista
       │
       ▼
comprobar_equipo()
       │
       ▼
    resultado
```

---

## 16. Utilizar un inventario CSV

Un archivo TXT es suficiente si únicamente necesitamos almacenar una dirección por equipo.

Pero normalmente tendremos más información.

Por ejemplo:

```text
Nombre
Dirección IP
Sistema operativo
Ubicación
```

Para ello podemos recuperar los archivos CSV estudiados en el capítulo 1.

Dentro de:

```text
practicas/capitulo3/datos/
```

crea:

```text
inventario.csv
```

Introduce:

```csv
nombre,ip,sistema,ubicacion
PC-AULA-01,192.168.1.101,Windows 11,Aula 1
PC-AULA-02,192.168.1.102,Windows 11,Aula 1
PC-AULA-03,192.168.1.103,Windows 11,Aula 1
SERVIDOR-01,192.168.1.10,Ubuntu Server,CPD
ROUTER-01,192.168.1.1,Cisco IOS,Armario comunicaciones
```

Nuestra carpeta `datos` contiene ahora:

```text
datos/
├── equipos.txt
└── inventario.csv
```

---

## 17. Leer el inventario CSV

Crea:

```text
leer_inventario_csv.py
```

Escribe:

```python
import csv
from pathlib import Path


DIRECTORIO_PROGRAMA = Path(__file__).resolve().parent
DIRECTORIO_CAPITULO = DIRECTORIO_PROGRAMA.parent

ARCHIVO_INVENTARIO = (
    DIRECTORIO_CAPITULO
    / "datos"
    / "inventario.csv"
)


with open(
    ARCHIVO_INVENTARIO,
    "r",
    encoding="utf-8"
) as archivo:

    lector = csv.DictReader(archivo)

    for equipo in lector:

        print(
            f"{equipo['nombre']} - "
            f"{equipo['ip']} - "
            f"{equipo['sistema']} - "
            f"{equipo['ubicacion']}"
        )
```

Resultado:

```text
PC-AULA-01 - 192.168.1.101 - Windows 11 - Aula 1
PC-AULA-02 - 192.168.1.102 - Windows 11 - Aula 1
PC-AULA-03 - 192.168.1.103 - Windows 11 - Aula 1
SERVIDOR-01 - 192.168.1.10 - Ubuntu Server - CPD
ROUTER-01 - 192.168.1.1 - Cisco IOS - Armario comunicaciones
```

Ahora cada equipo contiene varios campos.

Por ejemplo:

```python
equipo["nombre"]
```

```python
equipo["ip"]
```

```python
equipo["sistema"]
```

```python
equipo["ubicacion"]
```

---

## 18. Comprobar automáticamente un inventario CSV

Ahora vamos a utilizar la dirección IP de cada registro para realizar la comprobación.

Crea:

```text
comprobar_inventario_csv.py
```

Escribe:

```python
import csv
import subprocess
from pathlib import Path


DIRECTORIO_PROGRAMA = Path(__file__).resolve().parent
DIRECTORIO_CAPITULO = DIRECTORIO_PROGRAMA.parent

ARCHIVO_INVENTARIO = (
    DIRECTORIO_CAPITULO
    / "datos"
    / "inventario.csv"
)


def comprobar_equipo(ip):

    try:

        resultado = subprocess.run(
            [
                "ping",
                "-n",
                "2",
                ip
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        return resultado.returncode == 0

    except FileNotFoundError:

        return False

    except subprocess.TimeoutExpired:

        return False


with open(
    ARCHIVO_INVENTARIO,
    "r",
    encoding="utf-8"
) as archivo:

    lector = csv.DictReader(archivo)

    for equipo in lector:

        nombre = equipo["nombre"]
        ip = equipo["ip"]

        if comprobar_equipo(ip):
            estado = "RESPONDE"
        else:
            estado = "NO RESPONDE"

        print(
            f"{nombre} - "
            f"{ip} - "
            f"{estado}"
        )
```

El resultado podría ser:

```text
PC-AULA-01 - 192.168.1.101 - RESPONDE
PC-AULA-02 - 192.168.1.102 - NO RESPONDE
PC-AULA-03 - 192.168.1.103 - RESPONDE
SERVIDOR-01 - 192.168.1.10 - RESPONDE
ROUTER-01 - 192.168.1.1 - RESPONDE
```

Los resultados dependerán de los equipos realmente disponibles en nuestra red.

---

## 19. Contar los equipos disponibles

Podemos añadir contadores.

Antes del bucle:

```python
total = 0
activos = 0
inactivos = 0
```

Dentro del bucle:

```python
total += 1
```

Cuando responde:

```python
activos += 1
```

Cuando no responde:

```python
inactivos += 1
```

Al terminar podemos mostrar:

```python
print()
print("RESUMEN")
print("=======")
print(f"Equipos comprobados: {total}")
print(f"Responden: {activos}")
print(f"No responden: {inactivos}")
```

Nuestro script puede producir:

```text
PC-AULA-01 - 192.168.1.101 - RESPONDE
PC-AULA-02 - 192.168.1.102 - NO RESPONDE
PC-AULA-03 - 192.168.1.103 - RESPONDE
SERVIDOR-01 - 192.168.1.10 - RESPONDE
ROUTER-01 - 192.168.1.1 - RESPONDE

RESUMEN
=======
Equipos comprobados: 5
Responden: 4
No responden: 1
```

---

## 20. Guardar los resultados

Hasta ahora los resultados desaparecen cuando cerramos la terminal.

Vamos a guardarlos automáticamente.

Queremos crear:

```text
resultados/estado_equipos.txt
```

Crea:

```text
generar_estado_red.py
```

Escribe:

```python
import csv
import subprocess
from pathlib import Path


DIRECTORIO_PROGRAMA = Path(__file__).resolve().parent
DIRECTORIO_CAPITULO = DIRECTORIO_PROGRAMA.parent

ARCHIVO_INVENTARIO = (
    DIRECTORIO_CAPITULO
    / "datos"
    / "inventario.csv"
)

DIRECTORIO_RESULTADOS = (
    DIRECTORIO_CAPITULO
    / "resultados"
)

ARCHIVO_RESULTADOS = (
    DIRECTORIO_RESULTADOS
    / "estado_equipos.txt"
)


DIRECTORIO_RESULTADOS.mkdir(
    parents=True,
    exist_ok=True
)


def comprobar_equipo(ip):

    try:

        resultado = subprocess.run(
            [
                "ping",
                "-n",
                "2",
                ip
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        return resultado.returncode == 0

    except FileNotFoundError:

        return False

    except subprocess.TimeoutExpired:

        return False


total = 0
activos = 0
inactivos = 0

lineas_resultado = []


with open(
    ARCHIVO_INVENTARIO,
    "r",
    encoding="utf-8"
) as archivo:

    lector = csv.DictReader(archivo)

    for equipo in lector:

        nombre = equipo["nombre"]
        ip = equipo["ip"]

        total += 1

        if comprobar_equipo(ip):

            estado = "RESPONDE"
            activos += 1

        else:

            estado = "NO RESPONDE"
            inactivos += 1

        linea = (
            f"{nombre} - "
            f"{ip} - "
            f"{estado}"
        )

        print(linea)

        lineas_resultado.append(linea)


informe = ""

informe += "ESTADO DE LOS EQUIPOS\n"
informe += "======================\n\n"

for linea in lineas_resultado:
    informe += linea + "\n"

informe += "\n"
informe += "RESUMEN\n"
informe += "=======\n"

informe += (
    f"Equipos comprobados: {total}\n"
)

informe += (
    f"Responden: {activos}\n"
)

informe += (
    f"No responden: {inactivos}\n"
)


ARCHIVO_RESULTADOS.write_text(
    informe,
    encoding="utf-8"
)


print()
print("Informe generado:")
print(ARCHIVO_RESULTADOS)
```

Ejecuta:

```powershell
python generar_estado_red.py
```

Después comprueba:

```text
practicas/capitulo3/resultados/
```

Debe aparecer:

```text
estado_equipos.txt
```

---

## 21. Flujo completo de automatización

Ahora ya tenemos un proceso completo:

```text
inventario.csv
      │
      ▼
csv.DictReader()
      │
      ▼
lista de equipos
      │
      ▼
   bucle for
      │
      ▼
subprocess.run()
      │
      ▼
     ping
      │
      ▼
  returncode
      │
 ┌────┴─────┐
 ▼          ▼
RESPONDE   NO RESPONDE
 │          │
 └────┬─────┘
      ▼
   resumen
      │
      ▼
estado_equipos.txt
```

Estamos combinando ya los tres capítulos:

```text
CAPÍTULO 1
Archivos + CSV + pathlib
          │
          ▼
CAPÍTULO 2
subprocess + comandos
          │
          ▼
CAPÍTULO 3
automatización
          │
          ▼
HERRAMIENTA DE ADMINISTRACIÓN
```

---

## 22. Práctica propuesta: inventario del aula

Crea un archivo:

```text
datos/aula.csv
```

con al menos cinco equipos.

Debe tener:

```csv
nombre,ip,sistema,ubicacion
```

Por ejemplo:

```csv
nombre,ip,sistema,ubicacion
PC01,192.168.1.101,Windows 11,Aula 1
PC02,192.168.1.102,Windows 11,Aula 1
PC03,192.168.1.103,Windows 11,Aula 1
PC04,192.168.1.104,Ubuntu,Aula 1
PC05,192.168.1.105,Ubuntu,Aula 1
```

Crea:

```text
comprobar_aula_csv.py
```

El programa deberá:

1. Leer automáticamente `aula.csv`.
2. Obtener el nombre y la IP de cada equipo.
3. Realizar un `ping`.
4. Mostrar el resultado.
5. Contar equipos disponibles y no disponibles.
6. Generar:

```text
resultados/informe_aula.txt
```

El informe deberá tener una estructura similar a:

```text
INFORME DEL AULA
================

PC01 - 192.168.1.101 - RESPONDE
PC02 - 192.168.1.102 - RESPONDE
PC03 - 192.168.1.103 - NO RESPONDE
PC04 - 192.168.1.104 - RESPONDE
PC05 - 192.168.1.105 - NO RESPONDE

RESUMEN
=======

Equipos comprobados: 5
Responden: 3
No responden: 2
```

!!! tip "Pistas"

    Necesitarás combinar:

    - `csv.DictReader()`
    - `Path`
    - `subprocess.run()`
    - `returncode`
    - `for`
    - `if`
    - funciones
    - contadores
    - `write_text()`

---

## 23. Reto de ampliación

Modifica la práctica anterior para mostrar también:

```text
nombre
IP
sistema operativo
ubicación
estado
```

Por ejemplo:

```text
PC01
  IP: 192.168.1.101
  Sistema: Windows 11
  Ubicación: Aula 1
  Estado: RESPONDE

PC02
  IP: 192.168.1.102
  Sistema: Windows 11
  Ubicación: Aula 1
  Estado: NO RESPONDE
```

!!! example "Objetivo"

    El archivo CSV debe actuar como **inventario de entrada**.

    El programa Python debe realizar automáticamente las comprobaciones.

    El archivo generado debe actuar como **informe de salida**.

    Por tanto:

    ```text
    INVENTARIO
        ↓
    AUTOMATIZACIÓN
        ↓
    INFORME
    ```

---

## Resumen

En esta parte hemos mejorado considerablemente nuestros scripts de automatización.

Ya podemos separar:

```text
DATOS
  │
  ▼
TXT / CSV

PROGRAMA
  │
  ▼
Python

RESULTADOS
  │
  ▼
TXT
```

Hemos aprendido a:

- Leer listas de equipos desde archivos TXT.
- Cargar datos en listas.
- Ignorar líneas vacías.
- Utilizar `continue`.
- Leer inventarios mediante `csv.DictReader()`.
- Ejecutar automáticamente una acción sobre cada registro.
- Combinar CSV y `subprocess`.
- Contar resultados.
- Generar informes.
- Separar los datos del código.

El patrón fundamental es ahora:

```text
ARCHIVO DE ENTRADA
       ↓
      PYTHON
       ↓
     BUCLE
       ↓
    COMANDO
       ↓
   RESULTADO
       ↓
ARCHIVO DE SALIDA
```

En la siguiente parte mejoraremos esta automatización haciendo que nuestros scripts puedan **generar automáticamente rangos de direcciones y procesar grupos de equipos sin tener que escribir manualmente cada IP**, además de seguir organizando el código en funciones reutilizables.

---

## 24. Generar automáticamente grupos de equipos

Hasta ahora hemos utilizado archivos como:

```text
equipos.txt
```

o:

```text
inventario.csv
```

para indicar qué equipos debe procesar nuestro programa.

Esta solución es adecuada cuando cada equipo tiene información propia:

```text
nombre
IP
sistema operativo
ubicación
```

Sin embargo, algunas tareas requieren simplemente procesar un conjunto de direcciones consecutivas.

Por ejemplo:

```text
192.168.1.101
192.168.1.102
192.168.1.103
192.168.1.104
192.168.1.105
```

Escribir manualmente todas estas direcciones no resulta práctico si tenemos que comprobar decenas de equipos.

Python puede generarlas automáticamente.

---

## 25. Utilizar `range()`

La función:

```python
range()
```

permite generar secuencias de números.

Por ejemplo:

```python
for numero in range(1, 6):
    print(numero)
```

Resultado:

```text
1
2
3
4
5
```

Observa un detalle importante.

Hemos utilizado:

```python
range(1, 6)
```

pero el último número obtenido es:

```text
5
```

El segundo valor indica el límite, pero **no está incluido**.

Por tanto:

```python
range(1, 6)
```

genera:

```text
1
2
3
4
5
```

!!! note "El último valor no se incluye"

    Si queremos generar números desde `1` hasta `10`, utilizaremos:

    ```python
    range(1, 11)
    ```

---

### Generar direcciones IP

Podemos combinar `range()` con una cadena formateada.

Crea:

```text
generar_ips.py
```

dentro de:

```text
practicas/capitulo3/programas/
```

Escribe:

```python
for numero in range(101, 106):

    ip = f"192.168.1.{numero}"

    print(ip)
```

Ejecuta:

```powershell
python generar_ips.py
```

Obtendremos:

```text
192.168.1.101
192.168.1.102
192.168.1.103
192.168.1.104
192.168.1.105
```

Python ha construido automáticamente las cinco direcciones.

El proceso es:

```text
range(101, 106)
        │
        ▼
101 102 103 104 105
        │
        ▼
f"192.168.1.{numero}"
        │
        ▼
direcciones IP
```

---

## 26. Comprobar un rango de direcciones

Ahora podemos combinar:

```text
range()
+
subprocess
+
ping
```

Crea:

```text
comprobar_rango.py
```

Escribe:

```python
import subprocess


for numero in range(101, 106):

    ip = f"192.168.1.{numero}"

    resultado = subprocess.run(
        [
            "ping",
            "-n",
            "1",
            ip
        ],
        capture_output=True,
        text=True,
        timeout=5
    )

    if resultado.returncode == 0:
        print(f"{ip}: RESPONDE")
    else:
        print(f"{ip}: NO RESPONDE")
```

Ejecuta:

```powershell
python comprobar_rango.py
```

El resultado podría ser:

```text
192.168.1.101: RESPONDE
192.168.1.102: NO RESPONDE
192.168.1.103: RESPONDE
192.168.1.104: RESPONDE
192.168.1.105: NO RESPONDE
```

Los resultados dependerán de nuestra red.

!!! warning "Comprobaciones en una red"

    Realiza estas prácticas únicamente sobre equipos y redes en los que tengas autorización para efectuar las comprobaciones.

---

## 27. Elegir el rango desde el programa

Podemos almacenar los valores en variables:

```python
red = "192.168.1"
inicio = 101
fin = 105
```

Después:

```python
for numero in range(inicio, fin + 1):

    ip = f"{red}.{numero}"

    print(ip)
```

Observa:

```python
fin + 1
```

Como el último valor de `range()` no se incluye, añadimos `1` para que la dirección final también sea procesada.

Con:

```python
inicio = 101
fin = 105
```

obtenemos:

```text
192.168.1.101
192.168.1.102
192.168.1.103
192.168.1.104
192.168.1.105
```

---

### Solicitar los valores al usuario

Podemos permitir que el usuario indique el rango.

Crea:

```text
rango_personalizado.py
```

Escribe:

```python
red = input(
    "Introduce los tres primeros octetos "
    "de la red: "
)

inicio = int(
    input("Primer equipo: ")
)

fin = int(
    input("Último equipo: ")
)


for numero in range(inicio, fin + 1):

    ip = f"{red}.{numero}"

    print(ip)
```

Una ejecución podría ser:

```text
Introduce los tres primeros octetos de la red: 192.168.1
Primer equipo: 20
Último equipo: 25
```

Resultado:

```text
192.168.1.20
192.168.1.21
192.168.1.22
192.168.1.23
192.168.1.24
192.168.1.25
```

Ahora el programa puede trabajar con diferentes rangos sin modificar el código.

---

## 28. Crear una función para generar direcciones

Podemos separar nuevamente las responsabilidades.

Crea:

```text
funcion_generar_ips.py
```

Escribe:

```python
def generar_ips(red, inicio, fin):

    direcciones = []

    for numero in range(
        inicio,
        fin + 1
    ):

        ip = f"{red}.{numero}"

        direcciones.append(ip)

    return direcciones


equipos = generar_ips(
    "192.168.1",
    101,
    105
)


for equipo in equipos:
    print(equipo)
```

La función:

```python
generar_ips()
```

recibe:

```text
red
inicio
fin
```

y devuelve una lista.

Por ejemplo:

```python
equipos = generar_ips(
    "192.168.1",
    101,
    105
)
```

produce conceptualmente:

```python
[
    "192.168.1.101",
    "192.168.1.102",
    "192.168.1.103",
    "192.168.1.104",
    "192.168.1.105"
]
```

---

## 29. Separar generación y comprobación

Ahora podemos crear dos funciones independientes:

```text
generar_ips()
```

y:

```text
comprobar_equipo()
```

Crea:

```text
comprobar_red.py
```

Escribe:

```python
import subprocess


def generar_ips(red, inicio, fin):

    direcciones = []

    for numero in range(
        inicio,
        fin + 1
    ):

        direcciones.append(
            f"{red}.{numero}"
        )

    return direcciones


def comprobar_equipo(ip):

    try:

        resultado = subprocess.run(
            [
                "ping",
                "-n",
                "1",
                ip
            ],
            capture_output=True,
            text=True,
            timeout=5
        )

        return resultado.returncode == 0

    except FileNotFoundError:

        print(
            "ERROR: no se encuentra "
            "el comando ping."
        )

        return False

    except subprocess.TimeoutExpired:

        return False


equipos = generar_ips(
    "192.168.1",
    101,
    105
)


for equipo in equipos:

    if comprobar_equipo(equipo):
        print(f"{equipo}: RESPONDE")
    else:
        print(f"{equipo}: NO RESPONDE")
```

Fíjate en la organización:

```text
generar_ips()
      │
      ▼
lista de direcciones
      │
      ▼
     for
      │
      ▼
comprobar_equipo()
      │
      ▼
RESPONDE / NO RESPONDE
```

Cada función tiene una responsabilidad concreta.

---

## 30. Guardar únicamente los equipos que responden

En algunas situaciones nos interesará obtener una lista de los equipos que han respondido.

Podemos crear:

```python
equipos_activos = []
```

y añadir las direcciones disponibles:

```python
if comprobar_equipo(equipo):

    equipos_activos.append(equipo)
```

Por ejemplo:

```python
equipos_activos = []


for equipo in equipos:

    if comprobar_equipo(equipo):

        print(f"{equipo}: RESPONDE")

        equipos_activos.append(
            equipo
        )

    else:

        print(
            f"{equipo}: NO RESPONDE"
        )
```

Al finalizar, la lista podría contener:

```python
[
    "192.168.1.101",
    "192.168.1.103",
    "192.168.1.104"
]
```

Ahora podemos utilizar esa lista para realizar otras operaciones.

Por ejemplo:

```text
COMPROBAR RED
      ↓
EQUIPOS ACTIVOS
      ↓
OTRAS TAREAS
```

Este patrón es muy habitual en automatización:

> Primero seleccionamos los elementos que cumplen una condición y después trabajamos únicamente con ellos.

---

## 31. Guardar los equipos activos en un archivo

Vamos a utilizar nuevamente `pathlib`.

Crea:

```text
guardar_equipos_activos.py
```

Escribe:

```python
import subprocess
from pathlib import Path


DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)

DIRECTORIO_CAPITULO = (
    DIRECTORIO_PROGRAMA.parent
)

DIRECTORIO_RESULTADOS = (
    DIRECTORIO_CAPITULO
    / "resultados"
)

DIRECTORIO_RESULTADOS.mkdir(
    parents=True,
    exist_ok=True
)

ARCHIVO_ACTIVOS = (
    DIRECTORIO_RESULTADOS
    / "equipos_activos.txt"
)


def generar_ips(red, inicio, fin):

    direcciones = []

    for numero in range(
        inicio,
        fin + 1
    ):

        direcciones.append(
            f"{red}.{numero}"
        )

    return direcciones


def comprobar_equipo(ip):

    try:

        resultado = subprocess.run(
            [
                "ping",
                "-n",
                "1",
                ip
            ],
            capture_output=True,
            text=True,
            timeout=5
        )

        return resultado.returncode == 0

    except (
        FileNotFoundError,
        subprocess.TimeoutExpired
    ):

        return False


equipos = generar_ips(
    "192.168.1",
    101,
    105
)

equipos_activos = []


for equipo in equipos:

    if comprobar_equipo(equipo):

        print(
            f"{equipo}: RESPONDE"
        )

        equipos_activos.append(
            equipo
        )

    else:

        print(
            f"{equipo}: NO RESPONDE"
        )


contenido = "\n".join(
    equipos_activos
)


ARCHIVO_ACTIVOS.write_text(
    contenido,
    encoding="utf-8"
)


print()
print(
    f"Equipos activos encontrados: "
    f"{len(equipos_activos)}"
)

print(
    f"Resultado guardado en: "
    f"{ARCHIVO_ACTIVOS}"
)
```

Después de ejecutar el programa tendremos:

```text
resultados/
└── equipos_activos.txt
```

Su contenido podría ser:

```text
192.168.1.101
192.168.1.103
192.168.1.104
```

---

## 32. Utilizar parámetros de configuración

Nuestro programa todavía contiene estos valores:

```python
equipos = generar_ips(
    "192.168.1",
    101,
    105
)
```

Podemos agruparlos al principio:

```python
RED = "192.168.1"
INICIO = 101
FIN = 105
TIMEOUT = 5
```

Después:

```python
equipos = generar_ips(
    RED,
    INICIO,
    FIN
)
```

y:

```python
resultado = subprocess.run(
    [
        "ping",
        "-n",
        "1",
        ip
    ],
    capture_output=True,
    text=True,
    timeout=TIMEOUT
)
```

Ahora todos los valores que probablemente necesitemos modificar están localizados al principio del programa.

```text
CONFIGURACIÓN
      │
      ├── RED
      ├── INICIO
      ├── FIN
      └── TIMEOUT
            │
            ▼
         PROGRAMA
```

!!! tip "Configuración"

    Separar los valores de configuración del resto del código facilita la modificación y reutilización de nuestros scripts.

    Más adelante podremos incluso almacenar esta configuración fuera del propio programa.

---

## 33. Validar los datos introducidos

En este programa:

```python
inicio = int(
    input("Primer equipo: ")
)
```

suponemos que el usuario introduce un número.

Pero podría escribir:

```text
cien
```

En ese caso:

```python
int("cien")
```

produce:

```text
ValueError
```

Podemos controlarlo:

```python
try:

    inicio = int(
        input("Primer equipo: ")
    )

    fin = int(
        input("Último equipo: ")
    )

except ValueError:

    print(
        "ERROR: debes introducir "
        "valores numéricos."
    )
```

También podemos comprobar:

```python
if inicio < 1 or inicio > 254:
    print("El valor inicial no es válido.")
```

y:

```python
if fin < 1 or fin > 254:
    print("El valor final no es válido.")
```

Además:

```python
if inicio > fin:
    print(
        "El valor inicial no puede "
        "ser mayor que el final."
    )
```

La validación evita que nuestro programa continúe trabajando con datos incorrectos.

---

## 34. Práctica propuesta: comprobador de rango

Crea:

```text
comprobador_rango.py
```

El programa debe solicitar:

```text
Red: 192.168.1
Primera dirección: 100
Última dirección: 110
```

Después debe comprobar automáticamente:

```text
192.168.1.100
192.168.1.101
192.168.1.102
...
192.168.1.110
```

El resultado debe mostrar:

```text
COMPROBACIÓN DE RED
===================

192.168.1.100    NO RESPONDE
192.168.1.101    RESPONDE
192.168.1.102    RESPONDE
...
```

Al finalizar:

```text
RESUMEN
=======

Direcciones comprobadas: 11
Responden: 6
No responden: 5
```

Los valores dependerán de la red utilizada.

!!! example "Requisitos"

    El programa debe utilizar:

    - `range()`
    - funciones
    - `subprocess.run()`
    - `returncode`
    - `timeout`
    - control de excepciones
    - listas
    - contadores

    También debe comprobar que los valores inicial y final sean válidos.

---

## 35. Práctica de ampliación: generar un informe

Amplía:

```text
comprobador_rango.py
```

para generar:

```text
resultados/informe_rango.txt
```

El archivo deberá contener tanto los resultados como el resumen.

Por ejemplo:

```text
INFORME DE COMPROBACIÓN DE RED
==============================

Red: 192.168.1
Rango: 100 - 110

192.168.1.100    NO RESPONDE
192.168.1.101    RESPONDE
192.168.1.102    RESPONDE
192.168.1.103    NO RESPONDE

RESUMEN
=======

Direcciones comprobadas: 11
Responden: 6
No responden: 5
```

Utiliza:

```python
Path
```

para generar correctamente la ruta del archivo.

---

## 36. Inventario o generación automática

Ahora disponemos de dos formas diferentes de indicar qué equipos queremos procesar.

### Inventario

```text
inventario.csv
       ↓
     Python
       ↓
    equipos
```

Esta solución es adecuada cuando necesitamos información adicional:

```text
nombre
IP
sistema
ubicación
```

### Generación automática

```text
red + rango
     ↓
   range()
     ↓
direcciones
```

Esta solución es adecuada cuando únicamente necesitamos generar direcciones consecutivas.

No existe una única solución para todas las situaciones.

Debemos elegir la estructura que mejor se adapte al problema que queremos automatizar.

---

## 37. Un patrón reutilizable de automatización

Los programas que estamos creando empiezan a compartir una estructura común:

```text
1. OBTENER DATOS
       ↓
2. VALIDAR DATOS
       ↓
3. GENERAR / CARGAR ELEMENTOS
       ↓
4. RECORRER ELEMENTOS
       ↓
5. EJECUTAR UNA ACCIÓN
       ↓
6. COMPROBAR EL RESULTADO
       ↓
7. ALMACENAR RESULTADOS
       ↓
8. GENERAR UN INFORME
```

Este patrón no sirve únicamente para comprobar direcciones IP.

Podemos utilizarlo para:

```text
archivos
usuarios
equipos
servicios
directorios
procesos
copias de seguridad
logs
```

La acción concreta cambiará, pero la estructura general será muy similar.

---

## Resumen

En esta parte hemos aprendido a generar automáticamente grupos de elementos mediante:

```python
range()
```

y hemos aplicado esta técnica a direcciones IP.

También hemos aprendido a:

- Generar secuencias numéricas.
- Construir direcciones mediante f-strings.
- Definir un rango inicial y final.
- Solicitar parámetros al usuario.
- Crear funciones para generar listas.
- Separar generación y procesamiento.
- Guardar únicamente determinados resultados.
- Generar archivos con los equipos activos.
- Utilizar parámetros de configuración.
- Validar datos introducidos por el usuario.
- Controlar `ValueError`.

Nuestro flujo de automatización ha evolucionado hasta:

```text
     CONFIGURACIÓN
           │
           ▼
   GENERAR / CARGAR
           │
           ▼
        VALIDAR
           │
           ▼
         BUCLE
           │
           ▼
         ACCIÓN
           │
           ▼
       RESULTADOS
           │
           ▼
        INFORME
```

En la siguiente parte aplicaremos este patrón a **tareas sobre archivos y directorios**, automatizando operaciones como localizar archivos, procesar grupos de ficheros y realizar acciones sobre ellos sin tener que trabajar archivo por archivo.

---

## 38. Automatizar tareas con archivos

Hasta ahora hemos utilizado la automatización principalmente para trabajar con equipos de una red.

Sin embargo, un administrador también realiza continuamente tareas relacionadas con archivos:

```text
buscar archivos
copiar archivos
crear directorios
clasificar documentos
renombrar archivos
generar informes
```

Realizar estas operaciones manualmente puede resultar lento cuando tenemos decenas o cientos de archivos.

Python permite aplicar el mismo principio que hemos utilizado anteriormente:

```text
OBTENER ELEMENTOS
       ↓
RECORRERLOS
       ↓
COMPROBAR CONDICIONES
       ↓
REALIZAR ACCIONES
       ↓
GENERAR RESULTADOS
```

Vamos a aplicar este patrón al sistema de archivos.

---

## 39. Preparar un directorio de pruebas

Dentro de:

```text
practicas/capitulo3/
```

crea:

```text
archivos/
```

Dentro crea manualmente algunos archivos de prueba:

```text
informe.txt
usuarios.csv
servidor.log
notas.txt
equipos.csv
errores.log
```

La estructura será:

```text
capitulo3/
├── archivos/
│   ├── informe.txt
│   ├── usuarios.csv
│   ├── servidor.log
│   ├── notas.txt
│   ├── equipos.csv
│   └── errores.log
│
├── datos/
├── programas/
└── resultados/
```

No es necesario que los archivos contengan información importante.

Los utilizaremos para realizar nuestras pruebas.

---

## 40. Recorrer los archivos de un directorio

En el capítulo 1 aprendimos a utilizar:

```python
pathlib
```

Vamos a recuperarlo.

Dentro de:

```text
practicas/capitulo3/programas/
```

crea:

```text
listar_archivos.py
```

Escribe:

```python
from pathlib import Path


DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)

DIRECTORIO_CAPITULO = (
    DIRECTORIO_PROGRAMA.parent
)

DIRECTORIO_ARCHIVOS = (
    DIRECTORIO_CAPITULO
    / "archivos"
)


for elemento in DIRECTORIO_ARCHIVOS.iterdir():

    print(elemento.name)
```

Ejecuta:

```powershell
python listar_archivos.py
```

Obtendremos los elementos contenidos en la carpeta.

Por ejemplo:

```text
informe.txt
usuarios.csv
servidor.log
notas.txt
equipos.csv
errores.log
```

La instrucción:

```python
DIRECTORIO_ARCHIVOS.iterdir()
```

permite recorrer los elementos que contiene un directorio.

---

### Comprobar que son archivos

Un directorio puede contener:

```text
archivos
carpetas
```

Si queremos trabajar únicamente con archivos podemos utilizar:

```python
is_file()
```

Por ejemplo:

```python
for elemento in DIRECTORIO_ARCHIVOS.iterdir():

    if elemento.is_file():
        print(elemento.name)
```

De esta forma ignoraremos los subdirectorios.

---

## 41. Filtrar archivos por extensión

Supongamos que únicamente queremos localizar archivos:

```text
.txt
```

Podemos consultar la extensión mediante:

```python
elemento.suffix
```

Crea:

```text
buscar_txt.py
```

Escribe:

```python
from pathlib import Path


DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)

DIRECTORIO_ARCHIVOS = (
    DIRECTORIO_PROGRAMA.parent
    / "archivos"
)


for archivo in DIRECTORIO_ARCHIVOS.iterdir():

    if archivo.is_file():

        if archivo.suffix == ".txt":
            print(archivo.name)
```

Resultado:

```text
informe.txt
notas.txt
```

Podemos representar el proceso:

```text
DIRECTORIO
    │
    ▼
  iterdir()
    │
    ▼
¿es archivo?
    │
    ▼
¿termina en .txt?
    │
 ┌──┴──┐
 Sí    No
 │      │
 ▼      ▼
usar  ignorar
```

---

## 42. Utilizar `glob()`

`pathlib` proporciona una forma especialmente cómoda de buscar archivos mediante patrones.

Por ejemplo:

```python
DIRECTORIO_ARCHIVOS.glob("*.txt")
```

significa:

> Busca todos los elementos cuyo nombre termine en `.txt`.

Podemos simplificar el programa anterior:

```python
from pathlib import Path


DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)

DIRECTORIO_ARCHIVOS = (
    DIRECTORIO_PROGRAMA.parent
    / "archivos"
)


for archivo in DIRECTORIO_ARCHIVOS.glob("*.txt"):

    print(archivo.name)
```

Resultado:

```text
informe.txt
notas.txt
```

Otros ejemplos:

```python
DIRECTORIO_ARCHIVOS.glob("*.csv")
```

busca archivos CSV.

```python
DIRECTORIO_ARCHIVOS.glob("*.log")
```

busca archivos LOG.

```python
DIRECTORIO_ARCHIVOS.glob("informe*")
```

busca nombres que comiencen por:

```text
informe
```

!!! tip "Patrones"

    El carácter:

    ```text
    *
    ```

    representa cualquier conjunto de caracteres.

    Por ejemplo:

    ```text
    *.txt
    ```

    significa cualquier nombre que termine en `.txt`.

---

## 43. Contar archivos automáticamente

Podemos utilizar contadores para obtener información sobre un directorio.

Crea:

```text
contar_archivos.py
```

Escribe:

```python
from pathlib import Path


DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)

DIRECTORIO_ARCHIVOS = (
    DIRECTORIO_PROGRAMA.parent
    / "archivos"
)


total = 0
txt = 0
csv = 0
log = 0


for archivo in DIRECTORIO_ARCHIVOS.iterdir():

    if not archivo.is_file():
        continue

    total += 1

    if archivo.suffix == ".txt":
        txt += 1

    elif archivo.suffix == ".csv":
        csv += 1

    elif archivo.suffix == ".log":
        log += 1


print("RESUMEN DE ARCHIVOS")
print("===================")

print(f"Total: {total}")
print(f"TXT: {txt}")
print(f"CSV: {csv}")
print(f"LOG: {log}")
```

Con nuestros archivos de ejemplo obtendríamos:

```text
RESUMEN DE ARCHIVOS
===================

Total: 6
TXT: 2
CSV: 2
LOG: 2
```

Ya estamos automatizando una pequeña tarea de inventario.

---

## 44. Crear directorios automáticamente

Supongamos ahora que queremos organizar los archivos según su tipo.

Queremos crear:

```text
clasificados/
├── txt/
├── csv/
└── log/
```

Podemos hacerlo con:

```python
mkdir()
```

Crea:

```text
crear_clasificacion.py
```

Escribe:

```python
from pathlib import Path


DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)

DIRECTORIO_CAPITULO = (
    DIRECTORIO_PROGRAMA.parent
)

DIRECTORIO_CLASIFICADOS = (
    DIRECTORIO_CAPITULO
    / "clasificados"
)


tipos = [
    "txt",
    "csv",
    "log"
]


for tipo in tipos:

    directorio = (
        DIRECTORIO_CLASIFICADOS
        / tipo
    )

    directorio.mkdir(
        parents=True,
        exist_ok=True
    )

    print(
        f"Directorio preparado: {directorio}"
    )
```

Ejecuta:

```powershell
python crear_clasificacion.py
```

Se creará:

```text
clasificados/
├── txt/
├── csv/
└── log/
```

Observa nuevamente el patrón:

```text
LISTA
  │
  ▼
FOR
  │
  ▼
ACCIÓN
```

En este caso la acción repetitiva es:

```python
mkdir()
```

---

## 45. Copiar archivos automáticamente

Para copiar archivos podemos utilizar el módulo estándar:

```python
shutil
```

y concretamente:

```python
shutil.copy2()
```

Crea:

```text
copiar_txt.py
```

Escribe:

```python
import shutil
from pathlib import Path


DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)

DIRECTORIO_CAPITULO = (
    DIRECTORIO_PROGRAMA.parent
)

ORIGEN = (
    DIRECTORIO_CAPITULO
    / "archivos"
)

DESTINO = (
    DIRECTORIO_CAPITULO
    / "clasificados"
    / "txt"
)


DESTINO.mkdir(
    parents=True,
    exist_ok=True
)


for archivo in ORIGEN.glob("*.txt"):

    destino_archivo = (
        DESTINO
        / archivo.name
    )

    shutil.copy2(
        archivo,
        destino_archivo
    )

    print(
        f"Copiado: {archivo.name}"
    )
```

Ejecuta:

```powershell
python copiar_txt.py
```

Los archivos:

```text
informe.txt
notas.txt
```

se copiarán a:

```text
clasificados/txt/
```

!!! note "`copy2()`"

    `shutil.copy2()` copia el archivo e intenta conservar también metadatos como las fechas del archivo.

---

## 46. Clasificar varios tipos de archivo

Ahora podemos automatizar todo el proceso.

Queremos conseguir:

```text
archivos/
├── informe.txt
├── usuarios.csv
├── servidor.log
├── notas.txt
├── equipos.csv
└── errores.log

        ↓ Python

clasificados/
├── txt/
│   ├── informe.txt
│   └── notas.txt
│
├── csv/
│   ├── usuarios.csv
│   └── equipos.csv
│
└── log/
    ├── servidor.log
    └── errores.log
```

Crea:

```text
clasificar_archivos.py
```

Escribe:

```python
import shutil
from pathlib import Path


DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)

DIRECTORIO_CAPITULO = (
    DIRECTORIO_PROGRAMA.parent
)

ORIGEN = (
    DIRECTORIO_CAPITULO
    / "archivos"
)

DESTINO = (
    DIRECTORIO_CAPITULO
    / "clasificados"
)


for archivo in ORIGEN.iterdir():

    if not archivo.is_file():
        continue

    extension = (
        archivo.suffix
        .lower()
        .replace(".", "")
    )

    if extension not in [
        "txt",
        "csv",
        "log"
    ]:
        continue

    carpeta_destino = (
        DESTINO
        / extension
    )

    carpeta_destino.mkdir(
        parents=True,
        exist_ok=True
    )

    archivo_destino = (
        carpeta_destino
        / archivo.name
    )

    shutil.copy2(
        archivo,
        archivo_destino
    )

    print(
        f"{archivo.name} -> "
        f"{extension}/"
    )
```

Ejecuta:

```powershell
python clasificar_archivos.py
```

El programa determinará automáticamente la carpeta de destino según la extensión.

---

### Analizar la extensión

Observa:

```python
archivo.suffix
```

Para:

```text
informe.txt
```

devuelve:

```text
.txt
```

Después utilizamos:

```python
.lower()
```

para convertirla a minúsculas.

Esto permite tratar igual:

```text
.TXT
.txt
.Txt
```

Finalmente:

```python
.replace(".", "")
```

elimina el punto.

Por tanto:

```text
.TXT
 ↓
.txt
 ↓
txt
```

Este valor puede utilizarse directamente como nombre del directorio.

---

## 47. Copiar o mover

En el ejemplo anterior hemos utilizado:

```python
shutil.copy2()
```

Por tanto, los archivos originales permanecen en:

```text
archivos/
```

y obtenemos una copia en:

```text
clasificados/
```

También existe:

```python
shutil.move()
```

que permite mover un archivo.

Por ejemplo:

```python
shutil.move(
    archivo,
    archivo_destino
)
```

La diferencia es:

```text
copy2()

ORIGEN
  │
  ├──────────→ DESTINO
  │
archivo         copia
permanece
```

frente a:

```text
move()

ORIGEN ─────────→ DESTINO

el archivo cambia
de ubicación
```

!!! warning "Trabajar con archivos reales"

    Durante las prácticas utilizaremos archivos de prueba.

    Un script que mueve, renombra o elimina archivos puede modificar grandes cantidades de información muy rápidamente.

    Debemos probar primero nuestros programas con datos que podamos recuperar fácilmente.

---

## 48. Generar un informe de clasificación

Podemos registrar las operaciones realizadas.

Crea:

```text
clasificar_con_informe.py
```

Partiremos de una lista:

```python
operaciones = []
```

Cada vez que copiemos un archivo añadiremos:

```python
operaciones.append(
    f"{archivo.name} -> {extension}/"
)
```

Finalmente podemos crear un informe:

```python
contenido = "\n".join(
    operaciones
)
```

y guardarlo:

```python
ARCHIVO_INFORME.write_text(
    contenido,
    encoding="utf-8"
)
```

El archivo podría contener:

```text
informe.txt -> txt/
usuarios.csv -> csv/
servidor.log -> log/
notas.txt -> txt/
equipos.csv -> csv/
errores.log -> log/
```

Estamos aplicando nuevamente:

```text
ENTRADA
   ↓
PROCESAMIENTO
   ↓
ACCIÓN
   ↓
REGISTRO
   ↓
INFORME
```

---

## 49. Buscar archivos de forma recursiva

Hasta ahora:

```python
iterdir()
```

y:

```python
glob()
```

han trabajado sobre el directorio indicado.

Pero podemos encontrarnos con una estructura como:

```text
datos/
├── aula1/
│   ├── equipos.csv
│   └── notas.txt
│
├── aula2/
│   └── equipos.csv
│
└── aula3/
    └── inventario.csv
```

Si queremos buscar archivos también dentro de los subdirectorios podemos utilizar:

```python
rglob()
```

Por ejemplo:

```python
for archivo in directorio.rglob("*.csv"):
    print(archivo)
```

`rglob()` realiza una búsqueda recursiva.

Es decir:

```text
DIRECTORIO
    │
    ├── archivos
    │
    ├── subdirectorio
    │       │
    │       └── archivos
    │
    └── subdirectorio
            │
            └── archivos
```

Crea:

```text
buscar_csv_recursivo.py
```

y prueba:

```python
from pathlib import Path


DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)

DIRECTORIO_CAPITULO = (
    DIRECTORIO_PROGRAMA.parent
)


for archivo in (
    DIRECTORIO_CAPITULO.rglob("*.csv")
):

    print(archivo)
```

El programa localizará los archivos CSV dentro de toda la estructura del capítulo.

---

## 50. Obtener información de los archivos

Los objetos `Path` también nos permiten obtener información útil.

Por ejemplo:

```python
archivo.name
```

devuelve el nombre.

```python
archivo.suffix
```

devuelve la extensión.

Y podemos consultar información adicional mediante:

```python
archivo.stat()
```

Por ejemplo:

```python
tamano = archivo.stat().st_size
```

devuelve el tamaño del archivo en bytes.

Crea:

```text
inventario_archivos.py
```

Escribe:

```python
from pathlib import Path


DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)

DIRECTORIO_ARCHIVOS = (
    DIRECTORIO_PROGRAMA.parent
    / "archivos"
)


for archivo in DIRECTORIO_ARCHIVOS.iterdir():

    if archivo.is_file():

        tamano = (
            archivo.stat().st_size
        )

        print(
            f"{archivo.name} - "
            f"{tamano} bytes"
        )
```

Podemos obtener algo parecido a:

```text
informe.txt - 245 bytes
usuarios.csv - 520 bytes
servidor.log - 1240 bytes
notas.txt - 185 bytes
```

Los valores dependerán del contenido real de los archivos.

---

## 51. Práctica propuesta: organizador automático

Crea:

```text
organizador.py
```

El programa debe analizar todos los archivos contenidos en:

```text
archivos/
```

y clasificarlos automáticamente en:

```text
clasificados/
```

según su extensión.

Por ejemplo:

```text
.txt → clasificados/txt/
.csv → clasificados/csv/
.log → clasificados/log/
```

!!! example "Requisitos"

    El programa debe:

    - Utilizar `pathlib`.
    - Recorrer automáticamente los archivos.
    - Ignorar directorios.
    - Detectar la extensión.
    - Crear las carpetas necesarias.
    - Copiar los archivos mediante `shutil.copy2()`.
    - Contar los archivos procesados.
    - Generar un informe.

El resultado final debe mostrar:

```text
ORGANIZADOR DE ARCHIVOS
=======================

informe.txt -> txt/
usuarios.csv -> csv/
servidor.log -> log/
notas.txt -> txt/
equipos.csv -> csv/
errores.log -> log/

RESUMEN
=======

Archivos procesados: 6
```

Además debe generar:

```text
resultados/informe_organizacion.txt
```

---

## 52. Ampliación: clasificador genérico

En lugar de limitar nuestro programa a:

```text
txt
csv
log
```

podemos hacer que cree automáticamente una carpeta para cualquier extensión encontrada.

Por ejemplo:

```text
documento.pdf
foto.png
datos.csv
informe.txt
programa.py
```

podrían generar:

```text
clasificados/
├── pdf/
├── png/
├── csv/
├── txt/
└── py/
```

La clave está en obtener:

```python
extension = (
    archivo.suffix
    .lower()
    .replace(".", "")
)
```

y utilizarla para construir:

```python
carpeta_destino = (
    DESTINO
    / extension
)
```

!!! example "Reto"

    Modifica `organizador.py` para que funcione con cualquier extensión sin tener que indicar previamente los tipos de archivo.

    Decide también qué debe hacer el programa con los archivos que no tengan extensión.

---

## 53. Automatización y seguridad

La automatización tiene una característica muy importante:

> Un programa puede realizar cientos de operaciones en pocos segundos.

Esto es una ventaja, pero también implica un riesgo.

Un error en:

```python
shutil.copy2()
```

puede copiar archivos al lugar equivocado.

Un error utilizando:

```python
shutil.move()
```

puede mover muchos archivos.

Y operaciones de eliminación pueden provocar pérdidas de información.

Por ello, antes de ejecutar una automatización sobre información real conviene:

1. Probarla con archivos de prueba.
2. Comprobar las rutas.
3. Mostrar previamente las operaciones.
4. Mantener copias de seguridad cuando sea necesario.
5. Revisar los resultados.

Una técnica útil consiste en probar primero:

```python
print(
    f"Movería {archivo} "
    f"a {archivo_destino}"
)
```

en lugar de ejecutar directamente:

```python
shutil.move(
    archivo,
    archivo_destino
)
```

Primero comprobamos qué **haría** el programa y, cuando estemos seguros, activamos la operación real.

!!! tip "Primero mostrar, después modificar"

    Cuando desarrolles scripts que modifican muchos archivos, una buena estrategia es crear primero una versión que únicamente muestre las operaciones previstas.

    ```text
    ANALIZAR
        ↓
    MOSTRAR
        ↓
    VERIFICAR
        ↓
    EJECUTAR
    ```

---

## Resumen

En esta parte hemos comprobado que los principios de automatización no se aplican únicamente a las redes.

También podemos automatizar tareas sobre archivos y directorios.

Hemos utilizado:

- `Path.iterdir()`
- `Path.glob()`
- `Path.rglob()`
- `is_file()`
- `suffix`
- `stat().st_size`
- `mkdir()`
- `shutil.copy2()`
- `shutil.move()`
- listas
- bucles
- condiciones
- contadores

El patrón continúa siendo el mismo:

```text
        DIRECTORIO
            │
            ▼
      LOCALIZAR ARCHIVOS
            │
            ▼
         FILTRAR
            │
            ▼
        PROCESAR
            │
            ▼
     COPIAR / MOVER
            │
            ▼
      REGISTRAR ACCIÓN
            │
            ▼
         INFORME
```

Ahora somos capaces de automatizar tanto operaciones de red como operaciones sobre el sistema de archivos.

En la siguiente parte utilizaremos estas técnicas para crear **copias de seguridad automáticas**, combinando directorios, fechas, nombres de archivos y `shutil`.

---

## 54. Automatizar copias de seguridad

Una de las tareas más habituales en administración de sistemas consiste en realizar copias de seguridad.

Imaginemos que tenemos un directorio:

```text
datos_empresa/
```

que contiene:

```text
datos_empresa/
├── clientes.csv
├── equipos.csv
├── configuracion.txt
└── informes/
    ├── enero.txt
    └── febrero.txt
```

Podríamos copiar manualmente este directorio cada vez que queremos realizar una copia de seguridad.

Pero Python puede automatizar el proceso:

```text
DIRECTORIO ORIGINAL
        │
        ▼
      Python
        │
        ▼
crear nombre de copia
        │
        ▼
 copiar directorio
        │
        ▼
COPIA DE SEGURIDAD
```

Además, podemos incluir automáticamente la fecha y la hora en el nombre de cada copia.

---

## 55. Preparar los archivos de prueba

Dentro de:

```text
practicas/capitulo3/
```

crea:

```text
datos_empresa/
```

Dentro crea algunos archivos de prueba:

```text
datos_empresa/
├── clientes.csv
├── equipos.csv
├── configuracion.txt
└── informes/
    ├── enero.txt
    └── febrero.txt
```

También utilizaremos un directorio:

```text
backups/
```

No es necesario crearlo manualmente. Nuestro programa podrá hacerlo.

La estructura será:

```text
capitulo3/
├── archivos/
├── backups/
├── clasificados/
├── datos/
├── datos_empresa/
│   ├── clientes.csv
│   ├── equipos.csv
│   ├── configuracion.txt
│   └── informes/
│       ├── enero.txt
│       └── febrero.txt
├── programas/
└── resultados/
```

---

## 56. Copiar un directorio completo

Anteriormente utilizamos:

```python
shutil.copy2()
```

para copiar archivos individuales.

Para copiar un directorio completo podemos utilizar:

```python
shutil.copytree()
```

Crea:

```text
copia_directorio.py
```

dentro de:

```text
practicas/capitulo3/programas/
```

Escribe:

```python
import shutil
from pathlib import Path


DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)

DIRECTORIO_CAPITULO = (
    DIRECTORIO_PROGRAMA.parent
)

ORIGEN = (
    DIRECTORIO_CAPITULO
    / "datos_empresa"
)

DESTINO = (
    DIRECTORIO_CAPITULO
    / "backups"
    / "copia_datos"
)


DESTINO.parent.mkdir(
    parents=True,
    exist_ok=True
)


shutil.copytree(
    ORIGEN,
    DESTINO
)


print("Copia realizada correctamente.")

print(f"Origen: {ORIGEN}")
print(f"Destino: {DESTINO}")
```

Ejecuta:

```powershell
python copia_directorio.py
```

Obtendremos:

```text
backups/
└── copia_datos/
    ├── clientes.csv
    ├── equipos.csv
    ├── configuracion.txt
    └── informes/
        ├── enero.txt
        └── febrero.txt
```

`copytree()` ha copiado automáticamente toda la estructura.

---

### Un problema al ejecutar el programa otra vez

Ejecuta nuevamente:

```powershell
python copia_directorio.py
```

Dependiendo de cómo utilicemos `copytree()`, encontraremos un problema:

```text
copia_datos
```

ya existe.

Una solución consiste en permitir que el destino exista:

```python
shutil.copytree(
    ORIGEN,
    DESTINO,
    dirs_exist_ok=True
)
```

Sin embargo, en una copia de seguridad normalmente nos interesa conservar diferentes versiones.

Por ejemplo:

```text
copia_2026-09-16
copia_2026-09-17
copia_2026-09-18
```

Para conseguirlo necesitamos generar nombres automáticamente.

---

## 57. Trabajar con la fecha y la hora

Python dispone del módulo:

```python
datetime
```

Podemos obtener la fecha y hora actual mediante:

```python
from datetime import datetime


ahora = datetime.now()

print(ahora)
```

Obtendremos algo parecido a:

```text
2026-09-16 15:32:18.123456
```

El valor exacto dependerá del momento de ejecución.

Normalmente no queremos utilizar directamente todo este texto en el nombre de un archivo o directorio.

Podemos darle formato mediante:

```python
strftime()
```

Por ejemplo:

```python
from datetime import datetime


ahora = datetime.now()

fecha = ahora.strftime(
    "%Y-%m-%d"
)

print(fecha)
```

Resultado:

```text
2026-09-16
```

---

### Formatos de fecha

Algunos códigos habituales son:

```text
%Y → año con cuatro cifras
%m → mes
%d → día
%H → hora
%M → minutos
%S → segundos
```

Por ejemplo:

```python
fecha = datetime.now().strftime(
    "%Y-%m-%d_%H-%M-%S"
)
```

puede generar:

```text
2026-09-16_15-32-18
```

Este formato resulta especialmente útil para nombres de copias de seguridad.

!!! note "Evitar los dos puntos"

    En Windows no podemos utilizar `:` dentro de un nombre de archivo.

    Por ello utilizaremos:

    ```text
    15-32-18
    ```

    en lugar de:

    ```text
    15:32:18
    ```

---

## 58. Crear una copia con fecha y hora

Crea:

```text
backup_con_fecha.py
```

Escribe:

```python
import shutil
from datetime import datetime
from pathlib import Path


DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)

DIRECTORIO_CAPITULO = (
    DIRECTORIO_PROGRAMA.parent
)

ORIGEN = (
    DIRECTORIO_CAPITULO
    / "datos_empresa"
)

DIRECTORIO_BACKUPS = (
    DIRECTORIO_CAPITULO
    / "backups"
)


DIRECTORIO_BACKUPS.mkdir(
    parents=True,
    exist_ok=True
)


fecha = datetime.now().strftime(
    "%Y-%m-%d_%H-%M-%S"
)


DESTINO = (
    DIRECTORIO_BACKUPS
    / f"backup_{fecha}"
)


shutil.copytree(
    ORIGEN,
    DESTINO
)


print()
print("COPIA DE SEGURIDAD")
print("==================")
print()

print("Copia realizada correctamente.")

print()
print(f"Origen: {ORIGEN}")
print(f"Destino: {DESTINO}")
```

Cada vez que ejecutemos el programa se creará un directorio diferente.

Por ejemplo:

```text
backups/
├── backup_2026-09-16_15-32-18/
├── backup_2026-09-16_16-05-42/
└── backup_2026-09-17_08-15-10/
```

Ya tenemos un pequeño sistema de **versionado temporal de copias**.

---

## 59. Comprobar que el origen existe

Nuestro programa supone que:

```text
datos_empresa/
```

existe.

Pero podría haberse eliminado o cambiado de ubicación.

Podemos comprobarlo mediante:

```python
ORIGEN.exists()
```

Por ejemplo:

```python
if not ORIGEN.exists():

    print(
        "ERROR: el directorio "
        "de origen no existe."
    )
```

También podemos comprobar que realmente sea un directorio:

```python
if not ORIGEN.is_dir():

    print(
        "ERROR: el origen "
        "no es un directorio."
    )
```

Podemos combinar ambas comprobaciones:

```python
if not ORIGEN.exists():

    print(
        "ERROR: el directorio "
        "de origen no existe."
    )

elif not ORIGEN.is_dir():

    print(
        "ERROR: el origen "
        "no es un directorio."
    )

else:

    print(
        "El directorio "
        "de origen es correcto."
    )
```

Una automatización debe comprobar sus condiciones antes de realizar operaciones importantes.

---

## 60. Controlar errores durante la copia

`shutil.copytree()` también puede producir excepciones.

Por ejemplo:

- El origen puede no existir.
- Puede faltar permiso para acceder a un archivo.
- Puede producirse un problema durante la copia.

Podemos utilizar:

```python
try
```

y:

```python
except
```

Crea:

```text
backup_seguro.py
```

Escribe:

```python
import shutil
from datetime import datetime
from pathlib import Path


DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)

DIRECTORIO_CAPITULO = (
    DIRECTORIO_PROGRAMA.parent
)

ORIGEN = (
    DIRECTORIO_CAPITULO
    / "datos_empresa"
)

DIRECTORIO_BACKUPS = (
    DIRECTORIO_CAPITULO
    / "backups"
)


def realizar_backup():

    if not ORIGEN.exists():

        print(
            "ERROR: el directorio "
            "de origen no existe."
        )

        return False

    if not ORIGEN.is_dir():

        print(
            "ERROR: el origen "
            "no es un directorio."
        )

        return False


    DIRECTORIO_BACKUPS.mkdir(
        parents=True,
        exist_ok=True
    )


    fecha = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    destino = (
        DIRECTORIO_BACKUPS
        / f"backup_{fecha}"
    )


    try:

        shutil.copytree(
            ORIGEN,
            destino
        )

        print(
            "Copia realizada "
            "correctamente."
        )

        print(
            f"Destino: {destino}"
        )

        return True

    except OSError as error:

        print(
            "ERROR durante "
            "la copia."
        )

        print(error)

        return False


realizar_backup()
```

Ahora el programa devuelve:

```python
True
```

si la copia se realiza correctamente y:

```python
False
```

si falla.

---

## 61. Registrar las copias realizadas

Un administrador puede necesitar saber:

```text
cuándo se realizó una copia
si terminó correctamente
dónde se almacenó
```

Podemos crear un archivo:

```text
resultados/historial_backups.txt
```

Cada ejecución añadirá una nueva línea.

Para abrir un archivo sin borrar el contenido anterior utilizamos:

```python
"a"
```

Por ejemplo:

```python
with open(
    ARCHIVO_HISTORIAL,
    "a",
    encoding="utf-8"
) as archivo:

    archivo.write(
        "Backup realizado\n"
    )
```

El modo:

```text
a
```

significa:

```text
append
```

es decir, **añadir al final**.

---

### Añadir fecha al historial

Podemos registrar:

```python
fecha_registro = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)
```

Después:

```python
with open(
    ARCHIVO_HISTORIAL,
    "a",
    encoding="utf-8"
) as archivo:

    archivo.write(
        f"{fecha_registro} - "
        f"Backup correcto\n"
    )
```

El archivo podría contener:

```text
2026-09-16 15:32:18 - Backup correcto
2026-09-16 17:10:42 - Backup correcto
2026-09-17 08:15:10 - Backup correcto
```

Ahora disponemos de un pequeño **registro histórico**.

---

## 62. Crear una función de registro

Podemos separar esta tarea en una función:

```python
def registrar(mensaje):

    fecha = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        ARCHIVO_HISTORIAL,
        "a",
        encoding="utf-8"
    ) as archivo:

        archivo.write(
            f"{fecha} - {mensaje}\n"
        )
```

Después podemos utilizar:

```python
registrar(
    "Backup realizado correctamente"
)
```

o:

```python
registrar(
    "ERROR durante el backup"
)
```

Estamos introduciendo una idea muy utilizada en administración:

```text
OPERACIÓN
    │
    ▼
RESULTADO
    │
    ▼
REGISTRO
```

A estos registros se les suele denominar:

```text
logs
```

---

## 63. Programa completo de backup

Vamos a reunir los elementos anteriores.

Crea:

```text
backup_automatico.py
```

Escribe:

```python
import shutil
from datetime import datetime
from pathlib import Path


DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)

DIRECTORIO_CAPITULO = (
    DIRECTORIO_PROGRAMA.parent
)

ORIGEN = (
    DIRECTORIO_CAPITULO
    / "datos_empresa"
)

DIRECTORIO_BACKUPS = (
    DIRECTORIO_CAPITULO
    / "backups"
)

DIRECTORIO_RESULTADOS = (
    DIRECTORIO_CAPITULO
    / "resultados"
)

ARCHIVO_HISTORIAL = (
    DIRECTORIO_RESULTADOS
    / "historial_backups.txt"
)


DIRECTORIO_RESULTADOS.mkdir(
    parents=True,
    exist_ok=True
)


def registrar(mensaje):

    fecha = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        ARCHIVO_HISTORIAL,
        "a",
        encoding="utf-8"
    ) as archivo:

        archivo.write(
            f"{fecha} - {mensaje}\n"
        )


def realizar_backup():

    if not ORIGEN.exists():

        mensaje = (
            "ERROR: directorio "
            "de origen inexistente"
        )

        print(mensaje)
        registrar(mensaje)

        return False


    DIRECTORIO_BACKUPS.mkdir(
        parents=True,
        exist_ok=True
    )


    fecha_backup = (
        datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )
    )

    destino = (
        DIRECTORIO_BACKUPS
        / f"backup_{fecha_backup}"
    )


    try:

        shutil.copytree(
            ORIGEN,
            destino
        )

        mensaje = (
            f"Backup correcto -> "
            f"{destino.name}"
        )

        print(mensaje)

        registrar(mensaje)

        return True

    except OSError as error:

        mensaje = (
            f"ERROR durante backup: "
            f"{error}"
        )

        print(mensaje)

        registrar(mensaje)

        return False


realizar_backup()
```

Después de varias ejecuciones podemos tener:

```text
backups/
├── backup_2026-09-16_15-32-18/
├── backup_2026-09-16_17-10-42/
└── backup_2026-09-17_08-15-10/
```

y:

```text
resultados/
└── historial_backups.txt
```

---

## 64. Contar las copias existentes

También podemos obtener información sobre las copias almacenadas.

Por ejemplo:

```python
backups = list(
    DIRECTORIO_BACKUPS.glob(
        "backup_*"
    )
)
```

Después:

```python
print(
    f"Número de copias: "
    f"{len(backups)}"
)
```

Si tenemos:

```text
backup_2026-09-16_15-32-18
backup_2026-09-16_17-10-42
backup_2026-09-17_08-15-10
```

obtendremos:

```text
Número de copias: 3
```

Podemos también recorrerlas:

```python
for backup in backups:
    print(backup.name)
```

---

## 65. Práctica propuesta: gestor de copias

Crea:

```text
gestor_backups.py
```

El programa deberá mostrar:

```text
================================
       GESTOR DE BACKUPS
================================

1. Realizar copia de seguridad
2. Mostrar copias existentes
3. Mostrar historial
4. Salir

Selecciona una opción:
```

### Opción 1

Debe crear una copia completa de:

```text
datos_empresa/
```

en:

```text
backups/
```

utilizando un nombre con:

```text
fecha + hora
```

### Opción 2

Debe mostrar las copias existentes:

```text
COPIAS DISPONIBLES
==================

backup_2026-09-16_15-32-18
backup_2026-09-16_17-10-42
backup_2026-09-17_08-15-10
```

### Opción 3

Debe mostrar el contenido de:

```text
resultados/historial_backups.txt
```

### Opción 4

Debe finalizar el programa.

!!! example "Requisitos"

    El programa debe utilizar:

    - `pathlib`
    - `shutil`
    - `datetime`
    - funciones
    - `try` y `except`
    - bucles
    - archivos de texto
    - modo `a`
    - un menú mediante `while`

---

## 66. Reto: controlar el número de copias

Si realizamos una copia todos los días, el directorio:

```text
backups/
```

crecerá continuamente.

Podemos establecer, por ejemplo:

```python
MAX_BACKUPS = 5
```

El objetivo será conservar únicamente las cinco copias más recientes.

Podemos obtener las copias:

```python
backups = list(
    DIRECTORIO_BACKUPS.glob(
        "backup_*"
    )
)
```

Como nuestros nombres comienzan por una fecha en formato:

```text
YYYY-MM-DD_HH-MM-SS
```

podemos ordenarlos:

```python
backups.sort()
```

Si existen más de:

```python
MAX_BACKUPS
```

podemos identificar las más antiguas.

!!! warning "No elimines todavía automáticamente"

    En este ejercicio identifica y muestra primero qué copias deberían eliminarse:

    ```text
    Se eliminaría: backup_2026-09-10_08-00-00
    Se eliminaría: backup_2026-09-11_08-00-00
    ```

    No utilices todavía código de eliminación.

    Antes de automatizar operaciones destructivas debemos verificar cuidadosamente qué elementos van a verse afectados.

---

## 67. Automatizar no significa programar la ejecución

Nuestro script ya realiza automáticamente una copia completa cuando lo ejecutamos:

```powershell
python backup_automatico.py
```

Pero existe una diferencia importante entre:

```text
automatizar una tarea
```

y:

```text
programar cuándo se ejecuta
```

Nuestro programa automatiza **qué hay que hacer**:

```text
comprobar origen
      ↓
crear nombre
      ↓
copiar archivos
      ↓
registrar resultado
```

Pero todavía alguien debe iniciar:

```text
backup_automatico.py
```

Para ejecutar automáticamente un script todos los días, por ejemplo a las 22:00, podemos utilizar herramientas del propio sistema operativo, como el **Programador de tareas de Windows**.

La idea sería:

```text
Programador de tareas
         │
         │ 22:00
         ▼
      Python
         │
         ▼
backup_automatico.py
         │
         ▼
      backups/
```

En este capítulo nos centraremos principalmente en desarrollar correctamente los scripts. La programación periódica de su ejecución puede realizarse posteriormente con las herramientas de administración del sistema.

---

## 68. Buenas prácticas en copias automatizadas

Antes de considerar que un sistema de copias funciona correctamente debemos tener en cuenta varios aspectos.

### Comprobar el origen

Antes de copiar:

```python
ORIGEN.exists()
```

### Comprobar los resultados

No debemos asumir que una copia ha funcionado únicamente porque el programa ha terminado.

### Registrar las operaciones

Mantener:

```text
historial_backups.txt
```

nos permite conocer cuándo se realizaron las operaciones.

### Utilizar nombres únicos

Incluir:

```text
fecha + hora
```

evita sobrescribir copias anteriores.

### Probar con datos no importantes

Durante el desarrollo debemos trabajar con archivos de prueba.

### Verificar la recuperación

Una copia de seguridad solo resulta realmente útil si posteriormente podemos recuperar los datos que contiene.

!!! tip "Copia y recuperación"

    El objetivo de una copia de seguridad no es simplemente crear archivos duplicados.

    Debemos poder localizar la copia adecuada y recuperar la información cuando sea necesario.

---

## Resumen

En esta parte hemos aplicado la automatización a una tarea real de administración: las copias de seguridad.

Hemos aprendido a utilizar:

- `shutil.copytree()`
- `datetime`
- `datetime.now()`
- `strftime()`
- `Path.exists()`
- `Path.is_dir()`
- `glob()`
- el modo de apertura `a`
- registros históricos
- control de errores

Nuestro proceso de backup es:

```text
       ORIGEN
          │
          ▼
      COMPROBAR
          │
          ▼
   GENERAR FECHA/HORA
          │
          ▼
    CREAR DESTINO
          │
          ▼
     copytree()
          │
          ▼
   COPIA DE SEGURIDAD
          │
          ▼
      REGISTRAR
          │
          ▼
       HISTORIAL
```

A estas alturas ya somos capaces de combinar archivos, directorios, comandos, bucles, funciones y control de errores para construir pequeñas herramientas de administración.

En la siguiente parte integraremos los principales conocimientos del capítulo en una **práctica final de automatización**, antes de cerrar el capítulo 3.

---

## 69. Práctica final: herramienta de automatización

Para finalizar el capítulo vamos a desarrollar una pequeña herramienta que integre las técnicas de automatización estudiadas.

Nuestra aplicación permitirá:

```text
GESTOR DE ADMINISTRACIÓN
        │
        ├── comprobar equipos
        ├── generar informe de red
        ├── realizar backup
        ├── consultar backups
        └── consultar historial
```

Utilizaremos como entrada el inventario:

```text
datos/inventario.csv
```

y almacenaremos los resultados en:

```text
resultados/
```

y:

```text
backups/
```

---

## 70. Preparar el proyecto

Dentro de:

```text
practicas/capitulo3/
```

debemos tener una estructura similar a:

```text
capitulo3/
├── datos/
│   └── inventario.csv
│
├── datos_empresa/
│   ├── clientes.csv
│   ├── equipos.csv
│   ├── configuracion.txt
│   └── informes/
│       ├── enero.txt
│       └── febrero.txt
│
├── programas/
│   └── gestor_administracion.py
│
├── resultados/
│
└── backups/
```

El archivo:

```text
inventario.csv
```

puede contener:

```csv
nombre,ip,sistema,ubicacion
PC-AULA-01,192.168.1.101,Windows 11,Aula 1
PC-AULA-02,192.168.1.102,Windows 11,Aula 1
PC-AULA-03,192.168.1.103,Windows 11,Aula 1
SERVIDOR-01,192.168.1.10,Ubuntu Server,CPD
ROUTER-01,192.168.1.1,Cisco IOS,Armario comunicaciones
```

Adapta las direcciones IP a la red utilizada durante la práctica.

---

## 71. Definir las rutas

Crea:

```text
gestor_administracion.py
```

Comenzaremos importando los módulos necesarios:

```python
import csv
import shutil
import subprocess

from datetime import datetime
from pathlib import Path
```

Ahora definimos las rutas:

```python
DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)

DIRECTORIO_CAPITULO = (
    DIRECTORIO_PROGRAMA.parent
)

ARCHIVO_INVENTARIO = (
    DIRECTORIO_CAPITULO
    / "datos"
    / "inventario.csv"
)

DIRECTORIO_DATOS = (
    DIRECTORIO_CAPITULO
    / "datos_empresa"
)

DIRECTORIO_RESULTADOS = (
    DIRECTORIO_CAPITULO
    / "resultados"
)

DIRECTORIO_BACKUPS = (
    DIRECTORIO_CAPITULO
    / "backups"
)

ARCHIVO_HISTORIAL = (
    DIRECTORIO_RESULTADOS
    / "historial.txt"
)
```

Preparamos los directorios:

```python
DIRECTORIO_RESULTADOS.mkdir(
    parents=True,
    exist_ok=True
)

DIRECTORIO_BACKUPS.mkdir(
    parents=True,
    exist_ok=True
)
```

---

## 72. Crear el registro de operaciones

Vamos a registrar las principales acciones realizadas por nuestra herramienta.

```python
def registrar(mensaje):

    fecha = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        ARCHIVO_HISTORIAL,
        "a",
        encoding="utf-8"
    ) as archivo:

        archivo.write(
            f"{fecha} - {mensaje}\n"
        )
```

Podremos utilizar:

```python
registrar(
    "Comprobación de equipos realizada"
)
```

El archivo:

```text
historial.txt
```

irá acumulando información:

```text
2026-09-16 10:25:14 - Comprobación de equipos realizada
2026-09-16 10:30:02 - Informe de red generado
2026-09-16 10:42:18 - Backup realizado
```

---

## 73. Cargar el inventario

Creamos una función para cargar:

```text
inventario.csv
```

```python
def cargar_inventario():

    equipos = []

    try:

        with open(
            ARCHIVO_INVENTARIO,
            "r",
            encoding="utf-8"
        ) as archivo:

            lector = csv.DictReader(
                archivo
            )

            for equipo in lector:
                equipos.append(equipo)

    except FileNotFoundError:

        print(
            "ERROR: no se encuentra "
            "el inventario."
        )

    return equipos
```

La función devuelve una lista con los registros del CSV.

---

## 74. Comprobar un equipo

Creamos ahora la función encargada de realizar el `ping`.

```python
def comprobar_equipo(ip):

    try:

        resultado = subprocess.run(
            [
                "ping",
                "-n",
                "1",
                ip
            ],
            capture_output=True,
            text=True,
            timeout=5
        )

        return (
            resultado.returncode == 0
        )

    except FileNotFoundError:

        print(
            "ERROR: no se encuentra "
            "el comando ping."
        )

        return False

    except subprocess.TimeoutExpired:

        return False
```

Esta función recibe una dirección:

```python
comprobar_equipo(
    "192.168.1.101"
)
```

y devuelve:

```text
True
```

o:

```text
False
```

---

## 75. Comprobar todo el inventario

Ahora podemos utilizar las dos funciones anteriores.

```python
def comprobar_inventario():

    equipos = cargar_inventario()

    if not equipos:

        print(
            "No hay equipos "
            "para comprobar."
        )

        return


    print()
    print("ESTADO DE LOS EQUIPOS")
    print("=====================")
    print()


    activos = 0
    inactivos = 0


    for equipo in equipos:

        nombre = equipo["nombre"]
        ip = equipo["ip"]

        if comprobar_equipo(ip):

            estado = "RESPONDE"
            activos += 1

        else:

            estado = "NO RESPONDE"
            inactivos += 1


        print(
            f"{nombre} - "
            f"{ip} - "
            f"{estado}"
        )


    print()
    print("RESUMEN")
    print("=======")

    print(
        f"Equipos comprobados: "
        f"{len(equipos)}"
    )

    print(
        f"Responden: {activos}"
    )

    print(
        f"No responden: {inactivos}"
    )


    registrar(
        "Comprobación de equipos realizada"
    )
```

Ya podemos comprobar todo el inventario mediante:

```python
comprobar_inventario()
```

---

## 76. Generar un informe de red

Ahora queremos guardar los resultados.

```python
def generar_informe_red():

    equipos = cargar_inventario()

    if not equipos:

        print(
            "No hay equipos "
            "para comprobar."
        )

        return


    lineas = []

    activos = 0
    inactivos = 0


    for equipo in equipos:

        nombre = equipo["nombre"]
        ip = equipo["ip"]

        if comprobar_equipo(ip):

            estado = "RESPONDE"
            activos += 1

        else:

            estado = "NO RESPONDE"
            inactivos += 1


        linea = (
            f"{nombre} - "
            f"{ip} - "
            f"{estado}"
        )

        lineas.append(linea)


    informe = ""

    informe += (
        "INFORME DE ESTADO DE RED\n"
    )

    informe += (
        "=========================\n\n"
    )


    for linea in lineas:
        informe += linea + "\n"


    informe += "\nRESUMEN\n"
    informe += "=======\n"

    informe += (
        f"Equipos comprobados: "
        f"{len(equipos)}\n"
    )

    informe += (
        f"Responden: "
        f"{activos}\n"
    )

    informe += (
        f"No responden: "
        f"{inactivos}\n"
    )


    fecha = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )


    archivo_informe = (
        DIRECTORIO_RESULTADOS
        / f"informe_red_{fecha}.txt"
    )


    archivo_informe.write_text(
        informe,
        encoding="utf-8"
    )


    print()
    print(
        "Informe generado correctamente."
    )

    print(
        f"Archivo: {archivo_informe}"
    )


    registrar(
        f"Informe generado: "
        f"{archivo_informe.name}"
    )
```

Cada ejecución genera un archivo diferente:

```text
resultados/
├── informe_red_2026-09-16_10-30-02.txt
├── informe_red_2026-09-16_12-15-25.txt
└── historial.txt
```

---

## 77. Incorporar las copias de seguridad

Añadimos ahora:

```python
def realizar_backup():

    if not DIRECTORIO_DATOS.exists():

        print(
            "ERROR: no existe "
            "datos_empresa."
        )

        registrar(
            "ERROR: origen del backup "
            "inexistente"
        )

        return


    fecha = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )


    destino = (
        DIRECTORIO_BACKUPS
        / f"backup_{fecha}"
    )


    try:

        shutil.copytree(
            DIRECTORIO_DATOS,
            destino
        )

        print()
        print(
            "Backup realizado "
            "correctamente."
        )

        print(
            f"Destino: {destino}"
        )


        registrar(
            f"Backup realizado: "
            f"{destino.name}"
        )

    except OSError as error:

        print(
            f"ERROR durante "
            f"el backup: {error}"
        )

        registrar(
            f"ERROR durante backup: "
            f"{error}"
        )
```

Ahora nuestra aplicación también puede realizar copias de seguridad.

---

## 78. Mostrar las copias existentes

Creamos:

```python
def mostrar_backups():

    backups = sorted(
        DIRECTORIO_BACKUPS.glob(
            "backup_*"
        )
    )


    print()
    print("COPIAS DE SEGURIDAD")
    print("===================")
    print()


    if not backups:

        print(
            "No existen copias "
            "de seguridad."
        )

        return


    for backup in backups:

        print(
            backup.name
        )


    print()

    print(
        f"Total: {len(backups)}"
    )
```

Esta función permite consultar las copias almacenadas sin acceder manualmente al directorio.

---

## 79. Mostrar el historial

También podemos consultar nuestro registro.

```python
def mostrar_historial():

    print()
    print("HISTORIAL")
    print("=========")
    print()


    if not ARCHIVO_HISTORIAL.exists():

        print(
            "Todavía no existe "
            "un historial."
        )

        return


    contenido = (
        ARCHIVO_HISTORIAL.read_text(
            encoding="utf-8"
        )
    )


    print(contenido)
```

---

## 80. Crear el menú principal

Ahora podemos unir todas las funciones mediante un menú.

```python
def mostrar_menu():

    print()
    print(
        "===================================="
    )

    print(
        "      GESTOR DE ADMINISTRACIÓN"
    )

    print(
        "===================================="
    )

    print()

    print(
        "1. Comprobar equipos"
    )

    print(
        "2. Generar informe de red"
    )

    print(
        "3. Realizar copia de seguridad"
    )

    print(
        "4. Mostrar copias de seguridad"
    )

    print(
        "5. Mostrar historial"
    )

    print(
        "6. Salir"
    )

    print()
```

Y finalmente:

```python
while True:

    mostrar_menu()

    opcion = input(
        "Selecciona una opción: "
    )


    if opcion == "1":

        comprobar_inventario()

    elif opcion == "2":

        generar_informe_red()

    elif opcion == "3":

        realizar_backup()

    elif opcion == "4":

        mostrar_backups()

    elif opcion == "5":

        mostrar_historial()

    elif opcion == "6":

        print()
        print(
            "Programa finalizado."
        )

        break

    else:

        print()
        print(
            "Opción incorrecta."
        )
```

---

## 81. Funcionamiento de la aplicación

Ejecuta:

```powershell
python gestor_administracion.py
```

Debe aparecer:

```text
====================================
      GESTOR DE ADMINISTRACIÓN
====================================

1. Comprobar equipos
2. Generar informe de red
3. Realizar copia de seguridad
4. Mostrar copias de seguridad
5. Mostrar historial
6. Salir

Selecciona una opción:
```

Prueba todas las opciones.

---

### Comprobar equipos

Selecciona:

```text
1
```

El programa debe leer:

```text
inventario.csv
```

y comprobar automáticamente todos los equipos.

---

### Generar informe

Selecciona:

```text
2
```

Comprueba que aparece un nuevo archivo en:

```text
resultados/
```

Por ejemplo:

```text
informe_red_2026-09-16_10-30-02.txt
```

---

### Realizar backup

Selecciona:

```text
3
```

Comprueba:

```text
backups/
```

Debe aparecer un nuevo directorio:

```text
backup_2026-09-16_10-35-12/
```

---

### Consultar backups

Selecciona:

```text
4
```

El programa debe mostrar las copias existentes.

---

### Consultar historial

Selecciona:

```text
5
```

Debemos poder consultar las operaciones realizadas.

---

### Salir

Selecciona:

```text
6
```

El programa debe finalizar correctamente.

---

## 82. Qué estamos automatizando

Nuestra aplicación reúne diferentes procesos:

```text
             INVENTARIO CSV
                  │
                  ▼
           CARGAR EQUIPOS
                  │
                  ▼
            COMPROBAR RED
                  │
                  ▼
              INFORME


           DATOS EMPRESA
                  │
                  ▼
             COPYTREE
                  │
                  ▼
               BACKUP


             OPERACIONES
                  │
                  ▼
              REGISTRO
                  │
                  ▼
             HISTORIAL
```

Ya no estamos creando ejemplos independientes.

Estamos construyendo una pequeña aplicación de administración.

---

## 83. Práctica de ampliación

Amplía:

```text
gestor_administracion.py
```

añadiendo una nueva opción:

```text
6. Información del sistema
7. Salir
```

La nueva opción debe ejecutar:

```text
hostname
```

y:

```text
systeminfo
```

mediante:

```python
subprocess.run()
```

El resultado debe guardarse en:

```text
resultados/informacion_sistema.txt
```

También debe registrarse la operación en:

```text
historial.txt
```

De esta forma estaremos combinando directamente los capítulos 1, 2 y 3.

---

## 84. Reto final

Crea una nueva versión:

```text
gestor_administracion_v2.py
```

con el siguiente menú:

```text
====================================
      GESTOR DE ADMINISTRACIÓN
====================================

1. Comprobar inventario
2. Comprobar rango de IP
3. Generar informe de red
4. Organizar archivos
5. Realizar backup
6. Mostrar backups
7. Mostrar historial
8. Información del sistema
9. Salir
```

!!! example "Condiciones"

    La aplicación deberá:

    - Estar organizada mediante funciones.
    - Utilizar `pathlib`.
    - Leer archivos CSV.
    - Ejecutar comandos mediante `subprocess`.
    - Utilizar bucles.
    - Controlar errores.
    - Generar nombres mediante fecha y hora.
    - Crear directorios automáticamente.
    - Realizar copias de seguridad.
    - Generar informes.
    - Registrar las operaciones realizadas.

No es necesario copiar literalmente los programas anteriores.

El objetivo es reutilizar las técnicas estudiadas y decidir cómo organizar correctamente la aplicación.

---

## 85. Qué hemos aprendido

Durante este capítulo hemos partido de una tarea muy sencilla:

```text
repetir una operación
```

y hemos ido construyendo procesos cada vez más completos.

Hemos trabajado con:

```text
listas
   │
   ▼
bucles
   │
   ▼
funciones
   │
   ▼
automatización
```

También hemos utilizado archivos externos:

```text
TXT / CSV
    │
    ▼
  Python
    │
    ▼
procesamiento
```

Hemos generado automáticamente rangos:

```text
range()
   │
   ▼
direcciones
   │
   ▼
comprobaciones
```

Hemos automatizado operaciones sobre archivos:

```text
iterdir()
glob()
rglob()
copy2()
move()
```

Y hemos creado copias de seguridad utilizando:

```text
datetime
    +
copytree()
    +
registro
```

---

## 86. Integración de los tres primeros capítulos

Los tres capítulos de esta parte forman ahora un conjunto.

```text
CAPÍTULO 1
Gestión de archivos
       │
       ▼
pathlib + CSV
       │
       │
       ▼
CAPÍTULO 2
Comandos del sistema
       │
       ▼
subprocess
       │
       │
       ▼
CAPÍTULO 3
Automatización
       │
       ▼
bucles + funciones
       │
       ▼
HERRAMIENTAS DE ADMINISTRACIÓN
```

Esto nos permite pasar de scripts muy sencillos a programas capaces de realizar tareas reales de forma automática.

---

## 87. Buenas prácticas

Antes de finalizar debemos recordar algunas reglas importantes.

### Separar los datos del código

Siempre que sea posible:

```text
datos
  ↓
TXT / CSV
```

en lugar de introducir grandes cantidades de información directamente en el programa.

### Utilizar funciones

Una función debe realizar una tarea concreta.

Por ejemplo:

```python
cargar_inventario()
comprobar_equipo()
realizar_backup()
registrar()
```

### Controlar los errores

Una automatización debe estar preparada para situaciones como:

```text
archivo inexistente
directorio inexistente
comando no disponible
timeout
error durante una copia
```

### Registrar operaciones

Cuando una tarea se realiza automáticamente es importante saber posteriormente qué ocurrió.

### Probar antes de modificar

Especialmente cuando trabajamos con:

```text
mover
renombrar
sobrescribir
eliminar
```

primero debemos comprobar qué hará el programa.

---

## 88. Conclusión

Automatizar no consiste simplemente en utilizar un bucle.

Una automatización completa normalmente sigue un proceso:

```text
      ENTRADA
         │
         ▼
      VALIDAR
         │
         ▼
      PROCESAR
         │
         ▼
       ACTUAR
         │
         ▼
     COMPROBAR
         │
         ▼
     REGISTRAR
         │
         ▼
      INFORMAR
```

Python nos permite combinar estas etapas utilizando herramientas relativamente sencillas.

En este capítulo hemos utilizado estas técnicas para:

```text
comprobar equipos
procesar inventarios
generar rangos
clasificar archivos
crear informes
realizar backups
mantener historiales
```

Con ello hemos construido la base necesaria para desarrollar scripts de administración más completos.

!!! success "Capítulo completado"

    Al finalizar este capítulo debemos ser capaces de identificar una tarea repetitiva, dividirla en operaciones sencillas y crear un programa Python que la ejecute automáticamente de forma controlada.

    Ya disponemos de una base formada por:

```text
ARCHIVOS
    +
COMANDOS
    +
AUTOMATIZACIÓN
    =
SCRIPT DE ADMINISTRACIÓN
```