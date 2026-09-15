# Gestión del sistema de archivos

## 1. Introducción

Una de las aplicaciones más importantes de Python en la administración de sistemas es la **automatización de tareas relacionadas con archivos y directorios**.

Un programa Python puede, por ejemplo:

- Leer información almacenada en un archivo.
- Crear automáticamente nuevos archivos.
- Modificar archivos existentes.
- Procesar archivos de configuración.
- Leer inventarios de equipos.
- Crear informes.
- Comprobar si un archivo o una carpeta existe.
- Crear, copiar, mover o eliminar archivos y directorios.

Estas operaciones permiten construir **scripts de administración** capaces de realizar automáticamente tareas que manualmente serían repetitivas.

!!! example "Ejemplo"

    Imaginemos que administramos una red con 200 ordenadores.

    Podemos guardar sus nombres y direcciones IP en un archivo y crear un programa Python que lea automáticamente esa información para realizar diferentes operaciones sobre los equipos.

---

## 2. Archivos y directorios

Antes de trabajar con archivos desde Python debemos distinguir dos conceptos básicos.

### Archivo

Un **archivo** es una unidad de información almacenada en un dispositivo.

Algunos ejemplos son:

```text
usuarios.txt
equipos.csv
configuracion.json
informe.txt
errores.log
```

La extensión suele indicar el tipo de información almacenada:

| Extensión | Uso habitual |
|---|---|
| `.txt` | Texto |
| `.csv` | Datos separados por campos |
| `.json` | Datos estructurados |
| `.log` | Registros de actividad |
| `.py` | Programa Python |

### Directorio

Un **directorio** o carpeta permite organizar archivos y otros directorios.

Por ejemplo:

```text
proyecto/
│
├── datos/
│   ├── equipos.csv
│   └── usuarios.txt
│
├── informes/
│   └── informe.txt
│
└── programa.py
```

En este ejemplo, nuestro programa `programa.py` podría leer información de `datos/equipos.csv` y generar posteriormente un informe dentro de `informes`.

---

## 3. Rutas de archivos

Para acceder a un archivo, Python necesita conocer su **ruta**.

Una ruta indica dónde se encuentra un archivo o directorio dentro del sistema de archivos.

En Windows podemos encontrar rutas como:

```text
C:\Users\Jose\Documents\datos\equipos.csv
```

Podemos trabajar principalmente con dos tipos de rutas:

- **Rutas absolutas**
- **Rutas relativas**

### Ruta absoluta

Una ruta absoluta especifica completamente la ubicación del archivo.

Por ejemplo:

```text
C:\Users\Jose\Documents\Python\datos\equipos.csv
```

La ruta comienza desde una ubicación concreta del sistema.

El problema es que una ruta absoluta suele depender del ordenador en el que ejecutemos el programa.

Por ejemplo, este archivo:

```text
C:\Users\Jose\Documents\Python\datos\equipos.csv
```

probablemente no exista en el ordenador de otro alumno.

### Ruta relativa

Una ruta relativa indica la ubicación de un archivo tomando como referencia el directorio desde el que estamos trabajando.

Supongamos esta estructura:

```text
proyecto/
│
├── datos/
│   └── equipos.csv
│
└── programa.py
```

Desde `programa.py` podemos referirnos al archivo simplemente como:

```text
datos/equipos.csv
```

Esto hace que nuestros programas sean mucho más fáciles de trasladar entre diferentes ordenadores.

!!! tip "Recomendación"

    Siempre que sea posible utilizaremos **rutas relativas** en nuestros proyectos.

    De esta manera podremos copiar el proyecto completo a otro ordenador sin tener que modificar las rutas utilizadas por nuestros programas.

---

## 4. El directorio de trabajo

Cuando ejecutamos un programa Python existe un directorio denominado **directorio de trabajo actual**.

Podemos averiguar cuál es utilizando el módulo `os`.

Crea un archivo llamado:

```text
directorio_actual.py
```

Escribe:

```python
import os

directorio = os.getcwd()

print("Directorio de trabajo actual:")
print(directorio)
```

Ejecuta el programa desde la terminal de VS Code:

```powershell
python directorio_actual.py
```

Obtendremos una salida similar a:

```text
Directorio de trabajo actual:
C:\Users\Jose\Documents\Proyectos\Python
```

La función:

```python
os.getcwd()
```

significa **Get Current Working Directory** y devuelve el directorio de trabajo actual.

!!! note "Importante"

    El directorio de trabajo es especialmente importante cuando utilizamos **rutas relativas**, ya que Python buscará los archivos tomando este directorio como referencia.

---

## 5. Nuestra primera práctica con archivos

Vamos a preparar una pequeña estructura que utilizaremos en los siguientes apartados.

Crea una carpeta llamada:

```text
practicas
```

Dentro crea:

```text
practicas/
│
└── capitulo1/
    │
    ├── datos/
    └── programas/
```

Dentro de `datos` crea manualmente el archivo:

```text
equipos.txt
```

Introduce estas líneas:

```text
PC-AULA-01
PC-AULA-02
PC-AULA-03
SERVIDOR-01
ROUTER-01
```

La estructura quedará:

```text
practicas/
└── capitulo1/
    │
    ├── datos/
    │   └── equipos.txt
    │
    └── programas/
```

Todavía **no vamos a leer el archivo desde Python**.

En el siguiente apartado aprenderemos a abrirlo correctamente mediante:

```python
with open(...)
```

y veremos por qué esta es una de las formas más adecuadas de trabajar con archivos desde Python.

---

## Resumen

En esta primera parte hemos aprendido que:

- Python puede automatizar tareas relacionadas con archivos y directorios.
- Los archivos almacenan información.
- Los directorios permiten organizar archivos.
- Una ruta indica dónde se encuentra un archivo.
- Las rutas pueden ser absolutas o relativas.
- Las rutas relativas facilitan que nuestros programas funcionen en diferentes ordenadores.
- Python puede conocer el directorio de trabajo mediante `os.getcwd()`.

En el siguiente apartado comenzaremos a **leer archivos de texto desde Python**.