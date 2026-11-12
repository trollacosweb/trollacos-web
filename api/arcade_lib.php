<?php
/*
 * Trollaco Run - rankings del arcade (los usan marcadores.php y la cuenta del jugador en porra.php).
 */
// Un ranking por modo: "run" (carrera infinita) y los capítulos del modo historia
$MODOS = ['run' => 'marcadores.php', 'c1' => 'marcadores-c1.php', 'c2' => 'marcadores-c2.php', 'c3' => 'marcadores-c3.php', 'c4' => 'marcadores-c4.php', 'c5' => 'marcadores-c5.php', 'c6' => 'marcadores-c6.php', 'c7' => 'marcadores-c7.php', 'c8' => 'marcadores-c8.php'];
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

// Jugadores de relleno (como las recreativas de antes): no se guardan, solo completan la lista de cada modo.
// Nunca echan a un jugador real (solo ocupan huecos libres) y siempre quedan por debajo del mejor jugador real del modo.
const RELLENO = [
    'run' => [['PIXEL', 3874, 74], ['ZETA', 3512, 66], ['KIKO', 3290, 61], ['LUNA', 2985, 55], ['MAXX', 2741, 50],
              ['TITO', 2468, 44], ['BYTE', 2203, 39], ['CHUSO', 1957, 34], ['NURIA', 1720, 29]],
    'c1' => [['LUNA', 3412, 41], ['DAVO', 3388, 39], ['ZETA', 3301, 33], ['TXEMA', 3215, 27], ['IRENE', 2876, 22],
             ['KIKO', 2510, 19], ['ROCIO', 2104, 15], ['PACO7', 1688, 11], ['BYTE', 1240, 8]],
    'c2' => [['PIXEL', 3611, 44], ['NANDO', 3540, 40], ['LUNA', 3466, 35], ['SERGI', 3290, 29], ['MAXX', 2950, 24],
             ['GUAJE', 2533, 18], ['IRENE', 2120, 14], ['TITO', 1702, 10], ['ROCIO', 1315, 7]],
    'c3' => [['ZETA', 3790, 46], ['DAVO', 3702, 41], ['PIXEL', 3655, 37], ['LAURA', 3401, 30], ['TXEMA', 3010, 23],
             ['NANDO', 2602, 17], ['PEPU', 2188, 13], ['CHUSO', 1730, 9], ['KIKO', 1294, 6]],
    'c4' => [['LUNA', 3955, 47], ['SERGI', 3871, 43], ['ZETA', 3760, 38], ['GUAJE', 3412, 29], ['LAURA', 2998, 22],
             ['DAVO', 2570, 16], ['MAXX', 2140, 12], ['PEPU', 1702, 8], ['IRENE', 1288, 5]],
    'c6' => [['ZETA', 4296, 51], ['LAURA', 4180, 46], ['DAVO', 4054, 41], ['NANDO', 3702, 32], ['IRENE', 3240, 24],
             ['PEPU', 2745, 17], ['MAXX', 2290, 12], ['GUAJE', 1810, 8], ['TITO', 1366, 5]],
    'c5' => [['PIXEL', 4122, 49], ['NANDO', 4010, 44], ['LUNA', 3895, 39], ['TXEMA', 3520, 30], ['ROCIO', 3080, 22],
             ['SERGI', 2611, 16], ['ZETA', 2170, 11], ['PACO7', 1730, 8], ['CHUSO', 1302, 5]],
    'c7' => [['LAURA', 4502, 55], ['PIXEL', 4371, 49], ['GUAJE', 4210, 43], ['ROCIO', 3866, 34], ['TXEMA', 3390, 26],
             ['ZETA', 2880, 18], ['KIKO', 2402, 13], ['NANDO', 1904, 9], ['LUNA', 1420, 5]],
    'c8' => [['SERGI', 4688, 58], ['LUNA', 4560, 52], ['DAVO', 4398, 45], ['IRENE', 4012, 36], ['PEPU', 3520, 27],
             ['MAXX', 2990, 19], ['TITO', 2488, 13], ['CHUSO', 1975, 9], ['PACO7', 1470, 5]],
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
    // el relleno solo ocupa huecos libres y nunca supera al mejor real del modo
    $rell = RELLENO[$modo] ?? [];
    if ($rell && count($lista) < 10) {
        $tope = $rell[0][1];
        $escala = ($lista && $lista[0]['p'] <= $tope) ? ($lista[0]['p'] * 0.93) / $tope : 1;
        foreach ($rell as $r) {
            if (count($lista) >= 10) { break; }
            if (isset($vistos[$r[0]])) { continue; }
            $lista[] = ['n' => $r[0], 'p' => max(1, (int)round($r[1] * $escala)), 'f' => max(0, (int)round($r[2] * $escala)), 'd' => '2026-10-20', 'r' => 1];
        }
        usort($lista, function ($a, $b) { return $b['p'] <=> $a['p']; });
    }
    return $lista;
}
// ¿Queda sitio para cualquier jugador real? (hay menos de 10 reales: el relleno se aparta)
function hay_hueco($d) {
    $n = [];
    foreach ($d['top'] as $e) { $n[strtoupper($e['n'])] = true; }
    return count($n) < 10;
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
    foreach ($visibles as $e) { if (!empty($e['r']) && $e['p'] > $mejor['p']) { $delante++; } }
    return ['puntos' => $mejor['p'], 'fichas' => $mejor['f'], 'fecha' => $mejor['d'], 'puesto' => $delante + 1];
}
