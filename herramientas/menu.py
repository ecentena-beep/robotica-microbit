# -*- coding: utf-8 -*-
"""Genera actividades.html: el menú de las 28 actividades del cuaderno."""
import io, os, json, re

DESTINO = r"C:\Users\ecent\OneDrive - NOVO\DESARROLLO\Pagina robotica"
datos = json.loads(io.open("actividades.json", encoding="utf-8").read())

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def resumen(d, tope=115):
    t = d["objetivo"].strip()
    if len(t) <= tope: return t
    corte = t[:tope].rsplit(" ", 1)[0]
    return corte + "…"

ICONO = {"Individual":"🙋","Grupal":"👥","Duplas":"👤👤","Parejas":"👤👤"}

fichas = []
for d in datos:
    mod = d["modalidad"]
    dur = d["duracion"]
    niv = d["nivel"]
    pie = []
    if mod: pie.append(f'<span class="etiqueta-chica">{ICONO.get(mod,"")} {mod}</span>')
    if dur: pie.append(f'<span class="etiqueta-chica">⏱ {dur} min</span>')
    if niv: pie.append(f'<span class="nivel {niv}">{niv.capitalize()}</span>')
    if not d["encabezado_confiable"]:
        pie.append('<span class="etiqueta-chica dudosa" title="El PDF original no permite leer estos datos">⚠ a confirmar</span>')

    fichas.append(f'''      <a class="ficha" href="{d["archivo"]}"
         data-modalidad="{esc(mod or "")}" data-nivel="{esc(niv or "")}" data-duracion="{dur or ""}">
        <span class="numero">ACTIVIDAD {d["n"]:02d}</span>
        <h3>{esc(d["titulo"])}</h3>
        <p class="resumen">{esc(resumen(d))}</p>
        <div class="pie">{"".join(pie)}</div>
      </a>''')

modalidades = sorted({d["modalidad"] for d in datos if d["modalidad"]})
botones_mod = "\n".join(
    f'      <button class="filtro" data-filtro="modalidad" data-valor="{m}" aria-pressed="false">{ICONO.get(m,"")} {m}</button>'
    for m in modalidades)

html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Actividades micro:bit — Menú</title>
<link rel="stylesheet" href="css/estilos.css?v=2">
</head>
<body class="pagina">

<div class="envoltorio">

  <nav class="migas">
    <a href="index.html">Inicio</a> ·
    <a href="modulo1.html">Módulo 1</a> ·
    <a href="modulo2.html">Módulo 2</a> ·
    <span>Actividades</span>
  </nav>

  <header class="encabezado-menu">
    <h1>Las 28 actividades</h1>
    <p>
      El <strong>Cuaderno de actividades micro:bit</strong> de Ceibal, separado en fichas.
      Cada una es independiente: se puede hacer suelta, en una clase, sin haber hecho las anteriores.
      Entrá a la que quieras y usá las flechas para avanzar.
    </p>
  </header>

  <div class="filtros">
    <span class="titulo-filtro">Modalidad</span>
{botones_mod}
    <button class="filtro" data-filtro="reset" data-valor="" aria-pressed="false">Ver todas</button>
    <span id="recuento"></span>
  </div>

  <div class="rejilla-actividades" id="rejilla">
{chr(10).join(fichas)}
  </div>

  <p style="color:var(--texto-suave); font-size:.82rem; margin-top:3rem; line-height:1.6;">
    Contenido del <em>Cuaderno de actividades micro:bit — Actividades para Educación Básica
    Integrada</em> (Ceibal, Laboratorios Digitales, julio de 2023).
    Autoras: Elisa Cristi, María Elisa Ferenczi y Alicia Ferrando.
    <a href="docs/Cuadernos-Microbit_Actividades.pdf" target="_blank" style="color:var(--acento);">Descargar el cuaderno completo (PDF)</a>.
  </p>

</div>

<script>
/* Filtrado del menú. Sin dependencias: se muestran u ocultan las fichas. */
(function () {{
  var rejilla  = document.getElementById("rejilla");
  var fichas   = Array.prototype.slice.call(rejilla.querySelectorAll(".ficha"));
  var botones  = Array.prototype.slice.call(document.querySelectorAll(".filtro"));
  var recuento = document.getElementById("recuento");
  var activo   = null;

  function aplicar() {{
    var visibles = 0;
    fichas.forEach(function (f) {{
      var pasa = !activo || f.dataset.modalidad === activo;
      f.hidden = !pasa;
      if (pasa) visibles++;
    }});
    recuento.textContent = visibles === fichas.length
      ? fichas.length + " actividades"
      : visibles + " de " + fichas.length + " actividades";
    botones.forEach(function (b) {{
      b.setAttribute("aria-pressed",
        String(b.dataset.filtro === "modalidad" && b.dataset.valor === activo));
    }});
  }}

  botones.forEach(function (b) {{
    b.addEventListener("click", function () {{
      if (b.dataset.filtro === "reset") activo = null;
      else activo = (activo === b.dataset.valor) ? null : b.dataset.valor;
      aplicar();
    }});
  }});

  aplicar();
}})();
</script>
</body>
</html>
'''

io.open(os.path.join(DESTINO, "actividades.html"), "w", encoding="utf-8").write(html)
print("actividades.html generado ·", len(fichas), "fichas ·", len(html), "bytes")
