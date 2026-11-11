<?php
/*
 * Archivos Secretos - «Cuéntanos tu caso»: los lectores mandan sus historias de misterio.
 *   POST {alias?, lugar, anio?, relato, email?, acepto, web}   (web = trampa para bots: tiene que ir vacío)
 * Se guarda en api/datos/casos.php (protegido) y se avisa por correo a info@trollacos.com.
 * Nunca se guarda la IP (solo el resumen cifrado de quien() para el límite de envíos, y se borra a las 24 h).
 * El email, si lo dejan, va cifrado (AES-256-GCM, como en la Porra).
 */
require __DIR__ . '/comun.php';
require __DIR__ . '/correo.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { responder(['error' => 'metodo'], 405); }
$in = entrada();

function texto($s, $max) {
    $s = trim(preg_replace('/[\x00-\x09\x0B-\x1F\x7F]/u', '', (string)$s));
    return mb_substr($s, 0, $max);
}
if (!empty($in['web'])) { responder(['ok' => true]); }   // bot: se le dice que sí y no se guarda nada
$alias  = texto($in['alias'] ?? '', 40);
$lugar  = texto($in['lugar'] ?? '', 100);
$anio   = texto($in['anio'] ?? '', 30);
$relato = texto($in['relato'] ?? '', 4000);
$email  = email_normal($in['email'] ?? '');
if (empty($in['acepto'])) { responder(['error' => 'acepto', 'mensaje' => 'Tienes que marcar la casilla para mandarlo.'], 400); }
if (mb_strlen($lugar) < 2) { responder(['error' => 'lugar', 'mensaje' => 'Dinos dónde pasó (aunque sea el pueblo o la ciudad).'], 400); }
if (mb_strlen($relato) < 80) { responder(['error' => 'relato', 'mensaje' => 'Cuéntanos un poco más: al menos un par de frases.'], 400); }
if ($email !== '' && !email_ok($email)) { responder(['error' => 'email', 'mensaje' => 'Ese email no parece válido. Puedes dejarlo vacío.'], 400); }
if (preg_match_all('~https?://~i', $relato) > 2) { responder(['error' => 'enlaces', 'mensaje' => 'Demasiados enlaces. Cuéntanoslo con tus palabras.'], 400); }

$F = "$DIR/casos.php";
$VAC = ['casos' => [], 'lim' => []];
$fl = fopen("$DIR/.cerrojo-casos", 'c'); flock($fl, LOCK_EX);
$d = leer_json($F, $VAC);
$ahora = time();
foreach ($d['lim'] as $k => $ts) { $d['lim'][$k] = array_values(array_filter($ts, function ($t) use ($ahora) { return $ahora - $t < 86400; })); if (!$d['lim'][$k]) { unset($d['lim'][$k]); } }
$q = 'q' . quien();
if (count($d['lim'][$q] ?? []) >= 3 || count($d['lim']['total'] ?? []) >= 60) {
    flock($fl, LOCK_UN);
    responder(['error' => 'limite', 'mensaje' => 'Has mandado varios casos hoy. El Dr. Aris necesita tiempo para leerlos: vuelve mañana.'], 429);
}
$d['lim'][$q][] = $ahora; $d['lim']['total'][] = $ahora;
$id = date('Ymd-His') . '-' . bin2hex(random_bytes(2));
$d['casos'][] = ['id' => $id, 'fecha' => date('c'), 'alias' => $alias, 'lugar' => $lugar, 'anio' => $anio, 'relato' => $relato,
                 'email' => $email !== '' ? email_cifrar($email) : null, 'consentimiento' => date('c'), 'estado' => 'nuevo'];
guardar_json($F, $d);
flock($fl, LOCK_UN);

// aviso a Guillermo (no cuenta para el límite de correos de la Porra)
$txt = "Nuevo caso para los Archivos Secretos ($id)\n\nAlias: " . ($alias ?: '(sin alias)') . "\nLugar: $lugar\nAño: " . ($anio ?: '(no lo dice)')
     . "\nEmail para contestar: " . ($email ?: '(no lo ha dejado)') . "\n\n$relato\n";
$html = correo_html('Nuevo caso para los Archivos Secretos', [
    '<b>Alias:</b> ' . htmlspecialchars($alias ?: '(sin alias)') . '<br><b>Lugar:</b> ' . htmlspecialchars($lugar) . '<br><b>Año:</b> ' . htmlspecialchars($anio ?: '(no lo dice)')
    . '<br><b>Email para contestar:</b> ' . htmlspecialchars($email ?: '(no lo ha dejado)'),
    nl2br(htmlspecialchars($relato)),
    '<small>Referencia: ' . $id . '. Antes de publicarlo: sin nombres de particulares, direcciones ni nada que identifique a nadie.</small>']);
enviar_correo(CORREO_RESP, '👽 Nuevo caso: ' . mb_substr($lugar, 0, 60), $html, $txt);

responder(['ok' => true, 'id' => $id]);
