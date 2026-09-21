# Capítulo 6. Diagnóstico básico de red

En los capítulos anteriores hemos utilizado Python para realizar tareas de administración y comunicarnos con servicios web.

Hemos trabajado con:

```text
subprocess
requests
HTTP
APIs
JSON
```

Ahora vamos a trabajar a un nivel más cercano a la comunicación de red.

Utilizaremos el módulo:

```python
socket
```

que forma parte de la biblioteca estándar de Python.

Con él podremos desarrollar herramientas capaces de:

```text
comprobar puertos TCP
detectar servicios accesibles
realizar diagnósticos básicos
resolver nombres DNS
```

Nuestro objetivo no será construir herramientas complejas de análisis de redes.

Utilizaremos `socket` para comprender cómo puede Python comprobar directamente la conectividad con determinados servicios de red.

---

## 1. Introducción a los sockets y puertos TCP

Cuando dos aplicaciones se comunican mediante una red necesitamos identificar:

```text
equipo
+
servicio
```

La dirección IP identifica el equipo.

El puerto permite identificar un servicio o aplicación concreta.

Podemos representarlo así:

```text
192.168.1.20
     │
     ├── puerto 22
     │
     ├── puerto 80
     │
     └── puerto 443
```

Por tanto, para comprobar un servicio no siempre es suficiente saber si el equipo está conectado a la red.

También puede ser necesario comprobar si podemos establecer una conexión con el **puerto utilizado por ese servicio**.

---

### 2. Recordatorio: dirección IP

Una dirección IPv4 puede tener este aspecto:

```text
192.168.1.20
```

La dirección identifica una interfaz de red dentro de una red IP.

En capítulos anteriores ya hemos utilizado direcciones IP para realizar operaciones como:

```powershell
ping 192.168.1.20
```

Desde Python ejecutábamos el mismo comando mediante:

```python
subprocess.run()
```

Por ejemplo:

```python
resultado = subprocess.run(
    [
        "ping",
        "-n",
        "1",
        "192.168.1.20"
    ],
    capture_output=True,
    text=True,
    timeout=10
)
```

Pero `ping` y una conexión TCP no comprueban exactamente lo mismo.

---

### 3. ¿Qué es un puerto?

Un ordenador puede ejecutar simultáneamente muchos servicios de red.

Necesitamos alguna forma de distinguirlos.

Para ello se utilizan los:

```text
puertos
```

Un puerto se identifica mediante un número.

Por ejemplo:

```text
80
443
22
```

Podemos representar una comunicación como:

```text
        EQUIPO
    192.168.1.20
          │
    ┌─────┼─────┐
    │     │     │
    ▼     ▼     ▼
   22    80    443
```

La dirección IP nos permite localizar el equipo.

El puerto nos permite dirigir la comunicación hacia un determinado servicio.

---

### 4. Rango de puertos

Los números de puerto TCP y UDP pueden estar comprendidos entre:

```text
0
```

y:

```text
65535
```

Por tanto, un puerto válido deberá cumplir:

```text
0 <= puerto <= 65535
```

En nuestras herramientas validaremos normalmente los valores recibidos antes de intentar utilizarlos.

---

### 5. Algunos puertos conocidos

Existen determinados números de puerto asociados habitualmente a servicios conocidos.

Por ejemplo:

| Puerto | Servicio habitual |
|---:|---|
| 22 | SSH |
| 53 | DNS |
| 80 | HTTP |
| 443 | HTTPS |

!!! note "Puerto y servicio"

    Un número de puerto no garantiza por sí mismo qué aplicación se está ejecutando.

    Estos números corresponden a asociaciones habituales.

    Un servicio puede configurarse para utilizar otro puerto.

---

### 6. IP y puerto forman un destino

Para intentar establecer una conexión TCP necesitaremos dos datos:

```text
dirección IP o nombre
```

y:

```text
puerto
```

Por ejemplo:

```text
192.168.1.20:80
```

Podemos interpretarlo como:

```text
192.168.1.20
      │
      └── equipo

80
 │
 └── puerto
```

Otro ejemplo:

```text
192.168.1.20:22
```

indica el mismo equipo, pero un puerto diferente.

---

### 7. ¿Qué es TCP?

TCP significa:

```text
Transmission Control Protocol
```

Es un protocolo de transporte orientado a conexión.

De forma simplificada, antes de intercambiar datos se establece una conexión entre los extremos.

Podemos representarlo así:

```text
CLIENTE
   │
   │ intento de conexión
   ▼
SERVIDOR
   │
   │ conexión establecida
   ▼
CLIENTE
```

En este capítulo utilizaremos esta característica para comprobar si podemos establecer una conexión TCP con un determinado puerto.

---

### 8. ¿Qué es un socket?

Un **socket** es un mecanismo que permite a un programa comunicarse a través de una red.

Python incluye el módulo:

```python
socket
```

Podemos importarlo mediante:

```python
import socket
```

Con él podremos crear un socket y utilizarlo para intentar conectarnos a:

```text
host
+
puerto
```

Por ejemplo:

```text
example.com
+
443
```

---

### 9. Cliente y servidor

En nuestras primeras prácticas Python actuará como:

```text
CLIENTE
```

Nuestro programa intentará conectarse a un servicio que está actuando como:

```text
SERVIDOR
```

El modelo será:

```text
PROGRAMA PYTHON
     cliente
        │
        │ conexión TCP
        ▼
      SERVIDOR
        │
        ▼
      PUERTO
```

Por ejemplo:

```text
Python
   │
   │ TCP
   ▼
example.com
   │
   ▼
puerto 443
```

---

### 10. `ping` frente a comprobación de puerto

Esta diferencia es especialmente importante.

Cuando utilizamos:

```text
ping
```

estamos realizando una prueba basada normalmente en ICMP.

Cuando intentamos conectarnos mediante TCP a un puerto concreto estamos comprobando otra cosa.

```text
PING
 │
 ▼
¿obtenemos respuesta ICMP?


SOCKET TCP
 │
 ▼
¿podemos establecer una
conexión TCP con ese puerto?
```

Por tanto:

```text
equipo accesible
```

no significa necesariamente:

```text
servicio disponible
```

---

### 11. Ejemplo de la diferencia

Imaginemos un servidor:

```text
192.168.1.50
```

Podría responder correctamente:

```powershell
ping 192.168.1.50
```

pero su servidor web podría estar detenido.

Tendríamos conceptualmente:

```text
PING
192.168.1.50
     │
     └── responde


TCP
192.168.1.50:80
     │
     └── no acepta conexión
```

También puede ocurrir lo contrario.

Un equipo puede tener restringidas las respuestas ICMP y, sin embargo, ofrecer un servicio TCP accesible.

!!! tip "Diagnóstico"

    Para diagnosticar correctamente una red debemos distinguir entre:

    ```text
    conectividad con el equipo
    ```

    y:

    ```text
    conectividad con un servicio
    ```

---

### 12. Crear nuestra estructura de prácticas

Crearemos:

```text
practicas/
└── capitulo6/
    ├── datos/
    ├── logs/
    ├── programas/
    └── resultados/
```

Nuestros programas estarán en:

```text
practicas/capitulo6/programas/
```

Durante el capítulo utilizaremos los demás directorios para almacenar datos, logs y resultados.

---

### 13. Nuestro primer programa con `socket`

Dentro de:

```text
practicas/capitulo6/programas/
```

crea:

```text
primer_socket.py
```

Escribe:

```python
import socket


cliente = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)


print(
    "Socket creado correctamente."
)


cliente.close()
```

Ejecuta:

```powershell
python primer_socket.py
```

Obtendremos:

```text
Socket creado correctamente.
```

Aunque todavía no hemos realizado ninguna conexión, acabamos de crear nuestro primer socket.

---

### 14. Analizar `socket.socket()`

La instrucción:

```python
socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
```

contiene dos elementos importantes.

El primero es:

```python
socket.AF_INET
```

En nuestro ejemplo indica que trabajaremos con direcciones:

```text
IPv4
```

El segundo es:

```python
socket.SOCK_STREAM
```

Indica que utilizaremos un socket orientado a flujo, asociado normalmente con:

```text
TCP
```

Por tanto:

```python
socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
```

puede interpretarse en esta práctica como:

```text
socket IPv4
+
TCP
```

---

### 15. Cerrar el socket

Después de utilizar un socket debemos cerrarlo.

Podemos hacerlo mediante:

```python
cliente.close()
```

El esquema básico sería:

```text
crear socket
     │
     ▼
utilizar socket
     │
     ▼
cerrar socket
```

Más adelante veremos una forma más cómoda de gestionar automáticamente su cierre.

---

### 16. Intentar nuestra primera conexión

Vamos a intentar establecer una conexión TCP.

Crea:

```text
conexion_tcp.py
```

Escribe:

```python
import socket


host = "example.com"
puerto = 443


cliente = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)


cliente.settimeout(
    5
)


resultado = cliente.connect_ex(
    (
        host,
        puerto
    )
)


print(
    f"Resultado: {resultado}"
)


cliente.close()
```

Ejecuta:

```powershell
python conexion_tcp.py
```

El programa intentará establecer una conexión TCP con:

```text
example.com:443
```

---

### 17. El método `connect_ex()`

Hemos utilizado:

```python
cliente.connect_ex(
    (
        host,
        puerto
    )
)
```

Observa que el destino se proporciona mediante:

```python
(
    host,
    puerto
)
```

Es decir, una tupla con:

```text
host
puerto
```

Por ejemplo:

```python
(
    "example.com",
    443
)
```

---

### 18. Interpretar el resultado

`connect_ex()` devuelve un código.

Si devuelve:

```text
0
```

la conexión se ha podido establecer correctamente.

Por tanto podemos escribir:

```python
if resultado == 0:

    print(
        "Puerto accesible."
    )

else:

    print(
        "No se ha podido "
        "establecer la conexión."
    )
```

Programa:

```python
import socket


host = "example.com"
puerto = 443


cliente = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

cliente.settimeout(
    5
)


resultado = cliente.connect_ex(
    (
        host,
        puerto
    )
)


if resultado == 0:

    print(
        f"{host}:{puerto} "
        f"ACCESIBLE"
    )

else:

    print(
        f"{host}:{puerto} "
        f"NO ACCESIBLE"
    )


cliente.close()
```

---

### 19. ¿Significa que el puerto está abierto?

En herramientas sencillas es habitual describir un resultado correcto como:

```text
puerto abierto
```

Sin embargo, conviene comprender exactamente qué hemos comprobado.

Si:

```python
connect_ex()
```

devuelve:

```text
0
```

significa que hemos podido establecer una conexión TCP con ese destino.

Por eso en nuestras primeras herramientas utilizaremos preferentemente:

```text
ACCESIBLE
```

y:

```text
NO ACCESIBLE
```

Esto describe mejor lo que realmente ha comprobado nuestro programa.

---

### 20. Utilizar un tiempo de espera

Hemos añadido:

```python
cliente.settimeout(
    5
)
```

Esto establece un tiempo máximo para determinadas operaciones del socket.

Sin un tiempo de espera, una operación de red podría tardar demasiado dependiendo de las condiciones de la red.

El patrón es parecido al utilizado anteriormente con:

```python
requests.get(
    url,
    timeout=10
)
```

y:

```python
subprocess.run(
    comando,
    timeout=10
)
```

Podemos establecer una regla general:

```text
OPERACIÓN DE RED
       │
       ▼
establecer timeout
```

---

### 21. Utilizar `with`

Python permite utilizar un socket mediante:

```python
with
```

Por ejemplo:

```python
with socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
) as cliente:

    cliente.settimeout(
        5
    )

    resultado = cliente.connect_ex(
        (
            host,
            puerto
        )
    )
```

Cuando termina el bloque:

```python
with
```

el socket se cierra automáticamente.

Esto evita tener que escribir:

```python
cliente.close()
```

manualmente.

---

### 22. Reescribir el programa con `with`

Modifica:

```text
conexion_tcp.py
```

para utilizar:

```python
import socket


host = "example.com"
puerto = 443


with socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
) as cliente:

    cliente.settimeout(
        5
    )

    resultado = cliente.connect_ex(
        (
            host,
            puerto
        )
    )


if resultado == 0:

    print(
        f"{host}:{puerto} "
        f"ACCESIBLE"
    )

else:

    print(
        f"{host}:{puerto} "
        f"NO ACCESIBLE"
    )
```

Esta será la estructura que utilizaremos a partir de ahora.

---

### 23. Crear una función reutilizable

Vamos a encapsular la operación.

Crea:

```text
comprobar_puerto.py
```

Escribe:

```python
import socket


def comprobar_puerto(
    host,
    puerto
):

    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    ) as cliente:

        cliente.settimeout(
            3
        )

        resultado = (
            cliente.connect_ex(
                (
                    host,
                    puerto
                )
            )
        )

    return resultado == 0
```

Ahora podemos utilizar:

```python
if comprobar_puerto(
    "example.com",
    443
):

    print(
        "Puerto accesible."
    )

else:

    print(
        "Puerto no accesible."
    )
```

La función devuelve:

```python
True
```

si se puede establecer la conexión y:

```python
False
```

en caso contrario.

---

### 24. Ventajas de utilizar una función

Ahora hemos separado:

```text
COMPROBACIÓN
      │
      ▼
comprobar_puerto()
```

de:

```text
PRESENTACIÓN
      │
      ▼
print()
```

Podemos reutilizar la función con diferentes destinos:

```python
comprobar_puerto(
    "example.com",
    443
)
```

```python
comprobar_puerto(
    "192.168.1.20",
    80
)
```

```python
comprobar_puerto(
    "192.168.1.30",
    22
)
```

---

### 25. Recibir host y puerto mediante `input()`

Podemos hacer una primera versión interactiva:

```python
import socket


host = input(
    "Host: "
)

puerto = int(
    input(
        "Puerto: "
    )
)
```

Después utilizaremos:

```python
comprobar_puerto(
    host,
    puerto
)
```

Sin embargo, ya conocemos una herramienta más adecuada para scripts reutilizables:

```text
argparse
```

---

### 26. Comprobador mediante `argparse`

Crea:

```text
puerto_argparse.py
```

Escribe:

```python
import argparse
import socket


def comprobar_puerto(
    host,
    puerto
):

    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    ) as cliente:

        cliente.settimeout(
            3
        )

        resultado = (
            cliente.connect_ex(
                (
                    host,
                    puerto
                )
            )
        )

    return resultado == 0


parser = argparse.ArgumentParser(
    description=(
        "Comprueba la conectividad "
        "TCP con un puerto."
    )
)


parser.add_argument(
    "host",
    help=(
        "Dirección IP o nombre "
        "del equipo"
    )
)


parser.add_argument(
    "puerto",
    type=int,
    help="Puerto TCP"
)


args = parser.parse_args()


if not 0 <= args.puerto <= 65535:

    parser.error(
        "El puerto debe estar "
        "entre 0 y 65535."
    )


if comprobar_puerto(
    args.host,
    args.puerto
):

    print(
        f"{args.host}:"
        f"{args.puerto} "
        f"ACCESIBLE"
    )

else:

    print(
        f"{args.host}:"
        f"{args.puerto} "
        f"NO ACCESIBLE"
    )
```

---

### 27. Probar nuestro comprobador

Podemos probar:

```powershell
python puerto_argparse.py example.com 443
```

Si podemos establecer la conexión obtendremos:

```text
example.com:443 ACCESIBLE
```

Podemos probar otro puerto:

```powershell
python puerto_argparse.py example.com 80
```

También podemos utilizar equipos de nuestro laboratorio cuando tengamos autorización para realizar las pruebas.

!!! warning "Realiza pruebas únicamente sobre sistemas autorizados"

    Las herramientas de diagnóstico deben utilizarse únicamente sobre:

    - Tus propios equipos.
    - Los equipos del laboratorio.
    - Sistemas para los que tengas autorización.

    En las prácticas del curso utilizaremos servicios públicos destinados a pruebas o equipos de nuestro entorno docente.

---

### 28. Validar el puerto

Gracias a:

```python
type=int
```

`argparse` ya comprueba que el puerto pueda convertirse en un número entero.

Si ejecutamos:

```powershell
python puerto_argparse.py example.com hola
```

`argparse` mostrará un error.

Además hemos añadido:

```python
if not 0 <= args.puerto <= 65535:
```

para comprobar el rango.

Por tanto tenemos dos niveles de validación:

```text
¿es un entero?
      │
      ▼
   argparse
      │
      ▼
¿está entre 0 y 65535?
      │
      ▼
validación propia
```

---

### 29. ¿Qué errores pueden producirse?

Hasta ahora hemos supuesto que el host recibido es válido.

Pero pueden producirse situaciones como:

```text
nombre inexistente
problema de resolución DNS
dirección incorrecta
problema de red
timeout
```

Por ejemplo:

```powershell
python puerto_argparse.py equipo-que-no-existe.local 80
```

puede producir un error relacionado con la resolución del nombre.

Necesitamos recuperar lo aprendido sobre excepciones.

---

### 30. `socket.gaierror`

Una excepción especialmente importante es:

```python
socket.gaierror
```

Puede producirse cuando existe un problema al resolver un nombre.

Por ejemplo:

```python
try:

    resultado = cliente.connect_ex(
        (
            host,
            puerto
        )
    )

except socket.gaierror:

    print(
        "ERROR: no se ha podido "
        "resolver el nombre."
    )
```

Más adelante estudiaremos específicamente la resolución DNS.

---

### 31. `socket.timeout`

También podemos controlar:

```python
socket.timeout
```

Por ejemplo:

```python
except socket.timeout:

    print(
        "ERROR: tiempo de "
        "espera agotado."
    )
```

Podemos controlar otros problemas relacionados con sockets mediante:

```python
OSError
```

---

### 32. Crear una función más robusta

Podemos modificar nuestra función:

```python
def comprobar_puerto(
    host,
    puerto
):

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as cliente:

            cliente.settimeout(
                3
            )

            resultado = (
                cliente.connect_ex(
                    (
                        host,
                        puerto
                    )
                )
            )

    except socket.gaierror:

        print(
            "ERROR: no se ha podido "
            "resolver el host."
        )

        return False

    except socket.timeout:

        print(
            "ERROR: tiempo de "
            "espera agotado."
        )

        return False

    except OSError as error:

        print(
            f"ERROR de red: "
            f"{error}"
        )

        return False

    else:

        return resultado == 0
```

Ahora nuestra función está preparada para controlar algunos de los problemas más habituales.

---

### 33. Un detalle importante sobre `False`

Nuestra función devuelve:

```python
False
```

tanto cuando:

```text
no se establece la conexión
```

como cuando:

```text
se produce determinado error
```

Para una herramienta sencilla puede ser suficiente.

Sin embargo, conceptualmente no son exactamente lo mismo.

```text
NO ACCESIBLE
```

puede significar que hemos realizado la prueba pero no hemos conseguido establecer la conexión.

Mientras que:

```text
ERROR
```

puede significar que ni siquiera hemos podido realizar correctamente la comprobación.

Más adelante mejoraremos esta situación.

---

### 34. Devolver diferentes estados

Podemos hacer que la función devuelva textos diferentes.

Por ejemplo:

```python
def comprobar_puerto(
    host,
    puerto
):

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as cliente:

            cliente.settimeout(
                3
            )

            resultado = (
                cliente.connect_ex(
                    (
                        host,
                        puerto
                    )
                )
            )

    except socket.gaierror:

        return "ERROR_DNS"

    except socket.timeout:

        return "TIMEOUT"

    except OSError:

        return "ERROR"

    else:

        if resultado == 0:

            return "ACCESIBLE"

        return "NO_ACCESIBLE"
```

Después:

```python
estado = comprobar_puerto(
    args.host,
    args.puerto
)


print(
    f"Estado: {estado}"
)
```

Ahora distinguimos diferentes resultados.

---

### 35. Añadir `logging`

Podemos registrar las comprobaciones.

Añade:

```python
import logging
```

Configura:

```python
logging.basicConfig(
    filename="puertos.log",
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S"
)
```

Antes de comprobar:

```python
logging.info(
    f"Comprobando "
    f"{args.host}:{args.puerto}"
)
```

Si el puerto resulta accesible:

```python
logging.info(
    f"{args.host}:{args.puerto} "
    f"ACCESIBLE"
)
```

Si no:

```python
logging.warning(
    f"{args.host}:{args.puerto} "
    f"NO ACCESIBLE"
)
```

---

### 36. Comprobador completo de un puerto

Crea:

```text
diagnostico_puerto.py
```

Escribe:

```python
import argparse
import logging
import socket

from pathlib import Path


DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)

DIRECTORIO_CAPITULO = (
    DIRECTORIO_PROGRAMA.parent
)

DIRECTORIO_LOGS = (
    DIRECTORIO_CAPITULO
    / "logs"
)


DIRECTORIO_LOGS.mkdir(
    parents=True,
    exist_ok=True
)


ARCHIVO_LOG = (
    DIRECTORIO_LOGS
    / "puertos.log"
)


logging.basicConfig(
    filename=ARCHIVO_LOG,
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S"
)


def comprobar_puerto(
    host,
    puerto
):

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as cliente:

            cliente.settimeout(
                3
            )

            resultado = (
                cliente.connect_ex(
                    (
                        host,
                        puerto
                    )
                )
            )

    except socket.gaierror:

        logging.error(
            f"No se puede resolver "
            f"{host}"
        )

        return "ERROR_DNS"

    except socket.timeout:

        logging.warning(
            f"Timeout en "
            f"{host}:{puerto}"
        )

        return "TIMEOUT"

    except OSError as error:

        logging.error(
            f"Error en "
            f"{host}:{puerto}: "
            f"{error}"
        )

        return "ERROR"

    else:

        if resultado == 0:

            logging.info(
                f"{host}:{puerto} "
                f"ACCESIBLE"
            )

            return "ACCESIBLE"

        logging.warning(
            f"{host}:{puerto} "
            f"NO ACCESIBLE"
        )

        return "NO_ACCESIBLE"


parser = argparse.ArgumentParser(
    description=(
        "Comprueba la conectividad "
        "TCP con un puerto."
    )
)


parser.add_argument(
    "host",
    help=(
        "Dirección IP o nombre "
        "del equipo"
    )
)


parser.add_argument(
    "puerto",
    type=int,
    help="Puerto TCP"
)


args = parser.parse_args()


if not 0 <= args.puerto <= 65535:

    parser.error(
        "El puerto debe estar "
        "entre 0 y 65535."
    )


print()
print("DIAGNÓSTICO TCP")
print("===============")
print()

print(
    f"Host: {args.host}"
)

print(
    f"Puerto: {args.puerto}"
)


estado = comprobar_puerto(
    args.host,
    args.puerto
)


print(
    f"Estado: {estado}"
)
```

---

### 37. Probar diferentes situaciones

Podemos realizar varias pruebas.

#### Servicio accesible

```powershell
python diagnostico_puerto.py example.com 443
```

Podemos obtener:

```text
DIAGNÓSTICO TCP
===============

Host: example.com
Puerto: 443
Estado: ACCESIBLE
```

#### Puerto diferente

```powershell
python diagnostico_puerto.py example.com 80
```

#### Nombre incorrecto

```powershell
python diagnostico_puerto.py nombre-que-no-existe.invalid 80
```

Podremos obtener:

```text
Estado: ERROR_DNS
```

También podemos comprobar:

```text
logs/puertos.log
```

para consultar el historial de las operaciones.

---

### 38. Práctica guiada

Crea:

```text
comprobar_servicio.py
```

El programa deberá recibir:

```text
host
puerto
```

mediante `argparse`.

Por ejemplo:

```powershell
python comprobar_servicio.py example.com 443
```

Deberá mostrar:

```text
COMPROBACIÓN DE SERVICIO
========================

Host: example.com
Puerto: 443
Protocolo: TCP
Estado: ACCESIBLE
```

El programa deberá incluir:

```text
socket
argparse
timeout
try / except
logging
```

y validar que el puerto se encuentre en el rango correcto.

---

### 39. Práctica propuesta: varios servicios conocidos

Crea:

```text
servicios_conocidos.py
```

Define:

```python
servicios = [
    ("example.com", 80),
    ("example.com", 443)
]
```

Después recorre:

```python
for host, puerto in servicios:
```

y utiliza:

```python
comprobar_puerto(
    host,
    puerto
)
```

El resultado podría ser:

```text
COMPROBACIÓN TCP
================

example.com:80
ACCESIBLE

example.com:443
ACCESIBLE
```

Esta práctica prepara el siguiente paso: realizar varias comprobaciones automáticamente.

---

### 40. Lo que todavía no estamos haciendo

Nuestra herramienta actual comprueba:

```text
un host
+
un puerto
```

Todavía no estamos recorriendo automáticamente rangos de puertos.

Por ejemplo:

```text
20
21
22
23
...
```

Ese será el siguiente paso.

Partiremos de:

```python
comprobar_puerto(
    host,
    puerto
)
```

y utilizaremos:

```python
for
```

y:

```python
range()
```

para automatizar las comprobaciones.

!!! warning "Escaneo autorizado"

    Un programa que prueba múltiples puertos debe utilizarse únicamente sobre sistemas propios o sobre redes y equipos para los que exista autorización.

    En las prácticas trabajaremos con rangos pequeños y entornos controlados.

---

## Resumen

En esta primera parte del capítulo hemos aprendido que una dirección IP identifica un equipo o interfaz, mientras que un puerto permite dirigir una comunicación hacia un determinado servicio.

Podemos representar un destino como:

```text
HOST:PUERTO
```

por ejemplo:

```text
192.168.1.20:80
```

Hemos introducido:

```python
socket
```

y creado sockets TCP/IPv4 mediante:

```python
socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
```

Para comprobar una conexión hemos utilizado:

```python
connect_ex()
```

y aprendido que:

```text
resultado == 0
```

indica que se ha podido establecer la conexión TCP.

También hemos utilizado:

```python
settimeout()
```

para evitar esperas excesivas.

Hemos diferenciado:

```text
ping
```

de:

```text
conexión TCP a un puerto
```

y hemos integrado los nuevos conocimientos con:

```text
argparse
+
excepciones
+
logging
+
socket
```

Nuestro patrón básico es ahora:

```text
       HOST
        +
      PUERTO
        │
        ▼
 crear socket
        │
        ▼
   establecer
    timeout
        │
        ▼
  connect_ex()
        │
   ┌────┴────┐
   │         │
   ▼         ▼
conexión   sin conexión
   │         │
   ▼         ▼
ACCESIBLE  NO ACCESIBLE
        │
        ▼
       log
```

En la siguiente parte utilizaremos esta función para construir un **comprobador de varios puertos y un pequeño escáner TCP**, utilizando `range()`, listas, contadores, argumentos y generación de informes.

---

## 41. Comprobación de varios puertos y escáner TCP básico

En la primera parte del capítulo hemos creado una función capaz de comprobar un único puerto:

```python
comprobar_puerto(
    host,
    puerto
)
```

Por ejemplo:

```text
example.com:443
```

Ahora vamos a automatizar esta operación.

Nuestro objetivo será pasar de:

```text
un host
+
un puerto
```

a:

```text
un host
+
varios puertos
```

y posteriormente:

```text
un host
+
un rango de puertos
```

El proceso será:

```text
      HOST
       │
       ▼
lista o rango
 de puertos
       │
       ▼
      for
       │
       ▼
comprobar_puerto()
       │
       ▼
    resultado
       │
       ▼
mostrar / guardar
```

!!! warning "Uso autorizado"

    Las herramientas desarrolladas en esta práctica deben utilizarse únicamente sobre:

    - Equipos propios.
    - Equipos del laboratorio.
    - Máquinas virtuales preparadas para las prácticas.
    - Sistemas para los que tengamos autorización.

    El objetivo es aprender programación y diagnóstico básico de red.

---

### 42. Comprobar una lista de puertos

No siempre necesitamos comprobar todos los puertos de un rango.

Podemos comenzar utilizando una lista:

```python
puertos = [
    22,
    80,
    443
]
```

Después podemos recorrerla:

```python
for puerto in puertos:

    print(
        puerto
    )
```

Obtendremos:

```text
22
80
443
```

El siguiente paso consiste en realizar una comprobación TCP para cada uno.

---

### 43. Primer comprobador multipuerto

Crea:

```text
practicas/capitulo6/programas/
varios_puertos.py
```

Escribe:

```python
import socket


def comprobar_puerto(
    host,
    puerto
):

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as cliente:

            cliente.settimeout(
                2
            )

            resultado = (
                cliente.connect_ex(
                    (
                        host,
                        puerto
                    )
                )
            )

    except socket.gaierror:

        return "ERROR_DNS"

    except socket.timeout:

        return "TIMEOUT"

    except OSError:

        return "ERROR"

    else:

        if resultado == 0:

            return "ACCESIBLE"

        return "NO_ACCESIBLE"


host = "example.com"


puertos = [
    22,
    80,
    443
]


for puerto in puertos:

    estado = comprobar_puerto(
        host,
        puerto
    )

    print(
        f"{host}:{puerto} "
        f"{estado}"
    )
```

Ejecuta:

```powershell
python varios_puertos.py
```

El programa realizará una comprobación independiente para cada puerto.

---

### 44. Qué ocurre dentro del `for`

La parte fundamental es:

```python
for puerto in puertos:

    estado = comprobar_puerto(
        host,
        puerto
    )
```

En cada vuelta cambia:

```python
puerto
```

Podemos representarlo:

```text
puertos
   │
   ├── 22
   │    │
   │    ▼
   │  comprobar
   │
   ├── 80
   │    │
   │    ▼
   │  comprobar
   │
   └── 443
        │
        ▼
      comprobar
```

Estamos reutilizando la misma función para diferentes puertos.

---

### 45. Mostrar únicamente los puertos accesibles

En determinadas situaciones nos interesa mostrar únicamente las conexiones que se han podido establecer.

Podemos utilizar:

```python
if estado == "ACCESIBLE":

    print(
        f"Puerto {puerto}: "
        f"ACCESIBLE"
    )
```

El programa podría quedar:

```python
for puerto in puertos:

    estado = comprobar_puerto(
        host,
        puerto
    )

    if estado == "ACCESIBLE":

        print(
            f"Puerto {puerto}: "
            f"ACCESIBLE"
        )
```

Ahora la salida será más reducida.

---

### 46. Guardar los puertos accesibles

También podemos crear una lista:

```python
puertos_accesibles = []
```

Cuando encontremos uno:

```python
if estado == "ACCESIBLE":

    puertos_accesibles.append(
        puerto
    )
```

Después podemos mostrar:

```python
print(
    puertos_accesibles
)
```

Nuestro programa ya no se limita a mostrar información.

También la almacena para utilizarla posteriormente.

---

### 47. Contar los resultados

Podemos utilizar:

```python
len()
```

Por ejemplo:

```python
print(
    f"Puertos comprobados: "
    f"{len(puertos)}"
)
```

Y:

```python
print(
    f"Puertos accesibles: "
    f"{len(puertos_accesibles)}"
)
```

Esto nos permitirá generar un pequeño resumen.

---

### 48. Resumen de la comprobación

Podemos mostrar:

```python
print()
print("RESUMEN")
print("=======")
print()

print(
    f"Host: {host}"
)

print(
    f"Puertos comprobados: "
    f"{len(puertos)}"
)

print(
    f"Puertos accesibles: "
    f"{len(puertos_accesibles)}"
)
```

Por ejemplo:

```text
RESUMEN
=======

Host: example.com
Puertos comprobados: 3
Puertos accesibles: 2
```

Los resultados reales dependerán del equipo y de los servicios disponibles.

---

### 49. De una lista a un rango

Hasta ahora hemos definido:

```python
puertos = [
    22,
    80,
    443
]
```

Pero podemos generar automáticamente una secuencia mediante:

```python
range()
```

Por ejemplo:

```python
for puerto in range(
    20,
    26
):

    print(
        puerto
    )
```

Obtendremos:

```text
20
21
22
23
24
25
```

Recordemos que el último valor de:

```python
range()
```

no está incluido.

---

### 50. Incluir el puerto final

Supongamos que queremos comprobar desde:

```text
20
```

hasta:

```text
25
```

ambos incluidos.

Podemos utilizar:

```python
range(
    20,
    25 + 1
)
```

o:

```python
range(
    20,
    26
)
```

Cuando los valores se encuentren en variables será especialmente útil:

```python
for puerto in range(
    puerto_inicial,
    puerto_final + 1
):
```

Así incluiremos:

```text
puerto_inicial
```

y:

```text
puerto_final
```

---

### 51. Primer escáner de un rango

Crea:

```text
escaner_basico.py
```

Escribe:

```python
import socket


def comprobar_puerto(
    host,
    puerto
):

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as cliente:

            cliente.settimeout(
                1
            )

            resultado = (
                cliente.connect_ex(
                    (
                        host,
                        puerto
                    )
                )
            )

    except socket.gaierror:

        return "ERROR_DNS"

    except socket.timeout:

        return "TIMEOUT"

    except OSError:

        return "ERROR"

    else:

        if resultado == 0:

            return "ACCESIBLE"

        return "NO_ACCESIBLE"


host = "example.com"

puerto_inicial = 80
puerto_final = 85


print()
print("COMPROBACIÓN DE PUERTOS")
print("=======================")
print()


for puerto in range(
    puerto_inicial,
    puerto_final + 1
):

    estado = comprobar_puerto(
        host,
        puerto
    )

    print(
        f"{puerto}: {estado}"
    )
```

Ahora estamos realizando automáticamente varias comprobaciones TCP.

---

### 52. ¿Por qué hemos reducido el timeout?

En el programa anterior hemos utilizado:

```python
cliente.settimeout(
    1
)
```

Cuando comprobábamos un único puerto, esperar unos segundos no suponía un gran problema.

Pero cuando realizamos muchas comprobaciones:

```text
puerto 1
puerto 2
puerto 3
puerto 4
...
```

los tiempos de espera pueden acumularse.

Por ejemplo, si cada operación pudiera esperar:

```text
3 segundos
```

y realizamos:

```text
20 comprobaciones
```

el tiempo máximo teórico asociado a esas esperas podría crecer considerablemente.

!!! note "Timeout"

    Un timeout muy pequeño puede producir resultados poco útiles en redes lentas.

    Un timeout demasiado grande puede hacer que una comprobación de muchos puertos tarde demasiado.

    En nuestras prácticas utilizaremos rangos pequeños y tiempos moderados.

---

### 53. Añadir contadores

Podemos utilizar:

```python
total = 0
accesibles = 0
```

Dentro del bucle:

```python
total += 1
```

y:

```python
if estado == "ACCESIBLE":

    accesibles += 1
```

Al terminar:

```python
print(
    f"Comprobados: {total}"
)

print(
    f"Accesibles: {accesibles}"
)
```

Esto nos permite construir estadísticas básicas.

---

### 54. Lista de puertos accesibles

Otra posibilidad consiste en utilizar:

```python
puertos_accesibles = []
```

Dentro del bucle:

```python
if estado == "ACCESIBLE":

    puertos_accesibles.append(
        puerto
    )
```

Al finalizar:

```python
print()
print("PUERTOS ACCESIBLES")
print("==================")
print()


for puerto in puertos_accesibles:

    print(
        puerto
    )
```

Podemos obtener conceptualmente:

```text
PUERTOS ACCESIBLES
==================

80
443
```

Los valores dependerán del host comprobado.

---

### 55. Convertirlo en una herramienta reutilizable

Nuestro programa todavía contiene valores escritos directamente:

```python
host = "example.com"

puerto_inicial = 80
puerto_final = 85
```

Queremos poder ejecutar:

```powershell
python escaner.py example.com 80 85
```

Por tanto utilizaremos:

```python
argparse
```

---

### 56. Argumentos del escáner

Crea:

```text
escaner.py
```

Comienza:

```python
import argparse
import socket
```

Configura:

```python
parser = argparse.ArgumentParser(
    description=(
        "Comprueba un rango "
        "de puertos TCP."
    )
)
```

Añade el host:

```python
parser.add_argument(
    "host",
    help=(
        "Dirección IP o nombre "
        "del equipo"
    )
)
```

Puerto inicial:

```python
parser.add_argument(
    "inicio",
    type=int,
    help="Puerto inicial"
)
```

Puerto final:

```python
parser.add_argument(
    "fin",
    type=int,
    help="Puerto final"
)
```

Finalmente:

```python
args = parser.parse_args()
```

---

### 57. Validar el rango

Antes de realizar ninguna conexión debemos comprobar los argumentos.

Podemos utilizar:

```python
if not 0 <= args.inicio <= 65535:

    parser.error(
        "El puerto inicial debe "
        "estar entre 0 y 65535."
    )
```

Y:

```python
if not 0 <= args.fin <= 65535:

    parser.error(
        "El puerto final debe "
        "estar entre 0 y 65535."
    )
```

También debemos comprobar:

```python
if args.inicio > args.fin:

    parser.error(
        "El puerto inicial no "
        "puede ser mayor que "
        "el puerto final."
    )
```

Así evitamos rangos incorrectos.

---

### 58. Limitar el tamaño de las prácticas

Para las primeras pruebas no necesitamos recorrer miles de puertos.

Podemos limitar el rango:

```python
cantidad = (
    args.fin
    - args.inicio
    + 1
)
```

Y comprobar:

```python
if cantidad > 100:

    parser.error(
        "En esta práctica el rango "
        "máximo es de 100 puertos."
    )
```

!!! tip "Rangos pequeños"

    Limitar el rango hace que las prácticas sean más rápidas y facilita analizar qué está haciendo el programa.

    Nuestro objetivo es aprender el funcionamiento de `socket`, `range()`, los bucles y el control de errores.

---

### 59. Escáner parametrizable

Podemos utilizar:

```python
for puerto in range(
    args.inicio,
    args.fin + 1
):

    estado = comprobar_puerto(
        args.host,
        puerto
    )
```

Ahora el usuario decide:

```text
host
puerto inicial
puerto final
```

sin modificar el programa.

---

### 60. Ejemplo de ejecución

Podemos ejecutar:

```powershell
python escaner.py example.com 80 85
```

La aplicación comprobará:

```text
80
81
82
83
84
85
```

También podemos realizar pruebas sobre un equipo autorizado del laboratorio.

Por ejemplo:

```powershell
python escaner.py 192.168.1.20 20 30
```

si esa dirección corresponde a un equipo sobre el que tenemos permiso para realizar la práctica.

---

### 61. Añadir una opción `--timeout`

Podemos permitir que el usuario seleccione el tiempo máximo de espera.

Añade:

```python
parser.add_argument(
    "--timeout",
    type=float,
    default=1.0,
    help=(
        "Tiempo máximo de espera "
        "en segundos. "
        "Por defecto: 1"
    )
)
```

Validamos:

```python
if args.timeout <= 0:

    parser.error(
        "El timeout debe ser "
        "mayor que cero."
    )
```

Ahora podemos ejecutar:

```powershell
python escaner.py example.com 80 85 --timeout 2
```

---

### 62. Modificar la función para recibir el timeout

Cambia la función:

```python
def comprobar_puerto(
    host,
    puerto,
    timeout
):
```

Y utiliza:

```python
cliente.settimeout(
    timeout
)
```

La llamada será:

```python
estado = comprobar_puerto(
    args.host,
    puerto,
    args.timeout
)
```

Así eliminamos otro valor fijo del programa.

---

### 63. Medir la duración de la comprobación

Python incluye el módulo:

```python
time
```

Podemos importar:

```python
import time
```

Antes del bucle:

```python
inicio_tiempo = (
    time.perf_counter()
)
```

Después del bucle:

```python
fin_tiempo = (
    time.perf_counter()
)
```

Calculamos:

```python
duracion = (
    fin_tiempo
    - inicio_tiempo
)
```

Y mostramos:

```python
print(
    f"Duración: "
    f"{duracion:.2f} segundos"
)
```

Esto nos permitirá observar cómo influyen:

```text
número de puertos
timeout
respuesta de la red
```

en la duración del programa.

---

### 64. Mostrar un resumen final

Al finalizar podemos mostrar:

```python
print()
print("RESUMEN")
print("=======")
print()

print(
    f"Host: {args.host}"
)

print(
    f"Rango: "
    f"{args.inicio}-"
    f"{args.fin}"
)

print(
    f"Puertos comprobados: "
    f"{cantidad}"
)

print(
    f"Puertos accesibles: "
    f"{len(puertos_accesibles)}"
)

print(
    f"Duración: "
    f"{duracion:.2f} segundos"
)
```

Ahora nuestro programa proporciona un resultado más útil.

---

### 65. Guardar los resultados

Vamos a recuperar:

```python
pathlib
```

Importamos:

```python
from pathlib import Path
```

Definimos:

```python
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
```

Creamos el directorio:

```python
DIRECTORIO_RESULTADOS.mkdir(
    parents=True,
    exist_ok=True
)
```

Y definimos:

```python
ARCHIVO_RESULTADOS = (
    DIRECTORIO_RESULTADOS
    / "resultado_puertos.txt"
)
```

---

### 66. Generar un informe

Podemos construir:

```python
lineas = []

lineas.append(
    "INFORME DE PUERTOS"
)

lineas.append(
    "=================="
)

lineas.append(
    ""
)

lineas.append(
    f"Host: {args.host}"
)

lineas.append(
    f"Rango: "
    f"{args.inicio}-{args.fin}"
)

lineas.append(
    ""
)

lineas.append(
    "Puertos accesibles:"
)
```

Después:

```python
for puerto in puertos_accesibles:

    lineas.append(
        f"- {puerto}"
    )
```

Finalmente:

```python
contenido = "\n".join(
    lineas
)
```

y:

```python
ARCHIVO_RESULTADOS.write_text(
    contenido,
    encoding="utf-8"
)
```

---

### 67. ¿Qué ocurre si no encontramos ninguno?

Debemos contemplar esta situación.

Podemos hacer:

```python
if puertos_accesibles:

    for puerto in puertos_accesibles:

        lineas.append(
            f"- {puerto}"
        )

else:

    lineas.append(
        "Ninguno"
    )
```

Recordemos que una lista vacía:

```python
[]
```

se evalúa como falsa en una condición.

---

### 68. Añadir fecha y hora al informe

Podemos importar:

```python
from datetime import datetime
```

Después:

```python
ahora = datetime.now()
```

Y:

```python
fecha = ahora.strftime(
    "%Y-%m-%d %H:%M:%S"
)
```

Añadimos:

```python
lineas.append(
    f"Fecha: {fecha}"
)
```

Nuestro informe contendrá información sobre cuándo se realizó la comprobación.

---

### 69. Crear nombres de informe únicos

Si utilizamos siempre:

```text
resultado_puertos.txt
```

cada ejecución sustituirá el informe anterior.

Podemos crear un nombre con fecha y hora:

```python
marca_tiempo = (
    datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )
)
```

Después:

```python
nombre_archivo = (
    f"puertos_"
    f"{marca_tiempo}.txt"
)
```

Y:

```python
archivo_resultados = (
    DIRECTORIO_RESULTADOS
    / nombre_archivo
)
```

Podremos obtener:

```text
puertos_2026-09-21_11-30-25.txt
```

!!! note "Nombres compatibles con Windows"

    Evitamos utilizar:

    ```text
    :
    ```

    en la parte horaria del nombre porque este carácter no puede utilizarse normalmente en nombres de archivo de Windows.

    Por eso usamos:

    ```text
    11-30-25
    ```

    en lugar de:

    ```text
    11:30:25
    ```

---

### 70. Añadir `logging`

Nuestra herramienta también puede registrar su actividad.

Definimos:

```python
DIRECTORIO_LOGS = (
    DIRECTORIO_CAPITULO
    / "logs"
)
```

Creamos:

```python
DIRECTORIO_LOGS.mkdir(
    parents=True,
    exist_ok=True
)
```

Y:

```python
ARCHIVO_LOG = (
    DIRECTORIO_LOGS
    / "escaner.log"
)
```

Configuramos:

```python
logging.basicConfig(
    filename=ARCHIVO_LOG,
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S"
)
```

---

### 71. Registrar el inicio

Antes de comenzar:

```python
logging.info(
    f"Iniciando comprobación "
    f"de {args.host} "
    f"puertos "
    f"{args.inicio}-"
    f"{args.fin}"
)
```

Cuando encontremos una conexión:

```python
logging.info(
    f"{args.host}:{puerto} "
    f"ACCESIBLE"
)
```

Al terminar:

```python
logging.info(
    f"Comprobación terminada. "
    f"Accesibles: "
    f"{len(puertos_accesibles)}"
)
```

---

### 72. No llenar innecesariamente el log

Si comprobamos muchos puertos, registrar todos los resultados:

```text
NO_ACCESIBLE
```

puede producir un archivo muy grande.

En una herramienta sencilla podemos registrar:

```text
inicio
errores
puertos accesibles
resumen final
```

en lugar de guardar cada resultado negativo.

!!! tip "Logs útiles"

    Un buen log no consiste en guardar absolutamente todo.

    Debe conservar la información que resulte útil para comprender qué ha ocurrido durante la ejecución.

---

### 73. Programa completo

Crea:

```text
escaner_puertos.py
```

Escribe:

```python
import argparse
import logging
import socket
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


DIRECTORIO_RESULTADOS.mkdir(
    parents=True,
    exist_ok=True
)

DIRECTORIO_LOGS.mkdir(
    parents=True,
    exist_ok=True
)


ARCHIVO_LOG = (
    DIRECTORIO_LOGS
    / "escaner.log"
)


logging.basicConfig(
    filename=ARCHIVO_LOG,
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S"
)


def comprobar_puerto(
    host,
    puerto,
    timeout
):

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as cliente:

            cliente.settimeout(
                timeout
            )

            resultado = (
                cliente.connect_ex(
                    (
                        host,
                        puerto
                    )
                )
            )

    except socket.gaierror:

        return "ERROR_DNS"

    except socket.timeout:

        return "TIMEOUT"

    except OSError:

        return "ERROR"

    else:

        if resultado == 0:

            return "ACCESIBLE"

        return "NO_ACCESIBLE"


parser = argparse.ArgumentParser(
    description=(
        "Comprueba un rango "
        "de puertos TCP."
    )
)


parser.add_argument(
    "host",
    help=(
        "Dirección IP o nombre "
        "del equipo"
    )
)


parser.add_argument(
    "inicio",
    type=int,
    help="Puerto inicial"
)


parser.add_argument(
    "fin",
    type=int,
    help="Puerto final"
)


parser.add_argument(
    "--timeout",
    type=float,
    default=1.0,
    help=(
        "Tiempo máximo de espera "
        "por puerto. "
        "Por defecto: 1 segundo"
    )
)


args = parser.parse_args()


if not 0 <= args.inicio <= 65535:

    parser.error(
        "El puerto inicial debe "
        "estar entre 0 y 65535."
    )


if not 0 <= args.fin <= 65535:

    parser.error(
        "El puerto final debe "
        "estar entre 0 y 65535."
    )


if args.inicio > args.fin:

    parser.error(
        "El puerto inicial no "
        "puede ser mayor que "
        "el puerto final."
    )


if args.timeout <= 0:

    parser.error(
        "El timeout debe ser "
        "mayor que cero."
    )


cantidad = (
    args.fin
    - args.inicio
    + 1
)


if cantidad > 100:

    parser.error(
        "En esta práctica se permite "
        "un máximo de 100 puertos."
    )


logging.info(
    f"Iniciando comprobación "
    f"de {args.host} "
    f"puertos "
    f"{args.inicio}-{args.fin}"
)


print()
print("ESCÁNER TCP BÁSICO")
print("==================")
print()

print(
    f"Host: {args.host}"
)

print(
    f"Rango: "
    f"{args.inicio}-{args.fin}"
)

print(
    f"Timeout: "
    f"{args.timeout} segundos"
)

print()


puertos_accesibles = []


inicio_tiempo = (
    time.perf_counter()
)


for puerto in range(
    args.inicio,
    args.fin + 1
):

    estado = comprobar_puerto(
        args.host,
        puerto,
        args.timeout
    )

    if estado == "ACCESIBLE":

        print(
            f"{puerto}: ACCESIBLE"
        )

        puertos_accesibles.append(
            puerto
        )

        logging.info(
            f"{args.host}:{puerto} "
            f"ACCESIBLE"
        )

    elif estado == "ERROR_DNS":

        print(
            "ERROR: no se puede "
            "resolver el host."
        )

        logging.error(
            f"No se puede resolver "
            f"{args.host}"
        )

        break

    elif estado == "ERROR":

        print(
            f"{puerto}: "
            f"ERROR"
        )


fin_tiempo = (
    time.perf_counter()
)


duracion = (
    fin_tiempo
    - inicio_tiempo
)


print()
print("RESUMEN")
print("=======")
print()

print(
    f"Puertos comprobados: "
    f"{cantidad}"
)

print(
    f"Puertos accesibles: "
    f"{len(puertos_accesibles)}"
)

print(
    f"Duración: "
    f"{duracion:.2f} segundos"
)


marca_tiempo = (
    datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )
)


nombre_archivo = (
    f"puertos_"
    f"{marca_tiempo}.txt"
)


archivo_resultados = (
    DIRECTORIO_RESULTADOS
    / nombre_archivo
)


lineas = [
    "INFORME DE PUERTOS",
    "==================",
    "",
    (
        f"Fecha: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ),
    f"Host: {args.host}",
    (
        f"Rango: "
        f"{args.inicio}-{args.fin}"
    ),
    (
        f"Timeout: "
        f"{args.timeout} segundos"
    ),
    "",
    "Puertos accesibles:"
]


if puertos_accesibles:

    for puerto in puertos_accesibles:

        lineas.append(
            f"- {puerto}"
        )

else:

    lineas.append(
        "Ninguno"
    )


lineas.append(
    ""
)

lineas.append(
    f"Total comprobados: "
    f"{cantidad}"
)

lineas.append(
    f"Total accesibles: "
    f"{len(puertos_accesibles)}"
)

lineas.append(
    f"Duración: "
    f"{duracion:.2f} segundos"
)


contenido = "\n".join(
    lineas
)


try:

    archivo_resultados.write_text(
        contenido,
        encoding="utf-8"
    )

except OSError as error:

    print(
        "ERROR: no se ha podido "
        "guardar el informe."
    )

    logging.error(
        f"Error guardando informe: "
        f"{error}"
    )

else:

    print()

    print(
        f"Informe guardado en:"
    )

    print(
        archivo_resultados
    )


logging.info(
    f"Comprobación terminada. "
    f"Puertos accesibles: "
    f"{len(puertos_accesibles)}"
)
```

---

### 74. Probar el programa

Primero podemos consultar:

```powershell
python escaner_puertos.py --help
```

Después podemos realizar una prueba pequeña:

```powershell
python escaner_puertos.py example.com 80 85
```

También podemos modificar el timeout:

```powershell
python escaner_puertos.py example.com 80 85 --timeout 2
```

En el laboratorio podremos utilizar una dirección de un equipo autorizado:

```powershell
python escaner_puertos.py 192.168.1.20 20 30
```

---

### 75. Comprobar el informe

Después de ejecutar el programa entra en:

```text
practicas/capitulo6/resultados/
```

Encontrarás un archivo similar a:

```text
puertos_2026-09-21_11-30-25.txt
```

Su contenido tendrá una estructura parecida a:

```text
INFORME DE PUERTOS
==================

Fecha: 2026-09-21 11:30:25
Host: example.com
Rango: 80-85
Timeout: 1.0 segundos

Puertos accesibles:
- 80

Total comprobados: 6
Total accesibles: 1
Duración: 1.24 segundos
```

Los resultados concretos dependerán del destino y de las condiciones de red.

---

### 76. Comprobar el log

También tendremos:

```text
practicas/capitulo6/logs/
escaner.log
```

Podemos encontrar registros como:

```text
2026-09-21 11:30:24 - INFO - Iniciando comprobación de example.com puertos 80-85
2026-09-21 11:30:24 - INFO - example.com:80 ACCESIBLE
2026-09-21 11:30:25 - INFO - Comprobación terminada. Puertos accesibles: 1
```

Estamos diferenciando dos tipos de salida:

```text
INFORME
   │
   └── resultado de la operación


LOG
   │
   └── registro de la ejecución
```

---

### 77. Identificar servicios conocidos

Podemos asociar algunos puertos conocidos con nombres de servicios.

Por ejemplo:

```python
servicios = {
    22: "SSH",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS"
}
```

Podemos consultar:

```python
servicio = servicios.get(
    puerto,
    "Desconocido"
)
```

Si:

```python
puerto = 443
```

obtendremos:

```text
HTTPS
```

---

### 78. Mostrar puerto y servicio

Podemos utilizar:

```python
if estado == "ACCESIBLE":

    servicio = servicios.get(
        puerto,
        "Desconocido"
    )

    print(
        f"{puerto}: "
        f"ACCESIBLE "
        f"({servicio})"
    )
```

Podríamos obtener:

```text
80: ACCESIBLE (HTTP)
443: ACCESIBLE (HTTPS)
```

!!! note "Identificación orientativa"

    Asociar un número de puerto con un nombre de servicio no demuestra que ese servicio concreto esté funcionando realmente en el puerto.

    Por ejemplo, encontrar accesible el puerto:

    ```text
    80
    ```

    indica que podemos establecer una conexión TCP.

    El nombre:

    ```text
    HTTP
    ```

    corresponde al servicio habitualmente asociado con ese puerto.

---

### 79. Práctica propuesta: puertos conocidos

Modifica:

```text
escaner_puertos.py
```

para incluir:

```python
servicios = {
    21: "FTP",
    22: "SSH",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS"
}
```

Cuando un puerto resulte accesible deberá mostrar:

```text
22: ACCESIBLE (SSH)
```

o:

```text
443: ACCESIBLE (HTTPS)
```

Si no se encuentra en el diccionario:

```text
8080: ACCESIBLE (Desconocido)
```

---

### 80. Práctica propuesta: leer los puertos desde un archivo

Crea:

```text
datos/puertos.txt
```

con:

```text
22
80
443
```

Después crea:

```text
escaner_lista.py
```

El programa deberá:

1. Recibir un host mediante `argparse`.
2. Leer `puertos.txt`.
3. Convertir cada línea a `int`.
4. Validar el puerto.
5. Comprobar cada puerto.
6. Mostrar los accesibles.
7. Generar un informe.
8. Registrar errores mediante `logging`.

El flujo será:

```text
puertos.txt
     │
     ▼
   Path
     │
     ▼
read_text()
     │
     ▼
splitlines()
     │
     ▼
    int()
     │
     ▼
lista de puertos
     │
     ▼
    socket
     │
     ▼
 resultados
```

Esta práctica recupera directamente los conocimientos sobre archivos del **Capítulo 1**.

---

### 81. Práctica propuesta: inventario de servicios

Crea:

```text
datos/servicios.csv
```

con:

```csv
nombre,host,puerto
Web principal,example.com,443
Web HTTP,example.com,80
Servidor SSH,192.168.1.20,22
```

Crea:

```text
comprobar_servicios.py
```

El programa deberá:

1. Leer el archivo CSV.
2. Recorrer todos los servicios.
3. Comprobar cada combinación `host:puerto`.
4. Mostrar el estado.
5. Generar un informe.
6. Registrar los errores.

Conceptualmente:

```text
servicios.csv
      │
      ▼
  csv.DictReader
      │
      ▼
     fila
      │
      ├── nombre
      ├── host
      └── puerto
            │
            ▼
     comprobar_puerto()
            │
            ▼
          estado
```

!!! example "Resultado"

    La salida podría tener este aspecto:

    ```text
    COMPROBACIÓN DE SERVICIOS
    =========================

    Web principal
    example.com:443
    Estado: ACCESIBLE

    Web HTTP
    example.com:80
    Estado: ACCESIBLE

    Servidor SSH
    192.168.1.20:22
    Estado: NO ACCESIBLE
    ```

---

### 82. Qué hemos construido

Nuestro primer programa comprobaba:

```text
HOST
 │
 ▼
PUERTO
```

Ahora hemos evolucionado hasta:

```text
             HOST
              │
              ▼
      rango de puertos
              │
              ▼
             for
              │
              ▼
     comprobar_puerto()
              │
              ▼
     ┌────────┴────────┐
     │                 │
     ▼                 ▼
 ACCESIBLE       NO ACCESIBLE
     │
     ▼
lista de resultados
     │
     ├── pantalla
     ├── informe
     └── logging
```

Esto constituye un **escáner TCP básico y secuencial**.

---

### 83. Escaneo secuencial

Nuestro programa realiza las comprobaciones una detrás de otra:

```text
puerto 80
   │
   ▼
esperar resultado
   │
   ▼
puerto 81
   │
   ▼
esperar resultado
   │
   ▼
puerto 82
   │
   ▼
...
```

A este comportamiento podemos denominarlo:

```text
secuencial
```

Para los objetivos de esta unidad es suficiente y además permite comprender claramente el funcionamiento del programa.

No necesitamos introducir todavía técnicas más avanzadas de concurrencia.

---

### 84. Interpretar correctamente los resultados

Un resultado:

```text
ACCESIBLE
```

indica que nuestro programa ha podido establecer una conexión TCP con ese puerto.

Un resultado:

```text
NO ACCESIBLE
```

puede deberse a diferentes circunstancias:

```text
no existe un servicio escuchando
la conexión ha sido rechazada
un dispositivo intermedio la bloquea
la red no permite alcanzar el servicio
```

Por tanto, nuestra herramienta proporciona una **evidencia de conectividad TCP**, pero no explica automáticamente la causa de todos los resultados negativos.

---

### 85. Relación con las herramientas tradicionales

En administración de sistemas podemos combinar diferentes pruebas.

Por ejemplo:

```text
        DIAGNÓSTICO
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
    ping          socket
      │             │
      ▼             ▼
respuesta ICMP   conexión TCP
                  a un puerto
```

Esto nos proporciona información diferente.

Un buen diagnóstico puede necesitar varias pruebas antes de obtener una conclusión.

---

### 86. Práctica de consolidación

Desarrolla:

```text
diagnostico_tcp.py
```

El programa deberá aceptar:

```powershell
python diagnostico_tcp.py HOST INICIO FIN
```

y opcionalmente:

```text
--timeout
```

Deberá:

1. Validar los argumentos.
2. Limitar la práctica a un máximo de 100 puertos.
3. Comprobar el rango.
4. Mostrar únicamente los puertos accesibles.
5. Identificar servicios conocidos mediante un diccionario.
6. Contar los puertos comprobados.
7. Contar los puertos accesibles.
8. Medir la duración.
9. Crear un informe con fecha y hora.
10. Registrar la ejecución mediante `logging`.

El programa deberá utilizar como mínimo:

```text
argparse
socket
Path
datetime
time
logging
try / except
for
range
listas
diccionarios
```

!!! success "Objetivo de la práctica"

    Esta práctica integra contenidos estudiados desde los primeros capítulos del libro.

    El objetivo no es únicamente comprobar puertos, sino aprender a construir una herramienta de administración estructurada, reutilizable y capaz de gestionar errores.

---

### 87. Resumen de esta parte

En esta parte hemos pasado de comprobar:

```text
un puerto
```

a comprobar:

```text
varios puertos
```

mediante:

```python
for
```

y:

```python
range()
```

Hemos construido un escáner TCP básico utilizando:

```python
socket
```

y:

```python
connect_ex()
```

También hemos utilizado:

```text
listas
contadores
diccionarios
argparse
timeout
Path
datetime
time
logging
```

para transformar una prueba sencilla en una herramienta más completa.

El patrón principal es:

```text
HOST
 │
 ▼
RANGO DE PUERTOS
 │
 ▼
VALIDACIÓN
 │
 ▼
for + range()
 │
 ▼
socket
 │
 ▼
connect_ex()
 │
 ▼
RESULTADO
 │
 ├── mostrar
 ├── almacenar
 ├── informar
 └── registrar
```

Ya somos capaces de comprobar la conectividad TCP con servicios concretos y con pequeños rangos de puertos.

En la siguiente parte estudiaremos otro elemento fundamental del diagnóstico de red:

```text
DNS
```

Aprenderemos a convertir:

```text
nombre de host
        │
        ▼
   dirección IP
```

y también a consultar información asociada a direcciones mediante el módulo:

```python
socket
```

Esto nos permitirá construir posteriormente una herramienta de diagnóstico que combine:

```text
resolución DNS
+
comprobación TCP
+
informes
+
logging
```

---

## 88. Resolución DNS desde Python

Hasta ahora hemos utilizado indistintamente direcciones IP y nombres de host.

Por ejemplo:

```text
192.168.1.20
```

o:

```text
example.com
```

Cuando utilizamos un nombre como:

```text
example.com
```

nuestro ordenador necesita averiguar qué dirección IP corresponde a ese nombre.

Aquí interviene:

```text
DNS
```

En esta parte aprenderemos a utilizar Python para realizar operaciones básicas de resolución de nombres.

---

### 89. ¿Qué es DNS?

DNS significa:

```text
Domain Name System
```

Su función principal es permitir relacionar nombres con direcciones IP.

Por ejemplo:

```text
example.com
     │
     ▼
    DNS
     │
     ▼
dirección IP
```

Los usuarios normalmente prefieren trabajar con nombres:

```text
www.ejemplo.com
```

en lugar de recordar direcciones IP.

---

### 90. Nombres y direcciones IP

Podemos imaginar DNS como un sistema que mantiene relaciones del tipo:

```text
servidor.local
      │
      ▼
192.168.1.20
```

o:

```text
www.ejemplo.com
      │
      ▼
dirección IP
```

Cuando escribimos en un navegador:

```text
https://www.ejemplo.com
```

antes de poder establecer la comunicación es necesario obtener una dirección IP asociada al nombre.

De forma simplificada:

```text
NOMBRE
  │
  ▼
 DNS
  │
  ▼
DIRECCIÓN IP
  │
  ▼
CONEXIÓN
```

---

### 91. DNS dentro del diagnóstico de red

Imaginemos que intentamos acceder a:

```text
servidor.empresa.local
```

y no funciona.

Podemos plantearnos diferentes preguntas:

```text
¿Se puede resolver el nombre?
          │
          ▼
¿Obtenemos una dirección IP?
          │
          ▼
¿Existe conectividad?
          │
          ▼
¿Está accesible el servicio?
```

Por tanto, la resolución DNS es otra herramienta importante dentro del diagnóstico.

---

### 92. Herramientas del sistema para consultar DNS

En Windows podemos utilizar herramientas como:

```powershell
nslookup example.com
```

También podemos utilizar:

```powershell
Resolve-DnsName example.com
```

desde PowerShell.

Hasta ahora podríamos ejecutar estos comandos desde Python utilizando:

```python
subprocess
```

Pero el módulo:

```python
socket
```

también proporciona funciones para realizar determinadas operaciones de resolución.

---

### 93. `socket.gethostbyname()`

Una de las funciones más sencillas es:

```python
socket.gethostbyname()
```

Permite obtener una dirección IPv4 asociada a un nombre.

Crea:

```text
practicas/capitulo6/programas/
resolver_nombre.py
```

Escribe:

```python
import socket


host = "example.com"


ip = socket.gethostbyname(
    host
)


print(
    f"Host: {host}"
)

print(
    f"IP: {ip}"
)
```

Ejecuta:

```powershell
python resolver_nombre.py
```

Obtendremos una dirección IP asociada al nombre.

!!! note "La dirección puede variar"

    Un mismo nombre de Internet puede resolver a diferentes direcciones IP dependiendo del servicio, la infraestructura utilizada, la ubicación o el momento de la consulta.

    Por tanto, no debemos asumir que un nombre siempre devolverá una única dirección fija.

---

### 94. Flujo de `gethostbyname()`

Nuestro programa realiza conceptualmente:

```text
Python
  │
  │ example.com
  ▼
gethostbyname()
  │
  ▼
resolución
  │
  ▼
dirección IPv4
  │
  ▼
variable ip
```

Después podemos utilizar:

```python
ip
```

en otras operaciones de diagnóstico.

---

### 95. Recibir el nombre mediante `input()`

Podemos modificar:

```text
resolver_nombre.py
```

para escribir:

```python
import socket


host = input(
    "Nombre del host: "
)


ip = socket.gethostbyname(
    host
)


print(
    f"{host} -> {ip}"
)
```

Ahora podemos consultar diferentes nombres sin modificar el código.

Sin embargo, para nuestras herramientas utilizaremos nuevamente:

```text
argparse
```

---

### 96. Resolver nombres mediante `argparse`

Crea:

```text
dns_basico.py
```

Escribe:

```python
import argparse
import socket


parser = argparse.ArgumentParser(
    description=(
        "Resuelve un nombre "
        "a una dirección IPv4."
    )
)


parser.add_argument(
    "host",
    help=(
        "Nombre que se desea "
        "resolver"
    )
)


args = parser.parse_args()


ip = socket.gethostbyname(
    args.host
)


print()
print("RESOLUCIÓN DNS")
print("==============")
print()

print(
    f"Host: {args.host}"
)

print(
    f"IP: {ip}"
)
```

Podemos ejecutar:

```powershell
python dns_basico.py example.com
```

---

### 97. ¿Qué ocurre si el nombre no existe?

Prueba un nombre incorrecto:

```powershell
python dns_basico.py nombre-que-no-existe.invalid
```

La resolución no podrá completarse.

Python puede generar una excepción:

```python
socket.gaierror
```

Ya habíamos encontrado esta excepción durante las comprobaciones TCP.

Ahora podemos comprender mejor su significado.

---

### 98. Controlar `socket.gaierror`

Modifica el programa:

```python
import argparse
import socket


parser = argparse.ArgumentParser(
    description=(
        "Resuelve un nombre "
        "a una dirección IPv4."
    )
)


parser.add_argument(
    "host",
    help="Nombre del host"
)


args = parser.parse_args()


try:

    ip = socket.gethostbyname(
        args.host
    )

except socket.gaierror as error:

    print(
        "ERROR: no se ha podido "
        "resolver el nombre."
    )

    print(
        f"Detalle: {error}"
    )

else:

    print()
    print("RESOLUCIÓN DNS")
    print("==============")
    print()

    print(
        f"Host: {args.host}"
    )

    print(
        f"IP: {ip}"
    )
```

Ahora nuestro programa puede controlar correctamente un error de resolución.

---

### 99. Crear una función reutilizable

Vamos a separar la resolución del resto del programa.

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

    else:

        return ip
```

Podemos utilizar:

```python
ip = resolver_host(
    "example.com"
)


if ip is None:

    print(
        "No se ha podido "
        "resolver el host."
    )

else:

    print(
        f"IP: {ip}"
    )
```

Este diseño será útil para integrar DNS con nuestras herramientas anteriores.

---

### 100. Un nombre puede tener varias direcciones

La función:

```python
socket.gethostbyname()
```

devuelve una dirección IPv4.

Pero un nombre puede estar asociado a más de una dirección.

Por ejemplo, algunos servicios utilizan varios servidores:

```text
       servicio
          │
    ┌─────┼─────┐
    │     │     │
    ▼     ▼     ▼
   IP1   IP2   IP3
```

Esto puede utilizarse para:

```text
redundancia
distribución de carga
infraestructuras distribuidas
```

Por tanto, en algunas situaciones necesitaremos obtener más información que una única dirección.

---

### 101. `socket.gethostbyname_ex()`

Python proporciona:

```python
socket.gethostbyname_ex()
```

Podemos probar:

```python
import socket


resultado = (
    socket.gethostbyname_ex(
        "example.com"
    )
)


print(
    resultado
)
```

Esta función devuelve una tupla con diferentes elementos.

Conceptualmente:

```text
(
    nombre oficial,
    alias,
    lista de direcciones IP
)
```

---

### 102. Separar los valores recibidos

Podemos escribir:

```python
nombre, alias, ips = (
    socket.gethostbyname_ex(
        "example.com"
    )
)
```

Después:

```python
print(
    f"Nombre: {nombre}"
)

print(
    f"Alias: {alias}"
)

print(
    f"Direcciones: {ips}"
)
```

La variable:

```python
ips
```

es una lista.

Por tanto podemos recorrerla:

```python
for ip in ips:

    print(
        ip
    )
```

---

### 103. Programa para mostrar todas las IPv4

Crea:

```text
resolver_ips.py
```

Escribe:

```python
import argparse
import socket


parser = argparse.ArgumentParser(
    description=(
        "Obtiene direcciones IPv4 "
        "asociadas a un nombre."
    )
)


parser.add_argument(
    "host",
    help="Nombre del host"
)


args = parser.parse_args()


try:

    nombre, alias, ips = (
        socket.gethostbyname_ex(
            args.host
        )
    )

except socket.gaierror:

    print(
        "ERROR: no se ha podido "
        "resolver el nombre."
    )

else:

    print()
    print("INFORMACIÓN DNS")
    print("===============")
    print()

    print(
        f"Consulta: {args.host}"
    )

    print(
        f"Nombre: {nombre}"
    )

    print()

    print(
        "Direcciones IPv4:"
    )

    for ip in ips:

        print(
            f"- {ip}"
        )
```

Ahora nuestro programa puede mostrar varias direcciones si están disponibles.

---

### 104. Evitar direcciones repetidas

En determinadas situaciones podríamos querer evitar duplicados.

Podemos utilizar:

```python
set()
```

Por ejemplo:

```python
ips_unicas = set(
    ips
)
```

Después:

```python
for ip in ips_unicas:

    print(
        ip
    )
```

Un:

```text
set
```

es una colección que no mantiene elementos duplicados.

!!! note "Orden"

    Un conjunto (`set`) no debe utilizarse cuando necesitemos conservar necesariamente el mismo orden de los elementos.

    En esta práctica lo utilizaríamos únicamente para mostrar el concepto de eliminación de duplicados.

---

### 105. `socket.getaddrinfo()`

Existe otra función más completa:

```python
socket.getaddrinfo()
```

Puede proporcionar información necesaria para establecer conexiones utilizando diferentes familias y tipos de socket.

Por ejemplo:

```python
resultado = socket.getaddrinfo(
    "example.com",
    443
)
```

El resultado contiene varias estructuras.

En este nivel no necesitamos estudiar todos sus campos.

Nos interesa principalmente observar que puede proporcionar información tanto para IPv4 como, dependiendo del sistema y del nombre consultado, para IPv6.

---

### 106. IPv4 e IPv6

Hasta ahora hemos trabajado principalmente con:

```python
socket.AF_INET
```

que corresponde a IPv4.

También existe:

```python
socket.AF_INET6
```

para IPv6.

Podemos representar:

```text
AF_INET
   │
   └── IPv4


AF_INET6
   │
   └── IPv6
```

La función:

```python
socket.getaddrinfo()
```

puede ayudarnos a obtener información sobre ambas familias.

---

### 107. Consultar información de direcciones

Crea:

```text
info_direcciones.py
```

Escribe:

```python
import argparse
import socket


parser = argparse.ArgumentParser(
    description=(
        "Consulta información "
        "de direcciones de un host."
    )
)


parser.add_argument(
    "host",
    help="Nombre del host"
)


args = parser.parse_args()


try:

    resultados = (
        socket.getaddrinfo(
            args.host,
            None
        )
    )

except socket.gaierror:

    print(
        "ERROR: no se ha podido "
        "resolver el nombre."
    )

else:

    print()
    print("DIRECCIONES")
    print("===========")
    print()

    for resultado in resultados:

        familia = resultado[0]

        direccion = (
            resultado[4][0]
        )

        if familia == socket.AF_INET:

            tipo = "IPv4"

        elif familia == socket.AF_INET6:

            tipo = "IPv6"

        else:

            tipo = "Otro"

        print(
            f"{tipo}: {direccion}"
        )
```

Podemos ejecutar:

```powershell
python info_direcciones.py example.com
```

---

### 108. Eliminar resultados repetidos

`getaddrinfo()` puede devolver varias entradas relacionadas con una misma dirección.

Para mostrar una salida más sencilla podemos utilizar un conjunto:

```python
direcciones = set()
```

Dentro del bucle:

```python
direcciones.add(
    (
        tipo,
        direccion
    )
)
```

Después:

```python
for tipo, direccion in direcciones:

    print(
        f"{tipo}: {direccion}"
    )
```

Estamos almacenando tuplas:

```text
(
    tipo,
    dirección
)
```

dentro de un conjunto.

---

### 109. Resolución inversa

Hasta ahora hemos realizado:

```text
nombre
  │
  ▼
 IP
```

También podemos intentar el proceso contrario:

```text
 IP
  │
  ▼
nombre
```

Esto se conoce como:

```text
resolución inversa
```

Python proporciona:

```python
socket.gethostbyaddr()
```

---

### 110. `socket.gethostbyaddr()`

Podemos escribir:

```python
import socket


resultado = socket.gethostbyaddr(
    "8.8.8.8"
)


print(
    resultado
)
```

La función intenta obtener información asociada a la dirección.

!!! note "Resolución inversa"

    No todas las direcciones IP tienen necesariamente configurada una resolución inversa útil.

    Por tanto, una consulta inversa puede fallar aunque la dirección IP sea válida y el equipo sea accesible.

---

### 111. Controlar errores en la resolución inversa

Podemos utilizar:

```python
try:

    resultado = socket.gethostbyaddr(
        ip
    )

except socket.herror:

    print(
        "No existe información "
        "de resolución inversa."
    )
```

En determinadas situaciones también puede producirse:

```python
socket.gaierror
```

Por tanto, podemos controlar ambas:

```python
except (
    socket.herror,
    socket.gaierror
):

    print(
        "No se ha podido realizar "
        "la resolución inversa."
    )
```

---

### 112. Programa de resolución inversa

Crea:

```text
dns_inverso.py
```

Escribe:

```python
import argparse
import socket


parser = argparse.ArgumentParser(
    description=(
        "Realiza una resolución "
        "inversa de una IP."
    )
)


parser.add_argument(
    "ip",
    help="Dirección IP"
)


args = parser.parse_args()


try:

    nombre, alias, direcciones = (
        socket.gethostbyaddr(
            args.ip
        )
    )

except (
    socket.herror,
    socket.gaierror
):

    print(
        "No se ha podido obtener "
        "un nombre para la IP."
    )

else:

    print()
    print("RESOLUCIÓN INVERSA")
    print("==================")
    print()

    print(
        f"IP: {args.ip}"
    )

    print(
        f"Nombre: {nombre}"
    )
```

---

### 113. Validar una dirección IP

Hasta ahora el usuario puede introducir cualquier texto:

```powershell
python dns_inverso.py hola
```

Podemos comprobar si una cadena representa una dirección IPv4 válida utilizando:

```python
socket.inet_aton()
```

Por ejemplo:

```python
try:

    socket.inet_aton(
        args.ip
    )

except OSError:

    parser.error(
        "La dirección IPv4 "
        "no es válida."
    )
```

Esto nos permite introducir otra capa de validación.

---

### 114. DNS directo e inverso

Podemos resumir:

```text
RESOLUCIÓN DIRECTA

nombre
  │
  ▼
 DNS
  │
  ▼
 IP
```

y:

```text
RESOLUCIÓN INVERSA

 IP
  │
  ▼
 DNS
  │
  ▼
nombre
```

No debemos asumir que ambas operaciones producirán siempre resultados equivalentes.

La configuración DNS puede hacer que:

```text
nombre → IP
```

funcione y que:

```text
IP → nombre
```

no proporcione un resultado útil.

---

### 115. Crear una herramienta DNS

Ahora construiremos:

```text
diagnostico_dns.py
```

Permitirá realizar dos operaciones:

```text
--resolver
```

y:

```text
--inversa
```

Por ejemplo:

```powershell
python diagnostico_dns.py --resolver example.com
```

o:

```powershell
python diagnostico_dns.py --inversa 8.8.8.8
```

---

### 116. Crear los argumentos

Comenzamos:

```python
import argparse
import socket


parser = argparse.ArgumentParser(
    description=(
        "Herramienta básica "
        "de diagnóstico DNS."
    )
)


grupo = (
    parser.add_mutually_exclusive_group(
        required=True
    )
)


grupo.add_argument(
    "--resolver",
    metavar="HOST",
    help=(
        "Resuelve un nombre "
        "de host"
    )
)


grupo.add_argument(
    "--inversa",
    metavar="IP",
    help=(
        "Realiza resolución "
        "inversa"
    )
)


args = parser.parse_args()
```

---

### 117. Función de resolución directa

Añade:

```python
def resolver_nombre(
    host
):

    try:

        nombre, alias, ips = (
            socket.gethostbyname_ex(
                host
            )
        )

    except socket.gaierror:

        return None

    else:

        return {
            "consulta": host,
            "nombre": nombre,
            "ips": ips
        }
```

Observa que estamos devolviendo un:

```python
dict
```

Esto facilitará procesar posteriormente el resultado.

---

### 118. Función de resolución inversa

Añade:

```python
def resolver_ip(
    ip
):

    try:

        nombre, alias, direcciones = (
            socket.gethostbyaddr(
                ip
            )
        )

    except (
        socket.herror,
        socket.gaierror
    ):

        return None

    else:

        return {
            "ip": ip,
            "nombre": nombre,
            "alias": alias,
            "direcciones": direcciones
        }
```

Nuevamente devolvemos un diccionario.

Estamos separando:

```text
obtener información
```

de:

```text
mostrar información
```

---

### 119. Programa principal

Podemos utilizar:

```python
if args.resolver:

    resultado = resolver_nombre(
        args.resolver
    )

    if resultado is None:

        print(
            "ERROR: no se ha podido "
            "resolver el nombre."
        )

    else:

        print()
        print("RESOLUCIÓN DNS")
        print("==============")
        print()

        print(
            f"Nombre: "
            f"{resultado['nombre']}"
        )

        print(
            "Direcciones:"
        )

        for ip in resultado["ips"]:

            print(
                f"- {ip}"
            )
```

Para la resolución inversa:

```python
elif args.inversa:

    resultado = resolver_ip(
        args.inversa
    )

    if resultado is None:

        print(
            "No se ha podido realizar "
            "la resolución inversa."
        )

    else:

        print()
        print("RESOLUCIÓN INVERSA")
        print("==================")
        print()

        print(
            f"IP: "
            f"{resultado['ip']}"
        )

        print(
            f"Nombre: "
            f"{resultado['nombre']}"
        )
```

---

### 120. Añadir `logging`

Como en nuestras herramientas anteriores, podemos crear:

```text
practicas/capitulo6/logs/
```

y almacenar:

```text
dns.log
```

Configuramos:

```python
logging.basicConfig(
    filename=ARCHIVO_LOG,
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S"
)
```

Podemos registrar:

```python
logging.info(
    f"Resolviendo {host}"
)
```

Si falla:

```python
logging.error(
    f"No se puede resolver "
    f"{host}"
)
```

---

### 121. Guardar los resultados

También podemos utilizar:

```text
resultados/
```

para almacenar un informe.

Por ejemplo:

```text
dns_example.com.txt
```

con:

```text
INFORME DNS
===========

Consulta: example.com

Direcciones IPv4:
- ...
- ...
```

Así recuperamos nuevamente los conocimientos de:

```text
Path
archivos
try / except
```

---

### 122. Combinar DNS y comprobación TCP

Ahora tenemos dos herramientas:

```text
resolver_host()
```

y:

```text
comprobar_puerto()
```

Podemos combinarlas.

El flujo será:

```text
       HOST
        │
        ▼
resolver DNS
        │
   ┌────┴────┐
   │         │
 error       IP
             │
             ▼
      comprobar puerto
             │
        ┌────┴────┐
        │         │
        ▼         ▼
    ACCESIBLE   NO ACCESIBLE
```

Esta combinación es mucho más útil para diagnóstico.

---

### 123. Programa DNS + TCP

Crea:

```text
dns_tcp.py
```

Escribe:

```python
import argparse
import socket


def resolver_host(
    host
):

    try:

        return socket.gethostbyname(
            host
        )

    except socket.gaierror:

        return None


def comprobar_puerto(
    ip,
    puerto,
    timeout=2
):

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as cliente:

            cliente.settimeout(
                timeout
            )

            resultado = (
                cliente.connect_ex(
                    (
                        ip,
                        puerto
                    )
                )
            )

    except OSError:

        return False

    else:

        return resultado == 0


parser = argparse.ArgumentParser(
    description=(
        "Resuelve un host y "
        "comprueba un puerto TCP."
    )
)


parser.add_argument(
    "host",
    help="Nombre del host"
)


parser.add_argument(
    "puerto",
    type=int,
    help="Puerto TCP"
)


args = parser.parse_args()


if not 0 <= args.puerto <= 65535:

    parser.error(
        "El puerto debe estar "
        "entre 0 y 65535."
    )


print()
print("DIAGNÓSTICO DNS + TCP")
print("====================")
print()

print(
    f"Host: {args.host}"
)


ip = resolver_host(
    args.host
)


if ip is None:

    print(
        "DNS: ERROR"
    )

else:

    print(
        "DNS: CORRECTO"
    )

    print(
        f"IP: {ip}"
    )

    print(
        f"Puerto: {args.puerto}"
    )

    accesible = comprobar_puerto(
        ip,
        args.puerto
    )

    if accesible:

        print(
            "TCP: ACCESIBLE"
        )

    else:

        print(
            "TCP: NO ACCESIBLE"
        )
```

---

### 124. Probar el diagnóstico

Podemos ejecutar:

```powershell
python dns_tcp.py example.com 443
```

La salida podría ser:

```text
DIAGNÓSTICO DNS + TCP
====================

Host: example.com
DNS: CORRECTO
IP: ...
Puerto: 443
TCP: ACCESIBLE
```

También podemos probar:

```powershell
python dns_tcp.py nombre-que-no-existe.invalid 443
```

Obtendremos:

```text
DNS: ERROR
```

y el programa no intentará realizar la conexión TCP.

---

### 125. ¿Por qué no continuamos si DNS falla?

Si el usuario ha proporcionado:

```text
servidor.empresa.local
```

pero no podemos convertir ese nombre en una dirección IP, no tenemos todavía un destino IPv4 con el que realizar nuestra comprobación.

Por tanto:

```text
DNS falla
   │
   ▼
detener diagnóstico TCP
```

Esto muestra una idea importante del diagnóstico:

```text
comprobar primero
las dependencias anteriores
```

antes de continuar.

---

### 126. Interpretar los resultados

Podemos encontrarnos con diferentes situaciones.

#### Caso 1

```text
DNS: CORRECTO
TCP: ACCESIBLE
```

Hemos podido resolver el nombre y establecer una conexión TCP.

#### Caso 2

```text
DNS: CORRECTO
TCP: NO ACCESIBLE
```

La resolución funciona, pero no hemos podido establecer la conexión TCP con el puerto indicado.

#### Caso 3

```text
DNS: ERROR
```

El problema aparece antes de intentar la conexión TCP.

Este análisis nos permite localizar mejor en qué etapa se produce el problema.

---

### 127. Comparación con el capítulo anterior

En el capítulo 5 trabajábamos:

```text
URL
 │
 ▼
HTTP
 │
 ▼
respuesta
```

Ahora podemos observar algunas operaciones que se producen a niveles anteriores:

```text
https://example.com
        │
        ▼
      nombre
        │
        ▼
       DNS
        │
        ▼
        IP
        │
        ▼
    conexión TCP
        │
        ▼
      puerto
        │
        ▼
       HTTP
```

Esto ayuda a comprender que una petición HTTP depende de otros mecanismos de red.

---

### 128. Práctica guiada: diagnóstico de un servicio

Crea:

```text
diagnostico_servicio.py
```

El programa deberá recibir:

```powershell
python diagnostico_servicio.py HOST PUERTO
```

Por ejemplo:

```powershell
python diagnostico_servicio.py example.com 443
```

Deberá:

1. Validar el puerto.
2. Resolver el nombre.
3. Mostrar la dirección IPv4 obtenida.
4. Comprobar el puerto TCP.
5. Mostrar el resultado.
6. Registrar las operaciones mediante `logging`.

La salida tendrá una estructura similar a:

```text
DIAGNÓSTICO DE SERVICIO
=======================

Host: example.com
DNS: CORRECTO
IP: ...
Puerto: 443
TCP: ACCESIBLE
```

---

### 129. Práctica propuesta: varios servicios

Crea:

```text
datos/servicios_dns.csv
```

con:

```csv
nombre,host,puerto
Web principal,example.com,443
Web HTTP,example.com,80
```

Después crea:

```text
diagnostico_servicios.py
```

El programa deberá:

```text
leer CSV
   │
   ▼
obtener servicio
   │
   ▼
resolver host
   │
   ▼
obtener IP
   │
   ▼
comprobar puerto
   │
   ▼
guardar resultado
```

La salida podría ser:

```text
SERVICIO: Web principal
Host: example.com
IP: ...
Puerto: 443
DNS: CORRECTO
TCP: ACCESIBLE
```

---

### 130. Práctica propuesta: generar informe

Amplía:

```text
diagnostico_servicios.py
```

para generar:

```text
resultados/
diagnostico_servicios.txt
```

El informe deberá contener para cada servicio:

```text
nombre
host
IP resuelta
puerto
estado DNS
estado TCP
```

También deberá incluir:

```text
fecha y hora
total de servicios
servicios accesibles
errores DNS
```

Esto nos permitirá integrar:

```text
CSV
+
DNS
+
TCP
+
Path
+
datetime
+
logging
```

---

### 131. Práctica de investigación

Utiliza desde PowerShell:

```powershell
nslookup example.com
```

Después ejecuta:

```powershell
python resolver_ips.py example.com
```

Compara la información mostrada por ambas herramientas.

Responde:

1. ¿Aparece alguna dirección IP?
2. ¿Aparecen varias?
3. ¿Coinciden todos los resultados?
4. ¿Qué herramienta proporciona más información?
5. ¿Qué ventaja tiene realizar la consulta desde Python?

!!! tip "Objetivo"

    No buscamos sustituir herramientas como `nslookup`.

    Nuestro objetivo es aprender a incorporar la resolución de nombres dentro de nuestros propios scripts de administración.

---

### 132. Práctica de consolidación

Desarrolla:

```text
analizador_host.py
```

El programa recibirá:

```powershell
python analizador_host.py HOST
```

y deberá mostrar:

```text
ANÁLISIS DEL HOST
=================

Host: ...

IPv4:
- ...

IPv6:
- ...

Resolución inversa:
...

Puertos comprobados:
22  → ...
80  → ...
443 → ...
```

Los puertos que debe comprobar serán:

```python
puertos = [
    22,
    80,
    443
]
```

El programa deberá utilizar:

```text
socket.getaddrinfo()
socket.gethostbyaddr()
socket.socket()
connect_ex()
timeout
argparse
try / except
logging
```

!!! warning "Entorno autorizado"

    Realiza las comprobaciones TCP únicamente sobre sistemas propios, equipos del laboratorio o servicios para los que exista autorización.

---

### 133. Patrón de diagnóstico aprendido

Ahora disponemos de un patrón más completo:

```text
             HOST
              │
              ▼
        resolución DNS
              │
       ┌──────┴──────┐
       │             │
       ▼             ▼
     ERROR           IP
                      │
                      ▼
                puerto TCP
                      │
                      ▼
                connect_ex()
                      │
                ┌─────┴─────┐
                │           │
                ▼           ▼
            ACCESIBLE   NO ACCESIBLE
                │           │
                └─────┬─────┘
                      │
                      ▼
              informe + log
```

Este modelo nos permite identificar mejor dónde se produce un problema.

---

### 134. DNS no garantiza conectividad

Es importante recordar:

```text
DNS CORRECTO
```

significa que hemos podido obtener información de resolución.

No significa necesariamente que:

```text
el equipo esté disponible
```

ni que:

```text
un servicio esté accesible
```

Por ejemplo:

```text
DNS
 │
 ▼
CORRECTO
 │
 ▼
IP obtenida
 │
 ▼
TCP
 │
 ▼
NO ACCESIBLE
```

es una situación perfectamente posible.

---

### 135. TCP accesible tampoco identifica completamente el servicio

Si conseguimos conectarnos a:

```text
host:80
```

sabemos que se ha podido establecer una conexión TCP con ese puerto.

Pero eso no demuestra por sí solo qué aplicación concreta está escuchando.

Por tanto debemos diferenciar:

```text
conectividad TCP
```

de:

```text
identificación del servicio
```

En nuestro nivel utilizaremos los puertos conocidos únicamente como referencia orientativa.

---

### 136. Relación entre las herramientas estudiadas

A estas alturas podemos combinar diferentes herramientas:

```text
             DIAGNÓSTICO
                  │
       ┌──────────┼──────────┐
       │          │          │
       ▼          ▼          ▼
     ping        DNS       socket
       │          │          │
       ▼          ▼          ▼
     ICMP       nombre      TCP
                  ↕          │
                  IP       puerto
```

Y en el capítulo anterior añadimos:

```text
HTTP
 │
 ▼
servicio web
```

Esto nos permite construir diagnósticos progresivamente más completos.

---

### 137. Resumen de esta parte

En esta parte hemos aprendido a realizar operaciones básicas de resolución DNS desde Python utilizando:

```python
socket
```

Hemos utilizado:

```python
socket.gethostbyname()
```

para obtener una dirección IPv4.

También:

```python
socket.gethostbyname_ex()
```

para obtener información adicional y varias direcciones IPv4.

Hemos introducido:

```python
socket.getaddrinfo()
```

para consultar información de direcciones IPv4 e IPv6.

También hemos trabajado con:

```python
socket.gethostbyaddr()
```

para realizar resolución inversa.

Hemos controlado errores como:

```python
socket.gaierror
```

y:

```python
socket.herror
```

Finalmente hemos combinado:

```text
DNS
+
TCP
```

para crear un diagnóstico por etapas:

```text
nombre
  │
  ▼
DNS
  │
  ▼
IP
  │
  ▼
socket TCP
  │
  ▼
puerto
  │
  ▼
resultado
```

En la siguiente parte realizaremos la **práctica integradora y cierre del Capítulo 6**, construyendo una herramienta de diagnóstico de red que combine los conocimientos trabajados:

```text
DNS
+
comprobación TCP
+
varios servicios
+
CSV
+
argparse
+
excepciones
+
logging
+
informes
```

Con ella quedará completada la unidad dedicada al **diagnóstico básico de red con Python**.

---

## 138. Práctica integradora: herramienta de diagnóstico de red

Durante este capítulo hemos desarrollado pequeñas herramientas capaces de realizar tareas concretas:

```text
resolver nombres DNS
        │
        ▼
obtener direcciones IP

comprobar puertos TCP
        │
        ▼
determinar accesibilidad

leer inventarios
        │
        ▼
automatizar comprobaciones
```

Ahora integraremos todos estos elementos en una única aplicación.

Crearemos:

```text
diagnostico_red.py
```

La herramienta será capaz de:

```text
leer un inventario CSV
        │
        ▼
resolver cada host
        │
        ▼
obtener su dirección IP
        │
        ▼
comprobar un puerto TCP
        │
        ▼
clasificar el resultado
        │
        ▼
mostrar resumen
        │
        ├── generar informe
        │
        └── generar log
```

Esta práctica servirá también para repasar muchos de los conceptos estudiados durante el libro.

---

### 139. Objetivos de la práctica

Nuestra aplicación deberá:

1. Recibir un archivo CSV mediante `argparse`.
2. Comprobar que el archivo existe.
3. Leer una lista de servicios.
4. Validar los datos.
5. Resolver los nombres mediante DNS.
6. Comprobar la conectividad TCP.
7. Mostrar los resultados en pantalla.
8. Contabilizar los diferentes estados.
9. Generar un informe.
10. Registrar la ejecución mediante `logging`.
11. Controlar los errores más habituales.

Utilizaremos:

```text
argparse
csv
socket
logging
datetime
pathlib
try / except
funciones
listas
diccionarios
bucles
condicionales
```

---

### 140. Estructura de la práctica

Utilizaremos:

```text
practicas/
└── capitulo6/
    ├── datos/
    │   └── servicios.csv
    │
    ├── logs/
    │   └── diagnostico_red.log
    │
    ├── programas/
    │   └── diagnostico_red.py
    │
    └── resultados/
        └── diagnostico_....txt
```

Si los directorios:

```text
logs
resultados
```

no existen, nuestro programa los creará automáticamente.

---

### 141. Crear el inventario

Crea:

```text
practicas/capitulo6/datos/servicios.csv
```

Escribe:

```csv
nombre,host,puerto
Web de pruebas,example.com,443
Web HTTP,example.com,80
```

En el laboratorio podremos añadir nuestros propios equipos.

Por ejemplo:

```csv
nombre,host,puerto
Servidor web,192.168.1.20,80
Servidor seguro,192.168.1.30,443
Servidor SSH,192.168.1.40,22
```

!!! warning "Equipos autorizados"

    Las comprobaciones TCP deben realizarse únicamente sobre equipos propios, sistemas del laboratorio o dispositivos para los que exista autorización.

---

### 142. Estructura del CSV

Nuestro archivo contiene tres columnas:

```text
nombre
host
puerto
```

Por ejemplo:

```csv
Web de pruebas,example.com,443
```

representa:

```text
nombre
  │
  └── Web de pruebas

host
  │
  └── example.com

puerto
  │
  └── 443
```

Cada fila representa un servicio que queremos comprobar.

---

### 143. Flujo general del programa

La aplicación seguirá este proceso:

```text
INICIO
  │
  ▼
leer argumentos
  │
  ▼
validar CSV
  │
  ▼
leer inventario
  │
  ▼
recorrer servicios
  │
  ▼
resolver DNS
  │
  ├── ERROR
  │
  └── IP
       │
       ▼
 comprobar TCP
       │
   ┌───┴────┐
   │        │
   ▼        ▼
accesible  no accesible
   │        │
   └───┬────┘
       ▼
guardar resultado
       │
       ▼
generar informe
       │
       ▼
mostrar resumen
       │
       ▼
      FIN
```

---

### 144. Crear el programa

Crea:

```text
practicas/capitulo6/programas/
diagnostico_red.py
```

Comenzaremos con los módulos necesarios:

```python
import argparse
import csv
import logging
import socket

from datetime import datetime
from pathlib import Path
```

Todos los módulos utilizados en esta práctica forman parte de la biblioteca estándar de Python.

---

### 145. Definir los directorios

Añade:

```python
DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)

DIRECTORIO_CAPITULO = (
    DIRECTORIO_PROGRAMA.parent
)

DIRECTORIO_LOGS = (
    DIRECTORIO_CAPITULO
    / "logs"
)

DIRECTORIO_RESULTADOS = (
    DIRECTORIO_CAPITULO
    / "resultados"
)
```

Creamos los directorios:

```python
DIRECTORIO_LOGS.mkdir(
    parents=True,
    exist_ok=True
)

DIRECTORIO_RESULTADOS.mkdir(
    parents=True,
    exist_ok=True
)
```

Este patrón ya lo hemos utilizado anteriormente.

---

### 146. Configurar el log

Definimos:

```python
ARCHIVO_LOG = (
    DIRECTORIO_LOGS
    / "diagnostico_red.log"
)
```

Configuramos:

```python
logging.basicConfig(
    filename=ARCHIVO_LOG,
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)
```

En este caso hemos añadido:

```python
encoding="utf-8"
```

para establecer explícitamente la codificación del archivo.

---

### 147. Crear los argumentos

Queremos ejecutar:

```powershell
python diagnostico_red.py ../datos/servicios.csv
```

Por tanto necesitamos un argumento:

```text
inventario
```

Configuramos:

```python
parser = argparse.ArgumentParser(
    description=(
        "Realiza un diagnóstico "
        "DNS y TCP de varios servicios."
    )
)
```

Añadimos:

```python
parser.add_argument(
    "inventario",
    help=(
        "Archivo CSV con "
        "los servicios"
    )
)
```

Y:

```python
parser.add_argument(
    "--timeout",
    type=float,
    default=2.0,
    help=(
        "Timeout TCP en segundos. "
        "Por defecto: 2"
    )
)
```

Finalmente:

```python
args = parser.parse_args()
```

---

### 148. Validar el timeout

Comprobamos:

```python
if args.timeout <= 0:

    parser.error(
        "El timeout debe ser "
        "mayor que cero."
    )
```

Esto evita valores como:

```text
0
```

o:

```text
-5
```

---

### 149. Convertir el argumento en un `Path`

Podemos hacer:

```python
archivo_inventario = Path(
    args.inventario
)
```

Después comprobamos:

```python
if not archivo_inventario.exists():

    parser.error(
        "El archivo indicado "
        "no existe."
    )
```

También:

```python
if not archivo_inventario.is_file():

    parser.error(
        "La ruta indicada "
        "no es un archivo."
    )
```

---

### 150. Crear la función para resolver DNS

Definimos:

```python
def resolver_host(
    host
):

    try:

        ip = socket.gethostbyname(
            host
        )

    except socket.gaierror:

        logging.error(
            f"Error DNS: {host}"
        )

        return None

    else:

        logging.info(
            f"DNS correcto: "
            f"{host} -> {ip}"
        )

        return ip
```

La función devuelve:

```text
dirección IP
```

si la resolución funciona.

Si falla devuelve:

```python
None
```

---

### 151. Crear la función para comprobar TCP

Definimos:

```python
def comprobar_tcp(
    ip,
    puerto,
    timeout
):

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as cliente:

            cliente.settimeout(
                timeout
            )

            resultado = (
                cliente.connect_ex(
                    (
                        ip,
                        puerto
                    )
                )
            )

    except socket.timeout:

        return "TIMEOUT"

    except OSError as error:

        logging.error(
            f"Error TCP "
            f"{ip}:{puerto}: "
            f"{error}"
        )

        return "ERROR"

    else:

        if resultado == 0:

            return "ACCESIBLE"

        return "NO_ACCESIBLE"
```

Ahora hemos separado:

```text
DNS
```

de:

```text
TCP
```

en dos funciones diferentes.

---

### 152. Leer el archivo CSV

Creamos:

```python
def cargar_inventario(
    archivo
):

    servicios = []

    try:

        with archivo.open(
            "r",
            encoding="utf-8",
            newline=""
        ) as fichero:

            lector = csv.DictReader(
                fichero
            )

            for fila in lector:

                servicios.append(
                    fila
                )

    except OSError as error:

        logging.error(
            f"Error leyendo CSV: "
            f"{error}"
        )

        return None

    else:

        return servicios
```

La función devolverá una:

```text
lista de diccionarios
```

---

### 153. Resultado de `DictReader`

Una fila como:

```csv
Web de pruebas,example.com,443
```

se convertirá aproximadamente en:

```python
{
    "nombre": "Web de pruebas",
    "host": "example.com",
    "puerto": "443"
}
```

Observa que:

```python
fila["puerto"]
```

es inicialmente un texto.

Necesitaremos convertirlo mediante:

```python
int()
```

---

### 154. Validar cada fila

Podemos crear:

```python
def validar_servicio(
    fila
):

    try:

        nombre = fila["nombre"].strip()
        host = fila["host"].strip()

        puerto = int(
            fila["puerto"]
        )

    except (
        KeyError,
        ValueError,
        AttributeError
    ):

        return None
```

Después validamos:

```python
    if not nombre or not host:

        return None
```

Y:

```python
    if not 0 <= puerto <= 65535:

        return None
```

Finalmente:

```python
    return {
        "nombre": nombre,
        "host": host,
        "puerto": puerto
    }
```

---

### 155. Función completa de validación

La función será:

```python
def validar_servicio(
    fila
):

    try:

        nombre = fila["nombre"].strip()
        host = fila["host"].strip()

        puerto = int(
            fila["puerto"]
        )

    except (
        KeyError,
        ValueError,
        AttributeError
    ):

        return None

    if not nombre or not host:

        return None

    if not 0 <= puerto <= 65535:

        return None

    return {
        "nombre": nombre,
        "host": host,
        "puerto": puerto
    }
```

Estamos aplicando una idea importante:

```text
DATOS EXTERNOS
      │
      ▼
   validar
      │
      ▼
    utilizar
```

Nunca debemos asumir automáticamente que los datos de un archivo son correctos.

---

### 156. Diagnosticar un servicio

Ahora podemos crear una función que combine las anteriores:

```python
def diagnosticar_servicio(
    servicio,
    timeout
):

    nombre = servicio["nombre"]
    host = servicio["host"]
    puerto = servicio["puerto"]

    ip = resolver_host(
        host
    )
```

Si DNS falla:

```python
    if ip is None:

        return {
            "nombre": nombre,
            "host": host,
            "ip": "-",
            "puerto": puerto,
            "dns": "ERROR",
            "tcp": "NO_COMPROBADO"
        }
```

Si funciona:

```python
    estado_tcp = comprobar_tcp(
        ip,
        puerto,
        timeout
    )
```

Y devolvemos:

```python
    return {
        "nombre": nombre,
        "host": host,
        "ip": ip,
        "puerto": puerto,
        "dns": "CORRECTO",
        "tcp": estado_tcp
    }
```

---

### 157. Ventaja de devolver un diccionario

Nuestra función devuelve una estructura como:

```python
{
    "nombre": "Web de pruebas",
    "host": "example.com",
    "ip": "...",
    "puerto": 443,
    "dns": "CORRECTO",
    "tcp": "ACCESIBLE"
}
```

Esto facilita:

```text
mostrar
guardar
contar
generar informes
```

sin repetir la operación de diagnóstico.

---

### 158. Cargar el inventario

En el programa principal:

```python
servicios = cargar_inventario(
    archivo_inventario
)
```

Comprobamos:

```python
if servicios is None:

    print(
        "ERROR: no se ha podido "
        "leer el inventario."
    )

    raise SystemExit(1)
```

También:

```python
if not servicios:

    print(
        "El inventario está vacío."
    )

    raise SystemExit(1)
```

---

### 159. Crear la lista de resultados

Definimos:

```python
resultados = []
```

Después recorremos:

```python
for fila in servicios:
```

Validamos:

```python
servicio = validar_servicio(
    fila
)
```

Si no es válido:

```python
if servicio is None:

    logging.warning(
        f"Fila incorrecta: {fila}"
    )

    continue
```

Si es válido:

```python
resultado = (
    diagnosticar_servicio(
        servicio,
        args.timeout
    )
)
```

Y:

```python
resultados.append(
    resultado
)
```

---

### 160. Mostrar cada resultado

Podemos mostrar:

```python
print()
print(
    resultado["nombre"]
)

print(
    "-" * len(
        resultado["nombre"]
    )
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
    f"Puerto: "
    f"{resultado['puerto']}"
)

print(
    f"DNS: "
    f"{resultado['dns']}"
)

print(
    f"TCP: "
    f"{resultado['tcp']}"
)
```

Obtendremos algo parecido a:

```text
Web de pruebas
--------------

Host: example.com
IP: ...
Puerto: 443
DNS: CORRECTO
TCP: ACCESIBLE
```

---

### 161. Registrar los resultados

Podemos registrar:

```python
logging.info(
    f"{resultado['nombre']} - "
    f"{resultado['host']}:"
    f"{resultado['puerto']} - "
    f"DNS={resultado['dns']} - "
    f"TCP={resultado['tcp']}"
)
```

De esta manera el log mantiene un historial técnico de las comprobaciones.

---

### 162. Crear contadores

Al terminar tendremos:

```python
resultados
```

Podemos calcular:

```python
total = len(
    resultados
)
```

Servicios TCP accesibles:

```python
accesibles = sum(
    1
    for resultado in resultados
    if resultado["tcp"]
    == "ACCESIBLE"
)
```

Errores DNS:

```python
errores_dns = sum(
    1
    for resultado in resultados
    if resultado["dns"]
    == "ERROR"
)
```

---

### 163. Comprender `sum()` con una expresión generadora

La expresión:

```python
sum(
    1
    for resultado in resultados
    if resultado["tcp"]
    == "ACCESIBLE"
)
```

puede interpretarse como:

```text
recorrer resultados
        │
        ▼
¿TCP == ACCESIBLE?
        │
       sí
        │
        ▼
       +1
```

También podríamos realizarlo con un bucle tradicional.

Ambas soluciones son válidas.

---

### 164. Mostrar el resumen

Podemos utilizar:

```python
print()
print("RESUMEN")
print("=======")
print()

print(
    f"Servicios analizados: "
    f"{total}"
)

print(
    f"TCP accesibles: "
    f"{accesibles}"
)

print(
    f"Errores DNS: "
    f"{errores_dns}"
)
```

Esto proporciona una visión rápida del diagnóstico.

---

### 165. Generar el informe

Crearemos una función:

```python
def generar_informe(
    resultados
):
```

Primero generamos una marca temporal:

```python
    ahora = datetime.now()

    marca = ahora.strftime(
        "%Y-%m-%d_%H-%M-%S"
    )
```

Nombre:

```python
    nombre_archivo = (
        f"diagnostico_"
        f"{marca}.txt"
    )
```

Ruta:

```python
    archivo = (
        DIRECTORIO_RESULTADOS
        / nombre_archivo
    )
```

---

### 166. Crear el contenido del informe

Podemos comenzar:

```python
    lineas = [
        "INFORME DE DIAGNÓSTICO DE RED",
        "==============================",
        "",
        (
            "Fecha: "
            + ahora.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        ),
        ""
    ]
```

Después recorremos:

```python
    for resultado in resultados:

        lineas.append(
            resultado["nombre"]
        )

        lineas.append(
            "-" * len(
                resultado["nombre"]
            )
        )

        lineas.append(
            f"Host: "
            f"{resultado['host']}"
        )

        lineas.append(
            f"IP: "
            f"{resultado['ip']}"
        )

        lineas.append(
            f"Puerto: "
            f"{resultado['puerto']}"
        )

        lineas.append(
            f"DNS: "
            f"{resultado['dns']}"
        )

        lineas.append(
            f"TCP: "
            f"{resultado['tcp']}"
        )

        lineas.append(
            ""
        )
```

---

### 167. Añadir el resumen al informe

Calculamos:

```python
    total = len(
        resultados
    )
```

```python
    accesibles = sum(
        1
        for resultado in resultados
        if resultado["tcp"]
        == "ACCESIBLE"
    )
```

```python
    errores_dns = sum(
        1
        for resultado in resultados
        if resultado["dns"]
        == "ERROR"
    )
```

Añadimos:

```python
    lineas.append(
        "RESUMEN"
    )

    lineas.append(
        "======="
    )

    lineas.append(
        ""
    )

    lineas.append(
        f"Servicios analizados: "
        f"{total}"
    )

    lineas.append(
        f"TCP accesibles: "
        f"{accesibles}"
    )

    lineas.append(
        f"Errores DNS: "
        f"{errores_dns}"
    )
```

---

### 168. Guardar el informe

Convertimos la lista en texto:

```python
    contenido = "\n".join(
        lineas
    )
```

Guardamos:

```python
    try:

        archivo.write_text(
            contenido,
            encoding="utf-8"
        )

    except OSError as error:

        logging.error(
            f"No se puede guardar "
            f"el informe: {error}"
        )

        return None

    else:

        return archivo
```

La función devolverá la ruta del informe si se ha creado correctamente.

---

### 169. Programa completo `diagnostico_red.py`

El programa completo queda:

```python
import argparse
import csv
import logging
import socket

from datetime import datetime
from pathlib import Path


DIRECTORIO_PROGRAMA = (
    Path(__file__).resolve().parent
)

DIRECTORIO_CAPITULO = (
    DIRECTORIO_PROGRAMA.parent
)

DIRECTORIO_LOGS = (
    DIRECTORIO_CAPITULO
    / "logs"
)

DIRECTORIO_RESULTADOS = (
    DIRECTORIO_CAPITULO
    / "resultados"
)


DIRECTORIO_LOGS.mkdir(
    parents=True,
    exist_ok=True
)

DIRECTORIO_RESULTADOS.mkdir(
    parents=True,
    exist_ok=True
)


ARCHIVO_LOG = (
    DIRECTORIO_LOGS
    / "diagnostico_red.log"
)


logging.basicConfig(
    filename=ARCHIVO_LOG,
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)


def resolver_host(
    host
):

    try:

        ip = socket.gethostbyname(
            host
        )

    except socket.gaierror:

        logging.error(
            f"Error DNS: {host}"
        )

        return None

    else:

        logging.info(
            f"DNS correcto: "
            f"{host} -> {ip}"
        )

        return ip


def comprobar_tcp(
    ip,
    puerto,
    timeout
):

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as cliente:

            cliente.settimeout(
                timeout
            )

            resultado = (
                cliente.connect_ex(
                    (
                        ip,
                        puerto
                    )
                )
            )

    except socket.timeout:

        return "TIMEOUT"

    except OSError as error:

        logging.error(
            f"Error TCP "
            f"{ip}:{puerto}: "
            f"{error}"
        )

        return "ERROR"

    else:

        if resultado == 0:

            return "ACCESIBLE"

        return "NO_ACCESIBLE"


def cargar_inventario(
    archivo
):

    servicios = []

    try:

        with archivo.open(
            "r",
            encoding="utf-8",
            newline=""
        ) as fichero:

            lector = csv.DictReader(
                fichero
            )

            for fila in lector:

                servicios.append(
                    fila
                )

    except OSError as error:

        logging.error(
            f"Error leyendo CSV: "
            f"{error}"
        )

        return None

    else:

        return servicios


def validar_servicio(
    fila
):

    try:

        nombre = fila["nombre"].strip()
        host = fila["host"].strip()

        puerto = int(
            fila["puerto"]
        )

    except (
        KeyError,
        ValueError,
        AttributeError
    ):

        return None

    if not nombre or not host:

        return None

    if not 0 <= puerto <= 65535:

        return None

    return {
        "nombre": nombre,
        "host": host,
        "puerto": puerto
    }


def diagnosticar_servicio(
    servicio,
    timeout
):

    nombre = servicio["nombre"]
    host = servicio["host"]
    puerto = servicio["puerto"]

    ip = resolver_host(
        host
    )

    if ip is None:

        return {
            "nombre": nombre,
            "host": host,
            "ip": "-",
            "puerto": puerto,
            "dns": "ERROR",
            "tcp": "NO_COMPROBADO"
        }

    estado_tcp = comprobar_tcp(
        ip,
        puerto,
        timeout
    )

    return {
        "nombre": nombre,
        "host": host,
        "ip": ip,
        "puerto": puerto,
        "dns": "CORRECTO",
        "tcp": estado_tcp
    }


def generar_informe(
    resultados
):

    ahora = datetime.now()

    marca = ahora.strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    nombre_archivo = (
        f"diagnostico_"
        f"{marca}.txt"
    )

    archivo = (
        DIRECTORIO_RESULTADOS
        / nombre_archivo
    )

    lineas = [
        "INFORME DE DIAGNÓSTICO DE RED",
        "==============================",
        "",
        (
            "Fecha: "
            + ahora.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        ),
        ""
    ]

    for resultado in resultados:

        lineas.append(
            resultado["nombre"]
        )

        lineas.append(
            "-" * len(
                resultado["nombre"]
            )
        )

        lineas.append(
            f"Host: "
            f"{resultado['host']}"
        )

        lineas.append(
            f"IP: "
            f"{resultado['ip']}"
        )

        lineas.append(
            f"Puerto: "
            f"{resultado['puerto']}"
        )

        lineas.append(
            f"DNS: "
            f"{resultado['dns']}"
        )

        lineas.append(
            f"TCP: "
            f"{resultado['tcp']}"
        )

        lineas.append(
            ""
        )

    total = len(
        resultados
    )

    accesibles = sum(
        1
        for resultado in resultados
        if resultado["tcp"]
        == "ACCESIBLE"
    )

    errores_dns = sum(
        1
        for resultado in resultados
        if resultado["dns"]
        == "ERROR"
    )

    lineas.append(
        "RESUMEN"
    )

    lineas.append(
        "======="
    )

    lineas.append(
        ""
    )

    lineas.append(
        f"Servicios analizados: "
        f"{total}"
    )

    lineas.append(
        f"TCP accesibles: "
        f"{accesibles}"
    )

    lineas.append(
        f"Errores DNS: "
        f"{errores_dns}"
    )

    contenido = "\n".join(
        lineas
    )

    try:

        archivo.write_text(
            contenido,
            encoding="utf-8"
        )

    except OSError as error:

        logging.error(
            f"No se puede guardar "
            f"el informe: {error}"
        )

        return None

    else:

        return archivo


parser = argparse.ArgumentParser(
    description=(
        "Realiza un diagnóstico "
        "DNS y TCP de varios servicios."
    )
)


parser.add_argument(
    "inventario",
    help=(
        "Archivo CSV con "
        "los servicios"
    )
)


parser.add_argument(
    "--timeout",
    type=float,
    default=2.0,
    help=(
        "Timeout TCP en segundos. "
        "Por defecto: 2"
    )
)


args = parser.parse_args()


if args.timeout <= 0:

    parser.error(
        "El timeout debe ser "
        "mayor que cero."
    )


archivo_inventario = Path(
    args.inventario
)


if not archivo_inventario.exists():

    parser.error(
        "El archivo indicado "
        "no existe."
    )


if not archivo_inventario.is_file():

    parser.error(
        "La ruta indicada "
        "no es un archivo."
    )


logging.info(
    "Inicio del diagnóstico"
)


servicios = cargar_inventario(
    archivo_inventario
)


if servicios is None:

    print(
        "ERROR: no se ha podido "
        "leer el inventario."
    )

    raise SystemExit(1)


if not servicios:

    print(
        "El inventario está vacío."
    )

    raise SystemExit(1)


resultados = []


print()
print("DIAGNÓSTICO DE RED")
print("==================")
print()


for fila in servicios:

    servicio = validar_servicio(
        fila
    )

    if servicio is None:

        logging.warning(
            f"Fila incorrecta: "
            f"{fila}"
        )

        continue

    resultado = (
        diagnosticar_servicio(
            servicio,
            args.timeout
        )
    )

    resultados.append(
        resultado
    )

    print(
        resultado["nombre"]
    )

    print(
        "-" * len(
            resultado["nombre"]
        )
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
        f"Puerto: "
        f"{resultado['puerto']}"
    )

    print(
        f"DNS: "
        f"{resultado['dns']}"
    )

    print(
        f"TCP: "
        f"{resultado['tcp']}"
    )

    print()

    logging.info(
        f"{resultado['nombre']} - "
        f"{resultado['host']}:"
        f"{resultado['puerto']} - "
        f"DNS={resultado['dns']} - "
        f"TCP={resultado['tcp']}"
    )


total = len(
    resultados
)


accesibles = sum(
    1
    for resultado in resultados
    if resultado["tcp"]
    == "ACCESIBLE"
)


errores_dns = sum(
    1
    for resultado in resultados
    if resultado["dns"]
    == "ERROR"
)


print("RESUMEN")
print("=======")
print()

print(
    f"Servicios analizados: "
    f"{total}"
)

print(
    f"TCP accesibles: "
    f"{accesibles}"
)

print(
    f"Errores DNS: "
    f"{errores_dns}"
)


archivo_informe = generar_informe(
    resultados
)


if archivo_informe is None:

    print()

    print(
        "No se ha podido "
        "guardar el informe."
    )

else:

    print()

    print(
        "Informe generado:"
    )

    print(
        archivo_informe
    )


logging.info(
    f"Fin del diagnóstico. "
    f"Servicios={total}, "
    f"accesibles={accesibles}, "
    f"errores_dns={errores_dns}"
)
```

---

### 170. Primera ejecución

Sitúate en:

```text
practicas/capitulo6/programas/
```

Podemos consultar primero la ayuda:

```powershell
python diagnostico_red.py --help
```

Deberemos ver los argumentos disponibles.

Ahora ejecutamos:

```powershell
python diagnostico_red.py ../datos/servicios.csv
```

También podemos indicar otro timeout:

```powershell
python diagnostico_red.py ../datos/servicios.csv --timeout 3
```

---

### 171. Analizar la salida

Podríamos obtener una salida similar a:

```text
DIAGNÓSTICO DE RED
==================

Web de pruebas
--------------
Host: example.com
IP: ...
Puerto: 443
DNS: CORRECTO
TCP: ACCESIBLE

Web HTTP
--------
Host: example.com
IP: ...
Puerto: 80
DNS: CORRECTO
TCP: ACCESIBLE

RESUMEN
=======

Servicios analizados: 2
TCP accesibles: 2
Errores DNS: 0

Informe generado:
...\resultados\diagnostico_2026-09-21_12-15-30.txt
```

Los resultados concretos dependerán de la red y de los servicios utilizados.

---

### 172. Comprobar el informe

En:

```text
practicas/capitulo6/resultados/
```

encontraremos un archivo similar a:

```text
diagnostico_2026-09-21_12-15-30.txt
```

El informe contendrá:

```text
INFORME DE DIAGNÓSTICO DE RED
==============================

Fecha: 2026-09-21 12:15:30

Web de pruebas
--------------
Host: example.com
IP: ...
Puerto: 443
DNS: CORRECTO
TCP: ACCESIBLE

Web HTTP
--------
Host: example.com
IP: ...
Puerto: 80
DNS: CORRECTO
TCP: ACCESIBLE

RESUMEN
=======

Servicios analizados: 2
TCP accesibles: 2
Errores DNS: 0
```

---

### 173. Comprobar el log

También tendremos:

```text
practicas/capitulo6/logs/
diagnostico_red.log
```

Podemos encontrar:

```text
2026-09-21 12:15:29 - INFO - Inicio del diagnóstico
2026-09-21 12:15:29 - INFO - DNS correcto: example.com -> ...
2026-09-21 12:15:29 - INFO - Web de pruebas - example.com:443 - DNS=CORRECTO - TCP=ACCESIBLE
2026-09-21 12:15:30 - INFO - Fin del diagnóstico. Servicios=2, accesibles=2, errores_dns=0
```

Ahora tenemos claramente diferenciados:

```text
PANTALLA
    │
    └── información inmediata


INFORME
    │
    └── resultados del diagnóstico


LOG
    │
    └── historial técnico
```

---

### 174. Probar un error DNS

Añade temporalmente al CSV:

```csv
Servidor inexistente,nombre-que-no-existe.invalid,80
```

Ejecuta de nuevo:

```powershell
python diagnostico_red.py ../datos/servicios.csv
```

Para ese servicio deberíamos obtener:

```text
DNS: ERROR
TCP: NO_COMPROBADO
```

Esto es importante.

No mostramos:

```text
TCP: NO_ACCESIBLE
```

porque realmente **no hemos realizado la comprobación TCP**.

El problema se ha producido en una fase anterior.

---

### 175. Diferenciar estados

Nuestra herramienta distingue:

```text
DNS
├── CORRECTO
└── ERROR
```

y:

```text
TCP
├── ACCESIBLE
├── NO_ACCESIBLE
├── TIMEOUT
├── ERROR
└── NO_COMPROBADO
```

Esto proporciona mucha más información que devolver simplemente:

```text
True
```

o:

```text
False
```

---

### 176. Diagnóstico por etapas

Nuestra herramienta sigue una estrategia:

```text
ETAPA 1
Validar datos
     │
     ▼
ETAPA 2
Resolver DNS
     │
     ▼
ETAPA 3
Comprobar TCP
     │
     ▼
ETAPA 4
Registrar resultado
     │
     ▼
ETAPA 5
Generar informe
```

Si una etapa imprescindible falla, no siempre tiene sentido ejecutar las siguientes.

Por ejemplo:

```text
DNS ERROR
   │
   ▼
TCP NO_COMPROBADO
```

Esta forma de diseñar el programa facilita también localizar errores.

---

### 177. Práctica: añadir servicios conocidos

Añade al programa:

```python
SERVICIOS_CONOCIDOS = {
    21: "FTP",
    22: "SSH",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS"
}
```

Dentro de:

```python
diagnosticar_servicio()
```

podemos obtener:

```python
tipo_servicio = (
    SERVICIOS_CONOCIDOS.get(
        puerto,
        "Desconocido"
    )
)
```

Añade al diccionario de resultado:

```python
"servicio": tipo_servicio
```

La salida podría mostrar:

```text
Puerto: 443
Servicio habitual: HTTPS
TCP: ACCESIBLE
```

!!! note "Servicio habitual"

    El número de puerto únicamente nos permite indicar el servicio asociado habitualmente con él.

    No demuestra qué aplicación concreta está utilizando realmente ese puerto.

---

### 178. Práctica: añadir estadísticas

Amplía el resumen para mostrar:

```text
Servicios analizados
DNS correctos
Errores DNS
TCP accesibles
TCP no accesibles
Timeouts
Errores TCP
```

Por ejemplo:

```text
RESUMEN
=======

Servicios analizados: 8
DNS correctos: 7
Errores DNS: 1
TCP accesibles: 5
TCP no accesibles: 1
Timeouts: 1
Errores TCP: 0
```

Utiliza:

```python
sum()
```

para calcular cada categoría.

---

### 179. Práctica: añadir salida JSON

En el capítulo 5 hemos trabajado con JSON.

Podemos recuperar esos conocimientos importando:

```python
import json
```

Después podemos guardar:

```python
resultados
```

mediante:

```python
json.dumps(
    resultados,
    indent=4,
    ensure_ascii=False
)
```

y:

```python
archivo_json.write_text(
    contenido_json,
    encoding="utf-8"
)
```

De esta manera nuestra herramienta podría generar:

```text
diagnostico_2026-09-21_12-15-30.txt
```

y:

```text
diagnostico_2026-09-21_12-15-30.json
```

---

### 180. Ejemplo de resultado JSON

Podríamos obtener:

```json
[
    {
        "nombre": "Web de pruebas",
        "host": "example.com",
        "ip": "192.0.2.10",
        "puerto": 443,
        "dns": "CORRECTO",
        "tcp": "ACCESIBLE"
    },
    {
        "nombre": "Servidor inexistente",
        "host": "nombre-que-no-existe.invalid",
        "ip": "-",
        "puerto": 80,
        "dns": "ERROR",
        "tcp": "NO_COMPROBADO"
    }
]
```

!!! note "Direcciones del ejemplo"

    Las direcciones mostradas en los ejemplos son ilustrativas.

    Los resultados reales de una consulta DNS pueden ser diferentes.

---

### 181. Práctica: opción `--json`

Podemos añadir:

```python
parser.add_argument(
    "--json",
    action="store_true",
    help=(
        "Genera también "
        "un informe JSON"
    )
)
```

Entonces:

```powershell
python diagnostico_red.py ../datos/servicios.csv --json
```

podría generar:

```text
informe TXT
+
informe JSON
```

Así recuperamos:

```text
argparse
+
flags booleanos
+
JSON
```

---

### 182. Práctica: modo detallado

También podemos añadir:

```python
parser.add_argument(
    "-d",
    "--detallado",
    action="store_true",
    help=(
        "Muestra información "
        "detallada"
    )
)
```

Sin la opción:

```powershell
python diagnostico_red.py ../datos/servicios.csv
```

podríamos mostrar únicamente:

```text
Web de pruebas: ACCESIBLE
Web HTTP: ACCESIBLE
```

Con:

```powershell
python diagnostico_red.py ../datos/servicios.csv --detallado
```

mostraríamos:

```text
nombre
host
IP
puerto
DNS
TCP
```

Esta técnica ya la estudiamos con:

```python
argparse
```

---

### 183. Práctica: integrar HTTP

Podemos ampliar voluntariamente la herramienta para los puertos:

```text
80
443
```

Si encontramos un servicio TCP accesible, podríamos utilizar lo aprendido en el capítulo 5 mediante:

```python
requests
```

para intentar realizar una petición HTTP.

El diagnóstico podría evolucionar:

```text
DNS
 │
 ▼
TCP
 │
 ▼
¿80 o 443?
 │
 ├── no ──► finalizar
 │
 └── sí
      │
      ▼
    HTTP
      │
      ▼
status_code
```

!!! tip "Ampliación"

    Esta ampliación no es necesaria para completar el capítulo.

    Su objetivo es relacionar los contenidos de los capítulos 5 y 6.

---

### 184. Práctica final del capítulo

Crea una nueva versión:

```text
diagnostico_red_v2.py
```

Debe incorporar:

```text
lectura CSV
resolución DNS
comprobación TCP
identificación de servicios conocidos
timeout configurable
modo detallado
informe TXT
informe JSON opcional
logging
estadísticas
control de errores
```

La ejecución deberá permitir:

```powershell
python diagnostico_red_v2.py ../datos/servicios.csv
```

También:

```powershell
python diagnostico_red_v2.py ../datos/servicios.csv --timeout 3
```

Y:

```powershell
python diagnostico_red_v2.py ../datos/servicios.csv --json --detallado
```

---

### 185. Requisitos mínimos de `diagnostico_red_v2.py`

El programa deberá utilizar:

```text
argparse
csv
socket
logging
datetime
pathlib
json
```

y aplicar:

```text
funciones
diccionarios
listas
bucles
condicionales
try / except
validación de datos
```

El programa deberá estar dividido en funciones.

Por ejemplo:

```text
resolver_host()
comprobar_tcp()
cargar_inventario()
validar_servicio()
diagnosticar_servicio()
generar_informe_txt()
generar_informe_json()
mostrar_resumen()
```

---

### 186. Flujo de la versión final

La aplicación seguirá:

```text
               INICIO
                  │
                  ▼
             argparse
                  │
                  ▼
          validar argumentos
                  │
                  ▼
             leer CSV
                  │
                  ▼
          validar servicios
                  │
                  ▼
          ┌────── DNS ──────┐
          │                 │
        ERROR               IP
          │                 │
          │                 ▼
          │                TCP
          │            ┌────┴────┐
          │            │         │
          │        ACCESIBLE   OTRO
          │            │         │
          └────────────┴────┬────┘
                            │
                            ▼
                       resultados
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
           pantalla        TXT           JSON
                                           
                            │
                            ▼
                           LOG
```

---

### 187. Qué conocimientos estamos integrando

Esta práctica recupera contenidos de varios capítulos.

Del **Capítulo 1**:

```text
Path
archivos
CSV
directorios
```

Del **Capítulo 2**:

```text
herramientas de diagnóstico
comandos del sistema
conceptos de red
```

Del **Capítulo 3**:

```text
automatización
listas de equipos
informes
procesamiento repetitivo
```

Del **Capítulo 4**:

```text
argparse
excepciones
logging
scripts parametrizables
```

Del **Capítulo 5**:

```text
JSON
servicios de red
HTTP
APIs
```

Y del **Capítulo 6**:

```text
socket
TCP
puertos
DNS
resolución de nombres
```

---

### 188. Diferentes niveles del diagnóstico

Después de los capítulos 5 y 6 podemos distinguir:

```text
NOMBRE
  │
  ▼
 DNS
  │
  ▼
DIRECCIÓN IP
  │
  ▼
 TCP
  │
  ▼
PUERTO
  │
  ▼
SERVICIO
  │
  ▼
HTTP / API
```

Un problema puede aparecer en diferentes etapas.

Por ejemplo:

```text
DNS ERROR
```

es diferente de:

```text
DNS CORRECTO
TCP NO ACCESIBLE
```

y también es diferente de:

```text
DNS CORRECTO
TCP ACCESIBLE
HTTP 404
```

Cada resultado proporciona información distinta.

---

### 189. Método de diagnóstico

Una estrategia útil consiste en avanzar por etapas:

```text
1. ¿Los datos son válidos?
           │
           ▼
2. ¿Se resuelve el nombre?
           │
           ▼
3. ¿Existe conectividad TCP?
           │
           ▼
4. ¿Responde el servicio?
           │
           ▼
5. ¿La respuesta es la esperada?
```

Este enfoque evita mezclar problemas diferentes.

---

### 190. Buenas prácticas aplicadas

Durante el desarrollo hemos aplicado diferentes buenas prácticas:

```text
separar el programa en funciones
validar los datos externos
utilizar timeouts
controlar excepciones concretas
registrar operaciones
generar informes
usar rutas con pathlib
parametrizar mediante argparse
```

También hemos evitado:

```text
valores fijos innecesarios
rutas absolutas
except genéricos innecesarios
esperas de red sin timeout
mezclar toda la lógica en un único bloque
```

---

### 191. Seguridad y uso responsable

Las herramientas de diagnóstico de red son útiles para:

```text
administración
mantenimiento
inventario
monitorización
resolución de incidencias
```

Pero deben utilizarse de forma responsable.

!!! warning "Uso autorizado"

    Utiliza las herramientas de comprobación de puertos únicamente sobre:

    - Tus propios sistemas.
    - Equipos del laboratorio.
    - Infraestructuras sobre las que tengas autorización.

    No realices comprobaciones masivas sobre sistemas ajenos.

---

### 192. Resumen del Capítulo 6

En este capítulo hemos aprendido a utilizar:

```python
socket
```

para realizar diagnósticos básicos de red.

Primero hemos creado sockets TCP mediante:

```python
socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
```

Después hemos utilizado:

```python
connect_ex()
```

para comprobar la conectividad con determinados puertos.

Hemos evolucionado desde:

```text
un puerto
```

hasta:

```text
varios puertos
```

y posteriormente:

```text
pequeños rangos de puertos
```

También hemos utilizado:

```python
socket.gethostbyname()
```

```python
socket.gethostbyname_ex()
```

```python
socket.getaddrinfo()
```

y:

```python
socket.gethostbyaddr()
```

para trabajar con resolución de nombres.

Finalmente hemos combinado:

```text
CSV
+
DNS
+
TCP
+
argparse
+
excepciones
+
logging
+
informes
```

para desarrollar una herramienta de diagnóstico de red.

---

### 193. Competencias adquiridas

Al finalizar el capítulo debemos ser capaces de:

- Comprender la relación entre una dirección IP y un puerto.
- Diferenciar una prueba ICMP de una conexión TCP.
- Crear sockets TCP desde Python.
- Comprobar la accesibilidad de un puerto.
- Recorrer pequeños conjuntos o rangos de puertos.
- Establecer tiempos de espera.
- Resolver nombres mediante DNS.
- Obtener direcciones IPv4 e IPv6.
- Realizar consultas de resolución inversa.
- Controlar errores de red.
- Leer inventarios desde CSV.
- Automatizar comprobaciones sobre varios servicios.
- Generar informes.
- Registrar operaciones mediante `logging`.
- Construir herramientas de diagnóstico parametrizables.

---

### 194. Cierre del Capítulo 6

Con este capítulo hemos completado el bloque dedicado a:

```text
Diagnóstico básico de red
```

Nuestro recorrido ha sido:

```text
        RED
         │
    ┌────┴────┐
    │         │
    ▼         ▼
   DNS       TCP
    │         │
    ▼         ▼
 nombre     puerto
    │         │
    └────┬────┘
         ▼
     diagnóstico
         │
    ┌────┴────┐
    │         │
    ▼         ▼
 informe     log
```

!!! success "Capítulo 6 completado"

    Hemos desarrollado herramientas capaces de comprobar servicios de red mediante Python y hemos integrado los conocimientos de los capítulos anteriores en una aplicación completa de diagnóstico.

    Con este capítulo queda completado el bloque de **Utilidades de Red y Conectividad**.

---

### 195. Cierre del Módulo 2

Durante este módulo hemos trabajado dos grandes áreas.

En el **Capítulo 5**:

```text
HTTP
APIs
requests
GET
POST
JSON
```

En el **Capítulo 6**:

```text
socket
TCP
puertos
DNS
diagnóstico
```

Podemos resumir el módulo mediante:

```text
       PYTHON Y REDES
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
     HTTP           TCP
      │             │
      ▼             ▼
     API          socket
      │             │
      ▼             ▼
    JSON        puertos/DNS
      │             │
      └──────┬──────┘
             ▼
       automatización
         de redes
```

Con esto queda completado el:

```text
MÓDULO 2
Automatización de Redes y APIs
```

El siguiente bloque del libro será el **Módulo 3: Proyecto Final e Integración**.

Comenzaremos estudiando la **depuración profesional en VS Code**, trabajando con:

```text
breakpoints
variables durante la ejecución
ejecución paso a paso
pila de llamadas
consola de depuración
```

Después utilizaremos estos conocimientos para desarrollar el **proyecto final integrador del curso**.