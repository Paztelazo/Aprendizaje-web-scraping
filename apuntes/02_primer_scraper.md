# Primer scraper con Python y Beautiful Soup

En este apunte documento cómo funciona mi primer programa de web scraping, llamado `trial.py`.

El programa realiza cuatro tareas principales:

1. Guarda la dirección de una página web.
2. Se conecta con esa dirección.
3. Procesa el contenido HTML recibido.
4. Busca y muestra una etiqueta del documento.

---

## Código completo

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "http://pythonscraping.com/pages/page1.html"

html = urlopen(url)

bs = BeautifulSoup(html, "html.parser")

print(bs.h1)
```

---

# Explicación paso por paso

## 1. Importar las herramientas

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
```

Importamos dos herramientas.

### `urlopen`

```python
from urllib.request import urlopen
```

`urlopen` sirve para conectarnos con una URL y solicitar su contenido.

Pertenece al módulo:

```text
urllib.request
```

`urllib` forma parte de la biblioteca estándar de Python, por lo que no fue necesario instalarla con `pip`.

### `BeautifulSoup`

```python
from bs4 import BeautifulSoup
```

`BeautifulSoup` permite interpretar, organizar y recorrer el contenido HTML recibido.

Pertenece al paquete externo Beautiful Soup 4, que instalamos anteriormente con:

```bash
python -m pip install beautifulsoup4
```

---

## 2. Guardar la URL

```python
url = "http://pythonscraping.com/pages/page1.html"
```

Creamos una variable llamada `url`.

La variable guarda la dirección de la página web como una cadena de texto.

Podemos representarlo así:

```text
url → "http://pythonscraping.com/pages/page1.html"
```

En este momento el programa todavía no se ha conectado con la página.

Solo hemos guardado su dirección.

---

## 3. Abrir la URL

```python
html = urlopen(url)
```

La función `urlopen()` recibe la dirección almacenada en la variable `url`.

Después:

1. Se conecta con el servidor.
2. Solicita el recurso indicado por la URL.
3. Recibe una respuesta.
4. Guarda esa respuesta en la variable `html`.

El flujo es:

```text
url
 ↓
urlopen(url)
 ↓
respuesta del servidor
 ↓
html
```

### ¿Qué contiene `html`?

La variable `html` todavía no contiene simplemente un texto normal.

Contiene un objeto de respuesta parecido a un archivo abierto, desde el cual Python puede leer los datos enviados por el servidor.

El nombre `html` fue elegido por nosotros. También podría llamarse:

```python
respuesta = urlopen(url)
```

Pero en este programa utilizamos el nombre `html` porque la respuesta contiene el documento HTML de la página.

---

## 4. Procesar el HTML con Beautiful Soup

```python
bs = BeautifulSoup(html, "html.parser")
```

Beautiful Soup recibe dos argumentos:

```python
BeautifulSoup(html, "html.parser")
```

### Primer argumento: `html`

```python
html
```

Es la respuesta que obtuvimos mediante:

```python
html = urlopen(url)
```

Beautiful Soup utilizará esa respuesta para leer el contenido de la página.

### Segundo argumento: `"html.parser"`

```python
"html.parser"
```

Este argumento indica qué analizador debe utilizar Beautiful Soup para interpretar el documento.

`html.parser` es un analizador de HTML incluido con Python.

No fue necesario instalarlo por separado.

### Resultado

El resultado de procesar el documento se guarda en la variable:

```python
bs
```

El flujo es:

```text
respuesta HTML
       ↓
BeautifulSoup
       ↓
documento organizado
       ↓
      bs
```

La variable `bs` contiene ahora una representación organizada del HTML.

Gracias a esto podemos buscar elementos como:

```python
bs.h1
bs.title
bs.body
bs.head
```

---

## 5. Buscar la primera etiqueta `<h1>`

```python
print(bs.h1)
```

La expresión:

```python
bs.h1
```

busca la primera etiqueta `<h1>` dentro del documento HTML procesado.

Por ejemplo, si el HTML contiene:

```html
<h1>An Interesting Title</h1>
```

entonces:

```python
print(bs.h1)
```

mostrará:

```html
<h1>An Interesting Title</h1>
```

### Función `print()`

`print()` sirve para mostrar información en la terminal.

En este caso muestra la etiqueta completa, incluyendo:

- la etiqueta de apertura `<h1>`;
- el contenido;
- la etiqueta de cierre `</h1>`.

---

## Obtener solamente el texto

Para mostrar únicamente el texto que se encuentra dentro de la etiqueta se puede utilizar:

```python
print(bs.h1.get_text())
```

El resultado sería:

```text
An Interesting Title
```

La diferencia es:

```python
print(bs.h1)
```

Muestra la etiqueta completa:

```html
<h1>An Interesting Title</h1>
```

Mientras que:

```python
print(bs.h1.get_text())
```

muestra únicamente:

```text
An Interesting Title
```

---

# Flujo completo del programa

```text
Dirección web
     ↓
    url
     ↓
urlopen(url)
     ↓
respuesta del servidor
     ↓
   html
     ↓
BeautifulSoup(html, "html.parser")
     ↓
HTML organizado
     ↓
     bs
     ↓
   bs.h1
     ↓
primera etiqueta <h1>
     ↓
   print()
     ↓
resultado en la terminal
```

---

# Ejecutar el programa

Primero debemos estar dentro de la carpeta del proyecto:

```bash
cd ~/Escritorio/Web_Scrapping
```

Después activamos el entorno virtual:

```bash
source .venv/bin/activate
```

La terminal debe mostrar algo parecido a:

```text
(.venv) usuario@equipo:~/Escritorio/Web_Scrapping$
```

Finalmente, ejecutamos el archivo:

```bash
python trial.py
```

La estructura general para ejecutar un programa de Python es:

```bash
python nombre_del_archivo.py
```

En este proyecto:

```bash
python trial.py
```

El resultado esperado es:

```html
<h1>An Interesting Title</h1>
```

---

# Diferencia entre guardar y ejecutar

Guardar el archivo en Visual Studio Code no ejecuta automáticamente el programa.

Después de modificar el código debo:

1. Guardar el archivo con `Ctrl + S`.
2. Abrir o seleccionar la terminal.
3. Comprobar que el entorno virtual esté activo.
4. Ejecutar:

```bash
python trial.py
```

Cada vez que cambie el código, debo guardarlo y volver a ejecutar el comando.

---

# Convención para `BeautifulSoup`

La forma recomendada de importarlo es:

```python
from bs4 import BeautifulSoup
```

Y utilizarlo respetando sus mayúsculas:

```python
bs = BeautifulSoup(html, "html.parser")
```

También es posible crear un alias:

```python
from bs4 import BeautifulSoup as beautifulsoup
```

Pero para aprender es más claro conservar el nombre original de la clase:

```python
BeautifulSoup
```

---

# Lo que aprendí

- Una URL puede guardarse como texto dentro de una variable.
- `urlopen()` permite conectarse con una URL.
- La respuesta del servidor se guarda en la variable `html`.
- `html` no es solamente texto; inicialmente es un objeto de respuesta.
- Beautiful Soup interpreta y organiza el contenido HTML.
- `"html.parser"` indica el analizador que se utilizará.
- El resultado procesado se guarda en la variable `bs`.
- `bs.h1` busca la primera etiqueta `<h1>`.
- `print()` muestra el resultado en la terminal.
- `.get_text()` permite obtener solamente el texto de una etiqueta.
- Un programa se ejecuta con `python nombre_del_archivo.py`.

