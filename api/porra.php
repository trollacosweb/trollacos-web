<?php
/*
 * La Porra Trollaca - pronósticos de LaLiga con fichas del arcade. SIN DINERO REAL:
 * las fichas no se compran ni se canjean por nada.
 *
 *   POST ?accion=registrar  {nombre}                      -> crea cuenta y devuelve su código secreto
 *   POST ?accion=yo         {nombre, codigo}              -> fichas, pronósticos y movimientos
 *   POST ?accion=apostar    {nombre, codigo, partido, tipo: "1x2"|"exacto", seleccion, cantidad}
 *   POST ?accion=arcade     {nombre, codigo, ficha, puntos, fichas}  -> suma las fichas de una partida
 *   POST ?accion=cancelar   {nombre, codigo, id}          -> anula un pronóstico pendiente y devuelve las fichas
 *   POST ?accion=perfil     {nombre, codigo}              -> todas las estadísticas del jugador (cuenta)
 *   GET  ?accion=ranking                                  -> los 10 con más fichas
 *   GET  ?accion=partidos                                 -> jornada con cuotas (lee partidos.json)
 *   Email (opcional, sin contraseñas, ver correo.php):
 *   POST ?accion=email_vincular {nombre, codigo, email, boletin, edad14} -> manda enlace para confirmar el email
 *   POST ?accion=email_entrar   {email}                    -> manda enlace para entrar en otro dispositivo
 *   POST ?accion=email_token    {token}                    -> usa un enlace (confirma email o entra)
 *   POST ?accion=email_quitar   {nombre, codigo}           -> borra el email de la cuenta
 *   POST ?accion=boletin        {nombre, codigo, si}       -> apuntarse o borrarse del boletín
 *   POST ?accion=baja           {u, t}                     -> baja del boletín desde el enlace del correo
 *   POST ?accion=registrar      {nombre, email?, edad14?, boletin?} -> con email, le llegan el código y el enlace de confirmación
 *   POST ?accion=admin_recuperar {clave, cuenta}           -> código nuevo para una cuenta perdida (solo administrador)
 */
require __DIR__ . '/comun.php';
require __DIR__ . '/arcade_lib.php';
require __DIR__ . '/correo.php';

const BONO_BIENVENIDA = 10;   // fichas al crear la cuenta
const BONO_JORNADA    = 10;   // fichas por participar en cada jornada (al hacer el primer pronóstico)
const CUOTA_EXACTO    = 8.0;  // el resultado exacto paga x8
const CIERRE_SEG      = 300;  // no se admiten pronósticos 5 minutos antes del partido

$FPORRA = "$DIR/porra.php";
$FPARTIDOS = __DIR__ . '/partidos.json';
$VACIO = ['usuarios' => [], 'apuestas' => [], 'arcade' => [], 'fallos' => [], 'altas' => [], 'tokens' => [], 'envios' => []];

function partidos() {
    global $FPARTIDOS;
    $j = @json_decode(@file_get_contents($FPARTIDOS), true);
    return is_array($j) ? $j : ['partidos' => [], 'jornada' => null, 'actualizado' => null];
}
function partido_por_id($pp, $id) {
    foreach ($pp['partidos'] as $p) { if ((string)$p['id'] === (string)$id) { return $p; } }
    return null;
}
function hash_codigo($nombre, $codigo) {
    global $SECRETO;
    return hash_hmac('sha256', $nombre . '|' . strtoupper(trim($codigo)), $SECRETO);
}
function codigo_nuevo() {
    $abc = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
    $c = '';
    for ($i = 0; $i < 8; $i++) { $c .= $abc[random_int(0, strlen($abc) - 1)]; }
    return $c;
}

// Abre los datos con cerrojo, liquida lo que haya terminado y devuelve [datos, cerrojo]
function abrir() {
    global $DIR, $FPORRA, $VACIO;
    $fl = fopen("$DIR/.cerrojo-porra", 'c');
    flock($fl, LOCK_EX);
    $d = leer_json($FPORRA, $VACIO);
    liquidar($d);
    return [$d, $fl];
}
function cerrar($d, $fl, $guardar = true) {
    global $FPORRA;
    if ($guardar) { guardar_json($FPORRA, $d); }
    flock($fl, LOCK_UN);
}

// Reparte fichas de los pronósticos cuyo partido ya ha terminado (o devuelve si se suspendió)
function liquidar(&$d) {
    $pp = partidos();
    foreach ($d['apuestas'] as &$a) {
        if ($a['e'] !== 'pendiente') { continue; }
        $p = partido_por_id($pp, $a['p']);
        if (!$p) { continue; }
        $u = &$d['usuarios'][$a['u']];
        if ($p['estado'] === 'FINISHED' && $p['gl'] !== null && $p['gv'] !== null) {
            $res = $p['gl'] > $p['gv'] ? '1' : ($p['gl'] < $p['gv'] ? '2' : 'X');
            $gana = $a['t'] === '1x2' ? ($a['s'] === $res) : ($a['s'] === $p['gl'] . '-' . $p['gv']);
            if ($gana) {
                $a['e'] = 'ganada'; $a['g'] = (int)floor($a['c'] * $a['q']);
                $u['f'] += $a['g']; $u['ac'] = ($u['ac'] ?? 0) + 1;
            } else { $a['e'] = 'perdida'; $a['g'] = 0; }
        } elseif (in_array($p['estado'], ['POSTPONED', 'CANCELLED', 'SUSPENDED', 'AWARDED'], true)
                  && time() > strtotime($p['fecha']) + 3 * 86400) {
            $a['e'] = 'devuelta'; $a['g'] = $a['c']; $u['f'] += $a['c'];
        }
        unset($u);
    }
    unset($a);
}

// Comprueba nombre y código. Limita los intentos fallidos por conexión.
function usuario(&$d, $in) {
    $nombre = strtoupper(strtr(preg_replace('/\s+/u', '', (string)($in['nombre'] ?? '')), ['á'=>'Á','é'=>'É','í'=>'Í','ó'=>'Ó','ú'=>'Ú','ñ'=>'Ñ','ü'=>'Ü']));
    $codigo = (string)($in['codigo'] ?? '');
    $q = quien(); $ahora = time();
    $d['fallos'][$q] = array_values(array_filter($d['fallos'][$q] ?? [], function ($t) use ($ahora) { return $ahora - $t < 3600; }));
    if (count($d['fallos'][$q]) >= 10) { return [null, 'Demasiados intentos. Prueba dentro de un rato.']; }
    $u = $d['usuarios'][$nombre] ?? null;
    $hc = $u ? hash_codigo($nombre, $codigo) : '';
    $vale = $u && (hash_equals($u['h'], $hc) || in_array($hc, $u['hx'] ?? [], true));   // hx: códigos de otros dispositivos (entrada por email)
    if (!$vale) {
        $d['fallos'][$q][] = $ahora;
        return [null, 'Nombre o código incorrectos.'];
    }
    return [$nombre, null];
}

function resumen($d, $nombre) {
    $u = $d['usuarios'][$nombre];
    $mias = array_values(array_filter($d['apuestas'], function ($a) use ($nombre) { return $a['u'] === $nombre; }));
    usort($mias, function ($a, $b) { return $b['ts'] <=> $a['ts']; });
    $mias = array_map(function ($a) { return ['id' => $a['id'], 'partido' => $a['p'], 'jornada' => $a['j'], 'tipo' => $a['t'], 'seleccion' => $a['s'],
        'cantidad' => $a['c'], 'cuota' => $a['q'], 'estado' => $a['e'], 'premio' => $a['g'] ?? 0]; }, array_slice($mias, 0, 40));
    $em = !empty($u['ev']) ? email_descifrar($u['em'] ?? '') : null;
    return ['nombre' => $nombre, 'fichas' => $u['f'], 'aciertos' => $u['ac'] ?? 0, 'jornadas' => $u['jb'] ?? [], 'capitulos' => $u['caps'] ?? 0, 'pronosticos' => $mias,
            'email' => $em ? email_tapado($em) : null, 'boletin' => !empty($u['bo']), 'admin' => es_admin_email($em)];
}

$accion = $_GET['accion'] ?? '';
$post = $_SERVER['REQUEST_METHOD'] === 'POST';

if ($accion === 'partidos') {
    responder(partidos());
}

if ($accion === 'ranking') {
    [$d, $fl] = abrir();
    cerrar($d, $fl);
    $us = array_values($d['usuarios']);
    usort($us, function ($a, $b) { return $b['f'] <=> $a['f']; });
    responder(['top' => array_map(function ($u) { return ['nombre' => $u['n'], 'fichas' => $u['f'], 'aciertos' => $u['ac'] ?? 0]; }, array_slice($us, 0, 10)),
               'jugadores' => count($us)]);
}

if ($accion === 'registrar' && $post) {
    $in = entrada();
    $nombre = nombre_o_error($in['nombre'] ?? '');
    [$d, $fl] = abrir();
    $q = quien(); $ahora = time();
    // como mucho 3 cuentas nuevas por conexión y día
    $d['altas'][$q] = array_values(array_filter($d['altas'][$q] ?? [], function ($t) use ($ahora) { return $ahora - $t < 86400; }));
    if (count($d['altas'][$q]) >= 3) { cerrar($d, $fl); responder(['error' => 'rapido', 'mensaje' => 'Ya has creado varias cuentas hoy. Vuelve mañana.'], 429); }
    if (isset($d['usuarios'][$nombre])) { cerrar($d, $fl, false); responder(['error' => 'ocupado', 'mensaje' => 'Ese nombre ya está cogido. Prueba con otro.'], 400); }
    // email opcional: si viene, se le manda el código y el enlace para confirmarlo
    $email = email_normal($in['email'] ?? '');
    if ($email !== '') {
        if (!email_ok($email)) { cerrar($d, $fl, false); responder(['error' => 'email', 'mensaje' => 'Ese email no parece válido.'], 400); }
        if (empty($in['edad14'])) { cerrar($d, $fl, false); responder(['error' => 'edad', 'mensaje' => 'Para usar email tienes que tener 14 años o más. Si no, crea la cuenta sin email.'], 400); }
        if (cuenta_por_email($d, $email)) { cerrar($d, $fl, false); responder(['error' => 'ocupado', 'mensaje' => 'Ese email ya tiene cuenta. Entra con él en la pestaña «CON MI EMAIL».'], 400); }
    }
    $codigo = codigo_nuevo();
    $d['usuarios'][$nombre] = ['n' => $nombre, 'h' => hash_codigo($nombre, $codigo), 'f' => BONO_BIENVENIDA, 'c' => $ahora, 'jb' => [], 'ac' => 0];
    $d['altas'][$q][] = $ahora;
    $enviado = false;
    if ($email !== '' && puede_enviar($d, $email)) {
        $tok = token_nuevo($d, 'v', $nombre, $email, !empty($in['boletin']));
        $enviado = true;
    }
    cerrar($d, $fl);
    if ($enviado) {
        $url = WEB . '/cuenta/?t=' . $tok;
        $enviado = enviar_correo($email, 'Bienvenido a Trollacos, ' . $nombre,
            correo_html('¡Bienvenido a Trollacos, ' . $nombre . '!', [
                'Ya tienes cuenta para el arcade, el modo historia y La Porra Trollaca. Guarda este correo: aquí tienes tus datos.',
                'Nombre de jugador: <b style="color:#1ff2ff;font-size:20px">' . $nombre . '</b><br>Código secreto: <b style="color:#ffd23f;font-size:22px;letter-spacing:3px">' . $codigo . '</b>',
                'Pulsa el botón para confirmar tu email. Así podrás entrar desde cualquier móvil u ordenador sin acordarte del código.'],
                'CONFIRMAR MI EMAIL', $url, 'El botón caduca en ' . TOKEN_MIN . ' minutos (el código no caduca). Si no has creado tú esta cuenta, ignora este correo.'),
            "¡Bienvenido a Trollacos, $nombre!\n\nNombre de jugador: $nombre\nCódigo secreto: $codigo\n\nConfirma tu email aquí (caduca en " . TOKEN_MIN . " minutos):\n$url\n\nSi no has creado tú esta cuenta, ignora este correo.");
        if (!$enviado) { devolver_envio($email); }
    }
    responder(['ok' => true, 'nombre' => $nombre, 'codigo' => $codigo, 'fichas' => BONO_BIENVENIDA, 'email_enviado' => $enviado]);
}

if ($accion === 'yo' && $post) {
    $in = entrada();
    [$d, $fl] = abrir();
    [$nombre, $err] = usuario($d, $in);
    cerrar($d, $fl);
    if (!$nombre) { responder(['error' => 'login', 'mensaje' => $err], 401); }
    responder(['ok' => true] + resumen($d, $nombre));
}

if ($accion === 'arcade' && $post) {
    $in = entrada();
    $puntos = (int)($in['puntos'] ?? 0); $fichas = (int)($in['fichas'] ?? 0);
    $id = partida_valida($in['ficha'] ?? '', $puntos, $fichas);
    [$d, $fl] = abrir();
    [$nombre, $err] = usuario($d, $in);
    if (!$nombre) { cerrar($d, $fl); responder(['error' => 'login', 'mensaje' => $err], 401); }
    if (in_array($id, $d['arcade'], true)) { cerrar($d, $fl, false); responder(['error' => 'ficha', 'mensaje' => 'Esas fichas ya se sumaron.'], 400); }
    $d['arcade'][] = $id; $d['arcade'] = array_slice($d['arcade'], -5000);
    $u = &$d['usuarios'][$nombre];
    $u['f'] += $fichas;
    // estadísticas para la cuenta
    $m = (string)($in['modo'] ?? 'run'); if (!isset($MODOS[$m])) { $m = 'run'; }
    $u['pa'] = ($u['pa'] ?? 0) + 1; $u['fa'] = ($u['fa'] ?? 0) + $fichas;
    $u['pm'][$m] = ($u['pm'][$m] ?? 0) + 1;
    $dur = time() - (int)explode('.', (string)$in['ficha'])[0];
    if (!empty($in['gana']) && preg_match('/^c([1-5])$/', $m, $mm) && $dur >= 35) { $u['caps'] = max($u['caps'] ?? 0, (int)$mm[1]); }
    unset($u);
    cerrar($d, $fl);
    responder(['ok' => true, 'sumadas' => $fichas, 'fichas' => $d['usuarios'][$nombre]['f'], 'capitulos' => $d['usuarios'][$nombre]['caps'] ?? 0]);
}

if ($accion === 'perfil' && $post) {
    $in = entrada();
    [$d, $fl] = abrir();
    [$nombre, $err] = usuario($d, $in);
    cerrar($d, $fl);
    if (!$nombre) { responder(['error' => 'login', 'mensaje' => $err], 401); }
    $u = $d['usuarios'][$nombre];
    $st = ['total' => 0, 'ganada' => 0, 'perdida' => 0, 'pendiente' => 0, 'devuelta' => 0, 'apostadas' => 0, 'mayor' => 0, 'exactos' => 0];
    foreach ($d['apuestas'] as $a) {
        if ($a['u'] !== $nombre) { continue; }
        $st['total']++; $st[$a['e']] = ($st[$a['e']] ?? 0) + 1; $st['apostadas'] += $a['c'];
        if ($a['e'] === 'ganada') { $st['mayor'] = max($st['mayor'], $a['g'] ?? 0); if ($a['t'] === 'exacto') { $st['exactos']++; } }
    }
    // puesto en el ranking de fichas
    $puestoF = 1; foreach ($d['usuarios'] as $o) { if ($o['f'] > $u['f']) { $puestoF++; } }
    $arcade = [];
    foreach ($MODOS as $m => $f) { $arcade[$m] = marca_jugador($m, $nombre); }
    responder(['ok' => true] + resumen($d, $nombre) + [
        'alta' => date('Y-m-d', $u['c'] ?? time()), 'puesto_fichas' => $puestoF, 'jugadores' => count($d['usuarios']),
        'porra' => $st, 'partidas' => $u['pa'] ?? 0, 'fichas_arcade' => $u['fa'] ?? 0, 'partidas_modo' => $u['pm'] ?? (object)[],
        'arcade' => $arcade,
    ] + (es_admin_email(!empty($u['ev']) ? email_descifrar($u['em'] ?? '') : null) ? ['panel' => [
        'usuarios' => count($d['usuarios']),
        'con_email' => count(array_filter($d['usuarios'], function ($x) { return !empty($x['ev']); })),
        'boletin' => count(array_filter($d['usuarios'], function ($x) { return !empty($x['ev']) && !empty($x['bo']); })),
        'pronosticos' => count($d['apuestas']),
        'partidas' => array_sum(array_map(function ($x) { return $x['pa'] ?? 0; }, $d['usuarios'])),
        'altas_7d' => count(array_filter($d['usuarios'], function ($x) { return ($x['c'] ?? 0) > time() - 7 * 86400; })),
    ]] : []));
}

// Recuperar una cuenta que ha perdido el código (solo el administrador, con su clave)
if ($accion === 'admin_recuperar' && $post) {
    $in = entrada();
    [$d, $fl] = abrir();
    $q = quien(); $ahora = time();
    $d['fallos'][$q] = array_values(array_filter($d['fallos'][$q] ?? [], function ($t) use ($ahora) { return $ahora - $t < 3600; }));
    if (count($d['fallos'][$q]) >= 10) { cerrar($d, $fl); responder(['error' => 'rapido', 'mensaje' => 'Demasiados intentos. Prueba dentro de un rato.'], 429); }
    if (!hash_equals(ADMIN_CLAVE_HUELLA, hash('sha256', strtoupper(trim((string)($in['clave'] ?? '')))))) {
        $d['fallos'][$q][] = $ahora; cerrar($d, $fl); responder(['error' => 'clave', 'mensaje' => 'Clave de administrador incorrecta.'], 401);
    }
    $nombre = strtoupper(trim((string)($in['cuenta'] ?? '')));
    if (!isset($d['usuarios'][$nombre])) { cerrar($d, $fl, false); responder(['error' => 'cuenta', 'mensaje' => 'No existe ninguna cuenta con ese nombre.'], 404); }
    $codigo = codigo_nuevo();
    $d['usuarios'][$nombre]['hx'] = array_slice(array_merge($d['usuarios'][$nombre]['hx'] ?? [], [hash_codigo($nombre, $codigo)]), -8);
    cerrar($d, $fl);
    responder(['ok' => true, 'nombre' => $nombre, 'codigo' => $codigo]);
}

/* ================= EMAIL (opcional) ================= */
if ($accion === 'email_vincular' && $post) {
    $in = entrada();
    $email = email_normal($in['email'] ?? '');
    if (!email_ok($email)) { responder(['error' => 'email', 'mensaje' => 'Ese email no parece válido.'], 400); }
    if (empty($in['edad14'])) { responder(['error' => 'edad', 'mensaje' => 'Para añadir un email tienes que tener 14 años o más.'], 400); }
    [$d, $fl] = abrir();
    [$nombre, $err] = usuario($d, $in);
    if (!$nombre) { cerrar($d, $fl); responder(['error' => 'login', 'mensaje' => $err], 401); }
    $otra = cuenta_por_email($d, $email);
    if ($otra && $otra !== $nombre) { cerrar($d, $fl, false); responder(['error' => 'ocupado', 'mensaje' => 'Ese email ya está en otra cuenta. Entra con él desde «¿Perdiste tu código?».'], 400); }
    if (!puede_enviar($d, $email)) { cerrar($d, $fl); responder(['error' => 'rapido', 'mensaje' => 'Has pedido demasiados correos. Prueba dentro de un rato.'], 429); }
    $tok = token_nuevo($d, 'v', $nombre, $email, !empty($in['boletin']));
    cerrar($d, $fl);
    $url = WEB . '/cuenta/?t=' . $tok;
    $ok = enviar_correo($email, 'Confirma tu email en Trollacos',
        correo_html('¡Hola, ' . $nombre . '!', ['Has pedido añadir este email a tu cuenta de Trollacos. Pulsa el botón para confirmarlo.',
            'Con tu email podrás entrar desde cualquier móvil u ordenador sin acordarte del código.'], 'CONFIRMAR MI EMAIL', $url,
            'El enlace caduca en ' . TOKEN_MIN . ' minutos y solo sirve una vez. Si no has sido tú, ignora este correo y no pasará nada.'),
        "¡Hola, $nombre!\n\nPara confirmar tu email en Trollacos abre este enlace:\n$url\n\nCaduca en " . TOKEN_MIN . " minutos. Si no has sido tú, ignora este correo.");
    if (!$ok) { devolver_envio($email); responder(['error' => 'envio', 'mensaje' => 'No hemos podido mandar el correo. Prueba más tarde.'], 500); }
    responder(['ok' => true, 'mensaje' => 'Te hemos mandado un correo a ' . email_tapado($email) . '. Pulsa el enlace para confirmarlo (mira también en spam).']);
}

if ($accion === 'email_entrar' && $post) {
    $in = entrada();
    $email = email_normal($in['email'] ?? '');
    if (!email_ok($email)) { responder(['error' => 'email', 'mensaje' => 'Ese email no parece válido.'], 400); }
    [$d, $fl] = abrir();
    $nombre = cuenta_por_email($d, $email);
    $enviar = $nombre && puede_enviar($d, $email);
    $tok = $enviar ? token_nuevo($d, 'e', $nombre, $email) : null;
    cerrar($d, $fl);
    if ($tok) {
        $url = WEB . '/cuenta/?t=' . $tok;
        $ok = enviar_correo($email, 'Tu enlace para entrar en Trollacos',
            correo_html('Entra en tu cuenta, ' . $nombre, ['Pulsa el botón y entrarás en tu cuenta de Trollacos en este dispositivo.'], 'ENTRAR EN TROLLACOS', $url,
                'El enlace caduca en ' . TOKEN_MIN . ' minutos y solo sirve una vez. Si no lo has pedido tú, ignora este correo: sin el enlace nadie puede entrar.'),
            "Entra en tu cuenta de Trollacos ($nombre) con este enlace:\n$url\n\nCaduca en " . TOKEN_MIN . " minutos. Si no lo has pedido tú, ignora este correo.");
        if (!$ok) { devolver_envio($email); }
    }
    // misma respuesta siempre, para no desvelar qué emails tienen cuenta
    responder(['ok' => true, 'mensaje' => 'Si ese email está en una cuenta, te acabamos de mandar un enlace para entrar. Mira también en spam.']);
}

if ($accion === 'email_token' && $post) {
    $in = entrada();
    $h = hash('sha256', (string)($in['token'] ?? ''));
    [$d, $fl] = abrir();
    $t = $d['tokens'][$h] ?? null;
    if (!$t || $t['x'] < time() || !isset($d['usuarios'][$t['u']])) { cerrar($d, $fl, false); responder(['error' => 'token', 'mensaje' => 'Este enlace ha caducado o ya se ha usado. Pide uno nuevo.'], 400); }
    unset($d['tokens'][$h]);
    $nombre = $t['u']; $email = email_descifrar($t['em']);
    $u = &$d['usuarios'][$nombre];
    if ($t['t'] === 'v') {
        $otra = cuenta_por_email($d, $email);
        if ($otra && $otra !== $nombre) { unset($u); cerrar($d, $fl); responder(['error' => 'ocupado', 'mensaje' => 'Ese email ya está en otra cuenta.'], 400); }
        $u['em'] = email_cifrar($email); $u['eh'] = email_huella($email); $u['ev'] = true; $u['e14'] = true;
        $u['bo'] = (bool)$t['bo']; if ($t['bo']) { $u['bot'] = time(); }   // fecha del consentimiento
        unset($u); cerrar($d, $fl);
        responder(['ok' => true, 'tipo' => 'confirmado', 'nombre' => $nombre, 'mensaje' => '¡Email confirmado! Ya puedes entrar con él desde cualquier sitio.']);
    }
    // entrar: código nuevo solo para este dispositivo (los demás siguen funcionando)
    $codigo = codigo_nuevo();
    $u['hx'] = array_slice(array_merge($u['hx'] ?? [], [hash_codigo($nombre, $codigo)]), -8);
    unset($u); cerrar($d, $fl);
    responder(['ok' => true, 'tipo' => 'entrar', 'nombre' => $nombre, 'codigo' => $codigo]);
}

if (in_array($accion, ['email_quitar', 'boletin'], true) && $post) {
    $in = entrada();
    [$d, $fl] = abrir();
    [$nombre, $err] = usuario($d, $in);
    if (!$nombre) { cerrar($d, $fl); responder(['error' => 'login', 'mensaje' => $err], 401); }
    $u = &$d['usuarios'][$nombre];
    if ($accion === 'email_quitar') { unset($u['em'], $u['eh'], $u['ev'], $u['bo'], $u['bot'], $u['e14']); $m = 'Email borrado de tu cuenta.'; }
    else {
        if (empty($u['ev'])) { unset($u); cerrar($d, $fl, false); responder(['error' => 'email', 'mensaje' => 'Primero añade y confirma tu email.'], 400); }
        $u['bo'] = !empty($in['si']); if ($u['bo']) { $u['bot'] = time(); }
        $m = $u['bo'] ? '¡Apuntado al boletín!' : 'Te has borrado del boletín.';
    }
    unset($u); cerrar($d, $fl);
    responder(['ok' => true, 'mensaje' => $m]);
}

if ($accion === 'baja' && $post) {
    $in = entrada();
    $nombre = strtoupper((string)($in['u'] ?? ''));
    [$d, $fl] = abrir();
    $u = $d['usuarios'][$nombre] ?? null;
    $em = $u && !empty($u['ev']) ? email_descifrar($u['em'] ?? '') : null;
    if (!$em || !hash_equals(token_baja($em), (string)($in['t'] ?? ''))) { cerrar($d, $fl, false); responder(['error' => 'baja', 'mensaje' => 'Enlace de baja no válido.'], 400); }
    $d['usuarios'][$nombre]['bo'] = false;
    cerrar($d, $fl);
    responder(['ok' => true, 'mensaje' => 'Listo: ya no recibirás el boletín de Trollacos.']);
}

if ($accion === 'apostar' && $post) {
    $in = entrada();
    $tipo = (string)($in['tipo'] ?? '');
    $sel = strtoupper(trim((string)($in['seleccion'] ?? '')));
    $cant = (int)($in['cantidad'] ?? 0);
    if (!in_array($tipo, ['1x2', 'exacto'], true)) { responder(['error' => 'datos'], 400); }
    if ($tipo === '1x2' && !in_array($sel, ['1', 'X', '2'], true)) { responder(['error' => 'datos'], 400); }
    if ($tipo === 'exacto') {
        if (!preg_match('/^(\d{1,2})-(\d{1,2})$/', $sel, $m) || $m[1] > 15 || $m[2] > 15) { responder(['error' => 'datos', 'mensaje' => 'Pon un resultado como 2-1.'], 400); }
        $sel = ((int)$m[1]) . '-' . ((int)$m[2]);
    }
    if ($cant < 1 || $cant > 1000000) { responder(['error' => 'cantidad', 'mensaje' => 'Pon cuántas fichas quieres jugar.'], 400); }

    $p = partido_por_id(partidos(), $in['partido'] ?? '');
    if (!$p) { responder(['error' => 'partido', 'mensaje' => 'Ese partido no está disponible.'], 400); }
    if (!in_array($p['estado'], ['SCHEDULED', 'TIMED'], true) || time() > strtotime($p['fecha']) - CIERRE_SEG) {
        responder(['error' => 'cerrado', 'mensaje' => 'Este partido ya está cerrado para pronósticos.'], 400);
    }
    $cuota = $tipo === '1x2' ? (float)($p['cuotas'][$sel] ?? 0) : CUOTA_EXACTO;
    if ($cuota < 1.01) { responder(['error' => 'partido', 'mensaje' => 'Este partido aún no tiene cuotas.'], 400); }

    [$d, $fl] = abrir();
    [$nombre, $err] = usuario($d, $in);
    if (!$nombre) { cerrar($d, $fl); responder(['error' => 'login', 'mensaje' => $err], 401); }
    foreach ($d['apuestas'] as $a) {
        if ($a['u'] === $nombre && (string)$a['p'] === (string)$p['id'] && $a['t'] === $tipo) {
            cerrar($d, $fl, false); responder(['error' => 'repetida', 'mensaje' => 'Ya tienes un pronóstico de este tipo en este partido.'], 400);
        }
    }
    $u = &$d['usuarios'][$nombre];
    $bono = 0;
    if (!in_array($p['j'], $u['jb'] ?? [], true)) { $u['jb'][] = $p['j']; $u['f'] += BONO_JORNADA; $bono = BONO_JORNADA; }
    if ($cant > $u['f']) { if ($bono) { $u['f'] -= $bono; array_pop($u['jb']); } cerrar($d, $fl, false); responder(['error' => 'fichas', 'mensaje' => 'No tienes fichas suficientes. ¡Juega a Trollaco Run para ganar más!'], 400); }
    $u['f'] -= $cant;
    $d['apuestas'][] = ['id' => bin2hex(random_bytes(6)), 'u' => $nombre, 'p' => $p['id'], 'j' => $p['j'], 't' => $tipo, 's' => $sel,
                        'c' => $cant, 'q' => $cuota, 'e' => 'pendiente', 'g' => 0, 'ts' => time()];
    unset($u);
    cerrar($d, $fl);
    responder(['ok' => true, 'bono' => $bono] + resumen($d, $nombre));
}

if ($accion === 'cancelar' && $post) {
    $in = entrada();
    $id = (string)($in['id'] ?? '');
    [$d, $fl] = abrir();
    [$nombre, $err] = usuario($d, $in);
    if (!$nombre) { cerrar($d, $fl); responder(['error' => 'login', 'mensaje' => $err], 401); }
    $pp = partidos();
    foreach ($d['apuestas'] as $i => $a) {
        if ($a['id'] !== $id || $a['u'] !== $nombre) { continue; }
        if ($a['e'] !== 'pendiente') { cerrar($d, $fl, false); responder(['error' => 'cerrado', 'mensaje' => 'Ese pronóstico ya está resuelto.'], 400); }
        $p = partido_por_id($pp, $a['p']);
        if (!$p || !in_array($p['estado'], ['SCHEDULED', 'TIMED'], true) || time() > strtotime($p['fecha']) - CIERRE_SEG) {
            cerrar($d, $fl, false); responder(['error' => 'cerrado', 'mensaje' => 'El partido ya está cerrado: no se puede cancelar.'], 400);
        }
        $d['usuarios'][$nombre]['f'] += $a['c'];
        array_splice($d['apuestas'], $i, 1);
        cerrar($d, $fl);
        responder(['ok' => true, 'devueltas' => $a['c']] + resumen($d, $nombre));
    }
    cerrar($d, $fl, false);
    responder(['error' => 'datos', 'mensaje' => 'No encuentro ese pronóstico.'], 400);
}

responder(['error' => 'accion'], 400);
