# -*- coding: utf-8 -*-
"""Genera una página por actividad del cuaderno.

Se vuelve a correr entero cada vez: las páginas de actividades no se editan
a mano, se editan acá y se regeneran.

Estructura de cada actividad (6 slides como máximo):
  1. Portada — título, modalidad, duración y descarga del PDF
  2. ¿Para qué es esta actividad?
  3. Qué se trabaja — espacios curriculares y contenidos micro:bit
  4. Qué hay que conseguir — materiales
  5. Descargá el proyecto — el PDF completo
  6. Autoevaluación
"""
import io, os, re, json, unicodedata

DESTINO = r"C:\Users\ecent\OneDrive - NOVO\DESARROLLO\Pagina robotica"
VERSION = "4"          # cache busting de estilos.css y app.js

datos = json.loads(io.open("actividades.json", encoding="utf-8").read())


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return re.sub(r"-+", "-", s)


def esc(s):
    return (str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


ICONO_MOD = {"Individual": "🙋", "Grupal": "👥", "Duplas": "👤👤", "Parejas": "👤👤"}

CABECERA = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo} — Actividad {n}</title>
<link rel="stylesheet" href="../css/estilos.css?v={v}">
</head>
<body data-deck="actividad-{n}" data-inicio="../index.html">

<div id="barra-progreso"></div>

<main id="escenario">
"""

PIE = """</main>

<button class="zona-clic izq" aria-label="Slide anterior"></button>
<button class="zona-clic der" aria-label="Slide siguiente"></button>

<div id="titulo-deck"><a href="../index.html" style="color:inherit;">🏠 Inicio</a> · <a href="../actividades.html" style="color:inherit;">Todos los prototipos</a></div>

<div id="controles">
  <span id="contador">1 / 1</span>
  <button class="btn" id="btn-indice"   title="Índice (O)"            aria-label="Índice">☰</button>
  <button class="btn" id="btn-anterior" title="Anterior (&larr;)"     aria-label="Anterior">‹</button>
  <button class="btn" id="btn-siguiente" title="Siguiente (&rarr;)"   aria-label="Siguiente">›</button>
  <button class="btn" id="btn-pantalla" title="Pantalla completa (F)" aria-label="Pantalla completa">⛶</button>
</div>

<div id="indice"><h2>Índice de la actividad</h2><ul id="lista-indice"></ul></div>

<div id="ayuda"><div class="panel"><h2>Atajos de teclado</h2><dl>
<dt><kbd>&rarr;</kbd> <kbd>espacio</kbd></dt><dd>Siguiente</dd>
<dt><kbd>&larr;</kbd></dt><dd>Anterior</dd>
<dt><kbd>O</kbd></dt><dd>Índice</dd>
<dt><kbd>F</kbd></dt><dd>Pantalla completa</dd>
<dt><kbd>Esc</kbd></dt><dd>Cerrar</dd>
</dl></div></div>

<script src="../js/app.js?v={v}"></script>
</body>
</html>
"""

os.makedirs(os.path.join(DESTINO, "actividades"), exist_ok=True)
generadas, sin_pdf = 0, []

for d in datos:
    n, titulo = d["n"], d["titulo"]
    nombre = f"{n:02d}-{slug(titulo)}.html"
    pdf = d.get("pdf")
    if not pdf:
        sin_pdf.append(n)

    partes = [CABECERA.format(titulo=esc(titulo), n=n, v=VERSION)]

    # ---------- 1 · portada ----------
    meta = []
    if d["modalidad"]:
        meta.append(f'<span class="dato">{ICONO_MOD.get(d["modalidad"],"")} {d["modalidad"]}</span>')
    if d["duracion"]:
        meta.append(f'<span class="dato">⏱ {d["duracion"]} minutos</span>')
    if d.get("nivel"):
        meta.append(f'<span class="nivel {d["nivel"]}">{d["nivel"].capitalize()}</span>')
    meta_html = f'<div class="meta" style="justify-content:center;">{" ".join(meta)}</div>' if meta else ""

    descarga_portada = (
        f'<a class="boton-descarga" href="../{pdf}" download>⬇ Descargar el PDF del proyecto</a>'
        if pdf else ""
    )
    epi = (f'<blockquote class="cita" style="margin-top:1.2em;max-width:44ch;text-align:left;">'
           f'{esc(d["epigrafe"])}</blockquote>') if d.get("epigrafe") else ""

    partes.append(f"""  <section class="slide portada" data-titulo="Actividad {n} · {esc(titulo)}">
    <span class="etiqueta">Prototipo {n}</span>
    <h1>{esc(titulo)}</h1>
    {meta_html}
    {epi}
    {descarga_portada}
  </section>
""")

    # ---------- 2 · para qué ----------
    partes.append(f"""  <section class="slide" data-titulo="¿Para qué es esta actividad?">
    <span class="etiqueta">Prototipo {n}</span>
    <h2>¿Para qué es esta actividad?</h2>
    <p class="grande">{esc(d["objetivo"])}</p>
  </section>
""")

    # ---------- 3 · qué se trabaja ----------
    esp = "".join(f"<li>{esc(x)}</li>" for x in d["espacios"])
    con = "".join(f"<li>{esc(x)}</li>" for x in d["contenidos"])
    partes.append(f"""  <section class="slide" data-titulo="Qué se trabaja">
    <span class="etiqueta">Prototipo {n}</span>
    <h2>Qué se trabaja</h2>
    <div class="dos-columnas" style="align-items:start;">
      <div>
        <h3>Espacios curriculares</h3>
        <ul class="limpia">{esp}</ul>
      </div>
      <div>
        <h3>Contenidos micro:bit</h3>
        <ul class="limpia">{con}</ul>
      </div>
    </div>
  </section>
""")

    # ---------- 4 · materiales ----------
    mat = "".join(f"<li>{esc(x)}</li>" for x in d["materiales"])
    partes.append(f"""  <section class="slide" data-titulo="Qué hay que conseguir">
    <span class="etiqueta">Prototipo {n}</span>
    <h2>Qué hay que conseguir</h2>
    <ul class="materiales">{mat}</ul>
  </section>
""")

    # ---------- 5 · descarga ----------
    if pdf:
        partes.append(f"""  <section class="slide portada" data-titulo="Descargá el proyecto">
    <span class="etiqueta">El proyecto completo</span>
    <h2>Descargá el proyecto acá</h2>
    <p class="subtitulo">El PDF trae el paso a paso, los ejemplos de programa y la ficha
    de trabajo para completar.</p>
    <a class="boton-descarga grande" href="../{pdf}" download>⬇ Descargar el PDF del proyecto</a>
    <p style="color:var(--texto-suave); font-size:calc(var(--u)*.8); margin-top:1.4em;">
      También podés <a href="../{pdf}" target="_blank" style="color:var(--acento);">abrirlo sin descargar</a>.
    </p>
  </section>
""")

    # ---------- 6 · autoevaluación ----------
    partes.append(f"""  <section class="slide" data-titulo="Autoevaluación">
    <span class="etiqueta">Para cerrar</span>
    <h2>Autoevaluación</h2>
    <p>Evaluá tu trabajo del <strong>1 al 5</strong> (1 el más bajo, 5 el más alto):</p>
    <ul class="limpia" style="font-size:calc(var(--u)*1.05);">
      <li>La actividad fue interesante y me motivó.</li>
      <li>Pedí ayuda para salir adelante cuando no sabía resolverlo.</li>
      <li>Busqué información por mi cuenta.</li>
      <li>Logré programar la micro:bit.</li>
      <li>Aprendí y conocí nuevas funciones de la placa.</li>
    </ul>
    <p style="margin-top:1.4em;">
      <a href="../actividades.html" style="color:var(--acento);">&larr; Volver a todos los prototipos</a>
    </p>
  </section>
""")

    partes.append(PIE.format(v=VERSION))
    io.open(os.path.join(DESTINO, "actividades", nombre), "w", encoding="utf-8").write("".join(partes))
    d["archivo"] = f"actividades/{nombre}"
    d["slides"] = len(partes) - 2
    generadas += 1
    print(f"  {nombre:44s} {d['slides']} slides" + ("" if pdf else "   (sin PDF)"))

io.open("actividades.json", "w", encoding="utf-8").write(json.dumps(datos, ensure_ascii=False, indent=1))
print(f"\n{generadas} archivos generados")
if sin_pdf:
    print("sin PDF asociado:", sin_pdf)
