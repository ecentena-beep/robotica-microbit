# Robótica con micro:bit — sitio de clases

Deck de slides para enseñar robótica. Sin instalaciones, sin internet: se abre haciendo
doble clic en `index.html`.

## Estructura

```
index.html      ← Módulo 1: la placa micro:bit (29 slides)
modulo2.html    ← Módulo 2: tipos de proyectos (32 slides)
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

## Módulos siguientes

Para un módulo nuevo, copiá `modulo2.html` a `modulo3.html` y cambiá el
`data-deck="microbit-modulo3"` del `<body>` — así cada deck recuerda su propia posición
por separado. Después agregá el enlace en la slide de cierre del módulo anterior.

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
