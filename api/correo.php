<?php
/*
 * Trollacos - emails de las cuentas (opcionales), enlaces mágicos y boletín.
 * - El email se guarda CIFRADO (AES-256-GCM con una clave derivada del secreto del servidor) y una huella HMAC para buscarlo.
 * - Sin contraseñas: para entrar o confirmar el email se manda un enlace de un solo uso que caduca en 30 minutos.
 * - Los correos salen de no-reply@trollacos.com con mail() del propio servidor (no hace falta guardar ninguna contraseña).
 */
const CORREO_DE   = 'no-reply@trollacos.com';
const CORREO_RESP = 'info@trollacos.com';
const WEB         = 'https://trollacos.com';
const TOKEN_MIN   = 30;   // minutos que dura un enlace
// Administradores: huella SHA-256 del email en minúsculas (el email no aparece escrito en el código)
const ADMIN_HUELLAS = ['211ae0b0fbc48f992b063d59e0aafc1521366f89fcda34039da8128b2b4a8fde'];

// Clave de administrador (la misma del arcade): solo su huella. Sirve para recuperar cuentas que han perdido el código.
const ADMIN_CLAVE_HUELLA = 'cd4d9ff772689447fc3dea784b24b0f1acbb65c7e1144dd8cab262328154da61';

function clave_email() { global $SECRETO; return hash_hmac('sha256', 'clave-email', $SECRETO, true); }
function email_normal($e) { return strtolower(trim((string)$e)); }
function email_ok($e) { return strlen($e) <= 120 && filter_var($e, FILTER_VALIDATE_EMAIL) && preg_match('/\.[a-z]{2,}$/', $e); }
function email_huella($e) { global $SECRETO; return hash_hmac('sha256', 'email|' . email_normal($e), $SECRETO); }
function email_cifrar($e) {
    $iv = random_bytes(12); $tag = '';
    $c = openssl_encrypt(email_normal($e), 'aes-256-gcm', clave_email(), OPENSSL_RAW_DATA, $iv, $tag);
    return base64_encode($iv . $tag . $c);
}
function email_descifrar($b) {
    $r = base64_decode((string)$b, true); if ($r === false || strlen($r) < 29) { return null; }
    $p = openssl_decrypt(substr($r, 28), 'aes-256-gcm', clave_email(), OPENSSL_RAW_DATA, substr($r, 0, 12), substr($r, 12, 16));
    return $p === false ? null : $p;
}
function email_tapado($e) {   // jgf•••@gmail.com
    [$u, $dom] = explode('@', $e, 2) + ['', ''];
    return mb_substr($u, 0, min(3, max(1, mb_strlen($u) - 1))) . '•••@' . $dom;
}
function es_admin_email($e) { return $e !== null && in_array(hash('sha256', email_normal($e)), ADMIN_HUELLAS, true); }
function token_baja($e) { global $SECRETO; return substr(hash_hmac('sha256', 'baja|' . email_normal($e), $SECRETO), 0, 32); }

function local() { $h = $_SERVER['HTTP_HOST'] ?? ''; return preg_match('/^(127\.0\.0\.1|localhost)(:\d+)?$/', $h) === 1; }

// Plantilla con el estilo de Trollacos
function correo_html($titulo, $parrafos, $boton_txt = null, $boton_url = null, $pie = '') {
    $ps = implode('', array_map(function ($p) { return '<p style="margin:0 0 14px;font-size:16px;line-height:1.5;color:#e9e6ff">' . $p . '</p>'; }, $parrafos));
    $b = $boton_url ? '<p style="margin:22px 0;text-align:center"><a href="' . htmlspecialchars($boton_url) . '" style="display:inline-block;padding:14px 26px;background:#ff2bd6;color:#ffffff;font-weight:bold;text-decoration:none;border-radius:10px;font-size:17px">' . htmlspecialchars($boton_txt) . '</a></p>' : '';
    return '<!doctype html><html lang="es"><body style="margin:0;background:#07021a;font-family:Arial,Helvetica,sans-serif">'
        . '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#07021a"><tr><td align="center" style="padding:24px 12px">'
        . '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#140830;border:2px solid #ff2bd6;border-radius:14px">'
        . '<tr><td style="padding:22px 24px 6px;text-align:center"><a href="' . WEB . '" style="font-size:28px;font-weight:bold;letter-spacing:3px;color:#1ff2ff;text-decoration:none">TROLLACOS</a></td></tr>'
        . '<tr><td style="padding:10px 24px 20px"><h1 style="margin:0 0 16px;font-size:22px;color:#ffd23f">' . htmlspecialchars($titulo) . '</h1>' . $ps . $b
        . ($pie ? '<p style="margin:18px 0 0;font-size:13px;color:#a59dd0">' . $pie . '</p>' : '') . '</td></tr></table>'
        . '<p style="font-size:12px;color:#6f6894;margin:14px 0 0">Trollacos · trollacos.com · Si tienes dudas escríbenos a ' . CORREO_RESP . '</p>'
        . '</td></tr></table></body></html>';
}

// Envío: mail() si el hosting lo deja; si no (DonDominio lo tiene desactivado), SMTP con el buzón no-reply.
// La contraseña la pone Guillermo como secreto de GitHub (SMTP_PASSWORD) y el despliegue crea api/smtp.php con ella (fuera de git).
const SMTP_HOST = 'smtp.trollacos.com';
const SMTP_PORT = 587;
const SMTP_TLS_NOMBRE = 'smtp.dondominio.com';   // el certificado del servidor de correo es *.dondominio.com: se comprueba contra ese nombre
function smtp_conf() { $c = @include __DIR__ . '/smtp.php'; return (is_array($c) && !empty($c['pass'])) ? $c : null; }
function smtp_hablar($s, $cmd, $espera) {
    if ($cmd !== null) { fwrite($s, $cmd . "\r\n"); }
    $resp = '';
    while (($l = fgets($s, 1024)) !== false) { $resp .= $l; if (strlen($l) < 4 || $l[3] === ' ') { break; } }
    if (!in_array((int)substr($resp, 0, 3), (array)$espera, true)) { throw new Exception(trim(substr($resp, 0, 120)) ?: 'sin respuesta'); }
    return $resp;
}
function smtp_abrir($conf) {
    $ctx = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true, 'peer_name' => SMTP_TLS_NOMBRE, 'allow_self_signed' => false]]);
    $s = @stream_socket_client('tcp://' . SMTP_HOST . ':' . SMTP_PORT, $en, $es, 15, STREAM_CLIENT_CONNECT, $ctx);
    if (!$s) { throw new Exception("conexión: $es"); }
    stream_set_timeout($s, 20);
    smtp_hablar($s, null, 220);
    $ehlo = smtp_hablar($s, 'EHLO trollacos.com', 250);
    if (stripos($ehlo, 'STARTTLS') !== false) {
        smtp_hablar($s, 'STARTTLS', 220);
        if (!@stream_socket_enable_crypto($s, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) { throw new Exception('TLS'); }
        smtp_hablar($s, 'EHLO trollacos.com', 250);
    }
    smtp_hablar($s, 'AUTH LOGIN', 334);
    smtp_hablar($s, base64_encode($conf['user'] ?? CORREO_DE), 334);
    smtp_hablar($s, base64_encode($conf['pass']), 235);
    return $s;
}
function smtp_probar() {   // para el diagnóstico: entra y sale sin mandar nada
    $c = smtp_conf(); if (!$c) { return 'sin contraseña configurada'; }
    try { $s = smtp_abrir($c); smtp_hablar($s, 'QUIT', 221); fclose($s); return 'ok'; } catch (Exception $e) { return 'error: ' . $e->getMessage(); }
}

function enviar_correo($para, $asunto, $html, $texto, $extra_cab = []) {
    if (local()) {   // en pruebas no se manda nada: se apunta en un fichero
        global $DIR;
        file_put_contents("$DIR/correos-prueba.log", date('c') . " PARA $para | $asunto\n$texto\n\n", FILE_APPEND);
        return true;
    }
    $limite = 'b' . bin2hex(random_bytes(8));
    $asuntoC = '=?UTF-8?B?' . base64_encode($asunto) . '?=';
    $cab = ['From: =?UTF-8?B?' . base64_encode('Trollacos') . '?= <' . CORREO_DE . '>', 'Reply-To: ' . CORREO_RESP,
            'MIME-Version: 1.0', 'Content-Type: multipart/alternative; boundary="' . $limite . '"'];
    $cuerpo = "--$limite\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($texto))
            . "--$limite\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($html)) . "--$limite--";
    $df = array_map('trim', explode(',', (string)ini_get('disable_functions')));
    if (function_exists('mail') && !in_array('mail', $df, true)) {
        return @mail($para, $asuntoC, $cuerpo, implode("\r\n", array_merge($cab, $extra_cab)), '-f' . CORREO_DE);
    }
    $conf = smtp_conf(); if (!$conf) { return false; }
    try {
        $s = smtp_abrir($conf);
        smtp_hablar($s, 'MAIL FROM:<' . CORREO_DE . '>', 250);
        smtp_hablar($s, 'RCPT TO:<' . $para . '>', [250, 251]);
        smtp_hablar($s, 'DATA', 354);
        $todo = implode("\r\n", array_merge(['Date: ' . date('r'), 'Message-ID: <' . bin2hex(random_bytes(12)) . '@trollacos.com>', 'To: <' . $para . '>', 'Subject: ' . $asuntoC], $cab, $extra_cab))
              . "\r\n\r\n" . $cuerpo;
        $todo = preg_replace('/\r?\n/', "\r\n", $todo);
        $todo = preg_replace('/^\./m', '..', $todo);
        smtp_hablar($s, $todo . "\r\n.", 250);
        smtp_hablar($s, 'QUIT', 221);
        fclose($s);
        return true;
    } catch (Exception $e) { error_log('SMTP Trollacos: ' . $e->getMessage()); return false; }
}

// Límite de envíos: por conexión (5/hora), por email (3/hora) y en total (150/día). Solo cuentan los que salen de verdad.
function claves_envio($email) { return ['q' . quien(), 'e' . substr(email_huella($email), 0, 16), 'total']; }
function puede_enviar(&$d, $email) {
    $ahora = time(); [$q, $h] = claves_envio($email);
    $env = $d['env'] ?? [];
    foreach ($env as $k => $ts) { $env[$k] = array_values(array_filter($ts, function ($t) use ($ahora) { return $ahora - $t < 86400; })); if (!$env[$k]) { unset($env[$k]); } }
    $hora = function ($k) use ($env, $ahora) { return count(array_filter($env[$k] ?? [], function ($t) use ($ahora) { return $ahora - $t < 3600; })); };
    $d['env'] = $env; unset($d['envios']);
    if ($hora($q) >= 5 || $hora($h) >= 3 || count($env['total'] ?? []) >= 150) { return false; }
    foreach (claves_envio($email) as $k) { $d['env'][$k][] = $ahora; }
    return true;
}
// si el correo no ha salido, se devuelve el intento para no gastar el límite
function devolver_envio($email) {
    global $DIR, $FPORRA, $VACIO;
    $fl = fopen("$DIR/.cerrojo-porra", 'c'); flock($fl, LOCK_EX);
    $d = leer_json($FPORRA, $VACIO);
    foreach (claves_envio($email) as $k) { if (!empty($d['env'][$k])) { array_pop($d['env'][$k]); } }
    guardar_json($FPORRA, $d); flock($fl, LOCK_UN);
}

function token_nuevo(&$d, $tipo, $nombre, $email, $boletin = false) {
    $ahora = time();
    $d['tokens'] = array_filter($d['tokens'] ?? [], function ($t) use ($ahora) { return $t['x'] > $ahora; });
    $tok = bin2hex(random_bytes(24));
    $d['tokens'][hash('sha256', $tok)] = ['t' => $tipo, 'u' => $nombre, 'em' => email_cifrar($email), 'bo' => (bool)$boletin, 'x' => $ahora + TOKEN_MIN * 60];
    return $tok;
}
function cuenta_por_email($d, $email) {
    $h = email_huella($email);
    foreach ($d['usuarios'] as $n => $u) { if (($u['eh'] ?? '') === $h && !empty($u['ev'])) { return $n; } }
    return null;
}

/* ================= BOLETÍN ================= */
// Las últimas noticias propias salen del rss.xml de la web (solo enlaces a trollacos.com)
function noticias_rss($n = 4) {
    $x = @simplexml_load_file(dirname(__DIR__) . '/rss.xml'); $out = [];
    if ($x && isset($x->channel->item)) { foreach ($x->channel->item as $it) { $out[] = ['t' => (string)$it->title, 'u' => (string)$it->link, 'd' => (string)$it->description]; if (count($out) >= $n) { break; } } }
    return $out;
}
function dias_gta() { return max(0, (int)ceil((strtotime('2026-11-19 00:00:00 Europe/Madrid') - time()) / 86400)); }
function asunto_boletin_defecto() { $d = dias_gta(); return $d > 0 ? "Faltan $d días para GTA VI 🌴 Lo último de Trollacos" : 'GTA VI ya está aquí 🌴 Lo último de Trollacos'; }
function intro_boletin_defecto() {
    $d = dias_gta();
    return ($d > 0 ? "Quedan <b>$d días</b> para volver a Vice City y en Trollacos no paramos." : 'GTA VI ya está en la calle y en Trollacos lo estamos destripando.')
        . ' Aquí tienes lo último que hemos contado, la guía más completa en español y un par de retos para matar la espera.';
}
function boletin_html($asunto, $intro, $nombre, $url_baja) {
    $tarjeta = function ($emoji, $tit, $txt, $url, $color) {
        return '<tr><td style="padding:0 0 12px"><a href="' . htmlspecialchars($url) . '" style="display:block;text-decoration:none;border:2px solid ' . $color . ';border-radius:12px;padding:14px 16px;background:#0d0524">'
             . '<span style="font-size:18px;font-weight:bold;color:' . $color . '">' . $emoji . ' ' . htmlspecialchars($tit) . ' ›</span><br><span style="font-size:15px;color:#e9e6ff;line-height:1.4">' . $txt . '</span></a></td></tr>';
    };
    $noti = '';
    foreach (noticias_rss(4) as $n) {
        $noti .= '<tr><td style="padding:0 0 12px"><a href="' . htmlspecialchars($n['u']) . '?utm_source=boletin" style="display:block;text-decoration:none;border-left:4px solid #ff2bd6;padding:6px 0 6px 12px">'
               . '<span style="font-size:17px;font-weight:bold;color:#ffffff;line-height:1.3">' . htmlspecialchars($n['t']) . '</span><br><span style="font-size:14px;color:#a59dd0;line-height:1.4">' . htmlspecialchars($n['d']) . '</span></a></td></tr>';
    }
    $dias = dias_gta();
    $cuerpo = '<p style="margin:0 0 6px;font-size:16px;color:#e9e6ff">¡Hola, <b style="color:#1ff2ff">' . htmlspecialchars($nombre) . '</b>!</p>'
        . '<p style="margin:0 0 18px;font-size:16px;line-height:1.5;color:#e9e6ff">' . $intro . '</p>'
        . ($dias > 0 ? '<p style="margin:0 0 20px;text-align:center"><span style="display:inline-block;padding:10px 18px;border:2px solid #ffd23f;border-radius:10px;font-size:22px;font-weight:bold;color:#ffd23f">🌴 GTA VI · faltan ' . $dias . ' días</span></p>' : '')
        . '<h2 style="margin:0 0 12px;font-size:19px;color:#ffd23f">📰 Lo último, contado por Danna</h2><table role="presentation" width="100%" cellpadding="0" cellspacing="0">' . $noti . '</table>'
        . '<h2 style="margin:10px 0 12px;font-size:19px;color:#ffd23f">🎮 En Trollacos</h2><table role="presentation" width="100%" cellpadding="0" cellspacing="0">'
        . $tarjeta('📖', 'La Guía Trollacos de GTA VI', 'Personajes, mapa, jugabilidad, música… todo lo confirmado, en español.', WEB . '/gta-6/?utm_source=boletin', '#1ff2ff')
        . $tarjeta('📺', 'GTA VI a tope: tele, monitor y consola', 'Qué necesitas para jugarlo en la máxima calidad, sin tirar el dinero.', WEB . '/gta-6/que-comprar/?utm_source=boletin#tele', '#ffd23f')
        . $tarjeta('🕹️', 'Trollaco Run: el modo historia', 'Cinco capítulos para rescatar a la Princesa Neón… y Míster Glitch sigue suelto. ¿Superas el récord?', WEB . '/arcade/?utm_source=boletin', '#ff2bd6')
        . $tarjeta('⚽', 'La Porra Trollaca: LaLiga y Champions', 'Pronostica los partidos con tus fichas y sube en el ranking. Sin dinero real, solo pique.', WEB . '/porra/?utm_source=boletin', '#39ff88')
        . '</table>';
    return '<!doctype html><html lang="es"><body style="margin:0;background:#07021a;font-family:Arial,Helvetica,sans-serif">'
        . '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#07021a"><tr><td align="center" style="padding:24px 12px">'
        . '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;background:#140830;border:2px solid #ff2bd6;border-radius:14px">'
        . '<tr><td style="padding:22px 24px 4px;text-align:center"><a href="' . WEB . '/?utm_source=boletin" style="font-size:30px;font-weight:bold;letter-spacing:3px;color:#1ff2ff;text-decoration:none">TROLLACOS</a><div style="font-size:13px;color:#a59dd0;letter-spacing:2px">EL BOLETÍN</div></td></tr>'
        . '<tr><td style="padding:16px 24px 22px"><h1 style="margin:0 0 14px;font-size:22px;color:#ffffff">' . htmlspecialchars($asunto) . '</h1>' . $cuerpo . '</td></tr></table>'
        . '<p style="font-size:12px;color:#6f6894;margin:14px 0 0;line-height:1.5">Recibes este correo porque te apuntaste al boletín de Trollacos.<br>'
        . '<a href="' . htmlspecialchars($url_baja) . '" style="color:#a59dd0">Darme de baja</a> · ¿Dudas? Escríbenos a ' . CORREO_RESP . '</p>'
        . '</td></tr></table></body></html>';
}
function boletin_texto($asunto, $intro, $nombre, $url_baja) {
    $t = "¡Hola, $nombre!\n\n" . strip_tags($intro) . "\n\nLO ÚLTIMO\n";
    foreach (noticias_rss(4) as $n) { $t .= "- {$n['t']}\n  {$n['u']}\n"; }
    return $t . "\nLa guía de GTA VI: " . WEB . "/gta-6/\nGTA VI a tope (tele, monitor y consola): " . WEB . "/gta-6/que-comprar/#tele\nTrollaco Run: " . WEB . "/arcade/\nLa Porra (LaLiga y Champions): " . WEB . "/porra/\n\nDarte de baja: $url_baja\n";
}
