<?php
/*
 * Trollaco Run - marcador global.
 *   GET  ?accion=lista     -> los 10 mejores
 *   GET  ?accion=empezar   -> ficha firmada para la partida que empieza
 *   POST ?accion=enviar    -> {nombre, puntos, fichas, ficha}
 *   &modo=run|c1           -> ranking de la carrera infinita o del capítulo 1
 */
require __DIR__ . '/comun.php';

// Un ranking por modo: "run" (carrera infinita) y los capítulos del modo historia
$MODOS = ['run' => 'marcadores.php', 'c1' => 'marcadores-c1.php'];
$modo = $_GET['modo'] ?? 'run';
if (!isset($MODOS[$modo])) { $modo = 'run'; }
$FDATOS = "$DIR/" . $MODOS[$modo];

// Cambiar este número borra el ranking (empieza una temporada nueva)
const TEMPORADA = 2;

function leer_marcador($f) {
    global $CABECERA;
    $vacio = ['temporada' => TEMPORADA, 'top' => [], 'usadas' => [], 'ips' => []];
    if (!file_exists($f)) { return $vacio; }
    $j = json_decode(substr(file_get_contents($f), strlen($CABECERA)), true);
    if (!is_array($j)) { return $vacio; }
    if (($j['temporada'] ?? 1) !== TEMPORADA) { $j['top'] = []; $j['temporada'] = TEMPORADA; }
    $j += $vacio;
    // nombres vetados a mano (api/bloqueados.php) desaparecen del ranking
    $vetados = @include __DIR__ . '/bloqueados.php';
    if (is_array($vetados) && $vetados) {
        $v = array_map('strtoupper', $vetados);
        $j['top'] = array_values(array_filter($j['top'], function ($e) use ($v) { return !in_array(strtoupper($e['n']), $v, true); }));
    }
    return $j;
}

function top10($d) {
    return array_map(function ($e) { return ['nombre' => $e['n'], 'puntos' => $e['p'], 'fichas' => $e['f'], 'fecha' => $e['d']]; },
        array_slice($d['top'], 0, 10));
}

$accion = $_GET['accion'] ?? '';

if ($accion === 'lista') {
    responder(['top' => top10(leer_marcador($FDATOS))]);
}

if ($accion === 'empezar') {
    responder(['ficha' => ficha_nueva()]);
}

if ($accion === 'enviar' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $in = entrada();
    $nombre = nombre_o_error($in['nombre'] ?? '');
    $puntos = (int)($in['puntos'] ?? 0);
    $fichas = (int)($in['fichas'] ?? 0);
    if ($puntos < 1) { responder(['error' => 'trampa', 'mensaje' => 'Esa puntuación no cuadra. El Trollaco lo ha visto todo.'], 400); }
    $id = partida_valida($in['ficha'] ?? '', $puntos, $fichas);

    $fl = fopen("$DIR/.cerrojo", 'c');
    flock($fl, LOCK_EX);
    $d = leer_marcador($FDATOS);
    $ahora = time();

    // Ficha de un solo uso
    if (in_array($id, $d['usadas'], true)) { flock($fl, LOCK_UN); responder(['error' => 'ficha', 'mensaje' => 'Esa partida ya se guardó.'], 400); }
    $d['usadas'][] = $id;
    $d['usadas'] = array_slice($d['usadas'], -2000);

    // Un envío cada 10 segundos por conexión
    $q = quien();
    foreach ($d['ips'] as $k => $t) { if ($ahora - $t > 3600) { unset($d['ips'][$k]); } }
    if (isset($d['ips'][$q]) && $ahora - $d['ips'][$q] < 10) {
        flock($fl, LOCK_UN); responder(['error' => 'rapido', 'mensaje' => 'Espera unos segundos.'], 429);
    }
    $d['ips'][$q] = $ahora;

    $d['top'][] = ['n' => $nombre, 'p' => $puntos, 'f' => $fichas, 'd' => date('Y-m-d')];
    usort($d['top'], function ($a, $b) { return $b['p'] <=> $a['p']; });
    $d['top'] = array_slice($d['top'], 0, 100);

    guardar_json($FDATOS, $d);
    flock($fl, LOCK_UN);

    $pos = 0;
    foreach ($d['top'] as $i => $e) { if ($e['n'] === $nombre && $e['p'] === $puntos) { $pos = $i + 1; break; } }
    responder(['ok' => true, 'puesto' => $pos, 'top' => top10($d)]);
}

responder(['error' => 'accion'], 400);
