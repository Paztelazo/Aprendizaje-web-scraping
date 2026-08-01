# Instalación del entorno para Web Scraping

En este apunte documento cómo preparé mi entorno de trabajo para comenzar a aprender web scraping con Python y Beautiful Soup.

## Herramientas utilizadas

- Linux
- Python 3
- Visual Studio Code
- Entorno virtual de Python
- Beautiful Soup 4

---

## 1. Comprobar que Python está instalado

Para consultar la versión de Python:

```bash
python3 --version
```

El resultado debe ser parecido a:

```text
Python 3.11.x
```

También se puede comprobar dónde se encuentra instalado:

```bash
which python3
```

---

## 2. Entrar en la carpeta del proyecto

Mi proyecto se encuentra en la carpeta:

```bash
cd ~/Escritorio/Web_Scrapping
```

Para comprobar la ubicación actual:

```bash
pwd
```

Para listar los archivos de la carpeta:

```bash
ls
```

---

## 3. Crear un entorno virtual

El entorno virtual se crea con:

```bash
python3 -m venv .venv
```

Este comando crea una carpeta llamada `.venv`.

La carpeta contiene una instalación aislada de Python para este proyecto.

### ¿Qué es un entorno virtual?

Un entorno virtual permite instalar librerías para un proyecto sin afectar la instalación general de Python ni otros proyectos.

Por ejemplo, Beautiful Soup quedará instalada dentro de `.venv` y no de manera global en todo el sistema.

---

## 4. Activar el entorno virtual

En Linux, el entorno se activa con:

```bash
source .venv/bin/activate
```

Cuando está activo, la terminal muestra el nombre del entorno al comienzo:

```text
(.venv) usuario@equipo:~/Escritorio/Web_Scrapping$
```

Esto indica que los comandos de Python y `pip` se ejecutarán dentro del entorno virtual.

Para comprobar qué Python se está utilizando:

```bash
which python
```

El resultado debe apuntar a una ruta parecida a:

```text
/home/usuario/Escritorio/Web_Scrapping/.venv/bin/python
```

---

## 5. Actualizar `pip`

`pip` es el administrador de paquetes de Python.

Se actualiza con:

```bash
python -m pip install --upgrade pip
```

Utilizo:

```bash
python -m pip
```

en lugar de ejecutar solamente `pip`, porque así me aseguro de usar el `pip` asociado al Python del entorno virtual.

---

## 6. Instalar Beautiful Soup

El paquete se instala con:

```bash
python -m pip install beautifulsoup4
```

Aunque el paquete se llama:

```text
beautifulsoup4
```

dentro del código se importa desde:

```python
from bs4 import BeautifulSoup
```

---

## 7. Comprobar la instalación

Para comprobar que Beautiful Soup funciona:

```bash
python -c "from bs4 import BeautifulSoup; print('Beautiful Soup funciona')"
```

El resultado esperado es:

```text
Beautiful Soup funciona
```

Si el comando no muestra errores, la librería está instalada correctamente dentro del entorno virtual.

---

## 8. Guardar las dependencias

Para registrar las librerías instaladas en el proyecto:

```bash
python -m pip freeze > requirements.txt
```

Esto crea un archivo llamado:

```text
requirements.txt
```

Su contenido será parecido a:

```text
beautifulsoup4==4.x.x
soupsieve==2.x
typing_extensions==4.x.x
```

Otra persona puede instalar las mismas dependencias ejecutando:

```bash
python -m pip install -r requirements.txt
```

---

## 9. Desactivar el entorno virtual

Cuando termine de trabajar, puedo salir del entorno con:

```bash
deactivate
```

Para volver a trabajar en el proyecto debo entrar en la carpeta y activar nuevamente el entorno:

```bash
cd ~/Escritorio/Web_Scrapping
source .venv/bin/activate
```

---

## Posible error: falta el módulo `venv`

Si al crear el entorno aparece un error relacionado con `venv` o `ensurepip`, se puede instalar el componente con:

```bash
sudo apt update
sudo apt install python3-venv
```

Después se vuelve a crear el entorno:

```bash
python3 -m venv .venv
```

---

## Lo que aprendí

- Python permite crear entornos virtuales separados para cada proyecto.
- `.venv` contiene el Python y las librerías utilizadas por este proyecto.
- El entorno debe activarse antes de instalar librerías o ejecutar el programa.
- `pip` permite instalar paquetes externos de Python.
- Beautiful Soup se instala con el nombre `beautifulsoup4`.
- Beautiful Soup se importa en Python desde el módulo `bs4`.
- `requirements.txt` registra las dependencias necesarias para reproducir el proyecto.
