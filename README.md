# Aprendizaje de Web Scraping con Python

Repositorio donde documento mi aprendizaje de web scraping utilizando Python y Beautiful Soup.

## Entorno

- Sistema operativo: Linux
- Python: 3.11
- Editor: Visual Studio Code
- Entorno virtual: `venv`
- Librería principal: Beautiful Soup 4

## Contenido

1. Instalación de Python y creación del entorno virtual.
2. Instalación de Beautiful Soup.
3. Primera conexión a una página web.
4. Procesamiento de HTML.
5. Extracción de etiquetas.

## Ejecutar el proyecto

Crear el entorno:

```bash
python3 -m venv .venv
```

Activarlo:

```bash
source .venv/bin/activate
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

Ejecutar el programa:

```bash
python trial.py
```

## Código actual

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "http://pythonscraping.com/pages/page1.html"
html = urlopen(url)
bs = BeautifulSoup(html, "html.parser")

print(bs.h1)
```

## Bitácora

Los apuntes detallados se encuentran en la carpeta [`apuntes`](apuntes).
