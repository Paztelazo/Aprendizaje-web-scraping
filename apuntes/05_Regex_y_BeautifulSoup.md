# 05. Regex y BeautifulSoup

## 1. ¿Qué es regex?

**Regex** significa **regular expression**, en español **expresión regular**.

Una regex sirve para describir un **patrón de texto** mediante reglas.

En vez de buscar un valor exacto:

```python
nombre == "gato"
```

puedes buscar cualquier texto que empiece con `gat`:

```python
r"gat.*"
```

Esto puede coincidir con:

```text
gato
gata
gatito
gatuno
```

---

## 2. Ejemplo básico en Python

```python
import re

texto = "Mi número es 987654321"
resultado = re.search(r"\d+", texto)

print(resultado.group())
```

Resultado:

```text
987654321
```

La expresión:

```regex
\d+
```

significa:

- `\d`: cualquier dígito del `0` al `9`.
- `+`: una o más veces.

---

## 3. Construir una regex a partir de reglas

Antes de escribir una regex, conviene listar cómo debe verse el texto objetivo.

Ejemplo de reglas:

1. Escribir la letra `a` al menos una vez.
2. Escribir la letra `b` exactamente cinco veces.
3. Escribir la letra `c` una cantidad par de veces, incluyendo cero.
4. Terminar con la letra `d` o con la letra `e`.

Regex:

```regex
aa*bbbbb(cc)*(d|e)
```

### `aa*`

```regex
aa*
```

Significa:

- La primera `a` es obligatoria.
- `a*` permite cero o más letras `a` adicionales.

Por tanto, acepta una o más letras `a`:

```text
a
aa
aaa
aaaa
```

También podría escribirse de forma más directa:

```regex
a+
```

### `bbbbb`

```regex
bbbbb
```

Significa exactamente cinco letras `b` consecutivas.

### `(cc)*`

```regex
(cc)*
```

- Los paréntesis agrupan `cc`.
- `*` permite repetir ese grupo cero o más veces.

Acepta una cantidad par de letras `c`:

```text
0, 2, 4, 6, 8...
```

### `(d|e)`

```regex
(d|e)
```

La barra `|` significa **o**.

Por tanto, debe aparecer una `d` o una `e`.

### Ejemplos válidos

```text
aaaaabbbbbccccd
aabbbbbcce
abbbbbed
```

El último ejemplo correcto, siguiendo exactamente cinco `b`, sería:

```text
abbbbbd
```

### Exigir que toda la cadena cumpla el patrón

Puedes usar:

```regex
^aa*bbbbb(cc)*(d|e)$
```

- `^`: inicio del texto.
- `$`: final del texto.

---

## 4. Símbolos comunes de regex

| Símbolo | Significado |
|---|---|
| `.` | Cualquier carácter |
| `\d` | Un dígito |
| `\w` | Letra, número o guion bajo |
| `\s` | Espacio, tabulación o salto de línea |
| `*` | Cero o más repeticiones |
| `+` | Una o más repeticiones |
| `?` | Cero o una repetición |
| `[]` | Conjunto de caracteres permitidos |
| `()` | Agrupación |
| `|` | Una opción u otra |
| `^` | Inicio del texto |
| `$` | Final del texto |

---

## 5. Ejemplo simplificado de correo electrónico

Primero se definen reglas:

1. Antes del `@`, permitir letras, números, punto, guion bajo, `+` y `-`.
2. Debe aparecer `@`.
3. Después del `@`, debe haber un dominio.
4. Debe aparecer un punto literal `.`.
5. Debe terminar en una extensión como `com`, `org`, `edu` o `net`.

Una regex simplificada sería:

```regex
^[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.(com|org|edu|net)$
```

### Primera parte

```regex
[A-Za-z0-9._+-]+
```

Dentro de `[]`, se permite cualquiera de estos caracteres:

- `A-Z`: letras mayúsculas.
- `a-z`: letras minúsculas.
- `0-9`: números.
- `.`: punto.
- `_`: guion bajo.
- `+`: signo más.
- `-`: guion.

El `+` colocado después del corchete significa que ese conjunto debe aparecer una o más veces.

> Esta regex es educativa y simplificada. Validar todos los correos reales correctamente requiere reglas más complejas.

---

## 6. Regla práctica para crear regex

**Siempre que crees una regex, primero escribe una lista concreta de cómo debe verse el texto objetivo.**

Por ejemplo, para un número telefónico debes decidir:

- Si lleva código de país.
- Si permite `+` al inicio.
- Cuántos dígitos contiene.
- Si permite espacios o guiones.
- Si debe empezar con un número específico.

---

# Regex con BeautifulSoup

## 7. ¿Por qué usar regex con BeautifulSoup?

BeautifulSoup permite buscar etiquetas HTML. Regex permite filtrar valores que siguen un patrón.

Una imagen de producto puede verse así:

```html
<img src="../img/gifts/img3.jpg">
```

Si haces:

```python
bs.find_all("img")
```

obtendrás todas las imágenes de la página, por ejemplo:

```html
<img src="../img/gifts/img1.jpg">
<img src="../img/gifts/img2.jpg">
<img src="../img/gifts/img3.jpg">
<img src="../img/logo.png">
<img src="../icons/menu.jpg">
<img src="../img/blank.gif">
```

Pero quizá solo quieres las imágenes de productos.

Puedes filtrarlas por el patrón de su atributo `src`:

```python
import re

imagenes = bs.find_all(
    "img",
    src=re.compile(r"^\.\./img/gifts/img.*\.jpg$")
)
```

Esto significa:

> Buscar etiquetas `<img>` cuyo atributo `src` empiece con `../img/gifts/img` y termine en `.jpg`.

---

## 8. Explicación del patrón de imágenes

```regex
^\.\./img/gifts/img.*\.jpg$
```

| Parte | Significado |
|---|---|
| `^` | Inicio del valor |
| `\.\.` | Dos puntos literales: `..` |
| `/img/gifts/img` | Texto literal de la ruta |
| `.*` | Cualquier cantidad de caracteres |
| `\.jpg` | Extensión literal `.jpg` |
| `$` | Final del valor |

Ejemplos que coinciden:

```text
../img/gifts/img1.jpg
../img/gifts/img25.jpg
../img/gifts/imgproducto.jpg
```

Ejemplos que no coinciden:

```text
../img/logo.jpg
../img/gifts/img1.png
../icons/img1.jpg
```

---

## 9. No depender de la posición

Depender de la posición significa seleccionar un elemento por el lugar que ocupa.

Ejemplo:

```python
imagenes = bs.find_all("img")
producto_1 = imagenes[0]
producto_2 = imagenes[1]
```

Esto supone que los productos siempre serán la primera y segunda imagen.

Hoy el HTML podría ser:

```html
<img src="../img/gifts/img1.jpg">
<img src="../img/gifts/img2.jpg">
<img src="../img/logo.jpg">
```

Mañana podrían agregar un banner:

```html
<img src="../img/banner.jpg">
<img src="../img/gifts/img1.jpg">
<img src="../img/gifts/img2.jpg">
<img src="../img/logo.jpg">
```

Ahora `imagenes[0]` sería el banner.

Es mejor buscar por una característica identificadora:

```python
imagenes = bs.find_all(
    "img",
    src=re.compile(r"^\.\./img/gifts/img.*\.jpg$")
)
```

Así no importa si las imágenes aparecen primero, en medio o al final de la página.

---

# BeautifulSoup: búsquedas y estructura

## 10. Etiquetas y atributos

Ejemplo:

```html
<span class="precio">S/ 100</span>
```

- `span`: nombre de la etiqueta.
- `class`: atributo.
- `precio`: valor del atributo.
- `S/ 100`: contenido de la etiqueta.

Un atributo es información adicional colocada dentro de la etiqueta de apertura.

---

## 11. `find()` y `find_all()`

### `find()`

Busca una sola coincidencia: la primera que encuentre.

```python
resultado = bs.find("span", class_="precio")
```

### `find_all()`

Busca todas las coincidencias y devuelve una lista.

```python
resultados = bs.find_all("span", class_="precio")
```

Conceptualmente:

```python
find(...)
```

es parecido a:

```python
find_all(..., limit=1)
```

Pero `find()` devuelve directamente el elemento, mientras que `find_all(..., limit=1)` devuelve una lista con un elemento.

---

## 12. Argumentos comunes de búsqueda

Los argumentos más usados son:

- `name`: nombre de la etiqueta.
- `attrs`: atributos que debe tener.
- `recursive`: qué tan profundo buscar.
- `string`: texto que debe contener.
- `limit`: cantidad máxima de resultados.
- Keyword arguments: atributos escritos directamente, como `id="titulo"`.

Ejemplos de etiquetas:

```python
"h1"
"div"
"span"
"p"
"a"
```

Siempre se escriben como strings entre comillas.

---

## 13. Buscar por atributos

```python
bs.find_all("span", attrs={"class": "precio"})
```

También puede escribirse:

```python
bs.find_all("span", class_="precio")
```

Para varios atributos:

```python
bs.find_all(
    "span",
    attrs={
        "class": "precio",
        "data-moneda": "PEN"
    }
)
```

Para buscar elementos cuya clase sea `green` o `red`, una forma clara es:

```python
elementos = bs.find_all(
    "span",
    class_=["green", "red"]
)
```

---

## 14. Keyword arguments

BeautifulSoup permite escribir algunos atributos directamente:

```python
bs.find_all(id="title")
```

También puedes combinar etiqueta y atributos:

```python
bs.find_all("span", id="title", class_="text")
```

No se escribe:

```python
class="text"
```

porque `class` es una palabra reservada de Python.

Se usa:

```python
class_="text"
```

O mediante `attrs`:

```python
attrs={"class": "text"}
```

---

## 15. Acceder a atributos

Dada esta etiqueta:

```html
<img src="producto.jpg" alt="Producto principal">
```

```python
imagen = bs.find("img")
```

Todos sus atributos están en:

```python
imagen.attrs
```

Resultado aproximado:

```python
{
    "src": "producto.jpg",
    "alt": "Producto principal"
}
```

Para obtener uno:

```python
imagen.attrs["src"]
```

Forma abreviada:

```python
imagen["src"]
```

Forma segura si podría no existir:

```python
imagen.get("src")
```

---

## 16. Cuidado con `.get_text()`

```python
tag.get_text()
```

extrae el texto visible de una etiqueta y elimina la estructura HTML del resultado.

Ejemplo:

```html
<div class="producto">
    <span class="nombre">Laptop</span>
    <span class="precio">S/ 2500</span>
</div>
```

Después de usar `.get_text()`, puedes obtener algo parecido a:

```text
Laptop S/ 2500
```

Ya no tendrás los tags `<span>` dentro de ese texto.

Por eso conviene primero localizar y separar la información usando etiquetas y atributos, y usar `.get_text()` al final.

---

# Navegación del árbol HTML

## 17. Estructura de árbol

HTML se organiza como un árbol:

```html
<div id="contenedor">
    <h2>Título directo</h2>

    <section>
        <p>Texto más profundo</p>
    </section>
</div>
```

Representación:

```text
div
├── h2
└── section
    └── p
```

- `h2` y `section` son hijos directos de `div`.
- `p` es hijo de `section`.
- `p` también es descendiente de `div`.

---

## 18. Children y descendants

### Children

Son los hijos directos de un elemento.

```python
for hijo in contenedor.children:
    print(hijo)
```

### Descendants

Incluyen hijos, nietos y cualquier nivel inferior.

```python
for descendiente in contenedor.descendants:
    print(descendiente)
```

---

## 19. Recursividad

Por defecto, `find_all()` busca de forma recursiva: revisa hijos, nietos y niveles inferiores.

```python
contenedor.find_all("p", recursive=True)
```

Con:

```python
recursive=False
```

solo busca entre los hijos directos.

```python
contenedor.find_all("p", recursive=False)
```

En el ejemplo anterior no encontraría el `<p>`, porque este no es hijo directo de `div`; está dentro de `section`.

---

## 20. Navegar mediante etiquetas

```python
bs.body.h1
```

Busca el primer `<h1>` descendiente de `<body>`.

```python
bs.div.find_all("img")
```

Busca el primer `<div>` y luego todas las imágenes dentro de ese `div`.

Estas formas son cómodas, pero devuelven normalmente la primera coincidencia encontrada.

---

## 21. Siblings

Dos elementos son **siblings** o hermanos cuando tienen el mismo padre y están al mismo nivel.

```html
<table>
    <tr>Encabezado</tr>
    <tr>Producto 1</tr>
    <tr>Producto 2</tr>
</table>
```

Los tres `<tr>` son hermanos porque pertenecen directamente al mismo `<table>`.

```python
primera_fila = bs.find("table").find("tr")

for hermano in primera_fila.next_siblings:
    print(hermano)
```

Esto devuelve los hermanos posteriores, pero no incluye la primera fila seleccionada.

Una forma más precisa es:

```python
for fila in primera_fila.find_next_siblings("tr"):
    print(fila)
```

---

# Hacer búsquedas específicas

## 22. No seleccionar solo la primera coincidencia

Supón esta tabla:

```html
<table id="giftList">
    <tr>
        <th>Producto</th>
        <th>Precio</th>
    </tr>

    <tr>
        <td>Oso</td>
        <td>$10</td>
    </tr>
</table>
```

Podrías seleccionar la primera fila así:

```python
bs.tr
```

O así:

```python
bs.table.tr
```

Pero ambas formas dependen de que la fila o la tabla deseada aparezcan primero.

La forma más robusta es:

```python
bs.find("table", id="giftList").find("tr")
```

Primero localiza la tabla específica mediante su `id` y después busca su primera fila.

---

## 23. No exagerar con la estructura

Una búsqueda como esta puede ser demasiado frágil:

```python
bs.body.div.div.section.table.tr
```

Si agregan o eliminan un `<div>`, puede dejar de funcionar.

Normalmente es mejor buscar por un atributo distintivo:

```python
tabla = bs.find("table", id="giftList")
```

Y después buscar dentro:

```python
primera_fila = tabla.find("tr")
```

La regla práctica es:

> Sé específico usando atributos estables, pero no dependas innecesariamente de toda la estructura o posición de la página.
