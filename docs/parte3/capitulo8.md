# Capítulo 8. Proyecto final: herramienta de administración de red

Durante los capítulos anteriores hemos aprendido diferentes técnicas de programación aplicadas a la administración de sistemas y redes.

Hemos trabajado con:

```text
archivos y directorios
CSV
pathlib
subprocess
automatización
argparse
excepciones
logging
HTTP y APIs
JSON
socket
DNS
depuración
```

Hasta ahora hemos estudiado estas herramientas mediante programas y prácticas relativamente independientes.

Ha llegado el momento de utilizarlas conjuntamente.

En este capítulo desarrollaremos el:

```text
PROYECTO FINAL
```

del curso.

Construiremos progresivamente una herramienta de administración de red escrita en Python.

El programa permitirá:

```text
leer inventario de equipos
          │
          ▼
validar información
          │
          ▼
resolver nombres
          │
          ▼
comprobar conectividad
          │
          ├── ping
          │
          └── puertos TCP
          │
          ▼
procesar resultados
          │
          ▼
generar informes
          │
          ├── TXT
          │
          └── JSON
          │
          ▼
registrar incidencias
          │
          ▼
          LOG
```

Este proyecto servirá para integrar los conocimientos desarrollados durante todo el libro.

---

## 1. Diseño y preparación del proyecto final

Antes de comenzar a programar debemos definir claramente qué queremos construir.

Nuestro proyecto será una herramienta denominada:

```text
Administrador de red
```

El programa recibirá un inventario de equipos y realizará automáticamente diferentes comprobaciones.

No construiremos toda la aplicación de una sola vez.

Seguiremos un desarrollo incremental:

```text
VERSIÓN 1
Inventario
    │
    ▼
VERSIÓN 2
Ping
    │
    ▼
VERSIÓN 3
Puertos TCP
    │
    ▼
VERSIÓN 4
Informes
    │
    ▼
VERSIÓN 5
Logging y errores
    │
    ▼
VERSIÓN FINAL
Integración completa
```

Cada versión deberá funcionar antes de comenzar la siguiente.

!!! tip "Desarrollo incremental"

    Dividir una aplicación grande en pequeños pasos facilita su desarrollo y su depuración.

    Si aparece un problema sabremos aproximadamente qué modificación lo ha introducido.

---

### 2. Objetivo general

La aplicación deberá ser capaz de leer un archivo:

```text
equipos.csv
```

con información sobre diferentes equipos de una red.

Por ejemplo:

```csv
nombre,host,puertos
ServidorWeb,192.168.1.10,80;443
ServidorSSH,192.168.1.20,22
NAS,192.168.1.30,445
Router,192.168.1.1,80;443
```

Para cada equipo tendremos:

```text
nombre
host
puertos
```

Posteriormente comprobaremos:

```text
conectividad mediante ping
```

y:

```text
accesibilidad de puertos TCP
```

---

### 3. Resultado esperado

Al finalizar el proyecto podremos ejecutar un comando similar a:

```powershell
python administrador_red.py --inventario ../datos/equipos.csv
```

El programa analizará los equipos y generará información como:

```text
Analizando: ServidorWeb
Host: 192.168.1.10

Ping:
ACCESIBLE

Puertos:
80  -> ACCESIBLE
443 -> ACCESIBLE
```

Los resultados también podrán almacenarse en archivos.

Por ejemplo:

```text
resultados/
├── informe_red.txt
└── informe_red.json
```

Además tendremos:

```text
logs/
└── administrador_red.log
```

---

### 4. Arquitectura general

Podemos representar la aplicación:

```text
             equipos.csv
                  │
                  ▼
          cargar_inventario()
                  │
                  ▼
          validar_equipo()
                  │
                  ▼
             EQUIPO
                  │
         ┌────────┴────────┐
         │                 │
         ▼                 ▼
      PING              SOCKET
         │                 │
         ▼                 ▼
 conectividad        puertos TCP
         │                 │
         └────────┬────────┘
                  │
                  ▼
              RESULTADO
                  │
         ┌────────┴────────┐
         │                 │
         ▼                 ▼
        TXT               JSON
         │                 │
         └────────┬────────┘
                  │
                  ▼
                 LOG
```

Cada parte tendrá una responsabilidad concreta.

---

### 5. Estructura del proyecto

Crearemos:

```text
practicas/
└── capitulo8/
    ├── datos/
    │   └── equipos.csv
    │
    ├── logs/
    │
    ├── programas/
    │   └── administrador_red.py
    │
    └── resultados/
```

Esta estructura separa:

```text
DATOS
│
└── información de entrada


PROGRAMAS
│
└── código Python


RESULTADOS
│
└── informes generados


LOGS
│
└── registro de ejecución
```

---

### 6. Crear los directorios

Desde la raíz de nuestro proyecto podemos crear manualmente:

```text
practicas/capitulo8/
```

y dentro:

```text
datos
logs
programas
resultados
```

El resultado será:

```text
capitulo8
│
├── datos
├── logs
├── programas
└── resultados
```

!!! note "Organización"

    Mantener separados los datos, programas, resultados y logs facilita el mantenimiento de la aplicación.

---

### 7. Crear el inventario

Crea:

```text
practicas/capitulo8/datos/equipos.csv
```

Utilizaremos inicialmente:

```csv
nombre,host,puertos
Router,192.168.1.1,80;443
ServidorWeb,192.168.1.10,80;443
ServidorSSH,192.168.1.20,22
NAS,192.168.1.30,445
```

Las direcciones son solamente un ejemplo.

Debemos adaptarlas a la red utilizada durante las prácticas.

!!! warning "Red autorizada"

    Las pruebas de conectividad y puertos deben realizarse únicamente sobre equipos propios o redes donde tengamos autorización para realizar estas comprobaciones.

---

### 8. ¿Por qué utilizamos CSV?

CSV resulta adecuado para un inventario sencillo porque:

```text
es fácil de crear
```

```text
es fácil de modificar
```

```text
puede abrirse con un editor de texto
```

```text
puede abrirse con una hoja de cálculo
```

```text
Python puede procesarlo fácilmente
```

Ya utilizamos este formato en capítulos anteriores.

Ahora lo incorporaremos a una aplicación completa.

---

### 9. Diseño de cada registro

Cada línea representa un equipo.

Por ejemplo:

```csv
ServidorWeb,192.168.1.10,80;443
```

Podemos interpretarla como:

```text
nombre
│
└── ServidorWeb


host
│
└── 192.168.1.10


puertos
│
└── 80;443
```

El campo:

```text
puertos
```

contiene varios valores separados mediante:

```text
;
```

---

### 10. ¿Por qué utilizamos `;` dentro del campo?

Nuestro archivo utiliza:

```text
,
```

para separar columnas:

```csv
nombre,host,puertos
```

Por tanto, para separar varios puertos dentro de una misma columna utilizaremos:

```text
;
```

Ejemplo:

```text
80;443
```

Posteriormente Python podrá convertirlo en:

```python
[
    80,
    443
]
```

---

### 11. Representación interna de un equipo

Después de leer el CSV queremos representar:

```csv
ServidorWeb,192.168.1.10,80;443
```

mediante un diccionario:

```python
{
    "nombre": "ServidorWeb",
    "host": "192.168.1.10",
    "puertos": [
        80,
        443
    ]
}
```

Esta representación será más cómoda para trabajar desde Python.

---

### 12. Primer objetivo

En esta primera versión nuestro programa solamente hará:

```text
equipos.csv
     │
     ▼
leer archivo
     │
     ▼
convertir datos
     │
     ▼
crear lista
     │
     ▼
mostrar inventario
```

Todavía no utilizaremos:

```text
ping
socket
JSON
logging
```

Los añadiremos progresivamente.

---

### 13. Crear el programa

Crea:

```text
practicas/capitulo8/programas/
administrador_red.py
```

Comenzaremos con:

```python
import csv

from pathlib import Path
```

Utilizaremos:

```python
csv
```

para procesar el inventario.

Y:

```python
Path
```

para trabajar con rutas.

---

### 14. Construir las rutas

Añade:

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
    / "equipos.csv"
)
```

Así evitamos depender del directorio desde el que ejecutemos el programa.

---

### 15. Comprobar la ruta

Temporalmente podemos añadir:

```python
print(
    ARCHIVO_INVENTARIO
)
```

Ejecuta:

```powershell
python administrador_red.py
```

Deberíamos obtener una ruta que termine en:

```text
practicas\capitulo8\datos\equipos.csv
```

Una vez comprobada podemos eliminar el `print()` temporal.

---

### 16. Crear `cargar_inventario()`

Vamos a crear:

```python
def cargar_inventario(
    archivo
):

    equipos = []

    with archivo.open(
        "r",
        encoding="utf-8",
        newline=""
    ) as fichero:

        lector = csv.DictReader(
            fichero
        )

        for fila in lector:

            print(
                fila
            )

    return equipos
```

Todavía no estamos creando los equipos.

Únicamente queremos comprobar qué obtiene:

```python
csv.DictReader
```

---

### 17. Ejecutar la primera lectura

Al final añade:

```python
equipos = cargar_inventario(
    ARCHIVO_INVENTARIO
)
```

Ejecuta:

```powershell
python administrador_red.py
```

Obtendremos diccionarios similares a:

```text
{
    'nombre': 'Router',
    'host': '192.168.1.1',
    'puertos': '80;443'
}
```

Observa un detalle importante:

```text
puertos
```

es todavía:

```text
'80;443'
```

Es una cadena de texto.

---

### 18. Convertir los puertos

Necesitamos transformar:

```text
"80;443"
```

en:

```python
[
    80,
    443
]
```

Primero podemos utilizar:

```python
fila["puertos"].split(";")
```

Por ejemplo:

```python
"80;443".split(";")
```

produce:

```python
[
    "80",
    "443"
]
```

Todavía son cadenas.

---

### 19. Convertir cada puerto a entero

Podemos utilizar:

```python
puertos = []


for puerto in fila["puertos"].split(";"):

    puertos.append(
        int(puerto)
    )
```

Ahora:

```python
puertos
```

contendrá:

```python
[
    80,
    443
]
```

Cada elemento será un:

```text
int
```

---

### 20. Crear el diccionario del equipo

Dentro del bucle construiremos:

```python
equipo = {
    "nombre": fila["nombre"],
    "host": fila["host"],
    "puertos": puertos
}
```

Después:

```python
equipos.append(
    equipo
)
```

---

### 21. Primera versión de `cargar_inventario()`

La función completa será:

```python
def cargar_inventario(
    archivo
):

    equipos = []

    with archivo.open(
        "r",
        encoding="utf-8",
        newline=""
    ) as fichero:

        lector = csv.DictReader(
            fichero
        )

        for fila in lector:

            puertos = []

            for puerto in (
                fila["puertos"].split(";")
            ):

                puertos.append(
                    int(puerto)
                )

            equipo = {
                "nombre": fila["nombre"],
                "host": fila["host"],
                "puertos": puertos
            }

            equipos.append(
                equipo
            )

    return equipos
```

---

### 22. Mostrar los equipos

Después de cargar:

```python
equipos = cargar_inventario(
    ARCHIVO_INVENTARIO
)
```

podemos recorrerlos:

```python
for equipo in equipos:

    print(
        equipo
    )
```

La salida será similar a:

```text
{'nombre': 'Router', 'host': '192.168.1.1', 'puertos': [80, 443]}

{'nombre': 'ServidorWeb', 'host': '192.168.1.10', 'puertos': [80, 443]}

{'nombre': 'ServidorSSH', 'host': '192.168.1.20', 'puertos': [22]}

{'nombre': 'NAS', 'host': '192.168.1.30', 'puertos': [445]}
```

Ya hemos transformado el CSV en estructuras Python.

---

### 23. Limpiar cadenas de texto

Es recomendable eliminar espacios innecesarios.

Podemos utilizar:

```python
.strip()
```

Por ejemplo:

```python
nombre = (
    fila["nombre"].strip()
)
```

y:

```python
host = (
    fila["host"].strip()
)
```

También podemos limpiar cada puerto:

```python
puerto.strip()
```

antes de convertirlo.

---

### 24. Mejorar la conversión de puertos

Podemos escribir:

```python
puertos = []


for puerto in (
    fila["puertos"].split(";")
):

    puerto = puerto.strip()

    if puerto:

        puertos.append(
            int(puerto)
        )
```

La condición:

```python
if puerto:
```

evita intentar convertir una cadena vacía.

Por ejemplo:

```text
80;443;
```

produce también un elemento vacío después del último `;`.

---

### 25. Primera validación

No deberíamos asumir que todos los datos son correctos.

Vamos a crear:

```python
def validar_equipo(
    equipo
):

    if not equipo["nombre"]:

        return False

    if not equipo["host"]:

        return False

    if not equipo["puertos"]:

        return False

    return True
```

Esta será nuestra primera validación.

Más adelante podremos mejorarla.

---

### 26. Validar los puertos

Los puertos TCP tienen valores numéricos comprendidos entre:

```text
1
```

y:

```text
65535
```

Podemos comprobar:

```python
for puerto in equipo["puertos"]:

    if puerto < 1 or puerto > 65535:

        return False
```

Nuestra función será:

```python
def validar_equipo(
    equipo
):

    if not equipo["nombre"]:

        return False

    if not equipo["host"]:

        return False

    if not equipo["puertos"]:

        return False

    for puerto in equipo["puertos"]:

        if (
            puerto < 1
            or puerto > 65535
        ):

            return False

    return True
```

---

### 27. Separar carga y validación

Es importante diferenciar:

```text
CARGAR
```

de:

```text
VALIDAR
```

La función:

```python
cargar_inventario()
```

se ocupa de obtener los datos.

La función:

```python
validar_equipo()
```

decide si los datos son aceptables.

Podemos representar:

```text
CSV
 │
 ▼
cargar
 │
 ▼
diccionario
 │
 ▼
validar
 │
 ├── correcto
 │
 └── incorrecto
```

Separar responsabilidades facilita el mantenimiento del programa.

---

### 28. Mostrar el inventario

Crearemos:

```python
def mostrar_inventario(
    equipos
):

    for equipo in equipos:

        print(
            "\n"
            f"Nombre: "
            f"{equipo['nombre']}"
        )

        print(
            f"Host: "
            f"{equipo['host']}"
        )

        print(
            "Puertos:",
            equipo["puertos"]
        )
```

Así obtenemos una salida más legible que mostrando directamente los diccionarios.

---

### 29. Filtrar equipos válidos

Podemos crear:

```python
def obtener_equipos_validos(
    equipos
):

    validos = []

    for equipo in equipos:

        if validar_equipo(
            equipo
        ):

            validos.append(
                equipo
            )

    return validos
```

Ahora tenemos:

```text
inventario original
       │
       ▼
validación
       │
       ▼
inventario válido
```

---

### 30. Probar un puerto incorrecto

Modifica temporalmente el CSV:

```csv
nombre,host,puertos
Router,192.168.1.1,80;443
ServidorWeb,192.168.1.10,80;70000
ServidorSSH,192.168.1.20,22
NAS,192.168.1.30,445
```

Tenemos:

```text
70000
```

que está fuera del intervalo:

```text
1 - 65535
```

La función:

```python
validar_equipo()
```

deberá rechazar:

```text
ServidorWeb
```

---

### 31. Mostrar equipos rechazados

Podemos mejorar:

```python
def obtener_equipos_validos(
    equipos
):

    validos = []

    for equipo in equipos:

        if validar_equipo(
            equipo
        ):

            validos.append(
                equipo
            )

        else:

            print(
                "Equipo incorrecto:",
                equipo["nombre"]
            )

    return validos
```

Ahora sabremos qué equipos han sido descartados.

Más adelante sustituiremos o complementaremos estos mensajes con:

```text
logging
```

---

### 32. Otro problema: puerto no numérico

Modifica temporalmente:

```csv
ServidorSSH,192.168.1.20,SSH
```

Al ejecutar:

```python
int(
    "SSH"
)
```

obtendremos:

```text
ValueError
```

Esto significa que el error aparece:

```text
antes de validar_equipo()
```

durante la conversión de los datos.

Debemos gestionar esta situación.

---

### 33. Gestionar puertos incorrectos

Podemos crear una función específica:

```python
def convertir_puertos(
    texto
):

    puertos = []

    for puerto in texto.split(";"):

        puerto = puerto.strip()

        if not puerto:

            continue

        try:

            numero = int(
                puerto
            )

        except ValueError:

            return None

        puertos.append(
            numero
        )

    return puertos
```

Esta función transforma:

```text
"80;443"
```

en:

```python
[
    80,
    443
]
```

Pero si encuentra:

```text
"80;SSH"
```

devuelve:

```python
None
```

---

### 34. ¿Por qué devolver `None`?

Queremos diferenciar:

```python
[]
```

de:

```python
None
```

Podemos interpretar:

```text
[]
```

como:

```text
no hay puertos
```

y:

```text
None
```

como:

```text
no se han podido
convertir los puertos
```

Esta decisión forma parte del diseño de nuestra aplicación.

---

### 35. Utilizar `convertir_puertos()`

Dentro de:

```python
cargar_inventario()
```

podemos utilizar:

```python
puertos = convertir_puertos(
    fila["puertos"]
)
```

Después:

```python
if puertos is None:

    print(
        "Puertos incorrectos:",
        fila["nombre"]
    )

    continue
```

Así una fila incorrecta no detendrá todo el procesamiento.

---

### 36. Versión mejorada de la carga

Podemos escribir:

```python
def cargar_inventario(
    archivo
):

    equipos = []

    with archivo.open(
        "r",
        encoding="utf-8",
        newline=""
    ) as fichero:

        lector = csv.DictReader(
            fichero
        )

        for fila in lector:

            nombre = (
                fila["nombre"].strip()
            )

            host = (
                fila["host"].strip()
            )

            puertos = convertir_puertos(
                fila["puertos"]
            )

            if puertos is None:

                print(
                    "Puertos incorrectos:",
                    nombre
                )

                continue

            equipo = {
                "nombre": nombre,
                "host": host,
                "puertos": puertos
            }

            equipos.append(
                equipo
            )

    return equipos
```

---

### 37. Gestionar un archivo inexistente

¿Qué ocurre si:

```text
equipos.csv
```

no existe?

La instrucción:

```python
archivo.open(...)
```

puede producir:

```text
FileNotFoundError
```

Podemos gestionarlo en el programa principal:

```python
try:

    equipos = cargar_inventario(
        ARCHIVO_INVENTARIO
    )

except FileNotFoundError:

    print(
        "No se encuentra "
        "el inventario."
    )

    raise SystemExit(1)
```

---

### 38. Gestionar otros errores de archivo

También podemos capturar:

```python
OSError
```

por ejemplo:

```python
try:

    equipos = cargar_inventario(
        ARCHIVO_INVENTARIO
    )

except FileNotFoundError:

    print(
        "No se encuentra "
        "el inventario."
    )

    raise SystemExit(1)

except OSError as error:

    print(
        "Error leyendo "
        f"el inventario: {error}"
    )

    raise SystemExit(1)
```

---

### 39. Comprobar las columnas del CSV

Nuestro programa espera:

```text
nombre
host
puertos
```

Pero alguien podría crear:

```csv
equipo,direccion,servicios
```

En ese caso nuestro programa no encontraría:

```python
fila["nombre"]
```

Debemos poder detectar también este problema.

---

### 40. Utilizar `fieldnames`

`csv.DictReader` proporciona:

```python
lector.fieldnames
```

Podemos comprobar:

```python
columnas_necesarias = {
    "nombre",
    "host",
    "puertos"
}
```

y después:

```python
columnas_disponibles = set(
    lector.fieldnames or []
)
```

---

### 41. Comparar columnas

Podemos comprobar:

```python
if not columnas_necesarias.issubset(
    columnas_disponibles
):

    raise ValueError(
        "El CSV no contiene "
        "las columnas necesarias."
    )
```

Así detectamos un formato incorrecto antes de comenzar a procesar las filas.

---

### 42. Actualizar `cargar_inventario()`

Nuestra función puede comenzar:

```python
def cargar_inventario(
    archivo
):

    equipos = []

    with archivo.open(
        "r",
        encoding="utf-8",
        newline=""
    ) as fichero:

        lector = csv.DictReader(
            fichero
        )

        columnas_necesarias = {
            "nombre",
            "host",
            "puertos"
        }

        columnas_disponibles = set(
            lector.fieldnames or []
        )

        if not columnas_necesarias.issubset(
            columnas_disponibles
        ):

            raise ValueError(
                "El CSV no contiene "
                "las columnas necesarias."
            )

        # Continuará el procesamiento...
```

---

### 43. Capturar el formato incorrecto

En el programa principal podemos añadir:

```python
except ValueError as error:

    print(
        f"Inventario incorrecto: "
        f"{error}"
    )

    raise SystemExit(1)
```

Ahora distinguimos:

```text
archivo inexistente
```

```text
problema de lectura
```

```text
estructura CSV incorrecta
```

---

### 44. Primera versión funcional completa

Nuestro programa puede quedar de momento así:

```python
import csv

from pathlib import Path


DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)


DIRECTORIO_CAPITULO = (
    DIRECTORIO_PROGRAMA.parent
)


ARCHIVO_INVENTARIO = (
    DIRECTORIO_CAPITULO
    / "datos"
    / "equipos.csv"
)


def convertir_puertos(
    texto
):

    puertos = []

    for puerto in texto.split(";"):

        puerto = puerto.strip()

        if not puerto:

            continue

        try:

            numero = int(
                puerto
            )

        except ValueError:

            return None

        puertos.append(
            numero
        )

    return puertos


def cargar_inventario(
    archivo
):

    equipos = []

    with archivo.open(
        "r",
        encoding="utf-8",
        newline=""
    ) as fichero:

        lector = csv.DictReader(
            fichero
        )

        columnas_necesarias = {
            "nombre",
            "host",
            "puertos"
        }

        columnas_disponibles = set(
            lector.fieldnames or []
        )

        if not columnas_necesarias.issubset(
            columnas_disponibles
        ):

            raise ValueError(
                "El CSV no contiene "
                "las columnas necesarias."
            )

        for fila in lector:

            nombre = (
                fila["nombre"].strip()
            )

            host = (
                fila["host"].strip()
            )

            puertos = convertir_puertos(
                fila["puertos"]
            )

            if puertos is None:

                print(
                    "Puertos incorrectos:",
                    nombre
                )

                continue

            equipo = {
                "nombre": nombre,
                "host": host,
                "puertos": puertos
            }

            equipos.append(
                equipo
            )

    return equipos


def validar_equipo(
    equipo
):

    if not equipo["nombre"]:

        return False

    if not equipo["host"]:

        return False

    if not equipo["puertos"]:

        return False

    for puerto in equipo["puertos"]:

        if (
            puerto < 1
            or puerto > 65535
        ):

            return False

    return True


def obtener_equipos_validos(
    equipos
):

    validos = []

    for equipo in equipos:

        if validar_equipo(
            equipo
        ):

            validos.append(
                equipo
            )

        else:

            print(
                "Equipo incorrecto:",
                equipo["nombre"]
            )

    return validos


def mostrar_inventario(
    equipos
):

    for equipo in equipos:

        print(
            "\n"
            f"Nombre: "
            f"{equipo['nombre']}"
        )

        print(
            f"Host: "
            f"{equipo['host']}"
        )

        print(
            "Puertos:",
            equipo["puertos"]
        )


try:

    equipos = cargar_inventario(
        ARCHIVO_INVENTARIO
    )

except FileNotFoundError:

    print(
        "No se encuentra "
        "el inventario."
    )

    raise SystemExit(1)

except ValueError as error:

    print(
        f"Inventario incorrecto: "
        f"{error}"
    )

    raise SystemExit(1)

except OSError as error:

    print(
        "Error leyendo "
        f"el inventario: {error}"
    )

    raise SystemExit(1)


equipos_validos = (
    obtener_equipos_validos(
        equipos
    )
)


mostrar_inventario(
    equipos_validos
)
```

---

### 45. Probar la versión 1

Restaura:

```text
equipos.csv
```

a:

```csv
nombre,host,puertos
Router,192.168.1.1,80;443
ServidorWeb,192.168.1.10,80;443
ServidorSSH,192.168.1.20,22
NAS,192.168.1.30,445
```

Ejecuta:

```powershell
python administrador_red.py
```

Deberemos obtener los cuatro equipos.

---

### 46. Pruebas que debemos realizar

Antes de continuar prueba diferentes situaciones.

#### Inventario correcto

```csv
ServidorWeb,192.168.1.10,80;443
```

Debe cargarse.

#### Puerto fuera de rango

```csv
ServidorWeb,192.168.1.10,70000
```

Debe rechazarse durante la validación.

#### Puerto no numérico

```csv
ServidorWeb,192.168.1.10,HTTP
```

Debe detectarse durante la conversión.

#### Nombre vacío

```csv
,192.168.1.10,80
```

Debe rechazarse.

#### Host vacío

```csv
ServidorWeb,,80
```

Debe rechazarse.

#### Sin puertos

```csv
ServidorWeb,192.168.1.10,
```

Debe rechazarse.

---

### 47. Probar columnas incorrectas

Modifica temporalmente la cabecera:

```csv
equipo,direccion,servicios
```

El programa debe mostrar un mensaje similar a:

```text
Inventario incorrecto:
El CSV no contiene las columnas necesarias.
```

Después restaura:

```csv
nombre,host,puertos
```

---

### 48. Utilizar el depurador

Este proyecto es una buena oportunidad para aplicar el Capítulo 7.

Coloca un breakpoint en:

```python
for fila in lector:
```

Inicia:

```text
F5
```

Observa:

```text
fila
```

Después utiliza:

```text
F10
```

para seguir la conversión.

---

### 49. Utilizar Watch

Añade:

```python
fila["nombre"]
```

```python
fila["host"]
```

```python
fila["puertos"]
```

Después de crear:

```python
equipo
```

añade:

```python
equipo
```

Podremos observar cómo:

```text
fila CSV
```

se transforma en:

```text
diccionario Python
```

---

### 50. Depurar `convertir_puertos()`

Coloca un breakpoint en:

```python
puertos = convertir_puertos(
    fila["puertos"]
)
```

Utiliza:

```text
F11
```

para entrar en la función.

Observa:

```text
texto
puerto
numero
puertos
```

Esto nos permitirá seguir la transformación:

```text
"80;443"
    │
    ▼
"80" "443"
    │
    ▼
80 443
    │
    ▼
[80, 443]
```

---

### 51. Breakpoint condicional

Podemos detenernos únicamente cuando procesemos:

```text
ServidorWeb
```

utilizando una condición:

```python
fila["nombre"] == "ServidorWeb"
```

Esto demuestra cómo las herramientas del capítulo anterior se incorporan al desarrollo del proyecto final.

---

### 52. Primera versión completada

Ya tenemos:

```text
equipos.csv
      │
      ▼
cargar_inventario()
      │
      ▼
convertir_puertos()
      │
      ▼
validar_equipo()
      │
      ▼
obtener_equipos_validos()
      │
      ▼
mostrar_inventario()
```

Todavía no estamos comprobando la red.

Pero ya hemos construido una base fiable sobre la que continuar.

---

### 53. Separación de responsabilidades

Nuestro programa comienza a tener funciones especializadas:

```text
convertir_puertos()
        │
        └── convierte datos


cargar_inventario()
        │
        └── lee CSV


validar_equipo()
        │
        └── valida datos


obtener_equipos_validos()
        │
        └── filtra inventario


mostrar_inventario()
        │
        └── presenta información
```

Esta organización hará mucho más sencillo añadir nuevas funciones.

---

### 54. Lo que no debemos añadir todavía

En esta primera versión no necesitamos:

```text
ping
```

```text
socket
```

```text
JSON
```

```text
logging
```

```text
argparse
```

Aunque ya conocemos estas herramientas, las incorporaremos de manera progresiva.

Así podremos probar cada fase independientemente.

---

### 55. Ejercicio de ampliación

Añade al CSV:

```csv
PCProfesor,192.168.1.50,22;80;443;3389
```

Ejecuta el programa.

Comprueba que Python genera:

```python
{
    "nombre": "PCProfesor",
    "host": "192.168.1.50",
    "puertos": [
        22,
        80,
        443,
        3389
    ]
}
```

Cambia después uno de los puertos por:

```text
99999
```

y comprueba que el equipo es rechazado.

---

### 56. Reto de depuración

Introduce deliberadamente:

```csv
ServidorPrueba,192.168.1.100,80;ABC;443
```

No analices únicamente el mensaje de error.

Utiliza el depurador.

Debes:

1. Colocar un breakpoint antes de `convertir_puertos()`.
2. Utilizar `Step Into`.
3. Observar `texto`.
4. Observar cada valor de `puerto`.
5. Detectar cuándo aparece `ABC`.
6. Observar qué ocurre al intentar convertirlo.
7. Seguir el valor devuelto por la función.
8. Comprobar por qué la fila no se incorpora al inventario.

---

### 57. Estado actual del proyecto

Hemos completado:

```text
[✓] estructura del proyecto

[✓] inventario CSV

[✓] lectura del inventario

[✓] conversión de puertos

[✓] validación básica

[✓] control de errores de lectura

[✓] comprobación de columnas

[✓] filtrado de equipos incorrectos

[✓] visualización del inventario
```

Todavía falta:

```text
[ ] argumentos de ejecución

[ ] ping

[ ] resolución DNS

[ ] comprobación TCP

[ ] generación de resultados

[ ] informe TXT

[ ] informe JSON

[ ] logging

[ ] integración final
```

---

### 58. Resumen de esta primera parte

En esta primera fase del proyecto final hemos diseñado la arquitectura general de nuestra herramienta de administración de red.

Hemos creado:

```text
equipos.csv
```

y desarrollado funciones para:

```text
leer
convertir
validar
filtrar
mostrar
```

los equipos.

Nuestro programa ya transforma:

```text
CSV
```

en estructuras Python:

```python
{
    "nombre": "...",
    "host": "...",
    "puertos": [...]
}
```

También hemos comenzado a construir una aplicación robusta capaz de detectar:

```text
archivos inexistentes
columnas incorrectas
puertos no numéricos
puertos fuera de rango
datos incompletos
```

!!! success "Primera fase completada"

    La primera versión del proyecto final ya puede cargar y validar correctamente un inventario básico de equipos.

    Antes de continuar debemos asegurarnos de que todas las pruebas de esta parte funcionan correctamente.

En la siguiente fase incorporaremos la primera comprobación real de red:

```text
inventario
    │
    ▼
equipo
    │
    ▼
host
    │
    ▼
PING
    │
    ├── accesible
    │
    └── no accesible
```

Reutilizaremos `subprocess`, gestionaremos los diferentes resultados y construiremos una función de diagnóstico que posteriormente combinaremos con las comprobaciones TCP mediante `socket`.

---

## 59. Segunda fase: comprobación de conectividad mediante ping

En la primera fase del proyecto construimos la base de nuestra aplicación.

Actualmente podemos:

```text
leer equipos.csv
       │
       ▼
convertir los datos
       │
       ▼
validar equipos
       │
       ▼
obtener inventario válido
```

Ahora comenzaremos a realizar comprobaciones reales sobre los equipos.

La primera será:

```text
PING
```

El objetivo será determinar si un host responde a una comprobación básica de conectividad.

El nuevo flujo será:

```text
equipos.csv
     │
     ▼
cargar inventario
     │
     ▼
validar equipos
     │
     ▼
para cada equipo
     │
     ▼
    ping
     │
 ┌───┴──────────┐
 │              │
 ▼              ▼
RESPONDE     NO RESPONDE
```

!!! warning "Red autorizada"

    Realiza estas prácticas únicamente con equipos propios, máquinas del laboratorio o sistemas sobre los que tengas autorización.

---

### 60. Recordatorio de `subprocess`

En capítulos anteriores utilizamos:

```python
subprocess
```

para ejecutar comandos del sistema desde Python.

Por ejemplo:

```python
import subprocess
```

y posteriormente:

```python
subprocess.run(...)
```

Esto nos permite ejecutar desde Python comandos que normalmente escribiríamos en:

```text
PowerShell
```

o:

```text
Símbolo del sistema
```

En nuestro proyecto utilizaremos esta técnica para ejecutar:

```text
ping
```

---

### 61. Probar `ping` manualmente

Antes de programarlo debemos comprobar cómo funciona desde Windows.

Abre el terminal integrado de VS Code.

Prueba:

```powershell
ping 127.0.0.1
```

La dirección:

```text
127.0.0.1
```

representa normalmente la interfaz de loopback del propio equipo.

Deberíamos recibir respuestas.

También podemos probar:

```powershell
ping localhost
```

---

### 62. Limitar el número de paquetes

En Windows podemos utilizar:

```powershell
ping -n 1 127.0.0.1
```

La opción:

```text
-n 1
```

indica que queremos enviar:

```text
1
```

solicitud de eco.

Esto es adecuado para nuestro programa porque no queremos que cada comprobación envíe varios paquetes.

---

### 63. Código de retorno

Cuando ejecutamos un comando mediante:

```python
subprocess.run()
```

podemos consultar:

```python
resultado.returncode
```

En términos generales:

```text
returncode = 0
```

indica que el comando terminó correctamente.

Un valor diferente de:

```text
0
```

indica que el comando no terminó con éxito según su código de salida.

Para nuestro diagnóstico utilizaremos esta información como una primera aproximación.

---

### 64. Primera función de ping

Añade al principio de:

```text
administrador_red.py
```

la importación:

```python
import subprocess
```

Ahora crea:

```python
def comprobar_ping(
    host
):

    resultado = subprocess.run(
        [
            "ping",
            "-n",
            "1",
            host
        ],
        capture_output=True,
        text=True
    )

    return (
        resultado.returncode == 0
    )
```

La función devuelve:

```python
True
```

si el comando termina con código:

```text
0
```

y:

```python
False
```

en caso contrario.

---

### 65. Probar la función

Temporalmente podemos añadir:

```python
estado = comprobar_ping(
    "127.0.0.1"
)


print(
    estado
)
```

Ejecuta:

```powershell
python administrador_red.py
```

Deberíamos obtener:

```text
True
```

Si el equipo responde correctamente.

Después elimina esta prueba temporal.

---

### 66. Comprender los argumentos

La llamada:

```python
subprocess.run(
    [
        "ping",
        "-n",
        "1",
        host
    ]
)
```

equivale aproximadamente a ejecutar:

```powershell
ping -n 1 192.168.1.10
```

si:

```python
host = "192.168.1.10"
```

Utilizamos una lista:

```python
[
    "ping",
    "-n",
    "1",
    host
]
```

para indicar el programa y sus argumentos.

---

### 67. Evitar `shell=True`

Para este proyecto no necesitamos:

```python
shell=True
```

Podemos ejecutar directamente:

```python
subprocess.run(
    [
        "ping",
        "-n",
        "1",
        host
    ]
)
```

Esto hace más explícita la ejecución del comando y evita introducir innecesariamente un intérprete de comandos intermedio.

---

### 68. Capturar la salida

Hemos utilizado:

```python
capture_output=True
```

Esto permite capturar:

```text
stdout
```

y:

```text
stderr
```

en lugar de mostrar automáticamente toda la salida del comando en pantalla.

Podemos consultar:

```python
resultado.stdout
```

y:

```python
resultado.stderr
```

---

### 69. Probar `stdout`

Temporalmente podemos utilizar:

```python
resultado = subprocess.run(
    [
        "ping",
        "-n",
        "1",
        "127.0.0.1"
    ],
    capture_output=True,
    text=True
)


print(
    resultado.stdout
)
```

Veremos la salida producida por:

```text
ping
```

Pero para nuestro diagnóstico básico no necesitamos analizar todo ese texto.

Nos centraremos principalmente en:

```python
returncode
```

---

### 70. ¿Por qué no analizar el texto de `ping`?

La salida textual puede depender de:

```text
sistema operativo
idioma
versión
```

Por ejemplo, un Windows configurado en castellano puede mostrar mensajes diferentes de uno configurado en inglés.

Por tanto, para una comprobación sencilla es preferible utilizar:

```python
returncode
```

en lugar de buscar palabras concretas dentro de:

```python
stdout
```

---

### 71. Añadir un tiempo máximo

Existe un problema importante.

Un host que no responde puede hacer que:

```text
ping
```

tarde demasiado.

Podemos limitar el tiempo de ejecución utilizando:

```python
timeout
```

Por ejemplo:

```python
resultado = subprocess.run(
    [
        "ping",
        "-n",
        "1",
        host
    ],
    capture_output=True,
    text=True,
    timeout=3
)
```

Esto permite evitar que nuestra aplicación quede esperando indefinidamente.

---

### 72. `TimeoutExpired`

Si el comando supera el tiempo establecido:

```python
subprocess.run()
```

puede producir:

```python
subprocess.TimeoutExpired
```

Por tanto, debemos gestionarlo.

```python
try:

    resultado = subprocess.run(
        [
            "ping",
            "-n",
            "1",
            host
        ],
        capture_output=True,
        text=True,
        timeout=3
    )

except subprocess.TimeoutExpired:

    return False
```

---

### 73. Mejorar `comprobar_ping()`

Nuestra función será:

```python
def comprobar_ping(
    host,
    timeout=3
):

    try:

        resultado = subprocess.run(
            [
                "ping",
                "-n",
                "1",
                host
            ],
            capture_output=True,
            text=True,
            timeout=timeout
        )

    except subprocess.TimeoutExpired:

        return False

    return (
        resultado.returncode == 0
    )
```

Ahora tenemos una función más robusta.

---

### 74. ¿Qué significa que un ping falle?

Es importante interpretar correctamente el resultado.

Si obtenemos:

```text
PING NO RESPONDE
```

no podemos concluir automáticamente:

```text
el equipo está apagado
```

Puede ocurrir que:

```text
ICMP esté bloqueado
```

```text
un firewall no responda al ping
```

```text
exista un problema de red
```

```text
el nombre no pueda resolverse
```

```text
el host no esté disponible
```

Por tanto:

```text
ping sin respuesta
```

significa solamente que:

```text
no hemos obtenido una respuesta
satisfactoria mediante esta prueba
```

---

### 75. Ping y disponibilidad de servicios

Un equipo puede:

```text
NO responder al ping
```

y sin embargo tener:

```text
un puerto TCP accesible
```

Por ejemplo:

```text
PING
 │
 └── NO RESPONDE


TCP 443
 │
 └── ACCESIBLE
```

Por eso nuestro proyecto no dependerá exclusivamente de `ping`.

Más adelante comprobaremos también los puertos mediante:

```python
socket
```

---

### 76. Crear estados más descriptivos

En lugar de devolver:

```python
True
```

o:

```python
False
```

podemos utilizar estados más descriptivos.

Por ejemplo:

```text
ACCESIBLE
NO_ACCESIBLE
TIMEOUT
ERROR
```

Esto proporcionará mejores informes.

---

### 77. Nueva versión de `comprobar_ping()`

Podemos escribir:

```python
def comprobar_ping(
    host,
    timeout=3
):

    try:

        resultado = subprocess.run(
            [
                "ping",
                "-n",
                "1",
                host
            ],
            capture_output=True,
            text=True,
            timeout=timeout
        )

    except subprocess.TimeoutExpired:

        return "TIMEOUT"

    except OSError:

        return "ERROR"

    if resultado.returncode == 0:

        return "ACCESIBLE"

    return "NO_ACCESIBLE"
```

Ahora obtenemos más información.

---

### 78. ¿Por qué capturamos `OSError`?

`subprocess.run()` necesita ejecutar:

```text
ping
```

como programa externo.

Si por algún motivo el sistema no puede ejecutar el comando, puede producirse un error del sistema.

Capturamos:

```python
OSError
```

para evitar que nuestra aplicación termine bruscamente.

Más adelante registraremos este tipo de incidencias mediante:

```text
logging
```

---

### 79. Probar varios hosts

Podemos realizar una prueba temporal:

```python
hosts = [
    "127.0.0.1",
    "localhost",
    "192.168.1.1"
]


for host in hosts:

    estado = comprobar_ping(
        host
    )

    print(
        host,
        estado
    )
```

Los resultados dependerán de nuestra red.

Por ejemplo:

```text
127.0.0.1 ACCESIBLE
localhost ACCESIBLE
192.168.1.1 ACCESIBLE
```

o:

```text
192.168.1.1 NO_ACCESIBLE
```

No debemos asumir que todos los equipos del ejemplo existen en nuestra red.

---

### 80. Integrar ping con el inventario

Ya tenemos:

```python
equipos_validos
```

Podemos recorrerlos:

```python
for equipo in equipos_validos:

    estado_ping = comprobar_ping(
        equipo["host"]
    )

    print(
        equipo["nombre"],
        estado_ping
    )
```

Ahora nuestra aplicación comienza a realizar un diagnóstico real.

---

### 81. Primera salida del diagnóstico

Podemos obtener:

```text
Router ACCESIBLE
ServidorWeb NO_ACCESIBLE
ServidorSSH NO_ACCESIBLE
NAS NO_ACCESIBLE
```

Los resultados dependerán completamente de:

```text
la red utilizada
```

y de:

```text
los hosts configurados
```

en:

```text
equipos.csv
```

---

### 82. Crear una función específica

No queremos dejar todo el código en el programa principal.

Crearemos:

```python
def diagnosticar_equipo(
    equipo
):

    estado_ping = comprobar_ping(
        equipo["host"]
    )

    resultado = {
        "nombre": equipo["nombre"],
        "host": equipo["host"],
        "ping": estado_ping
    }

    return resultado
```

Esta función recibe:

```text
equipo
```

y devuelve:

```text
resultado
```

---

### 83. Entrada y salida de `diagnosticar_equipo()`

La entrada podría ser:

```python
{
    "nombre": "Router",
    "host": "192.168.1.1",
    "puertos": [
        80,
        443
    ]
}
```

La salida:

```python
{
    "nombre": "Router",
    "host": "192.168.1.1",
    "ping": "ACCESIBLE"
}
```

Más adelante añadiremos:

```text
DNS
puertos TCP
```

al mismo resultado.

---

### 84. Preparar la estructura futura

Podemos incluir ya:

```python
"puertos": []
```

en el resultado.

```python
resultado = {
    "nombre": equipo["nombre"],
    "host": equipo["host"],
    "ping": estado_ping,
    "puertos": []
}
```

Todavía no rellenaremos esa lista.

Pero estamos diseñando la estructura que utilizaremos posteriormente.

---

### 85. Crear `diagnosticar_red()`

Queremos diagnosticar todos los equipos.

Podemos crear:

```python
def diagnosticar_red(
    equipos
):

    resultados = []

    for equipo in equipos:

        resultado = diagnosticar_equipo(
            equipo
        )

        resultados.append(
            resultado
        )

    return resultados
```

Tenemos:

```text
lista de equipos
      │
      ▼
diagnosticar_red()
      │
      ▼
diagnosticar_equipo()
      │
      ▼
comprobar_ping()
      │
      ▼
lista de resultados
```

---

### 86. Ejecutar el diagnóstico

Después de obtener:

```python
equipos_validos
```

podemos utilizar:

```python
resultados = diagnosticar_red(
    equipos_validos
)
```

Ahora:

```python
resultados
```

será una lista de diccionarios.

Por ejemplo:

```python
[
    {
        "nombre": "Router",
        "host": "192.168.1.1",
        "ping": "ACCESIBLE",
        "puertos": []
    },
    {
        "nombre": "ServidorWeb",
        "host": "192.168.1.10",
        "ping": "NO_ACCESIBLE",
        "puertos": []
    }
]
```

---

### 87. Separar inventario y resultados

Es importante comprender que ahora tenemos dos estructuras diferentes.

El:

```text
INVENTARIO
```

describe lo que queremos comprobar.

Por ejemplo:

```python
{
    "nombre": "ServidorWeb",
    "host": "192.168.1.10",
    "puertos": [
        80,
        443
    ]
}
```

Mientras:

```text
RESULTADOS
```

describe qué hemos encontrado.

Por ejemplo:

```python
{
    "nombre": "ServidorWeb",
    "host": "192.168.1.10",
    "ping": "NO_ACCESIBLE",
    "puertos": []
}
```

Esta separación será importante al generar los informes.

---

### 88. Mostrar resultados

Crearemos:

```python
def mostrar_resultados(
    resultados
):

    for resultado in resultados:

        print(
            "\n"
            "===================="
        )

        print(
            f"Equipo: "
            f"{resultado['nombre']}"
        )

        print(
            f"Host: "
            f"{resultado['host']}"
        )

        print(
            f"Ping: "
            f"{resultado['ping']}"
        )
```

---

### 89. Ejecutar la nueva versión

El programa principal podrá terminar con:

```python
equipos_validos = (
    obtener_equipos_validos(
        equipos
    )
)


resultados = diagnosticar_red(
    equipos_validos
)


mostrar_resultados(
    resultados
)
```

Ya no necesitamos llamar obligatoriamente a:

```python
mostrar_inventario()
```

porque ahora estamos mostrando:

```text
resultados del diagnóstico
```

---

### 90. Primera arquitectura funcional

Nuestro programa tiene ahora este flujo:

```text
equipos.csv
     │
     ▼
cargar_inventario()
     │
     ▼
convertir_puertos()
     │
     ▼
validar_equipo()
     │
     ▼
equipos válidos
     │
     ▼
diagnosticar_red()
     │
     ▼
diagnosticar_equipo()
     │
     ▼
comprobar_ping()
     │
     ▼
resultados
     │
     ▼
mostrar_resultados()
```

La aplicación ya empieza a parecerse al proyecto final.

---

### 91. Añadir duración de la comprobación

Podemos medir cuánto tarda un ping.

Para ello utilizaremos:

```python
time
```

Añade:

```python
import time
```

Podemos medir:

```python
inicio = time.perf_counter()
```

antes de ejecutar el comando.

Y:

```python
fin = time.perf_counter()
```

después.

---

### 92. Calcular la duración

Podemos utilizar:

```python
duracion = (
    fin - inicio
)
```

Por ejemplo:

```text
0.0432 segundos
```

Esto representa cuánto ha tardado nuestra operación completa de comprobación.

No debemos confundirlo necesariamente con el tiempo ICMP que muestra el propio comando `ping`.

---

### 93. Devolver estado y duración

Podemos hacer que:

```python
comprobar_ping()
```

devuelva:

```python
{
    "estado": "ACCESIBLE",
    "duracion": 0.04
}
```

Esto será más útil para los informes.

---

### 94. Nueva versión de `comprobar_ping()`

```python
def comprobar_ping(
    host,
    timeout=3
):

    inicio = time.perf_counter()

    try:

        resultado = subprocess.run(
            [
                "ping",
                "-n",
                "1",
                host
            ],
            capture_output=True,
            text=True,
            timeout=timeout
        )

    except subprocess.TimeoutExpired:

        estado = "TIMEOUT"

    except OSError:

        estado = "ERROR"

    else:

        if resultado.returncode == 0:

            estado = "ACCESIBLE"

        else:

            estado = "NO_ACCESIBLE"

    fin = time.perf_counter()

    duracion = (
        fin - inicio
    )

    return {
        "estado": estado,
        "duracion": duracion
    }
```

---

### 95. Adaptar `diagnosticar_equipo()`

Ahora:

```python
ping = comprobar_ping(
    equipo["host"]
)
```

devolverá un diccionario.

Podemos guardar:

```python
resultado = {
    "nombre": equipo["nombre"],
    "host": equipo["host"],
    "ping": ping,
    "puertos": []
}
```

---

### 96. Nueva estructura de resultados

Tendremos:

```python
{
    "nombre": "Router",
    "host": "192.168.1.1",
    "ping": {
        "estado": "ACCESIBLE",
        "duracion": 0.032
    },
    "puertos": []
}
```

Esta estructura jerárquica será especialmente adecuada cuando generemos:

```text
JSON
```

más adelante.

---

### 97. Mostrar el nuevo resultado

Debemos modificar:

```python
mostrar_resultados()
```

para utilizar:

```python
resultado["ping"]["estado"]
```

y:

```python
resultado["ping"]["duracion"]
```

Por ejemplo:

```python
def mostrar_resultados(
    resultados
):

    for resultado in resultados:

        print(
            "\n"
            "===================="
        )

        print(
            f"Equipo: "
            f"{resultado['nombre']}"
        )

        print(
            f"Host: "
            f"{resultado['host']}"
        )

        print(
            f"Ping: "
            f"{resultado['ping']['estado']}"
        )

        print(
            "Duración: "
            f"{resultado['ping']['duracion']:.3f} s"
        )
```

---

### 98. Ejemplo de salida

Podemos obtener:

```text
====================
Equipo: Router
Host: 192.168.1.1
Ping: ACCESIBLE
Duración: 0.021 s

====================
Equipo: ServidorWeb
Host: 192.168.1.10
Ping: NO_ACCESIBLE
Duración: 0.987 s
```

Los valores serán diferentes en cada ejecución.

---

### 99. Una precisión importante sobre la duración

La duración que estamos midiendo incluye:

```text
lanzar el proceso ping
+
ejecutar el comando
+
esperar el resultado
+
finalizar el proceso
```

Por tanto:

```text
duracion
```

no representa necesariamente:

```text
latencia exacta de red
```

Es el tiempo empleado por nuestra comprobación.

!!! note "Duración"

    Si necesitáramos medir con precisión la latencia ICMP tendríamos que analizar específicamente los datos proporcionados por la herramienta o utilizar otro mecanismo.

    En este proyecto utilizamos la duración únicamente como información complementaria.

---

### 100. Problema de nombres inexistentes

Nuestro CSV también puede contener nombres:

```csv
ServidorPrueba,servidor-prueba.local,80
```

Si el nombre no puede resolverse, `ping` fallará.

Desde la perspectiva actual obtendremos probablemente:

```text
NO_ACCESIBLE
```

Pero existen diferentes causas posibles:

```text
DNS
red
firewall
host apagado
```

Más adelante utilizaremos:

```python
socket
```

para realizar una comprobación explícita de resolución de nombres.

---

### 101. No detener el diagnóstico tras un ping fallido

Podríamos pensar:

```text
si ping falla
no comprobar puertos
```

Pero esto sería una mala decisión para nuestro proyecto.

Como hemos visto:

```text
PING NO RESPONDE
```

no significa necesariamente:

```text
TCP NO DISPONIBLE
```

Por tanto, posteriormente haremos:

```text
PING
 │
 ├── responde
 │
 └── no responde
       │
       ▼
en ambos casos
       │
       ▼
comprobar TCP
```

Las pruebas serán independientes.

---

### 102. Añadir un equipo seguro para pruebas locales

Para disponer de una prueba sencilla podemos añadir temporalmente:

```csv
Localhost,127.0.0.1,80;443
```

El ping a:

```text
127.0.0.1
```

debería funcionar en una configuración normal.

Sin embargo, eso no significa que:

```text
80
443
```

estén abiertos.

Esto será muy útil en la siguiente fase.

Podremos comprobar la diferencia entre:

```text
host accesible
```

y:

```text
servicio TCP accesible
```

---

### 103. Ping y puertos son pruebas diferentes

Por ejemplo:

```text
127.0.0.1

PING
 │
 └── ACCESIBLE

PUERTO 80
 │
 └── puede estar cerrado

PUERTO 443
 │
 └── puede estar cerrado
```

Esto demuestra que:

```text
conectividad
```

y:

```text
disponibilidad de servicios
```

no son exactamente lo mismo.

---

### 104. Probar con un nombre de dominio

Podemos añadir temporalmente:

```csv
Ejemplo,example.com,80;443
```

El sistema intentará resolver:

```text
example.com
```

antes de realizar el ping.

El resultado puede variar según:

```text
conectividad
DNS
configuración de red
políticas del servidor
```

No debemos utilizar un resultado concreto como garantía de funcionamiento.

---

### 105. Depurar `comprobar_ping()`

Coloca un breakpoint en:

```python
resultado = subprocess.run(
```

Ejecuta con:

```text
F5
```

Observa:

```text
host
timeout
```

Después utiliza:

```text
F10
```

para ejecutar el comando.

Observa:

```python
resultado.returncode
```

en:

```text
Variables
```

---

### 106. Utilizar Watch

Añade:

```python
host
```

```python
resultado.returncode
```

```python
resultado.stdout
```

Cuando estas variables estén disponibles podrás observar su contenido.

También puedes añadir:

```python
resultado.returncode == 0
```

para comprobar directamente la condición.

---

### 107. Utilizar Debug Console

Con el programa detenido después de ejecutar el ping prueba:

```python
resultado.returncode
```

Después:

```python
resultado.stdout
```

Y:

```python
resultado.returncode == 0
```

Así aplicamos directamente las técnicas de depuración estudiadas en el capítulo anterior.

---

### 108. Breakpoint condicional por host

Si tenemos muchos equipos podemos detenernos solamente cuando:

```python
host == "192.168.1.10"
```

o:

```python
equipo["nombre"] == "ServidorWeb"
```

dependiendo de la función donde coloquemos el breakpoint.

Esto evita detenernos en cada equipo.

---

### 109. Comprobar Call Stack

Si nos detenemos dentro de:

```python
comprobar_ping()
```

podemos observar una pila similar a:

```text
comprobar_ping()
       │
       ▼
diagnosticar_equipo()
       │
       ▼
diagnosticar_red()
       │
       ▼
programa principal
```

Ahora las herramientas del depurador nos permiten comprender claramente la arquitectura que estamos construyendo.

---

### 110. Crear una prueba con timeout

Para observar el comportamiento podemos reducir temporalmente:

```python
timeout=3
```

a:

```python
timeout=1
```

y utilizar un host de nuestra red de prácticas que sepamos que no responde.

El resultado podrá ser:

```text
TIMEOUT
```

o:

```text
NO_ACCESIBLE
```

dependiendo de cómo responda el sistema y de cuánto tarde el comando.

No debemos asumir que todos los fallos producirán:

```text
TIMEOUT
```

---

### 111. Diferenciar los estados

Nuestro programa maneja:

```text
ACCESIBLE
```

El comando `ping` terminó satisfactoriamente.

```text
NO_ACCESIBLE
```

El comando terminó, pero su código de retorno no fue cero.

```text
TIMEOUT
```

Nuestro límite de tiempo para el proceso se agotó.

```text
ERROR
```

No fue posible ejecutar correctamente la comprobación.

Esta distinción será útil en los informes.

---

### 112. Preparar la versión completa de esta fase

Las nuevas importaciones serán:

```python
import csv
import subprocess
import time

from pathlib import Path
```

Conservaremos todas las funciones de la primera fase y añadiremos:

```text
comprobar_ping()
diagnosticar_equipo()
diagnosticar_red()
mostrar_resultados()
```

---

### 113. Programa completo hasta este punto

El archivo:

```text
administrador_red.py
```

puede quedar así:

```python
import csv
import subprocess
import time

from pathlib import Path


DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)


DIRECTORIO_CAPITULO = (
    DIRECTORIO_PROGRAMA.parent
)


ARCHIVO_INVENTARIO = (
    DIRECTORIO_CAPITULO
    / "datos"
    / "equipos.csv"
)


def convertir_puertos(
    texto
):

    puertos = []

    for puerto in texto.split(";"):

        puerto = puerto.strip()

        if not puerto:

            continue

        try:

            numero = int(
                puerto
            )

        except ValueError:

            return None

        puertos.append(
            numero
        )

    return puertos


def cargar_inventario(
    archivo
):

    equipos = []

    with archivo.open(
        "r",
        encoding="utf-8",
        newline=""
    ) as fichero:

        lector = csv.DictReader(
            fichero
        )

        columnas_necesarias = {
            "nombre",
            "host",
            "puertos"
        }

        columnas_disponibles = set(
            lector.fieldnames or []
        )

        if not columnas_necesarias.issubset(
            columnas_disponibles
        ):

            raise ValueError(
                "El CSV no contiene "
                "las columnas necesarias."
            )

        for fila in lector:

            nombre = (
                fila["nombre"].strip()
            )

            host = (
                fila["host"].strip()
            )

            puertos = convertir_puertos(
                fila["puertos"]
            )

            if puertos is None:

                print(
                    "Puertos incorrectos:",
                    nombre
                )

                continue

            equipo = {
                "nombre": nombre,
                "host": host,
                "puertos": puertos
            }

            equipos.append(
                equipo
            )

    return equipos


def validar_equipo(
    equipo
):

    if not equipo["nombre"]:

        return False

    if not equipo["host"]:

        return False

    if not equipo["puertos"]:

        return False

    for puerto in equipo["puertos"]:

        if (
            puerto < 1
            or puerto > 65535
        ):

            return False

    return True


def obtener_equipos_validos(
    equipos
):

    validos = []

    for equipo in equipos:

        if validar_equipo(
            equipo
        ):

            validos.append(
                equipo
            )

        else:

            print(
                "Equipo incorrecto:",
                equipo["nombre"]
            )

    return validos


def comprobar_ping(
    host,
    timeout=3
):

    inicio = time.perf_counter()

    try:

        resultado = subprocess.run(
            [
                "ping",
                "-n",
                "1",
                host
            ],
            capture_output=True,
            text=True,
            timeout=timeout
        )

    except subprocess.TimeoutExpired:

        estado = "TIMEOUT"

    except OSError:

        estado = "ERROR"

    else:

        if resultado.returncode == 0:

            estado = "ACCESIBLE"

        else:

            estado = "NO_ACCESIBLE"

    fin = time.perf_counter()

    duracion = (
        fin - inicio
    )

    return {
        "estado": estado,
        "duracion": duracion
    }


def diagnosticar_equipo(
    equipo
):

    ping = comprobar_ping(
        equipo["host"]
    )

    resultado = {
        "nombre": equipo["nombre"],
        "host": equipo["host"],
        "ping": ping,
        "puertos": []
    }

    return resultado


def diagnosticar_red(
    equipos
):

    resultados = []

    for equipo in equipos:

        resultado = diagnosticar_equipo(
            equipo
        )

        resultados.append(
            resultado
        )

    return resultados


def mostrar_resultados(
    resultados
):

    for resultado in resultados:

        print(
            "\n"
            "===================="
        )

        print(
            f"Equipo: "
            f"{resultado['nombre']}"
        )

        print(
            f"Host: "
            f"{resultado['host']}"
        )

        print(
            f"Ping: "
            f"{resultado['ping']['estado']}"
        )

        print(
            "Duración: "
            f"{resultado['ping']['duracion']:.3f} s"
        )


try:

    equipos = cargar_inventario(
        ARCHIVO_INVENTARIO
    )

except FileNotFoundError:

    print(
        "No se encuentra "
        "el inventario."
    )

    raise SystemExit(1)

except ValueError as error:

    print(
        f"Inventario incorrecto: "
        f"{error}"
    )

    raise SystemExit(1)

except OSError as error:

    print(
        "Error leyendo "
        f"el inventario: {error}"
    )

    raise SystemExit(1)


equipos_validos = (
    obtener_equipos_validos(
        equipos
    )
)


resultados = diagnosticar_red(
    equipos_validos
)


mostrar_resultados(
    resultados
)
```

---

### 114. Inventario recomendado para probar esta fase

Podemos utilizar inicialmente:

```csv
nombre,host,puertos
Localhost,127.0.0.1,80;443
Router,192.168.1.1,80;443
ServidorWeb,192.168.1.10,80;443
ServidorSSH,192.168.1.20,22
NAS,192.168.1.30,445
```

Adapta las direcciones:

```text
192.168.1.x
```

a la red real del laboratorio.

---

### 115. Práctica guiada

Realiza las siguientes pruebas.

Primero ejecuta:

```powershell
python administrador_red.py
```

Comprueba que:

```text
Localhost
```

responde correctamente.

Después comprueba los equipos reales disponibles en el laboratorio.

Anota para cada uno:

```text
nombre
host
estado ping
duración
```

---

### 116. Práctica de análisis

Selecciona un equipo que:

```text
responda al ping
```

y otro que:

```text
no responda
```

Utiliza el depurador para comparar:

```python
resultado.returncode
```

en ambos casos.

Observa también:

```python
resultado.stdout
```

pero recuerda que nuestro programa no depende del texto mostrado por el comando.

---

### 117. Práctica de depuración

Coloca un breakpoint dentro de:

```python
diagnosticar_equipo()
```

Añade a Watch:

```python
equipo["nombre"]
```

```python
equipo["host"]
```

```python
ping
```

Utiliza:

```text
F11
```

para entrar en:

```python
comprobar_ping()
```

Después utiliza:

```text
F10
```

para seguir su ejecución.

Finalmente utiliza:

```text
Shift + F11
```

para regresar.

---

### 118. Reto

Añade al inventario:

```csv
EquipoInexistente,192.168.1.250,80
```

si esa dirección está libre en la red de prácticas.

Ejecuta el diagnóstico.

Investiga mediante el depurador:

```text
qué estado obtiene
```

```text
cuánto tarda
```

```text
qué returncode devuelve ping
```

No presupongas que el resultado será necesariamente:

```text
TIMEOUT
```

porque dependerá del comportamiento del sistema y de la red.

---

### 119. Estado del proyecto

Ahora hemos completado:

```text
[✓] estructura del proyecto

[✓] inventario CSV

[✓] lectura del inventario

[✓] conversión de puertos

[✓] validación

[✓] control básico de errores

[✓] diagnóstico mediante ping

[✓] timeout

[✓] medición de duración

[✓] estructura de resultados
```

Todavía falta:

```text
[ ] argumentos de ejecución

[ ] resolución DNS explícita

[ ] comprobación de puertos TCP

[ ] informe TXT

[ ] informe JSON

[ ] logging completo

[ ] integración final
```

---

### 120. Resumen de esta segunda fase

En esta parte hemos incorporado:

```python
subprocess
```

al proyecto final.

Nuestra aplicación ya puede ejecutar:

```text
ping
```

sobre cada host del inventario.

Hemos aprendido a interpretar:

```python
resultado.returncode
```

y hemos añadido:

```python
timeout
```

para limitar el tiempo de ejecución.

También hemos creado los estados:

```text
ACCESIBLE
NO_ACCESIBLE
TIMEOUT
ERROR
```

y hemos medido la duración de cada comprobación mediante:

```python
time.perf_counter()
```

Nuestro diagnóstico tiene ahora esta estructura:

```text
EQUIPO
  │
  ├── nombre
  │
  ├── host
  │
  └── ping
       │
       ├── estado
       └── duración
```

Además hemos creado:

```python
diagnosticar_equipo()
```

y:

```python
diagnosticar_red()
```

que serán el núcleo sobre el que seguiremos construyendo la aplicación.

!!! success "Segunda fase completada"

    Nuestra herramienta ya realiza una comprobación real de conectividad sobre los equipos del inventario.

    Un fallo de ping no se utilizará para descartar automáticamente el equipo, porque la ausencia de respuesta ICMP no demuestra que sus servicios TCP sean inaccesibles.

En la siguiente fase incorporaremos:

```python
socket
```

y realizaremos para cada equipo:

```text
             EQUIPO
                │
       ┌────────┴────────┐
       │                 │
       ▼                 ▼
     PING              PUERTOS
       │                 │
       ▼                 ▼
   estado TCP       22 / 80 / 443...
```

Comprobaremos **solamente los puertos indicados en `equipos.csv`**, construiremos un resultado individual para cada puerto y combinaremos estas comprobaciones con el estado de `ping`. Después tendremos ya preparada la información necesaria para generar los informes TXT y JSON.

---

## 121. Tercera fase: resolución DNS y comprobación de puertos TCP

Nuestra aplicación ya puede realizar:

```text
equipos.csv
     │
     ▼
cargar inventario
     │
     ▼
validar equipos
     │
     ▼
realizar ping
     │
     ▼
guardar resultado
```

Ahora incorporaremos una segunda forma de comprobar la conectividad.

Utilizaremos:

```python
socket
```

para:

```text
resolver nombres
```

y:

```text
comprobar conexiones TCP
```

El nuevo diagnóstico será:

```text
                  EQUIPO
                     │
          ┌──────────┼──────────┐
          │          │          │
          ▼          ▼          ▼
        PING        DNS       PUERTOS
          │          │          │
          ▼          ▼          ▼
       estado        IP       TCP
```

De esta forma no dependeremos exclusivamente del resultado de `ping`.

!!! warning "Uso autorizado"

    Las comprobaciones de puertos deben realizarse únicamente sobre equipos propios, sistemas del laboratorio o redes donde tengamos autorización.

    Nuestro programa comprobará exclusivamente los puertos indicados explícitamente en `equipos.csv`.

---

### 122. Importar `socket`

Añade al principio de:

```text
administrador_red.py
```

la importación:

```python
import socket
```

Las importaciones serán ahora:

```python
import csv
import socket
import subprocess
import time

from pathlib import Path
```

---

### 123. ¿Qué utilizaremos de `socket`?

En esta fase utilizaremos principalmente:

```python
socket.gethostbyname()
```

para resolver un nombre.

Y:

```python
socket.socket()
```

junto con:

```python
connect_ex()
```

para intentar establecer una conexión TCP.

El flujo será:

```text
host
 │
 ▼
resolver
 │
 ▼
dirección IP
 │
 ▼
puerto
 │
 ▼
conexión TCP
 │
 ├── accesible
 │
 └── no accesible
```

---

### 124. Primera prueba de resolución

Podemos probar temporalmente:

```python
ip = socket.gethostbyname(
    "localhost"
)


print(
    ip
)
```

Obtendremos normalmente:

```text
127.0.0.1
```

También podemos probar un nombre que pueda resolverse desde nuestra red.

---

### 125. Resolver una dirección IP

Si utilizamos directamente:

```python
socket.gethostbyname(
    "192.168.1.1"
)
```

obtendremos normalmente la misma dirección:

```text
192.168.1.1
```

Por tanto, nuestra función podrá trabajar tanto con:

```text
nombres
```

como con:

```text
direcciones IPv4
```

---

### 126. Crear `resolver_host()`

Añade:

```python
def resolver_host(
    host
):

    try:

        ip = socket.gethostbyname(
            host
        )

    except socket.gaierror:

        return None

    return ip
```

La función devolverá:

```text
dirección IP
```

si puede resolver el host.

Si no puede hacerlo devolverá:

```python
None
```

---

### 127. Probar `resolver_host()`

Podemos probar:

```python
print(
    resolver_host(
        "localhost"
    )
)
```

Resultado esperado:

```text
127.0.0.1
```

También podemos probar un nombre inexistente:

```python
print(
    resolver_host(
        "equipo-que-no-existe.local"
    )
)
```

En ese caso podremos obtener:

```text
None
```

---

### 128. ¿Qué significa un error de resolución?

Si:

```python
resolver_host()
```

devuelve:

```python
None
```

sabemos que nuestra llamada de resolución no ha conseguido obtener una dirección IP para ese host.

Esto puede deberse a diferentes causas:

```text
nombre incorrecto
```

```text
registro DNS inexistente
```

```text
problema de resolución
```

```text
configuración de red
```

No debemos afirmar automáticamente cuál es la causa concreta.

---

### 129. Guardar el resultado DNS

Modificaremos:

```python
diagnosticar_equipo()
```

para obtener:

```python
ip = resolver_host(
    equipo["host"]
)
```

Nuestro resultado podrá contener:

```python
{
    "nombre": equipo["nombre"],
    "host": equipo["host"],
    "ip": ip,
    "ping": ping,
    "puertos": []
}
```

---

### 130. Ejemplo de resultado

Para:

```text
localhost
```

podríamos obtener:

```python
{
    "nombre": "Localhost",
    "host": "localhost",
    "ip": "127.0.0.1",
    "ping": {
        "estado": "ACCESIBLE",
        "duracion": 0.021
    },
    "puertos": []
}
```

Ya tenemos dos comprobaciones:

```text
PING
```

y:

```text
RESOLUCIÓN
```

---

### 131. ¿Qué es una conexión TCP?

Un servicio de red puede escuchar en un determinado puerto.

Por ejemplo:

```text
SSH
 │
 └── habitualmente 22


HTTP
 │
 └── habitualmente 80


HTTPS
 │
 └── habitualmente 443
```

Nuestro programa intentará establecer una conexión TCP con los puertos especificados en el inventario.

Por ejemplo:

```csv
ServidorWeb,192.168.1.10,80;443
```

significa que comprobaremos:

```text
192.168.1.10:80
```

y:

```text
192.168.1.10:443
```

---

### 132. No estamos realizando un escaneo general

Existe una diferencia importante.

Nuestro programa no probará:

```text
todos los puertos
```

de un equipo.

Solamente comprobará:

```text
los puertos declarados
en equipos.csv
```

Por ejemplo:

```csv
ServidorSSH,192.168.1.20,22
```

producirá una única comprobación:

```text
192.168.1.20:22
```

Esto mantiene el proyecto centrado en la verificación de servicios conocidos de nuestro inventario.

---

### 133. Crear un socket TCP

Podemos crear:

```python
sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
```

Donde:

```python
socket.AF_INET
```

indica que utilizaremos:

```text
IPv4
```

y:

```python
socket.SOCK_STREAM
```

indica:

```text
TCP
```

---

### 134. Establecer un timeout

No queremos esperar indefinidamente.

Podemos utilizar:

```python
sock.settimeout(
    1
)
```

Esto establece un tiempo máximo para determinadas operaciones del socket.

En nuestro proyecto utilizaremos inicialmente:

```text
1 segundo
```

por puerto.

---

### 135. Utilizar `connect_ex()`

Podemos intentar la conexión:

```python
codigo = sock.connect_ex(
    (
        host,
        puerto
    )
)
```

`connect_ex()` devuelve un código numérico.

Cuando la conexión se establece correctamente:

```text
0
```

indica éxito.

Por tanto:

```python
codigo == 0
```

significa que hemos podido establecer una conexión TCP.

---

### 136. Primera función TCP

Podemos crear:

```python
def comprobar_puerto(
    host,
    puerto,
    timeout=1
):

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.settimeout(
        timeout
    )

    try:

        codigo = sock.connect_ex(
            (
                host,
                puerto
            )
        )

    finally:

        sock.close()

    return (
        codigo == 0
    )
```

La función devuelve:

```python
True
```

si puede establecer la conexión.

Y:

```python
False
```

si no puede hacerlo.

---

### 137. Utilizar `with`

Podemos escribir una versión más limpia utilizando:

```python
with socket.socket(...) as sock:
```

Cuando termina el bloque:

```text
with
```

el socket se cierra automáticamente.

La función puede quedar:

```python
def comprobar_puerto(
    host,
    puerto,
    timeout=1
):

    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    ) as sock:

        sock.settimeout(
            timeout
        )

        codigo = sock.connect_ex(
            (
                host,
                puerto
            )
        )

    return (
        codigo == 0
    )
```

---

### 138. Probar con nuestro propio equipo

Podemos probar:

```python
print(
    comprobar_puerto(
        "127.0.0.1",
        80
    )
)
```

El resultado puede ser:

```text
True
```

o:

```text
False
```

dependiendo de si existe un servicio escuchando en el puerto:

```text
80
```

de nuestro ordenador.

---

### 139. Un resultado `False` no significa que el equipo esté apagado

Supongamos:

```text
127.0.0.1
```

responde al ping.

Pero:

```text
127.0.0.1:80
```

no tiene ningún servidor web.

Podríamos obtener:

```text
PING
ACCESIBLE

TCP 80
NO_ACCESIBLE
```

Esto es perfectamente normal.

El host existe, pero no hemos podido establecer una conexión TCP con ese puerto.

---

### 140. Estados más descriptivos

Igual que hicimos con `ping`, es preferible devolver un resultado descriptivo.

Queremos obtener algo como:

```python
{
    "puerto": 80,
    "estado": "ACCESIBLE"
}
```

en lugar de simplemente:

```python
True
```

---

### 141. Mejorar `comprobar_puerto()`

Podemos escribir:

```python
def comprobar_puerto(
    host,
    puerto,
    timeout=1
):

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as sock:

            sock.settimeout(
                timeout
            )

            codigo = sock.connect_ex(
                (
                    host,
                    puerto
                )
            )

    except OSError:

        return {
            "puerto": puerto,
            "estado": "ERROR"
        }

    if codigo == 0:

        estado = "ACCESIBLE"

    else:

        estado = "NO_ACCESIBLE"

    return {
        "puerto": puerto,
        "estado": estado
    }
```

---

### 142. ¿Por qué capturamos `OSError`?

Durante una operación de red pueden producirse errores relacionados con:

```text
socket
sistema operativo
dirección
conectividad
```

No queremos que un único problema termine todo el diagnóstico.

Por tanto:

```python
except OSError:
```

nos permite devolver:

```text
ERROR
```

y continuar con el resto de equipos.

---

### 143. Utilizar una IP ya resuelta

Tenemos:

```python
ip = resolver_host(
    equipo["host"]
)
```

Si obtenemos una IP, podemos utilizarla directamente para las comprobaciones TCP.

Por ejemplo:

```python
comprobar_puerto(
    ip,
    443
)
```

Esto evita repetir innecesariamente la resolución del mismo nombre para cada puerto.

---

### 144. ¿Qué ocurre si no podemos resolver el host?

Si:

```python
ip is None
```

no tenemos una dirección IPv4 con la que realizar las comprobaciones de esta versión.

Podemos generar resultados:

```text
NO_RESUELTO
```

para sus puertos.

Por ejemplo:

```python
{
    "puerto": 80,
    "estado": "NO_RESUELTO"
}
```

---

### 145. Crear `comprobar_puertos()`

Necesitamos comprobar todos los puertos indicados para un equipo.

Crearemos:

```python
def comprobar_puertos(
    host,
    puertos,
    timeout=1
):

    resultados = []

    for puerto in puertos:

        resultado = comprobar_puerto(
            host,
            puerto,
            timeout
        )

        resultados.append(
            resultado
        )

    return resultados
```

---

### 146. Ejemplo de funcionamiento

Si tenemos:

```python
puertos = [
    80,
    443
]
```

podemos obtener:

```python
[
    {
        "puerto": 80,
        "estado": "ACCESIBLE"
    },
    {
        "puerto": 443,
        "estado": "NO_ACCESIBLE"
    }
]
```

Ahora cada puerto tiene su propio resultado.

---

### 147. Incorporar duración a la comprobación TCP

También podemos medir cuánto tarda cada comprobación.

Utilizaremos:

```python
inicio = time.perf_counter()
```

antes de conectar.

Y:

```python
fin = time.perf_counter()
```

al finalizar.

Después:

```python
duracion = (
    fin - inicio
)
```

---

### 148. Nueva versión de `comprobar_puerto()`

Podemos utilizar:

```python
def comprobar_puerto(
    host,
    puerto,
    timeout=1
):

    inicio = time.perf_counter()

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as sock:

            sock.settimeout(
                timeout
            )

            codigo = sock.connect_ex(
                (
                    host,
                    puerto
                )
            )

    except OSError:

        estado = "ERROR"

    else:

        if codigo == 0:

            estado = "ACCESIBLE"

        else:

            estado = "NO_ACCESIBLE"

    fin = time.perf_counter()

    duracion = (
        fin - inicio
    )

    return {
        "puerto": puerto,
        "estado": estado,
        "duracion": duracion
    }
```

---

### 149. Resultado de un puerto

Ahora podemos obtener:

```python
{
    "puerto": 443,
    "estado": "ACCESIBLE",
    "duracion": 0.018
}
```

Esto encaja bien con la estructura utilizada para:

```text
ping
```

---

### 150. Modificar `diagnosticar_equipo()`

Vamos a integrar:

```text
ping
DNS
TCP
```

Nuestra función puede quedar:

```python
def diagnosticar_equipo(
    equipo
):

    ping = comprobar_ping(
        equipo["host"]
    )

    ip = resolver_host(
        equipo["host"]
    )

    if ip is None:

        puertos = []

        for puerto in equipo["puertos"]:

            puertos.append(
                {
                    "puerto": puerto,
                    "estado": "NO_RESUELTO",
                    "duracion": 0
                }
            )

    else:

        puertos = comprobar_puertos(
            ip,
            equipo["puertos"]
        )

    resultado = {
        "nombre": equipo["nombre"],
        "host": equipo["host"],
        "ip": ip,
        "ping": ping,
        "puertos": puertos
    }

    return resultado
```

---

### 151. Flujo completo de un equipo

Ahora:

```python
diagnosticar_equipo()
```

realiza:

```text
              EQUIPO
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
      PING          RESOLVER HOST
                          │
                   ┌──────┴──────┐
                   │             │
                   ▼             ▼
                  IP           ERROR
                   │             │
                   ▼             ▼
             comprobar TCP   NO_RESUELTO
```

---

### 152. Ping y DNS son independientes

Observa que ejecutamos:

```python
comprobar_ping(
    equipo["host"]
)
```

y después:

```python
resolver_host(
    equipo["host"]
)
```

Son comprobaciones distintas.

Aunque `ping` falle, continuamos intentando resolver el host.

Y aunque `ping` no responda, si obtenemos una IP:

```text
continuaremos comprobando TCP
```

---

### 153. Ejemplo de resultado completo

Podemos obtener:

```python
{
    "nombre": "ServidorWeb",
    "host": "192.168.1.10",
    "ip": "192.168.1.10",
    "ping": {
        "estado": "ACCESIBLE",
        "duracion": 0.021
    },
    "puertos": [
        {
            "puerto": 80,
            "estado": "ACCESIBLE",
            "duracion": 0.014
        },
        {
            "puerto": 443,
            "estado": "NO_ACCESIBLE",
            "duracion": 1.002
        }
    ]
}
```

Esta estructura contiene ya prácticamente toda la información necesaria para nuestros informes.

---

### 154. Actualizar `mostrar_resultados()`

Vamos a mostrar también:

```text
IP
```

y:

```text
puertos
```

Podemos utilizar:

```python
def mostrar_resultados(
    resultados
):

    for resultado in resultados:

        print(
            "\n"
            "===================="
        )

        print(
            f"Equipo: "
            f"{resultado['nombre']}"
        )

        print(
            f"Host: "
            f"{resultado['host']}"
        )

        print(
            f"IP: "
            f"{resultado['ip']}"
        )

        print(
            f"Ping: "
            f"{resultado['ping']['estado']}"
        )

        print(
            "Duración ping: "
            f"{resultado['ping']['duracion']:.3f} s"
        )

        print(
            "Puertos:"
        )

        for puerto in resultado["puertos"]:

            print(
                "  "
                f"{puerto['puerto']}: "
                f"{puerto['estado']} "
                f"({puerto['duracion']:.3f} s)"
            )
```

---

### 155. Ejemplo de salida

Podemos obtener:

```text
====================
Equipo: Localhost
Host: 127.0.0.1
IP: 127.0.0.1
Ping: ACCESIBLE
Duración ping: 0.018 s
Puertos:
  80: NO_ACCESIBLE (0.001 s)
  443: NO_ACCESIBLE (0.001 s)

====================
Equipo: ServidorWeb
Host: 192.168.1.10
IP: 192.168.1.10
Ping: ACCESIBLE
Duración ping: 0.024 s
Puertos:
  80: ACCESIBLE (0.003 s)
  443: ACCESIBLE (0.004 s)
```

Los resultados reales dependerán de la red y de los servicios disponibles.

---

### 156. Mostrar correctamente un host no resuelto

Si:

```python
resultado["ip"]
```

es:

```python
None
```

podemos mostrar:

```text
NO_RESUELTO
```

Por ejemplo:

```python
ip_mostrar = (
    resultado["ip"]
    if resultado["ip"] is not None
    else "NO_RESUELTO"
)
```

Después:

```python
print(
    f"IP: {ip_mostrar}"
)
```

---

### 157. Mejorar `mostrar_resultados()`

La función puede quedar:

```python
def mostrar_resultados(
    resultados
):

    for resultado in resultados:

        ip_mostrar = (
            resultado["ip"]
            if resultado["ip"] is not None
            else "NO_RESUELTO"
        )

        print(
            "\n"
            "===================="
        )

        print(
            f"Equipo: "
            f"{resultado['nombre']}"
        )

        print(
            f"Host: "
            f"{resultado['host']}"
        )

        print(
            f"IP: "
            f"{ip_mostrar}"
        )

        print(
            f"Ping: "
            f"{resultado['ping']['estado']}"
        )

        print(
            "Duración ping: "
            f"{resultado['ping']['duracion']:.3f} s"
        )

        print(
            "Puertos:"
        )

        for puerto in resultado["puertos"]:

            print(
                "  "
                f"{puerto['puerto']}: "
                f"{puerto['estado']} "
                f"({puerto['duracion']:.3f} s)"
            )
```

---

### 158. Prueba con `localhost`

Para realizar una primera prueba podemos utilizar:

```csv
nombre,host,puertos
Localhost,127.0.0.1,80;443
```

Sabemos que:

```text
127.0.0.1
```

corresponde al propio equipo.

El ping debería responder en una configuración normal.

Sin embargo, los puertos:

```text
80
443
```

solamente aparecerán como accesibles si tenemos servicios escuchando en ellos.

---

### 159. Crear temporalmente un servicio HTTP

Para realizar una prueba controlada podemos utilizar el servidor HTTP incluido en Python.

Desde otro terminal de VS Code ejecuta:

```powershell
python -m http.server 8000
```

El servidor quedará escuchando normalmente en:

```text
puerto 8000
```

Mantén ese terminal abierto.

---

### 160. Modificar el inventario

Utiliza:

```csv
nombre,host,puertos
ServidorLocal,127.0.0.1,8000;8001
```

Tenemos:

```text
8000
```

donde hemos iniciado un servidor.

Y:

```text
8001
```

donde, si no existe otro servicio, no debería haber ningún servidor escuchando.

---

### 161. Ejecutar el diagnóstico

Desde otro terminal ejecuta:

```powershell
python administrador_red.py
```

Deberíamos obtener un resultado similar a:

```text
ServidorLocal

Ping:
ACCESIBLE

Puerto 8000:
ACCESIBLE

Puerto 8001:
NO_ACCESIBLE
```

Esta es una prueba muy útil porque controlamos nosotros mismos el servicio.

---

### 162. Detener el servidor HTTP

Cuando terminemos la prueba vuelve al terminal donde ejecutaste:

```powershell
python -m http.server 8000
```

Pulsa:

```text
Ctrl + C
```

para detenerlo.

Vuelve a ejecutar:

```powershell
python administrador_red.py
```

Ahora el puerto:

```text
8000
```

debería dejar de aparecer como accesible.

---

### 163. Relación entre servicio y puerto

Esta prueba demuestra:

```text
SERVIDOR HTTP ACTIVO
        │
        ▼
puerto 8000
        │
        ▼
ACCESIBLE
```

Después:

```text
SERVIDOR HTTP DETENIDO
        │
        ▼
puerto 8000
        │
        ▼
NO_ACCESIBLE
```

Nuestra aplicación está comprobando realmente la posibilidad de establecer una conexión TCP.

---

### 164. Añadir nombre del servicio

Python dispone de:

```python
socket.getservbyport()
```

que puede identificar algunos servicios asociados convencionalmente a determinados puertos.

Por ejemplo:

```python
socket.getservbyport(
    80,
    "tcp"
)
```

puede devolver:

```text
http
```

---

### 165. Crear `obtener_servicio()`

Podemos añadir:

```python
def obtener_servicio(
    puerto
):

    try:

        return socket.getservbyport(
            puerto,
            "tcp"
        )

    except OSError:

        return "desconocido"
```

Esto es información complementaria.

No significa necesariamente que el servicio real que escucha en ese puerto sea exactamente el indicado.

---

### 166. Añadir el servicio al resultado

Dentro de:

```python
comprobar_puerto()
```

podemos obtener:

```python
servicio = obtener_servicio(
    puerto
)
```

Y devolver:

```python
return {
    "puerto": puerto,
    "servicio": servicio,
    "estado": estado,
    "duracion": duracion
}
```

---

### 167. Importante: puerto no equivale a servicio

Si:

```text
puerto 80
```

aparece asociado a:

```text
http
```

esto indica una asociación convencional.

No demuestra que el programa que realmente escucha en ese puerto sea necesariamente un servidor HTTP.

Un administrador puede configurar otros programas en puertos diferentes.

Por tanto:

```text
puerto
```

y:

```text
servicio real
```

no deben confundirse.

---

### 168. Adaptar los resultados no resueltos

Cuando no podamos resolver el host podemos crear:

```python
{
    "puerto": puerto,
    "servicio": obtener_servicio(
        puerto
    ),
    "estado": "NO_RESUELTO",
    "duracion": 0
}
```

Así todos los resultados de puertos tendrán la misma estructura.

---

### 169. Versión definitiva de `comprobar_puerto()`

```python
def comprobar_puerto(
    host,
    puerto,
    timeout=1
):

    inicio = time.perf_counter()

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as sock:

            sock.settimeout(
                timeout
            )

            codigo = sock.connect_ex(
                (
                    host,
                    puerto
                )
            )

    except OSError:

        estado = "ERROR"

    else:

        if codigo == 0:

            estado = "ACCESIBLE"

        else:

            estado = "NO_ACCESIBLE"

    fin = time.perf_counter()

    duracion = (
        fin - inicio
    )

    servicio = obtener_servicio(
        puerto
    )

    return {
        "puerto": puerto,
        "servicio": servicio,
        "estado": estado,
        "duracion": duracion
    }
```

---

### 170. Mostrar el servicio

En:

```python
mostrar_resultados()
```

podemos utilizar:

```python
for puerto in resultado["puertos"]:

    print(
        "  "
        f"{puerto['puerto']} "
        f"({puerto['servicio']}): "
        f"{puerto['estado']} "
        f"({puerto['duracion']:.3f} s)"
    )
```

Por ejemplo:

```text
80 (http): ACCESIBLE
443 (https): ACCESIBLE
22 (ssh): NO_ACCESIBLE
8000 (desconocido): ACCESIBLE
```

---

### 171. Depurar la resolución DNS

Coloca un breakpoint en:

```python
ip = socket.gethostbyname(
    host
)
```

Ejecuta mediante:

```text
F5
```

Observa:

```text
host
```

Después utiliza:

```text
F10
```

y observa:

```text
ip
```

Puedes añadir a Watch:

```python
host
```

```python
ip
```

---

### 172. Depurar una conexión TCP

Coloca un breakpoint en:

```python
codigo = sock.connect_ex(
```

Utiliza como prueba:

```text
127.0.0.1:8000
```

con el servidor HTTP activo.

Después de ejecutar la línea observa:

```python
codigo
```

Si la conexión se establece correctamente:

```text
codigo = 0
```

---

### 173. Comparar con un puerto sin servicio

Detén:

```text
python -m http.server 8000
```

y repite la prueba.

Observa nuevamente:

```python
codigo
```

Ahora debería ser distinto de:

```text
0
```

El valor exacto puede depender del sistema y de la situación.

Nuestro programa no necesita interpretar todos los códigos posibles.

Para esta práctica nos basta con:

```text
0
```

frente a:

```text
distinto de 0
```

---

### 174. Utilizar Watch durante TCP

Añade:

```python
host
```

```python
puerto
```

```python
codigo
```

```python
codigo == 0
```

Así podremos observar:

```text
host
+
puerto
+
resultado
```

en cada comprobación.

---

### 175. Breakpoint condicional por puerto

Si nuestro equipo tiene:

```python
[
    22,
    80,
    443,
    8000
]
```

podemos detenernos solamente cuando:

```python
puerto == 443
```

utilizando un breakpoint condicional.

Esto evita detenernos en todas las comprobaciones.

---

### 176. Breakpoint condicional por equipo

Dentro de:

```python
diagnosticar_equipo()
```

podemos utilizar:

```python
equipo["nombre"] == "ServidorWeb"
```

Así podemos investigar exclusivamente ese equipo.

---

### 177. Call Stack durante una comprobación TCP

Si nos detenemos dentro de:

```python
comprobar_puerto()
```

podemos encontrar una pila similar a:

```text
comprobar_puerto()
        │
        ▼
comprobar_puertos()
        │
        ▼
diagnosticar_equipo()
        │
        ▼
diagnosticar_red()
        │
        ▼
programa principal
```

Esta pila muestra claramente cómo está organizada nuestra aplicación.

---

### 178. Una arquitectura basada en funciones

Nuestro programa contiene ya funciones con responsabilidades específicas:

```text
convertir_puertos()
        │
        └── procesa datos CSV


cargar_inventario()
        │
        └── lee inventario


validar_equipo()
        │
        └── valida datos


comprobar_ping()
        │
        └── comprueba ICMP


resolver_host()
        │
        └── obtiene IPv4


obtener_servicio()
        │
        └── asociación de puerto


comprobar_puerto()
        │
        └── comprueba TCP


comprobar_puertos()
        │
        └── procesa puertos


diagnosticar_equipo()
        │
        └── integra diagnóstico


diagnosticar_red()
        │
        └── procesa inventario
```

Esto facilita:

```text
pruebas
depuración
mantenimiento
ampliación
```

---

### 179. Programa completo hasta esta fase

A continuación podemos integrar todo lo desarrollado.

```python
import csv
import socket
import subprocess
import time

from pathlib import Path


DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)


DIRECTORIO_CAPITULO = (
    DIRECTORIO_PROGRAMA.parent
)


ARCHIVO_INVENTARIO = (
    DIRECTORIO_CAPITULO
    / "datos"
    / "equipos.csv"
)


def convertir_puertos(
    texto
):

    puertos = []

    for puerto in texto.split(";"):

        puerto = puerto.strip()

        if not puerto:

            continue

        try:

            numero = int(
                puerto
            )

        except ValueError:

            return None

        puertos.append(
            numero
        )

    return puertos


def cargar_inventario(
    archivo
):

    equipos = []

    with archivo.open(
        "r",
        encoding="utf-8",
        newline=""
    ) as fichero:

        lector = csv.DictReader(
            fichero
        )

        columnas_necesarias = {
            "nombre",
            "host",
            "puertos"
        }

        columnas_disponibles = set(
            lector.fieldnames or []
        )

        if not columnas_necesarias.issubset(
            columnas_disponibles
        ):

            raise ValueError(
                "El CSV no contiene "
                "las columnas necesarias."
            )

        for fila in lector:

            nombre = (
                fila["nombre"].strip()
            )

            host = (
                fila["host"].strip()
            )

            puertos = convertir_puertos(
                fila["puertos"]
            )

            if puertos is None:

                print(
                    "Puertos incorrectos:",
                    nombre
                )

                continue

            equipo = {
                "nombre": nombre,
                "host": host,
                "puertos": puertos
            }

            equipos.append(
                equipo
            )

    return equipos


def validar_equipo(
    equipo
):

    if not equipo["nombre"]:

        return False

    if not equipo["host"]:

        return False

    if not equipo["puertos"]:

        return False

    for puerto in equipo["puertos"]:

        if (
            puerto < 1
            or puerto > 65535
        ):

            return False

    return True


def obtener_equipos_validos(
    equipos
):

    validos = []

    for equipo in equipos:

        if validar_equipo(
            equipo
        ):

            validos.append(
                equipo
            )

        else:

            print(
                "Equipo incorrecto:",
                equipo["nombre"]
            )

    return validos


def comprobar_ping(
    host,
    timeout=3
):

    inicio = time.perf_counter()

    try:

        resultado = subprocess.run(
            [
                "ping",
                "-n",
                "1",
                host
            ],
            capture_output=True,
            text=True,
            timeout=timeout
        )

    except subprocess.TimeoutExpired:

        estado = "TIMEOUT"

    except OSError:

        estado = "ERROR"

    else:

        if resultado.returncode == 0:

            estado = "ACCESIBLE"

        else:

            estado = "NO_ACCESIBLE"

    fin = time.perf_counter()

    return {
        "estado": estado,
        "duracion": (
            fin - inicio
        )
    }


def resolver_host(
    host
):

    try:

        ip = socket.gethostbyname(
            host
        )

    except socket.gaierror:

        return None

    return ip


def obtener_servicio(
    puerto
):

    try:

        return socket.getservbyport(
            puerto,
            "tcp"
        )

    except OSError:

        return "desconocido"


def comprobar_puerto(
    host,
    puerto,
    timeout=1
):

    inicio = time.perf_counter()

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as sock:

            sock.settimeout(
                timeout
            )

            codigo = sock.connect_ex(
                (
                    host,
                    puerto
                )
            )

    except OSError:

        estado = "ERROR"

    else:

        if codigo == 0:

            estado = "ACCESIBLE"

        else:

            estado = "NO_ACCESIBLE"

    fin = time.perf_counter()

    return {
        "puerto": puerto,
        "servicio": obtener_servicio(
            puerto
        ),
        "estado": estado,
        "duracion": (
            fin - inicio
        )
    }


def comprobar_puertos(
    host,
    puertos,
    timeout=1
):

    resultados = []

    for puerto in puertos:

        resultado = comprobar_puerto(
            host,
            puerto,
            timeout
        )

        resultados.append(
            resultado
        )

    return resultados


def diagnosticar_equipo(
    equipo
):

    ping = comprobar_ping(
        equipo["host"]
    )

    ip = resolver_host(
        equipo["host"]
    )

    if ip is None:

        puertos = []

        for puerto in equipo["puertos"]:

            puertos.append(
                {
                    "puerto": puerto,
                    "servicio": (
                        obtener_servicio(
                            puerto
                        )
                    ),
                    "estado": "NO_RESUELTO",
                    "duracion": 0
                }
            )

    else:

        puertos = comprobar_puertos(
            ip,
            equipo["puertos"]
        )

    return {
        "nombre": equipo["nombre"],
        "host": equipo["host"],
        "ip": ip,
        "ping": ping,
        "puertos": puertos
    }


def diagnosticar_red(
    equipos
):

    resultados = []

    for equipo in equipos:

        print(
            f"Analizando "
            f"{equipo['nombre']}..."
        )

        resultado = diagnosticar_equipo(
            equipo
        )

        resultados.append(
            resultado
        )

    return resultados


def mostrar_resultados(
    resultados
):

    for resultado in resultados:

        ip_mostrar = (
            resultado["ip"]
            if resultado["ip"] is not None
            else "NO_RESUELTO"
        )

        print(
            "\n"
            "===================="
        )

        print(
            f"Equipo: "
            f"{resultado['nombre']}"
        )

        print(
            f"Host: "
            f"{resultado['host']}"
        )

        print(
            f"IP: "
            f"{ip_mostrar}"
        )

        print(
            f"Ping: "
            f"{resultado['ping']['estado']}"
        )

        print(
            "Duración ping: "
            f"{resultado['ping']['duracion']:.3f} s"
        )

        print(
            "Puertos:"
        )

        for puerto in resultado["puertos"]:

            print(
                "  "
                f"{puerto['puerto']} "
                f"({puerto['servicio']}): "
                f"{puerto['estado']} "
                f"({puerto['duracion']:.3f} s)"
            )


try:

    equipos = cargar_inventario(
        ARCHIVO_INVENTARIO
    )

except FileNotFoundError:

    print(
        "No se encuentra "
        "el inventario."
    )

    raise SystemExit(1)

except ValueError as error:

    print(
        f"Inventario incorrecto: "
        f"{error}"
    )

    raise SystemExit(1)

except OSError as error:

    print(
        "Error leyendo "
        f"el inventario: {error}"
    )

    raise SystemExit(1)


equipos_validos = (
    obtener_equipos_validos(
        equipos
    )
)


resultados = diagnosticar_red(
    equipos_validos
)


mostrar_resultados(
    resultados
)
```

---

### 180. Prueba controlada recomendada

Para comprobar esta versión podemos utilizar:

```csv
nombre,host,puertos
ServidorLocal,127.0.0.1,8000;8001
Router,192.168.1.1,80;443
```

Adapta:

```text
192.168.1.1
```

a la dirección real del router o de otro equipo autorizado de la red de prácticas.

En un segundo terminal ejecuta:

```powershell
python -m http.server 8000
```

Después ejecuta:

```powershell
python administrador_red.py
```

La prueba nos permitirá comparar:

```text
8000
```

con un servicio activo y:

```text
8001
```

sin servicio, siempre que ningún otro programa esté utilizando ese puerto.

---

### 181. Práctica de depuración

Utiliza el depurador para seguir un equipo completo.

Coloca un breakpoint en:

```python
resultado = diagnosticar_equipo(
    equipo
)
```

Después utiliza:

```text
Step Into
```

para entrar.

Sigue:

```text
comprobar_ping()
```

Después:

```text
resolver_host()
```

Y finalmente:

```text
comprobar_puertos()
```

y:

```text
comprobar_puerto()
```

Observa Call Stack durante el proceso.

---

### 182. Práctica con Watch

Añade las siguientes expresiones cuando estén disponibles:

```python
equipo["nombre"]
```

```python
equipo["host"]
```

```python
ip
```

```python
puerto
```

```python
codigo
```

```python
codigo == 0
```

Observa cómo cambian durante el diagnóstico.

---

### 183. Práctica con breakpoint condicional

Configura un inventario con:

```text
22
80
443
8000
```

Coloca un breakpoint dentro de:

```python
comprobar_puerto()
```

y utiliza:

```python
puerto == 443
```

como condición.

Comprueba que el programa solamente se detiene al analizar ese puerto.

---

### 184. Reto: host inexistente

Añade temporalmente:

```csv
EquipoInexistente,equipo-inexistente.invalid,80;443
```

Ejecuta el programa.

Observa:

```text
IP
```

y:

```text
estado de los puertos
```

Después utiliza el depurador dentro de:

```python
resolver_host()
```

para observar qué ocurre durante la resolución.

---

### 185. Reto: ping y TCP diferentes

Busca dentro de tu red de prácticas un equipo autorizado que permita observar una situación como:

```text
PING:
NO_ACCESIBLE

TCP:
ACCESIBLE
```

si existe.

El objetivo es comprobar experimentalmente que:

```text
fallo de ping
```

no implica necesariamente:

```text
fallo TCP
```

Si no existe un equipo con esa configuración, basta con comprender conceptualmente esta diferencia.

---

### 186. Estado actual del proyecto

Ya hemos completado:

```text
[✓] estructura del proyecto

[✓] inventario CSV

[✓] lectura del inventario

[✓] validación

[✓] gestión básica de errores

[✓] ping

[✓] timeout de ping

[✓] resolución IPv4

[✓] comprobación TCP

[✓] timeout TCP

[✓] comprobación de varios puertos

[✓] identificación orientativa de servicios

[✓] estructura completa de resultados
```

Todavía falta:

```text
[ ] argumentos con argparse

[ ] informe TXT

[ ] informe JSON

[ ] logging completo

[ ] estadísticas finales

[ ] integración final

[ ] pruebas finales
```

---

### 187. Estructura actual de resultados

Nuestra estructura tiene aproximadamente esta forma:

```text
RESULTADO
│
├── nombre
│
├── host
│
├── ip
│
├── ping
│   ├── estado
│   └── duracion
│
└── puertos
    │
    ├── puerto
    ├── servicio
    ├── estado
    └── duracion
```

Esta estructura se ha diseñado pensando en el siguiente paso.

Puede convertirse directamente en:

```text
JSON
```

y también puede utilizarse para construir:

```text
TXT
```

---

### 188. Resumen de esta tercera fase

En esta fase hemos incorporado:

```python
socket
```

a nuestro proyecto.

Ahora la aplicación puede realizar tres tipos de operaciones:

```text
PING
```

```text
RESOLUCIÓN DE HOST
```

```text
CONEXIÓN TCP
```

Para cada equipo obtenemos:

```text
nombre
host
IP
estado del ping
duración del ping
estado de cada puerto
duración de cada comprobación
```

También hemos comprobado experimentalmente que:

```text
host accesible
```

no significa necesariamente:

```text
puerto accesible
```

y que:

```text
ping sin respuesta
```

no demuestra por sí solo que un servicio TCP no pueda estar disponible.

!!! success "Tercera fase completada"

    Nuestra aplicación ya realiza el núcleo del diagnóstico de red requerido por el proyecto final.

    A partir de este momento disponemos de una estructura de resultados suficientemente completa para almacenarla y procesarla.

En la siguiente fase incorporaremos:

```text
argparse
      +
informe TXT
      +
informe JSON
```

De esta forma podremos ejecutar el programa indicando el inventario desde la línea de comandos y convertir los resultados que ya tenemos en archivos permanentes:

```text
resultados/
├── informe_red.txt
└── informe_red.json
```

Después solamente nos quedará incorporar el sistema completo de `logging`, realizar las pruebas finales y cerrar el proyecto y el libro.

---

## 189. Cuarta fase: argumentos e informes TXT y JSON

Nuestra herramienta ya puede realizar el diagnóstico principal:

```text
equipos.csv
     │
     ▼
cargar inventario
     │
     ▼
validar
     │
     ▼
PING
     │
     ▼
resolver host
     │
     ▼
comprobar puertos TCP
     │
     ▼
resultados
```

Hasta ahora el archivo de inventario está definido directamente en el programa:

```python
ARCHIVO_INVENTARIO = (
    DIRECTORIO_CAPITULO
    / "datos"
    / "equipos.csv"
)
```

Esto funciona, pero limita la reutilización de la herramienta.

Queremos poder ejecutar:

```powershell
python administrador_red.py --inventario ../datos/equipos.csv
```

Además queremos almacenar los resultados en:

```text
resultados/
├── informe_red.txt
└── informe_red.json
```

El nuevo flujo será:

```text
LÍNEA DE COMANDOS
        │
        ▼
     argparse
        │
        ▼
    inventario
        │
        ▼
   diagnóstico
        │
        ▼
    resultados
        │
   ┌────┴────┐
   │         │
   ▼         ▼
  TXT       JSON
```

---

### 190. ¿Por qué utilizar argumentos?

Hasta ahora nuestro programa siempre utiliza:

```text
equipos.csv
```

Pero podríamos tener:

```text
equipos_aula.csv
equipos_taller.csv
servidores.csv
routers.csv
```

No queremos modificar el código cada vez.

Es preferible indicar el archivo al ejecutar el programa.

Por ejemplo:

```powershell
python administrador_red.py --inventario ../datos/equipos_aula.csv
```

o:

```powershell
python administrador_red.py --inventario ../datos/servidores.csv
```

---

### 191. Importar `argparse`

Añade:

```python
import argparse
```

También utilizaremos:

```python
json
```

para generar el segundo informe.

Las importaciones serán:

```python
import argparse
import csv
import json
import socket
import subprocess
import time

from pathlib import Path
```

---

### 192. Crear el analizador de argumentos

Vamos a crear:

```python
def obtener_argumentos():

    parser = argparse.ArgumentParser(
        description=(
            "Herramienta de diagnóstico "
            "básico de red"
        )
    )

    parser.add_argument(
        "--inventario",
        required=True,
        help=(
            "Archivo CSV con "
            "el inventario"
        )
    )

    return parser.parse_args()
```

Ahora nuestro programa exige:

```text
--inventario
```

---

### 193. Consultar la ayuda

Desde el directorio:

```text
practicas\capitulo8\programas
```

ejecuta:

```powershell
python administrador_red.py --help
```

Obtendremos una ayuda similar a:

```text
usage: administrador_red.py [-h] --inventario INVENTARIO

Herramienta de diagnóstico básico de red

options:
  -h, --help
  --inventario INVENTARIO
```

La presentación exacta puede variar ligeramente según la versión de Python.

---

### 194. Ejecutar indicando el inventario

Desde:

```text
practicas\capitulo8\programas
```

podemos ejecutar:

```powershell
python administrador_red.py --inventario ../datos/equipos.csv
```

El argumento:

```text
../datos/equipos.csv
```

significa:

```text
..
│
└── subir desde programas
        │
        ▼
      datos
        │
        ▼
   equipos.csv
```

---

### 195. Convertir el argumento a `Path`

`argparse` devuelve inicialmente:

```text
str
```

Podemos convertirlo:

```python
archivo_inventario = Path(
    argumentos.inventario
)
```

Así podremos seguir utilizando:

```python
archivo.open(...)
```

como hasta ahora.

---

### 196. Una solución mejor con `type=Path`

`argparse` puede realizar directamente la conversión.

Podemos definir:

```python
parser.add_argument(
    "--inventario",
    required=True,
    type=Path,
    help=(
        "Archivo CSV con "
        "el inventario"
    )
)
```

Entonces:

```python
argumentos.inventario
```

será directamente un objeto:

```text
Path
```

---

### 197. Versión definitiva de `obtener_argumentos()`

Utilizaremos:

```python
def obtener_argumentos():

    parser = argparse.ArgumentParser(
        description=(
            "Herramienta de diagnóstico "
            "básico de red"
        )
    )

    parser.add_argument(
        "--inventario",
        required=True,
        type=Path,
        help=(
            "Archivo CSV con "
            "el inventario"
        )
    )

    return parser.parse_args()
```

---

### 198. Eliminar el inventario fijo

Ya no necesitamos:

```python
ARCHIVO_INVENTARIO = (
    DIRECTORIO_CAPITULO
    / "datos"
    / "equipos.csv"
)
```

El usuario decidirá qué inventario utilizar.

Conservaremos:

```python
DIRECTORIO_PROGRAMA
```

y:

```python
DIRECTORIO_CAPITULO
```

porque nos serán útiles para localizar:

```text
resultados
```

y posteriormente:

```text
logs
```

---

### 199. Preparar el directorio de resultados

Podemos definir:

```python
DIRECTORIO_RESULTADOS = (
    DIRECTORIO_CAPITULO
    / "resultados"
)
```

Queremos asegurarnos de que exista.

Utilizaremos:

```python
DIRECTORIO_RESULTADOS.mkdir(
    parents=True,
    exist_ok=True
)
```

---

### 200. ¿Qué hace `mkdir()`?

La opción:

```python
parents=True
```

permite crear directorios intermedios si fueran necesarios.

La opción:

```python
exist_ok=True
```

evita un error si el directorio ya existe.

Por tanto podemos ejecutar:

```python
DIRECTORIO_RESULTADOS.mkdir(
    parents=True,
    exist_ok=True
)
```

cada vez que iniciamos el programa.

---

### 201. Definir los informes

Crearemos:

```python
ARCHIVO_TXT = (
    DIRECTORIO_RESULTADOS
    / "informe_red.txt"
)


ARCHIVO_JSON = (
    DIRECTORIO_RESULTADOS
    / "informe_red.json"
)
```

Nuestra estructura será:

```text
capitulo8
│
├── datos
│   └── equipos.csv
│
├── logs
│
├── programas
│   └── administrador_red.py
│
└── resultados
    ├── informe_red.txt
    └── informe_red.json
```

---

### 202. Primer informe: TXT

El informe TXT estará pensado principalmente para:

```text
personas
```

Queremos obtener algo parecido a:

```text
INFORME DE DIAGNÓSTICO DE RED
=============================

Equipo: ServidorWeb
Host: 192.168.1.10
IP: 192.168.1.10

Ping: ACCESIBLE
Duración: 0.024 s

Puertos:
80 (http): ACCESIBLE
443 (https): ACCESIBLE

-----------------------------
```

---

### 203. Crear `generar_informe_txt()`

Podemos crear:

```python
def generar_informe_txt(
    resultados,
    archivo
):

    with archivo.open(
        "w",
        encoding="utf-8"
    ) as fichero:

        fichero.write(
            "INFORME DE DIAGNÓSTICO DE RED\n"
        )

        fichero.write(
            "=============================\n\n"
        )
```

La opción:

```text
w
```

indica que escribiremos el archivo desde cero.

---

### 204. Recorrer los resultados

Dentro de la función añadiremos:

```python
for resultado in resultados:
```

Para cada equipo escribiremos:

```python
fichero.write(
    f"Equipo: "
    f"{resultado['nombre']}\n"
)

fichero.write(
    f"Host: "
    f"{resultado['host']}\n"
)
```

---

### 205. Escribir la dirección IP

Recordemos que:

```python
resultado["ip"]
```

puede ser:

```python
None
```

Podemos preparar:

```python
ip_mostrar = (
    resultado["ip"]
    if resultado["ip"] is not None
    else "NO_RESUELTO"
)
```

Después:

```python
fichero.write(
    f"IP: {ip_mostrar}\n"
)
```

---

### 206. Escribir el resultado del ping

Podemos utilizar:

```python
fichero.write(
    "Ping: "
    f"{resultado['ping']['estado']}\n"
)
```

Y:

```python
fichero.write(
    "Duración ping: "
    f"{resultado['ping']['duracion']:.3f} s\n"
)
```

---

### 207. Escribir los puertos

Podemos recorrer:

```python
for puerto in resultado["puertos"]:
```

y escribir:

```python
fichero.write(
    f"  {puerto['puerto']} "
    f"({puerto['servicio']}): "
    f"{puerto['estado']} "
    f"({puerto['duracion']:.3f} s)\n"
)
```

---

### 208. Función completa para TXT

Podemos escribir:

```python
def generar_informe_txt(
    resultados,
    archivo
):

    with archivo.open(
        "w",
        encoding="utf-8"
    ) as fichero:

        fichero.write(
            "INFORME DE DIAGNÓSTICO DE RED\n"
        )

        fichero.write(
            "=============================\n\n"
        )

        for resultado in resultados:

            ip_mostrar = (
                resultado["ip"]
                if resultado["ip"] is not None
                else "NO_RESUELTO"
            )

            fichero.write(
                f"Equipo: "
                f"{resultado['nombre']}\n"
            )

            fichero.write(
                f"Host: "
                f"{resultado['host']}\n"
            )

            fichero.write(
                f"IP: "
                f"{ip_mostrar}\n"
            )

            fichero.write(
                "Ping: "
                f"{resultado['ping']['estado']}\n"
            )

            fichero.write(
                "Duración ping: "
                f"{resultado['ping']['duracion']:.3f} s\n"
            )

            fichero.write(
                "Puertos:\n"
            )

            for puerto in resultado["puertos"]:

                fichero.write(
                    f"  {puerto['puerto']} "
                    f"({puerto['servicio']}): "
                    f"{puerto['estado']} "
                    f"({puerto['duracion']:.3f} s)\n"
                )

            fichero.write(
                "\n-----------------------------\n\n"
            )
```

---

### 209. Generar el TXT

Después del diagnóstico utilizaremos:

```python
generar_informe_txt(
    resultados,
    ARCHIVO_TXT
)
```

Al finalizar debería aparecer:

```text
resultados/informe_red.txt
```

---

### 210. Comprobar el informe

Abre:

```text
informe_red.txt
```

desde VS Code.

Comprueba que cada equipo incluye:

```text
nombre
host
IP
ping
duración
puertos
estado de cada puerto
```

---

### 211. Segundo informe: JSON

Ahora generaremos:

```text
informe_red.json
```

JSON es especialmente útil para:

```text
intercambiar datos
automatizar procesos
usar APIs
procesar resultados
importar información
```

Nuestra estructura de diccionarios y listas ya está preparada para este formato.

---

### 212. Recordatorio de la estructura

Tenemos resultados similares a:

```python
[
    {
        "nombre": "ServidorWeb",
        "host": "192.168.1.10",
        "ip": "192.168.1.10",
        "ping": {
            "estado": "ACCESIBLE",
            "duracion": 0.021
        },
        "puertos": [
            {
                "puerto": 80,
                "servicio": "http",
                "estado": "ACCESIBLE",
                "duracion": 0.003
            }
        ]
    }
]
```

Esta estructura puede convertirse directamente a JSON.

---

### 213. Crear `generar_informe_json()`

Podemos escribir:

```python
def generar_informe_json(
    resultados,
    archivo
):

    with archivo.open(
        "w",
        encoding="utf-8"
    ) as fichero:

        json.dump(
            resultados,
            fichero,
            indent=4,
            ensure_ascii=False
        )
```

---

### 214. ¿Qué hace `indent=4`?

Sin:

```python
indent=4
```

el JSON podría escribirse prácticamente en una única línea.

Con:

```python
indent=4
```

obtenemos un documento estructurado y fácil de leer.

Por ejemplo:

```json
{
    "nombre": "ServidorWeb",
    "host": "192.168.1.10"
}
```

---

### 215. ¿Qué hace `ensure_ascii=False`?

Utilizamos:

```python
ensure_ascii=False
```

para conservar correctamente caracteres como:

```text
á
é
í
ó
ú
ñ
```

en lugar de representarlos mediante secuencias Unicode escapadas.

---

### 216. Generar el informe JSON

Después del diagnóstico añadiremos:

```python
generar_informe_json(
    resultados,
    ARCHIVO_JSON
)
```

Ahora tendremos:

```text
resultados
│
├── informe_red.txt
└── informe_red.json
```

---

### 217. Abrir el JSON en VS Code

Abre:

```text
informe_red.json
```

Podremos observar claramente la estructura:

```text
lista
 │
 ├── equipo
 │    ├── nombre
 │    ├── host
 │    ├── ip
 │    ├── ping
 │    └── puertos
 │
 └── equipo
      └── ...
```

---

### 218. TXT frente a JSON

Los dos archivos contienen información similar, pero tienen objetivos diferentes.

```text
TXT
 │
 └── lectura humana
```

Mientras:

```text
JSON
 │
 └── datos estructurados
```

Por ejemplo, un administrador puede leer:

```text
informe_red.txt
```

mientras otro programa podría procesar:

```text
informe_red.json
```

---

### 219. Añadir fecha y hora

Un informe debería indicar cuándo se realizó el diagnóstico.

Importaremos:

```python
from datetime import datetime
```

Las importaciones incluirán:

```python
from datetime import datetime
from pathlib import Path
```

---

### 220. Obtener la fecha actual

Podemos utilizar:

```python
datetime.now()
```

y formatearla:

```python
fecha = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)
```

Por ejemplo:

```text
2026-09-21 11:30:45
```

---

### 221. Añadir fecha al TXT

Al principio de:

```python
generar_informe_txt()
```

podemos obtener:

```python
fecha = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)
```

Después:

```python
fichero.write(
    f"Fecha: {fecha}\n\n"
)
```

---

### 222. Estructura más profesional para JSON

En lugar de guardar directamente:

```python
resultados
```

podemos crear:

```python
informe = {
    "fecha": fecha,
    "equipos": resultados
}
```

Así el JSON tendrá:

```json
{
    "fecha": "2026-09-21 11:30:45",
    "equipos": [
        ...
    ]
}
```

---

### 223. Mejorar `generar_informe_json()`

Podemos escribir:

```python
def generar_informe_json(
    resultados,
    archivo
):

    fecha = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    informe = {
        "fecha": fecha,
        "equipos": resultados
    }

    with archivo.open(
        "w",
        encoding="utf-8"
    ) as fichero:

        json.dump(
            informe,
            fichero,
            indent=4,
            ensure_ascii=False
        )
```

---

### 224. Evitar fechas diferentes

Existe un pequeño detalle.

Si cada función ejecuta:

```python
datetime.now()
```

por separado, el TXT y el JSON podrían tener horas ligeramente diferentes.

Es mejor obtener la fecha:

```text
una sola vez
```

y enviarla a las dos funciones.

---

### 225. Obtener la fecha en el programa principal

Podemos utilizar:

```python
fecha = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)
```

Después:

```python
generar_informe_txt(
    resultados,
    ARCHIVO_TXT,
    fecha
)
```

y:

```python
generar_informe_json(
    resultados,
    ARCHIVO_JSON,
    fecha
)
```

---

### 226. Adaptar `generar_informe_txt()`

La cabecera será:

```python
def generar_informe_txt(
    resultados,
    archivo,
    fecha
):
```

Y escribiremos:

```python
fichero.write(
    f"Fecha: {fecha}\n\n"
)
```

---

### 227. Adaptar `generar_informe_json()`

La función será:

```python
def generar_informe_json(
    resultados,
    archivo,
    fecha
):

    informe = {
        "fecha": fecha,
        "equipos": resultados
    }

    with archivo.open(
        "w",
        encoding="utf-8"
    ) as fichero:

        json.dump(
            informe,
            fichero,
            indent=4,
            ensure_ascii=False
        )
```

Ahora ambos informes corresponden exactamente a la misma ejecución.

---

### 228. Añadir estadísticas

Podemos mejorar los informes incluyendo algunas estadísticas.

Por ejemplo:

```text
equipos analizados
equipos que responden al ping
puertos comprobados
puertos accesibles
```

Crearemos una función específica.

---

### 229. Crear `calcular_estadisticas()`

```python
def calcular_estadisticas(
    resultados
):

    equipos = len(
        resultados
    )

    ping_accesibles = 0
    puertos_comprobados = 0
    puertos_accesibles = 0

    for resultado in resultados:

        if (
            resultado["ping"]["estado"]
            == "ACCESIBLE"
        ):

            ping_accesibles += 1

        for puerto in resultado["puertos"]:

            puertos_comprobados += 1

            if (
                puerto["estado"]
                == "ACCESIBLE"
            ):

                puertos_accesibles += 1

    return {
        "equipos": equipos,
        "ping_accesibles": ping_accesibles,
        "puertos_comprobados": puertos_comprobados,
        "puertos_accesibles": puertos_accesibles
    }
```

---

### 230. Ejemplo de estadísticas

Podríamos obtener:

```python
{
    "equipos": 5,
    "ping_accesibles": 3,
    "puertos_comprobados": 9,
    "puertos_accesibles": 4
}
```

Esto nos permite generar un resumen.

---

### 231. Mostrar estadísticas en pantalla

Podemos crear:

```python
def mostrar_estadisticas(
    estadisticas
):

    print(
        "\n"
        "RESUMEN"
    )

    print(
        "======="
    )

    print(
        "Equipos analizados:",
        estadisticas["equipos"]
    )

    print(
        "Responden al ping:",
        estadisticas[
            "ping_accesibles"
        ]
    )

    print(
        "Puertos comprobados:",
        estadisticas[
            "puertos_comprobados"
        ]
    )

    print(
        "Puertos accesibles:",
        estadisticas[
            "puertos_accesibles"
        ]
    )
```

---

### 232. Incorporar estadísticas al JSON

Nuestro JSON puede tener:

```python
informe = {
    "fecha": fecha,
    "estadisticas": estadisticas,
    "equipos": resultados
}
```

La función será:

```python
def generar_informe_json(
    resultados,
    estadisticas,
    archivo,
    fecha
):

    informe = {
        "fecha": fecha,
        "estadisticas": estadisticas,
        "equipos": resultados
    }

    with archivo.open(
        "w",
        encoding="utf-8"
    ) as fichero:

        json.dump(
            informe,
            fichero,
            indent=4,
            ensure_ascii=False
        )
```

---

### 233. Incorporar estadísticas al TXT

Modificaremos:

```python
generar_informe_txt()
```

para recibir también:

```python
estadisticas
```

Su cabecera será:

```python
def generar_informe_txt(
    resultados,
    estadisticas,
    archivo,
    fecha
):
```

Después de la fecha podemos escribir:

```python
fichero.write(
    "RESUMEN\n"
)

fichero.write(
    "=======\n"
)

fichero.write(
    "Equipos analizados: "
    f"{estadisticas['equipos']}\n"
)

fichero.write(
    "Responden al ping: "
    f"{estadisticas['ping_accesibles']}\n"
)

fichero.write(
    "Puertos comprobados: "
    f"{estadisticas['puertos_comprobados']}\n"
)

fichero.write(
    "Puertos accesibles: "
    f"{estadisticas['puertos_accesibles']}\n\n"
)
```

---

### 234. Flujo actualizado

Nuestro programa realiza ahora:

```text
argumentos
    │
    ▼
inventario
    │
    ▼
validación
    │
    ▼
diagnóstico
    │
    ▼
resultados
    │
    ▼
estadísticas
    │
 ┌──┴───────┐
 │          │
 ▼          ▼
TXT        JSON
```

---

### 235. Organizar el programa principal

Hasta ahora tenemos bastante código directamente al final del archivo.

Es un buen momento para crear:

```python
main()
```

Esta función controlará el flujo general de la aplicación.

---

### 236. Crear `main()`

La estructura será:

```python
def main():

    argumentos = obtener_argumentos()

    archivo_inventario = (
        argumentos.inventario
    )

    # Cargar inventario

    # Validar

    # Diagnosticar

    # Calcular estadísticas

    # Generar informes
```

---

### 237. Utilizar `if __name__ == "__main__"`

Al final escribiremos:

```python
if __name__ == "__main__":

    main()
```

Esta estructura diferencia:

```text
definición de funciones
```

de:

```text
ejecución principal
```

y facilita posteriormente:

```text
pruebas
reutilización
depuración
```

---

### 238. Gestión de errores dentro de `main()`

Podemos mover:

```python
try:
```

y:

```python
except:
```

dentro de:

```python
main()
```

Por ejemplo:

```python
try:

    equipos = cargar_inventario(
        archivo_inventario
    )

except FileNotFoundError:

    print(
        "No se encuentra "
        "el inventario."
    )

    raise SystemExit(1)

except ValueError as error:

    print(
        f"Inventario incorrecto: "
        f"{error}"
    )

    raise SystemExit(1)

except OSError as error:

    print(
        "Error leyendo "
        f"el inventario: {error}"
    )

    raise SystemExit(1)
```

---

### 239. Crear el directorio de resultados desde `main()`

Antes de generar los informes utilizaremos:

```python
DIRECTORIO_RESULTADOS.mkdir(
    parents=True,
    exist_ok=True
)
```

Así garantizamos que el directorio exista.

---

### 240. Calcular estadísticas

Después del diagnóstico:

```python
resultados = diagnosticar_red(
    equipos_validos
)
```

añadiremos:

```python
estadisticas = calcular_estadisticas(
    resultados
)
```

---

### 241. Crear una fecha común

Utilizaremos:

```python
fecha = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)
```

Esta fecha se utilizará en:

```text
TXT
```

y:

```text
JSON
```

---

### 242. Generar los dos informes

Desde `main()`:

```python
generar_informe_txt(
    resultados,
    estadisticas,
    ARCHIVO_TXT,
    fecha
)


generar_informe_json(
    resultados,
    estadisticas,
    ARCHIVO_JSON,
    fecha
)
```

---

### 243. Confirmar la generación

Podemos mostrar:

```python
print(
    "\nInformes generados:"
)

print(
    ARCHIVO_TXT
)

print(
    ARCHIVO_JSON
)
```

Así el usuario sabe dónde se han guardado los resultados.

---

### 244. Nuevo programa principal

La parte final será:

```python
def main():

    argumentos = obtener_argumentos()

    archivo_inventario = (
        argumentos.inventario
    )

    try:

        equipos = cargar_inventario(
            archivo_inventario
        )

    except FileNotFoundError:

        print(
            "No se encuentra "
            "el inventario."
        )

        raise SystemExit(1)

    except ValueError as error:

        print(
            f"Inventario incorrecto: "
            f"{error}"
        )

        raise SystemExit(1)

    except OSError as error:

        print(
            "Error leyendo "
            f"el inventario: {error}"
        )

        raise SystemExit(1)

    equipos_validos = (
        obtener_equipos_validos(
            equipos
        )
    )

    resultados = diagnosticar_red(
        equipos_validos
    )

    estadisticas = (
        calcular_estadisticas(
            resultados
        )
    )

    mostrar_resultados(
        resultados
    )

    mostrar_estadisticas(
        estadisticas
    )

    DIRECTORIO_RESULTADOS.mkdir(
        parents=True,
        exist_ok=True
    )

    fecha = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    generar_informe_txt(
        resultados,
        estadisticas,
        ARCHIVO_TXT,
        fecha
    )

    generar_informe_json(
        resultados,
        estadisticas,
        ARCHIVO_JSON,
        fecha
    )

    print(
        "\nInformes generados:"
    )

    print(
        ARCHIVO_TXT
    )

    print(
        ARCHIVO_JSON
    )


if __name__ == "__main__":

    main()
```

---

### 245. Función definitiva del informe TXT

Utilizaremos:

```python
def generar_informe_txt(
    resultados,
    estadisticas,
    archivo,
    fecha
):

    with archivo.open(
        "w",
        encoding="utf-8"
    ) as fichero:

        fichero.write(
            "INFORME DE DIAGNÓSTICO DE RED\n"
        )

        fichero.write(
            "=============================\n\n"
        )

        fichero.write(
            f"Fecha: {fecha}\n\n"
        )

        fichero.write(
            "RESUMEN\n"
        )

        fichero.write(
            "=======\n"
        )

        fichero.write(
            "Equipos analizados: "
            f"{estadisticas['equipos']}\n"
        )

        fichero.write(
            "Responden al ping: "
            f"{estadisticas['ping_accesibles']}\n"
        )

        fichero.write(
            "Puertos comprobados: "
            f"{estadisticas['puertos_comprobados']}\n"
        )

        fichero.write(
            "Puertos accesibles: "
            f"{estadisticas['puertos_accesibles']}\n\n"
        )

        for resultado in resultados:

            ip_mostrar = (
                resultado["ip"]
                if resultado["ip"] is not None
                else "NO_RESUELTO"
            )

            fichero.write(
                f"Equipo: "
                f"{resultado['nombre']}\n"
            )

            fichero.write(
                f"Host: "
                f"{resultado['host']}\n"
            )

            fichero.write(
                f"IP: "
                f"{ip_mostrar}\n"
            )

            fichero.write(
                "Ping: "
                f"{resultado['ping']['estado']}\n"
            )

            fichero.write(
                "Duración ping: "
                f"{resultado['ping']['duracion']:.3f} s\n"
            )

            fichero.write(
                "Puertos:\n"
            )

            for puerto in resultado["puertos"]:

                fichero.write(
                    f"  {puerto['puerto']} "
                    f"({puerto['servicio']}): "
                    f"{puerto['estado']} "
                    f"({puerto['duracion']:.3f} s)\n"
                )

            fichero.write(
                "\n-----------------------------\n\n"
            )
```

---

### 246. Función definitiva del informe JSON

Utilizaremos:

```python
def generar_informe_json(
    resultados,
    estadisticas,
    archivo,
    fecha
):

    informe = {
        "fecha": fecha,
        "estadisticas": estadisticas,
        "equipos": resultados
    }

    with archivo.open(
        "w",
        encoding="utf-8"
    ) as fichero:

        json.dump(
            informe,
            fichero,
            indent=4,
            ensure_ascii=False
        )
```

---

### 247. Ejecutar la aplicación

Desde:

```text
practicas\capitulo8\programas
```

ejecuta:

```powershell
python administrador_red.py --inventario ../datos/equipos.csv
```

El programa deberá:

```text
1. leer el CSV

2. validar los equipos

3. realizar ping

4. resolver los hosts

5. comprobar los puertos

6. mostrar los resultados

7. calcular estadísticas

8. generar TXT

9. generar JSON
```

---

### 248. Comprobar los archivos generados

Después de ejecutar debemos tener:

```text
capitulo8
│
├── datos
│   └── equipos.csv
│
├── logs
│
├── programas
│   └── administrador_red.py
│
└── resultados
    ├── informe_red.txt
    └── informe_red.json
```

Abre ambos archivos desde VS Code.

---

### 249. Ejemplo del informe TXT

Podremos obtener algo similar a:

```text
INFORME DE DIAGNÓSTICO DE RED
=============================

Fecha: 2026-09-21 11:30:45

RESUMEN
=======

Equipos analizados: 2
Responden al ping: 2
Puertos comprobados: 4
Puertos accesibles: 1

Equipo: ServidorLocal
Host: 127.0.0.1
IP: 127.0.0.1
Ping: ACCESIBLE
Duración ping: 0.018 s
Puertos:
  8000 (desconocido): ACCESIBLE (0.001 s)
  8001 (desconocido): NO_ACCESIBLE (0.001 s)

-----------------------------
```

Los resultados dependerán de la red y de los servicios activos.

---

### 250. Ejemplo del informe JSON

Podremos obtener:

```json
{
    "fecha": "2026-09-21 11:30:45",
    "estadisticas": {
        "equipos": 2,
        "ping_accesibles": 2,
        "puertos_comprobados": 4,
        "puertos_accesibles": 1
    },
    "equipos": [
        {
            "nombre": "ServidorLocal",
            "host": "127.0.0.1",
            "ip": "127.0.0.1",
            "ping": {
                "estado": "ACCESIBLE",
                "duracion": 0.018
            },
            "puertos": [
                {
                    "puerto": 8000,
                    "servicio": "desconocido",
                    "estado": "ACCESIBLE",
                    "duracion": 0.001
                }
            ]
        }
    ]
}
```

---

### 251. Probar otro inventario

Crea:

```text
datos/equipos_prueba.csv
```

Por ejemplo:

```csv
nombre,host,puertos
Localhost,127.0.0.1,8000;8001
```

Ahora ejecuta:

```powershell
python administrador_red.py --inventario ../datos/equipos_prueba.csv
```

No hemos tenido que modificar:

```text
administrador_red.py
```

Esta es precisamente la ventaja de utilizar:

```python
argparse
```

---

### 252. Probar un archivo inexistente

Ejecuta:

```powershell
python administrador_red.py --inventario ../datos/no_existe.csv
```

El programa debe detectar el problema y mostrar:

```text
No se encuentra el inventario.
```

sin mostrar un traceback innecesario al usuario.

---

### 253. Probar sin argumentos

Ejecuta:

```powershell
python administrador_red.py
```

`argparse` detectará automáticamente que falta:

```text
--inventario
```

y mostrará el mensaje de uso correspondiente.

---

### 254. Probar `--help`

Ejecuta:

```powershell
python administrador_red.py --help
```

Comprueba que un usuario que no conozca el programa pueda descubrir cómo utilizarlo.

Esto es una característica importante de una herramienta de línea de comandos.

---

### 255. Depurar un programa con argumentos

Existe ahora una diferencia respecto a las prácticas anteriores.

Nuestro programa necesita:

```text
--inventario
```

Si pulsamos simplemente:

```text
F5
```

VS Code necesita saber qué argumentos debe proporcionar al programa.

Podemos solucionarlo creando una configuración de depuración.

---

### 256. Crear `launch.json`

En la raíz del proyecto crea, si no existe:

```text
.vscode/
```

y dentro:

```text
launch.json
```

La estructura será:

```text
Libro-Python-FP
│
├── .vscode
│   └── launch.json
│
├── docs
│
├── practicas
│
└── mkdocs.yml
```

---

### 257. Configuración de depuración

Añade:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Proyecto final - diagnóstico",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/practicas/capitulo8/programas/administrador_red.py",
            "console": "integratedTerminal",
            "args": [
                "--inventario",
                "${workspaceFolder}/practicas/capitulo8/datos/equipos.csv"
            ]
        }
    ]
}
```

Ahora VS Code podrá ejecutar el programa mediante el depurador proporcionando automáticamente:

```text
--inventario
```

---

### 258. Ejecutar con F5

Abre:

```text
Run and Debug
```

o:

```text
Ejecutar y depurar
```

Selecciona:

```text
Proyecto final - diagnóstico
```

y pulsa:

```text
F5
```

El programa deberá iniciarse con el inventario configurado.

---

### 259. Colocar un breakpoint en `main()`

Coloca un breakpoint en:

```python
argumentos = obtener_argumentos()
```

Después avanza con:

```text
F10
```

Observa:

```python
argumentos.inventario
```

Deberá contener una ruta al archivo:

```text
equipos.csv
```

---

### 260. Seguir el flujo completo

Continúa con:

```text
F10
```

y:

```text
F11
```

para recorrer:

```text
obtener_argumentos()
        │
        ▼
cargar_inventario()
        │
        ▼
obtener_equipos_validos()
        │
        ▼
diagnosticar_red()
        │
        ▼
calcular_estadisticas()
        │
        ▼
generar_informe_txt()
        │
        ▼
generar_informe_json()
```

Ahora podemos depurar prácticamente toda la aplicación desde:

```python
main()
```

---

### 261. Verificar el JSON desde Python

Podemos comprobar que el archivo generado es un JSON válido.

Desde una consola Python:

```python
import json
```

Después:

```python
with open(
    "../resultados/informe_red.json",
    "r",
    encoding="utf-8"
) as fichero:

    datos = json.load(
        fichero
    )
```

Y:

```python
print(
    datos["estadisticas"]
)
```

Esto demuestra que el informe no es solamente texto.

Puede volver a convertirse en estructuras Python.

---

### 262. Acceder a los resultados JSON

Podemos consultar:

```python
datos["equipos"]
```

O el primer equipo:

```python
datos["equipos"][0]
```

También:

```python
datos["equipos"][0]["ping"]
```

y:

```python
datos["equipos"][0]["puertos"]
```

Esto muestra una de las principales ventajas de almacenar información estructurada.

---

### 263. Separar presentación y datos

Nuestro proyecto tiene ahora dos formas de representar los resultados.

Para una persona:

```text
informe_red.txt
```

Para otro programa:

```text
informe_red.json
```

El diagnóstico se realiza solamente:

```text
una vez
```

y los mismos datos se utilizan para generar ambos formatos.

Esta separación es una práctica importante:

```text
obtener datos
      │
      ▼
procesar datos
      │
      ▼
presentar datos
```

---

### 264. No repetir el diagnóstico

No debemos hacer:

```text
diagnóstico
    │
    ▼
generar TXT

diagnóstico otra vez
    │
    ▼
generar JSON
```

Sería ineficiente y además los resultados podrían cambiar entre ambas ejecuciones.

Nuestro diseño correcto es:

```text
          diagnóstico
              │
              ▼
          resultados
          ┌───┴───┐
          │       │
          ▼       ▼
         TXT     JSON
```

---

### 265. Práctica propuesta

Crea:

```text
equipos_practica.csv
```

con al menos:

```text
4 equipos
```

Cada equipo deberá contener entre:

```text
1 y 4 puertos
```

Ejecuta:

```powershell
python administrador_red.py --inventario ../datos/equipos_practica.csv
```

Comprueba:

```text
salida por pantalla
informe TXT
informe JSON
estadísticas
```

---

### 266. Práctica de análisis del JSON

Abre:

```text
informe_red.json
```

Localiza:

```text
estadisticas
```

Después localiza:

```text
equipos
```

Selecciona un equipo y determina:

```text
nombre
host
IP
estado del ping
duración
puertos comprobados
estado de cada puerto
```

---

### 267. Reto de programación

Modifica:

```python
calcular_estadisticas()
```

para añadir:

```text
equipos_no_resueltos
```

El resultado podría ser:

```python
{
    "equipos": 5,
    "ping_accesibles": 3,
    "equipos_no_resueltos": 1,
    "puertos_comprobados": 9,
    "puertos_accesibles": 4
}
```

Después incorpora este dato a:

```text
pantalla
TXT
JSON
```

---

### 268. Reto adicional

Añade a las estadísticas:

```text
puertos_no_accesibles
```

Puedes calcularlo directamente o utilizar:

```text
puertos comprobados
-
puertos accesibles
```

Piensa cuál de las dos soluciones representa mejor los estados:

```text
NO_ACCESIBLE
ERROR
NO_RESUELTO
```

antes de decidir cómo implementarlo.

---

### 269. Estado actual del proyecto

Ya tenemos:

```text
[✓] inventario CSV

[✓] validación

[✓] ping

[✓] resolución de host

[✓] comprobación TCP

[✓] resultados estructurados

[✓] argparse

[✓] selección de inventario

[✓] estadísticas

[✓] informe TXT

[✓] informe JSON

[✓] fecha del diagnóstico

[✓] configuración de depuración con argumentos
```

Todavía debemos completar:

```text
[ ] logging completo

[ ] registro de errores en log.txt

[ ] mejorar la gestión de incidencias

[ ] pruebas finales

[ ] revisión del proyecto

[ ] cierre del módulo y del libro
```

---

### 270. Resumen de esta cuarta fase

En esta fase hemos convertido nuestro programa en una herramienta de línea de comandos.

Ahora podemos ejecutar:

```powershell
python administrador_red.py --inventario ../datos/equipos.csv
```

mediante:

```python
argparse
```

También hemos generado dos tipos de informes:

```text
informe_red.txt
```

para lectura humana y:

```text
informe_red.json
```

para almacenar los datos de forma estructurada.

Hemos incorporado:

```text
fecha de ejecución
estadísticas
directorio de resultados
main()
if __name__ == "__main__"
```

y hemos creado:

```text
.vscode/launch.json
```

para poder depurar el programa con argumentos desde VS Code.

Nuestro proyecto tiene ahora este flujo:

```text
              USUARIO
                 │
                 ▼
              argparse
                 │
                 ▼
            equipos.csv
                 │
                 ▼
              validar
                 │
                 ▼
             diagnóstico
        ┌────────┼────────┐
        │        │        │
        ▼        ▼        ▼
      PING      DNS      TCP
        │        │        │
        └────────┼────────┘
                 │
                 ▼
             resultados
                 │
                 ▼
            estadísticas
             ┌───┴───┐
             │       │
             ▼       ▼
            TXT     JSON
```

!!! success "Cuarta fase completada"

    Nuestra aplicación ya cumple la mayor parte de los requisitos funcionales del proyecto final.

    Lee un inventario CSV, realiza el diagnóstico de red y genera informes TXT y JSON con los resultados.

En la **siguiente y última fase del proyecto** incorporaremos `logging` para crear:

```text
logs/
└── log.txt
```

Registraremos el inicio y final de la ejecución, los equipos procesados y, especialmente, los errores e incidencias. Después realizaremos una batería de pruebas finales, revisaremos el programa completo y cerraremos el **proyecto final, el Módulo 3 y el libro**.

---

## 271. Quinta fase: logging, pruebas finales y cierre del proyecto

Nuestra aplicación ya realiza prácticamente todo el trabajo:

```text
equipos.csv
     │
     ▼
validación
     │
     ▼
diagnóstico
 ┌───┼────┐
 ▼   ▼    ▼
PING DNS  TCP
 └───┼────┘
     ▼
resultados
     │
     ▼
estadísticas
  ┌──┴──┐
  ▼     ▼
 TXT   JSON
```

Sin embargo, una aplicación de administración debe dejar constancia de lo que ocurre durante su ejecución.

Queremos registrar:

```text
inicio del programa
archivo utilizado
equipos procesados
errores
advertencias
finalización
```

Para ello utilizaremos:

```python
logging
```

y crearemos:

```text
logs/
└── log.txt
```

---

### 272. ¿Qué es un log?

Un log es un registro cronológico de acontecimientos producidos durante la ejecución de un programa.

Por ejemplo:

```text
2026-09-21 12:15:02 INFO Inicio del diagnóstico
2026-09-21 12:15:02 INFO Inventario: equipos.csv
2026-09-21 12:15:03 INFO Analizando ServidorWeb
2026-09-21 12:15:04 WARNING Host no resuelto: servidor2.local
2026-09-21 12:15:05 INFO Diagnóstico finalizado
```

Este archivo permite investigar posteriormente qué ocurrió.

---

### 273. `print()` y `logging`

Hasta ahora hemos utilizado frecuentemente:

```python
print()
```

`print()` es apropiado para mostrar información al usuario.

Pero:

```python
logging
```

permite registrar información de forma permanente.

Podemos utilizar ambos:

```text
print()
   │
   └── información para el usuario


logging
   │
   └── registro técnico de ejecución
```

No son necesariamente sustitutos.

---

### 274. Importar `logging`

Añade:

```python
import logging
```

Las importaciones principales serán:

```python
import argparse
import csv
import json
import logging
import socket
import subprocess
import time

from datetime import datetime
from pathlib import Path
```

---

### 275. Crear el directorio de logs

Ya tenemos:

```python
DIRECTORIO_CAPITULO
```

Podemos definir:

```python
DIRECTORIO_LOGS = (
    DIRECTORIO_CAPITULO
    / "logs"
)
```

Y el archivo:

```python
ARCHIVO_LOG = (
    DIRECTORIO_LOGS
    / "log.txt"
)
```

---

### 276. Crear el directorio automáticamente

Antes de configurar el sistema de logging debemos asegurarnos de que:

```text
logs
```

existe.

Utilizaremos:

```python
DIRECTORIO_LOGS.mkdir(
    parents=True,
    exist_ok=True
)
```

La estructura final será:

```text
capitulo8
│
├── datos
│   └── equipos.csv
│
├── logs
│   └── log.txt
│
├── programas
│   └── administrador_red.py
│
└── resultados
    ├── informe_red.txt
    └── informe_red.json
```

---

### 277. Configurar `logging`

Crearemos:

```python
def configurar_logging():

    DIRECTORIO_LOGS.mkdir(
        parents=True,
        exist_ok=True
    )

    logging.basicConfig(
        filename=ARCHIVO_LOG,
        level=logging.INFO,
        format=(
            "%(asctime)s "
            "%(levelname)s "
            "%(message)s"
        ),
        encoding="utf-8"
    )
```

---

### 278. Comprender `basicConfig()`

Hemos utilizado:

```python
filename=ARCHIVO_LOG
```

para indicar el archivo.

También:

```python
level=logging.INFO
```

para registrar mensajes desde el nivel:

```text
INFO
```

en adelante.

El formato:

```python
"%(asctime)s %(levelname)s %(message)s"
```

añade:

```text
fecha y hora
nivel
mensaje
```

---

### 279. Niveles de logging

Entre los niveles habituales encontramos:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

Podemos interpretarlos aproximadamente como:

```text
DEBUG
información detallada de diagnóstico

INFO
funcionamiento normal

WARNING
situación inesperada que permite continuar

ERROR
operación que ha fallado

CRITICAL
problema especialmente grave
```

En nuestro proyecto utilizaremos principalmente:

```text
INFO
WARNING
ERROR
```

---

### 280. Primer mensaje

Después de configurar logging podemos escribir:

```python
logging.info(
    "Inicio del diagnóstico"
)
```

Al ejecutar el programa aparecerá una línea similar a:

```text
2026-09-21 12:15:02,341 INFO Inicio del diagnóstico
```

---

### 281. Registrar el inventario utilizado

Después de procesar los argumentos podemos añadir:

```python
logging.info(
    "Inventario utilizado: %s",
    archivo_inventario
)
```

Observa que no necesitamos construir previamente una cadena con una f-string.

`logging` puede recibir:

```text
mensaje
+
argumentos
```

---

### 282. Registrar cada equipo

Dentro de:

```python
diagnosticar_red()
```

podemos añadir:

```python
logging.info(
    "Analizando equipo: %s (%s)",
    equipo["nombre"],
    equipo["host"]
)
```

Así podremos saber exactamente qué equipos fueron procesados.

---

### 283. Registrar el resultado del ping

Dentro de:

```python
diagnosticar_equipo()
```

después de:

```python
ping = comprobar_ping(
    equipo["host"]
)
```

podemos registrar:

```python
logging.info(
    "Ping %s: %s",
    equipo["host"],
    ping["estado"]
)
```

---

### 284. Registrar problemas de resolución

Después de:

```python
ip = resolver_host(
    equipo["host"]
)
```

podemos comprobar:

```python
if ip is None:

    logging.warning(
        "No se pudo resolver el host: %s",
        equipo["host"]
    )
```

Esto es una:

```text
WARNING
```

porque el diagnóstico puede continuar y registrar los puertos como:

```text
NO_RESUELTO
```

---

### 285. Registrar los puertos

Después de comprobar cada puerto podemos registrar:

```python
logging.info(
    "Puerto TCP %s:%s -> %s",
    host,
    puerto,
    estado
)
```

De esta forma el log podrá contener:

```text
INFO Puerto TCP 192.168.1.10:80 -> ACCESIBLE
INFO Puerto TCP 192.168.1.10:443 -> NO_ACCESIBLE
```

---

### 286. Registrar errores TCP

Dentro de:

```python
comprobar_puerto()
```

tenemos:

```python
except OSError:
```

Podemos mejorarlo:

```python
except OSError as error:

    estado = "ERROR"

    logging.error(
        "Error comprobando %s:%s: %s",
        host,
        puerto,
        error
    )
```

Así no perdemos la información técnica del error.

---

### 287. Registrar errores de ping

También podemos mejorar:

```python
except subprocess.TimeoutExpired:
```

con:

```python
except subprocess.TimeoutExpired:

    estado = "TIMEOUT"

    logging.warning(
        "Timeout de ping para %s",
        host
    )
```

Y:

```python
except OSError as error:

    estado = "ERROR"

    logging.error(
        "Error ejecutando ping para %s: %s",
        host,
        error
    )
```

---

### 288. Registrar errores del inventario

Dentro de `main()` podemos registrar:

```python
except FileNotFoundError:

    logging.error(
        "No se encuentra el inventario: %s",
        archivo_inventario
    )

    print(
        "No se encuentra el inventario."
    )

    raise SystemExit(1)
```

---

### 289. Registrar un CSV incorrecto

Podemos utilizar:

```python
except ValueError as error:

    logging.error(
        "Inventario incorrecto: %s",
        error
    )

    print(
        f"Inventario incorrecto: {error}"
    )

    raise SystemExit(1)
```

---

### 290. Registrar errores de lectura

Para:

```python
except OSError as error:
```

utilizaremos:

```python
logging.error(
    "Error leyendo el inventario: %s",
    error
)
```

antes de finalizar.

---

### 291. Registrar equipos incorrectos

En:

```python
obtener_equipos_validos()
```

podemos mejorar:

```python
else:

    logging.warning(
        "Equipo descartado por "
        "datos incorrectos: %s",
        equipo["nombre"]
    )

    print(
        "Equipo incorrecto:",
        equipo["nombre"]
    )
```

Ahora también quedará constancia en:

```text
log.txt
```

---

### 292. Registrar los informes generados

Después de generar los informes podemos añadir:

```python
logging.info(
    "Informe TXT generado: %s",
    ARCHIVO_TXT
)

logging.info(
    "Informe JSON generado: %s",
    ARCHIVO_JSON
)
```

---

### 293. Registrar el final

Al terminar correctamente:

```python
logging.info(
    "Diagnóstico finalizado correctamente"
)
```

Así podremos identificar claramente:

```text
inicio
```

y:

```text
final
```

de cada ejecución.

---

### 294. Ejemplo de `log.txt`

Después de una ejecución podríamos obtener:

```text
2026-09-21 12:15:02,341 INFO Inicio del diagnóstico
2026-09-21 12:15:02,342 INFO Inventario utilizado: ../datos/equipos.csv
2026-09-21 12:15:02,345 INFO Analizando equipo: Localhost (127.0.0.1)
2026-09-21 12:15:02,367 INFO Ping 127.0.0.1: ACCESIBLE
2026-09-21 12:15:02,369 INFO Puerto TCP 127.0.0.1:8000 -> ACCESIBLE
2026-09-21 12:15:02,370 INFO Puerto TCP 127.0.0.1:8001 -> NO_ACCESIBLE
2026-09-21 12:15:02,374 INFO Informe TXT generado
2026-09-21 12:15:02,375 INFO Informe JSON generado
2026-09-21 12:15:02,375 INFO Diagnóstico finalizado correctamente
```

Los valores reales dependerán de cada ejecución.

---

### 295. Conservar ejecuciones anteriores

Por defecto, si no indicamos:

```python
filemode="w"
```

`FileHandler` utilizado por `basicConfig()` trabaja normalmente añadiendo contenido al archivo.

Podemos hacerlo explícito:

```python
logging.basicConfig(
    filename=ARCHIVO_LOG,
    filemode="a",
    level=logging.INFO,
    format=(
        "%(asctime)s "
        "%(levelname)s "
        "%(message)s"
    ),
    encoding="utf-8"
)
```

La opción:

```text
a
```

significa:

```text
append
```

Por tanto, las nuevas ejecuciones se añadirán al final.

---

### 296. Separar las ejecuciones

Podemos registrar:

```python
logging.info(
    "========================================"
)

logging.info(
    "Inicio del diagnóstico"
)
```

Así resulta más sencillo distinguir diferentes ejecuciones.

---

### 297. Versión definitiva de `configurar_logging()`

Utilizaremos:

```python
def configurar_logging():

    DIRECTORIO_LOGS.mkdir(
        parents=True,
        exist_ok=True
    )

    logging.basicConfig(
        filename=ARCHIVO_LOG,
        filemode="a",
        level=logging.INFO,
        format=(
            "%(asctime)s "
            "%(levelname)s "
            "%(message)s"
        ),
        encoding="utf-8"
    )

    logging.info(
        "========================================"
    )

    logging.info(
        "Inicio del diagnóstico"
    )
```

---

### 298. Configurar logging al principio de `main()`

Nuestra función comenzará:

```python
def main():

    configurar_logging()

    argumentos = obtener_argumentos()

    archivo_inventario = (
        argumentos.inventario
    )
```

De esta forma el sistema de registro estará disponible durante prácticamente toda la ejecución.

---

### 299. Un detalle sobre `argparse`

Existe una particularidad.

Si el usuario ejecuta:

```powershell
python administrador_red.py
```

sin proporcionar el argumento obligatorio:

```text
--inventario
```

`argparse` puede finalizar el programa durante:

```python
parse_args()
```

Por tanto, ese error no pasará por la gestión posterior de nuestro programa.

Para este proyecto es perfectamente aceptable.

`argparse` ya proporciona automáticamente el mensaje correspondiente al usuario.

---

### 300. Mejorar `resolver_host()`

Podemos registrar los errores de resolución:

```python
def resolver_host(
    host
):

    try:

        ip = socket.gethostbyname(
            host
        )

    except socket.gaierror as error:

        logging.warning(
            "No se pudo resolver %s: %s",
            host,
            error
        )

        return None

    return ip
```

Ahora disponemos también del detalle técnico.

---

### 301. Mejorar `comprobar_ping()`

La función puede quedar:

```python
def comprobar_ping(
    host,
    timeout=3
):

    inicio = time.perf_counter()

    try:

        resultado = subprocess.run(
            [
                "ping",
                "-n",
                "1",
                host
            ],
            capture_output=True,
            text=True,
            timeout=timeout
        )

    except subprocess.TimeoutExpired:

        estado = "TIMEOUT"

        logging.warning(
            "Timeout de ping para %s",
            host
        )

    except OSError as error:

        estado = "ERROR"

        logging.error(
            "Error ejecutando ping "
            "para %s: %s",
            host,
            error
        )

    else:

        if resultado.returncode == 0:

            estado = "ACCESIBLE"

        else:

            estado = "NO_ACCESIBLE"

    fin = time.perf_counter()

    logging.info(
        "Ping %s -> %s",
        host,
        estado
    )

    return {
        "estado": estado,
        "duracion": (
            fin - inicio
        )
    }
```

---

### 302. Mejorar `comprobar_puerto()`

Podemos dejarla:

```python
def comprobar_puerto(
    host,
    puerto,
    timeout=1
):

    inicio = time.perf_counter()

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as sock:

            sock.settimeout(
                timeout
            )

            codigo = sock.connect_ex(
                (
                    host,
                    puerto
                )
            )

    except OSError as error:

        estado = "ERROR"

        logging.error(
            "Error comprobando "
            "%s:%s: %s",
            host,
            puerto,
            error
        )

    else:

        if codigo == 0:

            estado = "ACCESIBLE"

        else:

            estado = "NO_ACCESIBLE"

    fin = time.perf_counter()

    logging.info(
        "Puerto TCP %s:%s -> %s",
        host,
        puerto,
        estado
    )

    return {
        "puerto": puerto,
        "servicio": obtener_servicio(
            puerto
        ),
        "estado": estado,
        "duracion": (
            fin - inicio
        )
    }
```

---

### 303. Mejorar `diagnosticar_red()`

Podemos registrar cada equipo:

```python
def diagnosticar_red(
    equipos
):

    resultados = []

    for equipo in equipos:

        print(
            f"Analizando "
            f"{equipo['nombre']}..."
        )

        logging.info(
            "Analizando equipo: %s (%s)",
            equipo["nombre"],
            equipo["host"]
        )

        resultado = diagnosticar_equipo(
            equipo
        )

        resultados.append(
            resultado
        )

    return resultados
```

---

### 304. Programa completo final

A continuación se muestra una versión integrada del programa.

```python
import argparse
import csv
import json
import logging
import socket
import subprocess
import time

from datetime import datetime
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

DIRECTORIO_LOGS = (
    DIRECTORIO_CAPITULO
    / "logs"
)

ARCHIVO_TXT = (
    DIRECTORIO_RESULTADOS
    / "informe_red.txt"
)

ARCHIVO_JSON = (
    DIRECTORIO_RESULTADOS
    / "informe_red.json"
)

ARCHIVO_LOG = (
    DIRECTORIO_LOGS
    / "log.txt"
)


def configurar_logging():

    DIRECTORIO_LOGS.mkdir(
        parents=True,
        exist_ok=True
    )

    logging.basicConfig(
        filename=ARCHIVO_LOG,
        filemode="a",
        level=logging.INFO,
        format=(
            "%(asctime)s "
            "%(levelname)s "
            "%(message)s"
        ),
        encoding="utf-8"
    )

    logging.info(
        "========================================"
    )

    logging.info(
        "Inicio del diagnóstico"
    )


def obtener_argumentos():

    parser = argparse.ArgumentParser(
        description=(
            "Herramienta de diagnóstico "
            "básico de red"
        )
    )

    parser.add_argument(
        "--inventario",
        required=True,
        type=Path,
        help=(
            "Archivo CSV con "
            "el inventario"
        )
    )

    return parser.parse_args()


def convertir_puertos(
    texto
):

    puertos = []

    for puerto in texto.split(";"):

        puerto = puerto.strip()

        if not puerto:

            continue

        try:

            numero = int(
                puerto
            )

        except ValueError:

            return None

        puertos.append(
            numero
        )

    return puertos


def cargar_inventario(
    archivo
):

    equipos = []

    with archivo.open(
        "r",
        encoding="utf-8",
        newline=""
    ) as fichero:

        lector = csv.DictReader(
            fichero
        )

        columnas_necesarias = {
            "nombre",
            "host",
            "puertos"
        }

        columnas_disponibles = set(
            lector.fieldnames or []
        )

        if not columnas_necesarias.issubset(
            columnas_disponibles
        ):

            raise ValueError(
                "El CSV no contiene "
                "las columnas necesarias."
            )

        for fila in lector:

            nombre = (
                fila["nombre"].strip()
            )

            host = (
                fila["host"].strip()
            )

            puertos = convertir_puertos(
                fila["puertos"]
            )

            if puertos is None:

                logging.warning(
                    "Puertos incorrectos "
                    "en el equipo: %s",
                    nombre
                )

                continue

            equipos.append(
                {
                    "nombre": nombre,
                    "host": host,
                    "puertos": puertos
                }
            )

    return equipos


def validar_equipo(
    equipo
):

    if not equipo["nombre"]:

        return False

    if not equipo["host"]:

        return False

    if not equipo["puertos"]:

        return False

    for puerto in equipo["puertos"]:

        if (
            puerto < 1
            or puerto > 65535
        ):

            return False

    return True


def obtener_equipos_validos(
    equipos
):

    validos = []

    for equipo in equipos:

        if validar_equipo(
            equipo
        ):

            validos.append(
                equipo
            )

        else:

            logging.warning(
                "Equipo descartado por "
                "datos incorrectos: %s",
                equipo["nombre"]
            )

            print(
                "Equipo incorrecto:",
                equipo["nombre"]
            )

    return validos


def comprobar_ping(
    host,
    timeout=3
):

    inicio = time.perf_counter()

    try:

        resultado = subprocess.run(
            [
                "ping",
                "-n",
                "1",
                host
            ],
            capture_output=True,
            text=True,
            timeout=timeout
        )

    except subprocess.TimeoutExpired:

        estado = "TIMEOUT"

        logging.warning(
            "Timeout de ping para %s",
            host
        )

    except OSError as error:

        estado = "ERROR"

        logging.error(
            "Error ejecutando ping "
            "para %s: %s",
            host,
            error
        )

    else:

        if resultado.returncode == 0:

            estado = "ACCESIBLE"

        else:

            estado = "NO_ACCESIBLE"

    fin = time.perf_counter()

    logging.info(
        "Ping %s -> %s",
        host,
        estado
    )

    return {
        "estado": estado,
        "duracion": (
            fin - inicio
        )
    }


def resolver_host(
    host
):

    try:

        ip = socket.gethostbyname(
            host
        )

    except socket.gaierror as error:

        logging.warning(
            "No se pudo resolver "
            "%s: %s",
            host,
            error
        )

        return None

    return ip


def obtener_servicio(
    puerto
):

    try:

        return socket.getservbyport(
            puerto,
            "tcp"
        )

    except OSError:

        return "desconocido"


def comprobar_puerto(
    host,
    puerto,
    timeout=1
):

    inicio = time.perf_counter()

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as sock:

            sock.settimeout(
                timeout
            )

            codigo = sock.connect_ex(
                (
                    host,
                    puerto
                )
            )

    except OSError as error:

        estado = "ERROR"

        logging.error(
            "Error comprobando "
            "%s:%s: %s",
            host,
            puerto,
            error
        )

    else:

        if codigo == 0:

            estado = "ACCESIBLE"

        else:

            estado = "NO_ACCESIBLE"

    fin = time.perf_counter()

    logging.info(
        "Puerto TCP %s:%s -> %s",
        host,
        puerto,
        estado
    )

    return {
        "puerto": puerto,
        "servicio": obtener_servicio(
            puerto
        ),
        "estado": estado,
        "duracion": (
            fin - inicio
        )
    }


def comprobar_puertos(
    host,
    puertos,
    timeout=1
):

    resultados = []

    for puerto in puertos:

        resultados.append(
            comprobar_puerto(
                host,
                puerto,
                timeout
            )
        )

    return resultados


def diagnosticar_equipo(
    equipo
):

    ping = comprobar_ping(
        equipo["host"]
    )

    ip = resolver_host(
        equipo["host"]
    )

    if ip is None:

        puertos = []

        for puerto in equipo["puertos"]:

            puertos.append(
                {
                    "puerto": puerto,
                    "servicio": (
                        obtener_servicio(
                            puerto
                        )
                    ),
                    "estado": "NO_RESUELTO",
                    "duracion": 0
                }
            )

    else:

        puertos = comprobar_puertos(
            ip,
            equipo["puertos"]
        )

    return {
        "nombre": equipo["nombre"],
        "host": equipo["host"],
        "ip": ip,
        "ping": ping,
        "puertos": puertos
    }


def diagnosticar_red(
    equipos
):

    resultados = []

    for equipo in equipos:

        print(
            f"Analizando "
            f"{equipo['nombre']}..."
        )

        logging.info(
            "Analizando equipo: %s (%s)",
            equipo["nombre"],
            equipo["host"]
        )

        resultados.append(
            diagnosticar_equipo(
                equipo
            )
        )

    return resultados


def calcular_estadisticas(
    resultados
):

    equipos = len(
        resultados
    )

    ping_accesibles = 0
    puertos_comprobados = 0
    puertos_accesibles = 0

    for resultado in resultados:

        if (
            resultado["ping"]["estado"]
            == "ACCESIBLE"
        ):

            ping_accesibles += 1

        for puerto in resultado["puertos"]:

            puertos_comprobados += 1

            if (
                puerto["estado"]
                == "ACCESIBLE"
            ):

                puertos_accesibles += 1

    return {
        "equipos": equipos,
        "ping_accesibles": ping_accesibles,
        "puertos_comprobados": puertos_comprobados,
        "puertos_accesibles": puertos_accesibles
    }


def mostrar_resultados(
    resultados
):

    for resultado in resultados:

        ip_mostrar = (
            resultado["ip"]
            if resultado["ip"] is not None
            else "NO_RESUELTO"
        )

        print(
            "\n===================="
        )

        print(
            f"Equipo: {resultado['nombre']}"
        )

        print(
            f"Host: {resultado['host']}"
        )

        print(
            f"IP: {ip_mostrar}"
        )

        print(
            "Ping: "
            f"{resultado['ping']['estado']}"
        )

        print(
            "Duración ping: "
            f"{resultado['ping']['duracion']:.3f} s"
        )

        print(
            "Puertos:"
        )

        for puerto in resultado["puertos"]:

            print(
                "  "
                f"{puerto['puerto']} "
                f"({puerto['servicio']}): "
                f"{puerto['estado']} "
                f"({puerto['duracion']:.3f} s)"
            )


def mostrar_estadisticas(
    estadisticas
):

    print(
        "\nRESUMEN"
    )

    print(
        "======="
    )

    print(
        "Equipos analizados:",
        estadisticas["equipos"]
    )

    print(
        "Responden al ping:",
        estadisticas[
            "ping_accesibles"
        ]
    )

    print(
        "Puertos comprobados:",
        estadisticas[
            "puertos_comprobados"
        ]
    )

    print(
        "Puertos accesibles:",
        estadisticas[
            "puertos_accesibles"
        ]
    )


def generar_informe_txt(
    resultados,
    estadisticas,
    archivo,
    fecha
):

    with archivo.open(
        "w",
        encoding="utf-8"
    ) as fichero:

        fichero.write(
            "INFORME DE DIAGNÓSTICO DE RED\n"
        )

        fichero.write(
            "=============================\n\n"
        )

        fichero.write(
            f"Fecha: {fecha}\n\n"
        )

        fichero.write(
            "RESUMEN\n"
            "=======\n"
        )

        fichero.write(
            "Equipos analizados: "
            f"{estadisticas['equipos']}\n"
        )

        fichero.write(
            "Responden al ping: "
            f"{estadisticas['ping_accesibles']}\n"
        )

        fichero.write(
            "Puertos comprobados: "
            f"{estadisticas['puertos_comprobados']}\n"
        )

        fichero.write(
            "Puertos accesibles: "
            f"{estadisticas['puertos_accesibles']}\n\n"
        )

        for resultado in resultados:

            ip_mostrar = (
                resultado["ip"]
                if resultado["ip"] is not None
                else "NO_RESUELTO"
            )

            fichero.write(
                f"Equipo: {resultado['nombre']}\n"
            )

            fichero.write(
                f"Host: {resultado['host']}\n"
            )

            fichero.write(
                f"IP: {ip_mostrar}\n"
            )

            fichero.write(
                "Ping: "
                f"{resultado['ping']['estado']}\n"
            )

            fichero.write(
                "Duración ping: "
                f"{resultado['ping']['duracion']:.3f} s\n"
            )

            fichero.write(
                "Puertos:\n"
            )

            for puerto in resultado["puertos"]:

                fichero.write(
                    f"  {puerto['puerto']} "
                    f"({puerto['servicio']}): "
                    f"{puerto['estado']} "
                    f"({puerto['duracion']:.3f} s)\n"
                )

            fichero.write(
                "\n-----------------------------\n\n"
            )


def generar_informe_json(
    resultados,
    estadisticas,
    archivo,
    fecha
):

    informe = {
        "fecha": fecha,
        "estadisticas": estadisticas,
        "equipos": resultados
    }

    with archivo.open(
        "w",
        encoding="utf-8"
    ) as fichero:

        json.dump(
            informe,
            fichero,
            indent=4,
            ensure_ascii=False
        )


def main():

    configurar_logging()

    argumentos = obtener_argumentos()

    archivo_inventario = (
        argumentos.inventario
    )

    logging.info(
        "Inventario utilizado: %s",
        archivo_inventario
    )

    try:

        equipos = cargar_inventario(
            archivo_inventario
        )

    except FileNotFoundError:

        logging.error(
            "No se encuentra "
            "el inventario: %s",
            archivo_inventario
        )

        print(
            "No se encuentra el inventario."
        )

        raise SystemExit(1)

    except ValueError as error:

        logging.error(
            "Inventario incorrecto: %s",
            error
        )

        print(
            f"Inventario incorrecto: {error}"
        )

        raise SystemExit(1)

    except OSError as error:

        logging.error(
            "Error leyendo "
            "el inventario: %s",
            error
        )

        print(
            f"Error leyendo el inventario: {error}"
        )

        raise SystemExit(1)

    equipos_validos = (
        obtener_equipos_validos(
            equipos
        )
    )

    resultados = diagnosticar_red(
        equipos_validos
    )

    estadisticas = calcular_estadisticas(
        resultados
    )

    mostrar_resultados(
        resultados
    )

    mostrar_estadisticas(
        estadisticas
    )

    DIRECTORIO_RESULTADOS.mkdir(
        parents=True,
        exist_ok=True
    )

    fecha = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    generar_informe_txt(
        resultados,
        estadisticas,
        ARCHIVO_TXT,
        fecha
    )

    generar_informe_json(
        resultados,
        estadisticas,
        ARCHIVO_JSON,
        fecha
    )

    logging.info(
        "Informe TXT generado: %s",
        ARCHIVO_TXT
    )

    logging.info(
        "Informe JSON generado: %s",
        ARCHIVO_JSON
    )

    logging.info(
        "Diagnóstico finalizado correctamente"
    )

    print(
        "\nInformes generados:"
    )

    print(
        ARCHIVO_TXT
    )

    print(
        ARCHIVO_JSON
    )

    print(
        "\nLog:"
    )

    print(
        ARCHIVO_LOG
    )


if __name__ == "__main__":

    main()
```

---

### 305. Preparar la prueba final

Para realizar una prueba controlada podemos utilizar:

```text
datos/equipos_final.csv
```

con:

```csv
nombre,host,puertos
ServidorLocal,127.0.0.1,8000;8001
Router,192.168.1.1,80;443
EquipoInexistente,equipo-inexistente.invalid,80;443
```

La dirección:

```text
192.168.1.1
```

debe adaptarse a un equipo autorizado de nuestra red.

---

### 306. Levantar el servidor de pruebas

En un terminal ejecuta:

```powershell
python -m http.server 8000
```

Esto nos proporciona un servicio TCP controlado en:

```text
127.0.0.1:8000
```

---

### 307. Ejecutar la prueba final

En otro terminal:

```powershell
python administrador_red.py --inventario ../datos/equipos_final.csv
```

Comprueba que el programa termina correctamente.

---

### 308. Verificar la salida por pantalla

Debemos comprobar:

```text
equipos analizados
```

```text
IP resuelta
```

```text
estado del ping
```

```text
puertos comprobados
```

```text
estadísticas
```

y las rutas de los archivos generados.

---

### 309. Verificar el TXT

Abre:

```text
resultados/informe_red.txt
```

Comprueba que contiene:

```text
fecha
resumen
equipos
hosts
direcciones IP
ping
puertos
estados
duraciones
```

---

### 310. Verificar el JSON

Abre:

```text
resultados/informe_red.json
```

Comprueba que la estructura general sea:

```json
{
    "fecha": "...",
    "estadisticas": {
    },
    "equipos": [
    ]
}
```

VS Code no debería indicar errores de sintaxis JSON.

---

### 311. Verificar `log.txt`

Abre:

```text
logs/log.txt
```

Comprueba que aparezcan:

```text
inicio
inventario
equipos procesados
ping
puertos
advertencias
errores
informes generados
finalización
```

---

### 312. Prueba 1: ejecución correcta

Con:

```text
python -m http.server 8000
```

activo, ejecuta el diagnóstico.

Comprueba que:

```text
127.0.0.1:8000
```

aparece como:

```text
ACCESIBLE
```

---

### 313. Prueba 2: servicio detenido

Detén el servidor mediante:

```text
Ctrl + C
```

Vuelve a ejecutar.

El puerto:

```text
8000
```

debería aparecer como:

```text
NO_ACCESIBLE
```

si ningún otro servicio lo está utilizando.

---

### 314. Prueba 3: inventario inexistente

Ejecuta:

```powershell
python administrador_red.py --inventario ../datos/no_existe.csv
```

Debemos obtener un mensaje controlado.

Después abre:

```text
log.txt
```

y comprueba que el error ha quedado registrado.

---

### 315. Prueba 4: puerto incorrecto

Añade temporalmente:

```csv
EquipoError,127.0.0.1,70000
```

El puerto:

```text
70000
```

no pertenece al intervalo válido:

```text
1 - 65535
```

Por tanto, el equipo deberá ser descartado por:

```python
validar_equipo()
```

---

### 316. Prueba 5: puerto no numérico

Prueba:

```csv
EquipoError,127.0.0.1,HTTP
```

La función:

```python
convertir_puertos()
```

no podrá convertir:

```text
HTTP
```

a entero.

El equipo no deberá llegar al diagnóstico de red.

---

### 317. Prueba 6: nombre no resoluble

Utiliza:

```csv
EquipoInexistente,equipo-inexistente.invalid,80
```

La resolución deberá producir:

```text
NO_RESUELTO
```

y el incidente deberá quedar registrado en:

```text
log.txt
```

---

### 318. Prueba 7: CSV incorrecto

Crea temporalmente:

```csv
nombre,direccion,servicio
Servidor,127.0.0.1,80
```

Faltan las columnas:

```text
host
puertos
```

El programa deberá detectar:

```text
El CSV no contiene las columnas necesarias.
```

---

### 319. Prueba 8: ejecución sin argumentos

Ejecuta:

```powershell
python administrador_red.py
```

`argparse` deberá informar de que:

```text
--inventario
```

es obligatorio.

---

### 320. Prueba 9: ayuda

Ejecuta:

```powershell
python administrador_red.py --help
```

Comprueba que aparece una explicación suficiente para ejecutar la aplicación.

---

### 321. Prueba 10: depuración completa

Utiliza:

```text
F5
```

con nuestro:

```text
launch.json
```

Coloca breakpoints en:

```python
main()
```

```python
diagnosticar_equipo()
```

```python
comprobar_ping()
```

```python
resolver_host()
```

```python
comprobar_puerto()
```

Recorre el programa utilizando:

```text
F10
F11
Shift + F11
```

y observa:

```text
Variables
Watch
Call Stack
Debug Console
```

---

### 322. Lista de comprobación final

Antes de considerar terminado el proyecto debemos comprobar:

```text
[ ] el programa arranca correctamente

[ ] argparse funciona

[ ] el CSV se carga correctamente

[ ] los datos se validan

[ ] los puertos están entre 1 y 65535

[ ] ping funciona

[ ] existe timeout

[ ] la resolución de host funciona

[ ] los puertos TCP se comprueban

[ ] los errores no detienen innecesariamente el diagnóstico

[ ] se genera informe TXT

[ ] se genera informe JSON

[ ] se calculan estadísticas

[ ] se crea log.txt

[ ] los errores quedan registrados

[ ] el programa puede depurarse desde VS Code
```

---

### 323. Arquitectura final

La aplicación completa tiene esta arquitectura:

```text
                   USUARIO
                      │
                      ▼
                   argparse
                      │
                      ▼
                 INVENTARIO CSV
                      │
                      ▼
                  validación
                      │
                      ▼
                 DIAGNÓSTICO
              ┌───────┼───────┐
              │       │       │
              ▼       ▼       ▼
            PING     DNS     TCP
              │       │       │
              └───────┼───────┘
                      │
                      ▼
                  RESULTADOS
                      │
             ┌────────┼────────┐
             │        │        │
             ▼        ▼        ▼
        estadísticas  TXT     JSON
             │
             └────────┬────────┘
                      │
                      ▼
                    LOG
```

---

### 324. Conceptos integrados en el proyecto

Este proyecto combina contenidos estudiados a lo largo del libro:

```text
variables
```

```text
condicionales
```

```text
bucles
```

```text
funciones
```

```text
listas
```

```text
diccionarios
```

```text
archivos
```

```text
CSV
```

```text
JSON
```

```text
pathlib
```

```text
subprocess
```

```text
excepciones
```

```text
argparse
```

```text
socket
```

```text
logging
```

```text
depuración con VS Code
```

El objetivo no ha sido estudiar estos elementos de forma aislada, sino combinarlos para resolver un problema práctico.

---

### 325. Competencias trabajadas

Al finalizar el proyecto el alumno debe ser capaz de comprender el flujo completo:

```text
entrada
   │
   ▼
validación
   │
   ▼
procesamiento
   │
   ▼
diagnóstico
   │
   ▼
resultados
   │
   ▼
persistencia
   │
   ▼
registro
```

También debe ser capaz de investigar un problema utilizando:

```text
breakpoints
```

```text
Variables
```

```text
Watch
```

```text
Call Stack
```

```text
Debug Console
```

y:

```text
logs
```

---

### 326. Propuesta de entrega del proyecto

El alumno deberá entregar la carpeta:

```text
capitulo8/
```

con al menos:

```text
capitulo8
│
├── datos
│   └── equipos.csv
│
├── logs
│   └── log.txt
│
├── programas
│   └── administrador_red.py
│
└── resultados
    ├── informe_red.txt
    └── informe_red.json
```

También deberá comprobar que el programa puede ejecutarse mediante:

```powershell
python administrador_red.py --inventario ../datos/equipos.csv
```

---

### 327. Criterios de evaluación propuestos

Podemos evaluar el proyecto sobre:

| Apartado | Peso |
|---|---:|
| Lectura y validación del CSV | 15 % |
| Uso correcto de funciones y estructuras de datos | 15 % |
| Diagnóstico mediante ping | 10 % |
| Resolución de host | 10 % |
| Comprobación TCP | 15 % |
| Gestión de errores | 10 % |
| Informes TXT y JSON | 10 % |
| Logging | 10 % |
| Organización y claridad del código | 5 % |
| **Total** | **100 %** |

---

### 328. Ampliaciones voluntarias

Una vez completada la versión obligatoria pueden plantearse ampliaciones.

Por ejemplo:

```text
permitir elegir el directorio de salida
```

```text
añadir más estadísticas
```

```text
crear un informe CSV
```

```text
mostrar solamente equipos con incidencias
```

```text
permitir configurar los timeouts mediante argparse
```

```text
crear pruebas automáticas para funciones que no dependan de la red
```

Estas ampliaciones no son necesarias para completar el proyecto principal.

---

### 329. Posible argumento `--timeout`

Como ampliación podríamos añadir:

```python
parser.add_argument(
    "--timeout",
    type=float,
    default=1,
    help=(
        "Timeout de las conexiones TCP "
        "en segundos"
    )
)
```

Entonces podríamos ejecutar:

```powershell
python administrador_red.py --inventario ../datos/equipos.csv --timeout 2
```

Esta ampliación obligaría a pasar el valor hasta las funciones de diagnóstico.

---

### 330. Posible argumento `--salida`

También podríamos permitir:

```powershell
python administrador_red.py --inventario ../datos/equipos.csv --salida ../mis_resultados
```

De esta forma el usuario decidiría dónde almacenar los informes.

Esta modificación es una buena práctica adicional para alumnos que terminen antes.

---

### 331. Posible modo silencioso

Otra ampliación sería:

```text
--quiet
```

para evitar mostrar todos los resultados por pantalla.

El programa seguiría generando:

```text
TXT
JSON
log.txt
```

pero mostraría menos información en la consola.

Esto permitiría seguir evolucionando la herramienta sin modificar su núcleo.

---

### 332. Separar el programa en módulos

Nuestro proyecto utiliza actualmente un único archivo:

```text
administrador_red.py
```

Esto es adecuado para el alcance del curso.

En un proyecto mayor podríamos separar:

```text
inventario.py
red.py
informes.py
configuracion.py
main.py
```

Por ejemplo:

```text
programas/
│
├── main.py
├── inventario.py
├── diagnostico.py
└── informes.py
```

No realizaremos esta modificación ahora porque introduciría complejidad adicional que no necesitamos para cumplir los objetivos del proyecto.

---

### 333. Importancia de las funciones pequeñas

Durante el proyecto hemos evitado crear una única función que haga todo.

En su lugar tenemos funciones como:

```python
cargar_inventario()
```

```python
validar_equipo()
```

```python
comprobar_ping()
```

```python
resolver_host()
```

```python
comprobar_puerto()
```

```python
calcular_estadisticas()
```

```python
generar_informe_txt()
```

```python
generar_informe_json()
```

Cada una tiene una responsabilidad concreta.

Esto facilita:

```text
comprender
depurar
probar
modificar
reutilizar
```

el código.

---

### 334. Importancia de la gestión de errores

Un programa de administración no debería terminar inesperadamente ante cualquier problema.

Durante el proyecto hemos gestionado situaciones como:

```text
archivo inexistente
```

```text
CSV incorrecto
```

```text
puerto incorrecto
```

```text
problema de ping
```

```text
host no resuelto
```

```text
error de socket
```

El objetivo no consiste en ocultar los errores.

Consiste en:

```text
detectarlos
     │
     ▼
clasificarlos
     │
     ▼
registrarlos
     │
     ▼
actuar correctamente
```

---

### 335. Importancia del depurador

Cuando el programa no funciona como esperamos no debemos limitarnos a modificar código al azar.

Podemos utilizar:

```text
breakpoints
```

para detenerlo.

Después:

```text
Variables
```

para inspeccionar los datos.

También:

```text
Watch
```

para seguir expresiones concretas.

Con:

```text
Call Stack
```

podemos entender qué funciones nos han llevado al punto actual.

Y mediante:

```text
Debug Console
```

podemos evaluar expresiones mientras el programa está detenido.

---

### 336. Depuración y logging se complementan

El depurador permite investigar:

```text
qué está ocurriendo ahora
```

durante una ejecución controlada.

El log permite investigar:

```text
qué ocurrió anteriormente
```

Por tanto:

```text
DEBUGGER
   │
   └── investigación interactiva


LOGGING
   │
   └── registro histórico
```

Ambas técnicas forman parte de una forma profesional de trabajar con programas.

---

### 337. Resultado final del proyecto

Al finalizar disponemos de una aplicación capaz de:

```text
leer un inventario CSV
        │
        ▼
validar los equipos
        │
        ▼
comprobar conectividad
        │
        ▼
resolver nombres
        │
        ▼
comprobar puertos TCP
        │
        ▼
generar estadísticas
        │
        ▼
crear informe TXT
        │
        ▼
crear informe JSON
        │
        ▼
registrar incidencias
```

Todo ello puede iniciarse desde una única orden:

```powershell
python administrador_red.py --inventario ../datos/equipos.csv
```

---

### 338. Resultado de aprendizaje del proyecto

El objetivo final no es únicamente disponer de:

```text
administrador_red.py
```

El objetivo es comprender cómo podemos utilizar Python para automatizar tareas reales de administración.

Hemos pasado de ejecutar manualmente comandos como:

```powershell
ping 192.168.1.10
```

a trabajar con un inventario completo:

```text
CSV
 │
 ▼
PYTHON
 │
 ▼
DIAGNÓSTICO AUTOMÁTICO
 │
 ▼
INFORMES
```

Este cambio representa una de las principales ventajas del scripting aplicado a sistemas y redes.

---

### 339. Resumen del proyecto final

El proyecto ha integrado los principales contenidos trabajados durante el curso.

La entrada de información se realiza mediante:

```text
CSV
```

La aplicación recibe parámetros mediante:

```python
argparse
```

La gestión de rutas se realiza mediante:

```python
pathlib
```

La ejecución de comandos utiliza:

```python
subprocess
```

El diagnóstico TCP y la resolución utilizan:

```python
socket
```

La gestión de errores utiliza:

```python
try
except
```

Los informes estructurados utilizan:

```python
json
```

Y el registro de actividad utiliza:

```python
logging
```

Todo ello se integra dentro de una aplicación organizada mediante funciones y depurable desde VS Code.

---

### 340. Cierre del Capítulo 8

Con este capítulo hemos construido una aplicación completa partiendo de un problema real:

> Automatizar el diagnóstico básico de un conjunto de equipos de red y generar un informe de los resultados.

El programa final recibe:

```text
equipos.csv
```

y produce:

```text
informe_red.txt
```

```text
informe_red.json
```

y:

```text
log.txt
```

Además, puede analizarse mediante las herramientas profesionales de depuración de VS Code estudiadas anteriormente.

!!! success "Proyecto final completado"

    El alumno dispone ahora de una herramienta funcional de diagnóstico básico de red desarrollada íntegramente en Python.

    El proyecto integra gestión de archivos, ejecución de comandos, tratamiento de errores, automatización, redes, argumentos, generación de informes, logging y depuración.

---

### 341. Cierre del Módulo 3

En este módulo hemos trabajado dos elementos fundamentales.

Primero hemos aprendido a utilizar las herramientas de:

```text
depuración de VS Code
```

para investigar el comportamiento de nuestros programas.

Después hemos aplicado los conocimientos adquiridos durante el curso en un:

```text
proyecto final integrado
```

El resultado ha sido una aplicación que combina scripting de sistemas, automatización y diagnóstico básico de red.

---

### 342. Cierre del libro

A lo largo de este libro hemos avanzado desde scripts sencillos hasta construir una herramienta completa.

Hemos aprendido a utilizar Python para:

```text
trabajar con archivos
```

```text
ejecutar comandos del sistema
```

```text
automatizar tareas repetitivas
```

```text
gestionar errores
```

```text
trabajar con HTTP y APIs
```

```text
realizar diagnósticos básicos de red
```

```text
depurar programas profesionalmente
```

y finalmente:

```text
integrar todos estos conocimientos
en un proyecto completo
```

El siguiente paso consiste en aplicar estas técnicas a nuevos problemas.

Python puede utilizarse para automatizar muchas tareas habituales de sistemas y redes:

```text
inventarios
monitorización
informes
procesamiento de logs
comprobaciones de servicios
automatización de configuraciones
consumo de APIs
```

La clave está en aprender a transformar una tarea manual y repetitiva en:

```text
problema
   │
   ▼
algoritmo
   │
   ▼
script
   │
   ▼
automatización
```

!!! success "Libro completado"

    Hemos llegado al final del recorrido formativo.

    El alumno no solamente ha aprendido instrucciones de Python, sino que ha utilizado el lenguaje como herramienta para resolver problemas relacionados con sistemas y redes.