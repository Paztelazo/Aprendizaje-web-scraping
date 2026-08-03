# 06. Web Crawlers

Un **web crawler** es un programa que recorre páginas web siguiendo sus enlaces.

## Proceso básico

1. Entra a una URL.
2. Descarga el HTML.
3. Busca enlaces dentro de la página.
4. Entra a uno de esos enlaces.
5. Repite el proceso.

```text
Página A → Página B → Página C → Página D
```

## Diferencia entre scraper y crawler

- **Web scraper:** extrae información de una página.
- **Web crawler:** descubre y visita otras páginas.

Un crawler también puede usar scraping para extraer los enlaces que necesita seguir.

## Recursión o repetición

La idea se repite para cada nueva página:

```text
obtener página
→ encontrar enlaces
→ visitar otro enlace
→ volver a obtener página
```

No siempre tiene que implementarse con una función recursiva. También se puede usar un `while`.

## Six Degrees of Wikipedia

El objetivo es conectar dos artículos mediante una cadena de enlaces.

Ejemplo:

```text
Artículo A → Artículo B → Artículo C
```

Si A enlaza a B y B enlaza a C, existe una cadena de tres artículos y dos conexiones.

## Precauciones

Un crawler puede:

- consumir mucho ancho de banda;
- enviar demasiadas solicitudes;
- sobrecargar un servidor;
- hacer que bloqueen tu IP.

Por eso conviene limitar la velocidad y evitar visitar páginas innecesarias.
