# -*- coding: utf-8 -*-
"""Genera el menú de actividades y una página por actividad.
Se vuelve a correr entero cada vez: las páginas de actividades no se
editan a mano, se editan acá y se regeneran."""
import io, os, re, json, unicodedata

DESTINO = r"C:\Users\ecent\OneDrive - NOVO\DESARROLLO\Pagina robotica"
datos = json.loads(io.open("actividades.json", encoding="utf-8").read())

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return re.sub(r"-+", "-", s)

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

ICONO_MOD = {"Individual": "🙋", "Grupal": "👥", "Duplas": "👤👤", "Parejas": "👤👤", None: "❓"}

def trocear(texto, maximo=780):
    """Parte el desarrollo en bloques legibles, cortando en punto final."""
    frases = re.split(r"(?<=[.!?])\s+", texto)
    bloques, actual = [], ""
    for f in frases:
        if actual and len(actual) + len(f) > maximo:
            bloques.append(actual.strip()); actual = ""
        actual += f + " "
    if actual.strip(): bloques.append(actual.strip())
    return bloques

def resaltar(bloque):
    """Convierte las marcas del cuaderno en cajas destacadas."""
    m = re.match(r"^(NOTA PARA DOCENTES:|¿SABÍAS QUE|PLUS:|PLUS \d+:)\s*(.*)$", bloque, re.S)
    if m:
        etiqueta, resto = m.group(1).rstrip(":"), m.group(2)
        clase = "aviso" if etiqueta.startswith("NOTA") else ""
        icono = {"NOTA PARA DOCENTES": "📌", "¿SABÍAS QUE": "💡"}.get(etiqueta, "⭐")
        titulo = "¿Sabías que…" if etiqueta.startswith("¿SAB") else etiqueta.capitalize()
        return (f'<div class="destacado {clase}"><h3 style="margin-top:0;">{icono} {esc(titulo)}</h3>'
                f'<p style="margin:0;">{esc(resto)}</p></div>')
    return f"<p>{esc(bloque)}</p>"

CABECERA = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo} — Actividad {n}</title>
<link rel="stylesheet" href="../css/estilos.css?v=3">
</head>
<body data-deck="actividad-{n}" data-inicio="../index.html">

<div id="barra-progreso"></div>

<main id="escenario">
"""

PIE = """</main>

<button class="zona-clic izq" aria-label="Slide anterior"></button>
<button class="zona-clic der" aria-label="Slide siguiente"></button>

<div id="titulo-deck"><a href="../index.html" style="color:inherit;">🏠 Inicio</a> · <a href="../actividades.html" style="color:inherit;">Todas las actividades</a></div>

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

<script src="../js/app.js?v=3"></script>
</body>
</html>
"""

os.makedirs(os.path.join(DESTINO, "actividades"), exist_ok=True)
fichas = []

for d in datos:
    n, titulo = d["n"], d["titulo"]
    nombre = f"{n:02d}-{slug(titulo)}.html"
    partes = [CABECERA.format(titulo=esc(titulo), n=n)]

    # --- meta ---
    meta = []
    if d["modalidad"]:
        meta.append(f'<span class="dato">{ICONO_MOD[d["modalidad"]]} {d["modalidad"]}</span>')
    if d["duracion"]:
        meta.append(f'<span class="dato">⏱ {d["duracion"]} minutos</span>')
    if d["nivel"]:
        meta.append(f'<span class="nivel {d["nivel"]}">{d["nivel"].capitalize()}</span>')
    if not d["encabezado_confiable"]:
        meta.append('<span class="dato" title="El PDF original dibuja las variantes superpuestas y no permite leer cuál corresponde">⚠ A confirmar</span>')
    meta_html = f'<div class="meta" style="justify-content:center;">{" ".join(meta)}</div>' if meta else ""

    # 1 · portada
    epi = f'<blockquote class="cita" style="margin-top:1.4em;max-width:44ch;text-align:left;">{esc(d["epigrafe"])}</blockquote>' if d["epigrafe"] else ""
    partes.append(f"""  <section class="slide portada" data-titulo="Actividad {n} · {esc(titulo)}">
    <span class="etiqueta">Actividad {n}</span>
    <h1>{esc(titulo)}</h1>
    {meta_html}
    {epi}
  </section>
""")

    # 2 · objetivo
    partes.append(f"""  <section class="slide" data-titulo="Objetivo">
    <span class="etiqueta">Actividad {n}</span>
    <h2>¿Para qué esta actividad?</h2>
    <p class="grande">{esc(d["objetivo"])}</p>
  </section>
""")

    # 3 · espacios + contenidos
    esp = "".join(f"<li>{esc(x)}</li>" for x in d["espacios"])
    con = "".join(f"<li>{esc(x)}</li>" for x in d["contenidos"])
    partes.append(f"""  <section class="slide" data-titulo="Contenidos">
    <span class="etiqueta">Actividad {n}</span>
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

    # 4 · materiales
    mat = "".join(f"<li>{esc(x)}</li>" for x in d["materiales"])
    partes.append(f"""  <section class="slide" data-titulo="Materiales">
    <span class="etiqueta">Actividad {n}</span>
    <h2>Qué hay que conseguir</h2>
    <ul class="materiales">{mat}</ul>
  </section>
""")

    # 5..n · desarrollo
    bloques = trocear(d["desarrollo"])
    for i, b in enumerate(bloques, 1):
        suf = f" ({i}/{len(bloques)})" if len(bloques) > 1 else ""
        partes.append(f"""  <section class="slide" data-titulo="Desarrollo{suf}">
    <span class="etiqueta">Desarrollo{suf}</span>
    <h2>Cómo se hace</h2>
    {resaltar(b)}
  </section>
""")

    # final · autoevaluación
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
      <a href="../actividades.html" style="color:var(--acento);">&larr; Volver a todas las actividades</a>
    </p>
  </section>
""")

    partes.append(PIE)
    io.open(os.path.join(DESTINO, "actividades", nombre), "w", encoding="utf-8").write("".join(partes))
    d["archivo"] = f"actividades/{nombre}"
    d["slides"] = len(partes) - 2
    fichas.append(d)
    print(f"  {nombre:44s} {d['slides']:2d} slides")

io.open("actividades.json","w",encoding="utf-8").write(json.dumps(datos, ensure_ascii=False, indent=1))
print(f"\n{len(fichas)} archivos generados en actividades/")
