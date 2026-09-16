# Ejecución de comandos del sistema

## 1. Introducción

Hasta ahora nuestros programas Python han trabajado principalmente con archivos, directorios y datos.

Sin embargo, para utilizar Python como herramienta de **administración de sistemas** necesitamos que nuestros programas puedan interactuar directamente con el sistema operativo.

Desde Python podemos ejecutar comandos similares a los que escribiríamos manualmente en una terminal de Windows:

```powershell
ipconfig
ping 192.168.1.1
systeminfo
hostname
```

Esto nos permitirá crear scripts capaces de:

- Obtener información del sistema.
- Consultar la configuración de red.
- Comprobar la conectividad con otros equipos.
- Ejecutar herramientas del sistema operativo.
- Capturar los resultados de los comandos.
- Analizar automáticamente esos resultados.
- Detectar si un comando ha terminado correctamente.

El objetivo no será simplemente ejecutar comandos desde Python.

Queremos llegar a construir programas capaces de seguir este proceso:

```text
Python
   │
   ▼
Ejecutar comando
   │
   ▼
Sistema operativo
   │
   ▼
Resultado
   │
   ▼
Python
   │
   ├── mostrar
   ├── analizar
   ├── guardar
   └── tomar decisiones
```

Este mecanismo será fundamental cuando posteriormente construyamos scripts de diagnóstico de sistemas y redes.

---

## 2. El módulo `subprocess`

Python proporciona el módulo:

```python
subprocess
```

para ejecutar otros programas y comandos del sistema operativo.

Forma parte de la **biblioteca estándar de Python**, por lo que no necesitamos instalar ningún paquete mediante `pip`.

Para utilizarlo escribimos:

```python
import subprocess
```

Durante este capítulo utilizaremos principalmente:

```python
subprocess.run()
```

### Nuestro primer comando desde Python

Vamos a comenzar con un comando muy sencillo de Windows:

```powershell
hostname
```

Este comando muestra el nombre del ordenador.

Antes de utilizarlo desde Python, ejecútalo directamente en la terminal de VS Code:

```powershell
hostname
```

Obtendrás un resultado similar a:

```text
PC-AULA-01
```

Ahora vamos a conseguir que sea **Python quien ejecute ese mismo comando**.

Dentro de:

```text
practicas/
```

crea la estructura:

```text
capitulo2/
└── programas/
```

Por tanto, tendremos:

```text
practicas/
├── capitulo1/
│   ├── datos/
│   ├── informes/
│   └── programas/
│
└── capitulo2/
    └── programas/
```

Dentro de:

```text
practicas/capitulo2/programas/
```

crea:

```text
primer_comando.py
```

Escribe:

```python
import subprocess

subprocess.run(["hostname"])
```

Ejecuta:

```powershell
python primer_comando.py
```

En la terminal aparecerá el nombre de tu ordenador.

Por ejemplo:

```text
PC-AULA-01
```

Acabamos de ejecutar nuestro **primer comando del sistema operativo desde Python**.

---

### Comprender `subprocess.run()`

Observa:

```python
subprocess.run(["hostname"])
```

Tenemos dos elementos importantes.

Primero:

```python
subprocess
```

es el módulo que hemos importado.

Después:

```python
run()
```

es la función que utilizamos para ejecutar el programa externo.

El comando aparece dentro de una lista:

```python
["hostname"]
```

Por tanto:

```python
subprocess.run(["hostname"])
```

puede interpretarse como:

> Ejecuta el programa `hostname` y espera hasta que termine.

!!! tip "Importante"

    `subprocess.run()` espera normalmente a que el comando termine antes de que Python continúe ejecutando las siguientes instrucciones.

---

### Ejecutar un comando con argumentos

Muchos comandos necesitan parámetros.

Por ejemplo:

```powershell
ping 127.0.0.1
```

Aquí tenemos:

```text
ping          → comando
127.0.0.1     → argumento
```

Con `subprocess.run()` los escribimos como elementos separados de una lista:

```python
subprocess.run(["ping", "127.0.0.1"])
```

Crea:

```text
primer_ping.py
```

Escribe:

```python
import subprocess

subprocess.run(["ping", "127.0.0.1"])
```

Ejecuta:

```powershell
python primer_ping.py
```

Windows realizará un `ping` a:

```text
127.0.0.1
```

Esta dirección corresponde a la interfaz de **loopback** del propio equipo.

La salida será similar a:

```text
Haciendo ping a 127.0.0.1 con 32 bytes de datos:
Respuesta desde 127.0.0.1: bytes=32 tiempo<1ms TTL=128
Respuesta desde 127.0.0.1: bytes=32 tiempo<1ms TTL=128
Respuesta desde 127.0.0.1: bytes=32 tiempo<1ms TTL=128
Respuesta desde 127.0.0.1: bytes=32 tiempo<1ms TTL=128
```

!!! note "Comandos y argumentos"

    Cuando utilizamos una lista con `subprocess.run()`, escribiremos normalmente el comando y sus argumentos como elementos independientes.

    Por ejemplo:

    ```python
    subprocess.run(["ping", "127.0.0.1"])
    ```

    y no:

    ```python
    subprocess.run(["ping 127.0.0.1"])
    ```

---

### Limitar el número de paquetes de `ping`

En Windows podemos indicar el número de solicitudes mediante:

```powershell
ping -n 2 127.0.0.1
```

Desde Python:

```python
import subprocess

subprocess.run([
    "ping",
    "-n",
    "2",
    "127.0.0.1"
])
```

Observa que cada elemento está separado:

```text
"ping"
"-n"
"2"
"127.0.0.1"
```

Esto equivale a ejecutar:

```powershell
ping -n 2 127.0.0.1
```

---

### Ejecutar varios comandos

Podemos ejecutar diferentes comandos consecutivamente.

Crea:

```text
informacion_basica.py
```

Escribe:

```python
import subprocess

print("NOMBRE DEL EQUIPO")
print("=================")

subprocess.run(["hostname"])

print()
print("CONFIGURACIÓN DE RED")
print("====================")

subprocess.run(["ipconfig"])
```

Ejecuta:

```powershell
python informacion_basica.py
```

Python ejecutará primero:

```text
hostname
```

y posteriormente:

```text
ipconfig
```

El proceso es:

```text
Programa Python
      │
      ├── hostname
      │      ↓
      │   Windows
      │      ↓
      │   resultado
      │
      └── ipconfig
             ↓
          Windows
             ↓
          resultado
```

Ya podemos comenzar a utilizar Python como intermediario entre nuestros programas y las herramientas proporcionadas por el sistema operativo.

---

### Una primera práctica

Crea:

```text
diagnostico_basico.py
```

El programa debe ejecutar consecutivamente:

```powershell
hostname
```

```powershell
ipconfig
```

y:

```powershell
ping -n 2 127.0.0.1
```

Antes de cada comando debe mostrar un título para identificar claramente la información.

El resultado tendrá una estructura similar a:

```text
================================
NOMBRE DEL EQUIPO
================================

...

================================
CONFIGURACIÓN DE RED
================================

...

================================
PRUEBA DE CONECTIVIDAD
================================

...
```

!!! tip "Intenta resolverlo primero"

    Para realizar esta práctica únicamente necesitas combinar:

    ```python
    import subprocess
    ```

    ```python
    print()
    ```

    y:

    ```python
    subprocess.run([...])
    ```

---

## 3. El resultado de un comando

Hasta ahora hemos ejecutado comandos y hemos permitido que su resultado aparezca directamente en la terminal.

Por ejemplo:

```python
import subprocess

subprocess.run(["hostname"])
```

Sin embargo, nuestro verdadero objetivo será que **Python pueda obtener el resultado del comando y trabajar con él**.

Queremos pasar de:

```text
Python
   │
   ▼
hostname
   │
   ▼
Terminal
```

a:

```text
Python
   │
   ▼
hostname
   │
   ▼
resultado
   │
   ▼
variable Python
   │
   ├── mostrar
   ├── analizar
   ├── comparar
   └── guardar
```

Para ello tendremos que **capturar la salida del comando**.

Esta será la siguiente operación que aprenderemos.

---

## Resumen

En esta primera parte hemos aprendido que:

- Python puede ejecutar programas y comandos del sistema operativo.
- El módulo `subprocess` forma parte de la biblioteca estándar.
- `subprocess.run()` permite ejecutar un comando.
- Los argumentos pueden pasarse como elementos de una lista.
- Podemos ejecutar herramientas como `hostname`, `ipconfig` y `ping`.
- Python espera normalmente a que `subprocess.run()` termine antes de continuar.
- Podemos ejecutar varios comandos consecutivamente.

Hasta ahora la salida de los comandos aparece directamente en la terminal.

En el siguiente apartado aprenderemos a **capturar esa salida dentro de Python**, almacenarla en variables y comenzar a analizarla automáticamente.

---

## 4. Capturar la salida de un comando

Hasta ahora hemos ejecutado comandos de esta forma:

```python
import subprocess

subprocess.run(["hostname"])
```

El comando se ejecuta correctamente, pero su resultado aparece directamente en la terminal.

En un script de administración normalmente necesitaremos que **Python reciba ese resultado** para poder trabajar con él.

Por ejemplo, queremos poder:

- Guardar el nombre del equipo en una variable.
- Analizar el resultado de un `ping`.
- Obtener información de `ipconfig`.
- Detectar errores.
- Guardar resultados en archivos.
- Tomar decisiones dependiendo del resultado de un comando.

Para ello podemos utilizar:

```python
capture_output=True
```

### Capturar el resultado de `hostname`

Dentro de:

```text
practicas/capitulo2/programas/
```

crea:

```text
capturar_hostname.py
```

Escribe:

```python
import subprocess

resultado = subprocess.run(
    ["hostname"],
    capture_output=True,
    text=True
)

print(resultado.stdout)
```

Ejecuta:

```powershell
python capturar_hostname.py
```

Obtendrás el nombre de tu ordenador:

```text
PC-AULA-01
```

La diferencia fundamental es que ahora el resultado del comando está disponible dentro de Python.

---

### `capture_output=True`

Observa:

```python
capture_output=True
```

Esta opción indica a `subprocess.run()` que queremos **capturar la salida producida por el comando**.

Sin esta opción:

```text
hostname
    ↓
Terminal
```

Con esta opción:

```text
hostname
    ↓
subprocess
    ↓
resultado
    ↓
Python
```

Guardamos toda la información devuelta por `subprocess.run()` en:

```python
resultado
```

---

### `text=True`

También hemos utilizado:

```python
text=True
```

Esta opción hace que Python trate la salida capturada como **texto**.

Nuestro código:

```python
resultado = subprocess.run(
    ["hostname"],
    capture_output=True,
    text=True
)
```

puede interpretarse como:

> Ejecuta `hostname`, captura su salida y entrégamela como texto.

Durante este curso utilizaremos habitualmente:

```python
capture_output=True,
text=True
```

cuando necesitemos analizar la salida de un comando.

---

## 5. `stdout`, `stderr` y `returncode`

Cuando ejecutamos un comando, `subprocess.run()` devuelve información sobre su ejecución.

Tres elementos serán especialmente importantes:

```text
stdout
stderr
returncode
```

Podemos representarlos así:

```text
             COMANDO
                │
                ▼
         subprocess.run()
                │
        ┌───────┼────────┐
        ▼       ▼        ▼
     stdout   stderr  returncode
        │       │        │
      salida   error    código
      normal            final
```

### `stdout`: salida estándar

La propiedad:

```python
resultado.stdout
```

contiene la **salida estándar** generada por el comando.

Por ejemplo:

```python
import subprocess

resultado = subprocess.run(
    ["hostname"],
    capture_output=True,
    text=True
)

print("Salida del comando:")
print(resultado.stdout)
```

La salida será similar a:

```text
Salida del comando:
PC-AULA-01
```

Podemos guardar directamente esa información:

```python
nombre_equipo = resultado.stdout
```

Sin embargo, normalmente aparecerá un salto de línea al final.

Podemos eliminarlo mediante:

```python
strip()
```

Por ejemplo:

```python
import subprocess

resultado = subprocess.run(
    ["hostname"],
    capture_output=True,
    text=True
)

nombre_equipo = resultado.stdout.strip()

print(f"Nombre del equipo: {nombre_equipo}")
```

Resultado:

```text
Nombre del equipo: PC-AULA-01
```

Este patrón aparecerá muchas veces durante el curso:

```python
resultado.stdout.strip()
```

---

### `stderr`: salida de error

Los programas también pueden generar mensajes de error.

Estos mensajes se encuentran normalmente en:

```python
resultado.stderr
```

Podemos comprobarlo con:

```python
import subprocess

resultado = subprocess.run(
    ["hostname"],
    capture_output=True,
    text=True
)

print("SALIDA:")
print(resultado.stdout)

print("ERRORES:")
print(resultado.stderr)
```

Si el comando funciona correctamente, normalmente `stderr` estará vacío.

Obtendríamos algo parecido a:

```text
SALIDA:
PC-AULA-01

ERRORES:
```

!!! note "stdout y stderr"

    Un programa puede disponer de dos canales diferentes de salida:

    - `stdout`: salida normal del programa.
    - `stderr`: mensajes de error.

    Mantener ambos canales separados permite que nuestros scripts distingan entre resultados normales y errores.

---

### `returncode`: código de retorno

Además de producir una salida, los programas devuelven un **código de retorno** cuando terminan.

Podemos consultarlo mediante:

```python
resultado.returncode
```

Prueba:

```python
import subprocess

resultado = subprocess.run(
    ["hostname"],
    capture_output=True,
    text=True
)

print(f"Código de retorno: {resultado.returncode}")
```

Si `hostname` termina correctamente, normalmente obtendremos:

```text
Código de retorno: 0
```

Como regla general:

```text
0       → ejecución correcta
distinto de 0 → se ha producido algún problema
```

!!! note "Importante"

    El significado exacto de los códigos distintos de cero depende del programa ejecutado.

    Por ello, no debemos asumir que todos los comandos utilizan exactamente los mismos códigos de error.

---

### Comprobar si un comando ha funcionado

Podemos utilizar `returncode` dentro de una condición:

```python
import subprocess

resultado = subprocess.run(
    ["hostname"],
    capture_output=True,
    text=True
)

if resultado.returncode == 0:
    print("Comando ejecutado correctamente.")
    print(resultado.stdout.strip())
else:
    print("Se ha producido un error.")
    print(resultado.stderr.strip())
```

Ahora Python ya no se limita a ejecutar el comando.

También puede **tomar una decisión dependiendo del resultado**:

```text
Ejecutar comando
       │
       ▼
   returncode
       │
   ┌───┴───┐
   │       │
   0      != 0
   │       │
   ▼       ▼
correcto  error
```

Esta será una de las bases de nuestros scripts de diagnóstico.

---

## 6. Capturar la configuración de red

Vamos a aplicar lo aprendido a un comando que devuelve mucha más información.

En Windows podemos ejecutar:

```powershell
ipconfig
```

Crea:

```text
capturar_ipconfig.py
```

Escribe:

```python
import subprocess

resultado = subprocess.run(
    ["ipconfig"],
    capture_output=True,
    text=True
)

print(resultado.stdout)
```

Ejecuta:

```powershell
python capturar_ipconfig.py
```

Ahora la salida de `ipconfig` ha sido capturada por Python antes de mostrarse.

Esto significa que podemos almacenarla en una variable:

```python
configuracion = resultado.stdout
```

Por ejemplo:

```python
import subprocess

resultado = subprocess.run(
    ["ipconfig"],
    capture_output=True,
    text=True
)

configuracion = resultado.stdout

print("CONFIGURACIÓN DE RED")
print("====================")
print(configuracion)
```

---

### Buscar información dentro de la salida

Como `stdout` contiene texto, podemos utilizar las operaciones habituales de cadenas.

Por ejemplo:

```python
import subprocess

resultado = subprocess.run(
    ["ipconfig"],
    capture_output=True,
    text=True
)

configuracion = resultado.stdout

if "IPv4" in configuracion:
    print("Se ha encontrado información IPv4.")
else:
    print("No se ha encontrado información IPv4.")
```

Aquí aparece una idea fundamental:

```text
COMANDO DEL SISTEMA
        ↓
      stdout
        ↓
   cadena de texto
        ↓
 Python la analiza
        ↓
 toma una decisión
```

Ya no estamos utilizando `subprocess` únicamente para mostrar comandos.

Estamos empezando a **automatizar su análisis**.

---

### Procesar la salida línea a línea

También podemos dividir la salida mediante:

```python
splitlines()
```

Por ejemplo:

```python
import subprocess

resultado = subprocess.run(
    ["ipconfig"],
    capture_output=True,
    text=True
)

for linea in resultado.stdout.splitlines():
    print(linea)
```

Cada línea puede analizarse individualmente.

Podemos mostrar únicamente las que contengan determinadas palabras:

```python
import subprocess

resultado = subprocess.run(
    ["ipconfig"],
    capture_output=True,
    text=True
)

for linea in resultado.stdout.splitlines():

    if "IPv4" in linea:
        print(linea.strip())
```

Dependiendo de la configuración del ordenador, obtendremos una o varias líneas correspondientes a direcciones IPv4.

!!! warning "Idioma del sistema operativo"

    El texto producido por algunos comandos depende del idioma de Windows.

    Por ejemplo, determinados nombres mostrados por `ipconfig` pueden variar entre un Windows configurado en español y otro configurado en inglés.

    Por tanto, buscar palabras concretas dentro de la salida puede hacer que un script dependa del idioma del sistema.

Más adelante veremos otras formas de obtener y procesar información de red.

---

## 7. Analizar el resultado de `ping`

Uno de los usos más interesantes de `subprocess` en administración de redes consiste en comprobar si otro equipo responde.

Podemos ejecutar:

```powershell
ping -n 2 127.0.0.1
```

Ahora vamos a capturar el resultado.

Crea:

```text
capturar_ping.py
```

Escribe:

```python
import subprocess

resultado = subprocess.run(
    ["ping", "-n", "2", "127.0.0.1"],
    capture_output=True,
    text=True
)

print(resultado.stdout)
```

Ejecuta:

```powershell
python capturar_ping.py
```

Python almacenará toda la respuesta del comando en:

```python
resultado.stdout
```

---

### Utilizar el código de retorno de `ping`

Podemos comprobar el código de retorno:

```python
import subprocess

resultado = subprocess.run(
    ["ping", "-n", "2", "127.0.0.1"],
    capture_output=True,
    text=True
)

print(f"Código de retorno: {resultado.returncode}")
```

Ahora podemos utilizar una condición:

```python
import subprocess

resultado = subprocess.run(
    ["ping", "-n", "2", "127.0.0.1"],
    capture_output=True,
    text=True
)

if resultado.returncode == 0:
    print("El equipo responde.")
else:
    print("El equipo no responde.")
```

Resultado esperado para:

```text
127.0.0.1
```

será:

```text
El equipo responde.
```

---

### Solicitar la dirección al usuario

Vamos a convertir el programa en una pequeña herramienta.

Crea:

```text
comprobar_equipo.py
```

Escribe:

```python
import subprocess

direccion = input("Introduce una dirección IP o nombre de equipo: ")

resultado = subprocess.run(
    ["ping", "-n", "2", direccion],
    capture_output=True,
    text=True
)

if resultado.returncode == 0:
    print(f"{direccion} responde.")
else:
    print(f"{direccion} no responde.")
```

Podemos probar:

```text
Introduce una dirección IP o nombre de equipo: 127.0.0.1
```

Resultado:

```text
127.0.0.1 responde.
```

También podemos probar con la dirección IP de nuestra puerta de enlace o con otro equipo de nuestra red.

!!! tip "Primer script de diagnóstico"

    Este pequeño programa ya constituye una herramienta básica de diagnóstico:

    ```text
    usuario introduce IP
            ↓
          Python
            ↓
           ping
            ↓
        returncode
            ↓
       responde / no responde
    ```

---

## 8. Mostrar información de diagnóstico

Vamos a combinar varios elementos.

Crea:

```text
diagnostico_ping.py
```

Escribe:

```python
import subprocess

direccion = input("Dirección IP o nombre del equipo: ")

print()
print(f"Comprobando {direccion}...")
print()

resultado = subprocess.run(
    ["ping", "-n", "2", direccion],
    capture_output=True,
    text=True
)

print(f"Código de retorno: {resultado.returncode}")

if resultado.returncode == 0:

    print("Estado: RESPONDE")

    print()
    print("Resultado del ping:")
    print("-------------------")
    print(resultado.stdout)

else:

    print("Estado: NO RESPONDE")

    if resultado.stderr:
        print()
        print("Error:")
        print(resultado.stderr)
```

Ahora nuestro programa utiliza:

```text
input()
   ↓
subprocess.run()
   ↓
capture_output
   ↓
stdout / stderr
   ↓
returncode
   ↓
if / else
   ↓
diagnóstico
```

Estamos combinando conocimientos de Python con herramientas reales del sistema operativo.

---

## 9. Guardar el resultado de un comando

En el capítulo anterior aprendimos a generar archivos.

Ahora podemos combinar ambas técnicas:

```text
COMANDO
   ↓
subprocess
   ↓
stdout
   ↓
archivo
```

Crea:

```text
guardar_ipconfig.py
```

Primero crea dentro de:

```text
practicas/capitulo2/
```

una carpeta:

```text
resultados
```

La estructura será:

```text
capitulo2/
├── programas/
└── resultados/
```

Ahora escribe:

```python
import subprocess
from pathlib import Path

directorio_programa = Path(__file__).resolve().parent
directorio_capitulo = directorio_programa.parent

archivo_salida = directorio_capitulo / "resultados" / "ipconfig.txt"

resultado = subprocess.run(
    ["ipconfig"],
    capture_output=True,
    text=True
)

if resultado.returncode == 0:

    archivo_salida.write_text(
        resultado.stdout,
        encoding="utf-8"
    )

    print("Resultado guardado correctamente.")
    print(f"Archivo: {archivo_salida}")

else:

    print("No se ha podido ejecutar ipconfig.")
```

Después de ejecutar:

```powershell
python guardar_ipconfig.py
```

se generará:

```text
resultados/
└── ipconfig.txt
```

Acabamos de combinar dos capítulos:

```text
CAPÍTULO 1
Archivos + pathlib
       │
       │
       ▼
CAPÍTULO 2
subprocess + comandos
       │
       ▼
AUTOMATIZACIÓN
```

---

## 10. Práctica propuesta: comprobador de conectividad

Vamos a desarrollar una pequeña herramienta que compruebe varias direcciones.

Utilizaremos:

```python
direcciones = [
    "127.0.0.1",
    "192.168.1.1",
    "8.8.8.8"
]
```

El programa debe recorrer la lista y ejecutar:

```text
ping
```

sobre cada dirección.

El resultado debe tener un aspecto similar a:

```text
COMPROBACIÓN DE CONECTIVIDAD
============================

127.0.0.1       RESPONDE
192.168.1.1     RESPONDE
8.8.8.8         RESPONDE
```

Si alguna dirección no responde:

```text
192.168.1.200   NO RESPONDE
```

!!! tip "Pistas"

    Para resolverlo necesitarás:

    - Una lista.
    - Un bucle `for`.
    - `subprocess.run()`.
    - `capture_output=True`.
    - `text=True`.
    - `returncode`.
    - Una condición `if`.

!!! example "Ampliación"

    Modifica el programa para guardar los resultados en:

    ```text
    resultados/conectividad.txt
    ```

    Utiliza `pathlib` para construir la ruta.

---

## Resumen

En esta parte hemos dado un paso fundamental en el uso de `subprocess`.

Ya no nos limitamos a ejecutar comandos.

Ahora podemos:

- Capturar la salida mediante `capture_output=True`.
- Obtener texto mediante `text=True`.
- Consultar la salida estándar con `stdout`.
- Consultar la salida de error con `stderr`.
- Obtener el código de retorno mediante `returncode`.
- Utilizar `strip()` para limpiar la salida.
- Analizar la salida de comandos.
- Procesarla línea a línea mediante `splitlines()`.
- Tomar decisiones según el resultado.
- Comprobar conectividad mediante `ping`.
- Guardar resultados en archivos.

El patrón fundamental que hemos aprendido es:

```text
        COMANDO
           ↓
    subprocess.run()
           ↓
 ┌─────────┼──────────┐
 ↓         ↓          ↓
stdout   stderr   returncode
 ↓         ↓          ↓
 └──────── Python ─────┘
           ↓
     tomar decisiones
           ↓
 mostrar / guardar / procesar
```

En la siguiente parte utilizaremos este mismo mecanismo con comandos que proporcionan **información real del sistema**, como `systeminfo`, y comenzaremos a construir scripts de inventario y diagnóstico más completos.

---

## 11. Obtener información del sistema

Hasta ahora hemos utilizado principalmente:

```text
hostname
ipconfig
ping
```

Pero Windows dispone de muchas otras herramientas que podemos ejecutar desde Python.

Una de ellas es:

```powershell
systeminfo
```

Este comando proporciona información detallada sobre el equipo, como:

- Nombre del sistema.
- Versión de Windows.
- Fabricante.
- Modelo.
- Procesador.
- Memoria instalada.
- Fecha de instalación.
- Información de red.

Antes de utilizarlo desde Python, ejecútalo directamente en la terminal:

```powershell
systeminfo
```

La cantidad de información mostrada será considerable.

Nuestro objetivo será conseguir que Python pueda capturar y procesar esa información.

---

### Ejecutar `systeminfo` desde Python

Dentro de:

```text
practicas/capitulo2/programas/
```

crea:

```text
informacion_sistema.py
```

Escribe:

```python
import subprocess

resultado = subprocess.run(
    ["systeminfo"],
    capture_output=True,
    text=True
)

if resultado.returncode == 0:
    print(resultado.stdout)
else:
    print("No se ha podido obtener la información del sistema.")
    print(resultado.stderr)
```

Ejecuta:

```powershell
python informacion_sistema.py
```

Python ejecutará:

```text
systeminfo
```

y almacenará el resultado en:

```python
resultado.stdout
```

---

### Guardar la información obtenida

Podemos almacenar el resultado en una variable:

```python
informacion = resultado.stdout
```

Por ejemplo:

```python
import subprocess

resultado = subprocess.run(
    ["systeminfo"],
    capture_output=True,
    text=True
)

if resultado.returncode == 0:
    informacion = resultado.stdout

    print("INFORMACIÓN DEL SISTEMA")
    print("=======================")
    print(informacion)
else:
    print("Error al ejecutar systeminfo.")
```

El contenido de `informacion` es una cadena de texto que podemos posteriormente:

```text
mostrar
analizar
buscar
guardar
```

---

## 12. Buscar información concreta en la salida

Normalmente no necesitaremos mostrar toda la información generada por un comando.

Podemos procesarla línea a línea utilizando:

```python
splitlines()
```

Por ejemplo:

```python
import subprocess

resultado = subprocess.run(
    ["systeminfo"],
    capture_output=True,
    text=True
)

if resultado.returncode == 0:

    for linea in resultado.stdout.splitlines():
        print(linea)
```

Cada iteración del bucle contiene una línea diferente.

Esto nos permite buscar información concreta.

---

### Buscar una palabra

Por ejemplo:

```python
import subprocess

resultado = subprocess.run(
    ["systeminfo"],
    capture_output=True,
    text=True
)

if resultado.returncode == 0:

    for linea in resultado.stdout.splitlines():

        if "Windows" in linea:
            print(linea.strip())
```

Python mostrará únicamente las líneas que contengan:

```text
Windows
```

Estamos utilizando el patrón:

```text
systeminfo
    ↓
stdout
    ↓
splitlines()
    ↓
for
    ↓
if
    ↓
líneas seleccionadas
```

---

### El problema del idioma

Existe una limitación importante.

La salida de:

```powershell
systeminfo
```

depende del idioma de Windows.

Por ejemplo, determinados campos pueden aparecer con nombres diferentes en un sistema configurado en español y en otro configurado en inglés.

Por ello, un programa basado exclusivamente en buscar textos concretos como:

```python
if "Nombre del sistema operativo" in linea:
```

puede funcionar en un equipo y no hacerlo en otro configurado con un idioma diferente.

!!! warning "Scripts dependientes del idioma"

    Cuando analizamos la salida textual de un comando debemos tener en cuenta que algunos comandos muestran información traducida según el idioma del sistema operativo.

    Este tipo de scripts puede necesitar adaptaciones si se ejecuta en equipos con configuraciones diferentes.

---

## 13. Obtener el nombre del equipo

Para obtener únicamente el nombre del ordenador no necesitamos procesar toda la salida de `systeminfo`.

Ya conocemos:

```powershell
hostname
```

Podemos crear una función reutilizable.

Crea:

```text
inventario_sistema.py
```

Comenzaremos con:

```python
import subprocess


def obtener_hostname():

    resultado = subprocess.run(
        ["hostname"],
        capture_output=True,
        text=True
    )

    if resultado.returncode == 0:
        return resultado.stdout.strip()

    return "DESCONOCIDO"


nombre_equipo = obtener_hostname()

print(f"Nombre del equipo: {nombre_equipo}")
```

Observa que ahora aparece:

```python
return
```

La función obtiene el resultado del comando y devuelve el nombre del equipo.

Podemos utilizarlo posteriormente:

```python
nombre_equipo = obtener_hostname()
```

Esta forma de trabajar será muy útil porque podremos crear una función para cada dato que necesitemos obtener.

---

## 14. Ejecutar comandos de PowerShell

Hasta ahora hemos ejecutado programas directamente:

```text
hostname
ping
ipconfig
systeminfo
```

Pero también podemos pedir a Python que ejecute un comando mediante PowerShell.

Para ello podemos llamar a:

```text
powershell
```

desde `subprocess`.

Por ejemplo:

```python
import subprocess

resultado = subprocess.run(
    [
        "powershell",
        "-NoProfile",
        "-Command",
        "Get-Date"
    ],
    capture_output=True,
    text=True
)

print(resultado.stdout)
```

La opción:

```text
-NoProfile
```

indica a PowerShell que no cargue el perfil del usuario para esta ejecución.

Y:

```text
-Command
```

indica que a continuación proporcionaremos el comando que queremos ejecutar.

---

### Obtener información mediante PowerShell

PowerShell dispone de comandos especialmente útiles para administración.

Por ejemplo:

```powershell
Get-ComputerInfo
```

Podemos ejecutarlo desde Python:

```python
import subprocess

resultado = subprocess.run(
    [
        "powershell",
        "-NoProfile",
        "-Command",
        "Get-ComputerInfo"
    ],
    capture_output=True,
    text=True
)

if resultado.returncode == 0:
    print(resultado.stdout)
else:
    print("Error al obtener la información.")
    print(resultado.stderr)
```

!!! note "Python y PowerShell"

    Python no sustituye necesariamente a PowerShell.

    En administración de sistemas podemos utilizar ambos conjuntamente:

    ```text
    Python
       ↓
    PowerShell
       ↓
    Windows
       ↓
    resultado
       ↓
    Python
    ```

    Python puede encargarse de controlar el proceso, analizar los resultados y generar informes.

---

## 15. Obtener información específica con PowerShell

En lugar de obtener toda la información del sistema podemos solicitar únicamente determinados datos.

Por ejemplo, para obtener el fabricante:

```powershell
(Get-CimInstance Win32_ComputerSystem).Manufacturer
```

Desde Python:

```python
import subprocess

resultado = subprocess.run(
    [
        "powershell",
        "-NoProfile",
        "-Command",
        "(Get-CimInstance Win32_ComputerSystem).Manufacturer"
    ],
    capture_output=True,
    text=True
)

if resultado.returncode == 0:
    fabricante = resultado.stdout.strip()
    print(f"Fabricante: {fabricante}")
```

Para obtener el modelo:

```powershell
(Get-CimInstance Win32_ComputerSystem).Model
```

Desde Python:

```python
import subprocess

resultado = subprocess.run(
    [
        "powershell",
        "-NoProfile",
        "-Command",
        "(Get-CimInstance Win32_ComputerSystem).Model"
    ],
    capture_output=True,
    text=True
)

if resultado.returncode == 0:
    modelo = resultado.stdout.strip()
    print(f"Modelo: {modelo}")
```

Ahora disponemos de información mucho más concreta que la proporcionada por la salida completa de `systeminfo`.

---

## 16. Crear una función para ejecutar PowerShell

En los ejemplos anteriores estamos repitiendo muchas veces:

```python
subprocess.run(
    [
        "powershell",
        "-NoProfile",
        "-Command",
        ...
    ],
    capture_output=True,
    text=True
)
```

Podemos crear una función que simplifique esta tarea.

Crea:

```text
funciones_powershell.py
```

Escribe:

```python
import subprocess


def ejecutar_powershell(comando):

    resultado = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            comando
        ],
        capture_output=True,
        text=True
    )

    if resultado.returncode == 0:
        return resultado.stdout.strip()

    return "ERROR"


fabricante = ejecutar_powershell(
    "(Get-CimInstance Win32_ComputerSystem).Manufacturer"
)

modelo = ejecutar_powershell(
    "(Get-CimInstance Win32_ComputerSystem).Model"
)

print(f"Fabricante: {fabricante}")
print(f"Modelo: {modelo}")
```

La función:

```python
ejecutar_powershell()
```

recibe un comando:

```python
comando
```

lo ejecuta y devuelve su resultado.

Ahora podemos reutilizarla tantas veces como necesitemos.

---

## 17. Obtener información del hardware

Podemos ampliar el programa para obtener diferentes características del equipo.

Crea:

```text
inventario_hardware.py
```

Escribe:

```python
import subprocess


def ejecutar_powershell(comando):

    resultado = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            comando
        ],
        capture_output=True,
        text=True
    )

    if resultado.returncode == 0:
        return resultado.stdout.strip()

    return "ERROR"


fabricante = ejecutar_powershell(
    "(Get-CimInstance Win32_ComputerSystem).Manufacturer"
)

modelo = ejecutar_powershell(
    "(Get-CimInstance Win32_ComputerSystem).Model"
)

memoria = ejecutar_powershell(
    "[math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)"
)

procesador = ejecutar_powershell(
    "(Get-CimInstance Win32_Processor).Name"
)

print()
print("INVENTARIO DE HARDWARE")
print("======================")
print(f"Fabricante: {fabricante}")
print(f"Modelo: {modelo}")
print(f"Procesador: {procesador}")
print(f"Memoria RAM: {memoria} GB")
```

Obtendremos un resultado similar a:

```text
INVENTARIO DE HARDWARE
======================
Fabricante: Dell Inc.
Modelo: OptiPlex 7090
Procesador: Intel(R) Core(TM) i5-10500 CPU @ 3.10GHz
Memoria RAM: 16 GB
```

Los valores dependerán del ordenador utilizado.

---

## 18. Obtener información de Windows

También podemos consultar información del sistema operativo.

Por ejemplo:

```powershell
(Get-CimInstance Win32_OperatingSystem).Caption
```

y:

```powershell
(Get-CimInstance Win32_OperatingSystem).Version
```

Podemos añadir al programa:

```python
sistema = ejecutar_powershell(
    "(Get-CimInstance Win32_OperatingSystem).Caption"
)

version = ejecutar_powershell(
    "(Get-CimInstance Win32_OperatingSystem).Version"
)
```

Después:

```python
print(f"Sistema operativo: {sistema}")
print(f"Versión: {version}")
```

Nuestro inventario empieza a contener información realmente útil.

---

## 19. Generar un informe del sistema

Vamos a combinar nuevamente lo aprendido en el capítulo 1 con `subprocess`.

Queremos generar automáticamente:

```text
practicas/capitulo2/resultados/informe_sistema.txt
```

Crea:

```text
generar_informe_sistema.py
```

Escribe:

```python
import subprocess
from pathlib import Path


def ejecutar_powershell(comando):

    resultado = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            comando
        ],
        capture_output=True,
        text=True
    )

    if resultado.returncode == 0:
        return resultado.stdout.strip()

    return "ERROR"


directorio_programa = Path(__file__).resolve().parent
directorio_capitulo = directorio_programa.parent

directorio_resultados = directorio_capitulo / "resultados"

directorio_resultados.mkdir(
    parents=True,
    exist_ok=True
)

archivo_informe = directorio_resultados / "informe_sistema.txt"


hostname = ejecutar_powershell(
    "$env:COMPUTERNAME"
)

fabricante = ejecutar_powershell(
    "(Get-CimInstance Win32_ComputerSystem).Manufacturer"
)

modelo = ejecutar_powershell(
    "(Get-CimInstance Win32_ComputerSystem).Model"
)

procesador = ejecutar_powershell(
    "(Get-CimInstance Win32_Processor).Name"
)

memoria = ejecutar_powershell(
    "[math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)"
)

sistema = ejecutar_powershell(
    "(Get-CimInstance Win32_OperatingSystem).Caption"
)

version = ejecutar_powershell(
    "(Get-CimInstance Win32_OperatingSystem).Version"
)


informe = f"""INFORME DEL SISTEMA
===================

Nombre del equipo: {hostname}
Fabricante: {fabricante}
Modelo: {modelo}
Procesador: {procesador}
Memoria RAM: {memoria} GB
Sistema operativo: {sistema}
Versión: {version}
"""


archivo_informe.write_text(
    informe,
    encoding="utf-8"
)

print(informe)

print("Informe guardado en:")
print(archivo_informe)
```

Ejecuta:

```powershell
python generar_informe_sistema.py
```

El programa:

1. Obtendrá automáticamente la información.
2. La almacenará en variables.
3. Construirá un informe.
4. Lo mostrará en pantalla.
5. Lo guardará en un archivo.

El proceso completo es:

```text
Windows
   ↑
PowerShell
   ↑
subprocess
   │
   ▼
Python
   │
   ├── hostname
   ├── fabricante
   ├── modelo
   ├── procesador
   ├── memoria
   └── sistema operativo
           │
           ▼
      informe_sistema.txt
```

Este programa ya constituye un ejemplo sencillo de **automatización de inventario de sistemas**.

---

## 20. Práctica propuesta: inventario automático

Crea:

```text
inventario_completo.py
```

El programa debe obtener automáticamente:

```text
Nombre del equipo
Fabricante
Modelo
Procesador
Memoria RAM
Sistema operativo
Versión
```

Debe mostrar el resultado con este formato:

```text
================================
     INVENTARIO DEL EQUIPO
================================

Nombre:
Fabricante:
Modelo:
Procesador:
Memoria RAM:
Sistema operativo:
Versión:

================================
```

Después debe guardar la información en:

```text
resultados/inventario.txt
```

!!! tip "Pistas"

    Para realizar la práctica necesitarás combinar:

    - `subprocess.run()`
    - PowerShell
    - `capture_output=True`
    - `text=True`
    - `stdout`
    - `returncode`
    - funciones
    - `pathlib`
    - `write_text()`

!!! example "Ampliación"

    Añade al inventario la fecha y hora en la que se ha generado.

    Puedes investigar el comando PowerShell:

    ```powershell
    Get-Date
    ```

---

## Resumen

En esta parte hemos aprendido a utilizar `subprocess` para obtener información real del ordenador.

Hemos trabajado con:

- `systeminfo`.
- Procesamiento línea a línea de la salida.
- Búsqueda de información dentro de `stdout`.
- Ejecución de comandos de PowerShell desde Python.
- `Get-ComputerInfo`.
- `Get-CimInstance`.
- Obtención del fabricante y modelo.
- Obtención del procesador.
- Obtención de la memoria RAM.
- Obtención del sistema operativo.
- Creación de funciones reutilizables.
- Generación automática de informes.

Nuestro script ya puede seguir el proceso:

```text
OBTENER
   ↓
CAPTURAR
   ↓
PROCESAR
   ↓
ORGANIZAR
   ↓
GUARDAR
```

Estamos pasando de pequeños ejemplos de `subprocess` a auténticos **scripts de administración de sistemas**.

En la siguiente parte profundizaremos en el **tratamiento de errores durante la ejecución de comandos**, para evitar que nuestros programas fallen cuando un comando no existe, tarda demasiado en responder o devuelve un resultado inesperado.

---

## 21. Control de errores en `subprocess`

Hasta ahora hemos supuesto que los comandos que ejecutamos funcionan correctamente.

Por ejemplo:

```python
import subprocess

resultado = subprocess.run(
    ["hostname"],
    capture_output=True,
    text=True
)

print(resultado.stdout)
```

Pero en un script real pueden producirse muchos problemas:

- El comando puede no existir.
- Podemos escribir incorrectamente su nombre.
- El comando puede devolver un error.
- Un equipo remoto puede no responder.
- El comando puede tardar demasiado.
- Podemos proporcionar argumentos incorrectos.

Un script de administración debe estar preparado para estas situaciones.

El objetivo será pasar de:

```text
ERROR
  ↓
el programa termina
```

a:

```text
ERROR
  ↓
Python lo detecta
  ↓
identifica el problema
  ↓
muestra un mensaje
  ↓
continúa de forma controlada
```

---

### Excepciones en Python

Cuando durante la ejecución ocurre un problema, Python puede generar una **excepción**.

Podemos controlar determinadas excepciones mediante:

```python
try:
```

y:

```python
except:
```

La estructura básica es:

```python
try:
    # operación que puede producir un error

except:
    # qué hacer si se produce
```

Por ejemplo:

```python
try:
    numero = int(input("Introduce un número: "))

except ValueError:
    print("El valor introducido no es un número válido.")
```

Durante este capítulo aplicaremos este mecanismo a `subprocess`.

---

## 22. Comandos que no existen

Vamos a provocar deliberadamente un error.

Crea:

```text
comando_inexistente.py
```

Escribe:

```python
import subprocess

subprocess.run(["comando_que_no_existe"])
```

Ejecuta:

```powershell
python comando_inexistente.py
```

Python mostrará un error.

El problema es que Windows no puede localizar el programa que hemos solicitado.

En este caso Python genera:

```text
FileNotFoundError
```

Podemos controlar esta excepción.

Modifica el programa:

```python
import subprocess

try:

    subprocess.run(
        ["comando_que_no_existe"]
    )

except FileNotFoundError:

    print("ERROR: el comando no existe.")
```

Ahora el programa no termina mostrando una larga traza de error.

Obtendremos simplemente:

```text
ERROR: el comando no existe.
```

!!! note "FileNotFoundError"

    `FileNotFoundError` puede producirse cuando Python intenta ejecutar un programa que el sistema operativo no puede localizar.

---

### Mostrar el nombre del comando

Podemos hacer el programa más útil:

```python
import subprocess

comando = "comando_que_no_existe"

try:

    subprocess.run([comando])

except FileNotFoundError:

    print(f"ERROR: no se encuentra el comando '{comando}'.")
```

Resultado:

```text
ERROR: no se encuentra el comando 'comando_que_no_existe'.
```

---

## 23. Detectar errores con `check=True`

Hasta ahora hemos utilizado:

```python
resultado.returncode
```

para comprobar manualmente si un comando ha terminado correctamente.

Existe otra posibilidad.

Podemos utilizar:

```python
check=True
```

Por ejemplo:

```python
import subprocess

resultado = subprocess.run(
    ["hostname"],
    capture_output=True,
    text=True,
    check=True
)

print(resultado.stdout)
```

Si el comando finaliza con código:

```text
0
```

el programa continúa normalmente.

Pero si el comando termina con un código distinto de cero, `subprocess.run()` genera una excepción:

```text
CalledProcessError
```

Podemos controlarla mediante:

```python
try:
```

y:

```python
except subprocess.CalledProcessError:
```

---

### Ejemplo con `CalledProcessError`

Crea:

```text
controlar_returncode.py
```

Escribe:

```python
import subprocess

try:

    resultado = subprocess.run(
        ["ping", "-n", "1", "direccion-inexistente.invalid"],
        capture_output=True,
        text=True,
        check=True
    )

    print(resultado.stdout)

except subprocess.CalledProcessError:

    print("El comando se ha ejecutado, pero ha terminado con error.")
```

La diferencia con `FileNotFoundError` es importante.

```text
FileNotFoundError
        ↓
el programa solicitado
no se ha podido iniciar


CalledProcessError
        ↓
el programa se ha ejecutado
        ↓
ha terminado con un código
distinto de cero
```

!!! tip "Diferencia fundamental"

    `FileNotFoundError` indica que Python no ha podido localizar o iniciar el programa solicitado.

    `CalledProcessError` aparece con `check=True` cuando el programa sí se ha ejecutado, pero ha finalizado con un código de retorno distinto de cero.

---

## 24. Obtener información del error

Cuando capturamos:

```python
subprocess.CalledProcessError
```

podemos guardar la excepción en una variable:

```python
except subprocess.CalledProcessError as error:
```

Esto permite consultar información adicional.

Por ejemplo:

```python
import subprocess

try:

    resultado = subprocess.run(
        ["ping", "-n", "1", "direccion-inexistente.invalid"],
        capture_output=True,
        text=True,
        check=True
    )

    print(resultado.stdout)

except subprocess.CalledProcessError as error:

    print("El comando ha terminado con error.")
    print(f"Código de retorno: {error.returncode}")
```

También podemos consultar:

```python
error.stdout
```

y:

```python
error.stderr
```

si hemos utilizado:

```python
capture_output=True
```

Por ejemplo:

```python
except subprocess.CalledProcessError as error:

    print(f"Código: {error.returncode}")

    if error.stdout:
        print("Salida:")
        print(error.stdout)

    if error.stderr:
        print("Error:")
        print(error.stderr)
```

Esto proporciona mucha más información para diagnosticar qué ha ocurrido.

---

## 25. Limitar el tiempo de ejecución

Otro problema habitual es que un comando tarde demasiado.

`subprocess.run()` permite establecer un tiempo máximo mediante:

```python
timeout=
```

Por ejemplo:

```python
import subprocess

resultado = subprocess.run(
    ["ping", "-n", "2", "127.0.0.1"],
    capture_output=True,
    text=True,
    timeout=5
)
```

Aquí indicamos:

```python
timeout=5
```

es decir:

> Permite que el comando se ejecute durante un máximo aproximado de 5 segundos.

Si supera ese tiempo, Python genera:

```text
TimeoutExpired
```

---

### Controlar `TimeoutExpired`

Crea:

```text
controlar_timeout.py
```

Escribe:

```python
import subprocess

direccion = input("Dirección IP o nombre del equipo: ")

try:

    resultado = subprocess.run(
        ["ping", "-n", "2", direccion],
        capture_output=True,
        text=True,
        timeout=5
    )

    if resultado.returncode == 0:
        print(f"{direccion}: RESPONDE")
    else:
        print(f"{direccion}: NO RESPONDE")

except subprocess.TimeoutExpired:

    print("ERROR: el comando ha superado el tiempo máximo permitido.")
```

Ahora nuestro programa tiene un límite de tiempo.

Esto resulta especialmente importante en scripts que ejecutan muchos comandos consecutivamente.

!!! note "El timeout pertenece al proceso"

    `timeout` limita el tiempo que Python permite que continúe la ejecución del proceso externo.

    No debe confundirse necesariamente con los tiempos de espera internos que pueda utilizar el propio comando.

---

## 26. Controlar varios tipos de error

Un mismo programa puede controlar diferentes excepciones.

Por ejemplo:

```python
import subprocess

comando = ["ping", "-n", "2", "127.0.0.1"]

try:

    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True,
        timeout=5,
        check=True
    )

    print("Comando ejecutado correctamente.")
    print(resultado.stdout)

except FileNotFoundError:

    print("ERROR: no se encuentra el programa solicitado.")

except subprocess.TimeoutExpired:

    print("ERROR: el comando ha tardado demasiado.")

except subprocess.CalledProcessError as error:

    print("ERROR: el comando ha finalizado incorrectamente.")
    print(f"Código de retorno: {error.returncode}")
```

Nuestro script distingue ahora entre tres situaciones:

```text
              EJECUTAR COMANDO
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
 no existe       tarda demasiado  termina
                                 con error
        │            │            │
        ▼            ▼            ▼
FileNotFound   TimeoutExpired  CalledProcessError
```

---

## 27. Crear una función robusta para ejecutar comandos

Como vamos a ejecutar muchos comandos durante el curso, podemos crear una función reutilizable.

Crea:

```text
ejecutar_comando.py
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
            timeout=10,
            check=True
        )

        return resultado.stdout.strip()

    except FileNotFoundError:

        return "ERROR: comando no encontrado"

    except subprocess.TimeoutExpired:

        return "ERROR: tiempo de ejecución superado"

    except subprocess.CalledProcessError as error:

        return f"ERROR: código de retorno {error.returncode}"


resultado = ejecutar_comando(
    ["hostname"]
)

print(resultado)
```

La función recibe una lista:

```python
["hostname"]
```

o:

```python
["ping", "-n", "2", "127.0.0.1"]
```

y devuelve un resultado.

Podemos probar:

```python
print(
    ejecutar_comando(
        ["hostname"]
    )
)

print(
    ejecutar_comando(
        ["ping", "-n", "2", "127.0.0.1"]
    )
)
```

Estamos empezando a construir nuestras propias **herramientas reutilizables de administración**.

---

## 28. `check=True` o `returncode`

Hasta ahora hemos utilizado dos estrategias.

### Comprobar manualmente `returncode`

```python
resultado = subprocess.run(
    comando,
    capture_output=True,
    text=True
)

if resultado.returncode == 0:
    print("Correcto")
else:
    print("Error")
```

### Utilizar `check=True`

```python
try:

    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True,
        check=True
    )

except subprocess.CalledProcessError:

    print("Error")
```

Ambas formas son válidas.

La primera nos permite trabajar directamente con:

```python
returncode
```

La segunda integra los errores dentro del mecanismo de excepciones de Python.

Durante el curso utilizaremos una u otra dependiendo de lo que queramos conseguir.

!!! tip "Criterio práctico"

    Si necesitamos analizar directamente diferentes códigos de retorno, puede resultar cómodo utilizar `returncode`.

    Si queremos tratar una ejecución incorrecta como una excepción, podemos utilizar `check=True`.

---

## 29. Evitar `shell=True` cuando no sea necesario

Es posible encontrar ejemplos de `subprocess` como:

```python
subprocess.run(
    "ping 127.0.0.1",
    shell=True
)
```

Sin embargo, durante este curso utilizaremos preferentemente:

```python
subprocess.run(
    ["ping", "127.0.0.1"]
)
```

cuando sea posible.

La segunda forma separa claramente:

```text
comando
argumentos
```

y evita depender innecesariamente de un intérprete de comandos adicional.

!!! warning "Datos introducidos por el usuario"

    Debemos tener especial cuidado cuando construimos comandos utilizando información introducida por un usuario.

    No debemos insertar directamente texto no controlado dentro de comandos ejecutados mediante un shell.

    En nuestros ejemplos utilizaremos listas de argumentos siempre que sea posible.

---

## 30. Mejorar nuestro comprobador de conectividad

Vamos a recuperar el programa:

```text
comprobar_equipo.py
```

y crear una versión más robusta.

Crea:

```text
comprobar_equipo_seguro.py
```

Escribe:

```python
import subprocess


direccion = input(
    "Introduce una dirección IP o nombre de equipo: "
)

try:

    resultado = subprocess.run(
        [
            "ping",
            "-n",
            "2",
            direccion
        ],
        capture_output=True,
        text=True,
        timeout=10
    )

    if resultado.returncode == 0:

        print()
        print(f"{direccion}: RESPONDE")

    else:

        print()
        print(f"{direccion}: NO RESPONDE")

except FileNotFoundError:

    print("ERROR: no se encuentra el comando ping.")

except subprocess.TimeoutExpired:

    print("ERROR: la comprobación ha tardado demasiado.")
```

Ahora el programa contempla varias situaciones sin finalizar de forma inesperada.

---

## 31. Práctica propuesta: ejecutor controlado

Crea:

```text
ejecutor_controlado.py
```

El programa debe permitir seleccionar:

```text
================================
     EJECUTOR DE COMANDOS
================================

1. Nombre del equipo
2. Configuración de red
3. Información del sistema
4. Comprobar conectividad
5. Salir
```

Las opciones ejecutarán:

```text
1 → hostname
2 → ipconfig
3 → systeminfo
4 → ping
```

Para la opción 4 deberá solicitar:

```text
Dirección IP o nombre:
```

Todos los comandos deben ejecutarse mediante:

```python
subprocess.run()
```

y el programa deberá controlar:

- Comandos inexistentes.
- Tiempo máximo de ejecución.
- Código de retorno.

!!! tip "Pistas"

    Puedes crear una función:

    ```python
    def ejecutar_comando(comando):
    ```

    y reutilizarla para las diferentes opciones.

    Utiliza:

    ```python
    try
    except
    ```

    para controlar los errores.

!!! example "Ampliación"

    Guarda cada ejecución en:

    ```text
    resultados/historial.txt
    ```

    El archivo podría contener:

    ```text
    hostname -> CORRECTO
    ipconfig -> CORRECTO
    ping 192.168.1.1 -> CORRECTO
    ping 192.168.1.200 -> ERROR
    ```

    Utiliza los conocimientos del capítulo 1 para añadir información al archivo sin borrar el historial anterior.

---

## Resumen

En esta parte hemos aprendido que ejecutar un comando correctamente no consiste únicamente en llamar a `subprocess.run()`.

Un script robusto también debe estar preparado para los errores.

Hemos trabajado con:

- `try`.
- `except`.
- `FileNotFoundError`.
- `check=True`.
- `subprocess.CalledProcessError`.
- `subprocess.TimeoutExpired`.
- `timeout`.
- `returncode`.
- `stdout`.
- `stderr`.
- Funciones reutilizables para ejecutar comandos.
- Ejecución sin `shell=True` cuando no es necesario.

Nuestro modelo de ejecución es ahora:

```text
             COMANDO
                │
                ▼
        subprocess.run()
                │
       ┌────────┼─────────┐
       │        │         │
       ▼        ▼         ▼
    correcto   error    timeout
       │        │         │
       ▼        ▼         ▼
    stdout   excepción  excepción
       │        │         │
       └────────┼─────────┘
                ▼
             PYTHON
                │
       respuesta controlada
```

Esto permite construir scripts mucho más fiables y adecuados para tareas de administración.

En la siguiente parte integraremos todo lo aprendido en el capítulo para construir una **herramienta de diagnóstico del sistema y de la red**, que ejecutará varios comandos, analizará sus resultados y generará automáticamente un informe.

---

## 32. Práctica final: herramienta de diagnóstico

Para finalizar el capítulo vamos a desarrollar una pequeña herramienta de **diagnóstico de sistemas y redes**.

El objetivo es integrar en un único programa los principales conceptos estudiados:

- Ejecución de comandos mediante `subprocess`.
- Captura de `stdout` y `stderr`.
- Comprobación de `returncode`.
- Control de excepciones.
- Uso de funciones.
- Ejecución de comandos de Windows.
- Pruebas de conectividad.
- Gestión de rutas mediante `pathlib`.
- Generación automática de informes.

El programa mostrará un menú:

```text
====================================
     DIAGNÓSTICO DEL SISTEMA
====================================

1. Información del equipo
2. Configuración de red
3. Comprobar conectividad
4. Generar informe completo
5. Salir

Selecciona una opción:
```

Vamos a construirlo paso a paso.

---

### Preparar la estructura

Dentro de:

```text
practicas/capitulo2/
```

utilizaremos:

```text
capitulo2/
├── programas/
│   └── diagnostico_final.py
│
└── resultados/
```

Si la carpeta `resultados` no existe, nuestro programa deberá crearla automáticamente.

---

### Preparar las importaciones

Crea:

```text
diagnostico_final.py
```

Comenzaremos con:

```python
import subprocess
from pathlib import Path
```

Necesitamos `subprocess` para ejecutar los comandos y `Path` para gestionar las rutas.

Ahora obtenemos la ubicación del programa:

```python
DIRECTORIO_PROGRAMA = Path(__file__).resolve().parent
DIRECTORIO_CAPITULO = DIRECTORIO_PROGRAMA.parent

DIRECTORIO_RESULTADOS = DIRECTORIO_CAPITULO / "resultados"
```

Creamos el directorio si no existe:

```python
DIRECTORIO_RESULTADOS.mkdir(
    parents=True,
    exist_ok=True
)
```

---

## 33. Crear una función para ejecutar comandos

Vamos a centralizar la ejecución de comandos en una función.

```python
def ejecutar_comando(comando):

    try:

        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=15
        )

        return resultado

    except FileNotFoundError:

        print("ERROR: no se encuentra el comando.")
        return None

    except subprocess.TimeoutExpired:

        print("ERROR: el comando ha tardado demasiado.")
        return None
```

La función recibe una lista como:

```python
["hostname"]
```

o:

```python
["ping", "-n", "2", "192.168.1.1"]
```

y devuelve el resultado de `subprocess.run()`.

Si ocurre un problema grave durante la ejecución, devuelve:

```python
None
```

---

## 34. Obtener información básica del equipo

Vamos a crear una función que obtenga información del ordenador.

```python
def informacion_equipo():

    resultado_hostname = ejecutar_comando(
        ["hostname"]
    )

    resultado_systeminfo = ejecutar_comando(
        ["systeminfo"]
    )

    informacion = ""

    informacion += "INFORMACIÓN DEL EQUIPO\n"
    informacion += "======================\n\n"

    if resultado_hostname is not None:

        if resultado_hostname.returncode == 0:
            informacion += (
                "Nombre del equipo: "
                + resultado_hostname.stdout.strip()
                + "\n\n"
            )

    if resultado_systeminfo is not None:

        if resultado_systeminfo.returncode == 0:
            informacion += resultado_systeminfo.stdout

    return informacion
```

La función combina:

```text
hostname
+
systeminfo
```

y devuelve toda la información en una cadena.

Podemos probarla temporalmente:

```python
print(informacion_equipo())
```

---

## 35. Obtener la configuración de red

Ahora creamos:

```python
def informacion_red():

    resultado = ejecutar_comando(
        ["ipconfig"]
    )

    informacion = ""

    informacion += "CONFIGURACIÓN DE RED\n"
    informacion += "====================\n\n"

    if resultado is None:
        informacion += "No se ha podido ejecutar ipconfig.\n"

    elif resultado.returncode == 0:
        informacion += resultado.stdout

    else:
        informacion += "Error al obtener la configuración de red.\n"

    return informacion
```

Esta función ejecuta:

```text
ipconfig
```

y devuelve el resultado.

---

## 36. Comprobar la conectividad

Nuestra tercera función realizará una prueba de conectividad.

```python
def comprobar_conectividad():

    direccion = input(
        "Dirección IP o nombre del equipo: "
    )

    resultado = ejecutar_comando(
        [
            "ping",
            "-n",
            "2",
            direccion
        ]
    )

    if resultado is None:
        return "No se ha podido realizar la comprobación."

    if resultado.returncode == 0:
        return f"{direccion}: RESPONDE"

    return f"{direccion}: NO RESPONDE"
```

Ahora podemos introducir, por ejemplo:

```text
127.0.0.1
```

o la dirección de nuestra puerta de enlace.

El programa ejecutará:

```powershell
ping -n 2 DIRECCION
```

y analizará el código de retorno.

---

## 37. Generar un informe completo

Vamos a utilizar las funciones anteriores para crear automáticamente un informe.

Añade:

```python
def generar_informe():

    archivo_informe = (
        DIRECTORIO_RESULTADOS
        / "diagnostico_sistema.txt"
    )

    contenido = ""

    contenido += "DIAGNÓSTICO DEL SISTEMA\n"
    contenido += "=======================\n\n"

    contenido += informacion_equipo()

    contenido += "\n\n"

    contenido += informacion_red()

    archivo_informe.write_text(
        contenido,
        encoding="utf-8"
    )

    print()
    print("Informe generado correctamente.")
    print()
    print("Archivo:")
    print(archivo_informe)
```

Cuando ejecutemos esta función se creará:

```text
resultados/
└── diagnostico_sistema.txt
```

El archivo contendrá información del sistema y de la configuración de red.

---

## 38. Crear el menú principal

Ahora podemos crear el menú.

Añade:

```python
while True:

    print()
    print("====================================")
    print("     DIAGNÓSTICO DEL SISTEMA")
    print("====================================")
    print()
    print("1. Información del equipo")
    print("2. Configuración de red")
    print("3. Comprobar conectividad")
    print("4. Generar informe completo")
    print("5. Salir")
    print()

    opcion = input("Selecciona una opción: ")

    if opcion == "1":

        print()
        print(informacion_equipo())

    elif opcion == "2":

        print()
        print(informacion_red())

    elif opcion == "3":

        print()
        print(comprobar_conectividad())

    elif opcion == "4":

        generar_informe()

    elif opcion == "5":

        print()
        print("Programa finalizado.")
        break

    else:

        print()
        print("Opción incorrecta.")
```

El:

```python
while True:
```

mantendrá el programa en ejecución hasta seleccionar:

```text
5. Salir
```

---

## 39. Programa completo

Nuestro archivo:

```text
diagnostico_final.py
```

queda:

```python
import subprocess
from pathlib import Path


DIRECTORIO_PROGRAMA = Path(__file__).resolve().parent
DIRECTORIO_CAPITULO = DIRECTORIO_PROGRAMA.parent

DIRECTORIO_RESULTADOS = DIRECTORIO_CAPITULO / "resultados"

DIRECTORIO_RESULTADOS.mkdir(
    parents=True,
    exist_ok=True
)


def ejecutar_comando(comando):

    try:

        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=15
        )

        return resultado

    except FileNotFoundError:

        print("ERROR: no se encuentra el comando.")
        return None

    except subprocess.TimeoutExpired:

        print("ERROR: el comando ha tardado demasiado.")
        return None


def informacion_equipo():

    resultado_hostname = ejecutar_comando(
        ["hostname"]
    )

    resultado_systeminfo = ejecutar_comando(
        ["systeminfo"]
    )

    informacion = ""

    informacion += "INFORMACIÓN DEL EQUIPO\n"
    informacion += "======================\n\n"

    if resultado_hostname is not None:

        if resultado_hostname.returncode == 0:
            informacion += (
                "Nombre del equipo: "
                + resultado_hostname.stdout.strip()
                + "\n\n"
            )

    if resultado_systeminfo is not None:

        if resultado_systeminfo.returncode == 0:
            informacion += resultado_systeminfo.stdout

    return informacion


def informacion_red():

    resultado = ejecutar_comando(
        ["ipconfig"]
    )

    informacion = ""

    informacion += "CONFIGURACIÓN DE RED\n"
    informacion += "====================\n\n"

    if resultado is None:

        informacion += (
            "No se ha podido ejecutar ipconfig.\n"
        )

    elif resultado.returncode == 0:

        informacion += resultado.stdout

    else:

        informacion += (
            "Error al obtener la configuración de red.\n"
        )

    return informacion


def comprobar_conectividad():

    direccion = input(
        "Dirección IP o nombre del equipo: "
    )

    resultado = ejecutar_comando(
        [
            "ping",
            "-n",
            "2",
            direccion
        ]
    )

    if resultado is None:
        return "No se ha podido realizar la comprobación."

    if resultado.returncode == 0:
        return f"{direccion}: RESPONDE"

    return f"{direccion}: NO RESPONDE"


def generar_informe():

    archivo_informe = (
        DIRECTORIO_RESULTADOS
        / "diagnostico_sistema.txt"
    )

    contenido = ""

    contenido += "DIAGNÓSTICO DEL SISTEMA\n"
    contenido += "=======================\n\n"

    contenido += informacion_equipo()

    contenido += "\n\n"

    contenido += informacion_red()

    archivo_informe.write_text(
        contenido,
        encoding="utf-8"
    )

    print()
    print("Informe generado correctamente.")
    print()
    print("Archivo:")
    print(archivo_informe)


while True:

    print()
    print("====================================")
    print("     DIAGNÓSTICO DEL SISTEMA")
    print("====================================")
    print()
    print("1. Información del equipo")
    print("2. Configuración de red")
    print("3. Comprobar conectividad")
    print("4. Generar informe completo")
    print("5. Salir")
    print()

    opcion = input("Selecciona una opción: ")

    if opcion == "1":

        print()
        print(informacion_equipo())

    elif opcion == "2":

        print()
        print(informacion_red())

    elif opcion == "3":

        print()
        print(comprobar_conectividad())

    elif opcion == "4":

        generar_informe()

    elif opcion == "5":

        print()
        print("Programa finalizado.")
        break

    else:

        print()
        print("Opción incorrecta.")
```

---

## 40. Probar la herramienta

No debemos considerar terminada una herramienta simplemente porque no aparezcan errores de Python.

Debemos comprobar cada una de sus funciones.

### Prueba 1 — Información del equipo

Selecciona:

```text
1
```

Comprueba que aparece:

- El nombre del ordenador.
- La información proporcionada por `systeminfo`.

### Prueba 2 — Configuración de red

Selecciona:

```text
2
```

Debe aparecer la información proporcionada por:

```text
ipconfig
```

### Prueba 3 — Loopback

Selecciona:

```text
3
```

Introduce:

```text
127.0.0.1
```

Deberíamos obtener:

```text
127.0.0.1: RESPONDE
```

### Prueba 4 — Puerta de enlace

Consulta primero:

```powershell
ipconfig
```

Localiza la dirección de:

```text
Puerta de enlace predeterminada
```

y comprueba esa dirección mediante la opción 3.

### Prueba 5 — Generar informe

Selecciona:

```text
4
```

Comprueba que se crea:

```text
resultados/diagnostico_sistema.txt
```

Abre el archivo desde VS Code y verifica su contenido.

### Prueba 6 — Salir

Selecciona:

```text
5
```

El programa debe finalizar de forma controlada.

---

## 41. Mejorar el informe con una prueba de conectividad

Actualmente nuestro informe contiene:

```text
Información del sistema
+
Configuración de red
```

Vamos a añadir una prueba automática.

Podemos comprobar la interfaz de loopback:

```text
127.0.0.1
```

Añade esta función:

```python
def probar_direccion(direccion):

    resultado = ejecutar_comando(
        [
            "ping",
            "-n",
            "2",
            direccion
        ]
    )

    if resultado is None:
        return "ERROR"

    if resultado.returncode == 0:
        return "RESPONDE"

    return "NO RESPONDE"
```

Ahora, dentro de:

```python
generar_informe()
```

podemos añadir:

```python
estado_loopback = probar_direccion(
    "127.0.0.1"
)
```

y posteriormente:

```python
contenido += "\n\n"
contenido += "PRUEBAS DE CONECTIVIDAD\n"
contenido += "=======================\n\n"
contenido += (
    f"127.0.0.1: {estado_loopback}\n"
)
```

Nuestro informe incluirá ahora:

```text
PRUEBAS DE CONECTIVIDAD
=======================

127.0.0.1: RESPONDE
```

---

## 42. Práctica de ampliación

Amplía el programa para comprobar automáticamente:

```text
127.0.0.1
```

la puerta de enlace de tu red y:

```text
8.8.8.8
```

El informe podría mostrar:

```text
PRUEBAS DE CONECTIVIDAD
=======================

Loopback:          RESPONDE
Puerta de enlace:  RESPONDE
Internet:          RESPONDE
```

!!! warning "Interpretar correctamente las pruebas"

    Que `8.8.8.8` no responda a `ping` no demuestra por sí solo que no exista conexión a Internet.

    Un equipo o una red puede bloquear mensajes ICMP.

    Los resultados de una herramienta de diagnóstico deben interpretarse teniendo en cuenta qué estamos comprobando realmente.

---

## 43. Ejercicios de consolidación

### Ejercicio 1 — Nombre del equipo

Crea un programa que ejecute:

```text
hostname
```

capture su salida y muestre:

```text
Este programa se está ejecutando en: NOMBRE
```

---

### Ejercicio 2 — Guardar `ipconfig`

Ejecuta:

```text
ipconfig
```

desde Python y guarda el resultado en:

```text
resultados/red.txt
```

Utiliza `pathlib`.

---

### Ejercicio 3 — Comprobar varias direcciones

Utiliza:

```python
direcciones = [
    "127.0.0.1",
    "192.168.1.1",
    "8.8.8.8"
]
```

Recorre la lista mediante un bucle y muestra:

```text
127.0.0.1      RESPONDE
192.168.1.1    RESPONDE
8.8.8.8        RESPONDE
```

Los resultados reales dependerán de la red utilizada.

---

### Ejercicio 4 — Controlar un comando inexistente

Intenta ejecutar:

```text
comando_inexistente
```

y controla:

```python
FileNotFoundError
```

El programa debe mostrar un mensaje comprensible y finalizar correctamente.

---

### Ejercicio 5 — Utilizar un `timeout`

Realiza una prueba mediante `ping` estableciendo:

```python
timeout=5
```

Controla:

```python
subprocess.TimeoutExpired
```

---

### Ejercicio 6 — Informe personalizado

Crea un informe que contenga únicamente:

```text
Nombre del equipo
Sistema operativo
Procesador
Memoria RAM
Configuración de red
Estado de loopback
```

Guárdalo como:

```text
resultados/mi_equipo.txt
```

---

## 44. Reto final

Crea una nueva versión:

```text
diagnostico_avanzado.py
```

con este menú:

```text
====================================
     DIAGNÓSTICO DE SISTEMA Y RED
====================================

1. Nombre del equipo
2. Información del hardware
3. Información de Windows
4. Configuración de red
5. Comprobar una dirección
6. Comprobar varias direcciones
7. Generar informe
8. Salir
```

!!! example "Condiciones"

    El programa deberá:

    - Utilizar funciones.
    - Ejecutar comandos mediante `subprocess`.
    - Capturar la salida.
    - Comprobar códigos de retorno.
    - Controlar errores.
    - Utilizar un tiempo máximo de ejecución.
    - Utilizar `pathlib`.
    - Crear automáticamente la carpeta de resultados.
    - Generar al menos un archivo de informe.

    Intenta realizar el programa utilizando únicamente los conocimientos estudiados hasta ahora.

---

## 45. Qué hemos aprendido

Durante este capítulo hemos aprendido a utilizar Python como intermediario entre nuestros programas y el sistema operativo.

Partimos de:

```python
subprocess.run(["hostname"])
```

y progresivamente hemos incorporado:

```text
subprocess.run()
       │
       ├── comandos
       ├── argumentos
       │
       ├── capture_output
       ├── text
       │
       ├── stdout
       ├── stderr
       ├── returncode
       │
       ├── timeout
       └── check
```

También hemos aprendido a controlar:

```text
FileNotFoundError
TimeoutExpired
CalledProcessError
```

y hemos utilizado comandos reales como:

```text
hostname
ipconfig
ping
systeminfo
```

Además, hemos combinado estos conocimientos con lo estudiado en el capítulo anterior:

```text
CAPÍTULO 1
Archivos y pathlib
       │
       │
       ▼
CAPÍTULO 2
Comandos y subprocess
       │
       ▼
SCRIPT DE ADMINISTRACIÓN
```

---

## 46. Conclusión

`subprocess` permite que nuestros programas Python utilicen las herramientas disponibles en el sistema operativo.

Esto abre muchas posibilidades en administración:

```text
Python
   │
   ├── ejecutar comandos
   │
   ├── obtener información
   │
   ├── comprobar conectividad
   │
   ├── detectar errores
   │
   ├── analizar resultados
   │
   └── generar informes
   │
   ▼
AUTOMATIZACIÓN
```

Ya no estamos utilizando Python únicamente para realizar cálculos o manipular archivos.

Estamos comenzando a utilizarlo para **automatizar tareas reales de administración de sistemas**.

!!! success "Capítulo completado"

    Al finalizar este capítulo debemos ser capaces de ejecutar comandos del sistema desde Python, capturar sus resultados, detectar errores y utilizar esa información para construir pequeñas herramientas de diagnóstico.

    En el siguiente capítulo aprenderemos a **automatizar tareas repetitivas**, combinando bucles, funciones, archivos y comandos del sistema.