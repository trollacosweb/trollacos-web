<?php
/*
 * Trollaco Run - marcador global.
 *   GET  ?accion=lista     -> los 10 mejores
 *   GET  ?accion=empezar   -> ficha firmada para la partida que empieza
 *   POST ?accion=enviar    -> {nombre, puntos, fichas, ficha}
 * Los datos se guardan en api/datos/ (protegida). No se guardan IPs: solo un
 * resumen cifrado y temporal para limitar envíos seguidos.
 */
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

$DIR = __DIR__ . '/datos';
if (!is_dir($DIR)) { @mkdir($DIR, 0750, true); }
if (!file_exists("$DIR/.htaccess")) { @file_put_contents("$DIR/.htaccess", "Require all denied\nDeny from all\n"); }
if (!file_exists("$DIR/index.html")) { @file_put_contents("$DIR/index.html", ''); }

$fsec = "$DIR/secreto.php";
if (!file_exists($fsec)) { @file_put_contents($fsec, "<?php return '" . bin2hex(random_bytes(32)) . "';\n"); }
$SECRETO = @include $fsec;
if (!is_string($SECRETO) || strlen($SECRETO) < 32) { responder(['error' => 'config'], 500); }

$FDATOS = "$DIR/marcadores.php";   // .php con exit al principio: nadie puede leerlo desde fuera
$CABECERA = "<?php exit; ?>\n";

function responder($datos, $codigo = 200) {
    http_response_code($codigo);
    echo json_encode($datos, JSON_UNESCAPED_UNICODE);
    exit;
}

function leer($f, $cab) {
    if (!file_exists($f)) { return ['top' => [], 'usadas' => [], 'ips' => []]; }
    $t = file_get_contents($f);
    $j = json_decode(substr($t, strlen($cab)), true);
    return is_array($j) ? $j + ['top' => [], 'usadas' => [], 'ips' => []] : ['top' => [], 'usadas' => [], 'ips' => []];
}

function top10($d) {
    return array_map(function ($e) { return ['nombre' => $e['n'], 'puntos' => $e['p'], 'fichas' => $e['f'], 'fecha' => $e['d']]; },
        array_slice($d['top'], 0, 10));
}

/* ---------- filtro de nombres ---------- */
function normalizar($s) {
    $s = strtolower(strtr($s, [
        'Á'=>'a','À'=>'a','Ä'=>'a','Â'=>'a','á'=>'a','à'=>'a','ä'=>'a','â'=>'a',
        'É'=>'e','È'=>'e','Ë'=>'e','Ê'=>'e','é'=>'e','è'=>'e','ë'=>'e','ê'=>'e',
        'Í'=>'i','Ì'=>'i','Ï'=>'i','Î'=>'i','í'=>'i','ì'=>'i','ï'=>'i','î'=>'i',
        'Ó'=>'o','Ò'=>'o','Ö'=>'o','Ô'=>'o','ó'=>'o','ò'=>'o','ö'=>'o','ô'=>'o',
        'Ú'=>'u','Ù'=>'u','Ü'=>'u','Û'=>'u','ú'=>'u','ù'=>'u','ü'=>'u','û'=>'u',
        'Ñ'=>'n','ñ'=>'n','Ç'=>'c','ç'=>'c']));
    $s = strtr($s, ['0'=>'o','1'=>'i','3'=>'e','4'=>'a','5'=>'s','7'=>'t','8'=>'b','9'=>'g','@'=>'a','$'=>'s','!'=>'i','|'=>'i','€'=>'e']);
    return preg_replace('/[^a-z]/', '', $s);
}
function colapsar($s, $max) {   // "puuutaa" -> "puta" (max 1) o "puutaa" (max 2)
    return preg_replace('/(.)\1{' . $max . ',}/', str_repeat('$1', $max), $s);
}

function nombre_valido($n) {
    // Palabras que no pueden aparecer en ningún sitio del nombre
    $prohibidas = [
        'puta','puto','putit','zorra','guarra','cabron','cabrona','gilipoll','imbecil','subnormal','retrasad','mongol',
        'maricon','zorr','bollera','travelo','sudaca','panchit','moromier','negrat','gitanoasq','polla',
        'chocho','follar','follad','folla','mamada','corrida','culo','ojete','mierda','cagar','joder','jodid','hostia',
        'malparid','hijoput','hdp','gonorrea','pendej','verga','chinga','perra','idiota','tonto','tonta','capullo',
        'mamon','pajer','violad','violar','nazi','hitler','terroris','pedofil','pederast',
        'fuck','shit','bitch','cunt','dick','cock','pussy','whore','slut','nigg','fag','retard','porn','sex',
        'admin','moderador','trollacos','rockstar'
    ];
    // Palabras cortas que solo se bloquean si son el nombre entero (para no pillar nombres normales)
    $exactas = ['ano','ass','gay','teta','tetas','nabo','cipote','facha','moro','negro','chino','gordo','gorda',
        'pene','cono','paja','marica','rape','eta','kkk','puta','puto'];
    $base = normalizar($n);
    if ($base === '') { return false; }
    $n1 = colapsar($base, 1); $n2 = colapsar($base, 2);
    foreach ($prohibidas as $p) {
        $pn = normalizar($p);
        if ($pn === '') { continue; }
        $doble = (bool)preg_match('/(.)\1/', $pn);
        // si la palabra lleva letras dobles (polla, zorra) se compara sin quitarlas, para no bloquear "Polanco"
        if ($doble ? strpos($n2, $pn) !== false : strpos($n1, $pn) !== false) { return false; }
    }
    foreach ($exactas as $p) { if ($n1 === colapsar(normalizar($p), 1)) { return false; } }
    return true;
}

/* ---------- peticiones ---------- */
$accion = $_GET['accion'] ?? '';

if ($accion === 'lista') {
    responder(['top' => top10(leer($FDATOS, $CABECERA))]);
}

if ($accion === 'empezar') {
    $ts = time();
    $azar = bin2hex(random_bytes(8));
    responder(['ficha' => "$ts.$azar." . hash_hmac('sha256', "$ts.$azar", $SECRETO)]);
}

if ($accion === 'enviar' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $in = json_decode(file_get_contents('php://input'), true);
    if (!is_array($in)) { responder(['error' => 'datos'], 400); }
    $nombre = trim(preg_replace('/\s+/u', ' ', (string)($in['nombre'] ?? '')));
    $puntos = (int)($in['puntos'] ?? 0);
    $fichas = (int)($in['fichas'] ?? 0);
    $ficha  = (string)($in['ficha'] ?? '');

    // Formato del nombre: 2-14 caracteres, letras, números, espacio, punto, guion y guion bajo
    $largo = preg_match_all('/./u', $nombre);
    if ($largo < 2 || $largo > 14 || !preg_match('/^[\p{L}\p{N} ._-]+$/u', $nombre)) {
        responder(['error' => 'formato', 'mensaje' => 'El nombre debe tener entre 2 y 14 letras o números.'], 400);
    }
    if (!nombre_valido($nombre)) {
        responder(['error' => 'nombre', 'mensaje' => 'Ese nombre no está permitido. Prueba con otro.'], 400);
    }

    // Ficha firmada de la partida
    $partes = explode('.', $ficha);
    if (count($partes) !== 3 || !hash_equals(hash_hmac('sha256', "$partes[0].$partes[1]", $SECRETO), $partes[2])) {
        responder(['error' => 'ficha', 'mensaje' => 'Partida no válida.'], 400);
    }
    $duracion = time() - (int)$partes[0];
    if ($duracion < 1 || $duracion > 7200) { responder(['error' => 'ficha', 'mensaje' => 'Partida caducada.'], 400); }

    // ¿Es posible esa puntuación en ese tiempo? (velocidad máxima del juego + margen)
    if ($puntos < 1 || $puntos > 1000000 || $fichas < 0 || $fichas > 5 * $duracion + 5
        || ($puntos - $fichas * 10) > 90 * $duracion + 60 || ($puntos - $fichas * 10) < 0) {
        responder(['error' => 'trampa', 'mensaje' => 'Esa puntuación no cuadra. El Trollaco lo ha visto todo.'], 400);
    }

    $fl = fopen("$DIR/.cerrojo", 'c');
    flock($fl, LOCK_EX);
    $d = leer($FDATOS, $CABECERA);
    $ahora = time();

    // Ficha de un solo uso
    if (in_array($partes[1], $d['usadas'], true)) { flock($fl, LOCK_UN); responder(['error' => 'ficha', 'mensaje' => 'Esa partida ya se guardó.'], 400); }
    $d['usadas'][] = $partes[1];
    $d['usadas'] = array_slice($d['usadas'], -2000);

    // Un envío cada 10 segundos por conexión (se guarda un resumen cifrado, nunca la IP)
    $quien = substr(hash_hmac('sha256', $_SERVER['REMOTE_ADDR'] ?? '', $SECRETO), 0, 16);
    foreach ($d['ips'] as $k => $t) { if ($ahora - $t > 3600) { unset($d['ips'][$k]); } }
    if (isset($d['ips'][$quien]) && $ahora - $d['ips'][$quien] < 10) {
        flock($fl, LOCK_UN); responder(['error' => 'rapido', 'mensaje' => 'Espera unos segundos.'], 429);
    }
    $d['ips'][$quien] = $ahora;

    $d['top'][] = ['n' => $nombre, 'p' => $puntos, 'f' => $fichas, 'd' => date('Y-m-d')];
    usort($d['top'], function ($a, $b) { return $b['p'] <=> $a['p']; });
    $d['top'] = array_slice($d['top'], 0, 100);

    file_put_contents($FDATOS, $CABECERA . json_encode($d, JSON_UNESCAPED_UNICODE), LOCK_EX);
    flock($fl, LOCK_UN);

    $pos = 0;
    foreach ($d['top'] as $i => $e) { if ($e['n'] === $nombre && $e['p'] === $puntos) { $pos = $i + 1; break; } }
    responder(['ok' => true, 'puesto' => $pos, 'top' => top10($d)]);
}

responder(['error' => 'accion'], 400);
