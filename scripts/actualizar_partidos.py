#!/usr/bin/env python3
"""
La Porra Trollaca - descarga el calendario y los resultados de LaLiga (football-data.org)
y escribe api/partidos.json con la jornada en juego y unas cuotas propias, calculadas
a partir de la clasificación (no son cuotas de ninguna casa de apuestas).

Necesita la variable de entorno FOOTBALL_DATA_KEY (secreto de GitHub). Si no está, no hace nada.
"""
import json, math, os, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "api" / "partidos.json"
API = "https://api.football-data.org/v4/competitions/PD"


def pedir(ruta, clave):
    req = urllib.request.Request(API + ruta, headers={"X-Auth-Token": clave, "User-Agent": "TrollacosBot/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def fuerza(clasif):
    """Puntos por partido de cada equipo (con un poco de 'colchón' al principio de temporada)."""
    f = {}
    for t in clasif:
        pj = t.get("playedGames") or 0
        pts = t.get("points") or 0
        f[t["team"]["id"]] = (pts + 1.4 * 3) / (pj + 3)   # se parte de 1,4 pts/partido para no exagerar con pocas jornadas
    return f


def cuotas(fl, fv):
    """Probabilidades sencillas: diferencia de nivel + ventaja de jugar en casa. Cuotas redondeadas."""
    dif = (fl - fv) + 0.30
    p_emp = max(0.18, min(0.30, 0.28 - 0.06 * abs(dif)))
    p_loc = (1 - p_emp) / (1 + math.exp(-2.2 * dif))
    p_vis = 1 - p_emp - p_loc
    def q(p):
        return round(max(1.15, min(9.0, 0.95 / max(p, 0.01))) * 20) / 20
    return {"1": q(p_loc), "X": q(p_emp), "2": q(p_vis)}


def equipo(t):
    return {"n": t.get("shortName") or t.get("name") or "?", "c": t.get("crest") or "", "tla": t.get("tla") or ""}


def main():
    clave = os.environ.get("FOOTBALL_DATA_KEY", "").strip()
    if not clave:
        print("Sin FOOTBALL_DATA_KEY: no se actualizan los partidos.")
        return 0
    try:
        datos = pedir("/matches", clave)
        tabla = pedir("/standings", clave)
    except Exception as ex:
        print(f"No se han podido leer los partidos: {ex}")
        return 0
    clasif = []
    for s in tabla.get("standings", []):
        if s.get("type") == "TOTAL":
            clasif = s.get("table", [])
    f = fuerza(clasif)
    partidos = datos.get("matches", [])
    if not partidos:
        print("La API no ha devuelto partidos.")
        return 0
    # jornada en juego = la primera que aún tiene partidos sin terminar
    pend = [m["matchday"] for m in partidos if m.get("status") not in ("FINISHED", "AWARDED")]
    jornada = min(pend) if pend else max(m["matchday"] for m in partidos)
    salida = []
    for m in partidos:
        j = m.get("matchday")
        if j is None or not (jornada - 2 <= j <= jornada + 1):
            continue
        h, a = m["homeTeam"], m["awayTeam"]
        ft = (m.get("score") or {}).get("fullTime") or {}
        salida.append({
            "id": m["id"], "j": j, "fecha": m["utcDate"], "estado": m.get("status"),
            "local": equipo(h), "visit": equipo(a),
            "gl": ft.get("home"), "gv": ft.get("away"),
            "cuotas": cuotas(f.get(h.get("id"), 1.4), f.get(a.get("id"), 1.4)),
        })
    salida.sort(key=lambda p: (p["j"], p["fecha"]))
    temporada = (datos.get("filters") or {}).get("season") or (salida[0]["fecha"][:4] if salida else "")
    doc = {"actualizado": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "temporada": temporada,
           "jornada": jornada, "partidos": salida}
    SALIDA.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Partidos actualizados: jornada {jornada}, {len(salida)} partidos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
