# Búsqueda de etiquetas con `find()` y `find_all()`

Beautiful Soup permite buscar elementos dentro de una página HTML según el nombre de la etiqueta, sus atributos, su contenido o su posición en el árbol del documento.

Las dos funciones principales para realizar estas búsquedas son:

```python
find()
find_all()
```

## Etiquetas, atributos y clases

La mayoría de los sitios web utilizan hojas de estilo o *stylesheets* para definir su apariencia.

Para aplicar estilos diferentes, los elementos HTML suelen tener atributos como `class`:

```html
<span class="green">Pedro</span>
<span class="red">Hola</span>
```

En estos ejemplos:

- `span` es el nombre de la etiqueta.
- `class` es un atributo.
- `green` y `red` son valores del atributo `class`.

Beautiful Soup puede aprovechar estos atributos para distinguir elementos que utilizan la misma etiqueta.

Por ejemplo, es posible buscar solamente los elementos `span` de las clases `green` y `red`:

```python
elementos = bs.find_all(
    "span",
    {"class": {"green", "red"}}
)
```

## Uso de `.get_text()`

El método `.get_text()` extrae únicamente el texto contenido dentro de una etiqueta.

Por ejemplo:

```html
<span class="precio">S/ 100</span>
```

```python
precio = bs.find("span", class_="precio")

print(precio)
print(precio.get_text())
```

Resultado:

```text
<span class="precio">S/ 100</span>
S/ 100
```

Después de utilizar `.get_text()`, se pierde la estructura de las etiquetas y queda solamente un bloque de texto.

Por ese motivo, conviene conservar los objetos `Tag` mientras se realizan búsquedas y utilizar `.get_text()` al final, antes de mostrar, guardar o procesar el dato definitivo.

## Diferencia entre `find()` y `find_all()`

### `find()`

Busca una sola coincidencia: la primera que aparece en el documento.

```python
titulo = bs.find("h1")
```

El resultado es un objeto `Tag`:

```html
<h1>Título principal</h1>
```

### `find_all()`

Busca todas las coincidencias y las devuelve dentro de una lista.

```python
titulos = bs.find_all("h1")
```

El resultado sería parecido a:

```python
[
    <h1>Primer título</h1>,
    <h1>Segundo título</h1>
]
```

La diferencia principal es:

```text
find()     → devuelve la primera coincidencia
find_all() → devuelve una lista con todas las coincidencias
```

## Argumentos principales

Las funciones aceptan varios argumentos:

```python
find_all(tag, attributes, recursive, text, limit, keywords)
find(tag, attributes, recursive, text, keywords)
```

La mayoría de las búsquedas utilizan principalmente `tag` y `attributes`.

## `tag`: nombre de la etiqueta

Indica qué tipo de etiqueta se desea buscar.

```python
bs.find("h1")
bs.find_all("div")
bs.find_all("span")
```

Los nombres de las etiquetas se escriben como cadenas de texto:

```python
"h1"
"div"
"span"
"p"
"a"
```

También se pueden buscar varios tipos de etiquetas mediante una lista:

```python
encabezados = bs.find_all([
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6"
])
```

## `attributes`: atributos de la etiqueta

Permite especificar qué características debe tener la etiqueta.

HTML:

```html
<span class="precio">S/ 100</span>
```

Búsqueda:

```python
precio = bs.find(
    "span",
    {"class": "precio"}
)
```

Esto significa:

> Buscar la primera etiqueta `span` cuyo atributo `class` tenga el valor `precio`.

## `recursive`: profundidad de la búsqueda

El HTML se organiza como un árbol:

```html
<div id="contenedor">
    <h2>Título directo</h2>

    <section>
        <p>Texto más profundo</p>
    </section>
</div>
```

Su estructura es:

```text
div
├── h2
└── section
    └── p
```

- `h2` y `section` son hijos directos de `div`.
- `p` es hijo de `section`.
- `p` también es descendiente de `div`.

Con:

```python
recursive=True
```

la búsqueda revisa hijos, hijos de los hijos y niveles más profundos.

Con:

```python
recursive=False
```

la búsqueda revisa únicamente los hijos directos.

`find_all()` utiliza `recursive=True` de manera predeterminada, por lo que normalmente no es necesario cambiarlo.

## `text`: búsqueda por contenido

También es posible buscar según el texto contenido dentro de las etiquetas.

```python
resultados = bs.find_all(text="the prince")
```

Para contar las coincidencias:

```python
print(len(resultados))
```

`len()` devuelve la cantidad de elementos encontrados.

## `limit`: limitar los resultados

`limit` se utiliza únicamente con `find_all()`.

```python
productos = bs.find_all(
    "div",
    class_="producto",
    limit=3
)
```

Aunque existan más productos, solo devuelve los primeros tres según el orden del HTML.

Esto no significa que sean los tres resultados más importantes, sino los primeros que aparecen en el documento.

`find()` puede entenderse como una búsqueda similar a `find_all()` con límite de uno, aunque `find()` devuelve directamente una etiqueta y `find_all()` siempre devuelve una lista.

## Búsqueda mediante palabras clave

Los atributos también pueden escribirse directamente como argumentos:

```python
elementos = bs.find_all(
    id="title",
    class_="text"
)
```

Se utiliza `class_` con guion bajo porque `class` es una palabra reservada de Python.

Como `find_all()` devuelve una lista, para obtener una sola etiqueta sería más apropiado utilizar:

```python
titulo = bs.find(
    id="title",
    class_="text"
)
```

Si el atributo `id` identifica de manera única al elemento, también puede escribirse:

```python
titulo = bs.find(id="title")
```

## Lo que aprendí

- `find()` devuelve la primera coincidencia encontrada.
- `find_all()` devuelve todas las coincidencias dentro de una lista.
- `tag` indica el nombre de la etiqueta que se desea buscar.
- `attributes` permite filtrar según atributos como `class` o `id`.
- `recursive` controla la profundidad de la búsqueda.
- `limit` restringe la cantidad de resultados de `find_all()`.
- `.get_text()` debe utilizarse al final para no perder prematuramente la estructura HTML.

