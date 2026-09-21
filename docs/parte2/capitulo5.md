# Capítulo 5. Peticiones HTTP y consumo de APIs

Hasta ahora nuestros programas Python han trabajado principalmente con recursos del propio ordenador o de nuestra red local.

Hemos aprendido a:

- Leer y escribir archivos.
- Procesar archivos CSV.
- Trabajar con rutas y directorios.
- Ejecutar comandos del sistema.
- Automatizar tareas.
- Recibir argumentos desde la línea de comandos.
- Controlar excepciones.
- Registrar operaciones mediante logs.

En este capítulo daremos un paso más.

Nuestros programas comenzarán a comunicarse con **servicios disponibles a través de una red**.

Por ejemplo, un programa Python puede:

```text
consultar una página web
obtener nuestra IP pública
consultar información de un servidor
obtener datos meteorológicos
consultar el estado de un servicio
enviar información a una aplicación web
consumir una API
```

Para ello estudiaremos principalmente:

```text
HTTP
   │
   ▼
requests
   │
   ▼
GET / POST
   │
   ▼
respuestas HTTP
   │
   ▼
JSON
   │
   ▼
APIs
```

---

## 1. Comunicación HTTP desde Python

Cuando utilizamos un navegador para visitar una página web se produce una comunicación entre dos elementos:

```text
CLIENTE
   │
   │ petición
   ▼
SERVIDOR
   │
   │ respuesta
   ▼
CLIENTE
```

El navegador actúa como **cliente**.

El servidor web recibe una petición y devuelve una respuesta.

Por ejemplo:

```text
Navegador
    │
    │ GET
    ▼
Servidor web
    │
    │ respuesta
    ▼
Navegador
```

Python también puede actuar como cliente.

En lugar de utilizar un navegador podremos escribir un programa que realice la petición.

```text
Programa Python
      │
      │ petición HTTP
      ▼
Servidor
      │
      │ respuesta HTTP
      ▼
Programa Python
```

Esto permitirá automatizar la comunicación con servicios web.

---

### 2. ¿Qué es HTTP?

HTTP significa:

```text
HyperText Transfer Protocol
```

Es uno de los protocolos utilizados para intercambiar información entre clientes y servidores web.

Cuando escribimos una dirección en un navegador, por ejemplo:

```text
https://example.com
```

el navegador realiza una petición al servidor.

El servidor procesa esa petición y devuelve una respuesta.

De forma simplificada:

```text
CLIENTE                    SERVIDOR
   │                           │
   │ ------ petición --------> │
   │                           │
   │ <----- respuesta -------- │
   │                           │
```

HTTP utiliza diferentes tipos de peticiones.

En este capítulo trabajaremos principalmente con:

```text
GET
POST
```

---

### 3. El método GET

Una petición:

```text
GET
```

se utiliza habitualmente para **solicitar información** a un servidor.

Por ejemplo:

```text
GET /datos
```

podría solicitar determinada información.

El proceso sería:

```text
Python
   │
   │ GET /datos
   ▼
Servidor
   │
   │ datos solicitados
   ▼
Python
```

Algunos ejemplos de información que podríamos consultar son:

```text
IP pública
estado de un servicio
lista de dispositivos
datos meteorológicos
información de una aplicación
datos almacenados en un servidor
```

---

### 4. El método POST

Otro método que utilizaremos más adelante será:

```text
POST
```

Normalmente se utiliza para **enviar información al servidor**.

Por ejemplo:

```text
Python
   │
   │ POST
   │ datos
   ▼
Servidor
```

Podríamos utilizarlo para enviar:

```text
datos de un sensor
información de un equipo
un formulario
un registro
un nuevo elemento
```

Por ahora comenzaremos con:

```text
GET
```

porque resulta más sencillo para comprender el funcionamiento de las peticiones HTTP.

---

### 5. La biblioteca `requests`

Python permite realizar comunicaciones HTTP utilizando diferentes herramientas.

En este capítulo utilizaremos:

```python
requests
```

Esta biblioteca facilita enormemente el envío de peticiones HTTP.

Por ejemplo:

```python
requests.get(...)
```

permite realizar una petición:

```text
GET
```

y:

```python
requests.post(...)
```

permite realizar una petición:

```text
POST
```

Pero antes debemos instalarla.

---

### 6. Comprobar el entorno virtual

Antes de instalar una nueva biblioteca debemos comprobar que estamos trabajando dentro del entorno virtual del proyecto.

Abre el terminal integrado de VS Code.

Debemos encontrarnos en:

```text
C:\Users\aguileraj\Documents\Proyectos\Libro-Python-FP
```

Si el entorno virtual está activo, el terminal mostrará algo parecido a:

```text
(.venv)
```

al principio de la línea.

Por ejemplo:

```text
(.venv) PS C:\Users\aguileraj\Documents\Proyectos\Libro-Python-FP>
```

Si no está activo, desde PowerShell podemos ejecutar:

```powershell
.\.venv\Scripts\Activate.ps1
```

Después debería aparecer:

```text
(.venv)
```

!!! tip "Entorno virtual"

    Instalaremos `requests` dentro del entorno virtual del proyecto.

    De esta forma las dependencias del libro permanecen separadas de otras instalaciones de Python del ordenador.

---

### 7. Instalar `requests`

Con el entorno virtual activo ejecuta:

```powershell
python -m pip install requests
```

Durante la instalación aparecerán diferentes mensajes.

Al finalizar deberíamos ver que `requests` se ha instalado correctamente.

Podemos comprobarlo mediante:

```powershell
python -m pip show requests
```

Aparecerá información similar a:

```text
Name: requests
Version: ...
Summary: Python HTTP for Humans.
Location: ...
```

La versión exacta puede variar.

---

### 8. Comprobar que `requests` funciona

Vamos a realizar una prueba muy sencilla.

Dentro de:

```text
practicas/
```

crea:

```text
capitulo5/
```

y dentro:

```text
programas/
```

La estructura inicial será:

```text
practicas/
└── capitulo5/
    └── programas/
```

Dentro de:

```text
practicas/capitulo5/programas/
```

crea:

```text
probar_requests.py
```

Escribe:

```python
import requests


print(
    "requests importado "
    "correctamente."
)
```

Ejecuta:

```powershell
python probar_requests.py
```

Deberíamos obtener:

```text
requests importado correctamente.
```

Si aparece este mensaje, la biblioteca está preparada.

---

### 9. Nuestra primera petición HTTP

Vamos a realizar nuestra primera petición real.

Modifica:

```text
probar_requests.py
```

para que contenga:

```python
import requests


respuesta = requests.get(
    "https://example.com",
    timeout=10
)


print(
    respuesta
)
```

Ejecuta:

```powershell
python probar_requests.py
```

Podemos obtener algo parecido a:

```text
<Response [200]>
```

Acabamos de realizar una petición HTTP desde Python.

El proceso ha sido:

```text
probar_requests.py
       │
       ▼
requests.get()
       │
       ▼
https://example.com
       │
       ▼
servidor
       │
       ▼
respuesta HTTP
       │
       ▼
objeto Response
```

---

### 10. El objeto `Response`

La instrucción:

```python
respuesta = requests.get(
    "https://example.com",
    timeout=10
)
```

no guarda simplemente el texto de la página.

Guarda un objeto que representa la **respuesta HTTP**.

Podemos consultar diferentes propiedades de ese objeto.

Por ejemplo:

```python
respuesta.status_code
```

```python
respuesta.text
```

```python
respuesta.headers
```

Más adelante utilizaremos también:

```python
respuesta.json()
```

cuando el servidor devuelva datos JSON.

---

### 11. El código de estado HTTP

Modifica el programa:

```python
import requests


respuesta = requests.get(
    "https://example.com",
    timeout=10
)


print(
    f"Código HTTP: "
    f"{respuesta.status_code}"
)
```

Ejecuta:

```powershell
python probar_requests.py
```

Normalmente obtendremos:

```text
Código HTTP: 200
```

El número:

```text
200
```

es un **código de estado HTTP**.

Indica el resultado de la petición.

---

### 12. Algunos códigos HTTP importantes

Los códigos HTTP se agrupan en diferentes familias.

```text
1xx → información
2xx → operación correcta
3xx → redirección
4xx → problema relacionado con la petición
5xx → problema en el servidor
```

Algunos códigos habituales son:

```text
200 OK
```

La petición se ha procesado correctamente.

```text
201 Created
```

Se ha creado correctamente un recurso.

```text
301 Moved Permanently
```

El recurso ha sido movido permanentemente.

```text
400 Bad Request
```

La petición no es válida.

```text
401 Unauthorized
```

Es necesaria autenticación válida.

```text
403 Forbidden
```

El servidor rechaza el acceso al recurso.

```text
404 Not Found
```

El recurso solicitado no se encuentra.

```text
500 Internal Server Error
```

El servidor ha encontrado un problema interno.

!!! note "No memorices todos los códigos"

    No es necesario memorizar todos los códigos HTTP.

    Lo importante inicialmente es comprender las familias:

    ```text
    2xx → éxito
    4xx → problema con la petición
    5xx → problema en el servidor
    ```

---

### 13. Consultar el contenido de la respuesta

Podemos acceder al contenido textual mediante:

```python
respuesta.text
```

Modifica:

```text
probar_requests.py
```

Escribe:

```python
import requests


respuesta = requests.get(
    "https://example.com",
    timeout=10
)


print(
    f"Código HTTP: "
    f"{respuesta.status_code}"
)

print()
print("CONTENIDO")
print("=========")
print()

print(
    respuesta.text
)
```

Ejecuta:

```powershell
python probar_requests.py
```

Ahora veremos el código HTML recibido desde el servidor.

El proceso completo es:

```text
Python
   │
   │ GET
   ▼
example.com
   │
   │ HTTP 200
   │ HTML
   ▼
Python
   │
   ▼
respuesta.text
```

---

### 14. Python no es un navegador

Cuando hacemos:

```python
requests.get(...)
```

Python obtiene la respuesta del servidor.

Pero no representa gráficamente la página como haría Chrome, Edge o Firefox.

Si el servidor devuelve:

```html
<h1>Ejemplo</h1>
```

el navegador interpreta ese HTML y lo representa visualmente.

Nuestro programa recibe simplemente los datos.

```text
NAVEGADOR

HTML
 │
 ▼
interpretación
 │
 ▼
página visual


PYTHON + REQUESTS

HTML
 │
 ▼
texto/datos
 │
 ▼
procesamiento
```

Esto es precisamente lo que nos interesa.

Queremos que nuestros programas puedan **procesar automáticamente las respuestas**.

---

### 15. Consultar las cabeceras HTTP

Una respuesta HTTP contiene también cabeceras.

Podemos consultarlas mediante:

```python
respuesta.headers
```

Por ejemplo:

```python
import requests


respuesta = requests.get(
    "https://example.com",
    timeout=10
)


print(
    respuesta.headers
)
```

Las cabeceras contienen información adicional sobre la respuesta.

Podemos consultar una cabecera concreta.

Por ejemplo:

```python
print(
    respuesta.headers.get(
        "Content-Type"
    )
)
```

Podemos obtener algo parecido a:

```text
text/html
```

Esto nos indica qué tipo de contenido ha enviado el servidor.

---

### 16. `Content-Type`

Una cabecera especialmente importante es:

```text
Content-Type
```

Puede indicar diferentes tipos de contenido.

Por ejemplo:

```text
text/html
```

contenido HTML.

```text
text/plain
```

texto.

```text
application/json
```

datos JSON.

Esta última será especialmente importante cuando comencemos a trabajar con APIs.

```text
Content-Type
     │
     ├── text/html
     ├── text/plain
     └── application/json
```

---

### 17. Comprobar si la petición ha sido correcta

Podemos comprobar:

```python
respuesta.status_code
```

Por ejemplo:

```python
if respuesta.status_code == 200:

    print(
        "Petición correcta."
    )

else:

    print(
        "La petición no ha "
        "devuelto HTTP 200."
    )
```

Programa completo:

```python
import requests


respuesta = requests.get(
    "https://example.com",
    timeout=10
)


if respuesta.status_code == 200:

    print(
        "Petición correcta."
    )

else:

    print(
        f"Error HTTP: "
        f"{respuesta.status_code}"
    )
```

---

### 18. El método `raise_for_status()`

`requests` dispone de otro mecanismo muy útil:

```python
respuesta.raise_for_status()
```

Este método comprueba el código HTTP.

Si se ha producido un error HTTP, genera una excepción.

Por ejemplo:

```python
import requests


respuesta = requests.get(
    "https://example.com",
    timeout=10
)

respuesta.raise_for_status()


print(
    "Petición realizada "
    "correctamente."
)
```

Esto nos permitirá combinar `requests` con el control de excepciones estudiado en el capítulo anterior.

---

### 19. Errores de red

Cuando trabajamos con Internet pueden producirse problemas que no aparecían al trabajar únicamente con archivos locales.

Por ejemplo:

```text
servidor no disponible
problema de conexión
nombre DNS incorrecto
tiempo de espera agotado
respuesta HTTP de error
```

Por eso no deberíamos asumir que:

```python
requests.get(...)
```

siempre funcionará.

---

### 20. Controlar errores con `requests`

Vamos a crear:

```text
get_seguro.py
```

Escribe:

```python
import requests


url = "https://example.com"


try:

    respuesta = requests.get(
        url,
        timeout=10
    )

    respuesta.raise_for_status()

except requests.exceptions.Timeout:

    print(
        "ERROR: se ha superado "
        "el tiempo de espera."
    )

except requests.exceptions.ConnectionError:

    print(
        "ERROR: no se ha podido "
        "establecer la conexión."
    )

except requests.exceptions.HTTPError as error:

    print(
        f"ERROR HTTP: {error}"
    )

except requests.exceptions.RequestException as error:

    print(
        f"ERROR en la petición: "
        f"{error}"
    )

else:

    print(
        "Petición realizada "
        "correctamente."
    )

    print(
        f"Código HTTP: "
        f"{respuesta.status_code}"
    )
```

Aquí estamos aplicando directamente lo aprendido en el capítulo anterior.

---

### 21. Jerarquía de errores de `requests`

`requests` dispone de diferentes excepciones.

En este momento nos interesan principalmente:

```text
RequestException
      │
      ├── ConnectionError
      │
      ├── Timeout
      │
      └── HTTPError
```

Podemos interpretarlas así:

```text
ConnectionError
    problema estableciendo
    la conexión


Timeout
    la operación ha tardado
    demasiado


HTTPError
    respuesta HTTP considerada
    errónea


RequestException
    error general relacionado
    con requests
```

!!! tip "Orden de los `except`"

    Las excepciones más concretas deben comprobarse antes que las más generales.

    Por eso dejamos:

    ```python
    except requests.exceptions.RequestException:
    ```

    para el final.

---

### 22. ¿Por qué utilizar `timeout`?

Observa que nuestros ejemplos utilizan:

```python
timeout=10
```

Por ejemplo:

```python
requests.get(
    url,
    timeout=10
)
```

Esto evita que el programa pueda permanecer esperando indefinidamente una respuesta.

Si el servidor o la conexión no responden adecuadamente, `requests` puede generar:

```python
requests.exceptions.Timeout
```

que podemos controlar.

!!! warning "Utiliza tiempos de espera"

    En scripts de administración es recomendable establecer tiempos de espera en las operaciones de red.

    Un servicio que no responde no debería bloquear indefinidamente todo nuestro programa.

---

### 23. Crear una función reutilizable

Vamos a encapsular la petición en una función.

Crea:

```text
cliente_http.py
```

Escribe:

```python
import requests


def obtener_url(url):

    try:

        respuesta = requests.get(
            url,
            timeout=10
        )

        respuesta.raise_for_status()

    except requests.exceptions.Timeout:

        print(
            "ERROR: tiempo de "
            "espera agotado."
        )

        return None

    except requests.exceptions.ConnectionError:

        print(
            "ERROR: no se ha podido "
            "conectar."
        )

        return None

    except requests.exceptions.HTTPError as error:

        print(
            f"ERROR HTTP: {error}"
        )

        return None

    except requests.exceptions.RequestException as error:

        print(
            f"ERROR: {error}"
        )

        return None

    else:

        return respuesta
```

Después podemos utilizar:

```python
respuesta = obtener_url(
    "https://example.com"
)


if respuesta is not None:

    print(
        f"Código HTTP: "
        f"{respuesta.status_code}"
    )

    print(
        f"Tipo: "
        f"{respuesta.headers.get('Content-Type')}"
    )
```

La función:

```python
obtener_url()
```

podrá reutilizarse con diferentes direcciones.

---

### 24. Recibir la URL mediante `argparse`

Vamos a combinar este capítulo con el anterior.

Crea:

```text
consultar_web.py
```

Escribe:

```python
import argparse

import requests


parser = argparse.ArgumentParser(
    description=(
        "Consulta una dirección "
        "web mediante HTTP."
    )
)

parser.add_argument(
    "url",
    help=(
        "URL que se consultará"
    )
)

args = parser.parse_args()


try:

    respuesta = requests.get(
        args.url,
        timeout=10
    )

    respuesta.raise_for_status()

except requests.exceptions.Timeout:

    print(
        "ERROR: tiempo de "
        "espera agotado."
    )

except requests.exceptions.ConnectionError:

    print(
        "ERROR: no se ha podido "
        "establecer la conexión."
    )

except requests.exceptions.HTTPError as error:

    print(
        f"ERROR HTTP: {error}"
    )

except requests.exceptions.RequestException as error:

    print(
        f"ERROR: {error}"
    )

else:

    print()
    print("RESULTADO HTTP")
    print("==============")
    print()

    print(
        f"URL: {args.url}"
    )

    print(
        f"Código: "
        f"{respuesta.status_code}"
    )

    print(
        f"Tipo: "
        f"{respuesta.headers.get('Content-Type')}"
    )

    print(
        f"Tamaño: "
        f"{len(respuesta.content)} bytes"
    )
```

Podemos ejecutar:

```powershell
python consultar_web.py https://example.com
```

---

### 25. Añadir `logging`

Podemos incorporar también el registro aprendido en el capítulo 4.

Añade:

```python
import logging
```

y configura:

```python
logging.basicConfig(
    filename="http.log",
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    ),
    datefmt=(
        "%Y-%m-%d %H:%M:%S"
    )
)
```

Antes de realizar la petición:

```python
logging.info(
    f"Consultando {args.url}"
)
```

Si se produce un error:

```python
logging.error(
    f"Error consultando "
    f"{args.url}"
)
```

Si la petición funciona:

```python
logging.info(
    f"Respuesta HTTP "
    f"{respuesta.status_code} "
    f"de {args.url}"
)
```

De esta forma empezamos a integrar los diferentes capítulos:

```text
Capítulo 4
argparse
excepciones
logging
     │
     ▼
Capítulo 5
requests
HTTP
```

---

### 26. Práctica guiada: comprobar una página web

Crea:

```text
comprobar_web.py
```

El programa deberá recibir:

```powershell
python comprobar_web.py https://example.com
```

y mostrar:

```text
COMPROBACIÓN WEB
================

URL: https://example.com
Código HTTP: 200
Estado: DISPONIBLE
Tipo: text/html
```

El programa deberá utilizar:

```text
argparse
requests
timeout
try / except
raise_for_status()
```

Si se produce un problema de conexión deberá mostrar un mensaje comprensible.

---

### 27. Práctica propuesta: comprobador de varios servicios

Crea:

```text
comprobar_servicios.py
```

Dentro del programa define inicialmente:

```python
servicios = [
    "https://example.com",
    "https://www.python.org"
]
```

El programa deberá recorrer la lista:

```python
for url in servicios:
```

y realizar una petición a cada servicio.

El resultado podría ser:

```text
COMPROBACIÓN DE SERVICIOS
=========================

https://example.com
HTTP: 200
Estado: DISPONIBLE

https://www.python.org
HTTP: 200
Estado: DISPONIBLE
```

Si alguno no responde, el programa debe continuar comprobando los demás.

!!! note "Automatización"

    Observa que estamos aplicando nuevamente el patrón estudiado en capítulos anteriores:

    ```text
    lista de elementos
          │
          ▼
        bucle
          │
          ▼
       operación
          │
          ▼
      comprobación
          │
          ▼
       resultado
    ```

    La diferencia es que ahora la operación se realiza mediante HTTP.

---

### 28. HTTP frente a `ping`

Hasta ahora habíamos utilizado:

```text
ping
```

para comprobar conectividad.

Ahora podemos utilizar:

```text
HTTP
```

para comprobar un servicio web.

No responden exactamente a la misma pregunta.

```text
PING

¿Existe conectividad IP
y obtenemos respuesta ICMP?


HTTP

¿Podemos comunicarnos con
el servicio web?
```

Un servidor podría no responder a `ping` y, sin embargo, tener su servicio web disponible.

También podría ocurrir que el equipo estuviera accesible pero el servicio web tuviera un problema.

Por tanto:

```text
equipo accesible
```

y:

```text
servicio web disponible
```

no significan exactamente lo mismo.

---

### 29. De una página web a una API

Hasta ahora hemos realizado una petición a:

```text
https://example.com
```

y hemos recibido principalmente:

```text
HTML
```

Pero un programa normalmente no necesita una página diseñada para que la vea una persona.

Es mucho más útil recibir información estructurada.

Por ejemplo:

```text
IP: 203.0.113.10
Ciudad: Barcelona
Estado: activo
```

Los servicios destinados a ser utilizados por otros programas suelen proporcionar la información mediante una **API**.

En muchas APIs encontraremos respuestas en formato:

```text
JSON
```

En lugar de recibir:

```html
<h1>Servidor activo</h1>
```

podríamos recibir:

```json
{
    "servidor": "web01",
    "estado": "activo"
}
```

Python puede procesar esta información fácilmente.

Este será nuestro siguiente paso.

---

## Resumen

En esta primera parte del capítulo hemos aprendido que Python puede actuar como cliente HTTP:

```text
Python
   │
   │ petición HTTP
   ▼
Servidor
   │
   │ respuesta HTTP
   ▼
Python
```

Hemos instalado y utilizado:

```python
requests
```

y realizado nuestra primera petición:

```python
requests.get(
    url,
    timeout=10
)
```

Hemos aprendido a consultar:

```python
respuesta.status_code
```

```python
respuesta.text
```

```python
respuesta.headers
```

y hemos introducido:

```python
respuesta.raise_for_status()
```

También hemos estudiado algunos códigos HTTP:

```text
2xx → éxito
3xx → redirección
4xx → problema con la petición
5xx → problema en el servidor
```

y hemos combinado `requests` con el control de excepciones:

```text
Timeout
ConnectionError
HTTPError
RequestException
```

Finalmente hemos conectado lo aprendido en capítulos anteriores:

```text
argparse
    +
excepciones
    +
logging
    +
requests
```

para comenzar a construir herramientas capaces de comprobar servicios web.

Hasta ahora las respuestas que hemos procesado han sido principalmente HTML.

En la siguiente parte comenzaremos a trabajar con **APIs y JSON**, utilizando:

```python
respuesta.json()
```

para convertir las respuestas de los servicios web en estructuras de datos que Python puede procesar directamente.

---

## 30. Introducción a las APIs y JSON

En la primera parte del capítulo hemos realizado peticiones HTTP con:

```python
requests.get()
```

y hemos recibido respuestas de servidores web.

Por ejemplo:

```python
respuesta = requests.get(
    "https://example.com",
    timeout=10
)
```

En este caso el servidor devuelve principalmente:

```text
HTML
```

El HTML está pensado fundamentalmente para representar páginas que serán visualizadas por una persona mediante un navegador.

Sin embargo, cuando dos programas necesitan intercambiar información resulta más útil utilizar datos estructurados.

Aquí aparecen dos conceptos fundamentales:

```text
API
```

y:

```text
JSON
```

---

### 31. ¿Qué es una API?

API significa:

```text
Application Programming Interface
```

Una API permite que diferentes programas o servicios se comuniquen siguiendo unas reglas determinadas.

Podemos imaginar una API como un intermediario:

```text
PROGRAMA PYTHON
       │
       │ petición
       ▼
      API
       │
       ▼
  APLICACIÓN
  O SERVICIO
       │
       ▼
      API
       │
       │ respuesta
       ▼
PROGRAMA PYTHON
```

Nuestro programa no necesita conocer cómo funciona internamente el servidor.

Solo necesita conocer:

```text
qué dirección debe consultar
qué información debe enviar
qué respuesta recibirá
```

---

### 32. Ejemplo conceptual de una API

Imaginemos un servicio que proporciona información sobre equipos.

Podríamos realizar:

```text
GET /equipos/PC01
```

y recibir:

```json
{
    "nombre": "PC01",
    "ip": "192.168.1.20",
    "estado": "activo"
}
```

Nuestro programa Python podría utilizar esos datos.

Por ejemplo:

```text
API
 │
 ▼
JSON
 │
 ▼
Python
 │
 ├── nombre
 ├── ip
 └── estado
```

---

### 33. ¿Qué es JSON?

JSON significa:

```text
JavaScript Object Notation
```

Es un formato de texto utilizado ampliamente para intercambiar información estructurada.

Por ejemplo:

```json
{
    "nombre": "PC01",
    "ip": "192.168.1.20",
    "activo": true
}
```

Podemos observar una estructura formada por:

```text
clave : valor
```

Por ejemplo:

```text
"nombre" : "PC01"
```

```text
"ip" : "192.168.1.20"
```

```text
"activo" : true
```

---

### 34. JSON y los diccionarios de Python

JSON se parece mucho a los diccionarios que ya conocemos en Python.

JSON:

```json
{
    "nombre": "PC01",
    "ip": "192.168.1.20"
}
```

Python:

```python
equipo = {
    "nombre": "PC01",
    "ip": "192.168.1.20"
}
```

Por esta razón resulta muy cómodo trabajar con respuestas JSON desde Python.

Cuando `requests` procesa un objeto JSON, normalmente podremos trabajar con estructuras como:

```text
dict
list
str
int
float
bool
None
```

---

### 35. Algunas diferencias entre JSON y Python

Aunque visualmente se parecen, JSON y Python no son exactamente lo mismo.

Por ejemplo, JSON utiliza:

```json
true
false
null
```

Python utiliza:

```python
True
False
None
```

Por ejemplo, este JSON:

```json
{
    "activo": true,
    "error": null
}
```

al convertirse a estructuras Python corresponderá conceptualmente a:

```python
{
    "activo": True,
    "error": None
}
```

No necesitamos realizar estas conversiones manualmente cuando utilizamos:

```python
respuesta.json()
```

---

### 36. Nuestra primera API

Vamos a utilizar una API pública sencilla para realizar nuestras primeras pruebas.

Dentro de:

```text
practicas/capitulo5/programas/
```

crea:

```text
primera_api.py
```

Escribe:

```python
import requests


url = (
    "https://jsonplaceholder.typicode.com/"
    "users/1"
)


respuesta = requests.get(
    url,
    timeout=10
)


print(
    f"Código HTTP: "
    f"{respuesta.status_code}"
)

print()

print(
    respuesta.text
)
```

Ejecuta:

```powershell
python primera_api.py
```

Recibiremos información estructurada sobre un usuario de prueba.

!!! note "API de pruebas"

    JSONPlaceholder es un servicio pensado para realizar pruebas y ejemplos.

    Los datos que devuelve son ficticios y resultan adecuados para aprender a consumir APIs sin modificar información real.

---

### 37. Comprobar el tipo de contenido

Podemos consultar:

```python
respuesta.headers.get(
    "Content-Type"
)
```

Modifica el programa:

```python
print(
    f"Tipo: "
    f"{respuesta.headers.get('Content-Type')}"
)
```

La respuesta indicará un tipo relacionado con:

```text
application/json
```

Esto nos informa de que el servidor está devolviendo JSON.

---

### 38. `respuesta.text` frente a `respuesta.json()`

Hasta ahora hemos utilizado:

```python
respuesta.text
```

Esto devuelve el contenido como texto.

Pero si sabemos que la respuesta contiene JSON podemos utilizar:

```python
respuesta.json()
```

Modifica:

```text
primera_api.py
```

Escribe:

```python
import requests


url = (
    "https://jsonplaceholder.typicode.com/"
    "users/1"
)


respuesta = requests.get(
    url,
    timeout=10
)

respuesta.raise_for_status()


datos = respuesta.json()


print(
    datos
)
```

Ahora:

```python
datos
```

ya no contiene simplemente el texto recibido.

Contiene una estructura de datos Python.

---

### 39. Comprobar el tipo recibido

Añade:

```python
print(
    type(datos)
)
```

Obtendremos:

```text
<class 'dict'>
```

Esto significa que podemos trabajar con:

```python
datos
```

como con cualquier otro diccionario.

Por ejemplo:

```python
print(
    datos["name"]
)
```

También:

```python
print(
    datos["email"]
)
```

---

### 40. Acceder a los datos de la API

Podemos mostrar únicamente la información que nos interesa:

```python
print(
    f"Nombre: "
    f"{datos['name']}"
)

print(
    f"Usuario: "
    f"{datos['username']}"
)

print(
    f"Email: "
    f"{datos['email']}"
)
```

Observa lo que hemos conseguido:

```text
SERVIDOR
   │
   ▼
respuesta JSON
   │
   ▼
respuesta.json()
   │
   ▼
diccionario Python
   │
   ▼
datos["name"]
datos["email"]
```

Ya no necesitamos analizar manualmente el texto de la respuesta.

---

### 41. Datos JSON anidados

Una respuesta JSON puede contener estructuras dentro de otras estructuras.

Por ejemplo, los datos recibidos incluyen información de dirección.

Podemos acceder a:

```python
datos["address"]
```

Esto devuelve otro diccionario.

Podemos comprobarlo:

```python
direccion = datos["address"]

print(
    type(direccion)
)
```

Obtendremos:

```text
<class 'dict'>
```

Ahora podemos acceder a:

```python
direccion["city"]
```

Por ejemplo:

```python
print(
    f"Ciudad: "
    f"{datos['address']['city']}"
)
```

La estructura es:

```text
datos
 │
 ├── name
 ├── username
 ├── email
 │
 └── address
       │
       ├── street
       ├── suite
       ├── city
       └── zipcode
```

---

### 42. Crear una ficha a partir de una API

Crea:

```text
ficha_usuario.py
```

Escribe:

```python
import requests


url = (
    "https://jsonplaceholder.typicode.com/"
    "users/1"
)


try:

    respuesta = requests.get(
        url,
        timeout=10
    )

    respuesta.raise_for_status()

except requests.exceptions.RequestException as error:

    print(
        f"ERROR: {error}"
    )

else:

    datos = respuesta.json()

    print()
    print("FICHA DEL USUARIO")
    print("=================")
    print()

    print(
        f"Nombre: "
        f"{datos['name']}"
    )

    print(
        f"Usuario: "
        f"{datos['username']}"
    )

    print(
        f"Email: "
        f"{datos['email']}"
    )

    print(
        f"Ciudad: "
        f"{datos['address']['city']}"
    )

    print(
        f"Empresa: "
        f"{datos['company']['name']}"
    )
```

Ahora nuestro programa transforma una respuesta JSON en información seleccionada y presentada de forma comprensible.

---

### 43. Listas dentro de JSON

Una API también puede devolver una lista.

Cambia la URL por:

```python
url = (
    "https://jsonplaceholder.typicode.com/"
    "users"
)
```

Ahora la API devuelve varios usuarios.

Podemos hacer:

```python
datos = respuesta.json()

print(
    type(datos)
)
```

En este caso obtendremos:

```text
<class 'list'>
```

La estructura conceptual es:

```text
lista
 │
 ├── usuario 1
 │      ├── name
 │      ├── email
 │      └── ...
 │
 ├── usuario 2
 │      ├── name
 │      ├── email
 │      └── ...
 │
 └── usuario ...
```

---

### 44. Recorrer una respuesta JSON

Crea:

```text
listar_usuarios.py
```

Escribe:

```python
import requests


url = (
    "https://jsonplaceholder.typicode.com/"
    "users"
)


try:

    respuesta = requests.get(
        url,
        timeout=10
    )

    respuesta.raise_for_status()

except requests.exceptions.RequestException as error:

    print(
        f"ERROR: {error}"
    )

else:

    usuarios = respuesta.json()

    print()
    print("USUARIOS")
    print("========")
    print()

    for usuario in usuarios:

        print(
            f"{usuario['name']} "
            f"- {usuario['email']}"
        )
```

Aquí estamos combinando:

```text
HTTP
 │
 ▼
JSON
 │
 ▼
lista Python
 │
 ▼
for
 │
 ▼
diccionario
```

---

### 45. Contar elementos recibidos

Como:

```python
usuarios
```

es una lista, podemos utilizar:

```python
len()
```

Por ejemplo:

```python
print(
    f"Usuarios recibidos: "
    f"{len(usuarios)}"
)
```

Este patrón será frecuente cuando trabajemos con APIs:

```python
datos = respuesta.json()

for elemento in datos:

    # procesar elemento
```

---

### 46. Utilizar `.get()` con diccionarios

Hasta ahora hemos utilizado:

```python
datos["email"]
```

Si la clave:

```text
email
```

no existe, Python puede generar:

```text
KeyError
```

En algunas situaciones podemos utilizar:

```python
datos.get("email")
```

Por ejemplo:

```python
email = datos.get(
    "email"
)
```

Si la clave no existe, obtendremos:

```python
None
```

También podemos proporcionar un valor predeterminado:

```python
email = datos.get(
    "email",
    "No disponible"
)
```

Esto puede resultar útil cuando una API contiene campos opcionales.

---

### 47. ¿Puede fallar `respuesta.json()`?

Sí.

No debemos asumir que cualquier respuesta HTTP contiene JSON válido.

Por ejemplo, un servidor podría devolver:

```text
HTML
```

o:

```text
texto
```

Si intentamos convertir una respuesta que no contiene JSON válido:

```python
datos = respuesta.json()
```

puede producirse un error de decodificación.

Por tanto, en programas robustos también debemos tenerlo en cuenta.

---

### 48. Controlar errores al procesar JSON

Podemos escribir:

```python
import requests


url = (
    "https://jsonplaceholder.typicode.com/"
    "users/1"
)


try:

    respuesta = requests.get(
        url,
        timeout=10
    )

    respuesta.raise_for_status()

    datos = respuesta.json()

except requests.exceptions.Timeout:

    print(
        "ERROR: tiempo de "
        "espera agotado."
    )

except requests.exceptions.ConnectionError:

    print(
        "ERROR: problema "
        "de conexión."
    )

except requests.exceptions.HTTPError as error:

    print(
        f"ERROR HTTP: {error}"
    )

except requests.exceptions.JSONDecodeError:

    print(
        "ERROR: la respuesta "
        "no contiene JSON válido."
    )

except requests.exceptions.RequestException as error:

    print(
        f"ERROR: {error}"
    )

else:

    print(
        datos
    )
```

Ahora nuestro programa controla tanto problemas de comunicación como problemas al interpretar la respuesta.

---

### 49. Separar descarga y procesamiento

Una buena práctica consiste en separar diferentes responsabilidades.

Por ejemplo:

```python
def obtener_datos(url):

    try:

        respuesta = requests.get(
            url,
            timeout=10
        )

        respuesta.raise_for_status()

        return respuesta.json()

    except requests.exceptions.RequestException as error:

        print(
            f"ERROR HTTP: {error}"
        )

        return None
```

Después:

```python
datos = obtener_datos(
    url
)


if datos is not None:

    print(
        datos
    )
```

Ahora tenemos:

```text
obtener_datos()
      │
      ├── petición HTTP
      ├── comprobación
      ├── JSON
      └── errores
```

El resto del programa puede concentrarse en procesar los datos.

---

### 50. Consultar un usuario desde la línea de comandos

Vamos a combinar la API con `argparse`.

Crea:

```text
consultar_usuario.py
```

Escribe:

```python
import argparse

import requests


parser = argparse.ArgumentParser(
    description=(
        "Consulta un usuario "
        "mediante una API."
    )
)

parser.add_argument(
    "id",
    type=int,
    help="Identificador del usuario"
)

args = parser.parse_args()


if args.id < 1:

    parser.error(
        "El identificador debe "
        "ser mayor que cero."
    )


url = (
    "https://jsonplaceholder.typicode.com/"
    f"users/{args.id}"
)


try:

    respuesta = requests.get(
        url,
        timeout=10
    )

    respuesta.raise_for_status()

    datos = respuesta.json()

except requests.exceptions.Timeout:

    print(
        "ERROR: tiempo de "
        "espera agotado."
    )

except requests.exceptions.ConnectionError:

    print(
        "ERROR: no se ha podido "
        "establecer la conexión."
    )

except requests.exceptions.HTTPError as error:

    print(
        f"ERROR HTTP: {error}"
    )

except requests.exceptions.JSONDecodeError:

    print(
        "ERROR: respuesta JSON "
        "no válida."
    )

except requests.exceptions.RequestException as error:

    print(
        f"ERROR: {error}"
    )

else:

    print()
    print("DATOS DEL USUARIO")
    print("=================")
    print()

    print(
        f"ID: "
        f"{datos.get('id')}"
    )

    print(
        f"Nombre: "
        f"{datos.get('name')}"
    )

    print(
        f"Usuario: "
        f"{datos.get('username')}"
    )

    print(
        f"Email: "
        f"{datos.get('email')}"
    )
```

Ahora podemos ejecutar:

```powershell
python consultar_usuario.py 1
```

También:

```powershell
python consultar_usuario.py 5
```

La misma aplicación consulta diferentes recursos sin modificar el código.

---

### 51. ¿Qué es un endpoint?

En una API encontraremos frecuentemente el término:

```text
endpoint
```

Un endpoint es una dirección concreta de la API que permite acceder a un recurso o realizar una operación.

Por ejemplo:

```text
https://jsonplaceholder.typicode.com/users
```

podría representar el conjunto de usuarios.

Mientras que:

```text
https://jsonplaceholder.typicode.com/users/1
```

representa un usuario concreto.

Podemos verlo así:

```text
API
 │
 ├── /users
 │
 │     lista de usuarios
 │
 ├── /users/1
 │
 │     usuario 1
 │
 └── /users/2
       usuario 2
```

La documentación de cada API nos indicará qué endpoints están disponibles.

---

### 52. Parámetros de consulta

Muchas APIs permiten enviar parámetros en la propia URL.

Podemos encontrar direcciones como:

```text
/recurso?parametro=valor
```

La parte situada después de:

```text
?
```

contiene parámetros de consulta.

Por ejemplo:

```text
/posts?userId=1
```

indica que queremos filtrar los elementos utilizando:

```text
userId=1
```

---

### 53. Enviar parámetros con `requests`

No es necesario construir manualmente:

```text
?userId=1
```

Podemos utilizar:

```python
params
```

Por ejemplo:

```python
import requests


url = (
    "https://jsonplaceholder.typicode.com/"
    "posts"
)


parametros = {
    "userId": 1
}


respuesta = requests.get(
    url,
    params=parametros,
    timeout=10
)


respuesta.raise_for_status()


datos = respuesta.json()


print(
    f"Elementos recibidos: "
    f"{len(datos)}"
)
```

`requests` construirá la URL correspondiente.

Podemos comprobarla mediante:

```python
print(
    respuesta.url
)
```

---

### 54. Ventajas de utilizar `params`

En lugar de construir:

```python
url = (
    "https://servidor/recurso"
    "?userId=1"
)
```

podemos separar:

```python
url = (
    "https://servidor/recurso"
)

parametros = {
    "userId": 1
}
```

y realizar:

```python
requests.get(
    url,
    params=parametros
)
```

Esto hace que el código sea más claro, especialmente cuando tenemos varios parámetros.

---

### 55. Práctica guiada: consultar publicaciones

Crea:

```text
consultar_posts.py
```

Escribe:

```python
import argparse

import requests


parser = argparse.ArgumentParser(
    description=(
        "Consulta publicaciones "
        "de un usuario."
    )
)

parser.add_argument(
    "usuario",
    type=int,
    help="ID del usuario"
)

args = parser.parse_args()


url = (
    "https://jsonplaceholder.typicode.com/"
    "posts"
)


parametros = {
    "userId": args.usuario
}


try:

    respuesta = requests.get(
        url,
        params=parametros,
        timeout=10
    )

    respuesta.raise_for_status()

    publicaciones = (
        respuesta.json()
    )

except requests.exceptions.RequestException as error:

    print(
        f"ERROR: {error}"
    )

else:

    print()
    print("PUBLICACIONES")
    print("=============")
    print()

    print(
        f"Usuario: "
        f"{args.usuario}"
    )

    print(
        f"Total: "
        f"{len(publicaciones)}"
    )

    print()

    for publicacion in publicaciones:

        print(
            f"ID: "
            f"{publicacion['id']}"
        )

        print(
            f"Título: "
            f"{publicacion['title']}"
        )

        print()
```

Ejecuta:

```powershell
python consultar_posts.py 1
```

---

### 56. Obtener nuestra IP pública

Ahora vamos a realizar una aplicación más relacionada con administración de sistemas y redes.

Existen servicios web que devuelven la dirección IP pública desde la que se realiza una petición.

Conceptualmente:

```text
Nuestro PC
    │
    │ Internet
    ▼
Servicio web
    │
    │ detecta IP origen
    ▼
respuesta JSON
    │
    ▼
Python
```

Un servicio de este tipo puede devolver:

```json
{
    "ip": "203.0.113.25"
}
```

Nuestro programa podría hacer:

```python
datos = respuesta.json()

ip = datos["ip"]
```

!!! note "Direcciones de los ejemplos"

    Las direcciones IP utilizadas en las explicaciones son ejemplos.

    La dirección obtenida al consultar un servicio real dependerá de la conexión desde la que se ejecute el programa.

---

### 57. Programa para consultar la IP pública

Crea:

```text
ip_publica.py
```

Podemos utilizar un servicio que devuelva la dirección en formato JSON.

La estructura del programa será:

```python
import requests


url = (
    "https://api.ipify.org"
)


parametros = {
    "format": "json"
}


try:

    respuesta = requests.get(
        url,
        params=parametros,
        timeout=10
    )

    respuesta.raise_for_status()

    datos = respuesta.json()

except requests.exceptions.Timeout:

    print(
        "ERROR: tiempo de "
        "espera agotado."
    )

except requests.exceptions.ConnectionError:

    print(
        "ERROR: problema "
        "de conexión."
    )

except requests.exceptions.JSONDecodeError:

    print(
        "ERROR: respuesta JSON "
        "no válida."
    )

except requests.exceptions.RequestException as error:

    print(
        f"ERROR: {error}"
    )

else:

    ip = datos.get(
        "ip"
    )

    print()
    print("DIRECCIÓN IP PÚBLICA")
    print("====================")
    print()

    print(
        f"IP: {ip}"
    )
```

Ejecuta:

```powershell
python ip_publica.py
```

La dirección mostrada será la dirección pública observada por el servicio.

!!! note "IP pública"

    Si los equipos de una red utilizan NAT, varios dispositivos de la red local pueden aparecer en Internet utilizando la misma dirección IP pública.

---

### 58. Guardar datos obtenidos de una API

También podemos guardar los resultados.

Por ejemplo:

```python
from pathlib import Path


archivo = Path(
    "../resultados/ip_publica.txt"
)


archivo.parent.mkdir(
    parents=True,
    exist_ok=True
)


archivo.write_text(
    f"IP pública: {ip}\n",
    encoding="utf-8"
)
```

De esta forma combinamos:

```text
API
 │
 ▼
JSON
 │
 ▼
Python
 │
 ▼
procesamiento
 │
 ▼
archivo
```

---

### 59. Guardar JSON completo

Python incluye el módulo:

```python
json
```

que permite trabajar con JSON.

Por ejemplo:

```python
import json
```

Si tenemos:

```python
datos = respuesta.json()
```

podemos guardar esa estructura en un archivo:

```python
with open(
    "respuesta.json",
    "w",
    encoding="utf-8"
) as archivo:

    json.dump(
        datos,
        archivo,
        indent=4,
        ensure_ascii=False
    )
```

El parámetro:

```python
indent=4
```

hace que el archivo resulte más fácil de leer.

---

### 60. Práctica: guardar usuarios en JSON

Crea:

```text
guardar_usuarios.py
```

El programa deberá:

1. Consultar:

```text
/users
```

2. Convertir la respuesta mediante:

```python
respuesta.json()
```

3. Crear:

```text
resultados/
```

si no existe.

4. Guardar:

```text
usuarios.json
```

5. Mostrar cuántos usuarios se han almacenado.

El resultado podría ser:

```text
DESCARGA COMPLETADA
===================

Usuarios: 10
Archivo: resultados/usuarios.json
```

---

### 61. Añadir logs a nuestras consultas

Podemos combinar nuevamente:

```text
requests
+
JSON
+
logging
```

Por ejemplo:

```python
logging.info(
    f"Consultando API: {url}"
)
```

Si funciona:

```python
logging.info(
    f"Respuesta HTTP: "
    f"{respuesta.status_code}"
)
```

Si falla:

```python
logging.error(
    f"Error consultando {url}"
)
```

Esto resulta especialmente útil cuando las consultas se realizan automáticamente.

---

### 62. Patrón de consumo de una API

Ya podemos establecer un patrón general:

```text
      DEFINIR URL
           │
           ▼
       PARÁMETROS
           │
           ▼
     requests.get()
           │
           ▼
       RESPUESTA
           │
           ▼
    status / errores
           │
           ▼
  respuesta.json()
           │
           ▼
     datos Python
           │
           ▼
      procesar
           │
           ▼
 mostrar / guardar
```

En código:

```python
try:

    respuesta = requests.get(
        url,
        params=parametros,
        timeout=10
    )

    respuesta.raise_for_status()

    datos = respuesta.json()

except requests.exceptions.RequestException as error:

    print(
        f"ERROR: {error}"
    )

else:

    # Procesar datos
    ...
```

Este patrón aparecerá frecuentemente cuando trabajemos con APIs.

---

### 63. Práctica integradora de esta parte

Crea:

```text
consulta_api.py
```

El programa permitirá ejecutar:

```powershell
python consulta_api.py 1
```

El número representa el identificador de un usuario.

El programa deberá:

1. Recibir el ID mediante `argparse`.
2. Validar que sea mayor que cero.
3. Consultar la API.
4. Utilizar `timeout`.
5. Comprobar errores HTTP.
6. Convertir la respuesta con `respuesta.json()`.
7. Mostrar:

```text
nombre
usuario
email
ciudad
empresa
```

8. Registrar la operación mediante `logging`.
9. Guardar la respuesta completa en:

```text
resultados/usuario_ID.json
```

Por ejemplo:

```text
resultados/usuario_1.json
```

El flujo será:

```text
     argparse
        │
        ▼
       ID
        │
        ▼
 construir URL
        │
        ▼
 requests.get()
        │
        ▼
     HTTP
        │
        ▼
      JSON
        │
        ▼
 diccionario Python
        │
   ┌────┴─────┐
   │          │
   ▼          ▼
pantalla    archivo
              │
              ▼
             JSON

        +
        │
        ▼
      logging
```

!!! success "Objetivo"

    Si completas esta práctica serás capaz de consultar una API, procesar su respuesta JSON y utilizar los datos obtenidos dentro de un programa Python.

---

## Resumen

En esta parte hemos aprendido qué es una:

```text
API
```

y cómo puede utilizarse para intercambiar información entre aplicaciones.

Hemos trabajado con:

```text
JSON
```

y hemos comprobado su relación con las estructuras de Python.

Por ejemplo:

```json
{
    "nombre": "PC01"
}
```

puede convertirse en un diccionario Python mediante:

```python
datos = respuesta.json()
```

Después podemos acceder:

```python
datos["nombre"]
```

También hemos trabajado con respuestas que contienen listas:

```python
for elemento in datos:
```

y estructuras anidadas:

```python
datos["address"]["city"]
```

Hemos utilizado parámetros de consulta mediante:

```python
params=parametros
```

y hemos aplicado estos conocimientos para consultar información mediante APIs.

Nuestro patrón básico es ahora:

```text
API
 │
 ▼
GET
 │
 ▼
respuesta HTTP
 │
 ▼
JSON
 │
 ▼
dict / list
 │
 ▼
procesamiento
```

Además hemos conectado estos conocimientos con capítulos anteriores:

```text
argparse
+
pathlib
+
excepciones
+
logging
+
requests
+
JSON
```

En la siguiente parte estudiaremos el segundo método HTTP principal de esta unidad:

```text
POST
```

Hasta ahora hemos utilizado principalmente:

```text
GET → solicitar información
```

A continuación aprenderemos:

```text
POST → enviar información
```

y veremos cómo enviar datos JSON desde Python a un servicio web mediante `requests`.

---

## 64. Envío de datos mediante POST

Hasta ahora nuestras comunicaciones han seguido principalmente este modelo:

```text
Python
   │
   │ GET
   ▼
Servidor
   │
   │ datos
   ▼
Python
```

Hemos utilizado:

```python
requests.get()
```

para solicitar información.

Pero nuestros programas también pueden necesitar **enviar información a un servidor**.

Por ejemplo:

```text
registrar un equipo
enviar datos de un sensor
crear un usuario
guardar una incidencia
enviar resultados de diagnóstico
registrar información de inventario
```

Para estas operaciones podemos utilizar el método HTTP:

```text
POST
```

---

### 65. Diferencia básica entre GET y POST

Podemos establecer inicialmente esta diferencia:

```text
GET
 │
 └── solicitar información


POST
 │
 └── enviar información
     para que el servidor
     la procese
```

Por ejemplo:

```text
GET /equipos/1
```

podría solicitar información sobre un equipo.

Mientras que:

```text
POST /equipos
```

podría enviar los datos necesarios para crear un nuevo equipo.

!!! note "Métodos HTTP"

    `GET` y `POST` no son los únicos métodos HTTP.

    Existen otros como:

    ```text
    PUT
    PATCH
    DELETE
    ```

    En esta unidad nos centraremos en `GET` y `POST`.

---

### 66. Funcionamiento de una petición POST

Una petición POST puede contener información.

Por ejemplo:

```text
PROGRAMA PYTHON
      │
      │ POST
      │
      │ {
      │   "nombre": "PC01",
      │   "ip": "192.168.1.20"
      │ }
      ▼
    SERVIDOR
      │
      │ procesa
      │ los datos
      ▼
   RESPUESTA
```

El servidor puede:

```text
validar los datos
guardarlos
procesarlos
crear un recurso
devolver un resultado
```

---

### 67. `requests.post()`

La biblioteca `requests` proporciona:

```python
requests.post()
```

Su estructura básica es:

```python
respuesta = requests.post(
    url,
    json=datos,
    timeout=10
)
```

Observa:

```python
json=datos
```

Esto indica a `requests` que queremos enviar los datos como JSON.

---

### 68. Preparar los datos

Los datos que enviaremos pueden estar inicialmente en un diccionario Python.

Por ejemplo:

```python
datos = {
    "nombre": "PC01",
    "ip": "192.168.1.20",
    "ubicacion": "Aula 1"
}
```

Conceptualmente:

```text
diccionario Python
        │
        ▼
   requests.post()
        │
        ▼
       JSON
        │
        ▼
     servidor
```

`requests` se encargará de preparar los datos JSON necesarios.

---

### 69. Nuestra primera petición POST

Dentro de:

```text
practicas/capitulo5/programas/
```

crea:

```text
primer_post.py
```

Escribe:

```python
import requests


url = (
    "https://jsonplaceholder.typicode.com/"
    "posts"
)


datos = {
    "title": "Prueba desde Python",
    "body": (
        "Contenido enviado "
        "desde nuestro programa"
    ),
    "userId": 1
}


respuesta = requests.post(
    url,
    json=datos,
    timeout=10
)


print(
    f"Código HTTP: "
    f"{respuesta.status_code}"
)

print()

print(
    respuesta.text
)
```

Ejecuta:

```powershell
python primer_post.py
```

El servidor devolverá una respuesta relacionada con el recurso enviado.

!!! note "Servicio de pruebas"

    JSONPlaceholder simula determinadas operaciones para permitir practicar con peticiones HTTP.

    No debemos interpretar este ejemplo como la creación permanente de información en una base de datos real.

---

### 70. Código HTTP 201

En una operación POST podemos recibir:

```text
201 Created
```

El código:

```text
201
```

indica que la petición ha producido la creación de un recurso.

Recordemos:

```text
200 OK
```

indica una operación correcta de forma general.

Mientras que:

```text
201 Created
```

se utiliza para indicar que se ha creado un recurso correctamente.

---

### 71. Procesar la respuesta del POST

Si el servidor devuelve JSON podemos utilizar nuevamente:

```python
respuesta.json()
```

Modifica el programa:

```python
import requests


url = (
    "https://jsonplaceholder.typicode.com/"
    "posts"
)


datos = {
    "title": "Prueba desde Python",
    "body": (
        "Contenido enviado "
        "desde nuestro programa"
    ),
    "userId": 1
}


respuesta = requests.post(
    url,
    json=datos,
    timeout=10
)

respuesta.raise_for_status()


resultado = respuesta.json()


print(
    resultado
)
```

Podemos acceder a sus elementos como con cualquier diccionario:

```python
print(
    f"ID: "
    f"{resultado.get('id')}"
)
```

---

### 72. Datos enviados y datos recibidos

Es importante distinguir:

```python
datos
```

de:

```python
resultado
```

En nuestro ejemplo:

```text
datos
  │
  └── información enviada
      al servidor


resultado
  │
  └── información devuelta
      por el servidor
```

El flujo completo es:

```text
diccionario Python
      │
      ▼
     datos
      │
      ▼
requests.post()
      │
      ▼
     JSON
      │
      ▼
   SERVIDOR
      │
      ▼
respuesta JSON
      │
      ▼
respuesta.json()
      │
      ▼
   resultado
```

---

### 73. Mostrar una respuesta de forma organizada

Podemos presentar únicamente la información que nos interesa.

Por ejemplo:

```python
print()
print("RESULTADO")
print("=========")
print()

print(
    f"ID: "
    f"{resultado.get('id')}"
)

print(
    f"Título: "
    f"{resultado.get('title')}"
)

print(
    f"Usuario: "
    f"{resultado.get('userId')}"
)
```

No es necesario mostrar siempre todo el JSON recibido.

Nuestros programas pueden seleccionar y procesar únicamente los campos necesarios.

---

### 74. Controlar errores en una petición POST

Una petición POST también puede fallar.

Podemos tener:

```text
problema de conexión
timeout
error HTTP
respuesta JSON incorrecta
```

Crea:

```text
post_seguro.py
```

Escribe:

```python
import requests


url = (
    "https://jsonplaceholder.typicode.com/"
    "posts"
)


datos = {
    "title": "Prueba",
    "body": "Mensaje de prueba",
    "userId": 1
}


try:

    respuesta = requests.post(
        url,
        json=datos,
        timeout=10
    )

    respuesta.raise_for_status()

    resultado = respuesta.json()

except requests.exceptions.Timeout:

    print(
        "ERROR: tiempo de "
        "espera agotado."
    )

except requests.exceptions.ConnectionError:

    print(
        "ERROR: no se ha podido "
        "establecer la conexión."
    )

except requests.exceptions.HTTPError as error:

    print(
        f"ERROR HTTP: {error}"
    )

except requests.exceptions.JSONDecodeError:

    print(
        "ERROR: respuesta JSON "
        "no válida."
    )

except requests.exceptions.RequestException as error:

    print(
        f"ERROR en la petición: "
        f"{error}"
    )

else:

    print(
        "Datos enviados "
        "correctamente."
    )

    print(
        f"Código HTTP: "
        f"{respuesta.status_code}"
    )

    print(
        f"ID recibido: "
        f"{resultado.get('id')}"
    )
```

Este patrón es muy parecido al utilizado con `GET`.

---

### 75. GET y POST utilizan el mismo modelo de respuesta

Una idea importante es que tanto:

```python
requests.get()
```

como:

```python
requests.post()
```

devuelven un objeto:

```text
Response
```

Por eso podemos utilizar en ambos casos:

```python
respuesta.status_code
```

```python
respuesta.headers
```

```python
respuesta.text
```

```python
respuesta.json()
```

```python
respuesta.raise_for_status()
```

Lo que cambia principalmente es la operación HTTP que estamos solicitando al servidor.

---

### 76. Enviar datos introducidos por el usuario

Hasta ahora tenemos:

```python
datos = {
    "title": "Prueba",
    "body": "Mensaje de prueba",
    "userId": 1
}
```

Los valores están escritos directamente en el código.

Podemos obtenerlos mediante:

```python
input()
```

Por ejemplo:

```python
titulo = input(
    "Título: "
)

contenido = input(
    "Contenido: "
)
```

Después:

```python
datos = {
    "title": titulo,
    "body": contenido,
    "userId": 1
}
```

Ahora el programa puede enviar diferentes datos sin modificar el código.

---

### 77. Enviar datos mediante `argparse`

Para nuestros scripts de administración resulta más interesante utilizar:

```python
argparse
```

Crea:

```text
enviar_post.py
```

Escribe:

```python
import argparse

import requests


parser = argparse.ArgumentParser(
    description=(
        "Envía información "
        "mediante HTTP POST."
    )
)


parser.add_argument(
    "titulo",
    help="Título del mensaje"
)


parser.add_argument(
    "contenido",
    help="Contenido del mensaje"
)


parser.add_argument(
    "--usuario",
    type=int,
    default=1,
    help="Identificador del usuario"
)


args = parser.parse_args()


if args.usuario < 1:

    parser.error(
        "El identificador del "
        "usuario debe ser mayor "
        "que cero."
    )


datos = {
    "title": args.titulo,
    "body": args.contenido,
    "userId": args.usuario
}


url = (
    "https://jsonplaceholder.typicode.com/"
    "posts"
)


try:

    respuesta = requests.post(
        url,
        json=datos,
        timeout=10
    )

    respuesta.raise_for_status()

    resultado = respuesta.json()

except requests.exceptions.RequestException as error:

    print(
        f"ERROR: {error}"
    )

else:

    print()
    print("DATOS ENVIADOS")
    print("=============")
    print()

    print(
        f"Título: "
        f"{resultado.get('title')}"
    )

    print(
        f"Contenido: "
        f"{resultado.get('body')}"
    )

    print(
        f"Usuario: "
        f"{resultado.get('userId')}"
    )

    print(
        f"ID: "
        f"{resultado.get('id')}"
    )
```

Podemos ejecutar:

```powershell
python enviar_post.py "Prueba" "Mensaje desde Python"
```

También:

```powershell
python enviar_post.py "Incidencia" "Equipo sin red" --usuario 2
```

!!! tip "Argumentos con espacios"

    Cuando un argumento contiene espacios debemos escribirlo entre comillas:

    ```powershell
    "Equipo sin red"
    ```

---

### 78. ¿Qué envía realmente `json=datos`?

Cuando escribimos:

```python
requests.post(
    url,
    json=datos
)
```

`requests` prepara automáticamente el contenido JSON y configura la petición adecuadamente.

Nuestro diccionario:

```python
datos = {
    "nombre": "PC01",
    "activo": True
}
```

se representa en JSON de forma equivalente a:

```json
{
    "nombre": "PC01",
    "activo": true
}
```

Esto evita que tengamos que construir manualmente el texto JSON para las operaciones habituales.

---

### 79. Cabecera `Content-Type`

Cuando enviamos JSON, el servidor necesita saber qué tipo de información está recibiendo.

Para JSON encontraremos habitualmente:

```text
Content-Type: application/json
```

Al utilizar:

```python
json=datos
```

`requests` prepara la petición para enviar los datos como JSON.

Podemos comprobar qué cabeceras se enviaron utilizando información de la petición preparada.

Por ejemplo:

```python
print(
    respuesta.request.headers.get(
        "Content-Type"
    )
)
```

Podremos obtener:

```text
application/json
```

---

### 80. `json=` frente a `data=`

Podemos encontrar ejemplos de `requests` que utilizan:

```python
data=
```

y otros que utilizan:

```python
json=
```

No significan exactamente lo mismo.

En este capítulo, cuando queramos enviar un objeto JSON utilizaremos:

```python
json=datos
```

Por ejemplo:

```python
requests.post(
    url,
    json=datos,
    timeout=10
)
```

!!! tip "Para nuestras APIs"

    Cuando la API espere JSON utilizaremos:

    ```python
    json=datos
    ```

    Esto mantiene el código sencillo y expresa claramente nuestra intención.

---

### 81. Enviar información de un equipo

Vamos a acercar el ejemplo a una tarea de administración.

Crea:

```text
enviar_equipo.py
```

Escribe:

```python
import argparse

import requests


parser = argparse.ArgumentParser(
    description=(
        "Envía información "
        "de un equipo."
    )
)


parser.add_argument(
    "nombre",
    help="Nombre del equipo"
)


parser.add_argument(
    "ip",
    help="Dirección IP"
)


parser.add_argument(
    "--ubicacion",
    default="No indicada",
    help="Ubicación del equipo"
)


args = parser.parse_args()


datos = {
    "nombre": args.nombre,
    "ip": args.ip,
    "ubicacion": args.ubicacion
}


print()
print("DATOS PREPARADOS")
print("================")
print()

print(
    datos
)
```

Podemos ejecutarlo:

```powershell
python enviar_equipo.py PC01 192.168.1.20 --ubicacion "Aula 1"
```

Obtendremos un diccionario preparado para ser enviado a una API:

```text
{
    'nombre': 'PC01',
    'ip': '192.168.1.20',
    'ubicacion': 'Aula 1'
}
```

---

### 82. Separar preparación y envío

Podemos crear una función:

```python
def enviar_datos(
    url,
    datos
):

    try:

        respuesta = requests.post(
            url,
            json=datos,
            timeout=10
        )

        respuesta.raise_for_status()

        return respuesta.json()

    except requests.exceptions.RequestException as error:

        print(
            f"ERROR: {error}"
        )

        return None
```

Después:

```python
resultado = enviar_datos(
    url,
    datos
)


if resultado is not None:

    print(
        "Datos enviados."
    )
```

Estamos separando:

```text
preparar datos
      │
      ▼
enviar_datos()
      │
      ▼
procesar respuesta
```

Esto facilita reutilizar el código.

---

### 83. Registrar una petición POST mediante `logging`

También podemos registrar las operaciones.

Por ejemplo:

```python
logging.info(
    f"Enviando datos a {url}"
)
```

Si funciona:

```python
logging.info(
    f"POST correcto. "
    f"HTTP {respuesta.status_code}"
)
```

Si se produce un error:

```python
logging.error(
    f"Error enviando datos "
    f"a {url}"
)
```

!!! warning "No registres información sensible"

    Antes de guardar los datos enviados en un log debemos comprobar qué contienen.

    No debemos registrar información como:

    ```text
    contraseñas
    tokens
    claves de API
    credenciales
    ```

---

### 84. Programa POST con logging

Crea:

```text
post_logging.py
```

Escribe:

```python
import logging

import requests


logging.basicConfig(
    filename="http.log",
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    ),
    datefmt=(
        "%Y-%m-%d %H:%M:%S"
    )
)


url = (
    "https://jsonplaceholder.typicode.com/"
    "posts"
)


datos = {
    "title": "Prueba",
    "body": "Datos enviados desde Python",
    "userId": 1
}


logging.info(
    f"Iniciando POST a {url}"
)


try:

    respuesta = requests.post(
        url,
        json=datos,
        timeout=10
    )

    respuesta.raise_for_status()

    resultado = respuesta.json()

except requests.exceptions.Timeout:

    print(
        "ERROR: timeout."
    )

    logging.error(
        f"Timeout en POST a {url}"
    )

except requests.exceptions.ConnectionError:

    print(
        "ERROR: conexión."
    )

    logging.error(
        f"Error de conexión "
        f"con {url}"
    )

except requests.exceptions.HTTPError as error:

    print(
        f"ERROR HTTP: {error}"
    )

    logging.error(
        f"Error HTTP: {error}"
    )

except requests.exceptions.JSONDecodeError:

    print(
        "ERROR: JSON no válido."
    )

    logging.error(
        "Respuesta JSON no válida"
    )

except requests.exceptions.RequestException as error:

    print(
        f"ERROR: {error}"
    )

    logging.exception(
        "Error realizando POST"
    )

else:

    print(
        "Datos enviados "
        "correctamente."
    )

    logging.info(
        f"POST correcto. "
        f"HTTP {respuesta.status_code}"
    )

finally:

    logging.info(
        "Operación POST finalizada"
    )
```

Ahora combinamos:

```text
POST
+
JSON
+
excepciones
+
logging
```

---

### 85. GET y POST en una misma aplicación

Una aplicación puede utilizar diferentes métodos HTTP.

Por ejemplo:

```text
              API
               │
       ┌───────┴────────┐
       │                │
       ▼                ▼
      GET              POST
       │                │
       ▼                ▼
 consultar           enviar
 información       información
```

Podríamos crear un programa con:

```text
--listar
```

para realizar un GET.

Y:

```text
--crear
```

para realizar un POST.

Esto nos permitirá comenzar a construir pequeños **clientes de APIs**.

---

### 86. Práctica guiada: cliente de publicaciones

Crea:

```text
cliente_posts.py
```

El programa deberá ofrecer dos operaciones:

```text
--listar
```

y:

```text
--crear
```

Para evitar utilizar ambas simultáneamente podemos crear:

```python
grupo = (
    parser.add_mutually_exclusive_group(
        required=True
    )
)
```

Después:

```python
grupo.add_argument(
    "--listar",
    action="store_true",
    help="Lista publicaciones"
)
```

y:

```python
grupo.add_argument(
    "--crear",
    action="store_true",
    help="Crea una publicación"
)
```

También necesitaremos:

```text
--titulo
--contenido
--usuario
```

---

### 87. Estructura del cliente

Nuestro programa tendrá dos funciones:

```python
def listar_publicaciones():
```

y:

```python
def crear_publicacion(
    titulo,
    contenido,
    usuario
):
```

La primera utilizará:

```python
requests.get()
```

La segunda:

```python
requests.post()
```

El programa principal decidirá:

```python
if args.listar:

    listar_publicaciones()

elif args.crear:

    crear_publicacion(
        args.titulo,
        args.contenido,
        args.usuario
    )
```

---

### 88. Función GET

Podemos crear:

```python
def listar_publicaciones():

    try:

        respuesta = requests.get(
            URL,
            timeout=10
        )

        respuesta.raise_for_status()

        datos = respuesta.json()

    except requests.exceptions.RequestException as error:

        print(
            f"ERROR: {error}"
        )

        return

    print()
    print("PUBLICACIONES")
    print("=============")
    print()

    for publicacion in datos[:5]:

        print(
            f"ID: "
            f"{publicacion.get('id')}"
        )

        print(
            f"Título: "
            f"{publicacion.get('title')}"
        )

        print()
```

En esta práctica mostramos únicamente los cinco primeros elementos mediante:

```python
datos[:5]
```

---

### 89. Función POST

La segunda función será:

```python
def crear_publicacion(
    titulo,
    contenido,
    usuario
):

    datos = {
        "title": titulo,
        "body": contenido,
        "userId": usuario
    }

    try:

        respuesta = requests.post(
            URL,
            json=datos,
            timeout=10
        )

        respuesta.raise_for_status()

        resultado = respuesta.json()

    except requests.exceptions.RequestException as error:

        print(
            f"ERROR: {error}"
        )

        return

    print()
    print("PUBLICACIÓN ENVIADA")
    print("===================")
    print()

    print(
        f"ID: "
        f"{resultado.get('id')}"
    )

    print(
        f"Título: "
        f"{resultado.get('title')}"
    )
```

---

### 90. Validar los argumentos del POST

Si el usuario ejecuta:

```powershell
python cliente_posts.py --crear
```

nos faltan datos.

Necesitamos:

```text
título
contenido
```

Podemos comprobar:

```python
if args.crear:

    if not args.titulo:

        parser.error(
            "--crear necesita "
            "--titulo"
        )

    if not args.contenido:

        parser.error(
            "--crear necesita "
            "--contenido"
        )
```

Después llamaremos a:

```python
crear_publicacion(
    args.titulo,
    args.contenido,
    args.usuario
)
```

Esta es una buena demostración de que una aplicación necesita:

```text
argumentos
    │
    ▼
validación
    │
    ▼
operación
```

---

### 91. Ejemplos de ejecución

Para listar:

```powershell
python cliente_posts.py --listar
```

Para crear:

```powershell
python cliente_posts.py --crear --titulo "Prueba" --contenido "Mensaje desde Python"
```

También podemos indicar:

```powershell
python cliente_posts.py --crear --titulo "Incidencia" --contenido "PC sin conexión" --usuario 3
```

---

### 92. GET y POST no significan leer y escribir archivos

Es importante no confundir los métodos HTTP con operaciones locales.

```text
GET
```

no significa simplemente:

```text
leer archivo
```

y:

```text
POST
```

no significa simplemente:

```text
escribir archivo
```

Son métodos definidos por HTTP.

El comportamiento concreto depende de cómo esté diseñada la API.

Por ejemplo, una API puede definir:

```text
GET /equipos
```

para obtener equipos.

Y:

```text
POST /equipos
```

para crear uno nuevo.

La documentación de la API es la que nos indica cómo debemos utilizarla.

---

### 93. La documentación de una API

Antes de utilizar una API real debemos consultar su documentación.

Necesitamos conocer aspectos como:

```text
URL base
endpoints
métodos HTTP
parámetros
formato de los datos
campos obligatorios
autenticación
códigos de respuesta
estructura del JSON
```

Por ejemplo:

```text
Endpoint:
POST /equipos

Datos:

{
    "nombre": "...",
    "ip": "..."
}

Respuesta:

201 Created
```

Nuestro programa debe adaptarse al contrato definido por la API.

---

### 94. APIs que requieren autenticación

Muchas APIs públicas permiten algunas consultas sin autenticación.

Sin embargo, en servicios reales es frecuente necesitar algún mecanismo de autenticación.

Podemos encontrar conceptos como:

```text
API key
token
Authorization
```

En este capítulo no necesitamos entrar todavía en sistemas de autenticación complejos.

Lo importante es comprender que no todas las APIs permiten realizar peticiones libremente.

!!! warning "Credenciales"

    Nunca debemos escribir claves o tokens reales en ejemplos que vayan a publicarse en GitHub.

    Tampoco debemos almacenarlos directamente en el código de un repositorio público.

---

### 95. Práctica propuesta: registrar una incidencia

Crea:

```text
enviar_incidencia.py
```

El programa deberá recibir:

```text
equipo
descripción
prioridad
```

Por ejemplo:

```powershell
python enviar_incidencia.py PC01 "Sin conexión de red" --prioridad alta
```

Internamente deberá preparar:

```python
datos = {
    "equipo": ...,
    "descripcion": ...,
    "prioridad": ...
}
```

Después deberá:

1. Mostrar los datos que se enviarían.
2. Realizar un POST contra un servicio de pruebas.
3. Comprobar el código HTTP.
4. Procesar la respuesta JSON.
5. Mostrar el resultado.
6. Registrar la operación mediante `logging`.

!!! example "Objetivo"

    La finalidad de esta práctica es simular el comportamiento de una herramienta que envía incidencias a un servicio web.

---

### 96. Práctica propuesta: enviar inventario

Vamos a recuperar también los archivos CSV utilizados anteriormente.

Supongamos:

```text
datos/inventario.csv
```

con:

```csv
nombre,ip,ubicacion
PC01,192.168.1.20,Aula 1
PC02,192.168.1.21,Aula 1
PC03,192.168.1.22,Aula 2
```

El programa:

```text
enviar_inventario.py
```

deberá:

```text
leer CSV
    │
    ▼
recorrer equipos
    │
    ▼
crear diccionario
    │
    ▼
POST
    │
    ▼
comprobar respuesta
    │
    ▼
registrar resultado
```

Para cada fila tendremos:

```python
datos = {
    "nombre": fila["nombre"],
    "ip": fila["ip"],
    "ubicacion": fila["ubicacion"]
}
```

Después podremos realizar:

```python
requests.post(
    url,
    json=datos,
    timeout=10
)
```

!!! note "Integración"

    Esta práctica combina contenidos de diferentes capítulos:

    ```text
    CSV
      +
    bucles
      +
    excepciones
      +
    logging
      +
    HTTP
      +
    JSON
    ```

---

### 97. Patrón completo de una petición POST

Podemos establecer el siguiente patrón:

```text
      OBTENER DATOS
           │
           ▼
        VALIDAR
           │
           ▼
crear diccionario Python
           │
           ▼
    requests.post()
           │
           ▼
         JSON
           │
           ▼
        SERVIDOR
           │
           ▼
    respuesta HTTP
           │
           ▼
   raise_for_status()
           │
           ▼
    respuesta.json()
           │
           ▼
   procesar resultado
           │
           ▼
 mostrar / guardar / log
```

En código:

```python
try:

    respuesta = requests.post(
        url,
        json=datos,
        timeout=10
    )

    respuesta.raise_for_status()

    resultado = respuesta.json()

except requests.exceptions.RequestException as error:

    print(
        f"ERROR: {error}"
    )

else:

    # Procesar resultado
    ...
```

---

## Resumen

En esta parte hemos incorporado el método HTTP:

```text
POST
```

y hemos establecido una primera diferencia:

```text
GET
 │
 └── solicitar información


POST
 │
 └── enviar información
     para que sea procesada
```

Con `requests` utilizamos:

```python
requests.get()
```

y:

```python
requests.post()
```

Para enviar un diccionario Python como JSON podemos utilizar:

```python
datos = {
    "nombre": "PC01",
    "ip": "192.168.1.20"
}
```

y:

```python
respuesta = requests.post(
    url,
    json=datos,
    timeout=10
)
```

Después podemos comprobar:

```python
respuesta.status_code
```

procesar errores:

```python
respuesta.raise_for_status()
```

y convertir una respuesta JSON mediante:

```python
resultado = respuesta.json()
```

También hemos combinado:

```text
argparse
+
validación
+
requests
+
GET
+
POST
+
JSON
+
excepciones
+
logging
```

Con ello ya disponemos de los principales elementos necesarios para construir un pequeño **cliente de una API**.

En la siguiente parte realizaremos la **práctica integradora y cierre del capítulo 5**, construyendo una herramienta que combine consultas GET, envío mediante POST, procesamiento JSON, argumentos, control de errores, almacenamiento de resultados y logs.

---

## 98. Práctica final: cliente de una API

Durante este capítulo hemos aprendido a comunicarnos con servicios web desde Python.

Hemos utilizado:

```python
requests.get()
```

para solicitar información y:

```python
requests.post()
```

para enviar información.

También hemos procesado respuestas JSON mediante:

```python
respuesta.json()
```

Ahora construiremos una aplicación que integre estos conocimientos.

El programa se llamará:

```text
cliente_api.py
```

y permitirá realizar diferentes operaciones desde la línea de comandos.

---

### 99. Objetivos de la práctica

Nuestra aplicación permitirá:

```text
listar usuarios
consultar un usuario
listar publicaciones
crear una publicación
```

Además deberá:

- Recibir opciones mediante `argparse`.
- Realizar peticiones `GET`.
- Realizar peticiones `POST`.
- Procesar respuestas JSON.
- Controlar errores de conexión.
- Utilizar tiempos de espera.
- Registrar las operaciones mediante `logging`.
- Guardar algunos resultados en archivos JSON.

El flujo general será:

```text
          USUARIO
             │
             ▼
          argparse
             │
             ▼
        seleccionar
         operación
             │
       ┌─────┴─────┐
       │           │
       ▼           ▼
      GET         POST
       │           │
       └─────┬─────┘
             │
             ▼
         SERVIDOR
             │
             ▼
       respuesta HTTP
             │
             ▼
            JSON
             │
       ┌─────┴──────┐
       │            │
       ▼            ▼
    pantalla      archivo
       │
       └─────┬──────┘
             │
             ▼
           logging
```

---

### 100. Estructura de directorios

Utilizaremos:

```text
practicas/
└── capitulo5/
    ├── datos/
    ├── logs/
    ├── programas/
    │   └── cliente_api.py
    └── resultados/
```

El programa creará automáticamente:

```text
logs/
```

y:

```text
resultados/
```

si no existen.

---

### 101. API utilizada

Para la práctica utilizaremos el servicio de pruebas:

```text
JSONPlaceholder
```

Trabajaremos principalmente con los recursos:

```text
/users
```

y:

```text
/posts
```

Conceptualmente:

```text
API
 │
 ├── /users
 │      │
 │      ├── GET → usuarios
 │      │
 │      └── GET /ID → usuario
 │
 └── /posts
        │
        ├── GET → publicaciones
        │
        └── POST → crear publicación
```

!!! note "Entorno de aprendizaje"

    Estamos utilizando una API diseñada para realizar pruebas.

    Las operaciones de creación son simuladas y no deben interpretarse como modificaciones permanentes de una base de datos real.

---

### 102. Crear el programa

Dentro de:

```text
practicas/capitulo5/programas/
```

crea:

```text
cliente_api.py
```

Comenzamos con las importaciones:

```python
import argparse
import json
import logging

from pathlib import Path

import requests
```

Utilizaremos:

```text
argparse
    argumentos

json
    guardar datos JSON

logging
    registro de actividad

pathlib
    rutas y archivos

requests
    comunicaciones HTTP
```

---

### 103. Definir las rutas

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

---

### 104. Definir la URL base

Añade:

```python
URL_BASE = (
    "https://jsonplaceholder.typicode.com"
)
```

Después podremos construir diferentes endpoints:

```python
f"{URL_BASE}/users"
```

```python
f"{URL_BASE}/posts"
```

```python
f"{URL_BASE}/users/1"
```

Esto evita repetir continuamente la dirección completa.

---

### 105. Configurar el log

Creamos:

```python
ARCHIVO_LOG = (
    DIRECTORIO_LOGS
    / "cliente_api.log"
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

Ahora podremos registrar:

```python
logging.info(...)
```

```python
logging.warning(...)
```

```python
logging.error(...)
```

---

### 106. Crear una función GET reutilizable

Muchas operaciones utilizarán:

```python
requests.get()
```

Por tanto, crearemos una función:

```python
def obtener_json(
    url,
    parametros=None
):

    logging.info(
        f"GET {url}"
    )

    try:

        respuesta = requests.get(
            url,
            params=parametros,
            timeout=10
        )

        respuesta.raise_for_status()

        datos = respuesta.json()

    except requests.exceptions.Timeout:

        print(
            "ERROR: tiempo de "
            "espera agotado."
        )

        logging.error(
            f"Timeout en GET {url}"
        )

        return None

    except requests.exceptions.ConnectionError:

        print(
            "ERROR: no se ha podido "
            "establecer la conexión."
        )

        logging.error(
            f"Error de conexión: "
            f"{url}"
        )

        return None

    except requests.exceptions.HTTPError as error:

        print(
            f"ERROR HTTP: {error}"
        )

        logging.error(
            f"Error HTTP en "
            f"{url}: {error}"
        )

        return None

    except requests.exceptions.JSONDecodeError:

        print(
            "ERROR: respuesta JSON "
            "no válida."
        )

        logging.error(
            f"JSON no válido: {url}"
        )

        return None

    except requests.exceptions.RequestException as error:

        print(
            f"ERROR: {error}"
        )

        logging.exception(
            f"Error GET: {url}"
        )

        return None

    else:

        logging.info(
            f"GET correcto: "
            f"HTTP {respuesta.status_code}"
        )

        return datos
```

Ahora podremos reutilizar esta función para diferentes consultas.

---

### 107. Crear una función POST reutilizable

Haremos algo similar para:

```text
POST
```

Añade:

```python
def enviar_json(
    url,
    datos
):

    logging.info(
        f"POST {url}"
    )

    try:

        respuesta = requests.post(
            url,
            json=datos,
            timeout=10
        )

        respuesta.raise_for_status()

        resultado = respuesta.json()

    except requests.exceptions.Timeout:

        print(
            "ERROR: tiempo de "
            "espera agotado."
        )

        logging.error(
            f"Timeout en POST {url}"
        )

        return None

    except requests.exceptions.ConnectionError:

        print(
            "ERROR: problema "
            "de conexión."
        )

        logging.error(
            f"Error de conexión: "
            f"{url}"
        )

        return None

    except requests.exceptions.HTTPError as error:

        print(
            f"ERROR HTTP: {error}"
        )

        logging.error(
            f"Error HTTP en POST: "
            f"{error}"
        )

        return None

    except requests.exceptions.JSONDecodeError:

        print(
            "ERROR: respuesta JSON "
            "no válida."
        )

        logging.error(
            "Respuesta POST "
            "sin JSON válido"
        )

        return None

    except requests.exceptions.RequestException as error:

        print(
            f"ERROR: {error}"
        )

        logging.exception(
            f"Error POST: {url}"
        )

        return None

    else:

        logging.info(
            f"POST correcto: "
            f"HTTP {respuesta.status_code}"
        )

        return resultado
```

Ya tenemos dos funciones generales:

```text
obtener_json()
      │
      └── GET


enviar_json()
      │
      └── POST
```

---

### 108. Función para guardar JSON

Vamos a crear otra función reutilizable:

```python
def guardar_json(
    datos,
    nombre
):

    archivo = (
        DIRECTORIO_RESULTADOS
        / nombre
    )

    try:

        with open(
            archivo,
            "w",
            encoding="utf-8"
        ) as fichero:

            json.dump(
                datos,
                fichero,
                indent=4,
                ensure_ascii=False
            )

    except OSError as error:

        print(
            "ERROR: no se ha podido "
            "guardar el archivo."
        )

        logging.exception(
            f"Error guardando "
            f"{archivo}: {error}"
        )

        return False

    else:

        logging.info(
            f"Archivo guardado: "
            f"{archivo}"
        )

        return True
```

Esta función recibe:

```text
datos
```

y:

```text
nombre del archivo
```

y los almacena dentro de:

```text
resultados/
```

---

### 109. Operación: listar usuarios

Creamos:

```python
def listar_usuarios():

    url = (
        f"{URL_BASE}/users"
    )

    usuarios = obtener_json(
        url
    )

    if usuarios is None:

        return

    print()
    print("USUARIOS")
    print("========")
    print()

    for usuario in usuarios:

        print(
            f"{usuario.get('id')} - "
            f"{usuario.get('name')} - "
            f"{usuario.get('email')}"
        )

    print()

    print(
        f"Total: {len(usuarios)}"
    )
```

Esta función realiza:

```text
GET /users
      │
      ▼
lista JSON
      │
      ▼
for
      │
      ▼
usuarios
```

---

### 110. Operación: consultar un usuario

Añade:

```python
def consultar_usuario(
    identificador
):

    url = (
        f"{URL_BASE}/users/"
        f"{identificador}"
    )

    usuario = obtener_json(
        url
    )

    if usuario is None:

        return

    print()
    print("USUARIO")
    print("=======")
    print()

    print(
        f"ID: "
        f"{usuario.get('id')}"
    )

    print(
        f"Nombre: "
        f"{usuario.get('name')}"
    )

    print(
        f"Usuario: "
        f"{usuario.get('username')}"
    )

    print(
        f"Email: "
        f"{usuario.get('email')}"
    )

    direccion = usuario.get(
        "address",
        {}
    )

    print(
        f"Ciudad: "
        f"{direccion.get('city')}"
    )

    empresa = usuario.get(
        "company",
        {}
    )

    print(
        f"Empresa: "
        f"{empresa.get('name')}"
    )

    nombre_archivo = (
        f"usuario_"
        f"{identificador}.json"
    )

    if guardar_json(
        usuario,
        nombre_archivo
    ):

        print()
        print(
            f"Datos guardados en "
            f"{nombre_archivo}"
        )
```

Aquí utilizamos:

```python
usuario.get(
    "address",
    {}
)
```

para obtener un diccionario vacío si no existe la dirección.

De esta forma podemos utilizar posteriormente:

```python
direccion.get("city")
```

sin acceder directamente a una clave inexistente.

---

### 111. Operación: listar publicaciones

Añade:

```python
def listar_publicaciones(
    usuario=None
):

    url = (
        f"{URL_BASE}/posts"
    )

    parametros = None

    if usuario is not None:

        parametros = {
            "userId": usuario
        }

    publicaciones = obtener_json(
        url,
        parametros
    )

    if publicaciones is None:

        return

    print()
    print("PUBLICACIONES")
    print("=============")
    print()

    for publicacion in publicaciones:

        print(
            f"ID: "
            f"{publicacion.get('id')}"
        )

        print(
            f"Título: "
            f"{publicacion.get('title')}"
        )

        print(
            "-" * 40
        )

    print()

    print(
        f"Total: "
        f"{len(publicaciones)}"
    )
```

Si recibimos:

```python
usuario=None
```

consultaremos todas las publicaciones.

Si recibimos:

```python
usuario=1
```

se enviará:

```python
params={
    "userId": 1
}
```

---

### 112. Operación: crear una publicación

Añade:

```python
def crear_publicacion(
    titulo,
    contenido,
    usuario
):

    url = (
        f"{URL_BASE}/posts"
    )

    datos = {
        "title": titulo,
        "body": contenido,
        "userId": usuario
    }

    resultado = enviar_json(
        url,
        datos
    )

    if resultado is None:

        return

    print()
    print("PUBLICACIÓN ENVIADA")
    print("===================")
    print()

    print(
        f"ID: "
        f"{resultado.get('id')}"
    )

    print(
        f"Título: "
        f"{resultado.get('title')}"
    )

    print(
        f"Contenido: "
        f"{resultado.get('body')}"
    )

    print(
        f"Usuario: "
        f"{resultado.get('userId')}"
    )

    guardar_json(
        resultado,
        "ultima_publicacion.json"
    )
```

Tenemos ahora las cuatro operaciones principales:

```text
listar_usuarios()
consultar_usuario()
listar_publicaciones()
crear_publicacion()
```

---

### 113. Crear la interfaz con `argparse`

Ahora definiremos las opciones del programa.

Añade:

```python
parser = argparse.ArgumentParser(
    description=(
        "Cliente de API desarrollado "
        "con Python y requests."
    )
)
```

Creamos un grupo:

```python
grupo = (
    parser.add_mutually_exclusive_group(
        required=True
    )
)
```

Esto obligará a seleccionar una operación.

---

### 114. Añadir las operaciones

Añade:

```python
grupo.add_argument(
    "--usuarios",
    action="store_true",
    help="Lista los usuarios"
)
```

Después:

```python
grupo.add_argument(
    "--usuario",
    type=int,
    metavar="ID",
    help="Consulta un usuario"
)
```

Añadimos:

```python
grupo.add_argument(
    "--posts",
    action="store_true",
    help="Lista publicaciones"
)
```

Y:

```python
grupo.add_argument(
    "--crear",
    action="store_true",
    help="Crea una publicación"
)
```

---

### 115. Argumentos adicionales

Para crear una publicación necesitaremos:

```text
título
contenido
ID del usuario
```

Añade:

```python
parser.add_argument(
    "--titulo",
    help="Título de la publicación"
)
```

```python
parser.add_argument(
    "--contenido",
    help="Contenido de la publicación"
)
```

```python
parser.add_argument(
    "--autor",
    type=int,
    default=1,
    help=(
        "ID del usuario. "
        "Por defecto: 1"
    )
)
```

También permitiremos filtrar publicaciones:

```python
parser.add_argument(
    "--filtrar-usuario",
    type=int,
    metavar="ID",
    help=(
        "Filtra publicaciones "
        "por usuario"
    )
)
```

Finalmente:

```python
args = parser.parse_args()
```

---

### 116. Validar los argumentos

Antes de realizar las operaciones debemos validar algunos valores.

Por ejemplo:

```python
if (
    args.usuario is not None
    and args.usuario < 1
):

    parser.error(
        "El ID del usuario debe "
        "ser mayor que cero."
    )
```

También:

```python
if (
    args.filtrar_usuario is not None
    and args.filtrar_usuario < 1
):

    parser.error(
        "El ID para filtrar debe "
        "ser mayor que cero."
    )
```

Para crear una publicación:

```python
if args.crear:

    if not args.titulo:

        parser.error(
            "--crear necesita "
            "--titulo"
        )

    if not args.contenido:

        parser.error(
            "--crear necesita "
            "--contenido"
        )

    if args.autor < 1:

        parser.error(
            "--autor debe ser "
            "mayor que cero"
        )
```

---

### 117. Programa principal

Añade:

```python
logging.info(
    "Programa iniciado"
)


if args.usuarios:

    listar_usuarios()

elif args.usuario is not None:

    consultar_usuario(
        args.usuario
    )

elif args.posts:

    listar_publicaciones(
        args.filtrar_usuario
    )

elif args.crear:

    crear_publicacion(
        args.titulo,
        args.contenido,
        args.autor
    )


logging.info(
    "Programa finalizado"
)
```

Nuestra aplicación ya está completa.

---

### 118. Consultar la ayuda

Ejecuta:

```powershell
python cliente_api.py --help
```

Deberemos encontrar opciones similares a:

```text
--usuarios
--usuario ID
--posts
--crear
--titulo
--contenido
--autor
--filtrar-usuario
```

Gracias a `argparse`, nuestro programa dispone de su propia ayuda.

---

### 119. Prueba 1: listar usuarios

Ejecuta:

```powershell
python cliente_api.py --usuarios
```

El programa realizará:

```text
GET /users
```

y mostrará la lista recibida.

---

### 120. Prueba 2: consultar un usuario

Ejecuta:

```powershell
python cliente_api.py --usuario 1
```

Deberá mostrar información como:

```text
USUARIO
=======

ID: ...
Nombre: ...
Usuario: ...
Email: ...
Ciudad: ...
Empresa: ...
```

Además deberá crear:

```text
resultados/usuario_1.json
```

---

### 121. Comprobar el archivo JSON

Abre:

```text
resultados/usuario_1.json
```

El archivo deberá contener la información recibida de la API.

Gracias a:

```python
indent=4
```

el contenido aparecerá correctamente indentado.

Hemos realizado:

```text
API
 │
 ▼
GET
 │
 ▼
JSON
 │
 ▼
dict
 │
 ▼
json.dump()
 │
 ▼
archivo .json
```

---

### 122. Prueba 3: listar publicaciones

Ejecuta:

```powershell
python cliente_api.py --posts
```

El programa realizará:

```text
GET /posts
```

y mostrará las publicaciones recibidas.

---

### 123. Filtrar publicaciones

Ahora ejecuta:

```powershell
python cliente_api.py --posts --filtrar-usuario 1
```

Nuestro programa enviará un parámetro equivalente a:

```text
?userId=1
```

mediante:

```python
params={
    "userId": 1
}
```

Esto permite comprobar cómo una misma petición puede modificarse mediante parámetros.

---

### 124. Prueba 4: crear una publicación

Ejecuta:

```powershell
python cliente_api.py --crear --titulo "Prueba" --contenido "Mensaje enviado desde Python"
```

También podemos especificar el usuario:

```powershell
python cliente_api.py --crear --titulo "Incidencia" --contenido "Equipo sin conexión" --autor 3
```

El programa realizará:

```text
POST /posts
```

enviando:

```json
{
    "title": "...",
    "body": "...",
    "userId": 3
}
```

Después procesará la respuesta JSON.

---

### 125. Comprobar los logs

Abre:

```text
logs/cliente_api.log
```

Después de varias operaciones podremos encontrar registros similares a:

```text
2026-09-21 13:00:10 - INFO - Programa iniciado
2026-09-21 13:00:10 - INFO - GET https://...
2026-09-21 13:00:11 - INFO - GET correcto: HTTP 200
2026-09-21 13:00:11 - INFO - Programa finalizado
```

También podrán aparecer operaciones POST:

```text
2026-09-21 13:05:20 - INFO - POST https://...
2026-09-21 13:05:21 - INFO - POST correcto: HTTP 201
```

Ahora nuestra aplicación deja un registro de su actividad.

---

### 126. Código completo

Una vez comprendidas y probadas las partes anteriores, el programa completo será:

```python
import argparse
import json
import logging

from pathlib import Path

import requests


# -----------------------------
# Rutas
# -----------------------------

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


# -----------------------------
# Configuración
# -----------------------------

URL_BASE = (
    "https://jsonplaceholder.typicode.com"
)

ARCHIVO_LOG = (
    DIRECTORIO_LOGS
    / "cliente_api.log"
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


# -----------------------------
# Funciones HTTP
# -----------------------------

def obtener_json(
    url,
    parametros=None
):

    logging.info(
        f"GET {url}"
    )

    try:

        respuesta = requests.get(
            url,
            params=parametros,
            timeout=10
        )

        respuesta.raise_for_status()

        datos = respuesta.json()

    except requests.exceptions.Timeout:

        print(
            "ERROR: tiempo de "
            "espera agotado."
        )

        logging.error(
            f"Timeout en GET {url}"
        )

        return None

    except requests.exceptions.ConnectionError:

        print(
            "ERROR: no se ha podido "
            "establecer la conexión."
        )

        logging.error(
            f"Error de conexión: "
            f"{url}"
        )

        return None

    except requests.exceptions.HTTPError as error:

        print(
            f"ERROR HTTP: {error}"
        )

        logging.error(
            f"Error HTTP en "
            f"{url}: {error}"
        )

        return None

    except requests.exceptions.JSONDecodeError:

        print(
            "ERROR: respuesta JSON "
            "no válida."
        )

        logging.error(
            f"JSON no válido: {url}"
        )

        return None

    except requests.exceptions.RequestException as error:

        print(
            f"ERROR: {error}"
        )

        logging.exception(
            f"Error GET: {url}"
        )

        return None

    else:

        logging.info(
            f"GET correcto: "
            f"HTTP {respuesta.status_code}"
        )

        return datos


def enviar_json(
    url,
    datos
):

    logging.info(
        f"POST {url}"
    )

    try:

        respuesta = requests.post(
            url,
            json=datos,
            timeout=10
        )

        respuesta.raise_for_status()

        resultado = respuesta.json()

    except requests.exceptions.Timeout:

        print(
            "ERROR: tiempo de "
            "espera agotado."
        )

        logging.error(
            f"Timeout en POST {url}"
        )

        return None

    except requests.exceptions.ConnectionError:

        print(
            "ERROR: problema "
            "de conexión."
        )

        logging.error(
            f"Error de conexión: "
            f"{url}"
        )

        return None

    except requests.exceptions.HTTPError as error:

        print(
            f"ERROR HTTP: {error}"
        )

        logging.error(
            f"Error HTTP en POST: "
            f"{error}"
        )

        return None

    except requests.exceptions.JSONDecodeError:

        print(
            "ERROR: respuesta JSON "
            "no válida."
        )

        logging.error(
            "Respuesta POST "
            "sin JSON válido"
        )

        return None

    except requests.exceptions.RequestException as error:

        print(
            f"ERROR: {error}"
        )

        logging.exception(
            f"Error POST: {url}"
        )

        return None

    else:

        logging.info(
            f"POST correcto: "
            f"HTTP {respuesta.status_code}"
        )

        return resultado


# -----------------------------
# Archivos
# -----------------------------

def guardar_json(
    datos,
    nombre
):

    archivo = (
        DIRECTORIO_RESULTADOS
        / nombre
    )

    try:

        with open(
            archivo,
            "w",
            encoding="utf-8"
        ) as fichero:

            json.dump(
                datos,
                fichero,
                indent=4,
                ensure_ascii=False
            )

    except OSError as error:

        print(
            "ERROR: no se ha podido "
            "guardar el archivo."
        )

        logging.exception(
            f"Error guardando "
            f"{archivo}: {error}"
        )

        return False

    else:

        logging.info(
            f"Archivo guardado: "
            f"{archivo}"
        )

        return True


# -----------------------------
# Operaciones
# -----------------------------

def listar_usuarios():

    url = (
        f"{URL_BASE}/users"
    )

    usuarios = obtener_json(
        url
    )

    if usuarios is None:

        return

    print()
    print("USUARIOS")
    print("========")
    print()

    for usuario in usuarios:

        print(
            f"{usuario.get('id')} - "
            f"{usuario.get('name')} - "
            f"{usuario.get('email')}"
        )

    print()

    print(
        f"Total: {len(usuarios)}"
    )


def consultar_usuario(
    identificador
):

    url = (
        f"{URL_BASE}/users/"
        f"{identificador}"
    )

    usuario = obtener_json(
        url
    )

    if usuario is None:

        return

    print()
    print("USUARIO")
    print("=======")
    print()

    print(
        f"ID: "
        f"{usuario.get('id')}"
    )

    print(
        f"Nombre: "
        f"{usuario.get('name')}"
    )

    print(
        f"Usuario: "
        f"{usuario.get('username')}"
    )

    print(
        f"Email: "
        f"{usuario.get('email')}"
    )

    direccion = usuario.get(
        "address",
        {}
    )

    print(
        f"Ciudad: "
        f"{direccion.get('city')}"
    )

    empresa = usuario.get(
        "company",
        {}
    )

    print(
        f"Empresa: "
        f"{empresa.get('name')}"
    )

    nombre_archivo = (
        f"usuario_"
        f"{identificador}.json"
    )

    if guardar_json(
        usuario,
        nombre_archivo
    ):

        print()
        print(
            f"Datos guardados en "
            f"{nombre_archivo}"
        )


def listar_publicaciones(
    usuario=None
):

    url = (
        f"{URL_BASE}/posts"
    )

    parametros = None

    if usuario is not None:

        parametros = {
            "userId": usuario
        }

    publicaciones = obtener_json(
        url,
        parametros
    )

    if publicaciones is None:

        return

    print()
    print("PUBLICACIONES")
    print("=============")
    print()

    for publicacion in publicaciones:

        print(
            f"ID: "
            f"{publicacion.get('id')}"
        )

        print(
            f"Título: "
            f"{publicacion.get('title')}"
        )

        print(
            "-" * 40
        )

    print()

    print(
        f"Total: "
        f"{len(publicaciones)}"
    )


def crear_publicacion(
    titulo,
    contenido,
    usuario
):

    url = (
        f"{URL_BASE}/posts"
    )

    datos = {
        "title": titulo,
        "body": contenido,
        "userId": usuario
    }

    resultado = enviar_json(
        url,
        datos
    )

    if resultado is None:

        return

    print()
    print("PUBLICACIÓN ENVIADA")
    print("===================")
    print()

    print(
        f"ID: "
        f"{resultado.get('id')}"
    )

    print(
        f"Título: "
        f"{resultado.get('title')}"
    )

    print(
        f"Contenido: "
        f"{resultado.get('body')}"
    )

    print(
        f"Usuario: "
        f"{resultado.get('userId')}"
    )

    guardar_json(
        resultado,
        "ultima_publicacion.json"
    )


# -----------------------------
# Argumentos
# -----------------------------

parser = argparse.ArgumentParser(
    description=(
        "Cliente de API desarrollado "
        "con Python y requests."
    )
)


grupo = (
    parser.add_mutually_exclusive_group(
        required=True
    )
)


grupo.add_argument(
    "--usuarios",
    action="store_true",
    help="Lista los usuarios"
)


grupo.add_argument(
    "--usuario",
    type=int,
    metavar="ID",
    help="Consulta un usuario"
)


grupo.add_argument(
    "--posts",
    action="store_true",
    help="Lista publicaciones"
)


grupo.add_argument(
    "--crear",
    action="store_true",
    help="Crea una publicación"
)


parser.add_argument(
    "--titulo",
    help="Título de la publicación"
)


parser.add_argument(
    "--contenido",
    help="Contenido de la publicación"
)


parser.add_argument(
    "--autor",
    type=int,
    default=1,
    help=(
        "ID del usuario. "
        "Por defecto: 1"
    )
)


parser.add_argument(
    "--filtrar-usuario",
    type=int,
    metavar="ID",
    help=(
        "Filtra publicaciones "
        "por usuario"
    )
)


args = parser.parse_args()


# -----------------------------
# Validación
# -----------------------------

if (
    args.usuario is not None
    and args.usuario < 1
):

    parser.error(
        "El ID del usuario debe "
        "ser mayor que cero."
    )


if (
    args.filtrar_usuario is not None
    and args.filtrar_usuario < 1
):

    parser.error(
        "El ID para filtrar debe "
        "ser mayor que cero."
    )


if args.crear:

    if not args.titulo:

        parser.error(
            "--crear necesita "
            "--titulo"
        )

    if not args.contenido:

        parser.error(
            "--crear necesita "
            "--contenido"
        )

    if args.autor < 1:

        parser.error(
            "--autor debe ser "
            "mayor que cero"
        )


# -----------------------------
# Programa principal
# -----------------------------

logging.info(
    "Programa iniciado"
)


if args.usuarios:

    listar_usuarios()

elif args.usuario is not None:

    consultar_usuario(
        args.usuario
    )

elif args.posts:

    listar_publicaciones(
        args.filtrar_usuario
    )

elif args.crear:

    crear_publicacion(
        args.titulo,
        args.contenido,
        args.autor
    )


logging.info(
    "Programa finalizado"
)
```

---

### 127. Práctica de ampliación

Crea:

```text
cliente_api_v2.py
```

y añade nuevas funciones progresivamente.

#### Ampliación 1

Añade:

```text
--guardar-usuarios
```

para guardar la lista completa en:

```text
resultados/usuarios.json
```

#### Ampliación 2

Permite limitar el número de publicaciones mostradas:

```powershell
python cliente_api_v2.py --posts --limite 5
```

#### Ampliación 3

Añade una opción:

```text
--detallado
```

para mostrar:

```text
URL utilizada
código HTTP
tipo de contenido
```

#### Ampliación 4

Añade un contador de operaciones al log.

Por ejemplo:

```text
INFO - 10 usuarios recibidos
```

o:

```text
INFO - 5 publicaciones mostradas
```

---

### 128. Reto: comprobador de servicios web

Desarrolla:

```text
monitor_web.py
```

El programa recibirá un archivo:

```text
datos/servicios.txt
```

con direcciones como:

```text
https://example.com
https://www.python.org
```

El programa deberá:

1. Leer las URLs desde el archivo.
2. Realizar una petición GET a cada una.
3. Utilizar `timeout`.
4. Controlar errores de conexión.
5. Mostrar el código HTTP.
6. Registrar el resultado mediante `logging`.
7. Generar un informe en:

```text
resultados/estado_servicios.txt
```

El resultado podría tener esta estructura:

```text
ESTADO DE SERVICIOS
===================

https://example.com
HTTP: 200
Estado: DISPONIBLE

https://www.python.org
HTTP: 200
Estado: DISPONIBLE
```

!!! note "HTTP y disponibilidad"

    En esta práctica estamos comprobando la respuesta HTTP del servicio.

    Esto proporciona información diferente a una prueba de conectividad mediante `ping`.

---

### 129. Reto final del capítulo

Desarrolla una herramienta llamada:

```text
gestor_api.py
```

Deberá incluir como mínimo:

```text
1. argparse

2. requests

3. GET

4. POST

5. params

6. json=

7. respuesta.json()

8. raise_for_status()

9. timeout

10. control de excepciones

11. logging

12. almacenamiento de algún
    resultado en JSON
```

El programa deberá disponer de:

```powershell
python gestor_api.py --help
```

y permitir realizar al menos:

```text
una consulta GET
```

y:

```text
una operación POST
```

!!! success "Objetivo"

    Si completas esta práctica, ya eres capaz de construir un cliente básico para una API HTTP utilizando Python.

---

## 130. Qué hemos aprendido en el capítulo 5

Comenzamos estudiando el modelo:

```text
CLIENTE
   │
   │ petición HTTP
   ▼
SERVIDOR
   │
   │ respuesta HTTP
   ▼
CLIENTE
```

Después instalamos:

```python
requests
```

y realizamos peticiones:

```python
requests.get()
```

Aprendimos a consultar:

```python
respuesta.status_code
```

```python
respuesta.headers
```

```python
respuesta.text
```

También aprendimos a comprobar errores mediante:

```python
respuesta.raise_for_status()
```

---

### 131. APIs y JSON

Después introdujimos el concepto de:

```text
API
```

y trabajamos con respuestas:

```text
JSON
```

Utilizamos:

```python
datos = respuesta.json()
```

para convertir el JSON recibido en estructuras Python.

Podemos recibir:

```text
JSON
 │
 ▼
dict
```

o:

```text
JSON
 │
 ▼
list
```

y posteriormente utilizar las técnicas de Python que ya conocemos.

---

### 132. GET

Utilizamos:

```python
requests.get()
```

para solicitar información.

También aprendimos a enviar parámetros:

```python
parametros = {
    "userId": 1
}
```

mediante:

```python
requests.get(
    url,
    params=parametros,
    timeout=10
)
```

---

### 133. POST

Después utilizamos:

```python
requests.post()
```

para enviar información.

Preparamos un diccionario:

```python
datos = {
    "nombre": "PC01",
    "ip": "192.168.1.20"
}
```

y lo enviamos como JSON:

```python
requests.post(
    url,
    json=datos,
    timeout=10
)
```

---

### 134. Control de errores

También hemos aprendido que una comunicación de red puede fallar.

Hemos trabajado con:

```text
Timeout
ConnectionError
HTTPError
JSONDecodeError
RequestException
```

y hemos combinado:

```python
try
```

```python
except
```

con las operaciones HTTP.

---

### 135. Integración con capítulos anteriores

Este capítulo no funciona de forma aislada.

Hemos utilizado conocimientos anteriores:

```text
Capítulo 1
archivos
pathlib
JSON en archivos

        │
        ▼

Capítulo 2
concepto de ejecución
y diagnóstico

        │
        ▼

Capítulo 3
automatización
bucles
procesamiento repetitivo

        │
        ▼

Capítulo 4
argparse
excepciones
logging

        │
        ▼

Capítulo 5
HTTP
requests
APIs
GET
POST
JSON
```

Ahora podemos construir programas que no trabajan únicamente con el ordenador local.

También pueden intercambiar información con servicios disponibles a través de la red.

---

### 136. Patrón general aprendido

Podemos resumir el capítulo mediante:

```text
          INICIO
            │
            ▼
        argumentos
            │
            ▼
         validar
            │
            ▼
      preparar petición
            │
            ▼
     ┌──────HTTP───────┐
     │                 │
     ▼                 ▼
    GET               POST
     │                 │
     └────────┬────────┘
              │
              ▼
          respuesta
              │
              ▼
      código de estado
              │
              ▼
           JSON
              │
              ▼
        datos Python
              │
        ┌─────┼─────┐
        │     │     │
        ▼     ▼     ▼
      mostrar guardar log
        │     │     │
        └─────┼─────┘
              │
              ▼
             FIN
```

---

### 137. Buenas prácticas

Podemos establecer algunas reglas para nuestros clientes HTTP:

1. Utiliza `timeout` en las peticiones.

2. Controla los errores de conexión.

3. Comprueba los errores HTTP.

4. No asumas que cualquier respuesta contiene JSON válido.

5. Consulta la documentación de la API.

6. Valida los datos antes de enviarlos.

7. Utiliza `params=` para los parámetros de consulta.

8. Utiliza `json=` cuando la API espere datos JSON.

9. No publiques contraseñas, tokens ni claves de API.

10. Utiliza logs cuando necesites conservar información sobre las operaciones realizadas.

---

## 138. Fin del capítulo

!!! success "Capítulo 5 completado"

    Has completado el capítulo dedicado a **peticiones HTTP y consumo de APIs**.

    Ya sabes:

    - Realizar peticiones HTTP desde Python.
    - Utilizar la biblioteca `requests`.
    - Interpretar códigos de estado HTTP.
    - Realizar peticiones GET.
    - Enviar parámetros.
    - Realizar peticiones POST.
    - Enviar datos JSON.
    - Procesar respuestas JSON.
    - Controlar errores de comunicación.
    - Utilizar tiempos de espera.
    - Guardar respuestas en archivos.
    - Registrar las operaciones mediante logs.
    - Construir un cliente básico de una API.

El siguiente paso será utilizar Python para realizar **diagnóstico de red directamente mediante sockets**.

Trabajaremos con:

```python
socket
```

y aprenderemos a comprobar la conectividad a nivel de puerto y a realizar resolución de nombres DNS desde nuestros programas.