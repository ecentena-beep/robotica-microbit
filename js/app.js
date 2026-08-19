/* ============================================================
   Robótica — Motor del deck de slides
   No hay que tocar este archivo para agregar contenido:
   basta con agregar <section class="slide"> en el HTML.
   ============================================================ */

(function () {
  "use strict";

  var slides       = Array.prototype.slice.call(document.querySelectorAll(".slide"));
  var barra        = document.getElementById("barra-progreso");
  var contador     = document.getElementById("contador");
  var btnAnterior  = document.getElementById("btn-anterior");
  var btnSiguiente = document.getElementById("btn-siguiente");
  var btnIndice    = document.getElementById("btn-indice");
  var btnPantalla  = document.getElementById("btn-pantalla");
  var panelIndice  = document.getElementById("indice");
  var listaIndice  = document.getElementById("lista-indice");
  var panelAyuda   = document.getElementById("ayuda");

  if (!slides.length) return;

  var actual = 0;

  /* ---------- Guardar la posición para no perderla al recargar ---------- */
  var CLAVE = "robotica-slide-" + (document.body.dataset.deck || "principal");

  function guardarPosicion() {
    try { localStorage.setItem(CLAVE, String(actual)); } catch (e) {}
  }

  function posicionInicial() {
    // 1) Prioridad: el número en la URL (#5) para poder compartir un slide puntual
    var desdeHash = parseInt(location.hash.replace("#", ""), 10);
    if (!isNaN(desdeHash) && desdeHash >= 1 && desdeHash <= slides.length) {
      return desdeHash - 1;
    }
    // 2) Si no, la última slide vista
    try {
      var guardada = parseInt(localStorage.getItem(CLAVE), 10);
      if (!isNaN(guardada) && guardada >= 0 && guardada < slides.length) return guardada;
    } catch (e) {}
    return 0;
  }

  /* ---------- Mostrar una slide ---------- */
  function mostrar(indice, haciaAtras) {
    indice = Math.max(0, Math.min(slides.length - 1, indice));

    slides.forEach(function (s) {
      s.classList.remove("activa", "hacia-atras");
    });

    var slide = slides[indice];
    slide.classList.add("activa");
    if (haciaAtras) slide.classList.add("hacia-atras");
    slide.scrollTop = 0;

    actual = indice;

    // Progreso y contador
    var porcentaje = slides.length > 1 ? (indice / (slides.length - 1)) * 100 : 100;
    barra.style.width = porcentaje + "%";
    contador.textContent = (indice + 1) + " / " + slides.length;

    btnAnterior.disabled  = indice === 0;
    btnSiguiente.disabled = indice === slides.length - 1;

    // URL sin ensuciar el historial
    history.replaceState(null, "", "#" + (indice + 1));
    guardarPosicion();
    marcarIndiceActual();
    reiniciarMedios(slide);
  }

  /* Pausa videos de otras slides para que no sigan sonando */
  function reiniciarMedios(slideActiva) {
    slides.forEach(function (s) {
      if (s === slideActiva) return;
      s.querySelectorAll("video, audio").forEach(function (m) {
        if (!m.paused) m.pause();
      });
      s.querySelectorAll("iframe").forEach(function (f) {
        // Recargar el iframe detiene la reproducción de YouTube y similares
        if (f.dataset.pausable === "si") f.src = f.src;
      });
    });
  }

  function siguiente() { if (actual < slides.length - 1) mostrar(actual + 1, false); }
  function anterior()  { if (actual > 0) mostrar(actual - 1, true); }

  /* ---------- Índice de slides ---------- */
  function construirIndice() {
    listaIndice.innerHTML = "";
    slides.forEach(function (s, i) {
      var titulo = s.dataset.titulo;
      if (!titulo) {
        var h = s.querySelector("h1, h2, h3");
        titulo = h ? h.textContent.trim() : "Slide " + (i + 1);
      }
      var li = document.createElement("li");
      var b  = document.createElement("button");
      b.innerHTML = '<span class="num">' + String(i + 1).padStart(2, "0") + "</span><span>" + titulo + "</span>";
      b.addEventListener("click", function () {
        cerrarPaneles();
        mostrar(i, i < actual);
      });
      li.appendChild(b);
      listaIndice.appendChild(li);
    });
  }

  function marcarIndiceActual() {
    var botones = listaIndice.querySelectorAll("button");
    botones.forEach(function (b, i) {
      b.classList.toggle("actual", i === actual);
    });
  }

  function alternarIndice() {
    panelAyuda.classList.remove("abierto");
    panelIndice.classList.toggle("abierto");
  }

  function alternarAyuda() {
    panelIndice.classList.remove("abierto");
    panelAyuda.classList.toggle("abierto");
  }

  function cerrarPaneles() {
    panelIndice.classList.remove("abierto");
    panelAyuda.classList.remove("abierto");
  }

  function hayPanelAbierto() {
    return panelIndice.classList.contains("abierto") || panelAyuda.classList.contains("abierto");
  }

  /* ---------- Pantalla completa ---------- */
  function alternarPantallaCompleta() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(function () {});
    } else {
      document.exitFullscreen();
    }
  }

  /* ---------- Teclado ---------- */
  document.addEventListener("keydown", function (e) {
    if (e.ctrlKey || e.altKey || e.metaKey) return;

    switch (e.key) {
      case "ArrowRight":
      case "PageDown":
      case " ":
        e.preventDefault();
        cerrarPaneles();
        siguiente();
        break;
      case "ArrowLeft":
      case "PageUp":
        e.preventDefault();
        cerrarPaneles();
        anterior();
        break;
      case "Home":
        e.preventDefault();
        mostrar(0, true);
        break;
      case "End":
        e.preventDefault();
        mostrar(slides.length - 1, false);
        break;
      case "o":
      case "O":
        e.preventDefault();
        alternarIndice();
        break;
      case "f":
      case "F":
        e.preventDefault();
        alternarPantallaCompleta();
        break;
      case "?":
      case "h":
      case "H":
        e.preventDefault();
        alternarAyuda();
        break;
      case "Escape":
        if (hayPanelAbierto()) {
          e.preventDefault();
          cerrarPaneles();
        }
        break;
    }
  });

  /* ---------- Botones y zonas de clic ---------- */
  btnSiguiente.addEventListener("click", siguiente);
  btnAnterior.addEventListener("click", anterior);
  btnIndice.addEventListener("click", alternarIndice);
  btnPantalla.addEventListener("click", alternarPantallaCompleta);

  document.querySelector(".zona-clic.der").addEventListener("click", siguiente);
  document.querySelector(".zona-clic.izq").addEventListener("click", anterior);

  panelIndice.addEventListener("click", function (e) {
    if (e.target === panelIndice) cerrarPaneles();
  });
  panelAyuda.addEventListener("click", function (e) {
    if (e.target === panelAyuda) cerrarPaneles();
  });

  /* ---------- Deslizar con el dedo (tablet / celular) ---------- */
  var xInicio = null, yInicio = null;

  document.addEventListener("touchstart", function (e) {
    xInicio = e.changedTouches[0].clientX;
    yInicio = e.changedTouches[0].clientY;
  }, { passive: true });

  document.addEventListener("touchend", function (e) {
    if (xInicio === null) return;
    var dx = e.changedTouches[0].clientX - xInicio;
    var dy = e.changedTouches[0].clientY - yInicio;
    // Solo si el gesto fue claramente horizontal (para no romper el scroll)
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.6) {
      if (dx < 0) siguiente(); else anterior();
    }
    xInicio = yInicio = null;
  }, { passive: true });

  /* ---------- Tablas anchas en celulares ----------
     Una tabla de 3 o 4 columnas no entra en una pantalla angosta. En vez de
     que se desborde el slide entero, se la envuelve en una caja que se
     desliza sola. Se hace acá para que valga para cualquier tabla que se
     agregue después, sin tener que acordarse de envolverla a mano. */
  function envolverTablas() {
    slides.forEach(function (s) {
      s.querySelectorAll("table").forEach(function (tabla) {
        if (tabla.parentNode.classList.contains("tabla-scroll")) return;
        var caja = document.createElement("div");
        caja.className = "tabla-scroll";
        tabla.parentNode.insertBefore(caja, tabla);
        caja.appendChild(tabla);
      });
    });
  }

  /* ---------- Cambios de #numero en la URL ----------
     Necesario para que funcione compartir un slide puntual: si alguien ya
     tiene la página abierta y pega un enlace con otro #, el navegador no
     recarga, así que hay que reaccionar al cambio a mano.
     La guardia (indice !== actual) evita un bucle infinito, porque mostrar()
     también reescribe el hash. */
  window.addEventListener("hashchange", function () {
    var n = parseInt(location.hash.replace("#", ""), 10);
    if (isNaN(n) || n < 1 || n > slides.length) return;
    var indice = n - 1;
    if (indice !== actual) mostrar(indice, indice < actual);
  });

  /* ---------- Arranque ---------- */
  envolverTablas();
  construirIndice();
  mostrar(posicionInicial(), false);
})();
