# 12. Web Crawling Models

Cuando haces crawling de distintos sitios web, tarde o temprano tendrás que recopilar información de páginas con estructuras muy diferentes.

Por ejemplo:

- artículos;
- blogs;
- productos;
- restaurantes;
- precios;
- reseñas;
- noticias.

Cada sitio puede tener HTML diferente, layouts distintos, nombres diferentes para los mismos datos o monedas distintas.

Por eso no basta con saber extraer HTML.

También necesitas aprender a **modelar los datos**.

---

# La idea principal

Supongamos que quieres recopilar información de restaurantes desde:

```text
TripAdvisor
Yelp
Google
Páginas propias de restaurantes
```

Cada página tiene una estructura distinta.

Pero tú quieres terminar guardando algo parecido a:

```text
RESTAURANTE
├── nombre
├── dirección
├── puntuación
├── precio
└── reseñas
```

Entonces no conviene hacer un sistema completamente distinto para cada web.

La idea es crear un **modelo común**.

Ejemplo:

```python
class Restaurant:

    def __init__(self, name, address, rating):
        self.name = name
        self.address = address
        self.rating = rating
```

Después cada crawler traduce la información de su página hacia ese mismo modelo.

---

# Arquitectura general

```text
PÁGINA WEB 1
PÁGINA WEB 2
PÁGINA WEB 3
PÁGINA WEB 4
      ↓
   CRAWLERS
      ↓
"traducen" cada web
      ↓
MODELO DE DATOS COMÚN
      ↓
BASE DE DATOS
      ↓
ANÁLISIS
```

La web es desordenada porque cada sitio organiza la información de una manera distinta.

El modelo común es el que pone orden.

---

# Primero define qué datos necesitas

Supongamos que estás trabajando con productos.

Inicialmente podrías pensar en:

```text
Product
├── Price
├── Name
├── Description
├── Sizes
└── Colors
```

Luego visitas otro sitio y encuentras:

```text
Unidades en stock
```

Después otro:

```text
Link al fabricante
```

Después:

```text
Número de reviews
```

Y podrías seguir agregando atributos indefinidamente.

Eso se vuelve insostenible.

Podrías terminar con una tabla enorme llena de:

```text
NULL
NULL
NULL
NULL
```

porque muchos atributos solo existen en algunos productos.

Por eso:

> **Recopila únicamente lo que realmente necesitas.**

---

# Preguntas antes de agregar un dato

Cuando encuentres un dato nuevo, puedes preguntarte:

```text
Encontré un nuevo dato
        ↓
¿Lo necesito?
        ↓
       sí
        ↓
¿Aparece en casi todos los objetos?
        ↓
¿Es pequeño o muy grande?
        ↓
¿Lo necesito constantemente?
        ↓
¿Es estable o cambia mucho?
        ↓
Decido cómo almacenarlo
```

---

# 1. ¿El dato es dense o sparse?

## Dense

Un dato es **dense** cuando aparece en casi todos los objetos.

Por ejemplo:

```text
Nike A      S/ 300
Adidas B    S/ 250
Puma C      S/ 280
Reebok D    S/ 220
```

Todos tienen precio.

Entonces tiene sentido hacer:

```python
self.price
```

porque el campo estará ocupado casi siempre.

## Sparse

Un dato es **sparse** cuando solo aparece en algunos objetos.

Ejemplo:

```text
Nike A      Gore-Tex
Adidas B    NULL
Puma C      NULL
Reebok D    NULL
Salomon E   Gore-Tex
```

Solo algunos productos tienen:

```text
tecnología impermeable
```

Si creas una columna específica para cada característica rara, terminarás con demasiados campos vacíos.

---

# 2. ¿Qué tan grande es el dato?

No es lo mismo guardar:

```text
precio = 299
```

que guardar:

```text
500 reviews completas
```

Un campo pequeño puede estar directamente dentro de un objeto.

Un dato grande puede necesitar almacenarse aparte.

---

# 3. ¿Lo necesito constantemente?

Pregúntate:

> ¿Voy a necesitar este dato cada vez que trabaje con el producto?

Si la respuesta es no, puede tener sentido separarlo.

Por ejemplo:

```text
Product
|
+------ Reviews
```

Las reviews pueden ser muchas y no necesariamente las necesitas cada vez que consultas el producto.

---

# 4. ¿Qué tan variable es?

Un campo debería tener un comportamiento razonablemente predecible.

Por ejemplo, para tallas:

```text
38
39
40
41
```

Pero no quieres diseñar una estructura tan rígida que mañana falle si aparece algo diferente.

La pregunta es:

> ¿Este atributo tiene valores relativamente conocidos o puede variar muchísimo?

---

# Productos con muchos tipos de atributos

La categoría:

```text
Product
```

puede representar cosas completamente distintas:

```text
polo
laptop
libro
zapatilla
televisor
```

Una laptop y un polo casi no comparten características técnicas.

Por eso conviene separar lo común de lo variable.

```text
             PRODUCT
                |
    ┌───────────┴────────────┐
    ↓                        ↓
ATTRIBUTES                 PRICES
    |                        |
características           cambian con
del producto              tiempo/tienda
```

Los atributos variables se pueden guardar de forma flexible.

Los precios pueden almacenarse separadamente porque tienen otro comportamiento.

---

# No todo lo raro debe ir en `attributes`

No basta con decir:

```text
"Todo lo extraño lo guardo en attributes."
```

Algunos datos tienen comportamientos especiales.

Por ejemplo, las reviews.

Preguntas:

```text
¿Es grande?
Sí.

¿Lo necesito cada vez que analizo precios?
No.

¿Puede haber muchísimas?
Sí.
```

Entonces probablemente convenga separarlas:

```text
PRODUCT
|
+------ REVIEWS
|
+------ ATTRIBUTES
|
+------ PRICES
```

Cada entidad tiene una responsabilidad distinta.

---

# El precio debe modelarse aparte

El precio es especial porque puede cambiar:

- con el tiempo;
- según la tienda.

Por ejemplo:

```text
Laptop X

Amazon      S/ 3500
Ripley      S/ 3700
Falabella   S/ 3599
```

Y mañana:

```text
Amazon      S/ 3299
```

Si haces simplemente:

```python
product.price = 3299
```

pierdes mentalmente el precio anterior.

Por eso conviene que `Price` sea otra entidad.

```text
PRICE
├── product_id
├── store_id
├── price
└── timestamp
```

Así puedes guardar:

```text
Producto 10 | Amazon   | S/3500 | lunes
Producto 10 | Ripley   | S/3700 | lunes
Producto 10 | Amazon   | S/3299 | martes
```

Ahora puedes responder preguntas como:

```text
¿Cómo cambió el precio?
¿Qué tienda era más barata?
¿Cuánto costaba hace un mes?
```

---

# Cuando una característica modifica el precio

Supongamos:

```text
Camiseta Nike
```

Tiene:

```text
S   → S/50
M   → S/50
L   → S/55
XL  → S/60
```

Aquí la talla no es solamente un atributo descriptivo.

También afecta el precio.

Entonces esto ya no es suficiente:

```text
Product = Camiseta Nike
Price = S/50
```

Porque falta responder:

> ¿S/50 para qué talla?

---

# Product Instances

Para resolverlo se puede introducir otra entidad:

```text
PRODUCT
Camiseta Nike
      |
      ↓
PRODUCT INSTANCES
      |
├── talla S
├── talla M
├── talla L
└── talla XL
```

Ahora cada variante del producto tiene identidad propia.

Y los precios pueden pertenecer a esa instancia:

```text
PRICE
├── product_instance_id
├── store_id
├── price
└── date
```

Ejemplo:

```text
Camiseta Nike
|
├─ S
|   └── S/50
|
├─ M
|   └── S/50
|
├─ L
|   └── S/55
|
└─ XL
    └── S/60
```

Eso representa mejor la realidad.

---

# Pensar como diseñador de datos

El objetivo no es aprender solamente sobre:

```text
camisetas
libros
precios
```

La idea es aprender a diseñar estructuras de datos.

El mismo razonamiento se puede aplicar a noticias.

---

# Ejemplo con artículos

Podrías empezar con:

```text
ARTICLE
├── title
├── author
├── date
└── content
```

Pero luego aparecen:

```text
revision_date
related_articles
Facebook shares
LinkedIn shares
X shares
```

Entonces vuelves a hacer las mismas preguntas:

```text
¿Lo necesito?
¿Todos los artículos lo tienen?
¿Es estable?
¿Puede aparecer información nueva?
¿Debe estar dentro de Article?
¿O debería ser otra estructura?
```

---

# Datos flexibles

En lugar de crear:

```text
facebook_shares
twitter_shares
linkedin_shares
tiktok_shares
```

podrías usar algo flexible:

```python
social_shares = {
    "facebook": 200,
    "linkedin": 32
}
```

Si mañana aparece otra plataforma:

```python
social_shares["new_network"] = 56
```

el modelo sigue funcionando.

---

# La mentalidad correcta antes de scrapear

Evita comenzar pensando:

```text
"Voy a abrir una página
y ver qué puedo sacar."
```

Mejor piensa:

```text
¿Qué quiero estudiar?
        ↓
¿Qué entidades existen?
        ↓
¿Qué datos necesito de cada entidad?
        ↓
¿Qué datos son comunes?
        ↓
¿Qué datos son opcionales?
        ↓
¿Qué datos cambian?
        ↓
¿Qué datos necesitan su propia entidad?
        ↓
Diseño el modelo
        ↓
Ahora sí hago scraping
```

---

# Ejemplo: analizar laptops y precios

Objetivo:

```text
Analizar laptops y sus precios
```

Entidades:

```text
Product
ProductInstance
Price
Store
```

## Product

```text
Product
├── title
├── manufacturer
└── attributes
```

Representa el producto general.

## ProductInstance

```text
ProductInstance
├── product_id
└── configuration
```

Representa una variante concreta.

Por ejemplo:

```text
Laptop X
├── 8 GB RAM / 256 GB SSD
├── 16 GB RAM / 512 GB SSD
└── 32 GB RAM / 1 TB SSD
```

## Price

```text
Price
├── instance_id
├── store_id
├── price
└── date
```

Permite guardar el historial de precios por tienda y fecha.

## Store

Representa la tienda donde se encontró el precio.

Ejemplo:

```text
Amazon
Ripley
Falabella
Mercado Libre
```

---

# Recién después se crean los crawlers

Una vez definido el modelo:

```text
AmazonCrawler
RipleyCrawler
FalabellaCrawler
```

Cada crawler tiene HTML y lógica diferente.

Pero todos producen datos compatibles con el mismo modelo.

---

# Arquitectura completa

```text
                 INTERNET
                    |
        ┌───────────┼───────────┐
        ↓           ↓           ↓
      Amazon      Ripley     Falabella
        ↓           ↓           ↓
    crawler A   crawler B   crawler C
        │           │           │
        └───────────┼───────────┘
                    ↓
               MODELO COMÚN
                    ↓
        ┌───────────┼───────────┐
        ↓           ↓           ↓
     Product    Instances     Prices
        ↓           ↓           ↓
              BASE DE DATOS
                    ↓
                 ANÁLISIS
```

---

# ¿Cómo saber si el diseño es bueno?

Supongamos que mañana agregas:

```text
Mercado Libre
```

Idealmente no deberías rediseñar todo.

Solo agregas:

```text
Mercado Libre
      ↓
nuevo crawler
      ↓
mismo modelo
```

Si puedes agregar nuevas fuentes sin destruir tu estructura anterior, tu modelo está bien diseñado.

---

# Resumen mental

```text
La web es desordenada
        ↓
cada sitio tiene HTML diferente
        ↓
los crawlers extraen y traducen datos
        ↓
todos usan un modelo común
        ↓
los datos se almacenan de forma consistente
        ↓
puedes analizarlos juntos
```

Antes de escribir un crawler:

```text
NO:
"¿Qué puedo sacar de esta página?"

SÍ:
"¿Qué necesito representar
y cómo debería modelarlo?"
```
