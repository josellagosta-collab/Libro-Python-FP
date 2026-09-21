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

