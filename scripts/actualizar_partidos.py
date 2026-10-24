#!/usr/bin/env python3
"""
La Porra Trollaca - descarga el calendario y los resultados de LaLiga y escribe api/partidos.json
con la jornada en juego y unas cuotas propias, calculadas a partir de la clasificación
(no son cuotas de ninguna casa de apuestas).

Fuente: TheSportsDB (gratis, sin registro). Si falla y existe FOOTBALL_DATA_KEY, prueba football-data.org.
"""
import json, math, os, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "api" / "partidos.json"
TSDB = "https://www.thesportsdb.com/api/v1/json/123/"
LIGA = "4335"   # LaLiga en TheSportsDB


def get_json(url, cab=None):
    import time, urllib.error
    for intento in range(4):
        req = urllib.request.Request(url, headers={"User-Agent": "TrollacosBot/1.0", **(cab or {})})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as ex:
            if ex.code != 429 or intento == 3:
                raise
            time.sleep(35)   # demasiadas consultas: esperar y reintentar


def cuotas(fl, fv):
    """Probabilidades sencillas: diferencia de nivel + ventaja de jugar en casa. Cuotas redondeadas."""
    dif = (fl - fv) + 0.30
    p_emp = max(0.18, min(0.30, 0.28 - 0.06 * abs(dif)))
    p_loc = (1 - p_emp) / (1 + math.exp(-2.2 * dif))
    p_vis = 1 - p_emp - p_loc
    def q(p):
        return round(max(1.15, min(9.0, 0.95 / max(p, 0.01))) * 20) / 20
    return {"1": q(p_loc), "X": q(p_emp), "2": q(p_vis)}


def fuerza(pts, pj):
    """Puntos por partido (con un poco de 'colchón' al principio de temporada)."""
    return (pts + 1.4 * 3) / (pj + 3)


def temporada_actual():
    h = datetime.now(timezone.utc)
    return f"{h.year}-{h.year + 1}" if h.month >= 7 else f"{h.year - 1}-{h.year}"


def tla(nombre):
    letras = "".join(c for c in nombre.upper() if c.isalpha())
    return letras[:3] or "?"


# ---------------- TheSportsDB ----------------
def estado_tsdb(e):
    st = (e.get("strStatus") or "").strip().upper()
    if (e.get("strPostponed") or "").lower() == "yes" or st in ("POSTPONED", "PST"):
        return "POSTPONED"
    if st in ("CANC", "CANCELLED", "ABD", "ABANDONED"):
        return "CANCELLED"
    if st in ("SUSP", "SUSPENDED", "INT"):
        return "SUSPENDED"
    if st in ("MATCH FINISHED", "FT", "AET", "PEN", "AWD", "FINISHED"):
        return "FINISHED"
    if st in ("1H", "2H", "ET", "BT", "P", "LIVE", "IN PLAY"):
        return "IN_PLAY"
    if st in ("HT",):
        return "PAUSED"
    hl, hv = e.get("intHomeScore"), e.get("intAwayScore")
    fecha = fecha_tsdb(e)
    # sin estado claro: si tiene marcador y empezó hace más de 3 horas, lo damos por terminado
    if hl not in (None, "") and hv not in (None, "") and fecha:
        if (datetime.now(timezone.utc) - datetime.fromisoformat(fecha.replace("Z", "+00:00"))).total_seconds() > 3 * 3600:
            return "FINISHED"
    return "TIMED"


def fecha_tsdb(e):
    ts = (e.get("strTimestamp") or "").strip()
    if ts:
        ts = ts.replace(" ", "T").split("+")[0].rstrip("Z")
        return ts[:19] + "Z"
    d, t = e.get("dateEvent"), (e.get("strTime") or "00:00:00")
    return f"{d}T{t[:8]}Z" if d else ""


def num(x):
    try:
        return int(x)
    except (TypeError, ValueError):
        return None


def desde_tsdb():
    import time
    temp = temporada_actual()
    # Las jornadas ya terminadas se guardan en scripts/liga_cache.json: cada una se descarga una sola vez
    fcache = RAIZ / "scripts" / "liga_cache.json"
    try:
        cache = json.loads(fcache.read_text(encoding="utf-8"))
    except Exception:
        cache = {}
    if cache.get("temporada") != temp:
        cache = {"temporada": temp, "rondas": {}}
    def ronda(r):
        time.sleep(3)
        return (get_json(f"{TSDB}eventsround.php?id={LIGA}&r={r}&s={temp}") or {}).get("events") or []
    # última jornada con partidos jugados, según los últimos resultados de la liga (1 consulta)
    pasados = (get_json(f"{TSDB}eventspastleague.php?id={LIGA}") or {}).get("events") or []
    ultima = max([num(e.get("intRound")) or 0 for e in pasados if (e.get("strSeason") or temp) == temp] or [1])
    def guardar_cache():
        fcache.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    def a_cache(r, ev):
        if len(ev) >= 10 and all(estado_tsdb(e) in ("FINISHED", "CANCELLED") for e in ev):
            cache["rondas"][str(r)] = [{k: e.get(k) for k in ("idEvent", "intRound", "idHomeTeam", "idAwayTeam", "strHomeTeam", "strAwayTeam",
                "intHomeScore", "intAwayScore", "strStatus", "strPostponed", "strTimestamp", "dateEvent", "strTime",
                "strHomeTeamBadge", "strAwayTeamBadge")} for e in ev]
            guardar_cache()
    # primero, lo imprescindible: la jornada anterior, la actual y la siguiente (si falla, no se toca nada)
    rondas = {}
    for r in range(max(1, ultima - 1), min(38, ultima + 1) + 1):
        ev = ronda(r)
        if ev:
            rondas[r] = ev
            a_cache(r, ev)
    # después, como mucho 5 jornadas antiguas que falten (para la clasificación); el resto en la siguiente actualización
    nuevas = 0
    for r in range(1, max(1, ultima - 1)):
        if str(r) in cache["rondas"]:
            rondas[r] = cache["rondas"][str(r)]
        elif nuevas < 5:
            nuevas += 1
            try:
                ev = ronda(r)
            except Exception as ex:
                print(f"::warning::Porra: jornada {r} pendiente para la próxima vez ({ex})")
                nuevas = 99
                continue
            if ev:
                rondas[r] = ev
                a_cache(r, ev)
    guardar_cache()
    print(f"::notice::Porra: jornadas guardadas {len(cache['rondas'])}, última jugada {ultima}")
    if not any(rondas.values()):
        raise RuntimeError(f"TheSportsDB no ha devuelto partidos (temporada {temp})")
    # clasificación propia con los resultados de la temporada
    pts, pj = {}, {}
    for evs in rondas.values():
        for e in evs:
            if estado_tsdb(e) != "FINISHED":
                continue
            gl, gv = num(e.get("intHomeScore")), num(e.get("intAwayScore"))
            if gl is None or gv is None:
                continue
            h, a = e.get("idHomeTeam"), e.get("idAwayTeam")
            pj[h] = pj.get(h, 0) + 1; pj[a] = pj.get(a, 0) + 1
            pts[h] = pts.get(h, 0) + (3 if gl > gv else 1 if gl == gv else 0)
            pts[a] = pts.get(a, 0) + (3 if gv > gl else 1 if gl == gv else 0)
    fz = {t: fuerza(pts.get(t, 0), pj[t]) for t in pj}
    nombres = {}
    for evs in rondas.values():
        for e in evs:
            nombres[e.get("idHomeTeam")] = e.get("strHomeTeam"); nombres[e.get("idAwayTeam")] = e.get("strAwayTeam")
    tabla = sorted(pj, key=lambda t: -pts.get(t, 0))
    print("::notice::Porra tabla: " + ", ".join(f"{nombres.get(t)} {pts.get(t,0)}/{pj[t]}" for t in tabla)
          + " | jornadas leídas: " + ",".join(f"{r}:{len(v)}" for r, v in rondas.items()))
    partidos = []
    for r, evs in rondas.items():
        for e in evs:
            est = estado_tsdb(e)
            gl, gv = num(e.get("intHomeScore")), num(e.get("intAwayScore"))
            if est in ("TIMED", "POSTPONED", "CANCELLED"):
                gl = gv = None
            hn, an = e.get("strHomeTeam") or "?", e.get("strAwayTeam") or "?"
            partidos.append({
                "id": str(e.get("idEvent")), "j": num(e.get("intRound")) or r, "fecha": fecha_tsdb(e), "estado": est,
                "local": {"n": hn, "c": e.get("strHomeTeamBadge") or "", "tla": tla(hn)},
                "visit": {"n": an, "c": e.get("strAwayTeamBadge") or "", "tla": tla(an)},
                "gl": gl, "gv": gv,
                "cuotas": cuotas(fz.get(e.get("idHomeTeam"), 1.4), fz.get(e.get("idAwayTeam"), 1.4)),
            })
    return temp, partidos


# ---------------- football-data.org (respaldo) ----------------
def desde_football_data(clave):
    api = "https://api.football-data.org/v4/competitions/PD"
    cab = {"X-Auth-Token": clave}
    datos = get_json(api + "/matches", cab)
    tabla = get_json(api + "/standings", cab)
    fz = {}
    for s in tabla.get("standings", []):
        if s.get("type") == "TOTAL":
            for t in s.get("table", []):
                fz[t["team"]["id"]] = fuerza(t.get("points") or 0, t.get("playedGames") or 0)
    eq = lambda t: {"n": t.get("shortName") or t.get("name") or "?", "c": t.get("crest") or "", "tla": t.get("tla") or ""}
    partidos = []
    for m in datos.get("matches", []):
        ft = (m.get("score") or {}).get("fullTime") or {}
        h, a = m["homeTeam"], m["awayTeam"]
        partidos.append({"id": str(m["id"]), "j": m.get("matchday"), "fecha": m["utcDate"], "estado": m.get("status"),
                         "local": eq(h), "visit": eq(a), "gl": ft.get("home"), "gv": ft.get("away"),
                         "cuotas": cuotas(fz.get(h.get("id"), 1.4), fz.get(a.get("id"), 1.4))})
    return str((datos.get("filters") or {}).get("season") or ""), partidos


def main():
    fuente, temp, partidos = "", "", []
    try:
        temp, partidos = desde_tsdb()
        fuente = "TheSportsDB"
    except Exception as ex:
        print(f"::warning::Porra: TheSportsDB ha fallado: {ex}")
        clave = os.environ.get("FOOTBALL_DATA_KEY", "").strip()
        if clave:
            try:
                temp, partidos = desde_football_data(clave)
                fuente = "football-data.org"
            except Exception as ex2:
                print(f"::warning::Porra: football-data.org también ha fallado: {ex2}")
    partidos = [p for p in partidos if p.get("j") and p.get("fecha")]
    if not partidos:
        print("::warning::Porra: no hay partidos, se deja el fichero como estaba.")
        return 0
    pend = [p["j"] for p in partidos if p["estado"] not in ("FINISHED", "AWARDED", "CANCELLED", "POSTPONED", "SUSPENDED")]
    jornada = min(pend) if pend else max(p["j"] for p in partidos)
    salida = sorted((p for p in partidos if jornada - 2 <= p["j"] <= jornada + 1), key=lambda p: (p["j"], p["fecha"]))
    doc = {"actualizado": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "fuente": fuente,
           "temporada": temp, "jornada": jornada, "partidos": salida}
    SALIDA.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    ej = next((p for p in salida if p["j"] == jornada), salida[0])
    print(f"::notice::Porra ({fuente}): jornada {jornada}, {len(salida)} partidos. Ej: {ej['local']['n']} - {ej['visit']['n']} {ej['fecha']} {ej['estado']} {ej['cuotas']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
