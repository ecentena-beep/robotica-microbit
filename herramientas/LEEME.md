# Generadores de las fichas de actividades

Las 28 páginas de `actividades/` y el menú `actividades.html` **están generados**.
No los edites a mano: el próximo `generar.py` pisa los cambios.

## Los tres scripts

| Script | Qué hace |
|---|---|
| `extraer_del_pdf.py` | Lee el PDF del cuaderno y produce `actividades.json` |
| `generar.py` | De `actividades.json` produce las 28 páginas de `actividades/` |
| `menu.py` | De `actividades.json` produce `actividades.html` |

Para regenerar todo el sitio de actividades:

```bash
cd herramientas && python generar.py && python menu.py
```

`extraer_del_pdf.py` solo hace falta si cambia el PDF de origen; necesita el cuaderno
en la carpeta de materiales y la herramienta `pdftotext`.

## Los datos

Todo vive en `actividades.json`, un arreglo con un objeto por actividad:

```json
{
  "n": 15,
  "titulo": "Cubreasiento inteligente",
  "modalidad": "Grupal",
  "duracion": 90,
  "nivel": null,
  "encabezado_confiable": true,
  "epigrafe": "«…» — Autor",
  "objetivo": "…",
  "espacios": ["…"],
  "contenidos": ["…"],
  "materiales": ["…"],
  "desarrollo": "…"
}
```

Para corregir un dato, editá el JSON y volvé a correr `generar.py` y `menu.py`.

## Lo que no se pudo leer del PDF

**Modalidad y duración de 9 actividades** (4, 5, 6, 7, 8, 9, 24, 25, 26). El PDF dibuja
todas las variantes superpuestas —«Individual» encima de «Grupal», «45» encima de «60»—
y oculta las que no corresponden pintándolas de blanco. Al extraer el texto salen las dos
mezcladas: `GInrduipvaidlual`, `4650 minutos`. Esas actividades tienen
`"encabezado_confiable": false` y muestran un chip «⚠ a confirmar».

**El nivel de dificultad de las 28.** En el cuaderno es una línea de color en el borde
superior del encabezado (verde = baja, naranja = intermedia, rojo = avanzada), no un
texto. No se pudo extraer: los intentos de leer el color del PDF no dieron resultado y
renderizar las páginas se cuelga por el peso de los fondos vectoriales.

Cuando tengas los niveles, poné `"nivel": "baja"` (o `"intermedia"` / `"avanzada"`) en
cada actividad del JSON y regenerá. El chip de color aparece solo, tanto en el menú como
en la portada de cada ficha.

### Un atajo posible

Las 28 actividades usan solo **cuatro plantillas de fondo distintas**. Si el nivel se
corresponde con la plantilla, alcanza con saber el nivel de una actividad por grupo:

| Grupo | Actividades | Representante |
|---|---|---|
| A | 1, 3, 4, 6, 7, 9, 10 | 1 · Música:bit |
| B | 2, 5, 8, 11, 13, 14, 15, 16, 22, 23, 25 | 2 · Semáforo peatonal |
| C | 12, 17, 18, 19, 20, 21 | 12 · Modelo: energía térmica |
| D | 24, 26, 27, 28 | 24 · Micro:pedaleando en Scratch |

Son cuatro grupos y tres niveles, así que la correspondencia puede no ser exacta. Vale la
pena verificarla contra un par de actividades más antes de darla por buena.
