<?php
// SMTP: comprueba que se puede entrar con el buzón (no manda nada). Necesita las piezas de comun.php/correo.php.
// Diagnóstico del servidor para el correo (no muestra ningún dato privado). Se puede borrar cuando todo funcione.
require __DIR__ . '/comun.php';
require __DIR__ . '/correo.php';
$df = array_map('trim', explode(',', (string)ini_get('disable_functions')));
echo json_encode([
  'php' => PHP_VERSION,
  'mail' => function_exists('mail') && !in_array('mail', $df, true),
  'openssl' => function_exists('openssl_encrypt'),
  'gcm' => function_exists('openssl_get_cipher_methods') && in_array('aes-256-gcm', openssl_get_cipher_methods(), true),
  'mbstring' => function_exists('mb_substr'),
  'sendmail_path' => ini_get('sendmail_path') ? 'si' : 'no',
  'fsockopen' => function_exists('fsockopen') && !in_array('fsockopen', $df, true),
  'smtp' => smtp_probar(),
  'stream_socket_client' => function_exists('stream_socket_client') && !in_array('stream_socket_client', $df, true),
]);
