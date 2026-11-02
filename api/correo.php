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

function enviar_correo($para, $asunto, $html, $texto, $extra_cab = []) {
    if (local()) {   // en pruebas no se manda nada: se apunta en un fichero
        global $DIR;
        file_put_contents("$DIR/correos-prueba.log", date('c') . " PARA $para | $asunto\n$texto\n\n", FILE_APPEND);
        return true;
    }
    $limite = 'b' . bin2hex(random_bytes(8));
    $cab = ['From: =?UTF-8?B?' . base64_encode('Trollacos') . '?= <' . CORREO_DE . '>', 'Reply-To: ' . CORREO_RESP,
            'MIME-Version: 1.0', 'Content-Type: multipart/alternative; boundary="' . $limite . '"'];
    $cuerpo = "--$limite\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($texto))
            . "--$limite\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($html)) . "--$limite--";
    return @mail($para, '=?UTF-8?B?' . base64_encode($asunto) . '?=', $cuerpo, implode("\r\n", array_merge($cab, $extra_cab)), '-f' . CORREO_DE);
}

// Límite de envíos: por conexión (5/hora), por email (3/hora) y en total (150/día)
function puede_enviar(&$d, $email) {
    $ahora = time(); $q = 'q' . quien(); $h = 'e' . substr(email_huella($email), 0, 16);
    $env = $d['envios'] ?? [];
    foreach ($env as $k => $ts) { $env[$k] = array_values(array_filter($ts, function ($t) use ($ahora) { return $ahora - $t < 86400; })); if (!$env[$k]) { unset($env[$k]); } }
    $hora = function ($k) use ($env, $ahora) { return count(array_filter($env[$k] ?? [], function ($t) use ($ahora) { return $ahora - $t < 3600; })); };
    $total = count($env['total'] ?? []);
    $d['envios'] = $env;
    if ($hora($q) >= 5 || $hora($h) >= 3 || $total >= 150) { return false; }
    $d['envios'][$q][] = $ahora; $d['envios'][$h][] = $ahora; $d['envios']['total'][] = $ahora;
    return true;
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
