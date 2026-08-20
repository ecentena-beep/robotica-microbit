# -*- coding: utf-8 -*-
"""Extracción definitiva de las 28 actividades del Cuaderno micro:bit."""
import io, re, json

INDICE = [
 (1,"Música:bit",14),(2,"Semáforo peatonal",17),(3,"Adivina, adivinador, ¿qué animal es?",20),
 (4,"TQM, jugando con abreviaturas",24),(5,"Tiro al blanco",27),(6,"Póster interactivo",32),
 (7,"Otra forma de comunicarnos",36),(8,"Morfemas",41),(9,"Morfemas gráficos",46),
 (10,"Notas musicales",50),(11,"El barrio de nuestro centro educativo",53),
 (12,"Modelo: energía térmica y temperatura",58),(13,"Semáforo con cuenta regresiva",63),
 (14,"Semáforo con alerta sonora",67),(15,"Cubreasiento inteligente",71),
 (16,"Prevención de incendios",77),(17,"La ruleta del saber",82),
 (18,"Dado versus dado «arreglado»",86),(19,"Buena postura",90),(20,"¡Que no caiga!",94),
 (21,"Búsqueda de tarjetas",100),(22,"Aula sostenible",105),(23,"Dado de palabras",111),
 (24,"Micro:pedaleando en Scratch",116),(25,"¿Se divide?",121),(26,"¡Dime hacia dónde!",126),
 (27,"Sorteo de flechas",132),(28,"Distancia",138),
]
FIN = 145
PLAUSIBLES = {"45","60","90","135","180","225","270"}
MOD = ("Individual","Grupal","Duplas","Parejas")
MARCAS = ["PROPÓSITOS","PROPÓSITO","OBJETIVOS","OBJETIVO","ESPACIOS CURRICULARES",
          "CONTENIDOS MICRO:BIT","MATERIALES","DESARROLLO","AUTOEVALUACIÓN","COEVALUACIÓN"]

txt = io.open("act_paginado.txt", encoding="utf-8").read()
paginas = txt.split("\f")
limpiar = lambda s: re.sub(r"\s+", " ", s).strip()

def secciones(bloque):
    pos = []
    for m in MARCAS:
        mm = re.search(re.escape(m), bloque)
        if mm: pos.append((mm.start(), m, mm.end()))
    pos.sort()
    # descartar el singular si ya está el plural en la misma posición
    filtrado = []
    for p, m, e in pos:
        if filtrado and p - filtrado[-1][0] < 3: continue
        filtrado.append((p, m, e))
    out = {}
    for i, (p, m, e) in enumerate(filtrado):
        fin = filtrado[i+1][0] if i+1 < len(filtrado) else len(bloque)
        out[m] = limpiar(bloque[e:fin])
    return out

def viñetas(s):
    """Parte un texto del cuaderno en ítems por • y ·"""
    if not s: return []
    partes = re.split(r"\s*[•]\s*", s)
    items = []
    for p in partes:
        p = p.strip(" ·").strip()
        if len(p) > 1: items.append(p)
    return items

datos = []
for i, (num, titulo, ini) in enumerate(INDICE):
    fin = INDICE[i+1][2] if i+1 < len(INDICE) else FIN
    bloque = "\n".join(paginas[ini-1:fin-1])
    cab = paginas[ini-1]

    crudo = re.findall(r"(\d+)\s*minutos", cab)
    mods  = [m for m in MOD if m in cab]
    dur_ok = len(crudo) == 1 and crudo[0] in PLAUSIBLES
    mod_ok = len(mods) == 1

    # epígrafe: línea entre la modalidad y OBJETIVOS/PROPÓSITOS, entre comillas
    epi = ""
    me = re.search(r"«([^»]{15,300})»\.?\s*([A-ZÁÉÍÓÚÑ][\w\s.áéíóúñÀ-ÿ]{2,40})?", cab)
    if me:
        epi = "«" + limpiar(me.group(1)) + "»"
        if me.group(2): epi += " — " + limpiar(me.group(2))

    sec = secciones(bloque)
    obj = sec.get("PROPÓSITOS") or sec.get("PROPÓSITO") or sec.get("OBJETIVOS") or sec.get("OBJETIVO") or ""
    # el epígrafe se cuela al principio del objetivo: sacarlo
    if epi and obj.startswith("«"):
        obj = re.sub(r"^«[^»]*»\.?\s*[^.]{0,45}?\s*(?=[A-ZÁÉÍÓÚ])", "", obj, count=1)

    datos.append({
        "n": num, "titulo": titulo, "pag_inicio": ini, "pag_fin": fin-1,
        "modalidad": mods[0] if mod_ok else None,
        "duracion": int(crudo[0]) if dur_ok else None,
        "nivel": None,                       # no se pudo leer del PDF
        "encabezado_confiable": dur_ok and mod_ok,
        "epigrafe": epi,
        "objetivo": obj,
        "espacios": viñetas(sec.get("ESPACIOS CURRICULARES","")),
        "contenidos": viñetas(sec.get("CONTENIDOS MICRO:BIT","")),
        "materiales": viñetas(sec.get("MATERIALES","")),
        "desarrollo": sec.get("DESARROLLO",""),
    })

faltan = [d["n"] for d in datos if not d["encabezado_confiable"]]
sin_obj = [d["n"] for d in datos if len(d["objetivo"]) < 20]
print(f"actividades: {len(datos)}")
print(f"encabezado a confirmar: {faltan}")
print(f"sin objetivo: {sin_obj}\n")
for d in datos:
    print(f"{d['n']:2d}. {d['titulo'][:32]:34s} {str(d['modalidad'] or '?'):11s} {str(d['duracion'] or '?'):>4}min "
          f"obj={len(d['objetivo']):3d} esp={len(d['espacios'])} cont={len(d['contenidos'])} mat={len(d['materiales'])} des={len(d['desarrollo'])}")
io.open("actividades.json","w",encoding="utf-8").write(json.dumps(datos, ensure_ascii=False, indent=1))
