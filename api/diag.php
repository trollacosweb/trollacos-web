<?php
// SMTP: comprueba que se puede entrar con el buzón (no manda nada). Necesita las piezas de comun.php/correo.php.
// Diagnóstico del servidor para el correo (no muestra ningún dato privado). Se puede borrar cuando todo funcione.
require __DIR__ . '/comun.php';
require __DIR__ . '/correo.php';
$df = array_map('trim', explode(',', (string)ini_get('disable_functions')));
// a nombre de quién está el certificado del servidor de correo (sin comprobarlo, solo para leerlo)
function cert_smtp() {
    $ctx = stream_context_create(['ssl' => ['verify_peer' => false, 'verify_peer_name' => false, 'capture_peer_cert' => true]]);   // contexto propio: no toca el de los envíos
    $s = @stream_socket_client('tcp://' . SMTP_HOST . ':' . SMTP_PORT, $en, $es, 15, STREAM_CLIENT_CONNECT, $ctx); if (!$s) { return "sin conexión: $es"; }
    stream_set_timeout($s, 15);
    try { smtp_hablar($s, null, 220); $e = smtp_hablar($s, 'EHLO trollacos.com', 250); if (stripos($e, 'STARTTLS') === false) { return 'no ofrece STARTTLS'; } smtp_hablar($s, 'STARTTLS', 220); }
    catch (Exception $x) { return 'error: ' . $x->getMessage(); }
    if (!@stream_socket_enable_crypto($s, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) { return 'TLS falla incluso sin comprobar'; }
    $c = openssl_x509_parse(stream_context_get_options($s)['ssl']['peer_certificate']);
    return ($c['subject']['CN'] ?? '?') . ' | ' . ($c['extensions']['subjectAltName'] ?? '') . ' | caduca ' . date('Y-m-d', $c['validTo_time_t'] ?? 0);
}
$smtp = smtp_probar();
echo json_encode([
  'cert' => cert_smtp(),
  'php' => PHP_VERSION,
  'mail' => function_exists('mail') && !in_array('mail', $df, true),
  'openssl' => function_exists('openssl_encrypt'),
  'gcm' => function_exists('openssl_get_cipher_methods') && in_array('aes-256-gcm', openssl_get_cipher_methods(), true),
  'mbstring' => function_exists('mb_substr'),
  'sendmail_path' => ini_get('sendmail_path') ? 'si' : 'no',
  'fsockopen' => function_exists('fsockopen') && !in_array('fsockopen', $df, true),
  'smtp' => $smtp,
  'stream_socket_client' => function_exists('stream_socket_client') && !in_array('stream_socket_client', $df, true),
]);
