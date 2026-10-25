<?php
/*
 * La Porra Trollaca - pronósticos de LaLiga con fichas del arcade. SIN DINERO REAL:
 * las fichas no se compran ni se canjean por nada.
 *
 *   POST ?accion=registrar  {nombre}                      -> crea cuenta y devuelve su código secreto
 *   POST ?accion=yo         {nombre, codigo}              -> fichas, pronósticos y movimientos
 *   POST ?accion=apostar    {nombre, codigo, partido, tipo: "1x2"|"exacto", seleccion, cantidad}
 *   POST ?accion=arcade     {nombre, codigo, ficha, puntos, fichas}  -> suma las fichas de una partida
 *   POST ?accion=cancelar   {nombre, codigo, id}          -> anula un pronóstico pendiente y devuelve las fichas
 *   GET  ?accion=ranking                                  -> los 10 con más fichas
 *   GET  ?accion=partidos                                 -> jornada con cuotas (lee partidos.json)
 */
require __DIR__ . '/comun.php';

const BONO_BIENVENIDA = 10;   // fichas al crear la cuenta
const BONO_JORNADA    = 10;   // fichas por participar en cada jornada (al hacer el primer pronóstico)
const CUOTA_EXACTO    = 8.0;  // el resultado exacto paga x8
const CIERRE_SEG      = 300;  // no se admiten pronósticos 5 minutos antes del partido

$FPORRA = "$DIR/porra.php";
$FPARTIDOS = __DIR__ . '/partidos.json';
$VACIO = ['usuarios' => [], 'apuestas' => [], 'arcade' => [], 'fallos' => [], 'altas' => []];

function partidos() {
    global $FPARTIDOS;
    $j = @json_decode(@file_get_contents($FPARTIDOS), true);
    return is_array($j) ? $j : ['partidos' => [], 'jornada' => null, 'actualizado' => null];
}
function partido_por_id($pp, $id) {
    foreach ($pp['partidos'] as $p) { if ((string)$p['id'] === (string)$id) { return $p; } }
    return null;
}
function hash_codigo($nombre, $codigo) {
    global $SECRETO;
    return hash_hmac('sha256', $nombre . '|' . strtoupper(trim($codigo)), $SECRETO);
}
function codigo_nuevo() {
    $abc = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
    $c = '';
    for ($i = 0; $i < 8; $i++) { $c .= $abc[random_int(0, strlen($abc) - 1)]; }
    return $c;
}

// Abre los datos con cerrojo, liquida lo que haya terminado y devuelve [datos, cerrojo]
function abrir() {
    global $DIR, $FPORRA, $VACIO;
    $fl = fopen("$DIR/.cerrojo-porra", 'c');
    flock($fl, LOCK_EX);
    $d = leer_json($FPORRA, $VACIO);
    liquidar($d);
    return [$d, $fl];
}
function cerrar($d, $fl, $guardar = true) {
    global $FPORRA;
    if ($guardar) { guardar_json($FPORRA, $d); }
    flock($fl, LOCK_UN);
}

// Reparte fichas de los pronósticos cuyo partido ya ha terminado (o devuelve si se suspendió)
function liquidar(&$d) {
    $pp = partidos();
    foreach ($d['apuestas'] as &$a) {
        if ($a['e'] !== 'pendiente') { continue; }
        $p = partido_por_id($pp, $a['p']);
        if (!$p) { continue; }
        $u = &$d['usuarios'][$a['u']];
        if ($p['estado'] === 'FINISHED' && $p['gl'] !== null && $p['gv'] !== null) {
            $res = $p['gl'] > $p['gv'] ? '1' : ($p['gl'] < $p['gv'] ? '2' : 'X');
            $gana = $a['t'] === '1x2' ? ($a['s'] === $res) : ($a['s'] === $p['gl'] . '-' . $p['gv']);
            if ($gana) {
                $a['e'] = 'ganada'; $a['g'] = (int)floor($a['c'] * $a['q']);
                $u['f'] += $a['g']; $u['ac'] = ($u['ac'] ?? 0) + 1;
            } else { $a['e'] = 'perdida'; $a['g'] = 0; }
        } elseif (in_array($p['estado'], ['POSTPONED', 'CANCELLED', 'SUSPENDED', 'AWARDED'], true)
                  && time() > strtotime($p['fecha']) + 3 * 86400) {
            $a['e'] = 'devuelta'; $a['g'] = $a['c']; $u['f'] += $a['c'];
        }
        unset($u);
    }
    unset($a);
}

// Comprueba nombre y código. Limita los intentos fallidos por conexión.
function usuario(&$d, $in) {
    $nombre = strtoupper(strtr(preg_replace('/\s+/u', '', (string)($in['nombre'] ?? '')), ['á'=>'Á','é'=>'É','í'=>'Í','ó'=>'Ó','ú'=>'Ú','ñ'=>'Ñ','ü'=>'Ü']));
    $codigo = (string)($in['codigo'] ?? '');
    $q = quien(); $ahora = time();
    $d['fallos'][$q] = array_values(array_filter($d['fallos'][$q] ?? [], function ($t) use ($ahora) { return $ahora - $t < 3600; }));
    if (count($d['fallos'][$q]) >= 10) { return [null, 'Demasiados intentos. Prueba dentro de un rato.']; }
    $u = $d['usuarios'][$nombre] ?? null;
    if (!$u || !hash_equals($u['h'], hash_codigo($nombre, $codigo))) {
        $d['fallos'][$q][] = $ahora;
        return [null, 'Nombre o código incorrectos.'];
    }
    return [$nombre, null];
}

function resumen($d, $nombre) {
    $u = $d['usuarios'][$nombre];
    $mias = array_values(array_filter($d['apuestas'], function ($a) use ($nombre) { return $a['u'] === $nombre; }));
    usort($mias, function ($a, $b) { return $b['ts'] <=> $a['ts']; });
    $mias = array_map(function ($a) { return ['id' => $a['id'], 'partido' => $a['p'], 'jornada' => $a['j'], 'tipo' => $a['t'], 'seleccion' => $a['s'],
        'cantidad' => $a['c'], 'cuota' => $a['q'], 'estado' => $a['e'], 'premio' => $a['g'] ?? 0]; }, array_slice($mias, 0, 40));
    return ['nombre' => $nombre, 'fichas' => $u['f'], 'aciertos' => $u['ac'] ?? 0, 'jornadas' => $u['jb'] ?? [], 'pronosticos' => $mias];
}

$accion = $_GET['accion'] ?? '';
$post = $_SERVER['REQUEST_METHOD'] === 'POST';

if ($accion === 'partidos') {
    responder(partidos());
}

if ($accion === 'ranking') {
    [$d, $fl] = abrir();
    cerrar($d, $fl);
    $us = array_values($d['usuarios']);
    usort($us, function ($a, $b) { return $b['f'] <=> $a['f']; });
    responder(['top' => array_map(function ($u) { return ['nombre' => $u['n'], 'fichas' => $u['f'], 'aciertos' => $u['ac'] ?? 0]; }, array_slice($us, 0, 10)),
               'jugadores' => count($us)]);
}

if ($accion === 'registrar' && $post) {
    $in = entrada();
    $nombre = nombre_o_error($in['nombre'] ?? '');
    [$d, $fl] = abrir();
    $q = quien(); $ahora = time();
    // como mucho 3 cuentas nuevas por conexión y día
    $d['altas'][$q] = array_values(array_filter($d['altas'][$q] ?? [], function ($t) use ($ahora) { return $ahora - $t < 86400; }));
    if (count($d['altas'][$q]) >= 3) { cerrar($d, $fl); responder(['error' => 'rapido', 'mensaje' => 'Ya has creado varias cuentas hoy. Vuelve mañana.'], 429); }
    if (isset($d['usuarios'][$nombre])) { cerrar($d, $fl, false); responder(['error' => 'ocupado', 'mensaje' => 'Ese nombre ya está cogido. Prueba con otro.'], 400); }
    $codigo = codigo_nuevo();
    $d['usuarios'][$nombre] = ['n' => $nombre, 'h' => hash_codigo($nombre, $codigo), 'f' => BONO_BIENVENIDA, 'c' => $ahora, 'jb' => [], 'ac' => 0];
    $d['altas'][$q][] = $ahora;
    cerrar($d, $fl);
    responder(['ok' => true, 'nombre' => $nombre, 'codigo' => $codigo, 'fichas' => BONO_BIENVENIDA]);
}

if ($accion === 'yo' && $post) {
    $in = entrada();
    [$d, $fl] = abrir();
    [$nombre, $err] = usuario($d, $in);
    cerrar($d, $fl);
    if (!$nombre) { responder(['error' => 'login', 'mensaje' => $err], 401); }
    responder(['ok' => true] + resumen($d, $nombre));
}

if ($accion === 'arcade' && $post) {
    $in = entrada();
    $puntos = (int)($in['puntos'] ?? 0); $fichas = (int)($in['fichas'] ?? 0);
    $id = partida_valida($in['ficha'] ?? '', $puntos, $fichas);
    [$d, $fl] = abrir();
    [$nombre, $err] = usuario($d, $in);
    if (!$nombre) { cerrar($d, $fl); responder(['error' => 'login', 'mensaje' => $err], 401); }
    if (in_array($id, $d['arcade'], true)) { cerrar($d, $fl, false); responder(['error' => 'ficha', 'mensaje' => 'Esas fichas ya se sumaron.'], 400); }
    $d['arcade'][] = $id; $d['arcade'] = array_slice($d['arcade'], -5000);
    $d['usuarios'][$nombre]['f'] += $fichas;
    cerrar($d, $fl);
    responder(['ok' => true, 'sumadas' => $fichas, 'fichas' => $d['usuarios'][$nombre]['f']]);
}

if ($accion === 'apostar' && $post) {
    $in = entrada();
    $tipo = (string)($in['tipo'] ?? '');
    $sel = strtoupper(trim((string)($in['seleccion'] ?? '')));
    $cant = (int)($in['cantidad'] ?? 0);
    if (!in_array($tipo, ['1x2', 'exacto'], true)) { responder(['error' => 'datos'], 400); }
    if ($tipo === '1x2' && !in_array($sel, ['1', 'X', '2'], true)) { responder(['error' => 'datos'], 400); }
    if ($tipo === 'exacto') {
        if (!preg_match('/^(\d{1,2})-(\d{1,2})$/', $sel, $m) || $m[1] > 15 || $m[2] > 15) { responder(['error' => 'datos', 'mensaje' => 'Pon un resultado como 2-1.'], 400); }
        $sel = ((int)$m[1]) . '-' . ((int)$m[2]);
    }
    if ($cant < 1 || $cant > 1000000) { responder(['error' => 'cantidad', 'mensaje' => 'Pon cuántas fichas quieres jugar.'], 400); }

    $p = partido_por_id(partidos(), $in['partido'] ?? '');
    if (!$p) { responder(['error' => 'partido', 'mensaje' => 'Ese partido no está disponible.'], 400); }
    if (!in_array($p['estado'], ['SCHEDULED', 'TIMED'], true) || time() > strtotime($p['fecha']) - CIERRE_SEG) {
        responder(['error' => 'cerrado', 'mensaje' => 'Este partido ya está cerrado para pronósticos.'], 400);
    }
    $cuota = $tipo === '1x2' ? (float)($p['cuotas'][$sel] ?? 0) : CUOTA_EXACTO;
    if ($cuota < 1.01) { responder(['error' => 'partido', 'mensaje' => 'Este partido aún no tiene cuotas.'], 400); }

    [$d, $fl] = abrir();
    [$nombre, $err] = usuario($d, $in);
    if (!$nombre) { cerrar($d, $fl); responder(['error' => 'login', 'mensaje' => $err], 401); }
    foreach ($d['apuestas'] as $a) {
        if ($a['u'] === $nombre && (string)$a['p'] === (string)$p['id'] && $a['t'] === $tipo) {
            cerrar($d, $fl, false); responder(['error' => 'repetida', 'mensaje' => 'Ya tienes un pronóstico de este tipo en este partido.'], 400);
        }
    }
    $u = &$d['usuarios'][$nombre];
    $bono = 0;
    if (!in_array($p['j'], $u['jb'] ?? [], true)) { $u['jb'][] = $p['j']; $u['f'] += BONO_JORNADA; $bono = BONO_JORNADA; }
    if ($cant > $u['f']) { if ($bono) { $u['f'] -= $bono; array_pop($u['jb']); } cerrar($d, $fl, false); responder(['error' => 'fichas', 'mensaje' => 'No tienes fichas suficientes. ¡Juega a Trollaco Run para ganar más!'], 400); }
    $u['f'] -= $cant;
    $d['apuestas'][] = ['id' => bin2hex(random_bytes(6)), 'u' => $nombre, 'p' => $p['id'], 'j' => $p['j'], 't' => $tipo, 's' => $sel,
                        'c' => $cant, 'q' => $cuota, 'e' => 'pendiente', 'g' => 0, 'ts' => time()];
    unset($u);
    cerrar($d, $fl);
    responder(['ok' => true, 'bono' => $bono] + resumen($d, $nombre));
}

if ($accion === 'cancelar' && $post) {
    $in = entrada();
    $id = (string)($in['id'] ?? '');
    [$d, $fl] = abrir();
    [$nombre, $err] = usuario($d, $in);
    if (!$nombre) { cerrar($d, $fl); responder(['error' => 'login', 'mensaje' => $err], 401); }
    $pp = partidos();
    foreach ($d['apuestas'] as $i => $a) {
        if ($a['id'] !== $id || $a['u'] !== $nombre) { continue; }
        if ($a['e'] !== 'pendiente') { cerrar($d, $fl, false); responder(['error' => 'cerrado', 'mensaje' => 'Ese pronóstico ya está resuelto.'], 400); }
        $p = partido_por_id($pp, $a['p']);
        if (!$p || !in_array($p['estado'], ['SCHEDULED', 'TIMED'], true) || time() > strtotime($p['fecha']) - CIERRE_SEG) {
            cerrar($d, $fl, false); responder(['error' => 'cerrado', 'mensaje' => 'El partido ya está cerrado: no se puede cancelar.'], 400);
        }
        $d['usuarios'][$nombre]['f'] += $a['c'];
        array_splice($d['apuestas'], $i, 1);
        cerrar($d, $fl);
        responder(['ok' => true, 'devueltas' => $a['c']] + resumen($d, $nombre));
    }
    cerrar($d, $fl, false);
    responder(['error' => 'datos', 'mensaje' => 'No encuentro ese pronóstico.'], 400);
}

responder(['error' => 'accion'], 400);
