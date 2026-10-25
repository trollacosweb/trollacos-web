<?php
/*
 * Trollaco Run - rankings del arcade (los usan marcadores.php y la cuenta del jugador en porra.php).
 */
// Un ranking por modo: "run" (carrera infinita) y los capítulos del modo historia
$MODOS = ['run' => 'marcadores.php', 'c1' => 'marcadores-c1.php', 'c2' => 'marcadores-c2.php', 'c3' => 'marcadores-c3.php', 'c4' => 'marcadores-c4.php'];
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

// Jugadores de relleno del modo "Supera el récord" (como las recreativas de antes): no se guardan,
// solo completan la lista. Cuando un jugador real les supera, desaparecen solos.
const RELLENO = [
    ['n' => 'PIXEL', 'p' => 3874, 'f' => 74], ['n' => 'ZETA', 'p' => 3512, 'f' => 66], ['n' => 'KIKO', 'p' => 3290, 'f' => 61],
    ['n' => 'LUNA', 'p' => 2985, 'f' => 55], ['n' => 'MAXX', 'p' => 2741, 'f' => 50], ['n' => 'TITO', 'p' => 2468, 'f' => 44],
    ['n' => 'BYTE', 'p' => 2203, 'f' => 39], ['n' => 'CHUSO', 'p' => 1957, 'f' => 34], ['n' => 'NURIA', 'p' => 1720, 'f' => 29],
];

// Los 10 mejores, una sola vez por nombre (su mejor marca)
function lista_final($d, $modo = null) {
    if ($modo === null) { global $modo; }
    $reales = $d['top'];
    usort($reales, function ($a, $b) { return $b['p'] <=> $a['p']; });
    $vistos = []; $lista = [];
    foreach ($reales as $e) {
        $k = strtoupper($e['n']);
        if (isset($vistos[$k])) { continue; }
        $vistos[$k] = true; $lista[] = $e;
        if (count($lista) === 10) { break; }
    }
    // el relleno solo ocupa huecos libres: nunca echa a un jugador real
    if ($modo === 'run') {
        foreach (RELLENO as $r) {
            if (count($lista) >= 10) { break; }
            if (!isset($vistos[$r['n']])) { $lista[] = $r + ['d' => '2026-10-20']; }
        }
        usort($lista, function ($a, $b) { return $b['p'] <=> $a['p']; });
    }
    return $lista;
}
// Mejor marca y puesto de un jugador en un modo
function marca_jugador($modo, $nombre) {
    global $DIR, $MODOS;
    $d = leer_marcador("$DIR/" . $MODOS[$modo]);
    $mejor = null; $nombres = [];
    foreach ($d['top'] as $e) {
        $k = strtoupper($e['n']);
        if (!isset($nombres[$k]) || $e['p'] > $nombres[$k]) { $nombres[$k] = $e['p']; }
        if ($k === $nombre && (!$mejor || $e['p'] > $mejor['p'])) { $mejor = $e; }
    }
    if (!$mejor) { return null; }
    $visibles = lista_final($d, $modo);
    foreach ($visibles as $i => $e) { if (strtoupper($e['n']) === $nombre) { return ['puntos' => $mejor['p'], 'fichas' => $mejor['f'], 'fecha' => $mejor['d'], 'puesto' => $i + 1]; } }
    $delante = 0;
    foreach ($nombres as $k => $p) { if ($p > $mejor['p']) { $delante++; } }
    foreach ($visibles as $e) { if (!isset($nombres[strtoupper($e['n'])]) && $e['p'] > $mejor['p']) { $delante++; } }
    return ['puntos' => $mejor['p'], 'fichas' => $mejor['f'], 'fecha' => $mejor['d'], 'puesto' => $delante + 1];
}
