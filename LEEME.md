# Robótica con micro:bit — sitio de clases

Deck de slides para enseñar robótica. Sin instalaciones, sin internet: se abre haciendo
doble clic en `index.html`.

## Estructura

```
index.html      ← menú principal del sitio
modulo1.html    ← Módulo 1: la placa micro:bit (29 slides)
modulo2.html    ← Módulo 2: tipos de proyectos (14 slides)
comunidad.html  ← Módulo 3: Comunidad Robótica de Betel (el blog)
actividades.html← menú de las 28 actividades del cuaderno
actividades/    ← una página por actividad (GENERADAS, no editar a mano)
css/estilos.css ← todo el diseño (colores, tamaños, layouts)
js/app.js       ← navegación (no hay que tocarlo para agregar contenido)
media/          ← videos locales (NO se publican; ver nota abajo)
docs/           ← PDFs que se descargan desde el deck
img/            ← imágenes que quieras agregar
```

## Cómo se usa en clase

| Acción | Cómo |
|---|---|
| Avanzar | `→` · barra espaciadora · clic en el borde derecho · deslizar el dedo |
| Retroceder | `←` · clic en el borde izquierdo |
| Ir a una slide | `O` abre el índice |
| Pantalla completa | `F` |
| Ver atajos | `H` |
| Primera / última | `Inicio` / `Fin` |
| Guardar todo en PDF | `Ctrl` + `P` → «Guardar como PDF» |

El deck **recuerda en qué slide quedaste**, así que si se cierra el navegador a mitad de
clase, al reabrirlo sigue donde estabas. Para compartir una slide puntual, copiá la URL
con el `#12` del final.

## Cómo agregar una slide

Cada slide es un `<section class="slide">` dentro de `<main id="escenario">`.
Se agregan en el orden en que aparecen en el archivo. El índice y el contador se
actualizan solos.

```html
<section class="slide" data-titulo="Nombre que aparece en el índice">
  <span class="etiqueta">Categoría</span>
  <h2>Título de la slide</h2>
  <p>Texto normal.</p>
</section>
```

### Bloques disponibles

**Portada o slide de sección** (todo centrado, título con degradado)
```html
<section class="slide portada" data-titulo="...">
  <span class="etiqueta">Módulo 2</span>
  <h1>Título grande</h1>
  <p class="subtitulo">Bajada.</p>
</section>
```

**Tarjetas** (se acomodan solas según el ancho)
```html
<div class="tarjetas">
  <div class="tarjeta">
    <span class="icono">🔌</span>
    <h3>Título</h3>
    <p>Descripción corta.</p>
  </div>
</div>
```

**Dos columnas**
```html
<div class="dos-columnas">
  <div>Columna izquierda</div>
  <div>Columna derecha</div>
</div>
```

**Pasos numerados**
```html
<ol class="pasos">
  <li><h3>Primer paso</h3><p style="margin:0;">Explicación.</p></li>
</ol>
```

**Lista con flechitas**
```html
<ul class="limpia">
  <li>Un punto</li>
</ul>
```

**Caja destacada** — agregale `aviso` para que sea naranja, o `compacto` si la slide ya
tiene mucho contenido.
```html
<div class="destacado">
  <p style="margin:0;">Dato clave.</p>
</div>
```

**Cita**
```html
<blockquote class="cita">
  «Texto de la cita»
  <span class="autor">Quién lo dijo</span>
</blockquote>
```

**Código** (para mostrar bloques de MakeCode en texto)
```html
<pre><code>si (nivel de luz &lt; 50) entonces
    mostrar LEDs</code></pre>
```

> Ojo: dentro de `<pre>` hay que escribir `&lt;` en lugar de `<` y `&gt;` en lugar de `>`.

**Imagen** — poné el archivo en `img/`
```html
<figure>
  <img src="img/placa.jpg" alt="Descripción de la imagen">
  <figcaption>Epígrafe.</figcaption>
</figure>
```

**Video de YouTube** — es la forma recomendada. El `CODIGO` es lo que aparece
después de `v=` en la URL del video.
```html
<div class="video">
  <iframe src="https://www.youtube-nocookie.com/embed/CODIGO"
          title="Nombre del video" data-pausable="si"
          allow="accelerometer; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen></iframe>
</div>
```

> Usamos `youtube-nocookie.com` en lugar de `youtube.com`: es el modo de privacidad
> mejorada de YouTube, que no instala cookies de seguimiento hasta que el estudiante
> le da play. Es lo apropiado trabajando con menores.

**Video propio** — poné el archivo en `media/`. Solo para uso local: los `.mp4` están
excluidos del repositorio por peso y por derechos de autor.
```html
<video controls preload="metadata">
  <source src="media/mi-video.mp4" type="video/mp4">
</video>
```

**Tabla** — en celulares se desliza sola; no hace falta hacer nada.
```html
<table>
  <thead><tr><th>Columna</th><th>Columna</th></tr></thead>
  <tbody><tr><td>Dato</td><td>Dato</td></tr></tbody>
</table>
```

**Ficha de actividad** (Módulo 2) — la línea de datos y el chip de nivel.
```html
<div class="meta">
  <span class="dato">👥 Grupal</span>
  <span class="dato">⏱ 90 minutos</span>
  <span class="nivel avanzada">Avanzada</span>
</div>
```
Los niveles son `baja`, `intermedia` y `avanzada`.

**Lista de materiales** (a dos columnas)
```html
<ul class="materiales">
  <li>2 placas micro:bit</li>
  <li>2 cables cocodrilo</li>
</ul>
```

## Cambiar los colores

Todo está al principio de `css/estilos.css`, en `:root`. Cambiando `--acento` cambia el
color de títulos, viñetas, bordes y barra de progreso en todo el sitio.

## Comunidad Robótica de Betel (Módulo 3)

El blog donde los estudiantes cuentan sus proyectos. Antes de escribir tienen que poner
nombre y apellido, que queda firmando la publicación y guardado en su navegador para no
tener que repetirlo.

### Cómo está resuelto el guardado

GitHub Pages sirve archivos estáticos: **no puede guardar** lo que escriben. Por eso
`comunidad.html` tiene arriba de todo un bloque `CONFIG` con dos modos:

- **`local`** (el que está puesto): guarda en el navegador de cada uno. Cada estudiante ve
  solo lo suyo. La página muestra un aviso naranja diciéndolo. Sirve para probar y para
  que escriban el borrador.
- **`compartido`**: manda cada publicación a un formulario de Google y muestra las que
  vos aprobaste en una planilla.

### Pasar a modo compartido

1. Creá un formulario de Google con cinco preguntas de texto, en este orden:
   **Nombre**, **Apellido**, **Titulo**, **Texto**, **Enlace**.
2. En el formulario, abrí «Vista previa», clic derecho → «Inspeccionar», y buscá el
   atributo `name="entry.XXXXXXX"` de cada campo. Anotá los cinco números.
3. La URL para enviar es la del formulario cambiando `/viewform` por `/formResponse`.
4. En «Respuestas» → «Vincular a Hojas de cálculo». En esa planilla agregá una columna
   más y usala para marcar lo aprobado.
5. Creá una segunda hoja que traiga solo lo aprobado, y publicala:
   Archivo → Compartir → **Publicar en la web** → esa hoja → formato **CSV**.
6. Pegá todo en el `CONFIG` de `comunidad.html` y poné `modo: "compartido"`.

La planilla es tu **filtro de moderación**: nada aparece en el sitio hasta que lo marcás.

### Dos cosas a decidir antes de abrirlo a los estudiantes

- **Nombre y apellido completos en un sitio público.** Son menores. Se puede pedir nombre
  y la inicial del apellido, o un apodo de clase. El formulario y el sitio funcionan igual.
- **Moderación.** Con el modo compartido nada se publica sin tu aprobación. Si algún día
  se conecta algo que publique directo, conviene mantener ese paso.

## Las páginas de actividades

Las 28 páginas de `actividades/` y el menú `actividades.html` **no se editan a mano**:
están generadas a partir del PDF del cuaderno con dos scripts de Python
(`generar.py` y `menu.py`). Si hay que cambiar algo, se cambia en el script y se
regenera todo, si no el próximo cambio pisa las correcciones.

Los datos de cada actividad viven en `actividades.json`: número, título, modalidad,
duración, nivel, objetivo, espacios curriculares, contenidos micro:bit, materiales y
desarrollo.

### Datos que faltan

El PDF original dibuja **todas las variantes superpuestas** de modalidad y duración, y
tapa las que no corresponden pintándolas de blanco. Al extraer el texto salen las dos
mezcladas («GInrduipvaidlual»), así que en 9 actividades no se pudo saber cuál es:
**4, 5, 6, 7, 8, 9, 24, 25 y 26**. Esas aparecen marcadas con «⚠ a confirmar».

El **nivel de dificultad** (baja / intermedia / avanzada) está en el PDF como una línea
de color, no como texto, y no se pudo leer para ninguna actividad. El campo `nivel` de
`actividades.json` está en `null`; cuando se complete, el chip de color aparece solo en
el menú y en la portada de cada actividad.

## Módulos siguientes

Para un módulo nuevo, copiá `modulo2.html` a `modulo4.html` y cambiá el
`data-deck="microbit-modulo4"` del `<body>` — así cada deck recuerda su propia posición
por separado. Después agregá su tarjeta en `index.html`.

## Caché del navegador

`index.html` y compañía enlazan los archivos como `css/estilos.css?v=2` y `js/app.js?v=2`.
Si cambiás alguno de esos dos archivos, **subí el número de versión en todas las páginas**,
si no los navegadores que ya entraron siguen usando la copia vieja. En `herramientas/` hay
un `python generar.py && python menu.py` que se encarga de las 28 actividades; el resto
son cinco archivos y se hace a mano.

## Los videos

Las dos slides de video traen incrustados estos videos de YouTube:

| Slide | Video | Canal |
|---|---|---|
| 9 | [¿Qué es la placa micro:bit?](https://www.youtube.com/watch?v=rGVJtPt01gc) | Ceibal STEM |
| 28 | [Clase 1 · MICROBIT para principiantes](https://www.youtube.com/watch?v=5J3aVSQcksM) | STEAM Thinking |

Los `.mp4` originales siguen en `media/` de tu computadora por si algún día necesitás dar
la clase sin internet, pero **no se suben a GitHub**: pesan 50 MB y el segundo no es
material propio, así que republicarlo no correspondería.

Si vas a dar clase sin conexión, cambiá el bloque `<div class="video">` por el bloque
`<video>` que figura más arriba.

---

Contenido del Módulo 1 basado en el *Micro:manual 1 — La placa programable* y el
*Cuaderno de actividades micro:bit*, elaborados por **Ceibal** y **Chicos Net**.
