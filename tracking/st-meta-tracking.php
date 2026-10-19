<?php
/**
 * Study and Travel — Meta Pixel + Conversions API.
 *
 * Ставится как PHP-сниппет в плагин Code Snippets (scope: global, active).
 * При деплое строку <?php убрать, плейсхолдер __META_CAPI_TOKEN__ заменить токеном из env (не коммитить).
 *
 * Как устроен сайт (аудит 19.10.2026):
 *  - формы — свои, без плагинов: кнопка .send-ajax шлёт jQuery.ajax в мейлер темы
 *    (/wp-content/themes/main-template/mailer/form.php на страницах WP, mailer/slovakia.php на лендингах),
 *    мейлер отправляет заявку в Telegram, страница показывает модалку «Надіслано/Готово»;
 *  - /studying-in-slovakia/ и /consultation-studying-in-slovakia/ — статические папки вне WordPress,
 *    wp_head туда не попадает: им нужен один тег <script src="/?st-track-js=1" defer> перед </body>.
 *
 * Логика:
 *  - браузер ловит УСПЕШНЫЙ ответ мейлера (ajaxSuccess), без клика «ОК» и без страницы «Спасибо»,
 *    и сразу шлёт fbq('track', Lead|CompleteRegistration, {...}, {eventID}) во все пиксели страницы;
 *  - тем же моментом через navigator.sendBeacon уходит POST /wp-json/st/v1/lead на свой домен
 *    (адблок и ITP его не режут, закрытие вкладки не мешает) — сервер шлёт событие в CAPI с тем же event_id,
 *    захешированными телефоном/email/именем, IP, UA, fbc/fbp, external_id и страной. Meta склеивает пару.
 *  - пути из ST_REG_PATHS (регистрация на вебинар) → CompleteRegistration, всё остальное → Lead.
 */

if ( ! defined( 'ABSPATH' ) ) {
	return;
}

const ST_PIXEL_ID   = '1146010926423221';
const ST_CAPI_TOKEN = '__META_CAPI_TOKEN__';
const ST_GRAPH_VER  = 'v24.0';
// Регистрации на вебинар. /studying-in-slovakia/ — вебинарный лендинг («Зареєструватися», доступ через бот).
const ST_REG_PATHS  = array( '/webinar', '/studying-in-slovakia' );
// На регистрациях дополнительно шлём Lead — кампания увидит заявку, на что бы она ни оптимизировалась.
const ST_REG_ALSO_LEAD = true;
// Пиксели лендингов, куда сервер тоже шлёт события (токен имеет к ним доступ). Путь => ID.
const ST_EXTRA_PIXELS = array( '/studying-in-slovakia' => '1557571255679048' );
// Код из Events Manager → Test Events. Пусто в бою.
const ST_TEST_CODE  = '';
// Аудитория — Украина: '0XXXXXXXXX' → '380XXXXXXXXX'.
const ST_PHONE_CC   = '380';

/* ---------- Браузер ---------- */

function st_track_js() {
	$cfg = array(
		'pixel'    => ST_PIXEL_ID,
		'regPaths' => ST_REG_PATHS,
		'regLead'  => ST_REG_ALSO_LEAD,
		'endpoint' => rest_url( 'st/v1/lead' ),
	);
	$js = <<<'JS'
(function (C) {
	if (window.__stTrack) return;
	window.__stTrack = 1;

	/* Пиксель: базовый код, если его нет; основной пиксель — если страница его не инициализировала. */
	if (!window.fbq) {
		!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
		n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
		n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
		t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
		document,'script','https://connect.facebook.net/en_US/fbevents.js');
	}
	function hasMainPixel() {
		try {
			if (fbq.getState) {
				var px = fbq.getState().pixels || [];
				for (var i = 0; i < px.length; i++) if (String(px[i].id) === C.pixel) return true;
			}
		} catch (e) {}
		var q = fbq.queue || [];
		for (var j = 0; j < q.length; j++) if (q[j] && q[j][0] === 'init' && String(q[j][1]) === C.pixel) return true;
		return false;
	}

	function getCookie(n) {
		var m = document.cookie.match('(?:^|; )' + n + '=([^;]*)');
		return m ? decodeURIComponent(m[1]) : '';
	}
	function setCookie(n, v, days) {
		document.cookie = n + '=' + encodeURIComponent(v) + ';path=/;max-age=' + (days * 86400) +
			';SameSite=Lax' + (location.protocol === 'https:' ? ';Secure' : '');
	}
	function rnd() { return Math.random().toString(36).slice(2, 10); }

	// Свой id посетителя → external_id в CAPI (стабильный ключ для склейки визитов).
	var vid = getCookie('st_vid');
	if (!vid) { vid = 'v' + Date.now().toString(36) + rnd(); }
	setCookie('st_vid', vid, 365);

	if (!hasMainPixel()) {
		fbq('init', C.pixel, { external_id: vid });
		fbq('trackSingle', C.pixel, 'PageView');
	}

	// Свои _fbc/_fbp на случай, если fbevents.js заблокирован: сервер всё равно получит метку клика.
	var q = new URLSearchParams(location.search);
	var fbclid = q.get('fbclid');
	if (fbclid && getCookie('_fbc').slice(-fbclid.length) !== fbclid) {
		setCookie('_fbc', 'fb.1.' + Date.now() + '.' + fbclid, 90);
	}
	if (!getCookie('_fbp')) {
		setCookie('_fbp', 'fb.1.' + Date.now() + '.' + Math.floor(Math.random() * 1e10), 90);
	}

	// Последние UTM живут 90 дней — заявка унесёт их, даже если человек вернулся без меток.
	var UTM = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
	var utmNow = UTM.map(function (k) { return q.get(k) ? k + '=' + encodeURIComponent(q.get(k)) : ''; }).filter(Boolean);
	if (utmNow.length) setCookie('st_utm', utmNow.join('&') + '&landing=' + encodeURIComponent(location.pathname), 90);

	function eventName() {
		var p = location.pathname;
		for (var i = 0; i < C.regPaths.length; i++) if (p.indexOf(C.regPaths[i]) === 0) return 'CompleteRegistration';
		return 'Lead';
	}

	function parseData(data) {
		var out = {};
		if (!data) return out;
		if (typeof data === 'string') {
			new URLSearchParams(data).forEach(function (v, k) { out[k] = v; });
		} else if (window.FormData && data instanceof FormData) {
			data.forEach(function (v, k) { if (typeof v === 'string') out[k] = v; });
		} else if (typeof data === 'object') {
			for (var k in data) if (typeof data[k] !== 'object') out[k] = String(data[k]);
		}
		return out;
	}

	function pick(f, re) {
		for (var k in f) if (re.test(k) && String(f[k]).trim()) return String(f[k]).trim();
		return '';
	}

	var lastSig = '', lastAt = 0;
	function fireLead(fields) {
		var phone = pick(fields, /phone|tel/i);
		var email = pick(fields, /mail/i);
		var name = pick(fields, /^name$|first|fio|имя/i);
		if (!phone && !email) return;
		// Одна заявка — одно событие, даже если обработчик сработал дважды.
		var sig = phone + '|' + email;
		if (sig === lastSig && Date.now() - lastAt < 10000) return;
		lastSig = sig; lastAt = Date.now();

		var id = 'st-' + Date.now().toString(36) + '-' + rnd();
		var ev = eventName();
		var subject = fields.form_subject || document.title;
		try {
			var params = { content_name: subject, content_category: location.pathname };
			fbq('track', ev, params, { eventID: id });
			if (ev !== 'Lead' && C.regLead) fbq('track', 'Lead', params, { eventID: id });
		} catch (e) {}

		var utm = {};
		new URLSearchParams(getCookie('st_utm')).forEach(function (v, k) { utm[k] = v; });
		UTM.forEach(function (k) { if (fields[k]) utm[k] = fields[k]; });

		var payload = JSON.stringify({
			event_id: id, url: location.href, referrer: document.referrer, subject: subject,
			name: name, phone: phone, email: email,
			fbc: getCookie('_fbc'), fbp: getCookie('_fbp'), vid: vid, utm: utm
		});
		var sent = false;
		try {
			sent = navigator.sendBeacon && navigator.sendBeacon(C.endpoint, new Blob([payload], { type: 'application/json' }));
		} catch (e) {}
		if (!sent) {
			try {
				fetch(C.endpoint, { method: 'POST', keepalive: true, credentials: 'same-origin',
					headers: { 'Content-Type': 'application/json' }, body: payload });
			} catch (e) {}
		}
	}

	// Мейлеры темы: form.php отвечает пустой строкой при успехе (иначе — текст ошибки),
	// остальные (slovakia.php и т.п.) — успех = любой 2xx, как и в их собственном JS.
	function onAjaxSuccess(e, xhr, s, data) {
		var url = (s && s.url) || '';
		if (!/\/mailer\/[^\/?]+\.php/.test(url)) return;
		if (/\/mailer\/form\.php/.test(url) && String(data == null ? '' : data).trim() !== '') return;
		fireLead(parseData(s.data));
	}

	function formFields(form) {
		var f = {};
		if (form && form.elements) {
			for (var i = 0; i < form.elements.length; i++) {
				var el = form.elements[i];
				if (el.name && el.type !== 'password' && el.type !== 'file') f[el.name] = el.value;
			}
		}
		return f;
	}

	var tries = 0;
	(function bind() {
		if (!window.jQuery) { if (tries++ < 100) setTimeout(bind, 100); return; }
		jQuery(document).on('ajaxSuccess', onAjaxSuccess);
		jQuery(document).on('wpformsAjaxSubmitSuccess', function (e) { fireLead(formFields(e.target)); });
	})();

	// Для нестандартных форм: stTrackLead({name, phone, email}) после успешной отправки.
	window.stTrackLead = fireLead;
})(window.ST_TRACK_CFG);
JS;
	return 'window.ST_TRACK_CFG=' . wp_json_encode( $cfg ) . ";\n" . $js;
}

// Страницы WordPress: в футер, после jQuery темы.
add_action( 'wp_footer', function () {
	if ( is_admin() ) {
		return;
	}
	echo "<script>\n" . st_track_js() . "\n</script>\n"; // phpcs:ignore WordPress.Security.EscapeOutput
}, 99 );

// Статические лендинги: <script src="https://study-and-travel.net/?st-track-js=1" defer></script>
add_action( 'init', function () {
	if ( ! isset( $_GET['st-track-js'] ) ) { // phpcs:ignore WordPress.Security.NonceVerification
		return;
	}
	header( 'Content-Type: application/javascript; charset=utf-8' );
	header( 'Cache-Control: public, max-age=600' );
	header( 'X-Content-Type-Options: nosniff' );
	echo st_track_js(); // phpcs:ignore WordPress.Security.EscapeOutput
	exit;
}, 0 );

/* ---------- Сервер (Conversions API) ---------- */

function st_hash( $value ) {
	$value = trim( (string) $value );
	return '' === $value ? null : hash( 'sha256', mb_strtolower( $value, 'UTF-8' ) );
}

function st_normalize_phone( $raw ) {
	$digits = preg_replace( '/\D+/', '', (string) $raw );
	if ( 0 === strpos( $digits, '00' ) ) {
		$digits = substr( $digits, 2 );
	} elseif ( '' !== ST_PHONE_CC && 0 === strpos( $digits, '0' ) && 10 === strlen( $digits ) ) {
		$digits = ST_PHONE_CC . substr( $digits, 1 );
	}
	return strlen( $digits ) >= 8 ? $digits : '';
}

function st_normalize_name( $raw ) {
	$raw = mb_strtolower( trim( (string) $raw ), 'UTF-8' );
	$raw = preg_replace( '/[^\p{L}\s\-]+/u', '', $raw );
	return array_values( array_filter( preg_split( '/\s+/u', $raw ) ) );
}

function st_client_ip() {
	foreach ( array( 'HTTP_CF_CONNECTING_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR' ) as $h ) {
		if ( ! empty( $_SERVER[ $h ] ) ) {
			$ip = trim( explode( ',', sanitize_text_field( wp_unslash( $_SERVER[ $h ] ) ) )[0] );
			if ( filter_var( $ip, FILTER_VALIDATE_IP ) ) {
				return $ip;
			}
		}
	}
	return '';
}

function st_log( array $row ) {
	$log   = get_option( 'st_capi_log', array() );
	$log[] = array( 'time' => gmdate( 'c' ) ) + $row;
	update_option( 'st_capi_log', array_slice( $log, -100 ), false );
}

function st_capi_lead( WP_REST_Request $req ) {
	$home = wp_parse_url( home_url(), PHP_URL_HOST );
	$src  = $req->get_header( 'origin' ) ?: $req->get_header( 'referer' );
	if ( wp_parse_url( (string) $src, PHP_URL_HOST ) !== $home ) {
		return new WP_REST_Response( null, 403 );
	}

	$d   = (array) $req->get_json_params();
	$str = function ( $k, $max = 300 ) use ( $d ) {
		return isset( $d[ $k ] ) && is_scalar( $d[ $k ] ) ? mb_substr( sanitize_text_field( (string) $d[ $k ] ), 0, $max ) : '';
	};

	$event_id = $str( 'event_id', 64 );
	if ( ! preg_match( '/^st-[a-z0-9]+-[a-z0-9]+$/', $event_id ) ) {
		return new WP_REST_Response( null, 400 );
	}
	$url = esc_url_raw( $str( 'url', 1000 ) );
	if ( wp_parse_url( $url, PHP_URL_HOST ) !== $home ) {
		return new WP_REST_Response( null, 400 );
	}

	$ip = st_client_ip();
	// Защита от накрутки: не больше 20 заявок в час с одного IP, один event_id — один раз.
	$rl_key = 'st_rl_' . md5( $ip );
	$count  = (int) get_transient( $rl_key );
	if ( $count >= 20 ) {
		return new WP_REST_Response( null, 429 );
	}
	set_transient( $rl_key, $count + 1, HOUR_IN_SECONDS );
	if ( get_transient( 'st_ev_' . md5( $event_id ) ) ) {
		return new WP_REST_Response( null, 204 );
	}
	set_transient( 'st_ev_' . md5( $event_id ), 1, DAY_IN_SECONDS );

	$phone = st_normalize_phone( $str( 'phone', 40 ) );
	$email = is_email( $str( 'email', 200 ) ) ? $str( 'email', 200 ) : '';
	if ( ! $phone && ! $email ) {
		return new WP_REST_Response( null, 400 );
	}
	$names = st_normalize_name( $str( 'name', 100 ) );

	$path       = (string) wp_parse_url( $url, PHP_URL_PATH );
	$event_name = 'Lead';
	foreach ( ST_REG_PATHS as $p ) {
		if ( 0 === strpos( $path, $p ) ) {
			$event_name = 'CompleteRegistration';
		}
	}

	$fbc = $str( 'fbc', 300 ) ?: ( isset( $_COOKIE['_fbc'] ) ? sanitize_text_field( wp_unslash( $_COOKIE['_fbc'] ) ) : '' );
	if ( ! $fbc ) {
		parse_str( (string) wp_parse_url( $url, PHP_URL_QUERY ), $qs );
		if ( ! empty( $qs['fbclid'] ) ) {
			$fbc = 'fb.1.' . round( microtime( true ) * 1000 ) . '.' . sanitize_text_field( $qs['fbclid'] );
		}
	}
	$fbp     = $str( 'fbp', 300 ) ?: ( isset( $_COOKIE['_fbp'] ) ? sanitize_text_field( wp_unslash( $_COOKIE['_fbp'] ) ) : '' );
	$vid     = $str( 'vid', 64 );
	$country = isset( $_SERVER['HTTP_CF_IPCOUNTRY'] ) ? strtolower( sanitize_text_field( wp_unslash( $_SERVER['HTTP_CF_IPCOUNTRY'] ) ) ) : '';

	$user_data = array_filter( array(
		'ph'                => $phone ? array( st_hash( $phone ) ) : null,
		'em'                => $email ? array( st_hash( $email ) ) : null,
		'fn'                => isset( $names[0] ) ? array( st_hash( $names[0] ) ) : null,
		'ln'                => isset( $names[1] ) ? array( st_hash( end( $names ) ) ) : null,
		'country'           => preg_match( '/^[a-z]{2}$/', $country ) && 'xx' !== $country ? array( st_hash( $country ) ) : null,
		'external_id'       => $vid ? array( st_hash( $vid ) ) : null,
		'client_ip_address' => $ip,
		'client_user_agent' => $req->get_header( 'user_agent' ) ? mb_substr( (string) $req->get_header( 'user_agent' ), 0, 500 ) : '',
		'fbc'               => $fbc,
		'fbp'               => $fbp,
	) );

	$utm = array();
	foreach ( (array) ( $d['utm'] ?? array() ) as $k => $v ) {
		if ( preg_match( '/^(utm_(source|medium|campaign|content|term)|landing)$/', (string) $k ) && is_scalar( $v ) ) {
			$utm[ $k ] = mb_substr( sanitize_text_field( (string) $v ), 0, 200 );
		}
	}

	$event = array(
		'event_name'       => '',
		'event_time'       => time(),
		'event_id'         => $event_id,
		'action_source'    => 'website',
		'event_source_url' => $url,
		'user_data'        => $user_data,
		'custom_data'      => array_filter( array(
			'content_name'     => $str( 'subject', 200 ),
			'content_category' => $path,
		) + $utm ),
	);
	$referrer = esc_url_raw( $str( 'referrer', 1000 ) );
	if ( $referrer ) {
		$event['referrer_url'] = $referrer;
	}

	$names_to_send = array( $event_name );
	if ( 'Lead' !== $event_name && ST_REG_ALSO_LEAD ) {
		$names_to_send[] = 'Lead';
	}
	$data = array();
	foreach ( $names_to_send as $n ) {
		$data[] = array( 'event_name' => $n ) + $event;
	}
	$body = array( 'data' => $data );
	if ( '' !== ST_TEST_CODE ) {
		$body['test_event_code'] = ST_TEST_CODE;
	}

	$pixels = array( ST_PIXEL_ID );
	foreach ( ST_EXTRA_PIXELS as $p => $px ) {
		if ( 0 === strpos( $path, $p ) ) {
			$pixels[] = $px;
		}
	}

	foreach ( array_unique( $pixels ) as $px ) {
		$resp = wp_remote_post(
			'https://graph.facebook.com/' . ST_GRAPH_VER . '/' . $px . '/events?access_token=' . rawurlencode( ST_CAPI_TOKEN ),
			array(
				'timeout' => 6,
				'headers' => array( 'Content-Type' => 'application/json' ),
				'body'    => wp_json_encode( $body ),
			)
		);
		st_log( array(
			'pixel'  => $px,
			'event'  => implode( '+', $names_to_send ),
			'id'     => $event_id,
			'url'    => $url,
			'has_ph' => (bool) $phone,
			'has_em' => (bool) $email,
			'has_fn' => isset( $names[0] ),
			'fbc'    => (bool) $fbc,
			'fbp'    => (bool) $fbp,
			'code'   => is_wp_error( $resp ) ? $resp->get_error_message() : wp_remote_retrieve_response_code( $resp ),
			'resp'   => is_wp_error( $resp ) ? '' : substr( wp_remote_retrieve_body( $resp ), 0, 300 ),
		) );
	}

	return new WP_REST_Response( null, 204 );
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'st/v1', '/lead', array(
		'methods'             => 'POST',
		'permission_callback' => '__return_true',
		'callback'            => 'st_capi_lead',
	) );
	// Лог последних отправок в CAPI — только для админа (через пароль приложения).
	register_rest_route( 'st/v1', '/capi-log', array(
		'methods'             => 'GET',
		'permission_callback' => function () {
			return current_user_can( 'manage_options' );
		},
		'callback'            => function () {
			return get_option( 'st_capi_log', array() );
		},
	) );
} );
