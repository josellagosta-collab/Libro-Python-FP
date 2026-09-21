# Capítulo 4. Scripting avanzado y control de errores

Hasta ahora hemos creado programas Python que realizan tareas como:

- Leer y escribir archivos.
- Procesar archivos CSV.
- Ejecutar comandos del sistema.
- Comprobar equipos de una red.
- Automatizar operaciones repetitivas.
- Crear copias de seguridad.
- Generar informes.

Muchos de estos programas contienen dentro del propio código los valores que necesitan para funcionar.

Por ejemplo:

```python
ip = "192.168.1.1"
```

o:

```python
archivo = "inventario.csv"
```

Esto significa que, si queremos utilizar otra dirección IP o trabajar con otro archivo, debemos modificar el programa.

En este capítulo aprenderemos a crear scripts más flexibles y reutilizables.

Podremos ejecutar programas como:

```powershell
python comprobar.py 192.168.1.1
```

o:

```powershell
python informe.py inventario.csv
```

Los valores escritos después del nombre del programa serán enviados a Python como **argumentos de la línea de comandos**.

---

## 1. ¿Qué es un argumento de línea de comandos?

Cuando ejecutamos:

```powershell
python programa.py
```

estamos indicando a Python qué archivo queremos ejecutar.

Pero también podemos añadir información:

```powershell
python programa.py hola
```

En este caso:

```text
hola
```

es un argumento.

Podemos utilizar varios:

```powershell
python programa.py Jose 25 Barcelona
```

Conceptualmente:

```text
python programa.py Jose 25 Barcelona
       │          │    │     │
       │          │    │     └── argumento 3
       │          │    └──────── argumento 2
       │          └───────────── argumento 1
       │
       └──────────────────────── programa
```

Los argumentos permiten proporcionar información al programa **en el momento de ejecutarlo**.

Esto evita tener que modificar continuamente el código.

---

## 2. El módulo `sys`

Python incluye el módulo:

```python
sys
```

Este módulo proporciona diferentes funciones relacionadas con el intérprete de Python.

Para utilizarlo escribimos:

```python
import sys
```

Dentro de este módulo encontramos:

```python
sys.argv
```

`argv` procede de:

```text
argument vector
```

y contiene los argumentos utilizados para ejecutar el programa.

---

## 3. Nuestro primer programa con `sys.argv`

Vamos a crear una nueva estructura para las prácticas del capítulo.

Dentro de:

```text
practicas/
```

crea:

```text
capitulo4/
```

y dentro:

```text
programas/
```

La estructura inicial será:

```text
practicas/
└── capitulo4/
    └── programas/
```

Dentro de:

```text
practicas/capitulo4/programas/
```

crea:

```text
primer_argumento.py
```

Escribe:

```python
import sys


print(sys.argv)
```

Guarda el archivo.

Abre el terminal integrado de VS Code y ejecuta:

```powershell
python primer_argumento.py
```

Obtendremos algo parecido a:

```text
['primer_argumento.py']
```

Ahora ejecuta:

```powershell
python primer_argumento.py hola
```

Obtendremos:

```text
['primer_argumento.py', 'hola']
```

Finalmente prueba:

```powershell
python primer_argumento.py hola mundo
```

Resultado:

```text
['primer_argumento.py', 'hola', 'mundo']
```

!!! note "`sys.argv` es una lista"

    `sys.argv` contiene una lista de cadenas de texto.

    Por tanto, podemos trabajar con ella utilizando las mismas técnicas que ya conocemos para trabajar con listas.

---

## 4. La posición de los argumentos

Observa el resultado:

```python
[
    "primer_argumento.py",
    "hola",
    "mundo"
]
```

Cada elemento ocupa una posición:

```text
posición 0 → primer_argumento.py
posición 1 → hola
posición 2 → mundo
```

Podemos acceder a ellos mediante:

```python
sys.argv[0]
sys.argv[1]
sys.argv[2]
```

Hay un detalle muy importante:

> `sys.argv[0]` contiene normalmente el nombre o la ruta utilizada para ejecutar el script.

Por tanto, el primer argumento proporcionado por el usuario estará en:

```python
sys.argv[1]
```

---

## 5. Acceder a un argumento

Modifica:

```text
primer_argumento.py
```

para que contenga:

```python
import sys


print(
    f"Programa: {sys.argv[0]}"
)

print(
    f"Primer argumento: {sys.argv[1]}"
)
```

Ejecuta:

```powershell
python primer_argumento.py Barcelona
```

Obtendremos algo parecido a:

```text
Programa: primer_argumento.py
Primer argumento: Barcelona
```

Prueba ahora:

```powershell
python primer_argumento.py 192.168.1.1
```

Resultado:

```text
Programa: primer_argumento.py
Primer argumento: 192.168.1.1
```

El programa no ha cambiado.

Lo único que hemos cambiado es el argumento utilizado durante la ejecución.

---

## 6. ¿Qué ocurre si falta el argumento?

Ejecuta:

```powershell
python primer_argumento.py
```

Nuestro programa intenta acceder a:

```python
sys.argv[1]
```

pero ese elemento no existe.

Obtendremos un error similar a:

```text
IndexError: list index out of range
```

¿Por qué?

Porque la lista contiene únicamente:

```python
[
    "primer_argumento.py"
]
```

Existe:

```python
sys.argv[0]
```

pero no:

```python
sys.argv[1]
```

Este es un ejemplo perfecto de un problema que debemos controlar en un script profesional.

---

## 7. Comprobar el número de argumentos

Podemos conocer el número de elementos de la lista mediante:

```python
len(sys.argv)
```

Crea:

```text
numero_argumentos.py
```

Escribe:

```python
import sys


print(
    f"Número de elementos: "
    f"{len(sys.argv)}"
)

print(sys.argv)
```

Ejecuta:

```powershell
python numero_argumentos.py
```

Podemos obtener:

```text
Número de elementos: 1
['numero_argumentos.py']
```

Ahora:

```powershell
python numero_argumentos.py hola
```

Resultado:

```text
Número de elementos: 2
['numero_argumentos.py', 'hola']
```

Y:

```powershell
python numero_argumentos.py hola mundo
```

Resultado:

```text
Número de elementos: 3
['numero_argumentos.py', 'hola', 'mundo']
```

Recuerda que el nombre del programa también ocupa una posición.

---

## 8. Evitar el error cuando falta un argumento

Podemos comprobar primero:

```python
if len(sys.argv) < 2:
```

Crea:

```text
argumento_seguro.py
```

Escribe:

```python
import sys


if len(sys.argv) < 2:

    print(
        "ERROR: debes indicar "
        "un argumento."
    )

else:

    valor = sys.argv[1]

    print(
        f"Argumento recibido: {valor}"
    )
```

Ejecuta:

```powershell
python argumento_seguro.py
```

Ahora no se produce una excepción.

Obtendremos:

```text
ERROR: debes indicar un argumento.
```

Ejecuta:

```powershell
python argumento_seguro.py servidor
```

Resultado:

```text
Argumento recibido: servidor
```

Nuestro script ya es más robusto.

---

## 9. Finalizar un programa con `sys.exit()`

En el programa anterior hemos utilizado:

```python
else:
```

Otra posibilidad consiste en finalizar el programa cuando detectamos un problema.

Podemos utilizar:

```python
sys.exit()
```

Por ejemplo:

```python
import sys


if len(sys.argv) < 2:

    print(
        "ERROR: debes indicar "
        "un argumento."
    )

    sys.exit()


valor = sys.argv[1]

print(
    f"Argumento recibido: {valor}"
)
```

Si falta el argumento:

```text
ERROR
  │
  ▼
sys.exit()
  │
  ▼
FIN DEL PROGRAMA
```

El código posterior no se ejecutará.

---

### Código de salida

Podemos indicar un código:

```python
sys.exit(1)
```

Habitualmente:

```text
0 → ejecución correcta
valor distinto de 0 → se ha producido algún problema
```

Por ejemplo:

```python
if len(sys.argv) < 2:

    print(
        "ERROR: falta un argumento."
    )

    sys.exit(1)
```

Esta idea está relacionada con los códigos de retorno que estudiamos al utilizar:

```python
subprocess
```

Los programas pueden comunicar al sistema operativo si han finalizado correctamente.

---

## 10. Crear un script parametrizable

Vamos a aplicar lo aprendido a una tarea conocida.

Crea:

```text
comprobar_equipo.py
```

Escribe:

```python
import subprocess
import sys


if len(sys.argv) < 2:

    print(
        "Uso:"
    )

    print(
        "python comprobar_equipo.py "
        "DIRECCION_IP"
    )

    sys.exit(1)


ip = sys.argv[1]


resultado = subprocess.run(
    [
        "ping",
        "-n",
        "1",
        ip
    ],
    capture_output=True,
    text=True
)


if resultado.returncode == 0:

    print(
        f"{ip}: RESPONDE"
    )

else:

    print(
        f"{ip}: NO RESPONDE"
    )
```

Ahora podemos utilizar el mismo programa con diferentes equipos.

Por ejemplo:

```powershell
python comprobar_equipo.py 127.0.0.1
```

o:

```powershell
python comprobar_equipo.py 192.168.1.1
```

o:

```powershell
python comprobar_equipo.py 8.8.8.8
```

No necesitamos modificar:

```text
comprobar_equipo.py
```

para cambiar el equipo.

---

## 11. Comparar dos formas de programar

Antes podíamos tener:

```python
ip = "192.168.1.1"
```

Cada vez que quisiéramos comprobar otra dirección tendríamos que modificar el código:

```python
ip = "192.168.1.20"
```

Ahora utilizamos:

```python
ip = sys.argv[1]
```

y ejecutamos:

```powershell
python comprobar_equipo.py 192.168.1.20
```

Podemos representar la diferencia:

```text
VALOR DENTRO DEL PROGRAMA

código
  │
  └── IP fija


ARGUMENTO

terminal
   │
   ▼
argumento
   │
   ▼
sys.argv
   │
   ▼
programa
```

La segunda solución hace que nuestro script sea mucho más reutilizable.

---

## 12. Utilizar varios argumentos

Un programa puede recibir más de un argumento.

Crea:

```text
datos_equipo.py
```

Escribe:

```python
import sys


if len(sys.argv) < 4:

    print(
        "Uso:"
    )

    print(
        "python datos_equipo.py "
        "NOMBRE IP UBICACION"
    )

    sys.exit(1)


nombre = sys.argv[1]
ip = sys.argv[2]
ubicacion = sys.argv[3]


print()
print("DATOS DEL EQUIPO")
print("================")
print()

print(
    f"Nombre: {nombre}"
)

print(
    f"IP: {ip}"
)

print(
    f"Ubicación: {ubicacion}"
)
```

Ejecuta:

```powershell
python datos_equipo.py PC01 192.168.1.20 Aula1
```

Resultado:

```text
DATOS DEL EQUIPO
================

Nombre: PC01
IP: 192.168.1.20
Ubicación: Aula1
```

La correspondencia será:

```text
sys.argv[0] → datos_equipo.py
sys.argv[1] → PC01
sys.argv[2] → 192.168.1.20
sys.argv[3] → Aula1
```

---

## 13. Argumentos que contienen espacios

Supongamos que queremos utilizar:

```text
Aula informática
```

Si ejecutamos:

```powershell
python datos_equipo.py PC01 192.168.1.20 Aula informática
```

la terminal interpreta:

```text
Aula
```

e:

```text
informática
```

como argumentos diferentes.

Cuando un argumento contiene espacios debemos utilizar comillas:

```powershell
python datos_equipo.py PC01 192.168.1.20 "Aula informática"
```

Ahora:

```python
sys.argv[3]
```

contendrá:

```text
Aula informática
```

!!! tip "Argumentos con espacios"

    Utiliza comillas cuando un argumento contenga espacios:

    ```powershell
    python programa.py "texto con espacios"
    ```

---

## 14. Todos los argumentos son cadenas de texto

Existe otro detalle importante.

Ejecuta:

```powershell
python programa.py 25
```

Aunque hemos escrito:

```text
25
```

`sys.argv` lo recibe como:

```python
"25"
```

es decir, como una cadena de texto.

Si necesitamos un número debemos convertirlo:

```python
numero = int(
    sys.argv[1]
)
```

Por ejemplo:

```python
import sys


if len(sys.argv) < 2:

    print(
        "Debes indicar un número."
    )

    sys.exit(1)


numero = int(
    sys.argv[1]
)


print(
    f"El doble es: {numero * 2}"
)
```

Si ejecutamos:

```powershell
python programa.py 25
```

obtendremos:

```text
El doble es: 50
```

Pero aparece una nueva pregunta:

> ¿Qué ocurre si el usuario escribe una palabra en lugar de un número?

Por ejemplo:

```powershell
python programa.py hola
```

La instrucción:

```python
int("hola")
```

provocará:

```text
ValueError
```

Más adelante estudiaremos cómo controlar correctamente este tipo de excepciones.

---

## 15. Crear un comprobador de rango parametrizable

Podemos recuperar una de las prácticas del capítulo anterior y mejorarla.

En lugar de tener:

```python
red = "192.168.1"
inicio = 100
fin = 110
```

podemos ejecutar:

```powershell
python comprobar_rango.py 192.168.1 100 110
```

Crea:

```text
comprobar_rango.py
```

Escribe:

```python
import subprocess
import sys


if len(sys.argv) != 4:

    print()
    print("Uso:")

    print(
        "python comprobar_rango.py "
        "RED INICIO FIN"
    )

    print()

    print("Ejemplo:")

    print(
        "python comprobar_rango.py "
        "192.168.1 100 110"
    )

    sys.exit(1)


red = sys.argv[1]

inicio = int(
    sys.argv[2]
)

fin = int(
    sys.argv[3]
)


print()
print("COMPROBACIÓN DE RED")
print("===================")
print()

print(
    f"Red: {red}"
)

print(
    f"Rango: {inicio} - {fin}"
)

print()


for numero in range(
    inicio,
    fin + 1
):

    ip = f"{red}.{numero}"

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

        print(
            f"{ip}: RESPONDE"
        )

    else:

        print(
            f"{ip}: NO RESPONDE"
        )
```

Podemos utilizar:

```powershell
python comprobar_rango.py 192.168.1 1 10
```

o:

```powershell
python comprobar_rango.py 192.168.1 100 120
```

El programa es el mismo.

Los parámetros determinan qué debe hacer.

!!! warning "Redes autorizadas"

    Realiza las comprobaciones únicamente sobre redes y equipos en los que tengas autorización.

---

## 16. Parámetros frente a `input()`

Hasta ahora también podíamos solicitar información mediante:

```python
input()
```

Por ejemplo:

```python
ip = input(
    "Introduce la dirección IP: "
)
```

Esto requiere interacción:

```text
programa
   │
   ▼
pregunta
   │
   ▼
usuario escribe
   │
   ▼
programa continúa
```

Con argumentos:

```powershell
python comprobar_equipo.py 192.168.1.1
```

el proceso es:

```text
comando completo
      │
      ▼
   programa
      │
      ▼
    acción
```

Los dos métodos son válidos, pero tienen usos diferentes.

### `input()`

Resulta adecuado para programas interactivos.

```python
nombre = input(
    "Introduce tu nombre: "
)
```

### Argumentos

Resultan especialmente útiles para scripts que queremos ejecutar directamente:

```powershell
python backup.py datos
```

También facilitan posteriormente la automatización de los scripts desde otras herramientas.

---

## 17. Práctica guiada: información de un archivo

Vamos a crear un script que reciba el nombre de un archivo como argumento.

Crea:

```text
informacion_archivo.py
```

Escribe:

```python
import sys

from pathlib import Path


if len(sys.argv) != 2:

    print()
    print("Uso:")

    print(
        "python informacion_archivo.py "
        "ARCHIVO"
    )

    sys.exit(1)


archivo = Path(
    sys.argv[1]
)


if not archivo.exists():

    print(
        f"ERROR: no existe "
        f"{archivo}"
    )

    sys.exit(1)


if not archivo.is_file():

    print(
        f"ERROR: {archivo} "
        f"no es un archivo."
    )

    sys.exit(1)


tamano = (
    archivo.stat().st_size
)


print()
print("INFORMACIÓN DEL ARCHIVO")
print("=======================")
print()

print(
    f"Nombre: {archivo.name}"
)

print(
    f"Extensión: {archivo.suffix}"
)

print(
    f"Tamaño: {tamano} bytes"
)

print(
    f"Ruta: {archivo.resolve()}"
)
```

Podemos ejecutarlo indicando una ruta real.

Por ejemplo:

```powershell
python informacion_archivo.py inventario.csv
```

Si la ruta contiene espacios:

```powershell
python informacion_archivo.py "C:\Mis datos\inventario.csv"
```

---

## 18. Práctica propuesta: copiador de archivos

Crea:

```text
copiar_archivo.py
```

El programa deberá ejecutarse de esta forma:

```powershell
python copiar_archivo.py origen.txt copia.txt
```

Los argumentos serán:

```text
sys.argv[1] → archivo de origen
sys.argv[2] → archivo de destino
```

El programa deberá:

1. Comprobar que se han recibido exactamente dos argumentos.
2. Convertir ambos argumentos en objetos `Path`.
3. Comprobar que el archivo de origen existe.
4. Comprobar que el origen es realmente un archivo.
5. Copiarlo utilizando `shutil.copy2()`.
6. Mostrar un mensaje indicando que la operación se ha realizado.

!!! example "Resultado esperado"

    Una ejecución podría ser:

    ```powershell
    python copiar_archivo.py datos.txt copia.txt
    ```

    y mostrar:

    ```text
    COPIA DE ARCHIVO
    ================

    Origen: datos.txt
    Destino: copia.txt

    Archivo copiado correctamente.
    ```

Esta práctica combina:

```text
sys.argv
   +
pathlib
   +
shutil
```

---

## 19. Práctica propuesta: backup parametrizable

Recupera el programa de copias de seguridad del capítulo anterior.

En lugar de utilizar un directorio fijo:

```python
ORIGEN = (
    DIRECTORIO_CAPITULO
    / "datos_empresa"
)
```

el directorio deberá recibirse mediante:

```python
sys.argv[1]
```

La ejecución será:

```powershell
python backup.py "C:\Datos"
```

El programa deberá:

- Comprobar que existe el argumento.
- Comprobar que la ruta existe.
- Comprobar que es un directorio.
- Crear automáticamente el directorio de backups.
- Añadir fecha y hora al nombre de la copia.
- Realizar la copia mediante `shutil.copytree()`.
- Mostrar el destino generado.

De esta forma, el mismo script podrá utilizarse para realizar copias de diferentes directorios.

---

## 20. Limitaciones de `sys.argv`

`sys.argv` funciona correctamente para programas sencillos.

Por ejemplo:

```powershell
python comprobar.py 192.168.1.1
```

Pero imaginemos un programa más completo:

```powershell
python diagnostico.py 192.168.1.1 5 informe.txt True
```

¿Qué significa cada valor?

```text
192.168.1.1
5
informe.txt
True
```

Tenemos que recordar la posición de cada argumento:

```python
sys.argv[1]
sys.argv[2]
sys.argv[3]
sys.argv[4]
```

Además, tendremos que programar manualmente:

- La comprobación de argumentos.
- Los mensajes de ayuda.
- Las conversiones.
- Los argumentos opcionales.
- Los valores predeterminados.

A medida que un script crece, esta solución resulta poco cómoda.

Sería mucho más claro poder escribir algo como:

```powershell
python diagnostico.py 192.168.1.1 --intentos 5
```

o:

```powershell
python diagnostico.py 192.168.1.1 --informe resultado.txt
```

Python dispone de un módulo específicamente diseñado para construir este tipo de interfaces de línea de comandos:

```python
argparse
```

Este será el siguiente paso.

---

## Resumen

En esta primera parte del capítulo hemos aprendido a proporcionar información a nuestros scripts desde la línea de comandos.

La pieza fundamental ha sido:

```python
sys.argv
```

Hemos aprendido que:

```text
sys.argv[0] → programa
sys.argv[1] → primer argumento
sys.argv[2] → segundo argumento
...
```

También hemos utilizado:

```python
len(sys.argv)
```

para comprobar el número de argumentos y:

```python
sys.exit()
```

para finalizar un programa cuando no puede continuar.

El cambio fundamental respecto a nuestros primeros scripts es:

```text
ANTES

datos dentro
del código
    │
    ▼
 programa


AHORA

argumentos
    │
    ▼
sys.argv
    │
    ▼
 programa
```

Gracias a ello podemos crear scripts reutilizables:

```powershell
python comprobar_equipo.py 192.168.1.1
```

```powershell
python comprobar_equipo.py 192.168.1.20
```

```powershell
python informacion_archivo.py datos.csv
```

sin modificar el código fuente.

En la siguiente parte aprenderemos a utilizar:

```python
argparse
```

para construir scripts de línea de comandos más claros y profesionales, con argumentos obligatorios, argumentos opcionales, valores predeterminados y ayuda automática.

---

## 21. Introducción a `argparse`

En la parte anterior hemos aprendido a recibir argumentos mediante:

```python
sys.argv
```

Por ejemplo:

```powershell
python comprobar_equipo.py 192.168.1.1
```

y recuperábamos la dirección mediante:

```python
ip = sys.argv[1]
```

Este sistema funciona bien para programas sencillos.

Sin embargo, cuando aumenta el número de parámetros aparecen algunos problemas:

```text
¿Qué significa cada argumento?
¿Cuáles son obligatorios?
¿Cuáles son opcionales?
¿Qué tipo de dato necesita cada uno?
¿Qué ocurre si falta alguno?
¿Cómo mostramos ayuda al usuario?
```

Python incluye un módulo específicamente diseñado para solucionar estos problemas:

```python
argparse
```

`argparse` permite crear programas de línea de comandos mucho más claros y fáciles de utilizar.

---

## 22. Nuestro primer programa con `argparse`

Dentro de:

```text
practicas/capitulo4/programas/
```

crea:

```text
primer_argparse.py
```

Escribe:

```python
import argparse


parser = argparse.ArgumentParser()

parser.add_argument(
    "nombre"
)

args = parser.parse_args()

print(
    f"Hola {args.nombre}"
)
```

Ejecuta:

```powershell
python primer_argparse.py Jose
```

Obtendremos:

```text
Hola Jose
```

Aunque el programa es muy sencillo, han ocurrido varias cosas.

Primero creamos un analizador de argumentos:

```python
parser = argparse.ArgumentParser()
```

Después indicamos que queremos recibir un argumento:

```python
parser.add_argument(
    "nombre"
)
```

Finalmente analizamos los argumentos recibidos:

```python
args = parser.parse_args()
```

Y podemos acceder al argumento mediante:

```python
args.nombre
```

El proceso es:

```text
Terminal
   │
   ▼
argumentos
   │
   ▼
ArgumentParser
   │
   ▼
parse_args()
   │
   ▼
args
   │
   ▼
args.nombre
```

---

## 23. Argumentos posicionales

El argumento:

```python
parser.add_argument(
    "nombre"
)
```

se denomina **argumento posicional**.

Esto significa que su posición es importante.

Por ejemplo:

```powershell
python primer_argparse.py Jose
```

`Jose` corresponde a:

```text
nombre
```

Podemos añadir más argumentos.

Crea:

```text
datos_equipo_argparse.py
```

Escribe:

```python
import argparse


parser = argparse.ArgumentParser()

parser.add_argument(
    "nombre"
)

parser.add_argument(
    "ip"
)

parser.add_argument(
    "ubicacion"
)

args = parser.parse_args()


print()
print("DATOS DEL EQUIPO")
print("================")
print()

print(
    f"Nombre: {args.nombre}"
)

print(
    f"IP: {args.ip}"
)

print(
    f"Ubicación: {args.ubicacion}"
)
```

Ejecuta:

```powershell
python datos_equipo_argparse.py PC01 192.168.1.20 "Aula 1"
```

Obtendremos:

```text
DATOS DEL EQUIPO
================

Nombre: PC01
IP: 192.168.1.20
Ubicación: Aula 1
```

La correspondencia será:

```text
PC01
 │
 ▼
args.nombre


192.168.1.20
     │
     ▼
   args.ip


"Aula 1"
    │
    ▼
args.ubicacion
```

---

## 24. Ayuda automática

Una de las ventajas de `argparse` es que crea automáticamente un sistema de ayuda.

Ejecuta:

```powershell
python datos_equipo_argparse.py -h
```

También podemos utilizar:

```powershell
python datos_equipo_argparse.py --help
```

Aparecerá información similar a:

```text
usage: datos_equipo_argparse.py
       [-h]
       nombre ip ubicacion

positional arguments:
  nombre
  ip
  ubicacion

options:
  -h, --help
        show this help message and exit
```

Nosotros no hemos programado:

```text
-h
```

ni:

```text
--help
```

`argparse` los ha creado automáticamente.

!!! tip "Probar siempre --help"

    Cuando trabajes con un programa creado con `argparse`, una de las primeras pruebas debería ser:

    ```powershell
    python programa.py --help
    ```

    De esta forma puedes comprobar rápidamente cómo debe utilizarse.

---

## 25. Añadir una descripción

Podemos mejorar la ayuda añadiendo una descripción del programa.

Modifica:

```python
parser = argparse.ArgumentParser()
```

por:

```python
parser = argparse.ArgumentParser(
    description=(
        "Muestra información "
        "sobre un equipo."
    )
)
```

Ahora ejecuta:

```powershell
python datos_equipo_argparse.py --help
```

La descripción aparecerá en la ayuda.

Esto resulta especialmente útil cuando nuestros scripts comienzan a crecer.

---

## 26. Añadir ayuda a cada argumento

También podemos explicar individualmente cada argumento.

```python
parser.add_argument(
    "nombre",
    help="Nombre del equipo"
)

parser.add_argument(
    "ip",
    help="Dirección IP del equipo"
)

parser.add_argument(
    "ubicacion",
    help="Ubicación del equipo"
)
```

Ejecuta nuevamente:

```powershell
python datos_equipo_argparse.py --help
```

Ahora la ayuda resulta mucho más clara:

```text
positional arguments:

nombre
    Nombre del equipo

ip
    Dirección IP del equipo

ubicacion
    Ubicación del equipo
```

!!! note "Documentar la interfaz"

    Un script puede funcionar perfectamente y, sin embargo, resultar difícil de utilizar.

    Una buena interfaz de línea de comandos debe explicar claramente qué información necesita.

---

## 27. Control automático de argumentos obligatorios

Con `sys.argv` teníamos que comprobar manualmente:

```python
if len(sys.argv) < 2:
```

Con `argparse`, los argumentos posicionales son obligatorios por defecto.

Prueba:

```powershell
python datos_equipo_argparse.py
```

`argparse` detectará que faltan argumentos y mostrará automáticamente un mensaje de error.

No necesitamos programar:

```python
if len(sys.argv) != 4:
```

Esta es una de las ventajas de utilizar `argparse`.

---

## 28. Especificar el tipo de un argumento

Recordemos que con `sys.argv` todos los argumentos llegaban inicialmente como texto.

Por ejemplo:

```python
inicio = int(
    sys.argv[2]
)
```

Con `argparse` podemos indicar directamente el tipo:

```python
parser.add_argument(
    "inicio",
    type=int
)
```

`argparse` realizará la conversión automáticamente.

Crea:

```text
rango_argparse.py
```

Escribe:

```python
import argparse


parser = argparse.ArgumentParser(
    description=(
        "Genera un rango "
        "de números."
    )
)

parser.add_argument(
    "inicio",
    type=int,
    help="Primer número"
)

parser.add_argument(
    "fin",
    type=int,
    help="Último número"
)

args = parser.parse_args()


for numero in range(
    args.inicio,
    args.fin + 1
):
    print(numero)
```

Ejecuta:

```powershell
python rango_argparse.py 5 10
```

Resultado:

```text
5
6
7
8
9
10
```

---

### ¿Qué ocurre si introducimos texto?

Prueba:

```powershell
python rango_argparse.py cinco diez
```

`argparse` detectará que:

```text
cinco
```

no puede convertirse a:

```python
int
```

y mostrará automáticamente un error.

No necesitamos escribir manualmente:

```python
int(sys.argv[1])
```

ni controlar ese error en este caso.

---

## 29. Mejorar el comprobador de red

Vamos a recuperar:

```text
comprobar_rango.py
```

pero esta vez utilizaremos `argparse`.

Crea:

```text
comprobar_rango_argparse.py
```

Escribe:

```python
import argparse
import subprocess


parser = argparse.ArgumentParser(
    description=(
        "Comprueba mediante ping "
        "un rango de direcciones IP."
    )
)

parser.add_argument(
    "red",
    help=(
        "Parte de red. "
        "Ejemplo: 192.168.1"
    )
)

parser.add_argument(
    "inicio",
    type=int,
    help="Primer host"
)

parser.add_argument(
    "fin",
    type=int,
    help="Último host"
)

args = parser.parse_args()


print()
print("COMPROBACIÓN DE RED")
print("===================")
print()

print(
    f"Red: {args.red}"
)

print(
    f"Rango: "
    f"{args.inicio}-{args.fin}"
)

print()


for numero in range(
    args.inicio,
    args.fin + 1
):

    ip = (
        f"{args.red}.{numero}"
    )

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

        print(
            f"{ip}: RESPONDE"
        )

    else:

        print(
            f"{ip}: NO RESPONDE"
        )
```

Ahora podemos ejecutar:

```powershell
python comprobar_rango_argparse.py 192.168.1 1 10
```

!!! warning "Redes autorizadas"

    Realiza estas comprobaciones únicamente sobre redes y equipos en los que tengas autorización.

---

## 30. Argumentos opcionales

Hasta ahora hemos utilizado argumentos posicionales.

También podemos crear argumentos opcionales.

Normalmente comienzan por:

```text
-
```

o:

```text
--
```

Por ejemplo:

```text
--intentos
```

Añadimos:

```python
parser.add_argument(
    "--intentos",
    type=int
)
```

Ahora podemos ejecutar:

```powershell
python programa.py --intentos 5
```

y recuperar el valor mediante:

```python
args.intentos
```

---

## 31. Valores predeterminados

Supongamos que queremos realizar un ping.

Normalmente utilizaremos:

```text
1 intento
```

pero queremos permitir al usuario modificarlo.

Podemos escribir:

```python
parser.add_argument(
    "--intentos",
    type=int,
    default=1,
    help="Número de intentos"
)
```

Si ejecutamos:

```powershell
python programa.py
```

el valor será:

```python
args.intentos == 1
```

Si ejecutamos:

```powershell
python programa.py --intentos 5
```

será:

```python
args.intentos == 5
```

Por tanto:

```text
sin --intentos
       │
       ▼
 default=1


--intentos 5
       │
       ▼
      5
```

---

## 32. Comprobador con número de intentos

Crea:

```text
ping_argparse.py
```

Escribe:

```python
import argparse
import subprocess


parser = argparse.ArgumentParser(
    description=(
        "Comprueba la conectividad "
        "con un equipo."
    )
)

parser.add_argument(
    "ip",
    help="Dirección IP o nombre"
)

parser.add_argument(
    "--intentos",
    type=int,
    default=1,
    help=(
        "Número de paquetes "
        "enviados (por defecto: 1)"
    )
)

args = parser.parse_args()


resultado = subprocess.run(
    [
        "ping",
        "-n",
        str(args.intentos),
        args.ip
    ],
    capture_output=True,
    text=True
)


if resultado.returncode == 0:

    print(
        f"{args.ip}: RESPONDE"
    )

else:

    print(
        f"{args.ip}: NO RESPONDE"
    )
```

Podemos ejecutar:

```powershell
python ping_argparse.py 127.0.0.1
```

Se enviará un único ping.

También:

```powershell
python ping_argparse.py 127.0.0.1 --intentos 4
```

Ahora se realizarán cuatro intentos.

Observa esta línea:

```python
str(args.intentos)
```

Aunque `argparse` convierte el argumento a:

```python
int
```

`subprocess.run()` necesita que los elementos de la lista de argumentos sean cadenas.

Por eso volvemos a convertir el valor:

```python
str(args.intentos)
```

---

## 33. Forma corta y forma larga

Podemos permitir:

```text
-i
```

como versión corta de:

```text
--intentos
```

Escribimos:

```python
parser.add_argument(
    "-i",
    "--intentos",
    type=int,
    default=1,
    help="Número de intentos"
)
```

Ahora son válidas las dos formas:

```powershell
python ping_argparse.py 127.0.0.1 -i 4
```

y:

```powershell
python ping_argparse.py 127.0.0.1 --intentos 4
```

Ambas producen:

```python
args.intentos
```

con valor:

```text
4
```

---

## 34. Opciones que funcionan como interruptores

En ocasiones no queremos proporcionar un valor.

Simplemente queremos activar una opción.

Por ejemplo:

```text
--detallado
```

Podemos utilizar:

```python
parser.add_argument(
    "--detallado",
    action="store_true"
)
```

Si ejecutamos:

```powershell
python programa.py
```

obtendremos:

```python
args.detallado == False
```

Si ejecutamos:

```powershell
python programa.py --detallado
```

obtendremos:

```python
args.detallado == True
```

Podemos utilizar:

```python
if args.detallado:
    print(
        "Modo detallado activado"
    )
```

Este tipo de opción se conoce habitualmente como una **bandera** o *flag*.

---

## 35. Añadir modo detallado al ping

Modifica:

```text
ping_argparse.py
```

añadiendo:

```python
parser.add_argument(
    "-d",
    "--detallado",
    action="store_true",
    help=(
        "Muestra la salida "
        "completa de ping"
    )
)
```

Después de ejecutar `ping`, podemos utilizar:

```python
if args.detallado:

    print()
    print("SALIDA COMPLETA")
    print("===============")
    print()

    print(
        resultado.stdout
    )
```

Ahora:

```powershell
python ping_argparse.py 127.0.0.1
```

mostrará únicamente el resultado general.

Mientras que:

```powershell
python ping_argparse.py 127.0.0.1 --detallado
```

también mostrará la salida completa del comando.

---

## 36. Programa completo

Nuestro programa puede quedar así:

```python
import argparse
import subprocess


parser = argparse.ArgumentParser(
    description=(
        "Herramienta básica "
        "de comprobación de red."
    )
)

parser.add_argument(
    "ip",
    help=(
        "Dirección IP o nombre "
        "del equipo"
    )
)

parser.add_argument(
    "-i",
    "--intentos",
    type=int,
    default=1,
    help=(
        "Número de intentos "
        "(por defecto: 1)"
    )
)

parser.add_argument(
    "-d",
    "--detallado",
    action="store_true",
    help=(
        "Muestra la salida "
        "completa del comando"
    )
)

args = parser.parse_args()


resultado = subprocess.run(
    [
        "ping",
        "-n",
        str(args.intentos),
        args.ip
    ],
    capture_output=True,
    text=True
)


print()
print("RESULTADO")
print("=========")
print()


if resultado.returncode == 0:

    print(
        f"{args.ip}: RESPONDE"
    )

else:

    print(
        f"{args.ip}: NO RESPONDE"
    )


if args.detallado:

    print()
    print("SALIDA COMPLETA")
    print("===============")
    print()

    print(
        resultado.stdout
    )
```

Podemos probar:

```powershell
python ping_argparse.py --help
```

```powershell
python ping_argparse.py 127.0.0.1
```

```powershell
python ping_argparse.py 127.0.0.1 -i 4
```

```powershell
python ping_argparse.py 127.0.0.1 -i 4 -d
```

También:

```powershell
python ping_argparse.py 127.0.0.1 --intentos 4 --detallado
```

El mismo programa puede adoptar diferentes comportamientos sin modificar su código.

---

## 37. `sys.argv` frente a `argparse`

Ahora podemos comparar ambos sistemas.

### Utilizando `sys.argv`

```python
import sys


if len(sys.argv) != 3:

    print(
        "Uso: programa.py IP INTENTOS"
    )

    sys.exit(1)


ip = sys.argv[1]

intentos = int(
    sys.argv[2]
)
```

Debemos controlar manualmente:

```text
número de argumentos
posiciones
conversiones
mensajes de ayuda
errores
```

### Utilizando `argparse`

```python
import argparse


parser = argparse.ArgumentParser()

parser.add_argument(
    "ip"
)

parser.add_argument(
    "--intentos",
    type=int,
    default=1
)

args = parser.parse_args()
```

Ahora obtenemos automáticamente muchas de estas funciones.

!!! tip "¿Cuál debemos utilizar?"

    Para scripts muy pequeños, `sys.argv` puede ser suficiente.

    Cuando un script necesita varios parámetros, opciones, tipos de datos o ayuda para el usuario, `argparse` resulta normalmente mucho más adecuado.

---

## 38. Práctica guiada: información de archivos con `argparse`

Vamos a mejorar una práctica anterior.

Crea:

```text
archivo_argparse.py
```

Escribe:

```python
import argparse

from pathlib import Path


parser = argparse.ArgumentParser(
    description=(
        "Muestra información "
        "sobre un archivo."
    )
)

parser.add_argument(
    "archivo",
    help="Archivo que se analizará"
)

parser.add_argument(
    "-d",
    "--detallado",
    action="store_true",
    help=(
        "Muestra información "
        "adicional"
    )
)

args = parser.parse_args()


archivo = Path(
    args.archivo
)


if not archivo.exists():

    print(
        "ERROR: el archivo "
        "no existe."
    )

    raise SystemExit(1)


if not archivo.is_file():

    print(
        "ERROR: la ruta indicada "
        "no es un archivo."
    )

    raise SystemExit(1)


print()
print("INFORMACIÓN DEL ARCHIVO")
print("=======================")
print()

print(
    f"Nombre: {archivo.name}"
)

print(
    f"Tamaño: "
    f"{archivo.stat().st_size} bytes"
)


if args.detallado:

    print(
        f"Extensión: "
        f"{archivo.suffix}"
    )

    print(
        f"Ruta completa: "
        f"{archivo.resolve()}"
    )
```

Podemos utilizar:

```powershell
python archivo_argparse.py datos.txt
```

o:

```powershell
python archivo_argparse.py datos.txt --detallado
```

---

## 39. Práctica propuesta: backup con `argparse`

Crea:

```text
backup_argparse.py
```

El programa deberá permitir:

```powershell
python backup_argparse.py "C:\Datos"
```

y opcionalmente:

```powershell
python backup_argparse.py "C:\Datos" --destino "C:\Backups"
```

La definición de argumentos puede comenzar así:

```python
parser.add_argument(
    "origen",
    help=(
        "Directorio que se "
        "copiará"
    )
)

parser.add_argument(
    "-d",
    "--destino",
    default="backups",
    help=(
        "Directorio donde se "
        "guardarán las copias"
    )
)
```

El programa deberá:

1. Convertir las rutas mediante `Path`.
2. Comprobar que el origen existe.
3. Comprobar que el origen es un directorio.
4. Crear el directorio de destino si no existe.
5. Generar un nombre utilizando fecha y hora.
6. Realizar la copia con `shutil.copytree()`.
7. Mostrar la ruta de la copia creada.

!!! example "Prueba"

    Prueba primero con directorios que contengan únicamente archivos de práctica.

    Evita utilizar datos importantes mientras estás desarrollando el programa.

---

## 40. Práctica propuesta: generador de informes

Crea:

```text
informe_argparse.py
```

Queremos poder ejecutar:

```powershell
python informe_argparse.py inventario.csv
```

También:

```powershell
python informe_argparse.py inventario.csv --salida informe.txt
```

Y:

```powershell
python informe_argparse.py inventario.csv --salida informe.txt --detallado
```

El programa deberá aceptar:

```text
inventario
    argumento obligatorio

--salida
    argumento opcional

--detallado
    bandera opcional
```

Utiliza:

```python
type=str
```

para los argumentos de texto y:

```python
action="store_true"
```

para:

```text
--detallado
```

El objetivo de esta práctica no es únicamente generar el informe.

El objetivo principal es diseñar correctamente la **interfaz de línea de comandos**.

---

## 41. Diseñar una buena interfaz de línea de comandos

Cuando desarrollamos un script debemos pensar también en la persona que tendrá que utilizarlo.

No es lo mismo:

```powershell
python programa.py red 1 20 4 True informe.txt
```

que:

```powershell
python programa.py 192.168.1 --inicio 1 --fin 20 --intentos 4 --informe informe.txt
```

La segunda forma resulta mucho más fácil de comprender.

Una buena interfaz debe intentar que:

- Los argumentos tengan nombres claros.
- Los parámetros imprescindibles sean obligatorios.
- Los parámetros secundarios sean opcionales.
- Existan valores predeterminados razonables.
- Cada argumento tenga una descripción.
- `--help` explique cómo utilizar el programa.

Por ejemplo:

```powershell
python diagnostico.py --help
```

debería permitir comprender el funcionamiento del script sin necesidad de leer su código.

---

## 42. Práctica de integración

Vamos a diseñar la interfaz de una herramienta de diagnóstico.

El programa se llamará:

```text
diagnostico.py
```

Queremos poder ejecutar:

```powershell
python diagnostico.py 192.168.1.1
```

También:

```powershell
python diagnostico.py 192.168.1.1 --intentos 4
```

Y:

```powershell
python diagnostico.py 192.168.1.1 --intentos 4 --detallado
```

La estructura inicial será:

```python
import argparse


parser = argparse.ArgumentParser(
    description=(
        "Herramienta de "
        "diagnóstico de red."
    )
)


parser.add_argument(
    "equipo",
    help=(
        "Dirección IP o nombre "
        "del equipo"
    )
)


parser.add_argument(
    "-i",
    "--intentos",
    type=int,
    default=1,
    help=(
        "Número de intentos"
    )
)


parser.add_argument(
    "-d",
    "--detallado",
    action="store_true",
    help=(
        "Muestra información "
        "detallada"
    )
)


args = parser.parse_args()
```

Completa el programa utilizando:

```python
subprocess.run()
```

para ejecutar:

```text
ping
```

El programa deberá mostrar si el equipo responde.

Si:

```text
--detallado
```

está activado, deberá mostrar también la salida completa del comando.

---

## 43. Qué hemos conseguido

Al principio del capítulo utilizábamos:

```python
sys.argv[1]
sys.argv[2]
sys.argv[3]
```

Ahora podemos escribir:

```python
args.equipo
args.intentos
args.detallado
```

Hemos pasado de:

```text
POSICIONES
    │
    ▼
sys.argv[1]
sys.argv[2]
sys.argv[3]
```

a:

```text
NOMBRES
   │
   ▼
args.equipo
args.intentos
args.detallado
```

Además, `argparse` puede encargarse de:

```text
analizar argumentos
        │
        ├── comprobar obligatorios
        ├── convertir tipos
        ├── aplicar valores por defecto
        ├── gestionar opciones
        └── generar ayuda
```

Esto permite crear scripts más fáciles de utilizar y mantener.

---

## Resumen

En esta parte hemos aprendido a utilizar:

```python
argparse
```

Los pasos básicos son:

```python
import argparse
```

Crear el analizador:

```python
parser = argparse.ArgumentParser()
```

Definir argumentos:

```python
parser.add_argument(
    "archivo"
)
```

Procesarlos:

```python
args = parser.parse_args()
```

y acceder a ellos:

```python
args.archivo
```

También hemos utilizado:

```python
type=int
```

para convertir valores:

```python
parser.add_argument(
    "--intentos",
    type=int
)
```

valores predeterminados:

```python
default=1
```

formas cortas y largas:

```python
"-i",
"--intentos"
```

y banderas:

```python
action="store_true"
```

Además, hemos comprobado una de las principales ventajas de `argparse`:

```powershell
python programa.py --help
```

Con `sys.argv` hemos aprendido cómo recibe Python los argumentos.

Con `argparse` hemos aprendido a construir una verdadera interfaz de línea de comandos.

En la siguiente parte profundizaremos en el **control de errores y excepciones**:

```text
try
except
else
finally
```

Estudiaremos diferentes tipos de excepciones y aprenderemos a decidir cuáles debemos capturar para evitar que nuestros scripts terminen de forma inesperada.

---

## 44. Control avanzado de errores y excepciones

En capítulos anteriores ya hemos utilizado:

```python
try
```

y:

```python
except
```

para evitar que algunos errores provocaran la finalización inmediata de nuestros programas.

Ahora vamos a estudiar este mecanismo con más detalle.

Cuando desarrollamos scripts de administración debemos asumir que pueden aparecer problemas:

```text
archivo inexistente
ruta incorrecta
dato no válido
permiso denegado
comando inexistente
timeout
error durante una copia
```

Un buen script no debería simplemente mostrar un mensaje de error de Python y terminar.

Debería intentar:

```text
detectar
   │
   ▼
identificar
   │
   ▼
informar
   │
   ▼
actuar correctamente
```

---

## 45. ¿Qué es una excepción?

Una **excepción** es un problema que se produce durante la ejecución de un programa.

Por ejemplo:

```python
numero = int("hola")
```

Python no puede convertir:

```text
hola
```

en un número entero.

Se produce:

```text
ValueError
```

Otro ejemplo:

```python
archivo = open(
    "no_existe.txt"
)
```

puede provocar:

```text
FileNotFoundError
```

Las excepciones tienen nombres diferentes dependiendo del problema producido.

---

## 46. Provocar algunas excepciones

Antes de controlarlas vamos a observar algunas.

Dentro de:

```text
practicas/capitulo4/programas/
```

crea:

```text
probar_excepciones.py
```

Escribe:

```python
numero = int("hola")

print(
    "El programa continúa."
)
```

Ejecuta:

```powershell
python probar_excepciones.py
```

Obtendremos un mensaje que terminará indicando:

```text
ValueError
```

Observa que:

```python
print(
    "El programa continúa."
)
```

no se ejecuta.

Cuando se produce una excepción no controlada, el flujo normal del programa se interrumpe.

---

## 47. Utilizar `try` y `except`

Podemos controlar el problema:

```python
try:

    numero = int("hola")

except ValueError:

    print(
        "ERROR: no se puede "
        "convertir el valor."
    )
```

Ahora el programa no termina mostrando el error técnico completo de Python.

Nosotros decidimos cómo responder.

El funcionamiento es:

```text
       try
        │
        ▼
 ejecutar código
        │
    ┌───┴───┐
    │       │
 sin error  error
    │       │
    ▼       ▼
 continuar except
```

---

## 48. Ejemplo con entrada del usuario

Crea:

```text
convertir_numero.py
```

Escribe:

```python
try:

    texto = input(
        "Introduce un número: "
    )

    numero = int(texto)

    print(
        f"El doble es "
        f"{numero * 2}"
    )

except ValueError:

    print(
        "ERROR: debes introducir "
        "un número entero."
    )
```

Si introducimos:

```text
25
```

obtendremos:

```text
El doble es 50
```

Si introducimos:

```text
hola
```

obtendremos:

```text
ERROR: debes introducir un número entero.
```

El programa controla la situación.

---

## 49. Capturar excepciones concretas

Podríamos escribir:

```python
try:

    # código

except:

    print(
        "Se ha producido un error."
    )
```

Pero esta forma no suele ser la más adecuada.

No sabemos qué problema se ha producido.

Es preferible capturar una excepción concreta:

```python
except ValueError:
```

o:

```python
except FileNotFoundError:
```

o:

```python
except PermissionError:
```

Esto nos permite reaccionar de forma diferente según el problema.

!!! tip "Captura errores concretos"

    Siempre que conozcas qué excepción puede producir una operación, intenta capturar específicamente esa excepción.

    Esto hace que el programa sea más claro y evita ocultar otros problemas que podrían indicar un error en nuestro propio código.

---

## 50. Diferentes tipos de excepciones

Veamos algunas excepciones habituales.

### `ValueError`

Se produce cuando un valor tiene un formato incorrecto para una operación.

```python
numero = int("hola")
```

puede producir:

```text
ValueError
```

### `FileNotFoundError`

Puede aparecer cuando intentamos abrir un archivo inexistente:

```python
with open(
    "datos.txt",
    "r"
) as archivo:

    contenido = archivo.read()
```

### `PermissionError`

Puede aparecer cuando el programa no tiene permisos suficientes para acceder a un archivo o directorio.

### `IndexError`

Puede aparecer al intentar acceder a una posición inexistente:

```python
datos = [
    "uno",
    "dos"
]

print(
    datos[10]
)
```

### `KeyError`

Puede aparecer al solicitar una clave inexistente en un diccionario:

```python
equipo = {
    "nombre": "PC01",
    "ip": "192.168.1.20"
}

print(
    equipo["ubicacion"]
)
```

### `ZeroDivisionError`

Aparece al dividir entre cero:

```python
resultado = 10 / 0
```

No necesitamos memorizar todas las excepciones de Python.

Lo importante es aprender a identificar las que pueden producirse en nuestros programas.

---

## 51. Controlar varios tipos de error

Un mismo bloque puede tener diferentes `except`.

Crea:

```text
leer_archivo.py
```

Escribe:

```python
from pathlib import Path


ruta = input(
    "Introduce un archivo: "
)

archivo = Path(ruta)


try:

    contenido = archivo.read_text(
        encoding="utf-8"
    )

    print()
    print(contenido)

except FileNotFoundError:

    print(
        "ERROR: el archivo "
        "no existe."
    )

except PermissionError:

    print(
        "ERROR: no tienes permiso "
        "para leer el archivo."
    )
```

Ahora podemos reaccionar de forma distinta:

```text
archivo inexistente
       │
       ▼
FileNotFoundError


sin permisos
       │
       ▼
PermissionError
```

Esto es mucho mejor que mostrar:

```text
Se ha producido un error.
```

para cualquier problema.

---

## 52. Obtener información de la excepción

En ocasiones queremos mostrar información adicional sobre el problema.

Podemos escribir:

```python
except OSError as error:
```

La variable:

```python
error
```

contendrá información sobre la excepción.

Por ejemplo:

```python
try:

    contenido = archivo.read_text(
        encoding="utf-8"
    )

except OSError as error:

    print(
        "Se ha producido "
        "un error."
    )

    print(
        f"Detalle: {error}"
    )
```

Esto puede ser especialmente útil durante el desarrollo o para registrar posteriormente el problema en un archivo de log.

---

## 53. La cláusula `else`

Una estructura `try` puede incluir:

```python
else
```

El bloque `else` se ejecuta únicamente cuando el bloque `try` termina sin producir las excepciones que estamos controlando.

Por ejemplo:

```python
try:

    numero = int(
        input(
            "Introduce un número: "
        )
    )

except ValueError:

    print(
        "Valor incorrecto."
    )

else:

    print(
        f"Número correcto: "
        f"{numero}"
    )
```

Podemos representar el proceso:

```text
           try
            │
        ┌───┴───┐
        │       │
      error   correcto
        │       │
        ▼       ▼
     except    else
```

---

## 54. ¿Por qué utilizar `else`?

Podríamos escribir:

```python
try:

    numero = int(
        input(
            "Introduce un número: "
        )
    )

    print(
        f"Número correcto: "
        f"{numero}"
    )

except ValueError:

    print(
        "Valor incorrecto."
    )
```

Funciona.

Sin embargo, podemos limitar el bloque `try` únicamente al código que realmente puede producir la excepción que queremos controlar:

```python
try:

    numero = int(
        input(
            "Introduce un número: "
        )
    )

except ValueError:

    print(
        "Valor incorrecto."
    )

else:

    print(
        f"Número correcto: "
        f"{numero}"
    )
```

Esto permite separar mejor:

```text
operación que puede fallar
          │
          ▼
         try


respuesta al error
          │
          ▼
        except


operaciones posteriores
          │
          ▼
         else
```

---

## 55. La cláusula `finally`

Existe otro bloque:

```python
finally
```

El código incluido en `finally` se ejecuta tanto si se produce una excepción como si no.

Ejemplo:

```python
try:

    numero = int(
        input(
            "Introduce un número: "
        )
    )

except ValueError:

    print(
        "Valor incorrecto."
    )

else:

    print(
        f"Número correcto: "
        f"{numero}"
    )

finally:

    print(
        "Fin de la operación."
    )
```

Si introducimos:

```text
25
```

obtendremos:

```text
Número correcto: 25
Fin de la operación.
```

Si introducimos:

```text
hola
```

obtendremos:

```text
Valor incorrecto.
Fin de la operación.
```

`finally` se ejecuta en ambos casos.

---

## 56. Estructura completa

La estructura completa puede ser:

```python
try:

    # operación que puede fallar

except ValueError:

    # tratamiento del error

else:

    # se ejecuta si no se produce
    # la excepción controlada

finally:

    # se ejecuta siempre
```

Visualmente:

```text
                TRY
                 │
          ┌──────┴──────┐
          │             │
        ERROR        SIN ERROR
          │             │
          ▼             ▼
       EXCEPT           ELSE
          │             │
          └──────┬──────┘
                 │
                 ▼
              FINALLY
                 │
                 ▼
             CONTINUAR
```

No es obligatorio utilizar siempre las cuatro partes.

Podemos tener:

```python
try:
    ...
except ValueError:
    ...
```

o:

```python
try:
    ...
except ValueError:
    ...
finally:
    ...
```

o:

```python
try:
    ...
except ValueError:
    ...
else:
    ...
finally:
    ...
```

Utilizaremos únicamente las partes que necesitemos.

---

## 57. `finally` y los archivos

Cuando trabajamos con:

```python
with open(...)
```

Python ya gestiona automáticamente el cierre del archivo al salir del bloque.

Por ejemplo:

```python
with open(
    "datos.txt",
    "r",
    encoding="utf-8"
) as archivo:

    contenido = archivo.read()
```

No necesitamos utilizar `finally` simplemente para cerrar ese archivo.

!!! note "`with` sigue siendo la opción recomendada"

    Para abrir archivos continuaremos utilizando:

    ```python
    with open(...)
    ```

    `finally` resulta útil para comprender y controlar tareas de limpieza en situaciones donde necesitamos garantizar que una operación final se ejecute.

---

## 58. Excepciones con `subprocess`

Los scripts de administración ejecutan frecuentemente comandos externos.

Ya hemos utilizado:

```python
subprocess.run()
```

Veamos algunos problemas que pueden aparecer.

### Comando inexistente

```python
import subprocess


try:

    subprocess.run(
        [
            "comando_que_no_existe"
        ],
        check=True
    )

except FileNotFoundError:

    print(
        "ERROR: no se encuentra "
        "el comando."
    )
```

### Tiempo de espera agotado

También podemos establecer:

```python
timeout=5
```

y controlar:

```python
subprocess.TimeoutExpired
```

Ejemplo:

```python
try:

    resultado = subprocess.run(
        [
            "ping",
            "-n",
            "1",
            "192.168.1.1"
        ],
        capture_output=True,
        text=True,
        timeout=5
    )

except subprocess.TimeoutExpired:

    print(
        "ERROR: se ha superado "
        "el tiempo de espera."
    )
```

---

## 59. `check=True` y `CalledProcessError`

Recordemos:

```python
check=True
```

Cuando el comando termina con un código distinto de cero, `subprocess.run()` puede lanzar:

```python
subprocess.CalledProcessError
```

Por ejemplo:

```python
try:

    resultado = subprocess.run(
        [
            "ping",
            "-n",
            "1",
            "equipo-inexistente"
        ],
        capture_output=True,
        text=True,
        timeout=5,
        check=True
    )

except subprocess.CalledProcessError:

    print(
        "El comando terminó "
        "con un error."
    )

except subprocess.TimeoutExpired:

    print(
        "Tiempo de espera agotado."
    )

except FileNotFoundError:

    print(
        "No se encuentra "
        "el comando ping."
    )
```

Tenemos tres situaciones distintas:

```text
comando no existe
      │
      ▼
FileNotFoundError


comando tarda demasiado
      │
      ▼
TimeoutExpired


comando devuelve error
      │
      ▼
CalledProcessError
```

---

## 60. No confundir un resultado negativo con un error del programa

Este punto es especialmente importante.

Imaginemos que hacemos:

```text
ping
```

a un equipo y este no responde.

Esto no significa necesariamente que nuestro programa Python esté mal.

Puede significar simplemente:

```text
el equipo está apagado
la dirección es incorrecta
no existe conectividad
un firewall bloquea la respuesta
```

Debemos distinguir entre:

```text
ERROR DEL PROGRAMA
```

y:

```text
RESULTADO DE LA OPERACIÓN
```

Por ejemplo:

```text
ping devuelve código distinto de 0
        │
        ▼
resultado de la comprobación


Python no encuentra "ping"
        │
        ▼
problema al ejecutar la operación
```

Esta diferencia será muy importante al diseñar herramientas de administración.

---

## 61. Crear una función segura para ejecutar comandos

Vamos a crear una función reutilizable.

Crea:

```text
ejecutar_seguro.py
```

Escribe:

```python
import subprocess


def ejecutar_comando(comando):

    try:

        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=10
        )

    except FileNotFoundError:

        print(
            "ERROR: comando "
            "no encontrado."
        )

        return None

    except subprocess.TimeoutExpired:

        print(
            "ERROR: tiempo "
            "de espera agotado."
        )

        return None

    except OSError as error:

        print(
            f"ERROR del sistema: "
            f"{error}"
        )

        return None

    else:

        return resultado
```

Podemos utilizarla:

```python
resultado = ejecutar_comando(
    [
        "hostname"
    ]
)


if resultado is not None:

    print(
        resultado.stdout
    )
```

Ahora hemos encapsulado el control de errores en una función.

---

## 62. Ventajas de encapsular el control de errores

Imaginemos un programa que ejecuta:

```text
hostname
ipconfig
ping
systeminfo
```

Podríamos repetir en cada operación:

```python
try:
    ...
except:
    ...
```

Pero resulta más adecuado crear una función reutilizable:

```text
              programa
                  │
        ┌─────────┼─────────┐
        │         │         │
    hostname   ipconfig    ping
        │         │         │
        └─────────┼─────────┘
                  │
                  ▼
         ejecutar_comando()
                  │
                  ▼
          control de errores
```

Esto reduce código repetido y facilita el mantenimiento.

---

## 63. Excepciones y `argparse`

Podemos combinar lo aprendido en esta parte con `argparse`.

Crea:

```text
leer_archivo_argparse.py
```

Escribe:

```python
import argparse

from pathlib import Path


parser = argparse.ArgumentParser(
    description=(
        "Muestra el contenido "
        "de un archivo de texto."
    )
)

parser.add_argument(
    "archivo",
    help="Archivo que se leerá"
)

args = parser.parse_args()


ruta = Path(
    args.archivo
)


try:

    contenido = ruta.read_text(
        encoding="utf-8"
    )

except FileNotFoundError:

    print(
        "ERROR: el archivo "
        "no existe."
    )

except PermissionError:

    print(
        "ERROR: no tienes "
        "permiso de lectura."
    )

except OSError as error:

    print(
        f"ERROR del sistema: "
        f"{error}"
    )

else:

    print()
    print(contenido)

finally:

    print()
    print(
        "Operación finalizada."
    )
```

Prueba:

```powershell
python leer_archivo_argparse.py datos.txt
```

Después prueba con un archivo inexistente:

```powershell
python leer_archivo_argparse.py no_existe.txt
```

El programa debe responder de forma controlada en ambos casos.

---

## 64. Validación y excepciones no son exactamente lo mismo

Supongamos que recibimos:

```python
inicio = 200
fin = 100
```

Python puede trabajar perfectamente con ambos números.

No se produce automáticamente una excepción.

Sin embargo, para nuestro programa puede ser un dato incorrecto porque:

```text
inicio > fin
```

Esto es un problema de **validación**.

Por ejemplo:

```python
if inicio > fin:

    print(
        "ERROR: el valor inicial "
        "no puede ser mayor "
        "que el final."
    )
```

Por tanto debemos diferenciar:

```text
VALIDACIÓN

¿Los datos cumplen las reglas
de nuestra aplicación?


EXCEPCIÓN

¿Se ha producido un problema
durante una operación?
```

Un programa robusto necesita ambas cosas.

---

## 65. Validar argumentos con `argparse`

Recuperemos el ejemplo:

```text
comprobar_rango_argparse.py
```

Podemos añadir:

```python
if args.inicio < 1:

    parser.error(
        "El host inicial debe "
        "ser mayor o igual que 1."
    )
```

También:

```python
if args.fin > 254:

    parser.error(
        "El host final debe "
        "ser menor o igual que 254."
    )
```

Y:

```python
if args.inicio > args.fin:

    parser.error(
        "El host inicial no puede "
        "ser mayor que el final."
    )
```

Ahora nuestro programa comprueba tanto el tipo:

```python
type=int
```

como las reglas propias de nuestra aplicación.

---

## 66. Práctica guiada: copiador seguro

Vamos a combinar:

```text
argparse
+
pathlib
+
shutil
+
excepciones
```

Crea:

```text
copiador_seguro.py
```

Escribe:

```python
import argparse
import shutil

from pathlib import Path


parser = argparse.ArgumentParser(
    description=(
        "Copia un archivo "
        "de forma controlada."
    )
)

parser.add_argument(
    "origen",
    help="Archivo de origen"
)

parser.add_argument(
    "destino",
    help="Archivo de destino"
)

args = parser.parse_args()


origen = Path(
    args.origen
)

destino = Path(
    args.destino
)


if not origen.exists():

    parser.error(
        "El archivo de origen "
        "no existe."
    )


if not origen.is_file():

    parser.error(
        "El origen debe ser "
        "un archivo."
    )


try:

    shutil.copy2(
        origen,
        destino
    )

except PermissionError:

    print(
        "ERROR: permiso denegado."
    )

except OSError as error:

    print(
        f"ERROR durante la copia: "
        f"{error}"
    )

else:

    print()
    print(
        "Archivo copiado "
        "correctamente."
    )

    print(
        f"Origen: {origen}"
    )

    print(
        f"Destino: {destino}"
    )

finally:

    print()
    print(
        "Proceso de copia "
        "finalizado."
    )
```

Podemos probar:

```powershell
python copiador_seguro.py datos.txt copia.txt
```

También podemos provocar diferentes situaciones para comprobar el comportamiento del programa.

---

## 67. Práctica propuesta: backup seguro

Crea:

```text
backup_seguro_argparse.py
```

El programa deberá ejecutarse mediante:

```powershell
python backup_seguro_argparse.py "C:\Datos"
```

También deberá aceptar:

```powershell
python backup_seguro_argparse.py "C:\Datos" --destino "C:\Backups"
```

El programa deberá utilizar:

```text
argparse
pathlib
datetime
shutil
try
except
else
finally
```

Deberá controlar al menos:

```text
origen inexistente
origen que no es un directorio
problemas de permisos
errores durante la copia
```

Si la copia termina correctamente deberá mostrar:

```text
COPIA REALIZADA CORRECTAMENTE

Origen:
C:\Datos

Destino:
C:\Backups\backup_2026-09-21_11-30-00
```

!!! warning "Datos de prueba"

    Realiza esta práctica inicialmente con un directorio creado expresamente para las pruebas.

    No utilices como primera prueba carpetas con información importante.

---

## 68. Práctica propuesta: diagnóstico robusto

Crea:

```text
diagnostico_seguro.py
```

El programa deberá aceptar:

```powershell
python diagnostico_seguro.py 192.168.1.1
```

y:

```powershell
python diagnostico_seguro.py 192.168.1.1 --intentos 4
```

Deberá combinar:

```text
argparse
+
subprocess
+
validación
+
excepciones
```

Controlará:

- Argumentos incorrectos.
- Número de intentos menor que 1.
- Comando `ping` no disponible.
- Tiempo de espera agotado.
- Resultado positivo o negativo del `ping`.

!!! example "Objetivo"

    El programa no debe mostrar al usuario una traza de error de Python ante las situaciones previstas.

    Debe responder mediante mensajes comprensibles.

---

## 69. ¿Debemos capturar todos los errores?

No.

Un error frecuente consiste en escribir:

```python
try:

    # muchas instrucciones

except Exception:

    print(
        "Ha ocurrido un error."
    )
```

Esto puede ocultar problemas importantes.

Por ejemplo, podemos tener un error en nuestro propio código y convertirlo simplemente en:

```text
Ha ocurrido un error.
```

Entonces resulta mucho más difícil encontrar el problema.

Es preferible:

```python
except FileNotFoundError:
```

```python
except PermissionError:
```

```python
except ValueError:
```

cuando sabemos que esas son las situaciones que queremos controlar.

!!! warning "No ocultes los errores"

    El objetivo del control de excepciones no es conseguir que desaparezcan todos los mensajes de error.

    El objetivo es controlar aquellas situaciones que nuestro programa sabe gestionar correctamente.

---

## 70. Dónde colocar el `try`

También debemos evitar bloques `try` innecesariamente grandes.

En lugar de:

```python
try:

    # leer argumentos
    # crear rutas
    # hacer cálculos
    # leer archivo
    # ejecutar comandos
    # generar informe
    # guardar resultados

except Exception:

    print(
        "Error."
    )
```

es preferible proteger únicamente la operación que puede producir el problema:

```python
try:

    contenido = archivo.read_text(
        encoding="utf-8"
    )

except FileNotFoundError:

    print(
        "Archivo inexistente."
    )
```

Esto permite identificar mucho mejor dónde puede producirse el error.

---

## 71. Diseñar scripts robustos

A estas alturas podemos establecer un patrón para nuestros programas:

```text
ARGUMENTOS
    │
    ▼
argparse
    │
    ▼
VALIDACIÓN
    │
    ▼
OPERACIÓN
    │
    ▼
try
    │
 ┌──┴─────┐
 │        │
ERROR   CORRECTO
 │        │
 ▼        ▼
except   else
 │        │
 └───┬────┘
     │
     ▼
  finally
```

Este patrón puede aplicarse a:

```text
copias de seguridad
procesamiento de archivos
comandos del sistema
diagnóstico de red
generación de informes
```

---

## Resumen

En esta parte hemos profundizado en el control de excepciones.

La estructura básica es:

```python
try:

    # operación

except ValueError:

    # controlar error
```

También hemos aprendido:

```python
else
```

que permite ejecutar código cuando la operación termina correctamente, y:

```python
finally
```

que permite ejecutar código al finalizar el proceso independientemente del resultado.

Hemos visto algunas excepciones frecuentes:

```text
ValueError
FileNotFoundError
PermissionError
IndexError
KeyError
ZeroDivisionError
OSError
```

y excepciones relacionadas con `subprocess`:

```text
FileNotFoundError
subprocess.TimeoutExpired
subprocess.CalledProcessError
```

También hemos diferenciado dos conceptos fundamentales:

```text
VALIDACIÓN
    │
    └── comprobar si los datos
        cumplen nuestras reglas


EXCEPCIONES
    │
    └── controlar problemas
        durante una operación
```

Un script robusto combina ambos mecanismos.

Finalmente hemos establecido un patrón:

```text
recibir datos
     │
     ▼
validarlos
     │
     ▼
realizar operación
     │
     ▼
controlar excepciones
     │
     ▼
informar del resultado
```

En la siguiente parte incorporaremos el tercer elemento fundamental de esta unidad:

```python
logging
```

Aprenderemos a crear **logs de ejecución**, utilizar niveles como `DEBUG`, `INFO`, `WARNING`, `ERROR` y `CRITICAL`, guardar los registros en archivos y utilizarlos para auditar nuestros scripts de administración.

---

## 72. Registro de actividad con `logging`

En el capítulo anterior creamos manualmente archivos de historial.

Por ejemplo:

```python
with open(
    "historial.txt",
    "a",
    encoding="utf-8"
) as archivo:

    archivo.write(
        "Backup realizado\n"
    )
```

Este sistema funciona, pero Python dispone de una herramienta específicamente diseñada para registrar la actividad de los programas:

```python
logging
```

El módulo `logging` permite guardar automáticamente información como:

```text
fecha y hora
nivel del mensaje
operación realizada
errores producidos
avisos
información de diagnóstico
```

Un archivo de registro podría contener:

```text
2026-09-21 11:45:10 - INFO - Programa iniciado
2026-09-21 11:45:12 - INFO - Inventario cargado
2026-09-21 11:45:15 - WARNING - Equipo 192.168.1.20 no responde
2026-09-21 11:45:18 - ERROR - No se encuentra datos.csv
2026-09-21 11:45:20 - INFO - Programa finalizado
```

Este tipo de archivo se denomina habitualmente **log**.

---

## 73. ¿Para qué sirve un log?

Cuando ejecutamos un programa desde el terminal podemos utilizar:

```python
print()
```

para mostrar información.

Por ejemplo:

```python
print(
    "Backup realizado."
)
```

Pero cuando cerramos el terminal esa información deja de estar disponible.

Un log permite conservar un registro de lo ocurrido.

```text
PROGRAMA
   │
   ├──────► pantalla
   │          print()
   │
   └──────► archivo
              logging
```

Esto resulta especialmente útil en scripts que:

- Se ejecutan automáticamente.
- Funcionan durante mucho tiempo.
- Realizan muchas operaciones.
- Se ejecutan sin supervisión.
- Necesitan dejar constancia de los errores.
- Administran sistemas o redes.

---

## 74. Nuestro primer programa con `logging`

Dentro de:

```text
practicas/capitulo4/programas/
```

crea:

```text
primer_logging.py
```

Escribe:

```python
import logging


logging.basicConfig(
    level=logging.INFO
)


logging.info(
    "Programa iniciado"
)

logging.info(
    "Realizando operación"
)

logging.info(
    "Programa finalizado"
)
```

Ejecuta:

```powershell
python primer_logging.py
```

Obtendremos mensajes similares a:

```text
INFO:root:Programa iniciado
INFO:root:Realizando operación
INFO:root:Programa finalizado
```

Hemos creado nuestros primeros mensajes de log.

---

## 75. Los niveles de `logging`

No todos los mensajes tienen la misma importancia.

`logging` utiliza diferentes niveles.

Los principales son:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

Podemos ordenarlos de menor a mayor gravedad:

```text
DEBUG
  │
  ▼
INFO
  │
  ▼
WARNING
  │
  ▼
ERROR
  │
  ▼
CRITICAL
```

Cada nivel tiene una finalidad diferente.

---

### `DEBUG`

Se utiliza para información detallada útil durante el desarrollo y la depuración.

```python
logging.debug(
    "Valor de la variable ip: "
    "192.168.1.1"
)
```

---

### `INFO`

Indica que una operación normal se ha realizado.

```python
logging.info(
    "Inventario cargado correctamente"
)
```

---

### `WARNING`

Indica una situación que merece atención, pero que no impide necesariamente continuar.

```python
logging.warning(
    "El equipo no responde"
)
```

---

### `ERROR`

Indica que una operación no ha podido realizarse correctamente.

```python
logging.error(
    "No se ha podido abrir "
    "el archivo"
)
```

---

### `CRITICAL`

Indica un problema especialmente grave.

```python
logging.critical(
    "No se puede continuar "
    "la ejecución"
)
```

---

## 76. Probar los niveles de log

Crea:

```text
niveles_logging.py
```

Escribe:

```python
import logging


logging.basicConfig(
    level=logging.DEBUG
)


logging.debug(
    "Mensaje DEBUG"
)

logging.info(
    "Mensaje INFO"
)

logging.warning(
    "Mensaje WARNING"
)

logging.error(
    "Mensaje ERROR"
)

logging.critical(
    "Mensaje CRITICAL"
)
```

Ejecuta:

```powershell
python niveles_logging.py
```

Deberán aparecer los cinco niveles.

---

## 77. Filtrar mensajes por nivel

Modifica:

```python
level=logging.DEBUG
```

por:

```python
level=logging.WARNING
```

Vuelve a ejecutar el programa.

Ahora únicamente aparecerán:

```text
WARNING
ERROR
CRITICAL
```

No aparecerán:

```text
DEBUG
INFO
```

Esto ocurre porque hemos establecido el nivel mínimo en:

```python
logging.WARNING
```

Podemos imaginarlo como un filtro:

```text
DEBUG       ✗
INFO        ✗
WARNING     ✓
ERROR       ✓
CRITICAL    ✓
```

Si utilizamos:

```python
level=logging.INFO
```

obtendremos:

```text
DEBUG       ✗
INFO        ✓
WARNING     ✓
ERROR       ✓
CRITICAL    ✓
```

!!! tip "Nivel durante el desarrollo"

    Durante el desarrollo puede ser útil utilizar:

    ```python
    logging.DEBUG
    ```

    para obtener información detallada.

    Para una ejecución normal podemos utilizar:

    ```python
    logging.INFO
    ```

---

## 78. Guardar el log en un archivo

Hasta ahora los mensajes aparecen en el terminal.

Podemos enviarlos a un archivo.

Crea:

```text
logging_archivo.py
```

Escribe:

```python
import logging


logging.basicConfig(
    filename="programa.log",
    level=logging.INFO
)


logging.info(
    "Programa iniciado"
)

logging.info(
    "Operación realizada"
)

logging.warning(
    "Mensaje de prueba"
)

logging.info(
    "Programa finalizado"
)
```

Ejecuta:

```powershell
python logging_archivo.py
```

Ahora aparecerá:

```text
programa.log
```

Abre el archivo desde VS Code.

Encontraremos algo similar a:

```text
INFO:root:Programa iniciado
INFO:root:Operación realizada
WARNING:root:Mensaje de prueba
INFO:root:Programa finalizado
```

---

## 79. Añadir fecha y hora

En un registro resulta fundamental saber **cuándo** ocurrió cada operación.

Podemos configurar el formato:

```python
logging.basicConfig(
    filename="programa.log",
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    )
)
```

Ahora los registros tendrán un aspecto parecido a:

```text
2026-09-21 11:45:10,251 - INFO - Programa iniciado
2026-09-21 11:45:12,315 - INFO - Operación realizada
2026-09-21 11:45:14,822 - WARNING - Mensaje de prueba
```

Las partes principales son:

```text
%(asctime)s
```

fecha y hora.

```text
%(levelname)s
```

nivel del mensaje.

```text
%(message)s
```

mensaje que hemos registrado.

---

## 80. Personalizar el formato de la fecha

También podemos utilizar:

```python
datefmt="%Y-%m-%d %H:%M:%S"
```

Por ejemplo:

```python
logging.basicConfig(
    filename="programa.log",
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

Ahora tendremos:

```text
2026-09-21 11:45:10 - INFO - Programa iniciado
```

Este formato resulta más sencillo de leer.

---

## 81. Crear un directorio para los logs

Vamos a organizar correctamente nuestro proyecto.

Añadiremos:

```text
logs/
```

La estructura será:

```text
practicas/
└── capitulo4/
    ├── datos/
    ├── logs/
    ├── programas/
    └── resultados/
```

Podemos crear la ruta mediante `pathlib`.

```python
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
    / "programa.log"
)
```

Después configuramos:

```python
logging.basicConfig(
    filename=ARCHIVO_LOG,
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

De esta forma los registros quedan separados del código.

---

## 82. Crear nuestro primer script con auditoría

Crea:

```text
script_auditado.py
```

Escribe:

```python
import logging

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
    / "script.log"
)


logging.basicConfig(
    filename=ARCHIVO_LOG,
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


logging.info(
    "Programa iniciado"
)


print(
    "Realizando operación..."
)


logging.info(
    "Operación realizada"
)


logging.info(
    "Programa finalizado"
)
```

Ejecuta varias veces:

```powershell
python script_auditado.py
```

Después abre:

```text
logs/script.log
```

Verás cómo se van acumulando los registros de las diferentes ejecuciones.

---

## 83. Registrar variables

Los logs pueden incluir información procedente de variables.

Por ejemplo:

```python
ip = "192.168.1.1"

logging.info(
    f"Comprobando equipo {ip}"
)
```

Podemos registrar:

```text
2026-09-21 11:50:20 - INFO - Comprobando equipo 192.168.1.1
```

Esto resulta muy útil para saber exactamente qué estaba haciendo el programa.

---

## 84. Combinar `logging` y excepciones

Una de las aplicaciones más importantes de `logging` es registrar errores.

Crea:

```text
leer_archivo_logging.py
```

Escribe:

```python
import logging

from pathlib import Path


logging.basicConfig(
    filename="errores.log",
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


ruta = Path(
    "datos.txt"
)


logging.info(
    f"Intentando leer {ruta}"
)


try:

    contenido = ruta.read_text(
        encoding="utf-8"
    )

except FileNotFoundError:

    print(
        "ERROR: archivo inexistente."
    )

    logging.error(
        f"No existe el archivo {ruta}"
    )

except PermissionError:

    print(
        "ERROR: permiso denegado."
    )

    logging.error(
        f"Sin permiso para leer {ruta}"
    )

else:

    print(contenido)

    logging.info(
        f"Archivo {ruta} "
        f"leído correctamente"
    )

finally:

    logging.info(
        "Operación de lectura finalizada"
    )
```

Ahora tenemos dos tipos de información:

```text
USUARIO
   │
   ▼
mensajes por pantalla


ADMINISTRADOR
   │
   ▼
archivo de log
```

No tienen por qué contener exactamente la misma información.

---

## 85. Registrar información de una excepción

Podemos guardar el contenido de una excepción.

Por ejemplo:

```python
try:

    contenido = ruta.read_text(
        encoding="utf-8"
    )

except OSError as error:

    print(
        "No se ha podido "
        "leer el archivo."
    )

    logging.error(
        f"Error leyendo {ruta}: "
        f"{error}"
    )
```

El usuario puede recibir un mensaje sencillo:

```text
No se ha podido leer el archivo.
```

mientras que el log puede contener información más detallada.

Esto resulta útil para diagnosticar posteriormente el problema.

---

## 86. Registrar la traza de una excepción

`logging` dispone también de:

```python
logging.exception()
```

Esta función se utiliza dentro de un bloque `except`.

Por ejemplo:

```python
try:

    numero = int("hola")

except ValueError:

    logging.exception(
        "Error convirtiendo "
        "el valor a entero"
    )
```

Además del mensaje, el log incluirá información sobre la excepción.

!!! note "`logging.exception()`"

    Utilizaremos `logging.exception()` cuando nos interese conservar información técnica sobre una excepción.

    Normalmente se utiliza dentro de:

    ```python
    except
    ```

---

## 87. `print()` y `logging` no son lo mismo

No debemos pensar que:

```python
logging
```

simplemente sustituye a:

```python
print()
```

Tienen objetivos diferentes.

Podemos utilizar:

```python
print(
    "Backup completado."
)
```

para informar al usuario.

Y:

```python
logging.info(
    "Backup completado en "
    "C:\\Backups\\backup_..."
)
```

para registrar información de la ejecución.

Podemos representarlo así:

```text
             PROGRAMA
                │
        ┌───────┴────────┐
        │                │
        ▼                ▼
     print()          logging
        │                │
        ▼                ▼
     usuario          registro
```

---

## 88. Sustituir nuestro historial manual

En el capítulo anterior creamos una función parecida a:

```python
def registrar(mensaje):

    fecha = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        "historial.txt",
        "a",
        encoding="utf-8"
    ) as archivo:

        archivo.write(
            f"{fecha} - {mensaje}\n"
        )
```

Ahora podemos configurar:

```python
logging.basicConfig(
    filename="programa.log",
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    )
)
```

y simplemente escribir:

```python
logging.info(
    "Backup realizado"
)
```

Además podemos distinguir:

```python
logging.debug(...)
logging.info(...)
logging.warning(...)
logging.error(...)
logging.critical(...)
```

Por tanto, `logging` nos proporciona un sistema de registro mucho más completo.

---

## 89. Añadir logs a un comprobador de red

Vamos a recuperar una tarea conocida.

Crea:

```text
ping_logging.py
```

Escribe:

```python
import argparse
import logging
import subprocess

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
    / "red.log"
)


logging.basicConfig(
    filename=ARCHIVO_LOG,
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


parser = argparse.ArgumentParser(
    description=(
        "Comprueba la conectividad "
        "con un equipo."
    )
)

parser.add_argument(
    "equipo",
    help=(
        "Dirección IP o nombre "
        "del equipo"
    )
)

parser.add_argument(
    "-i",
    "--intentos",
    type=int,
    default=1,
    help="Número de intentos"
)

args = parser.parse_args()


if args.intentos < 1:

    parser.error(
        "El número de intentos "
        "debe ser mayor que cero."
    )


logging.info(
    f"Comprobando {args.equipo}"
)


try:

    resultado = subprocess.run(
        [
            "ping",
            "-n",
            str(args.intentos),
            args.equipo
        ],
        capture_output=True,
        text=True,
        timeout=10
    )

except FileNotFoundError:

    print(
        "ERROR: no se encuentra "
        "el comando ping."
    )

    logging.critical(
        "Comando ping no disponible"
    )

except subprocess.TimeoutExpired:

    print(
        "ERROR: tiempo de espera "
        "agotado."
    )

    logging.error(
        f"Timeout comprobando "
        f"{args.equipo}"
    )

except OSError as error:

    print(
        "ERROR al ejecutar ping."
    )

    logging.exception(
        f"Error comprobando "
        f"{args.equipo}: {error}"
    )

else:

    if resultado.returncode == 0:

        print(
            f"{args.equipo}: RESPONDE"
        )

        logging.info(
            f"{args.equipo}: RESPONDE"
        )

    else:

        print(
            f"{args.equipo}: "
            f"NO RESPONDE"
        )

        logging.warning(
            f"{args.equipo}: "
            f"NO RESPONDE"
        )

finally:

    logging.info(
        "Comprobación finalizada"
    )
```

Ejecuta:

```powershell
python ping_logging.py 127.0.0.1
```

Después:

```powershell
python ping_logging.py 192.168.1.250
```

Finalmente abre:

```text
logs/red.log
```

Podremos encontrar registros similares a:

```text
2026-09-21 12:05:10 - INFO - Comprobando 127.0.0.1
2026-09-21 12:05:10 - INFO - 127.0.0.1: RESPONDE
2026-09-21 12:05:10 - INFO - Comprobación finalizada
2026-09-21 12:06:15 - INFO - Comprobando 192.168.1.250
2026-09-21 12:06:18 - WARNING - 192.168.1.250: NO RESPONDE
2026-09-21 12:06:18 - INFO - Comprobación finalizada
```

Ahora nuestro programa no solo realiza una operación.

También deja constancia de ella.

---

## 90. ¿Qué nivel debemos utilizar?

Podemos utilizar esta regla sencilla:

```text
DEBUG
│
└── información técnica para
    entender el funcionamiento


INFO
│
└── operación normal realizada


WARNING
│
└── situación inesperada,
    pero el programa puede continuar


ERROR
│
└── una operación ha fallado


CRITICAL
│
└── problema grave que puede
    impedir continuar
```

Por ejemplo:

```python
logging.debug(
    f"Argumentos recibidos: {args}"
)
```

```python
logging.info(
    "Backup completado"
)
```

```python
logging.warning(
    "Equipo sin respuesta"
)
```

```python
logging.error(
    "No se pudo copiar el archivo"
)
```

```python
logging.critical(
    "Directorio principal "
    "no disponible"
)
```

---

## 91. Evitar registrar información innecesaria

Un log no debería convertirse en un archivo lleno de información inútil.

Por ejemplo, registrar continuamente:

```text
Entrando en línea 1
Entrando en línea 2
Entrando en línea 3
```

normalmente no resulta útil.

Debemos registrar información que ayude a responder preguntas como:

```text
¿Cuándo se ejecutó el programa?
¿Qué operación realizó?
¿Sobre qué archivo o equipo?
¿Terminó correctamente?
¿Qué error ocurrió?
```

!!! warning "Información sensible"

    Evita escribir en los logs información sensible como:

    - Contraseñas.
    - Tokens.
    - Claves de API.
    - Credenciales.
    - Información privada innecesaria.

    Los archivos de log también deben protegerse adecuadamente.

---

## 92. Práctica guiada: backup con log

Vamos a mejorar nuestro sistema de copias de seguridad.

Crea:

```text
backup_logging.py
```

El programa deberá poder ejecutarse mediante:

```powershell
python backup_logging.py "C:\Datos"
```

y opcionalmente:

```powershell
python backup_logging.py "C:\Datos" --destino "C:\Backups"
```

Deberá utilizar:

```text
argparse
pathlib
datetime
shutil
logging
try / except
```

El log deberá registrar:

```text
inicio del programa
origen seleccionado
destino seleccionado
inicio de la copia
copia realizada correctamente
errores producidos
fin de la operación
```

Por ejemplo:

```text
2026-09-21 12:20:01 - INFO - Programa iniciado
2026-09-21 12:20:01 - INFO - Origen: C:\Datos
2026-09-21 12:20:01 - INFO - Iniciando backup
2026-09-21 12:20:04 - INFO - Backup completado
2026-09-21 12:20:04 - INFO - Programa finalizado
```

El archivo deberá almacenarse en:

```text
practicas/capitulo4/logs/backup.log
```

---

## 93. Práctica propuesta: auditar el inventario

Crea:

```text
inventario_logging.py
```

Utiliza como entrada:

```text
datos/inventario.csv
```

El programa deberá:

1. Recibir el archivo mediante `argparse`.
2. Comprobar que existe.
3. Leerlo mediante `csv.DictReader`.
4. Comprobar cada equipo mediante `ping`.
5. Mostrar los resultados por pantalla.
6. Registrar las operaciones mediante `logging`.
7. Controlar las excepciones previstas.

El log podría contener:

```text
INFO - Inventario cargado
INFO - Comprobando PC01 - 192.168.1.20
INFO - PC01 responde
INFO - Comprobando PC02 - 192.168.1.21
WARNING - PC02 no responde
INFO - Comprobación finalizada
```

!!! example "Objetivo"

    El usuario debe recibir información clara por pantalla.

    El administrador debe poder consultar posteriormente el archivo de log para conocer qué ocurrió durante la ejecución.

---

## 94. Práctica de análisis de logs

Los logs también pueden convertirse en datos que nuestros programas pueden analizar.

Supongamos que tenemos:

```text
red.log
```

Crea:

```text
analizar_log.py
```

El programa deberá leer el archivo y contar cuántas líneas contienen:

```text
INFO
WARNING
ERROR
CRITICAL
```

El resultado podría ser:

```text
RESUMEN DEL LOG
===============

INFO: 25
WARNING: 4
ERROR: 2
CRITICAL: 0
```

Para esta primera versión puedes utilizar simplemente:

```python
if "INFO" in linea:
```

```python
if "WARNING" in linea:
```

y contadores.

Esta práctica combina el contenido actual con la lectura de archivos estudiada en el capítulo 1.

---

## 95. Integración de lo aprendido

En este capítulo hemos incorporado tres herramientas fundamentales.

Primero:

```text
ARGUMENTOS
    │
    ▼
sys.argv
    │
    ▼
argparse
```

Después:

```text
CONTROL DE ERRORES
        │
        ▼
       try
        │
   ┌────┴────┐
   │         │
except      else
   │         │
   └────┬────┘
        │
        ▼
     finally
```

Y ahora:

```text
REGISTRO
   │
   ▼
logging
   │
   ├── DEBUG
   ├── INFO
   ├── WARNING
   ├── ERROR
   └── CRITICAL
```

Las tres técnicas pueden trabajar conjuntamente:

```text
      USUARIO
         │
         ▼
      argparse
         │
         ▼
     validación
         │
         ▼
       try
         │
    ┌────┴────┐
    │         │
 correcto    error
    │         │
    ▼         ▼
   INFO     ERROR
    │         │
    └────┬────┘
         │
         ▼
       LOG
```

---

## 96. De script sencillo a script de administración

Podemos observar cómo han evolucionado nuestros programas.

Al principio escribíamos:

```python
ip = "192.168.1.1"
```

Después:

```python
ip = sys.argv[1]
```

Más tarde:

```python
args = parser.parse_args()

ip = args.ip
```

Añadimos:

```python
try:
    ...
except:
    ...
```

Y finalmente:

```python
logging.info(...)
logging.warning(...)
logging.error(...)
```

Nuestro script ya puede:

```text
recibir parámetros
      │
      ▼
validarlos
      │
      ▼
ejecutar operaciones
      │
      ▼
controlar problemas
      │
      ▼
informar al usuario
      │
      ▼
registrar lo ocurrido
```

Este es un salto importante respecto a nuestros primeros programas.

---

## Resumen

El módulo:

```python
logging
```

permite registrar información sobre la ejecución de nuestros programas.

Los principales niveles son:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

Podemos configurar un archivo de registro mediante:

```python
logging.basicConfig(
    filename="programa.log",
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

Después podemos registrar eventos mediante:

```python
logging.info(
    "Operación correcta"
)
```

```python
logging.warning(
    "Situación que requiere atención"
)
```

```python
logging.error(
    "La operación ha fallado"
)
```

También podemos combinar:

```python
try
```

con:

```python
logging.exception()
```

para conservar información sobre las excepciones.

Con ello ya disponemos de los tres grandes elementos estudiados en este capítulo:

```text
ARGUMENTOS
     +
CONTROL DE ERRORES
     +
LOGS
     =
SCRIPT ROBUSTO
```

En la siguiente parte construiremos la **práctica final del capítulo 4**, integrando `argparse`, validación, `try/except/finally`, `subprocess`, `pathlib` y `logging` en una única herramienta de administración.

---

## 97. Práctica final: herramienta de administración robusta

En este capítulo hemos aprendido a transformar pequeños programas Python en scripts más adecuados para tareas reales de administración.

Ahora vamos a reunir los principales conceptos en una única aplicación.

Desarrollaremos:

```text
administrador.py
```

La herramienta permitirá:

- Recibir parámetros mediante `argparse`.
- Comprobar la conectividad con un equipo.
- Mostrar información del sistema.
- Consultar información de un archivo.
- Generar una copia de seguridad.
- Controlar errores mediante excepciones.
- Registrar las operaciones mediante `logging`.

El objetivo no es introducir nuevas técnicas.

Utilizaremos únicamente conceptos que ya hemos estudiado.

---

### 98. Estructura de la práctica

Utilizaremos la siguiente estructura:

```text
practicas/
└── capitulo4/
    ├── datos/
    │   └── datos_empresa/
    ├── logs/
    ├── programas/
    │   └── administrador.py
    └── resultados/
        └── backups/
```

Si todavía no existen los directorios, puedes crearlos desde VS Code.

Dentro de:

```text
datos/datos_empresa/
```

puedes colocar algunos archivos de prueba.

Por ejemplo:

```text
clientes.txt
equipos.csv
notas.txt
```

!!! warning "Utiliza datos de prueba"

    Durante el desarrollo de herramientas que copian, modifican o procesan archivos es recomendable trabajar inicialmente con información creada expresamente para las prácticas.

---

### 99. Funcionamiento de la herramienta

El programa tendrá varias operaciones.

Podremos consultar la ayuda:

```powershell
python administrador.py --help
```

Comprobar un equipo:

```powershell
python administrador.py --ping 192.168.1.1
```

Mostrar información del sistema:

```powershell
python administrador.py --sistema
```

Consultar información de un archivo:

```powershell
python administrador.py --archivo "../datos/equipos.csv"
```

Realizar una copia de seguridad:

```powershell
python administrador.py --backup "../datos/datos_empresa"
```

También podremos activar información adicional mediante:

```text
--detallado
```

Por ejemplo:

```powershell
python administrador.py --ping 192.168.1.1 --detallado
```

---

### 100. Preparar las importaciones

Crea:

```text
practicas/capitulo4/programas/administrador.py
```

Comenzamos con:

```python
import argparse
import logging
import shutil
import subprocess

from datetime import datetime
from pathlib import Path
```

Cada módulo tendrá una función:

```text
argparse
    argumentos

logging
    registro de actividad

shutil
    copias de seguridad

subprocess
    comandos del sistema

datetime
    fecha y hora

pathlib
    rutas y archivos
```

---

### 101. Definir las rutas del proyecto

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

DIRECTORIO_BACKUPS = (
    DIRECTORIO_RESULTADOS
    / "backups"
)
```

Creamos los directorios necesarios:

```python
DIRECTORIO_LOGS.mkdir(
    parents=True,
    exist_ok=True
)

DIRECTORIO_BACKUPS.mkdir(
    parents=True,
    exist_ok=True
)
```

Nuestro programa podrá encontrar sus directorios independientemente del directorio desde el que lo ejecutemos.

---

### 102. Configurar el sistema de logs

Añade:

```python
ARCHIVO_LOG = (
    DIRECTORIO_LOGS
    / "administrador.log"
)
```

Configuramos `logging`:

```python
logging.basicConfig(
    filename=ARCHIVO_LOG,
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

A partir de este momento podremos utilizar:

```python
logging.info(...)
```

```python
logging.warning(...)
```

```python
logging.error(...)
```

para registrar la actividad.

---

### 103. Crear el analizador de argumentos

Añade:

```python
parser = argparse.ArgumentParser(
    description=(
        "Herramienta básica "
        "de administración "
        "de sistemas."
    )
)
```

Ahora definimos las operaciones disponibles.

---

### 104. Argumento `--ping`

Añade:

```python
parser.add_argument(
    "--ping",
    metavar="EQUIPO",
    help=(
        "Comprueba la conectividad "
        "con una IP o nombre"
    )
)
```

Podremos utilizar:

```powershell
python administrador.py --ping 127.0.0.1
```

El valor estará disponible mediante:

```python
args.ping
```

---

### 105. Argumento `--sistema`

Esta opción no necesita ningún valor.

Utilizamos:

```python
parser.add_argument(
    "--sistema",
    action="store_true",
    help=(
        "Muestra información "
        "del sistema"
    )
)
```

Podremos ejecutar:

```powershell
python administrador.py --sistema
```

---

### 106. Argumento `--archivo`

Añade:

```python
parser.add_argument(
    "--archivo",
    metavar="RUTA",
    help=(
        "Muestra información "
        "sobre un archivo"
    )
)
```

Por ejemplo:

```powershell
python administrador.py --archivo datos.txt
```

---

### 107. Argumento `--backup`

Añade:

```python
parser.add_argument(
    "--backup",
    metavar="DIRECTORIO",
    help=(
        "Realiza una copia "
        "de seguridad"
    )
)
```

Podremos ejecutar:

```powershell
python administrador.py --backup "../datos/datos_empresa"
```

---

### 108. Modo detallado

Añadimos:

```python
parser.add_argument(
    "-d",
    "--detallado",
    action="store_true",
    help=(
        "Muestra información "
        "adicional"
    )
)
```

Finalmente:

```python
args = parser.parse_args()
```

---

### 109. Función para comprobar un equipo

Creamos:

```python
def comprobar_equipo(
    equipo,
    detallado=False
):

    logging.info(
        f"Comprobando equipo: "
        f"{equipo}"
    )

    try:

        resultado = subprocess.run(
            [
                "ping",
                "-n",
                "1",
                equipo
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

    except FileNotFoundError:

        print(
            "ERROR: no se encuentra "
            "el comando ping."
        )

        logging.critical(
            "Comando ping "
            "no disponible"
        )

        return

    except subprocess.TimeoutExpired:

        print(
            "ERROR: tiempo de "
            "espera agotado."
        )

        logging.error(
            f"Timeout comprobando "
            f"{equipo}"
        )

        return

    except OSError as error:

        print(
            "ERROR ejecutando ping."
        )

        logging.exception(
            f"Error ejecutando ping: "
            f"{error}"
        )

        return

    if resultado.returncode == 0:

        print(
            f"{equipo}: RESPONDE"
        )

        logging.info(
            f"{equipo}: RESPONDE"
        )

    else:

        print(
            f"{equipo}: NO RESPONDE"
        )

        logging.warning(
            f"{equipo}: NO RESPONDE"
        )

    if detallado:

        print()
        print("SALIDA DEL COMANDO")
        print("==================")
        print()

        print(
            resultado.stdout
        )
```

Aquí estamos combinando:

```text
subprocess
+
try / except
+
logging
```

---

### 110. Función de información del sistema

Añade:

```python
def mostrar_sistema(
    detallado=False
):

    logging.info(
        "Consultando información "
        "del sistema"
    )

    try:

        hostname = subprocess.run(
            [
                "hostname"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

    except FileNotFoundError:

        print(
            "ERROR: comando "
            "no disponible."
        )

        logging.error(
            "No se encuentra hostname"
        )

        return

    except subprocess.TimeoutExpired:

        print(
            "ERROR: tiempo de "
            "espera agotado."
        )

        logging.error(
            "Timeout ejecutando "
            "hostname"
        )

        return

    except OSError as error:

        print(
            "ERROR consultando "
            "el sistema."
        )

        logging.exception(
            f"Error del sistema: "
            f"{error}"
        )

        return

    print()
    print("INFORMACIÓN DEL SISTEMA")
    print("=======================")
    print()

    print(
        f"Nombre: "
        f"{hostname.stdout.strip()}"
    )

    if detallado:

        try:

            informacion = (
                subprocess.run(
                    [
                        "systeminfo"
                    ],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            )

        except (
            FileNotFoundError,
            subprocess.TimeoutExpired
        ) as error:

            print(
                "No se ha podido "
                "obtener información "
                "detallada."
            )

            logging.error(
                f"Error ejecutando "
                f"systeminfo: {error}"
            )

        else:

            print()
            print(
                informacion.stdout
            )

    logging.info(
        "Consulta del sistema "
        "finalizada"
    )
```

!!! note "Windows"

    Esta práctica está preparada para el entorno Windows utilizado durante el curso.

    Por eso utilizamos comandos como:

    ```text
    ping -n
    ```

    y:

    ```text
    systeminfo
    ```

---

### 111. Función para analizar un archivo

Añade:

```python
def mostrar_archivo(ruta):

    archivo = Path(ruta)

    logging.info(
        f"Consultando archivo: "
        f"{archivo}"
    )

    if not archivo.exists():

        print(
            "ERROR: el archivo "
            "no existe."
        )

        logging.error(
            f"Archivo inexistente: "
            f"{archivo}"
        )

        return

    if not archivo.is_file():

        print(
            "ERROR: la ruta no "
            "corresponde a un archivo."
        )

        logging.warning(
            f"No es un archivo: "
            f"{archivo}"
        )

        return

    try:

        tamano = (
            archivo.stat().st_size
        )

    except OSError as error:

        print(
            "ERROR: no se puede "
            "consultar el archivo."
        )

        logging.exception(
            f"Error consultando "
            f"{archivo}: {error}"
        )

        return

    print()
    print("INFORMACIÓN DEL ARCHIVO")
    print("=======================")
    print()

    print(
        f"Nombre: {archivo.name}"
    )

    print(
        f"Extensión: "
        f"{archivo.suffix}"
    )

    print(
        f"Tamaño: "
        f"{tamano} bytes"
    )

    print(
        f"Ruta: "
        f"{archivo.resolve()}"
    )

    logging.info(
        f"Archivo consultado: "
        f"{archivo}"
    )
```

---

### 112. Función para realizar backups

Añade:

```python
def realizar_backup(ruta):

    origen = Path(ruta)

    logging.info(
        f"Solicitud de backup: "
        f"{origen}"
    )

    if not origen.exists():

        print(
            "ERROR: el directorio "
            "no existe."
        )

        logging.error(
            f"Origen inexistente: "
            f"{origen}"
        )

        return

    if not origen.is_dir():

        print(
            "ERROR: el origen debe "
            "ser un directorio."
        )

        logging.warning(
            f"El origen no es "
            f"directorio: {origen}"
        )

        return

    fecha = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    destino = (
        DIRECTORIO_BACKUPS
        / f"backup_{fecha}"
    )

    print()
    print("COPIA DE SEGURIDAD")
    print("==================")
    print()

    print(
        f"Origen: {origen}"
    )

    print(
        f"Destino: {destino}"
    )

    print()

    try:

        shutil.copytree(
            origen,
            destino
        )

    except PermissionError:

        print(
            "ERROR: permiso "
            "denegado."
        )

        logging.error(
            f"Permiso denegado "
            f"copiando {origen}"
        )

    except OSError as error:

        print(
            "ERROR durante "
            "la copia."
        )

        logging.exception(
            f"Error realizando "
            f"backup: {error}"
        )

    else:

        print(
            "Backup realizado "
            "correctamente."
        )

        logging.info(
            f"Backup completado: "
            f"{destino}"
        )

    finally:

        logging.info(
            "Operación de backup "
            "finalizada"
        )
```

---

### 113. Programa principal

Ya tenemos las funciones.

Ahora debemos decidir cuál ejecutar dependiendo de los argumentos recibidos.

Añade al final:

```python
logging.info(
    "Programa iniciado"
)


if args.ping:

    comprobar_equipo(
        args.ping,
        args.detallado
    )

elif args.sistema:

    mostrar_sistema(
        args.detallado
    )

elif args.archivo:

    mostrar_archivo(
        args.archivo
    )

elif args.backup:

    realizar_backup(
        args.backup
    )

else:

    parser.print_help()


logging.info(
    "Programa finalizado"
)
```

El flujo general será:

```text
             administrador.py
                    │
                    ▼
                 argparse
                    │
       ┌────────────┼────────────┐
       │            │            │
       ▼            ▼            ▼
    --ping       --sistema    --archivo
       │            │            │
       │            │            │
       └────────┬───┴─────┬──────┘
                │         │
                │     --backup
                │         │
                └────┬────┘
                     │
                     ▼
                  función
                     │
                     ▼
                validación
                     │
                     ▼
                 operación
                     │
                     ▼
             control de errores
                     │
                     ▼
                   logging
```

---

### 114. Probar la ayuda

Antes de probar las operaciones ejecuta:

```powershell
python administrador.py --help
```

Debemos comprobar que aparecen las opciones:

```text
--ping
--sistema
--archivo
--backup
-d
--detallado
```

Esta prueba nos permite comprobar que `argparse` se ha configurado correctamente.

---

### 115. Prueba 1: comprobar localhost

Ejecuta:

```powershell
python administrador.py --ping 127.0.0.1
```

Deberíamos obtener:

```text
127.0.0.1: RESPONDE
```

Ahora:

```powershell
python administrador.py --ping 127.0.0.1 --detallado
```

Además del resultado aparecerá la salida del comando `ping`.

Comprueba:

```text
logs/administrador.log
```

Deberán haberse registrado ambas operaciones.

---

### 116. Prueba 2: información del sistema

Ejecuta:

```powershell
python administrador.py --sistema
```

Después:

```powershell
python administrador.py --sistema --detallado
```

La segunda ejecución utilizará también:

```text
systeminfo
```

y mostrará más información.

---

### 117. Prueba 3: consultar un archivo

Crea un archivo de prueba:

```text
datos/prueba.txt
```

Puedes escribir:

```text
Archivo de prueba del capítulo 4.
```

Desde el directorio:

```text
programas/
```

ejecuta:

```powershell
python administrador.py --archivo "../datos/prueba.txt"
```

El programa mostrará:

```text
nombre
extensión
tamaño
ruta completa
```

Después prueba:

```powershell
python administrador.py --archivo "../datos/no_existe.txt"
```

El programa deberá informar del problema y registrarlo en el log.

---

### 118. Prueba 4: realizar un backup

Dentro de:

```text
datos/datos_empresa/
```

coloca algunos archivos de prueba.

Después ejecuta:

```powershell
python administrador.py --backup "../datos/datos_empresa"
```

Deberá aparecer un nuevo directorio parecido a:

```text
resultados/
└── backups/
    └── backup_2026-09-21_12-30-15/
```

Dentro encontraremos la copia de los archivos.

También deberá aparecer un registro en:

```text
logs/administrador.log
```

---

### 119. Comprobar el log completo

Después de realizar varias pruebas abre:

```text
logs/administrador.log
```

Podremos encontrar algo parecido a:

```text
2026-09-21 12:30:01 - INFO - Programa iniciado
2026-09-21 12:30:01 - INFO - Comprobando equipo: 127.0.0.1
2026-09-21 12:30:01 - INFO - 127.0.0.1: RESPONDE
2026-09-21 12:30:01 - INFO - Programa finalizado
2026-09-21 12:32:15 - INFO - Programa iniciado
2026-09-21 12:32:15 - INFO - Solicitud de backup: ../datos/datos_empresa
2026-09-21 12:32:15 - INFO - Backup completado: ...
2026-09-21 12:32:15 - INFO - Operación de backup finalizada
2026-09-21 12:32:15 - INFO - Programa finalizado
```

Observa que ahora podemos reconstruir qué ha hecho el programa incluso después de haber cerrado el terminal.

Eso es precisamente una de las finalidades de la auditoría mediante logs.

---

### 120. Mejorar la selección de operaciones

Nuestro programa utiliza:

```python
if
elif
elif
elif
```

Por tanto, está pensado para realizar una operación en cada ejecución.

Sin embargo, actualmente `argparse` permitiría escribir algo como:

```powershell
python administrador.py --ping 127.0.0.1 --sistema
```

Aunque posteriormente nuestro `if/elif` ejecutaría solamente una de las operaciones.

Podemos evitar esta situación utilizando un **grupo mutuamente excluyente**.

Sustituye la definición individual de las operaciones por:

```python
grupo = (
    parser.add_mutually_exclusive_group()
)
```

Después añade los argumentos al grupo:

```python
grupo.add_argument(
    "--ping",
    metavar="EQUIPO",
    help=(
        "Comprueba la conectividad "
        "con una IP o nombre"
    )
)

grupo.add_argument(
    "--sistema",
    action="store_true",
    help=(
        "Muestra información "
        "del sistema"
    )
)

grupo.add_argument(
    "--archivo",
    metavar="RUTA",
    help=(
        "Muestra información "
        "sobre un archivo"
    )
)

grupo.add_argument(
    "--backup",
    metavar="DIRECTORIO",
    help=(
        "Realiza una copia "
        "de seguridad"
    )
)
```

Ahora `argparse` impedirá seleccionar varias operaciones incompatibles simultáneamente.

Por ejemplo:

```powershell
python administrador.py --ping 127.0.0.1 --sistema
```

generará un mensaje de error.

!!! tip "La validación también puede formar parte de la interfaz"

    Siempre que sea posible debemos aprovechar las herramientas que proporciona `argparse` para impedir combinaciones incorrectas de argumentos.

---

### 121. Código completo de `administrador.py`

Una vez desarrolladas y probadas las partes anteriores, el programa completo puede quedar así:

```python
import argparse
import logging
import shutil
import subprocess

from datetime import datetime
from pathlib import Path


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

DIRECTORIO_BACKUPS = (
    DIRECTORIO_RESULTADOS
    / "backups"
)


DIRECTORIO_LOGS.mkdir(
    parents=True,
    exist_ok=True
)

DIRECTORIO_BACKUPS.mkdir(
    parents=True,
    exist_ok=True
)


# -----------------------------
# Logging
# -----------------------------

ARCHIVO_LOG = (
    DIRECTORIO_LOGS
    / "administrador.log"
)


logging.basicConfig(
    filename=ARCHIVO_LOG,
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


# -----------------------------
# Funciones
# -----------------------------

def comprobar_equipo(
    equipo,
    detallado=False
):

    logging.info(
        f"Comprobando equipo: "
        f"{equipo}"
    )

    try:

        resultado = subprocess.run(
            [
                "ping",
                "-n",
                "1",
                equipo
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

    except FileNotFoundError:

        print(
            "ERROR: no se encuentra "
            "el comando ping."
        )

        logging.critical(
            "Comando ping "
            "no disponible"
        )

        return

    except subprocess.TimeoutExpired:

        print(
            "ERROR: tiempo de "
            "espera agotado."
        )

        logging.error(
            f"Timeout comprobando "
            f"{equipo}"
        )

        return

    except OSError as error:

        print(
            "ERROR ejecutando ping."
        )

        logging.exception(
            f"Error ejecutando ping: "
            f"{error}"
        )

        return

    if resultado.returncode == 0:

        print(
            f"{equipo}: RESPONDE"
        )

        logging.info(
            f"{equipo}: RESPONDE"
        )

    else:

        print(
            f"{equipo}: NO RESPONDE"
        )

        logging.warning(
            f"{equipo}: NO RESPONDE"
        )

    if detallado:

        print()
        print("SALIDA DEL COMANDO")
        print("==================")
        print()

        print(
            resultado.stdout
        )


def mostrar_sistema(
    detallado=False
):

    logging.info(
        "Consultando información "
        "del sistema"
    )

    try:

        hostname = subprocess.run(
            ["hostname"],
            capture_output=True,
            text=True,
            timeout=10
        )

    except FileNotFoundError:

        print(
            "ERROR: comando "
            "no disponible."
        )

        logging.error(
            "No se encuentra hostname"
        )

        return

    except subprocess.TimeoutExpired:

        print(
            "ERROR: tiempo de "
            "espera agotado."
        )

        logging.error(
            "Timeout ejecutando "
            "hostname"
        )

        return

    except OSError as error:

        print(
            "ERROR consultando "
            "el sistema."
        )

        logging.exception(
            f"Error del sistema: "
            f"{error}"
        )

        return

    print()
    print("INFORMACIÓN DEL SISTEMA")
    print("=======================")
    print()

    print(
        f"Nombre: "
        f"{hostname.stdout.strip()}"
    )

    if detallado:

        try:

            informacion = (
                subprocess.run(
                    ["systeminfo"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            )

        except (
            FileNotFoundError,
            subprocess.TimeoutExpired
        ) as error:

            print(
                "No se ha podido "
                "obtener información "
                "detallada."
            )

            logging.error(
                f"Error ejecutando "
                f"systeminfo: {error}"
            )

        else:

            print()
            print(
                informacion.stdout
            )

    logging.info(
        "Consulta del sistema "
        "finalizada"
    )


def mostrar_archivo(ruta):

    archivo = Path(ruta)

    logging.info(
        f"Consultando archivo: "
        f"{archivo}"
    )

    if not archivo.exists():

        print(
            "ERROR: el archivo "
            "no existe."
        )

        logging.error(
            f"Archivo inexistente: "
            f"{archivo}"
        )

        return

    if not archivo.is_file():

        print(
            "ERROR: la ruta no "
            "corresponde a un archivo."
        )

        logging.warning(
            f"No es un archivo: "
            f"{archivo}"
        )

        return

    try:

        tamano = (
            archivo.stat().st_size
        )

    except OSError as error:

        print(
            "ERROR: no se puede "
            "consultar el archivo."
        )

        logging.exception(
            f"Error consultando "
            f"{archivo}: {error}"
        )

        return

    print()
    print("INFORMACIÓN DEL ARCHIVO")
    print("=======================")
    print()

    print(
        f"Nombre: {archivo.name}"
    )

    print(
        f"Extensión: "
        f"{archivo.suffix}"
    )

    print(
        f"Tamaño: "
        f"{tamano} bytes"
    )

    print(
        f"Ruta: "
        f"{archivo.resolve()}"
    )

    logging.info(
        f"Archivo consultado: "
        f"{archivo}"
    )


def realizar_backup(ruta):

    origen = Path(ruta)

    logging.info(
        f"Solicitud de backup: "
        f"{origen}"
    )

    if not origen.exists():

        print(
            "ERROR: el directorio "
            "no existe."
        )

        logging.error(
            f"Origen inexistente: "
            f"{origen}"
        )

        return

    if not origen.is_dir():

        print(
            "ERROR: el origen debe "
            "ser un directorio."
        )

        logging.warning(
            f"No es directorio: "
            f"{origen}"
        )

        return

    fecha = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    destino = (
        DIRECTORIO_BACKUPS
        / f"backup_{fecha}"
    )

    print()
    print("COPIA DE SEGURIDAD")
    print("==================")
    print()

    print(
        f"Origen: {origen}"
    )

    print(
        f"Destino: {destino}"
    )

    print()

    try:

        shutil.copytree(
            origen,
            destino
        )

    except PermissionError:

        print(
            "ERROR: permiso "
            "denegado."
        )

        logging.error(
            f"Permiso denegado "
            f"copiando {origen}"
        )

    except OSError as error:

        print(
            "ERROR durante "
            "la copia."
        )

        logging.exception(
            f"Error realizando "
            f"backup: {error}"
        )

    else:

        print(
            "Backup realizado "
            "correctamente."
        )

        logging.info(
            f"Backup completado: "
            f"{destino}"
        )

    finally:

        logging.info(
            "Operación de backup "
            "finalizada"
        )


# -----------------------------
# Argumentos
# -----------------------------

parser = argparse.ArgumentParser(
    description=(
        "Herramienta básica "
        "de administración "
        "de sistemas."
    )
)


grupo = (
    parser.add_mutually_exclusive_group()
)


grupo.add_argument(
    "--ping",
    metavar="EQUIPO",
    help=(
        "Comprueba la conectividad "
        "con una IP o nombre"
    )
)


grupo.add_argument(
    "--sistema",
    action="store_true",
    help=(
        "Muestra información "
        "del sistema"
    )
)


grupo.add_argument(
    "--archivo",
    metavar="RUTA",
    help=(
        "Muestra información "
        "sobre un archivo"
    )
)


grupo.add_argument(
    "--backup",
    metavar="DIRECTORIO",
    help=(
        "Realiza una copia "
        "de seguridad"
    )
)


parser.add_argument(
    "-d",
    "--detallado",
    action="store_true",
    help=(
        "Muestra información "
        "adicional"
    )
)


args = parser.parse_args()


# -----------------------------
# Programa principal
# -----------------------------

logging.info(
    "Programa iniciado"
)


if args.ping:

    comprobar_equipo(
        args.ping,
        args.detallado
    )

elif args.sistema:

    mostrar_sistema(
        args.detallado
    )

elif args.archivo:

    mostrar_archivo(
        args.archivo
    )

elif args.backup:

    realizar_backup(
        args.backup
    )

else:

    parser.print_help()


logging.info(
    "Programa finalizado"
)
```

---

### 122. Práctica de ampliación

Crea una segunda versión:

```text
administrador_v2.py
```

Añade progresivamente nuevas posibilidades.

#### Primera ampliación

Añade:

```text
--ipconfig
```

para ejecutar:

```text
ipconfig
```

y mostrar la configuración de red del equipo.

#### Segunda ampliación

Añade:

```text
--informe
```

para guardar los resultados en:

```text
resultados/informe.txt
```

#### Tercera ampliación

Permite indicar:

```text
--intentos
```

al utilizar:

```text
--ping
```

Por ejemplo:

```powershell
python administrador_v2.py --ping 192.168.1.1 --intentos 4
```

#### Cuarta ampliación

Añade un argumento:

```text
--log-debug
```

que permita trabajar con información más detallada durante las pruebas.

El objetivo no es añadir funciones sin límite.

El objetivo es practicar cómo hacer crecer un script manteniendo una estructura organizada.

---

### 123. Reto final del capítulo

Desarrolla:

```text
gestor_sistemas.py
```

El programa deberá incluir como mínimo:

```text
1. argparse

2. Al menos tres operaciones

3. Validación de argumentos

4. Uso de pathlib

5. Ejecución de algún comando
   mediante subprocess

6. Control de al menos tres
   tipos de excepción

7. Uso de try / except

8. Uso de else o finally

9. Registro mediante logging

10. Archivo .log con fecha,
    nivel y mensaje
```

El programa deberá disponer de ayuda:

```powershell
python gestor_sistemas.py --help
```

y nunca deberá depender de modificar manualmente variables dentro del código para realizar las operaciones habituales.

!!! success "Objetivo de la práctica"

    Si has completado esta práctica, ya eres capaz de construir scripts de administración parametrizables, con control de errores y registro de actividad.

---

## 124. Qué hemos aprendido en el capítulo 4

Comenzamos utilizando:

```python
sys.argv
```

para comprender cómo recibe Python los argumentos de la línea de comandos.

Después utilizamos:

```python
argparse
```

para crear interfaces más claras.

Aprendimos a definir:

```text
argumentos posicionales
argumentos opcionales
valores predeterminados
tipos de datos
banderas
ayuda automática
```

Posteriormente profundizamos en:

```python
try
except
else
finally
```

y aprendimos a controlar excepciones concretas como:

```text
ValueError
FileNotFoundError
PermissionError
OSError
subprocess.TimeoutExpired
subprocess.CalledProcessError
```

Finalmente incorporamos:

```python
logging
```

para registrar la actividad de nuestros scripts mediante:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

---

### 125. Evolución de nuestros scripts

A lo largo de los primeros cuatro capítulos hemos seguido una evolución progresiva.

```text
CAPÍTULO 1
Gestión de archivos
        │
        ▼
CAPÍTULO 2
Comandos del sistema
        │
        ▼
CAPÍTULO 3
Automatización
        │
        ▼
CAPÍTULO 4
Scripts robustos
```

Ahora podemos combinar:

```text
archivos
   +
CSV
   +
pathlib
   +
subprocess
   +
funciones
   +
automatización
   +
argparse
   +
excepciones
   +
logging
```

para desarrollar herramientas de administración considerablemente más completas.

---

### 126. Patrón de un script de administración

Podemos resumir la estructura que hemos aprendido mediante:

```text
        INICIO
          │
          ▼
      argparse
          │
          ▼
     argumentos
          │
          ▼
      validación
          │
          ▼
       función
          │
          ▼
     ┌────try────┐
     │           │
     ▼           ▼
 operación     excepción
     │           │
     ▼           ▼
   else        except
     │           │
     └─────┬─────┘
           │
           ▼
        finally
           │
           ▼
        logging
           │
           ▼
     resultado/log
           │
           ▼
          FIN
```

No todos los programas necesitarán todos estos elementos.

Debemos utilizar únicamente aquellos que tengan sentido para cada problema.

---

### 127. Buenas prácticas del capítulo

Antes de terminar, podemos establecer algunas reglas:

1. No guardes valores que cambian frecuentemente dentro del código si pueden recibirse como argumentos.

2. Utiliza `argparse` cuando el script tenga una interfaz de línea de comandos con varias opciones.

3. Valida los datos antes de utilizarlos.

4. Captura excepciones concretas siempre que sea posible.

5. Evita utilizar un `except` genérico para ocultar cualquier problema.

6. Utiliza bloques `try` pequeños y centrados en la operación que puede fallar.

7. Utiliza `logging` para registrar información útil sobre la ejecución.

8. No almacenes contraseñas, tokens ni otras credenciales en los logs.

9. Utiliza `print()` para informar al usuario y `logging` para registrar la actividad cuando ambos sean necesarios.

10. Prueba también los casos incorrectos, no únicamente los casos en los que todo funciona.

---

## 128. Fin del capítulo

!!! success "Capítulo 4 completado"

    Has completado el capítulo dedicado al **scripting avanzado y control de errores**.

    Ya sabes crear scripts capaces de:

    - Recibir argumentos desde la línea de comandos.
    - Crear interfaces mediante `argparse`.
    - Validar los datos recibidos.
    - Controlar excepciones.
    - Ejecutar comandos de forma controlada.
    - Registrar la actividad mediante `logging`.
    - Generar archivos de log.
    - Combinar estas herramientas en una aplicación completa.

Con este capítulo finalizamos el bloque dedicado al **scripting y automatización de sistemas**.

El siguiente paso será comenzar a utilizar Python para comunicarnos con servicios y recursos de red.