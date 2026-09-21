# Capítulo 7. Depuración profesional en VS Code

Hasta ahora hemos desarrollado programas cada vez más completos.

Hemos trabajado con:

```text
archivos
CSV
comandos del sistema
automatización
argparse
excepciones
logging
HTTP
APIs
JSON
socket
DNS
TCP
```

A medida que un programa aumenta de tamaño también aumenta la dificultad para localizar los errores.

Hasta ahora hemos utilizado frecuentemente:

```python
print()
```

para comprobar el valor de una variable o averiguar por qué una parte del programa no funciona como esperábamos.

Por ejemplo:

```python
print(
    resultado
)
```

Esta técnica puede ser útil en programas pequeños, pero Visual Studio Code dispone de una herramienta mucho más potente:

```text
DEPURADOR
```

El depurador nos permite detener temporalmente un programa durante su ejecución y observar exactamente qué está ocurriendo.

En este capítulo aprenderemos a utilizarlo.

---

## 1. Introducción a la depuración de programas

Cuando escribimos un programa podemos encontrar diferentes tipos de problemas.

Por ejemplo:

```text
el programa no arranca
```

```text
aparece una excepción
```

```text
el programa funciona,
pero el resultado es incorrecto
```

```text
una condición se ejecuta
cuando no debería
```

```text
una variable contiene
un valor inesperado
```

Encontrar la causa de estos problemas forma parte del proceso de:

```text
depuración
```

---

### 2. ¿Qué significa depurar?

Depurar un programa consiste en analizar su ejecución para localizar y corregir errores.

En inglés se utiliza el término:

```text
debugging
```

y la herramienta utilizada para hacerlo se denomina:

```text
debugger
```

o:

```text
depurador
```

Podemos representar el proceso:

```text
PROGRAMA
   │
   ▼
ejecución
   │
   ▼
resultado incorrecto
   │
   ▼
depuración
   │
   ▼
localizar el problema
   │
   ▼
corregir código
   │
   ▼
volver a probar
```

La depuración es una parte normal del desarrollo de software.

---

### 3. Un error no siempre produce una excepción

Consideremos:

```python
precio = 100
iva = 21

total = precio + iva

print(
    total
)
```

El programa funciona y no produce ninguna excepción.

Sin embargo, si nuestra intención era calcular un precio con un IVA del 21 %, el cálculo es incorrecto.

El problema es:

```python
total = precio + iva
```

La operación correcta podría ser:

```python
total = precio + (
    precio * iva / 100
)
```

Este tipo de problema se denomina habitualmente:

```text
error lógico
```

Python puede ejecutar perfectamente el programa, pero el resultado no es el esperado.

---

### 4. Tipos de errores

Podemos distinguir inicialmente tres situaciones.

#### Error de sintaxis

Por ejemplo:

```python
if edad >= 18
    print("Mayor de edad")
```

Falta:

```text
:
```

Python no puede interpretar correctamente el programa.

---

#### Error durante la ejecución

Por ejemplo:

```python
numero = int(
    "hola"
)
```

Python puede interpretar el código, pero durante la ejecución aparece:

```text
ValueError
```

---

#### Error lógico

Por ejemplo:

```python
base = 100
iva = 21

total = base + iva
```

El programa termina normalmente, pero el cálculo no representa un incremento del 21 %.

!!! note "Depuración"

    El depurador resulta especialmente útil cuando el programa puede ejecutarse pero necesitamos comprender por qué se comporta de una determinada manera.

---

### 5. Utilizar `print()` para investigar

Una técnica sencilla consiste en introducir temporalmente:

```python
print()
```

Por ejemplo:

```python
precio = 100
iva = 21

print(
    f"precio = {precio}"
)

print(
    f"iva = {iva}"
)

total = precio + iva

print(
    f"total = {total}"
)
```

Esto nos permite observar determinados valores.

Esta técnica recibe informalmente nombres como:

```text
depuración con print
```

o:

```text
print debugging
```

Puede ser útil, pero tiene algunas limitaciones.

---

### 6. Limitaciones de utilizar `print()`

Imaginemos un programa con:

```text
300 líneas
```

y muchos:

```text
if
for
funciones
variables
```

Podríamos terminar añadiendo:

```python
print(variable1)
print(variable2)
print(variable3)
print("he llegado aquí")
print("entro en el if")
print("salgo del bucle")
```

Después tendríamos que eliminar todas estas instrucciones.

Además, modificar el código únicamente para observarlo no siempre es la mejor solución.

El depurador nos permitirá inspeccionar el programa sin llenar nuestro código de instrucciones `print()` temporales.

---

### 7. ¿Qué puede hacer un depurador?

Un depurador permite, entre otras cosas:

```text
detener el programa
```

```text
ejecutar línea a línea
```

```text
observar variables
```

```text
entrar dentro de funciones
```

```text
salir de funciones
```

```text
continuar la ejecución
```

```text
examinar expresiones
```

```text
observar la pila de llamadas
```

Visual Studio Code proporciona estas herramientas mediante su sistema de depuración.

---

### 8. Preparar nuestra primera práctica

Vamos a crear:

```text
practicas/
└── capitulo7/
    └── programas/
        └── primera_depuracion.py
```

Crea:

```text
practicas/capitulo7/programas/
primera_depuracion.py
```

Escribe:

```python
precio = 100
iva = 21

importe_iva = (
    precio * iva / 100
)

total = (
    precio + importe_iva
)

print(
    f"Precio: {precio}"
)

print(
    f"IVA: {importe_iva}"
)

print(
    f"Total: {total}"
)
```

Antes de utilizar el depurador comprobaremos que el programa funciona normalmente.

---

### 9. Ejecutar normalmente el programa

Desde el terminal integrado de VS Code podemos ejecutar:

```powershell
python primera_depuracion.py
```

Obtendremos:

```text
Precio: 100
IVA: 21.0
Total: 121.0
```

Hasta aquí no estamos utilizando el depurador.

Estamos realizando una:

```text
ejecución normal
```

El programa comienza:

```text
inicio
```

ejecuta todas sus instrucciones y termina:

```text
inicio
  │
  ▼
línea 1
  │
  ▼
línea 2
  │
  ▼
línea 3
  │
  ▼
...
  │
  ▼
fin
```

Ahora cambiaremos esta forma de ejecutar el programa.

---

### 10. Abrir la herramienta de depuración

En Visual Studio Code localiza en la barra lateral izquierda el apartado:

```text
Run and Debug
```

En una instalación en castellano puede aparecer relacionado con:

```text
Ejecutar y depurar
```

También podemos utilizar:

```text
Ctrl + Shift + D
```

Esto abre la vista dedicada a la ejecución y depuración.

!!! tip "VS Code"

    Los nombres exactos de algunos botones pueden variar ligeramente según el idioma o la versión instalada de Visual Studio Code.

    Los conceptos y el funcionamiento general son los mismos.

---

### 11. ¿Qué es un breakpoint?

Uno de los elementos fundamentales del depurador es el:

```text
breakpoint
```

En castellano:

```text
punto de interrupción
```

Un breakpoint indica al depurador:

```text
cuando llegues aquí,
detén temporalmente
la ejecución
```

Podemos representarlo:

```text
línea 1
   │
   ▼
línea 2
   │
   ▼
● línea 3
   │
   └── DETENER
```

El programa no termina.

Simplemente queda:

```text
pausado
```

en ese punto.

---

### 12. Crear nuestro primer breakpoint

Abre:

```text
primera_depuracion.py
```

Busca:

```python
importe_iva = (
    precio * iva / 100
)
```

Haz clic en el margen izquierdo del editor, junto al número de la primera línea de esa instrucción.

Aparecerá un indicador del breakpoint.

También puedes colocar el cursor en la línea y utilizar:

```text
F9
```

En este momento todavía no hemos ejecutado el programa.

Únicamente hemos indicado:

```text
detente aquí
cuando ejecutes
con el depurador
```

---

### 13. Iniciar la depuración

Con:

```text
primera_depuracion.py
```

abierto, inicia la depuración.

Una forma habitual es utilizar:

```text
F5
```

VS Code puede pedir inicialmente qué depurador queremos utilizar.

Seleccionaremos:

```text
Python
```

y, cuando corresponda:

```text
Python File
```

o la opción equivalente para depurar el archivo Python actual.

El programa comenzará a ejecutarse.

Cuando llegue al breakpoint:

```text
se detendrá
```

---

### 14. Ejecución pausada

Cuando el programa se detiene podemos imaginar:

```text
precio = 100
     │
     ▼
iva = 21
     │
     ▼
● importe_iva = ...
     │
     ▼
total = ...
```

Las instrucciones anteriores ya se han ejecutado.

La línea marcada es la siguiente instrucción relevante que el depurador está preparado para ejecutar.

Esto es muy importante.

!!! note "Programa pausado"

    El programa no ha finalizado.

    Su ejecución está temporalmente detenida para permitirnos examinar su estado.

---

### 15. El estado de un programa

Cuando hablamos del:

```text
estado del programa
```

nos referimos a la información existente en un determinado momento de la ejecución.

Por ejemplo:

```text
precio = 100
iva = 21
```

El depurador nos permite observar estos valores mientras el programa está detenido.

Esto es mucho más potente que analizar únicamente el código escrito.

Podemos observar:

```text
qué está ocurriendo realmente
```

durante la ejecución.

---

### 16. Panel de variables

Con el programa detenido observa el panel:

```text
VARIABLES
```

o:

```text
Variables
```

VS Code mostrará las variables disponibles en ese momento.

Deberías poder observar valores como:

```text
precio    100
iva       21
```

Dependiendo del punto exacto en el que se haya detenido el programa, algunas variables posteriores todavía no existirán.

Por ejemplo:

```text
importe_iva
```

puede no tener todavía un valor si su instrucción aún no se ha ejecutado.

---

### 17. El momento de creación de una variable

Consideremos:

```python
precio = 100

iva = 21

importe_iva = (
    precio * iva / 100
)
```

Después de ejecutar:

```python
precio = 100
```

existe:

```text
precio
```

Después de:

```python
iva = 21
```

existen:

```text
precio
iva
```

Después de calcular:

```python
importe_iva
```

existirán:

```text
precio
iva
importe_iva
```

El depurador nos permite observar esta evolución.

---

### 18. Ejecutar una línea cada vez

Cuando el programa está detenido podemos ejecutar la siguiente instrucción utilizando:

```text
Step Over
```

Habitualmente su atajo es:

```text
F10
```

Pulsa:

```text
F10
```

una vez.

La línea actual se ejecutará y el programa se detendrá en la siguiente instrucción.

Podemos representar:

```text
ANTES

● importe_iva = precio * iva / 100

  total = precio + importe_iva
```

Después de pulsar `F10`:

```text
importe_iva = precio * iva / 100

● total = precio + importe_iva
```

Ahora:

```text
importe_iva
```

ya tendrá un valor.

---

### 19. Observar cómo cambian las variables

Después de ejecutar el cálculo:

```python
importe_iva = (
    precio * iva / 100
)
```

observa nuevamente:

```text
Variables
```

Ahora tendremos aproximadamente:

```text
precio        100
iva           21
importe_iva   21.0
```

Pulsa otra vez:

```text
F10
```

Después de ejecutar:

```python
total = (
    precio + importe_iva
)
```

aparecerá:

```text
total   121.0
```

Estamos viendo cómo cambia el estado del programa línea a línea.

---

### 20. Step Over

La operación:

```text
Step Over
```

significa:

```text
ejecutar la instrucción actual
y detenerse en la siguiente
```

Su atajo habitual es:

```text
F10
```

Durante nuestras primeras prácticas será una de las operaciones que más utilizaremos.

---

### 21. Continuar la ejecución

No siempre queremos avanzar línea por línea hasta terminar.

Podemos utilizar:

```text
Continue
```

Su atajo habitual es:

```text
F5
```

Si no existe ningún otro breakpoint, el programa continuará hasta finalizar.

Si existe otro breakpoint:

```text
breakpoint 1
      │
      ▼
   Continue
      │
      ▼
ejecución normal
      │
      ▼
breakpoint 2
      │
      ▼
    pausa
```

---

### 22. Añadir un segundo breakpoint

En:

```text
primera_depuracion.py
```

mantén el primer breakpoint y añade otro junto a:

```python
print(
    f"Total: {total}"
)
```

Ahora tenemos:

```text
breakpoint 1
     │
     ▼
cálculos
     │
     ▼
breakpoint 2
```

Inicia nuevamente la depuración con:

```text
F5
```

El programa se detendrá en el primero.

Pulsa otra vez:

```text
F5
```

El programa continuará hasta el segundo.

---

### 23. Diferencia entre `F5` y `F10`

Durante una sesión de depuración:

```text
F5
```

se utiliza normalmente para:

```text
continuar
```

hasta el siguiente breakpoint.

Mientras que:

```text
F10
```

permite:

```text
ejecutar la siguiente instrucción
```

y volver a detenerse.

Podemos resumir:

```text
F5
│
└── continuar


F10
│
└── avanzar paso a paso
```

---

### 24. Detener la depuración

Podemos finalizar manualmente una sesión mediante:

```text
Stop
```

Habitualmente también podemos utilizar:

```text
Shift + F5
```

Esto termina la sesión de depuración.

No debemos confundir:

```text
pausar
```

con:

```text
detener
```

Pausar:

```text
el programa sigue activo
pero temporalmente detenido
```

Detener:

```text
finaliza la sesión
de depuración
```

---

### 25. Activar y desactivar breakpoints

No es necesario eliminar un breakpoint cada vez que no queramos utilizarlo.

VS Code permite:

```text
activar
desactivar
eliminar
```

breakpoints.

Esto resulta especialmente útil cuando tenemos varios puntos de interés en un programa grande.

Podemos preparar:

```text
breakpoint A
breakpoint B
breakpoint C
```

y activar únicamente los que necesitemos para una prueba determinada.

---

### 26. Panel Breakpoints

En la vista de depuración encontraremos un apartado relacionado con:

```text
BREAKPOINTS
```

Desde él podemos gestionar los puntos de interrupción existentes.

Esto resulta especialmente útil cuando el proyecto contiene:

```text
varios archivos
```

y tenemos breakpoints repartidos por diferentes programas.

---

### 27. Primera práctica con un error lógico

Crea:

```text
practicas/capitulo7/programas/
calcular_media.py
```

Escribe:

```python
nota1 = 7
nota2 = 8
nota3 = 9

suma = (
    nota1
    + nota2
    + nota3
)

media = (
    suma / 2
)

print(
    f"Media: {media}"
)
```

Ejecuta:

```powershell
python calcular_media.py
```

Obtendremos:

```text
Media: 12.0
```

El programa:

```text
no produce una excepción
```

pero el resultado es incorrecto.

---

### 28. Depurar `calcular_media.py`

Coloca un breakpoint en:

```python
suma = (
    nota1
    + nota2
    + nota3
)
```

Inicia la depuración:

```text
F5
```

Observa:

```text
nota1
nota2
nota3
```

Avanza con:

```text
F10
```

Después observa:

```text
suma
```

Deberá contener:

```text
24
```

Avanza nuevamente.

Ahora observa:

```text
media
```

Contendrá:

```text
12.0
```

Podemos deducir que:

```text
suma
```

es correcta.

El problema aparece en:

```python
media = (
    suma / 2
)
```

---

### 29. Localizar el error

Tenemos tres notas:

```text
7
8
9
```

La suma es:

```text
24
```

Pero el programa realiza:

```text
24 / 2
```

cuando debería realizar:

```text
24 / 3
```

Corregimos:

```python
media = (
    suma / 3
)
```

Volvemos a ejecutar.

Obtendremos:

```text
Media: 8.0
```

Este ejemplo muestra una idea fundamental:

```text
el depurador no corrige
automáticamente el programa
```

El depurador nos proporciona información para que podamos localizar la causa del problema.

---

### 30. Observar el flujo de un `if`

Crea:

```text
comprobar_nota.py
```

Escribe:

```python
nota = 4.5


if nota >= 5:

    resultado = "Aprobado"

else:

    resultado = "Suspendido"


print(
    resultado
)
```

Coloca un breakpoint en:

```python
if nota >= 5:
```

Ejecuta mediante:

```text
F5
```

Después avanza utilizando:

```text
F10
```

Observa qué bloque ejecuta Python.

---

### 31. Seguir una condición

Tenemos:

```python
nota = 4.5
```

La condición:

```python
nota >= 5
```

produce:

```text
False
```

Por tanto, Python continúa por:

```python
else:
```

y ejecuta:

```python
resultado = "Suspendido"
```

El depurador nos permite observar directamente el camino seguido por el programa.

---

### 32. Cambiar el valor

Modifica:

```python
nota = 7
```

Vuelve a iniciar la depuración.

Ahora:

```python
nota >= 5
```

será:

```text
True
```

y el flujo cambiará:

```text
if
 │
 ▼
True
 │
 ▼
resultado = "Aprobado"
```

Este tipo de análisis será muy útil cuando tengamos condiciones más complejas.

---

### 33. Depurar un bucle

Crea:

```text
depurar_bucle.py
```

Escribe:

```python
numeros = [
    10,
    20,
    30,
    40
]


total = 0


for numero in numeros:

    total = (
        total + numero
    )


print(
    f"Total: {total}"
)
```

Coloca un breakpoint en:

```python
total = (
    total + numero
)
```

Inicia la depuración.

---

### 34. Primera iteración

En la primera iteración:

```text
numero = 10
total = 0
```

Después de ejecutar:

```python
total = (
    total + numero
)
```

tendremos:

```text
total = 10
```

El bucle volverá a comenzar.

---

### 35. Segunda iteración

Ahora:

```text
numero = 20
total = 10
```

Después:

```text
total = 30
```

En las siguientes iteraciones observaremos:

```text
numero = 30
total = 60
```

y finalmente:

```text
numero = 40
total = 100
```

El depurador nos permite observar cómo una variable cambia durante las diferentes iteraciones.

---

### 36. Depurar bucles

Los bucles son uno de los lugares donde la depuración resulta especialmente útil.

Podemos investigar problemas como:

```text
el bucle se ejecuta
demasiadas veces
```

```text
el bucle no se ejecuta
```

```text
una variable acumuladora
tiene un valor incorrecto
```

```text
un elemento concreto
produce un error
```

Más adelante veremos cómo utilizar breakpoints condicionales para detenernos únicamente cuando se cumpla una determinada condición.

---

### 37. Introducción a las funciones

Hasta ahora hemos avanzado línea por línea dentro del mismo bloque.

Pero nuestros programas utilizan muchas funciones.

Por ejemplo:

```python
def calcular_total(
    precio,
    iva
):

    importe_iva = (
        precio * iva / 100
    )

    return (
        precio + importe_iva
    )


resultado = calcular_total(
    100,
    21
)


print(
    resultado
)
```

Cuando llegamos a:

```python
resultado = calcular_total(
    100,
    21
)
```

tenemos dos posibilidades:

```text
ejecutar la función completa
```

o:

```text
entrar dentro de la función
```

Aquí aparece otra herramienta fundamental del depurador.

---

### 38. Step Into

La operación:

```text
Step Into
```

permite entrar dentro de una función que estamos llamando.

Su atajo habitual es:

```text
F11
```

Podemos representar:

```text
resultado = calcular_total(...)
             │
             │ F11
             ▼
def calcular_total(...)
             │
             ▼
    importe_iva = ...
```

Esto nos permite depurar el interior de la función.

---

### 39. Preparar una práctica con funciones

Crea:

```text
depurar_funcion.py
```

Escribe:

```python
def calcular_total(
    precio,
    iva
):

    importe_iva = (
        precio * iva / 100
    )

    total = (
        precio + importe_iva
    )

    return total


precio = 150
iva = 21


resultado = calcular_total(
    precio,
    iva
)


print(
    f"Total: {resultado}"
)
```

Coloca un breakpoint en:

```python
resultado = calcular_total(
    precio,
    iva
)
```

---

### 40. Entrar dentro de la función

Inicia:

```text
F5
```

Cuando el programa se detenga en la llamada:

```python
calcular_total()
```

utiliza:

```text
F11
```

En lugar de ejecutar toda la función de una vez, el depurador entrará en ella.

Ahora podremos observar:

```text
precio
iva
```

dentro de:

```python
calcular_total()
```

---

### 41. Observar parámetros

Dentro de la función tendremos:

```text
precio = 150
iva = 21
```

Estos valores proceden de:

```python
calcular_total(
    precio,
    iva
)
```

Podemos avanzar mediante:

```text
F10
```

y observar la aparición de:

```text
importe_iva
```

y posteriormente:

```text
total
```

Esto nos permite comprobar no solamente las variables globales del programa, sino también los parámetros y variables locales de una función.

---

### 42. Step Over frente a Step Into

Supongamos que estamos en:

```python
resultado = calcular_total(
    precio,
    iva
)
```

Si utilizamos:

```text
F10
```

`Step Over`:

```text
ejecuta la función
sin detenerse dentro
```

Después apareceremos en la siguiente instrucción.

Si utilizamos:

```text
F11
```

`Step Into`:

```text
entra dentro de la función
```

Podemos resumir:

```text
          llamada a función
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
      F10               F11
        │                 │
        ▼                 ▼
  Step Over          Step Into
        │                 │
        ▼                 ▼
ejecutar función      entrar en
   completa           la función
```

---

### 43. ¿Cuándo utilizar cada uno?

Utilizaremos:

```text
Step Over
```

cuando confiemos en la función y simplemente queramos continuar.

Utilizaremos:

```text
Step Into
```

cuando sospechemos que el problema puede encontrarse dentro de la función.

Por ejemplo:

```text
resultado incorrecto
        │
        ▼
¿la función recibe
los datos correctos?
        │
        ▼
    Step Into
        │
        ▼
examinar parámetros
        │
        ▼
seguir cálculos
```

---

### 44. Step Out

Existe otra operación:

```text
Step Out
```

que permite terminar la ejecución de la función actual y regresar al lugar desde el que fue llamada.

Su atajo habitual es:

```text
Shift + F11
```

Por ejemplo:

```text
programa principal
       │
       ▼
calcular_total()
       │
       ▼
estamos aquí
       │
       │ Step Out
       ▼
terminar función
       │
       ▼
programa principal
```

Esto resulta útil cuando hemos entrado en una función, hemos comprobado lo necesario y ya no queremos recorrer todas sus instrucciones.

---

### 45. Controles fundamentales del depurador

Por ahora debemos recordar:

| Acción | Atajo habitual | Función |
|---|---|---|
| Continue | `F5` | Continúa hasta el siguiente breakpoint |
| Step Over | `F10` | Ejecuta la línea sin entrar en funciones |
| Step Into | `F11` | Entra dentro de una función |
| Step Out | `Shift + F11` | Sale de la función actual |
| Stop | `Shift + F5` | Finaliza la depuración |
| Breakpoint | `F9` | Añade o elimina un breakpoint |

!!! tip "Atajos"

    No es necesario memorizar todos los atajos inmediatamente.

    VS Code muestra también los controles de depuración en su interfaz.

    Con la práctica acabarán resultando familiares.

---

### 46. Práctica guiada: localizar un error en una función

Crea:

```text
calcular_descuento.py
```

Escribe:

```python
def aplicar_descuento(
    precio,
    porcentaje
):

    descuento = (
        precio * porcentaje
    )

    precio_final = (
        precio - descuento
    )

    return precio_final


precio = 200
descuento = 10


resultado = aplicar_descuento(
    precio,
    descuento
)


print(
    f"Precio inicial: {precio}"
)

print(
    f"Descuento: {descuento}%"
)

print(
    f"Precio final: {resultado}"
)
```

El resultado será incorrecto.

No corrijas todavía el programa.

Vamos a utilizar el depurador para encontrar el problema.

---

### 47. Primera hipótesis

Sabemos:

```text
precio = 200
descuento = 10 %
```

Por tanto, esperamos:

```text
descuento aplicado = 20
```

y:

```text
precio final = 180
```

Ejecuta primero el programa normalmente.

Después iniciaremos la investigación.

---

### 48. Colocar el breakpoint

Coloca un breakpoint en:

```python
resultado = aplicar_descuento(
    precio,
    descuento
)
```

Inicia la depuración:

```text
F5
```

Comprueba:

```text
precio = 200
descuento = 10
```

Los argumentos parecen correctos.

Ahora utiliza:

```text
F11
```

para entrar en:

```python
aplicar_descuento()
```

---

### 49. Examinar el cálculo

Dentro de la función tenemos:

```python
descuento = (
    precio * porcentaje
)
```

Avanza con:

```text
F10
```

Observa el valor de:

```text
descuento
```

El resultado será:

```text
2000
```

Ya hemos localizado el punto donde aparece un valor inesperado.

---

### 50. Corregir el error

La expresión:

```python
precio * porcentaje
```

no calcula un porcentaje.

Debemos utilizar:

```python
precio * porcentaje / 100
```

Por tanto:

```python
descuento = (
    precio * porcentaje / 100
)
```

Ahora:

```text
200 × 10 / 100 = 20
```

y:

```text
200 - 20 = 180
```

Vuelve a iniciar la depuración para comprobarlo.

---

### 51. Depurar antes de modificar

Durante una incidencia conviene evitar cambiar muchas líneas simultáneamente sin conocer la causa.

Una estrategia mejor es:

```text
reproducir problema
        │
        ▼
colocar breakpoint
        │
        ▼
observar variables
        │
        ▼
seguir ejecución
        │
        ▼
localizar punto incorrecto
        │
        ▼
formular causa
        │
        ▼
modificar código
        │
        ▼
volver a probar
```

Esto convierte la depuración en un proceso sistemático.

---

### 52. Práctica propuesta: contador incorrecto

Crea:

```text
contador.py
```

con:

```python
equipos = [
    "PC01",
    "PC02",
    "PC03",
    "PC04"
]


contador = 1


for equipo in equipos:

    contador += 1


print(
    f"Equipos: {contador}"
)
```

El resultado no coincide con el número de equipos.

Utiliza únicamente el depurador para investigar inicialmente el problema.

Debes:

1. Colocar un breakpoint dentro del `for`.
2. Observar `equipo`.
3. Observar `contador`.
4. Avanzar iteración por iteración.
5. Determinar cuándo aparece el valor incorrecto.
6. Corregir el programa.
7. Volver a depurarlo.

---

### 53. Práctica propuesta: buscar un error en una condición

Crea:

```text
estado_servicio.py
```

Escribe:

```python
codigo = 404


if codigo >= 200 or codigo < 300:

    estado = "Correcto"

else:

    estado = "Error"


print(
    f"Estado: {estado}"
)
```

Ejecuta el programa.

Después utiliza el depurador para analizar:

```python
codigo >= 200
```

y:

```python
codigo < 300
```

Estudia por qué la condición completa produce un resultado incorrecto.

!!! tip "Pista"

    Piensa si queremos que se cumpla:

    ```text
    una condición O la otra
    ```

    o:

    ```text
    una condición Y la otra
    ```

---

### 54. Práctica propuesta: depurar una lista

Crea:

```text
inventario.py
```

Escribe:

```python
equipos = [
    {
        "nombre": "PC01",
        "ram": 8
    },
    {
        "nombre": "PC02",
        "ram": 16
    },
    {
        "nombre": "PC03",
        "ram": 32
    }
]


total_ram = 0


for equipo in equipos:

    total_ram = (
        equipo["ram"]
    )


print(
    f"RAM total: "
    f"{total_ram} GB"
)
```

El programa debería sumar toda la memoria RAM del inventario.

Sin embargo, no lo hace.

Utiliza el depurador para observar:

```text
equipo
total_ram
```

en cada iteración.

No corrijas el programa hasta haber identificado qué ocurre con:

```text
total_ram
```

durante el bucle.

---

### 55. Lo que debemos dominar hasta ahora

Después de estas prácticas debemos saber:

```text
iniciar una sesión de depuración
```

```text
crear un breakpoint
```

```text
detenernos en una línea
```

```text
observar variables
```

```text
continuar la ejecución
```

```text
avanzar línea a línea
```

```text
entrar en una función
```

```text
salir de una función
```

```text
seguir un if
```

```text
seguir las iteraciones de un for
```

---

### 56. Depuración frente a `logging`

No debemos confundir:

```text
debugger
```

con:

```python
logging
```

El depurador permite analizar interactivamente una ejecución:

```text
ejecutar
   │
   ▼
pausar
   │
   ▼
examinar
   │
   ▼
continuar
```

`logging` registra información para consultarla durante o después de la ejecución:

```text
ejecutar
   │
   ▼
registrar eventos
   │
   ▼
archivo log
   │
   ▼
analizar posteriormente
```

Ambas herramientas son complementarias.

---

### 57. Depuración frente a excepciones

Tampoco debemos confundir el depurador con:

```python
try
```

y:

```python
except
```

Las excepciones forman parte del diseño del programa.

Por ejemplo:

```python
try:

    numero = int(
        texto
    )

except ValueError:

    print(
        "Valor incorrecto."
    )
```

El depurador es una herramienta que utilizamos durante el desarrollo y diagnóstico del programa.

Por tanto:

```text
try / except
     │
     └── gestión de errores
         dentro del programa


debugger
     │
     └── herramienta para analizar
         la ejecución del programa
```

---

### 58. Tres herramientas diferentes

A estas alturas conocemos tres herramientas importantes:

```text
EXCEPCIONES
     │
     ▼
controlar errores
esperados


LOGGING
     │
     ▼
registrar
ejecuciones


DEBUGGER
     │
     ▼
investigar
la ejecución
```

No compiten entre ellas.

Se complementan.

Un programa profesional puede utilizar:

```text
try / except
+
logging
+
depuración durante el desarrollo
```

---

### 59. Práctica de consolidación

Crea:

```text
analizar_inventario.py
```

Escribe:

```python
def calcular_memoria(
    equipos
):

    total = 0

    for equipo in equipos:

        total += (
            equipo["ram"]
        )

    return total


def contar_equipos_activos(
    equipos
):

    activos = 0

    for equipo in equipos:

        if equipo["estado"] == "activo":

            activos += 1

    return activos


equipos = [
    {
        "nombre": "PC01",
        "ram": 8,
        "estado": "activo"
    },
    {
        "nombre": "PC02",
        "ram": 16,
        "estado": "inactivo"
    },
    {
        "nombre": "PC03",
        "ram": 32,
        "estado": "activo"
    }
]


memoria = calcular_memoria(
    equipos
)


activos = contar_equipos_activos(
    equipos
)


print(
    f"RAM total: "
    f"{memoria} GB"
)

print(
    f"Equipos activos: "
    f"{activos}"
)
```

Utiliza el depurador aunque el programa funcione correctamente.

El objetivo de esta práctica no es corregir un error.

Debes utilizar:

1. Un breakpoint antes de llamar a `calcular_memoria()`.
2. `Step Into` para entrar en la función.
3. `Step Over` para recorrer el `for`.
4. Observar `equipo`.
5. Observar `total`.
6. `Step Out` para regresar al programa principal.
7. Entrar en `contar_equipos_activos()`.
8. Observar `activos`.
9. Seguir las condiciones del `if`.
10. Continuar hasta finalizar.

!!! important "Depurar programas correctos"

    Es recomendable aprender a utilizar el depurador con programas que funcionan correctamente.

    Así podemos comprender cómo se comporta una ejecución normal antes de utilizar la herramienta para investigar errores más complejos.

---

### 60. Resumen de esta primera parte

En esta primera parte hemos introducido la depuración profesional de programas Python desde Visual Studio Code.

Hemos aprendido qué es:

```text
debugging
```

y qué función realiza un:

```text
debugger
```

Hemos creado nuestros primeros:

```text
breakpoints
```

y hemos utilizado:

```text
F5
```

para continuar la ejecución.

También hemos utilizado:

```text
F10
```

para:

```text
Step Over
```

y:

```text
F11
```

para:

```text
Step Into
```

Además hemos introducido:

```text
Shift + F11
```

para:

```text
Step Out
```

Hemos observado:

```text
variables
parámetros
condiciones
bucles
funciones
```

mientras el programa se encontraba detenido.

El flujo básico aprendido es:

```text
ejecutar con depurador
        │
        ▼
    breakpoint
        │
        ▼
      pausa
        │
        ▼
observar variables
        │
        ▼
F10 / F11
        │
        ▼
seguir ejecución
        │
        ▼
localizar problema
```

En la siguiente parte profundizaremos en las herramientas de inspección de VS Code.

Trabajaremos con:

```text
Variables
Watch
Call Stack
Debug Console
```

y aprenderemos a utilizar:

```text
breakpoints condicionales
```

para detener un programa únicamente cuando se produzca una situación concreta.

Estas herramientas nos permitirán depurar programas más grandes y nos prepararán para analizar posteriormente el **proyecto final del curso**.

---

## 61. Inspección avanzada durante la depuración

En la primera parte hemos aprendido el funcionamiento básico del depurador:

```text
breakpoint
    │
    ▼
programa detenido
    │
    ▼
observar variables
    │
    ▼
F10 / F11
    │
    ▼
continuar ejecución
```

Sin embargo, cuando un programa aumenta de tamaño necesitamos herramientas que nos permitan responder preguntas más concretas.

Por ejemplo:

```text
¿Qué valor tiene esta expresión?
```

```text
¿Desde qué función hemos llegado hasta aquí?
```

```text
¿Cuántas funciones están activas?
```

```text
¿Podemos detener el programa únicamente
cuando una variable tenga cierto valor?
```

```text
¿Podemos probar expresiones mientras
el programa está detenido?
```

Visual Studio Code proporciona diferentes herramientas para hacerlo.

En esta parte trabajaremos principalmente con:

```text
Variables
Watch
Call Stack
Debug Console
Breakpoints condicionales
```

---

### 62. Preparar el programa de trabajo

Crearemos un programa con varias funciones para poder analizarlo.

Crea:

```text
practicas/capitulo7/programas/
analizar_pedido.py
```

Escribe:

```python
def calcular_subtotal(
    precio,
    unidades
):

    subtotal = (
        precio * unidades
    )

    return subtotal


def calcular_descuento(
    subtotal,
    porcentaje
):

    descuento = (
        subtotal
        * porcentaje
        / 100
    )

    return descuento


def calcular_total(
    subtotal,
    descuento
):

    total = (
        subtotal - descuento
    )

    return total


precio = 25
unidades = 4
porcentaje_descuento = 10


subtotal = calcular_subtotal(
    precio,
    unidades
)


descuento = calcular_descuento(
    subtotal,
    porcentaje_descuento
)


total = calcular_total(
    subtotal,
    descuento
)


print(
    f"Subtotal: {subtotal}"
)

print(
    f"Descuento: {descuento}"
)

print(
    f"Total: {total}"
)
```

Ejecuta primero normalmente:

```powershell
python analizar_pedido.py
```

Obtendremos:

```text
Subtotal: 100
Descuento: 10.0
Total: 90.0
```

El programa funciona correctamente.

Lo utilizaremos para aprender a inspeccionar su ejecución.

---

### 63. Colocar el primer breakpoint

Coloca un breakpoint en:

```python
subtotal = calcular_subtotal(
    precio,
    unidades
)
```

Inicia la depuración:

```text
F5
```

El programa se detendrá antes de realizar la llamada.

En este momento podremos observar:

```text
precio = 25
unidades = 4
porcentaje_descuento = 10
```

en el panel:

```text
Variables
```

---

### 64. Recordatorio del panel Variables

El panel:

```text
Variables
```

muestra las variables disponibles en el contexto actual.

Por ejemplo:

```text
precio                  25
unidades                 4
porcentaje_descuento    10
```

Todavía no tendremos:

```text
subtotal
descuento
total
```

porque estas variables todavía no han recibido ningún valor.

Utiliza:

```text
F11
```

para entrar en:

```python
calcular_subtotal()
```

Ahora el contexto cambia.

---

### 65. Variables locales

Dentro de:

```python
calcular_subtotal()
```

tenemos:

```python
precio
unidades
subtotal
```

Las variables:

```text
precio
unidades
```

son parámetros de la función.

La variable:

```text
subtotal
```

será una variable local.

Esto significa que pertenece al contexto de ejecución de esa función.

Podemos representarlo:

```text
calcular_subtotal()
│
├── precio
├── unidades
└── subtotal
```

Cuando estamos dentro de la función, el depurador nos permite inspeccionar este contexto.

---

### 66. El contexto de ejecución

Imaginemos:

```python
def funcion_a():

    x = 10


def funcion_b():

    y = 20
```

La variable:

```text
x
```

pertenece al contexto de:

```text
funcion_a()
```

mientras:

```text
y
```

pertenece a:

```text
funcion_b()
```

Cuando depuramos un programa debemos tener presente:

```text
¿en qué función estamos?
```

porque las variables disponibles pueden cambiar según el contexto.

---

### 67. Introducción a Watch

El panel:

```text
Variables
```

muestra muchas variables automáticamente.

Pero en ocasiones queremos seguir específicamente:

```text
una variable
```

o:

```text
una expresión
```

Para ello podemos utilizar:

```text
Watch
```

Podemos traducirlo conceptualmente como:

```text
expresiones a observar
```

---

### 68. Añadir una expresión a Watch

Con el programa detenido busca en la vista de depuración:

```text
WATCH
```

Pulsa:

```text
+
```

para añadir una expresión.

Escribe:

```python
precio
```

Añade también:

```python
unidades
```

Ahora Watch mostrará sus valores.

Por ejemplo:

```text
precio      25
unidades     4
```

---

### 69. Watch puede contener expresiones

Watch no está limitado a nombres de variables.

Podemos añadir:

```python
precio * unidades
```

El depurador evaluará la expresión.

Obtendremos:

```text
100
```

También podemos observar:

```python
precio * unidades / 2
```

o:

```python
unidades > 3
```

Por ejemplo:

```text
unidades > 3
```

producirá:

```text
True
```

---

### 70. Ventaja de Watch

Supongamos que queremos investigar constantemente:

```python
precio * unidades
```

Sin Watch tendríamos que realizar mentalmente el cálculo o añadir temporalmente:

```python
print(
    precio * unidades
)
```

Con Watch podemos observar:

```text
precio * unidades    100
```

sin modificar el programa.

Por tanto:

```text
Watch
  │
  ▼
observar expresiones
durante la depuración
```

---

### 71. Watch y el contexto

Una expresión de Watch solamente puede evaluarse si las variables necesarias existen en el contexto actual.

Por ejemplo:

```python
subtotal
```

puede no existir antes de ejecutar:

```python
subtotal = calcular_subtotal(...)
```

En ese momento VS Code puede indicar que la expresión no está disponible o no puede evaluarse.

Después de crear la variable:

```text
subtotal
```

Watch podrá mostrar su valor.

!!! note "Contexto"

    Que una expresión de Watch no pueda evaluarse no significa necesariamente que exista un error en el programa.

    Puede significar simplemente que esa variable todavía no existe en el punto actual de ejecución.

---

### 72. Práctica con Watch

Añade a Watch:

```python
precio
```

```python
unidades
```

```python
precio * unidades
```

```python
precio > 20
```

Avanza mediante:

```text
F10
```

y observa los resultados.

Después utiliza:

```text
Shift + F11
```

para salir de la función.

Comprueba cómo cambia el contexto.

---

### 73. Introducción a Call Stack

Otra herramienta fundamental es:

```text
CALL STACK
```

En castellano hablamos de:

```text
pila de llamadas
```

La pila de llamadas permite conocer:

```text
qué funciones se están ejecutando
```

y:

```text
cómo hemos llegado
hasta el punto actual
```

---

### 74. Comprender la pila de llamadas

Supongamos:

```python
def funcion_c():

    print(
        "Función C"
    )


def funcion_b():

    funcion_c()


def funcion_a():

    funcion_b()


funcion_a()
```

El flujo será:

```text
programa principal
       │
       ▼
  funcion_a()
       │
       ▼
  funcion_b()
       │
       ▼
  funcion_c()
```

Si detenemos el programa dentro de:

```python
funcion_c()
```

la pila representa aproximadamente:

```text
funcion_c
funcion_b
funcion_a
programa principal
```

---

### 75. ¿Por qué se llama pila?

Una pila funciona según el principio:

```text
último en entrar
primero en salir
```

Podemos imaginar:

```text
┌───────────────┐
│  funcion_c()  │ ← actual
├───────────────┤
│  funcion_b()  │
├───────────────┤
│  funcion_a()  │
├───────────────┤
│   programa    │
└───────────────┘
```

Cuando termina:

```text
funcion_c()
```

se elimina de la parte superior.

Después continúa:

```text
funcion_b()
```

---

### 76. Crear una práctica para Call Stack

Crea:

```text
pila_llamadas.py
```

Escribe:

```python
def calcular_iva(
    precio,
    porcentaje
):

    importe = (
        precio
        * porcentaje
        / 100
    )

    return importe


def calcular_factura(
    precio,
    porcentaje
):

    iva = calcular_iva(
        precio,
        porcentaje
    )

    total = (
        precio + iva
    )

    return total


def procesar_pedido(
    precio
):

    resultado = calcular_factura(
        precio,
        21
    )

    return resultado


total = procesar_pedido(
    100
)


print(
    f"Total: {total}"
)
```

---

### 77. Entrar en las funciones

Coloca un breakpoint en:

```python
total = procesar_pedido(
    100
)
```

Inicia:

```text
F5
```

Utiliza:

```text
F11
```

para entrar en:

```text
procesar_pedido()
```

Después vuelve a utilizar:

```text
F11
```

para entrar en:

```text
calcular_factura()
```

Y nuevamente:

```text
F11
```

para entrar en:

```text
calcular_iva()
```

Ahora observa:

```text
Call Stack
```

---

### 78. Interpretar Call Stack

Cuando estamos dentro de:

```python
calcular_iva()
```

la pila mostrará conceptualmente:

```text
calcular_iva()
       │
calcular_factura()
       │
procesar_pedido()
       │
programa principal
```

Esto responde a una pregunta muy importante:

```text
¿Cómo hemos llegado hasta aquí?
```

En programas grandes una función puede ser llamada desde muchos lugares diferentes.

Call Stack permite saber cuál ha sido el recorrido concreto.

---

### 79. Cambiar de contexto desde Call Stack

Durante la depuración podemos seleccionar diferentes elementos de la pila.

Por ejemplo:

```text
calcular_iva()
calcular_factura()
procesar_pedido()
```

Si seleccionamos:

```text
calcular_factura()
```

podemos inspeccionar las variables correspondientes a ese contexto.

Si seleccionamos:

```text
procesar_pedido()
```

podemos observar sus variables.

!!! important "No cambia la ejecución"

    Seleccionar otro elemento de Call Stack permite inspeccionar otro contexto.

    No significa que el programa retroceda en el tiempo ni vuelva a ejecutar esa función.

---

### 80. Utilidad de Call Stack

Call Stack es especialmente útil cuando aparece un error dentro de una función utilizada por otras funciones.

Por ejemplo:

```text
ERROR
  │
  ▼
guardar_resultado()
  │
  ▼
generar_informe()
  │
  ▼
procesar_equipo()
  │
  ▼
programa principal
```

Podemos investigar:

```text
quién llamó a la función
```

y:

```text
con qué valores
```

---

### 81. Introducción a Debug Console

VS Code también dispone de:

```text
Debug Console
```

o:

```text
Consola de depuración
```

Esta herramienta permite evaluar expresiones mientras el programa está detenido.

Por ejemplo, si tenemos:

```python
precio = 100
iva = 21
```

podemos escribir en Debug Console:

```python
precio
```

y obtener:

```text
100
```

También:

```python
precio * iva / 100
```

y obtener:

```text
21.0
```

---

### 82. Abrir Debug Console

Durante una sesión de depuración podemos acceder a:

```text
Debug Console
```

desde la zona inferior de VS Code.

También podemos utilizar la paleta de comandos de VS Code si no aparece visible.

El programa debe encontrarse detenido en un punto donde existan las variables que queremos consultar.

---

### 83. Evaluar expresiones

Vuelve a:

```text
analizar_pedido.py
```

Detén el programa cuando existan:

```text
precio
unidades
porcentaje_descuento
```

En Debug Console escribe:

```python
precio
```

Después:

```python
unidades
```

Después:

```python
precio * unidades
```

Y:

```python
porcentaje_descuento / 100
```

Podemos probar expresiones sin modificar el archivo `.py`.

---

### 84. Probar condiciones

También podemos escribir:

```python
precio > 20
```

Obtendremos:

```text
True
```

O:

```python
unidades == 10
```

Obtendremos:

```text
False
```

Esto es muy útil cuando investigamos una condición compleja.

Por ejemplo:

```python
precio > 20 and unidades >= 4
```

podemos evaluarla directamente.

---

### 85. Debug Console frente a terminal

No debemos confundir:

```text
Terminal
```

con:

```text
Debug Console
```

El terminal permite ejecutar comandos:

```powershell
python programa.py
```

```powershell
pip list
```

```powershell
dir
```

Debug Console trabaja con el programa que está siendo depurado.

Por ejemplo:

```python
precio
```

```python
len(equipos)
```

```python
resultado["estado"]
```

Podemos resumir:

```text
TERMINAL
   │
   └── comandos del sistema


DEBUG CONSOLE
   │
   └── expresiones del programa
       durante la depuración
```

---

### 86. Watch frente a Debug Console

Las dos herramientas permiten evaluar expresiones, pero tienen usos diferentes.

```text
WATCH
  │
  └── seguir automáticamente
      determinadas expresiones
```

```text
DEBUG CONSOLE
  │
  └── realizar consultas
      interactivas
```

Por ejemplo, si queremos observar durante toda la depuración:

```python
total
```

podemos utilizar Watch.

Si queremos probar puntualmente:

```python
total * 1.21
```

podemos utilizar Debug Console.

---

### 87. Precaución al evaluar expresiones

Durante la depuración conviene utilizar principalmente expresiones que permitan:

```text
consultar
```

el estado del programa.

Por ejemplo:

```python
len(equipos)
```

```python
equipo["nombre"]
```

```python
total > 100
```

Debemos tener más cuidado con expresiones que puedan modificar datos o producir efectos secundarios.

!!! warning "Depuración"

    Durante estas prácticas utilizaremos Debug Console principalmente para consultar valores y evaluar expresiones.

    Evitaremos utilizarla para modificar deliberadamente el estado del programa.

---

### 88. El problema de los breakpoints dentro de bucles

Consideremos:

```python
for numero in range(
    1,
    101
):

    resultado = (
        numero * 2
    )
```

Si colocamos un breakpoint en:

```python
resultado = (
    numero * 2
)
```

el programa se detendrá:

```text
100 veces
```

Pero quizá solamente nos interese:

```text
numero == 75
```

Para resolver este problema podemos utilizar:

```text
breakpoints condicionales
```

---

### 89. ¿Qué es un breakpoint condicional?

Un breakpoint normal significa:

```text
detener siempre
```

Un breakpoint condicional significa:

```text
detener solamente
si se cumple una condición
```

Por ejemplo:

```python
numero == 75
```

El flujo será:

```text
numero = 1
   │
   └── continuar

numero = 2
   │
   └── continuar

...

numero = 75
   │
   ▼
condición verdadera
   │
   ▼
DETENER
```

---

### 90. Crear una práctica

Crea:

```text
breakpoint_condicional.py
```

Escribe:

```python
for numero in range(
    1,
    101
):

    resultado = (
        numero * 2
    )

    print(
        numero,
        resultado
    )
```

Ejecuta normalmente para comprobar que funciona.

---

### 91. Crear el breakpoint

Coloca un breakpoint en:

```python
resultado = (
    numero * 2
)
```

Si ejecutamos ahora:

```text
F5
```

se detendrá desde la primera iteración.

Esto no es lo que queremos.

Queremos detenernos únicamente cuando:

```python
numero == 75
```

---

### 92. Convertirlo en breakpoint condicional

Sobre el breakpoint utiliza las opciones disponibles en VS Code para editarlo.

Una forma habitual es:

```text
clic derecho sobre el breakpoint
```

y seleccionar una opción similar a:

```text
Edit Breakpoint
```

Después seleccionamos:

```text
Expression
```

o la opción equivalente para una condición.

Escribimos:

```python
numero == 75
```

Inicia nuevamente la depuración.

---

### 93. Resultado del breakpoint condicional

El programa ejecutará automáticamente:

```text
numero = 1
numero = 2
numero = 3
...
```

sin detenerse.

Cuando:

```text
numero = 75
```

la expresión:

```python
numero == 75
```

será:

```text
True
```

y el depurador se detendrá.

Ahora podemos observar:

```text
numero
resultado
```

y el resto de variables disponibles.

---

### 94. Condiciones más complejas

Podemos utilizar condiciones como:

```python
numero > 90
```

o:

```python
numero % 10 == 0
```

También:

```python
numero >= 50 and numero <= 60
```

El breakpoint se activará cuando la expresión produzca:

```text
True
```

---

### 95. Breakpoint condicional con una lista

Crea:

```text
equipos_breakpoint.py
```

Escribe:

```python
equipos = [
    {
        "nombre": "PC01",
        "estado": "activo"
    },
    {
        "nombre": "PC02",
        "estado": "activo"
    },
    {
        "nombre": "PC03",
        "estado": "error"
    },
    {
        "nombre": "PC04",
        "estado": "activo"
    }
]


for equipo in equipos:

    nombre = equipo["nombre"]
    estado = equipo["estado"]

    print(
        nombre,
        estado
    )
```

Coloca un breakpoint en:

```python
nombre = equipo["nombre"]
```

---

### 96. Detenerse solamente ante un error

Convierte el breakpoint en condicional.

Utiliza:

```python
equipo["estado"] == "error"
```

Inicia la depuración.

El programa ignorará:

```text
PC01
PC02
```

y se detendrá cuando:

```text
equipo = {
    "nombre": "PC03",
    "estado": "error"
}
```

Este tipo de breakpoint resulta extremadamente útil cuando procesamos:

```text
listas
CSV
inventarios
respuestas de APIs
equipos de red
```

y solamente un elemento concreto produce un problema.

---

### 97. Otro ejemplo con direcciones IP

Supongamos:

```python
equipos = [
    "192.168.1.10",
    "192.168.1.20",
    "192.168.1.30",
    "192.168.1.40"
]


for ip in equipos:

    print(
        f"Comprobando {ip}"
    )
```

Podemos establecer un breakpoint condicional:

```python
ip == "192.168.1.30"
```

El programa se detendrá únicamente cuando procese esa dirección.

---

### 98. Breakpoints condicionales y diagnóstico de red

Esta técnica será especialmente útil con programas como los desarrollados en el capítulo 6.

Por ejemplo:

```python
for servicio in servicios:

    resultado = diagnosticar_servicio(
        servicio,
        timeout
    )
```

Podríamos detenernos únicamente cuando:

```python
servicio["host"] == "servidor.local"
```

o cuando:

```python
servicio["puerto"] == 443
```

Así podemos investigar un elemento concreto sin detenernos en todos los demás.

---

### 99. Crear un programa con un error difícil de localizar

Crea:

```text
buscar_error.py
```

Escribe:

```python
equipos = [
    {
        "nombre": "PC01",
        "ram": 8
    },
    {
        "nombre": "PC02",
        "ram": 16
    },
    {
        "nombre": "PC03",
        "ram": 32
    },
    {
        "nombre": "PC04",
        "ram": -8
    },
    {
        "nombre": "PC05",
        "ram": 16
    }
]


total = 0


for equipo in equipos:

    total += equipo["ram"]


print(
    f"RAM total: {total} GB"
)
```

El programa no produce ninguna excepción.

Sin embargo:

```text
PC04
```

contiene un valor imposible:

```text
RAM = -8
```

---

### 100. Buscar el dato incorrecto

Podríamos detenernos en cada iteración y observar:

```python
equipo["ram"]
```

Pero podemos utilizar un breakpoint condicional.

Colócalo en:

```python
total += equipo["ram"]
```

Utiliza como condición:

```python
equipo["ram"] < 0
```

Ejecuta:

```text
F5
```

El programa se detendrá directamente en:

```text
PC04
```

---

### 101. Analizar el problema

Ahora podemos observar en Variables:

```text
equipo
```

y expandir el diccionario.

Encontraremos:

```text
nombre    "PC04"
ram       -8
```

En Watch podemos añadir:

```python
equipo["nombre"]
```

y:

```python
equipo["ram"]
```

También podemos utilizar Debug Console:

```python
equipo["ram"] < 0
```

Obtendremos:

```text
True
```

Hemos utilizado tres herramientas sobre el mismo problema:

```text
breakpoint condicional
+
Watch
+
Debug Console
```

---

### 102. Utilizar Call Stack con errores

Ahora crearemos una versión con funciones.

Crea:

```text
buscar_error_funciones.py
```

Escribe:

```python
def validar_ram(
    equipo
):

    if equipo["ram"] < 0:

        return False

    return True


def procesar_equipo(
    equipo
):

    valido = validar_ram(
        equipo
    )

    return valido


def procesar_inventario(
    equipos
):

    for equipo in equipos:

        valido = procesar_equipo(
            equipo
        )

        if not valido:

            print(
                "Equipo incorrecto:",
                equipo["nombre"]
            )


equipos = [
    {
        "nombre": "PC01",
        "ram": 8
    },
    {
        "nombre": "PC02",
        "ram": 16
    },
    {
        "nombre": "PC03",
        "ram": -4
    }
]


procesar_inventario(
    equipos
)
```

---

### 103. Investigar la cadena de llamadas

Coloca un breakpoint en:

```python
if equipo["ram"] < 0:
```

Hazlo condicional:

```python
equipo["ram"] < 0
```

Ejecuta:

```text
F5
```

Cuando el programa se detenga observa:

```text
Call Stack
```

Conceptualmente tendremos:

```text
validar_ram()
       │
       ▼
procesar_equipo()
       │
       ▼
procesar_inventario()
       │
       ▼
programa principal
```

Ahora sabemos:

```text
dónde estamos
```

y también:

```text
cómo hemos llegado hasta allí
```

---

### 104. Inspeccionar cada nivel

Selecciona en Call Stack:

```text
validar_ram()
```

Observa:

```text
equipo
```

Después selecciona:

```text
procesar_equipo()
```

Observa sus variables.

Después:

```text
procesar_inventario()
```

Podremos examinar:

```text
equipos
equipo
```

en el contexto correspondiente.

Esto permite reconstruir el recorrido del programa.

---

### 105. Combinar las herramientas del depurador

En una investigación real no utilizaremos necesariamente una única herramienta.

Podemos combinar:

```text
BREAKPOINT
    │
    ▼
detener ejecución
    │
    ▼
VARIABLES
    │
    ▼
observar estado
    │
    ▼
WATCH
    │
    ▼
seguir expresiones
    │
    ▼
DEBUG CONSOLE
    │
    ▼
probar expresiones
    │
    ▼
CALL STACK
    │
    ▼
analizar llamadas
```

Cada herramienta responde a una pregunta diferente.

---

### 106. Qué herramienta utilizar

Podemos utilizar esta referencia:

| Necesidad | Herramienta |
|---|---|
| Detener el programa | Breakpoint |
| Ver variables actuales | Variables |
| Seguir una expresión | Watch |
| Probar una expresión | Debug Console |
| Saber cómo llegamos a una función | Call Stack |
| Detenernos ante una condición concreta | Breakpoint condicional |
| Avanzar una línea | Step Over |
| Entrar en una función | Step Into |
| Salir de una función | Step Out |

No es necesario utilizar todas las herramientas en cada depuración.

---

### 107. Práctica guiada: analizar un inventario

Crea:

```text
depurar_inventario.py
```

Escribe:

```python
def calcular_total_ram(
    equipos
):

    total = 0

    for equipo in equipos:

        total += equipo["ram"]

    return total


equipos = [
    {
        "nombre": "PC01",
        "ram": 8
    },
    {
        "nombre": "PC02",
        "ram": 16
    },
    {
        "nombre": "PC03",
        "ram": 32
    },
    {
        "nombre": "PC04",
        "ram": -16
    },
    {
        "nombre": "PC05",
        "ram": 8
    }
]


total_ram = calcular_total_ram(
    equipos
)


print(
    f"RAM total: "
    f"{total_ram} GB"
)
```

El programa funciona, pero los datos contienen un error.

---

### 108. Objetivos de la práctica

Realiza los siguientes pasos:

1. Coloca un breakpoint en:

```python
total += equipo["ram"]
```

2. Conviértelo en condicional:

```python
equipo["ram"] < 0
```

3. Inicia la depuración.

4. Observa:

```text
Variables
```

5. Añade a Watch:

```python
equipo["nombre"]
```

```python
equipo["ram"]
```

```python
total
```

6. En Debug Console consulta:

```python
equipo["ram"] < 0
```

7. Observa Call Stack.

8. Identifica el equipo incorrecto.

9. Corrige el dato.

10. Ejecuta nuevamente el programa.

---

### 109. Práctica propuesta: localizar un código HTTP incorrecto

Crea:

```text
codigos_http.py
```

Escribe:

```python
respuestas = [
    {
        "url": "servicio1",
        "codigo": 200
    },
    {
        "url": "servicio2",
        "codigo": 201
    },
    {
        "url": "servicio3",
        "codigo": 404
    },
    {
        "url": "servicio4",
        "codigo": 200
    },
    {
        "url": "servicio5",
        "codigo": 500
    }
]


for respuesta in respuestas:

    codigo = respuesta["codigo"]

    print(
        respuesta["url"],
        codigo
    )
```

Crea un breakpoint condicional para detener el programa únicamente cuando:

```python
codigo >= 400
```

!!! note "Posición del breakpoint"

    La condición solamente puede utilizar una variable que ya exista en el punto donde se evalúa el breakpoint.

    Si colocas el breakpoint antes de asignar:

    ```python
    codigo = respuesta["codigo"]
    ```

    utiliza directamente:

    ```python
    respuesta["codigo"] >= 400
    ```

---

### 110. Práctica propuesta: combinar varias condiciones

Sobre el programa anterior intenta detenerte únicamente cuando:

```text
el código sea 500
```

Puedes utilizar:

```python
respuesta["codigo"] == 500
```

Después intenta una condición que detecte cualquier error:

```python
respuesta["codigo"] >= 400
```

Compara ambas ejecuciones.

---

### 111. Práctica propuesta: depurar funciones encadenadas

Crea un programa con estas funciones:

```text
leer_dato()
    │
    ▼
validar_dato()
    │
    ▼
procesar_dato()
    │
    ▼
mostrar_resultado()
```

Introduce deliberadamente un valor incorrecto.

Utiliza:

```text
Step Into
Call Stack
Variables
Watch
Debug Console
```

para seguir el dato desde que entra en el programa hasta que produce el resultado.

El objetivo es comprender:

```text
cómo viajan los datos
entre las funciones
```

---

### 112. Estrategia para investigar un error

Cuando encontremos un problema podemos utilizar un procedimiento como:

```text
1. Reproducir el problema
          │
          ▼
2. Identificar una zona sospechosa
          │
          ▼
3. Colocar breakpoint
          │
          ▼
4. Ejecutar con el depurador
          │
          ▼
5. Examinar Variables
          │
          ▼
6. Utilizar Watch
          │
          ▼
7. Seguir la ejecución
          │
          ▼
8. Consultar Call Stack
          │
          ▼
9. Probar expresiones
   en Debug Console
          │
          ▼
10. Localizar la causa
          │
          ▼
11. Corregir
          │
          ▼
12. Volver a probar
```

Esta metodología evita modificar el programa al azar.

---

### 113. Síntoma y causa

Un concepto importante durante la depuración es diferenciar:

```text
síntoma
```

de:

```text
causa
```

Por ejemplo:

```text
SÍNTOMA

total = 92
```

pero la causa podría estar varias funciones antes:

```text
precio incorrecto
```

o:

```text
porcentaje incorrecto
```

o:

```text
dato leído incorrectamente
```

El lugar donde observamos el error no siempre es el lugar donde se originó.

---

### 114. Ejemplo de propagación de un error

Podemos tener:

```text
CSV
 │
 ▼
dato incorrecto
 │
 ▼
leer_inventario()
 │
 ▼
procesar_equipo()
 │
 ▼
calcular_total()
 │
 ▼
informe incorrecto
```

El informe contiene el:

```text
síntoma
```

pero la causa puede encontrarse en:

```text
CSV
```

o durante su procesamiento.

Herramientas como:

```text
Call Stack
Watch
breakpoints
```

nos ayudan a seguir el recorrido del dato.

---

### 115. No modificar varias cosas simultáneamente

Si sospechamos de cinco partes diferentes y modificamos todas a la vez:

```text
cambio A
cambio B
cambio C
cambio D
cambio E
```

aunque el programa empiece a funcionar no sabremos necesariamente cuál era la causa.

Durante una depuración sistemática es preferible:

```text
observar
   │
   ▼
formular hipótesis
   │
   ▼
comprobar
   │
   ▼
realizar cambio
   │
   ▼
volver a comprobar
```

---

### 116. Breakpoints frente a `print()`

Comparemos.

Con `print()`:

```python
print(
    "DEBUG:",
    variable
)
```

modificamos temporalmente el código.

Con un breakpoint:

```text
detenemos
   │
   ▼
inspeccionamos
   │
   ▼
continuamos
```

sin necesidad de añadir instrucciones de diagnóstico al archivo.

Esto no significa que `print()` sea inútil.

Significa que disponemos de herramientas más adecuadas cuando el análisis se vuelve complejo.

---

### 117. Breakpoints frente a logging

También debemos recordar:

```text
BREAKPOINT
    │
    ▼
investigación interactiva
durante el desarrollo
```

mientras:

```text
LOGGING
    │
    ▼
registro de información
durante la ejecución
```

Por ejemplo, un problema que ocurre en un equipo remoto podría detectarse inicialmente mediante:

```text
logs
```

y después reproducirse en nuestro entorno para analizarlo con:

```text
debugger
```

---

### 118. Práctica integradora de esta parte

Crea:

```text
diagnostico_equipos_debug.py
```

con:

```python
def validar_equipo(
    equipo
):

    if not equipo["nombre"]:

        return False

    if equipo["ram"] <= 0:

        return False

    return True


def contar_validos(
    equipos
):

    contador = 0

    for equipo in equipos:

        if validar_equipo(
            equipo
        ):

            contador += 1

    return contador


equipos = [
    {
        "nombre": "PC01",
        "ram": 8
    },
    {
        "nombre": "PC02",
        "ram": 16
    },
    {
        "nombre": "",
        "ram": 32
    },
    {
        "nombre": "PC04",
        "ram": -8
    },
    {
        "nombre": "PC05",
        "ram": 16
    }
]


validos = contar_validos(
    equipos
)


print(
    f"Equipos válidos: "
    f"{validos}"
)
```

No modifiques inicialmente los datos.

---

### 119. Primera investigación

Coloca un breakpoint dentro de:

```python
validar_equipo()
```

en:

```python
if not equipo["nombre"]:
```

Ejecuta el programa.

Observa cómo la función se ejecuta para cada equipo.

Después detén la depuración.

---

### 120. Mejorar la investigación

Ahora convierte el breakpoint en condicional.

Queremos detenernos cuando:

```python
not equipo["nombre"]
```

Ejecuta nuevamente.

El programa se detendrá únicamente en el equipo cuyo nombre está vacío.

Observa:

```text
Variables
Watch
Call Stack
```

---

### 121. Segundo problema

Ahora queremos localizar:

```text
RAM <= 0
```

Modifica la condición del breakpoint:

```python
equipo["ram"] <= 0
```

Ejecuta de nuevo.

El programa deberá detenerse en:

```text
PC04
```

con:

```text
ram = -8
```

---

### 122. Utilizar Debug Console

Mientras el programa está detenido prueba:

```python
equipo
```

Después:

```python
equipo["nombre"]
```

Después:

```python
equipo["ram"]
```

Y:

```python
equipo["ram"] <= 0
```

Podemos investigar el problema sin modificar el código.

---

### 123. Analizar Call Stack

Cuando estamos dentro de:

```python
validar_equipo()
```

la pila será aproximadamente:

```text
validar_equipo()
       │
       ▼
contar_validos()
       │
       ▼
programa principal
```

Podemos seleccionar:

```text
contar_validos()
```

para observar el estado del bucle que llamó a:

```python
validar_equipo()
```

Esta información resulta especialmente útil cuando una función es utilizada desde diferentes lugares.

---

### 124. Reto de depuración

Sin utilizar inicialmente `print()` adicionales, crea una copia:

```text
diagnostico_equipos_error.py
```

e introduce varios problemas deliberadamente:

```text
un nombre vacío
una RAM negativa
una RAM igual a cero
```

Después utiliza exclusivamente:

```text
breakpoints condicionales
Variables
Watch
Debug Console
Call Stack
```

para localizar cada elemento incorrecto.

Registra en una tabla:

```text
Equipo | Problema | Herramienta utilizada
```

Por ejemplo:

```text
PC04 | RAM negativa | Breakpoint condicional
```

El objetivo no es únicamente encontrar los errores.

El objetivo es elegir la herramienta de depuración adecuada.

---

### 125. Flujo profesional de depuración

Podemos resumir el proceso estudiado hasta ahora:

```text
          PROBLEMA
              │
              ▼
        reproducir error
              │
              ▼
      localizar zona probable
              │
              ▼
          breakpoint
              │
              ▼
           Variables
              │
       ┌──────┼──────┐
       │      │      │
       ▼      ▼      ▼
     Watch   Stack  Console
       │      │      │
       └──────┼──────┘
              │
              ▼
        seguir ejecución
              │
              ▼
       identificar causa
              │
              ▼
           corregir
              │
              ▼
          comprobar
```

---

### 126. Qué hemos añadido al depurador

En la primera parte utilizamos:

```text
Breakpoints
Variables
Continue
Step Over
Step Into
Step Out
```

Ahora añadimos:

```text
Watch
Call Stack
Debug Console
Breakpoints condicionales
```

Nuestro conjunto de herramientas es ya suficiente para analizar programas considerablemente más complejos.

---

### 127. Resumen de esta segunda parte

En esta parte hemos profundizado en las herramientas de depuración de Visual Studio Code.

Hemos utilizado:

```text
Variables
```

para inspeccionar el estado actual del programa.

Hemos utilizado:

```text
Watch
```

para seguir variables y expresiones concretas.

Hemos aprendido a interpretar:

```text
Call Stack
```

para comprender la cadena de llamadas entre funciones.

También hemos utilizado:

```text
Debug Console
```

para evaluar expresiones mientras el programa está detenido.

Finalmente hemos trabajado con:

```text
breakpoints condicionales
```

que permiten detener la ejecución solamente cuando se cumple una condición determinada.

Podemos resumir:

```text
             DEBUGGER
                 │
      ┌──────────┼──────────┐
      │          │          │
      ▼          ▼          ▼
  Breakpoint  Variables    Watch
      │                     │
      ▼                     ▼
   detener               observar
      │
      └──────────┬──────────┘
                 │
          ┌──────┴──────┐
          │             │
          ▼             ▼
     Call Stack    Debug Console
          │             │
          ▼             ▼
       llamadas      expresiones
```

En la siguiente parte realizaremos la **práctica integradora y cierre del Capítulo 7**.

Utilizaremos el depurador sobre un programa más próximo a los desarrollados durante el curso, combinando:

```text
CSV
funciones
diccionarios
validación
excepciones
logging
```

e introduciremos deliberadamente varios errores para aplicar un proceso completo de diagnóstico.

Con esa práctica quedará completada la unidad de **Depuración profesional en VS Code** y estaremos preparados para comenzar el **proyecto final integrador del curso**.

---

## 128. Práctica integradora: depuración de una aplicación completa

Hasta ahora hemos aprendido a utilizar las principales herramientas del depurador de Visual Studio Code:

```text
Breakpoints
Variables
Watch
Call Stack
Debug Console
Breakpoints condicionales
Step Over
Step Into
Step Out
```

En esta práctica utilizaremos estas herramientas sobre un programa más completo.

El programa gestionará un pequeño inventario de equipos almacenado en un archivo CSV.

El objetivo no será únicamente conseguir que el programa funcione.

Nuestro objetivo principal será:

```text
LOCALIZAR
    │
    ▼
COMPRENDER
    │
    ▼
CORREGIR
    │
    ▼
COMPROBAR
```

los errores mediante el depurador.

!!! important "No corregir directamente"

    El programa contiene varios errores introducidos deliberadamente.

    No debemos corregirlos simplemente leyendo el código.

    Primero utilizaremos el depurador para obtener evidencias sobre qué está ocurriendo.

---

### 129. Objetivos de la práctica

Durante esta práctica tendremos que:

1. Ejecutar un programa con errores.
2. Analizar los resultados obtenidos.
3. Formular hipótesis.
4. Colocar breakpoints.
5. Inspeccionar variables.
6. Utilizar Watch.
7. Ejecutar paso a paso.
8. Entrar dentro de funciones.
9. Consultar Call Stack.
10. Utilizar Debug Console.
11. Crear breakpoints condicionales.
12. Localizar errores lógicos.
13. Corregirlos.
14. Comprobar nuevamente el programa.

El proceso será:

```text
problema
   │
   ▼
reproducir
   │
   ▼
investigar
   │
   ▼
localizar
   │
   ▼
corregir
   │
   ▼
volver a probar
```

---

### 130. Estructura de la práctica

Utilizaremos:

```text
practicas/
└── capitulo7/
    ├── datos/
    │   └── inventario.csv
    │
    ├── logs/
    │   └── inventario.log
    │
    ├── programas/
    │   └── gestor_inventario_debug.py
    │
    └── resultados/
```

Crea los directorios necesarios antes de continuar.

---

### 131. Crear el archivo CSV

Crea:

```text
practicas/capitulo7/datos/inventario.csv
```

Escribe:

```csv
nombre,ip,ram,estado
PC01,192.168.1.10,8,activo
PC02,192.168.1.11,16,activo
PC03,192.168.1.12,32,inactivo
PC04,192.168.1.13,-8,activo
PC05,192.168.1.14,16,activo
PC06,192.168.1.15,8,inactivo
```

Observa que uno de los datos es incorrecto.

Sin embargo, inicialmente no modificaremos el CSV.

---

### 132. Qué debería hacer la aplicación

Nuestro programa deberá:

```text
leer inventario.csv
        │
        ▼
convertir los datos
        │
        ▼
validar equipos
        │
        ▼
calcular estadísticas
        │
        ▼
mostrar resultados
        │
        ▼
registrar ejecución
```

Queremos obtener información como:

```text
número total de equipos
equipos activos
equipos inactivos
RAM total
RAM media
equipos incorrectos
```

---

### 133. Crear el programa con errores

Crea:

```text
practicas/capitulo7/programas/
gestor_inventario_debug.py
```

Escribe exactamente el siguiente programa.

No corrijas todavía nada.

```python
import csv
import logging

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
    / "inventario.csv"
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
    / "inventario.log"
)


logging.basicConfig(
    filename=ARCHIVO_LOG,
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    ),
    encoding="utf-8"
)


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

            equipo = {
                "nombre": fila["nombre"],
                "ip": fila["ip"],
                "ram": int(
                    fila["ram"]
                ),
                "estado": fila["estado"]
            }

            equipos.append(
                equipo
            )

    return equipos


def equipo_valido(
    equipo
):

    if equipo["ram"] < 0:

        return True

    if not equipo["nombre"]:

        return False

    return True


def contar_activos(
    equipos
):

    activos = 0

    for equipo in equipos:

        if equipo["estado"] == "inactivo":

            activos += 1

    return activos


def calcular_ram_total(
    equipos
):

    total = 0

    for equipo in equipos:

        total = equipo["ram"]

    return total


def calcular_ram_media(
    total,
    numero_equipos
):

    return (
        total / numero_equipos
    )


def obtener_equipos_validos(
    equipos
):

    validos = []

    for equipo in equipos:

        if equipo_valido(
            equipo
        ):

            validos.append(
                equipo
            )

    return validos


def mostrar_resumen(
    equipos
):

    validos = obtener_equipos_validos(
        equipos
    )

    numero_equipos = len(
        validos
    )

    activos = contar_activos(
        validos
    )

    ram_total = calcular_ram_total(
        validos
    )

    ram_media = calcular_ram_media(
        ram_total,
        numero_equipos
    )

    print(
        f"Equipos válidos: "
        f"{numero_equipos}"
    )

    print(
        f"Equipos activos: "
        f"{activos}"
    )

    print(
        f"RAM total: "
        f"{ram_total} GB"
    )

    print(
        f"RAM media: "
        f"{ram_media:.2f} GB"
    )


logging.info(
    "Inicio del programa"
)


equipos = cargar_inventario(
    ARCHIVO_INVENTARIO
)


mostrar_resumen(
    equipos
)


logging.info(
    "Fin del programa"
)
```

---

### 134. Primera ejecución

Ejecuta normalmente:

```powershell
python gestor_inventario_debug.py
```

El programa terminará sin mostrar necesariamente una excepción.

Sin embargo, los resultados obtenidos no coincidirán con los esperados.

Esto es precisamente lo que queremos investigar.

Tenemos:

```text
programa ejecutado
        │
        ▼
sin excepción
        │
        ▼
resultado incorrecto
        │
        ▼
ERROR LÓGICO
```

---

### 135. No buscar todos los errores a la vez

El programa contiene varios problemas.

No intentaremos encontrarlos todos simultáneamente.

Seguiremos este procedimiento:

```text
ERROR 1
   │
   ▼
localizar
   │
   ▼
corregir
   │
   ▼
probar

ERROR 2
   │
   ▼
localizar
   │
   ▼
corregir
   │
   ▼
probar

...
```

Este método facilita saber qué modificación ha corregido cada problema.

---

### 136. Primera investigación: validación de equipos

Sabemos que nuestro CSV contiene:

```text
PC04
RAM = -8
```

Una cantidad negativa de memoria RAM debe considerarse incorrecta.

Coloca un breakpoint en:

```python
if equipo["ram"] < 0:
```

Pero si utilizamos un breakpoint normal se detendrá para todos los equipos.

Conviértelo en un breakpoint condicional:

```python
equipo["ram"] < 0
```

Inicia:

```text
F5
```

---

### 137. Examinar PC04

Cuando el programa se detenga utiliza el panel:

```text
Variables
```

Busca:

```text
equipo
```

Deberíamos encontrar:

```text
nombre = PC04
ip = 192.168.1.13
ram = -8
estado = activo
```

Añade a Watch:

```python
equipo["nombre"]
```

```python
equipo["ram"]
```

```python
equipo["ram"] < 0
```

---

### 138. Utilizar Debug Console

En Debug Console prueba:

```python
equipo["ram"]
```

Después:

```python
equipo["ram"] < 0
```

Obtendremos:

```text
True
```

Ahora utiliza:

```text
F10
```

para ejecutar la siguiente instrucción.

Observa qué devuelve la función.

---

### 139. Primer error localizado

Tenemos:

```python
if equipo["ram"] < 0:

    return True
```

Esto significa:

```text
RAM negativa
     │
     ▼
equipo válido
```

La lógica es incorrecta.

Debe ser:

```python
if equipo["ram"] <= 0:

    return False
```

Corrige:

```python
def equipo_valido(
    equipo
):

    if equipo["ram"] <= 0:

        return False

    if not equipo["nombre"]:

        return False

    return True
```

Ahora vuelve a ejecutar el programa.

---

### 140. Registrar nuestra investigación

Podemos llevar una pequeña tabla durante la práctica:

| Problema | Evidencia | Causa | Corrección |
|---|---|---|---|
| PC04 aceptado | `ram = -8` | `equipo_valido()` devuelve `True` | devolver `False` |

Esta forma de documentar una depuración es muy útil.

No escribimos simplemente:

```text
estaba mal
```

sino:

```text
síntoma
+
evidencia
+
causa
+
solución
```

---

### 141. Segunda investigación: número de equipos activos

Después de corregir la validación, analiza:

```text
Equipos activos
```

Observa el CSV.

Entre los equipos válidos tenemos varios estados:

```text
activo
inactivo
```

Queremos contar:

```text
activo
```

Coloca un breakpoint en:

```python
if equipo["estado"] == "inactivo":
```

---

### 142. Observar el bucle

Añade a Watch:

```python
equipo["nombre"]
```

```python
equipo["estado"]
```

```python
activos
```

Utiliza:

```text
F10
```

para recorrer varias iteraciones.

Observa cuándo aumenta:

```text
activos
```

---

### 143. Segundo error localizado

El programa utiliza:

```python
if equipo["estado"] == "inactivo":

    activos += 1
```

Por tanto está contando:

```text
equipos inactivos
```

aunque la función se llama:

```python
contar_activos()
```

La condición correcta es:

```python
if equipo["estado"] == "activo":

    activos += 1
```

Corrige el programa.

---

### 144. Utilizar un breakpoint condicional

También podríamos haber investigado utilizando:

```python
equipo["estado"] == "inactivo"
```

como condición del breakpoint.

Esto nos habría permitido detenernos solamente cuando apareciera uno de esos equipos.

Podemos utilizar breakpoints condicionales para comprobar hipótesis concretas.

---

### 145. Tercera investigación: RAM total

Ahora observa:

```text
RAM total
```

La cantidad mostrada sigue sin ser correcta.

Coloca un breakpoint en:

```python
total = equipo["ram"]
```

Añade a Watch:

```python
equipo["nombre"]
```

```python
equipo["ram"]
```

```python
total
```

Inicia nuevamente la depuración.

---

### 146. Seguir el acumulador

En la primera iteración tendremos aproximadamente:

```text
equipo = PC01
ram = 8
```

Después:

```text
total = 8
```

En la siguiente:

```text
equipo = PC02
ram = 16
```

Después:

```text
total = 16
```

Pero esperábamos:

```text
8 + 16 = 24
```

El valor anterior se ha perdido.

---

### 147. Tercer error localizado

La instrucción:

```python
total = equipo["ram"]
```

sustituye el valor anterior.

Necesitamos acumular:

```python
total += equipo["ram"]
```

que equivale a:

```python
total = (
    total
    + equipo["ram"]
)
```

Corrige:

```python
def calcular_ram_total(
    equipos
):

    total = 0

    for equipo in equipos:

        total += equipo["ram"]

    return total
```

---

### 148. Comprobar la RAM media

La función:

```python
calcular_ram_media()
```

utiliza:

```python
return (
    total / numero_equipos
)
```

Una vez corregido:

```text
RAM total
```

debemos comprobar si:

```text
RAM media
```

también se corrige.

Este punto es importante.

Un resultado incorrecto puede ser consecuencia de un error anterior.

Podemos tener:

```text
RAM total incorrecta
        │
        ▼
RAM media incorrecta
```

La RAM media era un:

```text
síntoma
```

pero no necesariamente contenía un error propio.

---

### 149. Dependencia entre resultados

Podemos representar:

```text
equipos válidos
      │
      ▼
RAM total
      │
      ▼
RAM media
```

Si:

```text
equipos válidos
```

es incorrecto, puede afectar a:

```text
RAM total
RAM media
```

Por eso no debemos asumir que cada resultado incorrecto corresponde a un error diferente.

---

### 150. Utilizar Call Stack

Coloca un breakpoint dentro de:

```python
calcular_ram_media()
```

en:

```python
return (
    total / numero_equipos
)
```

Inicia la depuración.

Observa:

```text
Call Stack
```

La cadena será aproximadamente:

```text
calcular_ram_media()
        │
        ▼
mostrar_resumen()
        │
        ▼
programa principal
```

---

### 151. Inspeccionar el nivel anterior

Selecciona en Call Stack:

```text
mostrar_resumen()
```

Observa:

```text
validos
numero_equipos
activos
ram_total
```

Después vuelve a:

```text
calcular_ram_media()
```

Observa:

```text
total
numero_equipos
```

Esto nos permite comprobar qué valores ha recibido la función.

---

### 152. Una función puede ser correcta y recibir datos incorrectos

Supongamos:

```python
def dividir(
    a,
    b
):

    return a / b
```

La función puede ser completamente correcta.

Pero si recibe:

```text
a = 1000
```

cuando debería recibir:

```text
a = 100
```

el resultado será incorrecto.

El error puede encontrarse:

```text
antes de llamar
a la función
```

Por eso Call Stack resulta útil para investigar el origen de los datos.

---

### 153. Comprobar los resultados esperados

Después de eliminar el equipo con RAM negativa tenemos como equipos válidos:

```text
PC01 → 8 GB
PC02 → 16 GB
PC03 → 32 GB
PC05 → 16 GB
PC06 → 8 GB
```

Número de equipos válidos:

```text
5
```

Equipos activos:

```text
PC01
PC02
PC05
```

Por tanto:

```text
3
```

RAM total:

```text
8 + 16 + 32 + 16 + 8
```

Resultado:

```text
80 GB
```

RAM media:

```text
80 / 5
```

Resultado:

```text
16 GB
```

La salida correcta debería ser:

```text
Equipos válidos: 5
Equipos activos: 3
RAM total: 80 GB
RAM media: 16.00 GB
```

---

### 154. Corregir también el dato

Hasta ahora hemos corregido el programa para que detecte:

```text
RAM <= 0
```

Pero el archivo CSV sigue conteniendo:

```text
PC04,192.168.1.13,-8,activo
```

En una situación real tendríamos que investigar por qué existe ese dato.

Podría ser:

```text
error de introducción
```

```text
error de importación
```

```text
dato corrupto
```

```text
problema de origen
```

Nuestro programa debe validar los datos, pero también puede ser necesario corregir el origen.

---

### 155. Errores de datos frente a errores de código

En esta práctica tenemos dos categorías:

```text
ERROR DE DATOS
```

Ejemplo:

```text
RAM = -8
```

y:

```text
ERROR DE CÓDIGO
```

Ejemplo:

```python
if equipo["ram"] < 0:
    return True
```

Debemos aprender a diferenciarlos.

Un programa correctamente diseñado debe ser capaz de detectar muchos datos incorrectos sin fallar.

---

### 156. Añadir logging a la validación

Podemos mejorar:

```python
equipo_valido()
```

para registrar los datos incorrectos.

Por ejemplo:

```python
def equipo_valido(
    equipo
):

    if equipo["ram"] <= 0:

        logging.warning(
            f"RAM incorrecta: "
            f"{equipo['nombre']} "
            f"({equipo['ram']} GB)"
        )

        return False

    if not equipo["nombre"]:

        logging.warning(
            "Equipo sin nombre"
        )

        return False

    return True
```

Ahora el programa no solamente rechaza el dato.

También deja constancia del motivo.

---

### 157. Comprobar el archivo de log

Después de ejecutar el programa consulta:

```text
practicas/capitulo7/logs/
inventario.log
```

Podremos encontrar una entrada similar a:

```text
WARNING - RAM incorrecta: PC04 (-8 GB)
```

Estamos combinando:

```text
VALIDACIÓN
    │
    ▼
detecta problema

LOGGING
    │
    ▼
registra problema

DEBUGGER
    │
    ▼
investiga problema
```

---

### 158. Introducir un nuevo error

Vamos a practicar con un problema diferente.

Modifica temporalmente el CSV:

```csv
nombre,ip,ram,estado
PC01,192.168.1.10,8,activo
PC02,192.168.1.11,dieciseis,activo
PC03,192.168.1.12,32,inactivo
PC04,192.168.1.13,8,activo
PC05,192.168.1.14,16,activo
PC06,192.168.1.15,8,inactivo
```

Ahora:

```text
PC02
```

contiene:

```text
dieciseis
```

en lugar de:

```text
16
```

Ejecuta el programa.

---

### 159. Aparece una excepción

Esta vez el programa no termina normalmente.

La causa aparece cuando intentamos:

```python
int(
    fila["ram"]
)
```

Python no puede convertir:

```text
"dieciseis"
```

en un entero.

Obtendremos una excepción:

```text
ValueError
```

Ahora tenemos un problema diferente a los anteriores.

---

### 160. Depurar una excepción

Coloca un breakpoint dentro de:

```python
cargar_inventario()
```

en:

```python
equipo = {
```

Utiliza:

```text
F10
```

para recorrer las filas.

Añade a Watch:

```python
fila["nombre"]
```

```python
fila["ram"]
```

Cuando lleguemos a:

```text
PC02
```

veremos:

```text
fila["ram"] = "dieciseis"
```

---

### 161. Utilizar Debug Console

Antes de ejecutar la conversión prueba en Debug Console:

```python
fila["ram"]
```

Obtendremos:

```text
'dieciseis'
```

Podemos comprobar:

```python
fila["ram"].isdigit()
```

El resultado será:

```text
False
```

Esto nos proporciona información sobre el dato antes de ejecutar la conversión.

---

### 162. Gestionar la conversión

Podemos mejorar la carga:

```python
try:

    ram = int(
        fila["ram"]
    )

except ValueError:

    logging.warning(
        f"RAM no válida: "
        f"{fila['nombre']} - "
        f"{fila['ram']}"
    )

    continue
```

Después:

```python
equipo = {
    "nombre": fila["nombre"],
    "ip": fila["ip"],
    "ram": ram,
    "estado": fila["estado"]
}
```

Ahora una fila incorrecta no detendrá necesariamente todo el programa.

---

### 163. Excepciones y depuración

Este ejemplo muestra la relación entre dos herramientas estudiadas.

Podemos utilizar:

```text
try / except
```

para gestionar una situación prevista.

Y podemos utilizar:

```text
debugger
```

para investigar:

```text
qué dato produjo
la excepción
```

No son herramientas alternativas.

Se complementan.

---

### 164. Programa corregido

Después de la investigación podemos construir una versión corregida.

```python
import csv
import logging

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
    / "inventario.csv"
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
    / "inventario.log"
)


logging.basicConfig(
    filename=ARCHIVO_LOG,
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    ),
    encoding="utf-8"
)


def cargar_inventario(
    archivo
):

    equipos = []

    try:

        fichero = archivo.open(
            "r",
            encoding="utf-8",
            newline=""
        )

    except OSError as error:

        logging.error(
            f"No se puede abrir "
            f"el inventario: {error}"
        )

        return None

    with fichero:

        lector = csv.DictReader(
            fichero
        )

        for fila in lector:

            try:

                ram = int(
                    fila["ram"]
                )

            except (
                ValueError,
                TypeError
            ):

                logging.warning(
                    f"RAM no válida: "
                    f"{fila.get('nombre')} - "
                    f"{fila.get('ram')}"
                )

                continue

            try:

                equipo = {
                    "nombre": (
                        fila["nombre"].strip()
                    ),
                    "ip": (
                        fila["ip"].strip()
                    ),
                    "ram": ram,
                    "estado": (
                        fila["estado"].strip()
                    )
                }

            except (
                KeyError,
                AttributeError
            ):

                logging.warning(
                    f"Fila incorrecta: "
                    f"{fila}"
                )

                continue

            equipos.append(
                equipo
            )

    return equipos


def equipo_valido(
    equipo
):

    if not equipo["nombre"]:

        logging.warning(
            "Equipo sin nombre"
        )

        return False

    if equipo["ram"] <= 0:

        logging.warning(
            f"RAM incorrecta: "
            f"{equipo['nombre']} "
            f"({equipo['ram']} GB)"
        )

        return False

    if equipo["estado"] not in (
        "activo",
        "inactivo"
    ):

        logging.warning(
            f"Estado incorrecto: "
            f"{equipo['nombre']} - "
            f"{equipo['estado']}"
        )

        return False

    return True


def contar_activos(
    equipos
):

    activos = 0

    for equipo in equipos:

        if equipo["estado"] == "activo":

            activos += 1

    return activos


def calcular_ram_total(
    equipos
):

    total = 0

    for equipo in equipos:

        total += equipo["ram"]

    return total


def calcular_ram_media(
    total,
    numero_equipos
):

    if numero_equipos == 0:

        return 0

    return (
        total / numero_equipos
    )


def obtener_equipos_validos(
    equipos
):

    validos = []

    for equipo in equipos:

        if equipo_valido(
            equipo
        ):

            validos.append(
                equipo
            )

    return validos


def mostrar_resumen(
    equipos
):

    validos = obtener_equipos_validos(
        equipos
    )

    numero_equipos = len(
        validos
    )

    activos = contar_activos(
        validos
    )

    inactivos = (
        numero_equipos
        - activos
    )

    ram_total = calcular_ram_total(
        validos
    )

    ram_media = calcular_ram_media(
        ram_total,
        numero_equipos
    )

    print(
        f"Equipos válidos: "
        f"{numero_equipos}"
    )

    print(
        f"Equipos activos: "
        f"{activos}"
    )

    print(
        f"Equipos inactivos: "
        f"{inactivos}"
    )

    print(
        f"RAM total: "
        f"{ram_total} GB"
    )

    print(
        f"RAM media: "
        f"{ram_media:.2f} GB"
    )


logging.info(
    "Inicio del programa"
)


equipos = cargar_inventario(
    ARCHIVO_INVENTARIO
)


if equipos is None:

    print(
        "No se puede cargar "
        "el inventario."
    )

    raise SystemExit(1)


mostrar_resumen(
    equipos
)


logging.info(
    "Fin del programa"
)
```

---

### 165. No basta con que el programa funcione

Después de realizar una corrección debemos comprobar diferentes situaciones.

Por ejemplo:

```text
CSV correcto
```

```text
RAM negativa
```

```text
RAM igual a cero
```

```text
RAM no numérica
```

```text
nombre vacío
```

```text
estado desconocido
```

```text
archivo inexistente
```

La corrección de un error no debe introducir otros problemas.

---

### 166. Pruebas de regresión

Cuando corregimos un error debemos comprobar que las partes que funcionaban anteriormente continúan funcionando.

A esto se relaciona el concepto de:

```text
regresión
```

Una modificación puede corregir:

```text
problema A
```

pero provocar:

```text
problema B
```

Por eso después de una corrección debemos volver a probar el programa.

---

### 167. Tabla de pruebas

Podemos preparar:

| Prueba | Resultado esperado |
|---|---|
| Inventario correcto | Procesamiento normal |
| RAM negativa | Equipo rechazado |
| RAM cero | Equipo rechazado |
| RAM no numérica | Fila ignorada y warning |
| Nombre vacío | Equipo rechazado |
| Estado desconocido | Equipo rechazado |
| Archivo inexistente | Error controlado |

Ejecuta varias de estas pruebas.

Consulta también:

```text
inventario.log
```

para comprobar que los errores quedan registrados.

---

### 168. Reto: error de estado

Modifica temporalmente:

```csv
PC05,192.168.1.14,16,encendido
```

Nuestro programa solamente admite:

```text
activo
inactivo
```

Utiliza un breakpoint condicional para detenerte cuando:

```python
equipo["estado"] not in (
    "activo",
    "inactivo"
)
```

Inspecciona el equipo.

Después comprueba que el programa lo rechaza y genera el correspondiente:

```text
WARNING
```

---

### 169. Reto: equipo concreto

Supongamos que un usuario nos informa:

```text
PC05 produce resultados incorrectos
```

No queremos detenernos en todos los equipos.

Podemos utilizar:

```python
equipo["nombre"] == "PC05"
```

como condición del breakpoint.

Después podemos inspeccionar:

```text
nombre
IP
RAM
estado
```

únicamente cuando se procesa ese equipo.

---

### 170. Reto: combinación de condiciones

Podemos utilizar:

```python
equipo["ram"] > 16
```

para detenernos ante equipos con más de 16 GB.

O:

```python
(
    equipo["estado"] == "activo"
    and equipo["ram"] >= 16
)
```

para investigar solamente equipos:

```text
activos
```

con:

```text
16 GB o más
```

Los breakpoints condicionales permiten reducir enormemente el número de interrupciones.

---

### 171. Reto: utilizar Watch

Durante la ejecución añade:

```python
len(equipos)
```

```python
len(validos)
```

```python
ram_total
```

```python
numero_equipos
```

```python
ram_total / numero_equipos
```

Observa cuándo puede evaluarse cada expresión.

Recuerda:

```text
una variable debe existir
en el contexto seleccionado
```

para poder utilizarla.

---

### 172. Reto: seguir una función completa

Coloca un breakpoint antes de:

```python
mostrar_resumen(
    equipos
)
```

Después utiliza:

```text
F11
```

para entrar en:

```python
mostrar_resumen()
```

Continúa entrando en:

```text
obtener_equipos_validos()
```

y:

```text
equipo_valido()
```

Observa cómo aumenta:

```text
Call Stack
```

Después utiliza:

```text
Shift + F11
```

para regresar progresivamente.

---

### 173. Reto: investigar sin modificar código

El profesor puede modificar uno de los datos del CSV sin indicar cuál.

El alumno deberá encontrarlo utilizando exclusivamente:

```text
Variables
Watch
Debug Console
Breakpoints
Breakpoints condicionales
Call Stack
```

Durante la investigación no se permite añadir:

```python
print()
```

al programa.

Una vez localizado el problema se podrá corregir.

---

### 174. Documentar una incidencia

Una parte importante del trabajo técnico consiste en documentar lo ocurrido.

Para cada error podemos utilizar:

```text
INCIDENCIA:

Síntoma:

Resultado esperado:

Resultado obtenido:

Breakpoint utilizado:

Variables observadas:

Causa:

Corrección:

Prueba posterior:

Resultado final:
```

Por ejemplo:

```text
INCIDENCIA:
RAM total incorrecta

Resultado esperado:
80 GB

Resultado obtenido:
8 GB

Breakpoint utilizado:
calcular_ram_total()

Variables observadas:
total
equipo["ram"]

Causa:
El valor de total se sustituía
en cada iteración.

Corrección:
Cambiar:

total = equipo["ram"]

por:

total += equipo["ram"]

Prueba posterior:
Ejecutar nuevamente el inventario.

Resultado final:
80 GB
```

---

### 175. Actividad evaluable

El profesor entregará un programa similar a:

```text
gestor_inventario_debug.py
```

con varios errores introducidos deliberadamente.

El alumno deberá localizar al menos:

```text
un error de validación
un error en una condición
un error en un acumulador
un dato incorrecto
```

Deberá utilizar obligatoriamente:

```text
un breakpoint normal
un breakpoint condicional
Variables
Watch
Debug Console
Call Stack
Step Into
Step Over
```

No bastará con entregar el programa corregido.

También deberá explicar:

```text
cómo localizó cada error
```

---

### 176. Entrega propuesta

La entrega puede contener:

```text
programa_original.py
programa_corregido.py
informe_depuracion.txt
```

El archivo:

```text
informe_depuracion.txt
```

deberá indicar para cada problema:

```text
síntoma
evidencia
causa
corrección
comprobación
```

De esta forma evaluamos no solamente:

```text
programar
```

sino también:

```text
diagnosticar
```

---

### 177. Metodología general de depuración

Después de todas las prácticas del capítulo podemos establecer una metodología.

```text
1. REPRODUCIR
      │
      ▼
   confirmar problema

2. OBSERVAR
      │
      ▼
   obtener evidencias

3. AISLAR
      │
      ▼
   reducir zona sospechosa

4. INSPECCIONAR
      │
      ▼
   variables y flujo

5. FORMULAR HIPÓTESIS
      │
      ▼
   posible causa

6. COMPROBAR
      │
      ▼
   debugger

7. CORREGIR
      │
      ▼
   modificar código

8. VOLVER A PROBAR
      │
      ▼
   comprobar solución
```

---

### 178. Elegir correctamente el breakpoint

No siempre debemos colocar el breakpoint exactamente donde aparece el resultado incorrecto.

Supongamos:

```text
leer CSV
   │
   ▼
validar
   │
   ▼
calcular
   │
   ▼
generar informe
   │
   ▼
resultado incorrecto
```

Podemos comenzar cerca del resultado.

Después retroceder conceptualmente:

```text
¿qué datos recibió?
```

```text
¿quién llamó a esta función?
```

```text
¿de dónde procedían esos datos?
```

Para ello utilizamos:

```text
Call Stack
Variables
Watch
```

---

### 179. Las preguntas del depurador

Durante una investigación podemos hacernos siempre estas preguntas:

```text
¿Dónde estoy?
```

```text
¿Cómo he llegado aquí?
```

```text
¿Qué variables existen?
```

```text
¿Qué valores tienen?
```

```text
¿Qué instrucción se ejecutará ahora?
```

```text
¿Qué esperaba que ocurriera?
```

```text
¿Qué ha ocurrido realmente?
```

```text
¿En qué momento divergen ambos?
```

Encontrar ese punto suele acercarnos a la causa del problema.

---

### 180. Herramientas y preguntas

Podemos relacionarlas:

| Pregunta | Herramienta |
|---|---|
| ¿Dónde quiero detenerme? | Breakpoint |
| ¿Cuándo quiero detenerme? | Breakpoint condicional |
| ¿Qué valores existen? | Variables |
| ¿Cómo cambia esta expresión? | Watch |
| ¿Cómo he llegado aquí? | Call Stack |
| ¿Cuánto vale esta expresión? | Debug Console |
| ¿Qué hace la siguiente línea? | Step Over |
| ¿Qué ocurre dentro de esta función? | Step Into |
| ¿Cómo regreso al llamador? | Step Out |

Esta tabla resume gran parte del capítulo.

---

### 181. Errores que hemos investigado

Durante el capítulo hemos trabajado con:

```text
errores lógicos
```

por ejemplo:

```python
total = equipo["ram"]
```

en lugar de acumular.

También:

```text
condiciones incorrectas
```

como:

```python
estado == "inactivo"
```

cuando queríamos contar activos.

También:

```text
datos incorrectos
```

como:

```text
RAM = -8
```

Y:

```text
excepciones
```

como:

```text
ValueError
```

al intentar convertir texto a entero.

---

### 182. Depuración y calidad del software

La depuración no consiste únicamente en:

```text
hacer desaparecer errores
```

También nos ayuda a comprender mejor nuestros programas.

Durante una sesión de depuración podemos descubrir:

```text
funciones demasiado grandes
```

```text
variables confusas
```

```text
validaciones insuficientes
```

```text
dependencias innecesarias
```

```text
flujo demasiado complejo
```

Por tanto, depurar también puede ayudarnos a mejorar el diseño del programa.

---

### 183. Relación con capítulos anteriores

Las técnicas de este capítulo pueden aplicarse a todo lo desarrollado anteriormente.

En programas de archivos:

```text
Path
CSV
lectura
escritura
```

podemos inspeccionar:

```text
rutas
filas
datos
```

En automatización:

```text
bucles
inventarios
backups
```

podemos seguir:

```text
iteraciones
contadores
estados
```

En APIs:

```text
requests
JSON
```

podemos observar:

```text
status_code
diccionarios
respuestas
```

En redes:

```text
socket
DNS
TCP
```

podemos investigar:

```text
host
IP
puerto
estado
```

---

### 184. Aplicar el depurador al Capítulo 6

Por ejemplo, en nuestro:

```text
diagnostico_red.py
```

podemos colocar un breakpoint en:

```python
resultado = (
    diagnosticar_servicio(
        servicio,
        args.timeout
    )
)
```

y utilizar:

```text
F11
```

para entrar en la función.

Después podemos observar:

```text
host
puerto
ip
estado_tcp
```

Esto permite analizar paso a paso una herramienta real desarrollada anteriormente.

---

### 185. Breakpoint condicional en `diagnostico_red.py`

Si tenemos muchos servicios podemos detenernos únicamente ante:

```python
servicio["puerto"] == 443
```

o:

```python
servicio["host"] == "example.com"
```

También podemos investigar posteriormente un resultado concreto mediante una condición como:

```python
resultado["tcp"] != "ACCESIBLE"
```

si colocamos el breakpoint en un punto donde `resultado` ya haya sido creado.

---

### 186. Debug Console en aplicaciones de red

Con el programa detenido podemos consultar:

```python
servicio["host"]
```

```python
servicio["puerto"]
```

```python
args.timeout
```

o:

```python
resultado["tcp"]
```

sin añadir instrucciones `print()`.

Así podemos utilizar las técnicas del Capítulo 7 sobre programas del Capítulo 6.

---

### 187. Preparación para el proyecto final

El siguiente paso del curso será construir un proyecto que integre buena parte de lo aprendido.

El proyecto deberá trabajar con:

```text
inventario de equipos
CSV
ping
socket
puertos
informes
JSON
logging
argparse
excepciones
```

Durante su desarrollo utilizaremos también:

```text
depuración
```

Por tanto, el Capítulo 7 no es un contenido aislado.

Será una herramienta de trabajo durante el proyecto final.

---

### 188. Resumen del Capítulo 7

En este capítulo hemos aprendido a utilizar el depurador de Visual Studio Code para analizar programas Python.

Comenzamos utilizando:

```text
breakpoints
```

para detener temporalmente la ejecución.

Después aprendimos:

```text
Continue
Step Over
Step Into
Step Out
```

para controlar el avance del programa.

Utilizamos:

```text
Variables
```

para observar el estado de la aplicación.

Después incorporamos:

```text
Watch
```

para seguir expresiones concretas.

Aprendimos a interpretar:

```text
Call Stack
```

para conocer la cadena de llamadas entre funciones.

Utilizamos:

```text
Debug Console
```

para evaluar expresiones durante una pausa.

Y finalmente trabajamos con:

```text
breakpoints condicionales
```

para detenernos solamente cuando se produce una situación determinada.

---

### 189. Mapa de herramientas del depurador

Podemos resumir:

```text
                   DEPURADOR
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   BREAKPOINTS      INSPECCIÓN       EJECUCIÓN
        │              │              │
   ┌────┴────┐    ┌────┼────┐    ┌────┼────┐
   │         │    │    │    │    │    │    │
   ▼         ▼    ▼    ▼    ▼    ▼    ▼    ▼
normal  condicional Var Watch Stack F10  F11  F5
                        │
                        ▼
                 Debug Console
```

Cada herramienta tiene una finalidad concreta.

---

### 190. Competencias adquiridas

Al finalizar el capítulo debemos ser capaces de:

- Iniciar una sesión de depuración en VS Code.
- Crear y eliminar breakpoints.
- Continuar una ejecución.
- Ejecutar paso a paso.
- Entrar y salir de funciones.
- Inspeccionar variables.
- Observar expresiones con Watch.
- Interpretar Call Stack.
- Utilizar Debug Console.
- Crear breakpoints condicionales.
- Depurar condiciones.
- Depurar bucles.
- Depurar funciones.
- Investigar errores lógicos.
- Investigar datos incorrectos.
- Analizar excepciones.
- Diferenciar síntomas y causas.
- Documentar una incidencia.
- Comprobar una corrección.

---

### 191. Buenas prácticas de depuración

Durante una investigación:

```text
reproduce primero el problema
```

```text
no cambies código al azar
```

```text
observa los datos reales
```

```text
utiliza breakpoints cerca
de la zona sospechosa
```

```text
sigue el flujo paso a paso
```

```text
utiliza Call Stack para
buscar el origen
```

```text
formula una hipótesis
antes de modificar
```

```text
realiza cambios pequeños
```

```text
vuelve a probar
después de corregir
```

---

### 192. Depuración, excepciones y logging

Ahora podemos distinguir claramente tres herramientas:

```text
              PROGRAMA
                  │
       ┌──────────┼──────────┐
       │          │          │
       ▼          ▼          ▼
 EXCEPCIONES   LOGGING    DEBUGGER
       │          │          │
       ▼          ▼          ▼
 gestionar     registrar   investigar
 errores       eventos     ejecución
```

Un programa bien diseñado puede utilizar las tres.

Por ejemplo:

```text
try / except
```

gestiona un error previsto.

```text
logging
```

deja constancia del problema.

```text
debugger
```

nos ayuda a investigar su causa durante el desarrollo.

---

### 193. Cierre de la unidad de depuración

La depuración profesional cambia nuestra forma de enfrentarnos a un programa que no funciona correctamente.

En lugar de:

```text
probar cambios
al azar
```

podemos utilizar:

```text
evidencias
```

obtenidas durante la ejecución.

El proceso se convierte en:

```text
observar
   │
   ▼
comprender
   │
   ▼
formular hipótesis
   │
   ▼
comprobar
   │
   ▼
corregir
   │
   ▼
validar
```

!!! success "Capítulo 7 completado"

    Hemos aprendido a utilizar las principales herramientas de depuración de Visual Studio Code para investigar programas Python.

    Ya podemos detener una aplicación, inspeccionar su estado, seguir su ejecución, entrar en funciones, analizar la pila de llamadas y utilizar breakpoints condicionales para localizar problemas concretos.

    Estas técnicas serán utilizadas durante el desarrollo del proyecto final.

---

### 194. Siguiente etapa: proyecto final

Con este capítulo hemos completado la parte dedicada a:

```text
Depuración profesional en VS Code
```

Ahora estamos preparados para desarrollar el **proyecto final integrador**.

El objetivo será construir una herramienta de administración de red capaz de:

```text
leer equipos desde CSV
        │
        ▼
validar inventario
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
        ├── equipos accesibles
        ├── equipos no accesibles
        └── servicios disponibles
        │
        ▼
generar informe
        │
        ├── TXT
        └── JSON
        │
        ▼
registrar actividad
        │
        ▼
       LOG
```

El proyecto nos permitirá integrar los principales conocimientos desarrollados durante todo el libro:

```text
PYTHON
  │
  ├── archivos
  ├── CSV
  ├── pathlib
  ├── subprocess
  ├── automatización
  ├── argparse
  ├── excepciones
  ├── logging
  ├── JSON
  ├── socket
  └── depuración
```

A partir de este momento dejaremos de estudiar estos elementos principalmente de forma aislada.

Los utilizaremos conjuntamente para construir una aplicación completa.