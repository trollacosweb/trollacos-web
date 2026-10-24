<?php
/*
 * Trollacos - piezas comunes del arcade y de la Porra.
 * Datos en api/datos/ (protegida). Nunca se guardan IPs: solo un resumen cifrado y temporal.
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

$CABECERA = "<?php exit; ?>\n";   // los ficheros de datos son .php con exit: nadie puede leerlos desde fuera

function responder($datos, $codigo = 200) {
    http_response_code($codigo);
    echo json_encode($datos, JSON_UNESCAPED_UNICODE);
    exit;
}
if (!is_string($SECRETO) || strlen($SECRETO) < 32) { responder(['error' => 'config'], 500); }

function leer_json($f, $vacio) {
    global $CABECERA;
    if (!file_exists($f)) { return $vacio; }
    $j = json_decode(substr(file_get_contents($f), strlen($CABECERA)), true);
    return is_array($j) ? $j + $vacio : $vacio;
}
function guardar_json($f, $d) {
    global $CABECERA;
    file_put_contents($f, $CABECERA . json_encode($d, JSON_UNESCAPED_UNICODE), LOCK_EX);
}
function entrada() {
    $in = json_decode(file_get_contents('php://input'), true);
    if (!is_array($in)) { responder(['error' => 'datos'], 400); }
    return $in;
}
function quien() {   // resumen cifrado de la conexión, no la IP
    global $SECRETO;
    return substr(hash_hmac('sha256', $_SERVER['REMOTE_ADDR'] ?? '', $SECRETO), 0, 16);
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
// Estilo recreativa: una sola palabra de 2 a 5 letras o números, en mayúsculas. Devuelve el nombre limpio o responde con error.
function nombre_o_error($nombre) {
    $nombre = trim(preg_replace('/\s+/u', '', (string)$nombre));
    $nombre = strtoupper(strtr($nombre, ['á'=>'Á','é'=>'É','í'=>'Í','ó'=>'Ó','ú'=>'Ú','ñ'=>'Ñ','ü'=>'Ü']));
    $largo = preg_match_all('/./u', $nombre);
    if ($largo < 2 || $largo > 5 || !preg_match('/^[\p{L}\p{N}]+$/u', $nombre)) {
        responder(['error' => 'formato', 'mensaje' => 'Una sola palabra de 2 a 5 letras o números, sin espacios.'], 400);
    }
    $vetados = @include __DIR__ . '/bloqueados.php';
    if ((is_array($vetados) && in_array($nombre, array_map('strtoupper', $vetados), true)) || !nombre_valido($nombre)) {
        responder(['error' => 'nombre', 'mensaje' => 'Ese nombre no está permitido. Prueba con otro.'], 400);
    }
    return $nombre;
}

/* ---------- partidas firmadas del arcade ---------- */
function ficha_nueva() {
    global $SECRETO;
    $ts = time(); $azar = bin2hex(random_bytes(8));
    return "$ts.$azar." . hash_hmac('sha256', "$ts.$azar", $SECRETO);
}
// Comprueba la ficha de partida y que puntos/fichas sean posibles en ese tiempo. Devuelve el identificador único de la partida.
function partida_valida($ficha, $puntos, $fichas) {
    global $SECRETO;
    $partes = explode('.', (string)$ficha);
    if (count($partes) !== 3 || !hash_equals(hash_hmac('sha256', "$partes[0].$partes[1]", $SECRETO), $partes[2])) {
        responder(['error' => 'ficha', 'mensaje' => 'Partida no válida.'], 400);
    }
    $duracion = time() - (int)$partes[0];
    if ($duracion < 1 || $duracion > 7200) { responder(['error' => 'ficha', 'mensaje' => 'Partida caducada.'], 400); }
    if ($puntos < 0 || $puntos > 1000000 || $fichas < 0 || $fichas > 5 * $duracion + 5
        || ($puntos - $fichas * 10) > 90 * $duracion + 60 || ($puntos - $fichas * 10) < 0) {
        responder(['error' => 'trampa', 'mensaje' => 'Esa puntuación no cuadra. El Trollaco lo ha visto todo.'], 400);
    }
    return $partes[1];
}
