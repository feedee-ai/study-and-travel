<?php
/**
 * Study and Travel — Meta Pixel + Conversions API.
 *
 * Ставится как PHP-сниппет в плагин Code Snippets (scope: global, active).
 * При деплое строку <?php и плейсхолдер __META_CAPI_TOKEN__ заменить (токен — из env, не коммитить).
 *
 * Логика:
 *  - браузер: базовый пиксель + PageView; на любой форме перед отправкой добавляются скрытые поля
 *    st_event_id / st_url / st_utm / st_fbc / st_fbp; после УСПЕШНОЙ отправки (без страницы «Спасибо»)
 *    — fbq('track', Lead|CompleteRegistration, {}, {eventID});
 *  - сервер: в момент, когда WordPress принял форму, то же событие с тем же event_id уходит в CAPI.
 *    Meta склеивает их по event_id, дублей нет.
 *  - /webinar* → CompleteRegistration, всё остальное → Lead. Пиксель один.
 */

if ( ! defined( 'ABSPATH' ) ) {
	return;
}

const ST_PIXEL_ID     = '1146010926423221';
const ST_CAPI_TOKEN   = '__META_CAPI_TOKEN__';
const ST_GRAPH_VER    = 'v24.0';
const ST_WEBINAR_PATH = '/webinar';
// Код из Events Manager → Test Events. Пусто в бою.
const ST_TEST_CODE    = '';
// Выводить базовый код пикселя. false — если пиксель уже грузит что-то другое (но тогда PageView может задвоиться).
const ST_LOAD_BASE    = true;
// Код страны для номеров без него: '0XXXXXXXXX' → ST_PHONE_CC . 'XXXXXXXXX'. Пусто — не трогать.
const ST_PHONE_CC     = '';

/* ---------- Браузер ---------- */

add_action( 'wp_head', function () {
	if ( is_admin() ) {
		return;
	}
	$cfg = array(
		'pixel'       => ST_PIXEL_ID,
		'webinarPath' => ST_WEBINAR_PATH,
		'loadBase'    => ST_LOAD_BASE,
	);
	?>
<script>
window.ST_TRACK = <?php echo wp_json_encode( $cfg ); ?>;
(function (C) {
	if (C.loadBase) {
		!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
		n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
		n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
		t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
		document,'script','https://connect.facebook.net/en_US/fbevents.js');
		fbq('init', C.pixel);
		fbq('track', 'PageView');
	}

	function getCookie(n) {
		var m = document.cookie.match('(?:^|; )' + n + '=([^;]*)');
		return m ? decodeURIComponent(m[1]) : '';
	}
	function setCookie(n, v, days) {
		document.cookie = n + '=' + encodeURIComponent(v) + ';path=/;max-age=' + (days * 86400) +
			';SameSite=Lax' + (location.protocol === 'https:' ? ';Secure' : '');
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
	var utm = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term']
		.map(function (k) { return q.get(k) ? k + '=' + q.get(k) : ''; })
		.filter(Boolean);
	if (utm.length) {
		setCookie('st_utm', utm.join('&') + '&landing=' + location.pathname, 90);
	}

	function isWebinar(url) {
		try { return new URL(url, location.href).pathname.indexOf(C.webinarPath) === 0; }
		catch (e) { return false; }
	}

	function setHidden(form, name, value) {
		var el = form.querySelector('input[name="' + name + '"]');
		if (!el) {
			el = document.createElement('input');
			el.type = 'hidden';
			el.name = name;
			form.appendChild(el);
		}
		el.value = value;
	}

	// capture-фаза на document: срабатывает раньше обработчиков CF7/Elementor/WPForms,
	// поэтому скрытые поля попадают в их FormData.
	document.addEventListener('submit', function (e) {
		var form = e.target;
		if (!form || form.tagName !== 'FORM' || form.querySelector('input[name="s"]')) return;
		var id = 'st-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 8);
		form.dataset.stEventId = id;
		setHidden(form, 'st_event_id', id);
		setHidden(form, 'st_url', location.href);
		setHidden(form, 'st_utm', getCookie('st_utm'));
		setHidden(form, 'st_fbc', getCookie('_fbc'));
		setHidden(form, 'st_fbp', getCookie('_fbp'));
	}, true);

	function formOf(el) {
		if (!el) return null;
		if (el.tagName === 'FORM') return el;
		return (el.querySelector && el.querySelector('form')) || (el.closest && el.closest('form'));
	}

	function fireSuccess(el) {
		var form = formOf(el);
		var id = form && form.dataset.stEventId;
		if (!id || form.dataset.stFired === id || typeof fbq !== 'function') return;
		form.dataset.stFired = id;
		var name = isWebinar(location.href) ? 'CompleteRegistration' : 'Lead';
		fbq('track', name, { content_name: document.title }, { eventID: id });
	}

	// Contact Form 7
	document.addEventListener('wpcf7mailsent', function (e) { fireSuccess(e.target); });
	// Elementor Pro и WPForms шлют jQuery-события
	function bindJq() {
		if (!window.jQuery) return;
		jQuery(document).on('submit_success', function (e) { fireSuccess(e.target); });
		jQuery(document).on('wpformsAjaxSubmitSuccess', function (e) { fireSuccess(e.target); });
	}
	if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', bindJq);
	else bindJq();

	window.stTrackSuccess = fireSuccess; // для нестандартных форм: stTrackSuccess(formElement)
})(window.ST_TRACK);
</script>
	<?php
}, 1 );

/* ---------- Сервер (Conversions API) ---------- */

function st_post( $key ) {
	return isset( $_POST[ $key ] ) ? sanitize_text_field( wp_unslash( $_POST[ $key ] ) ) : '';
}

function st_hash( $value ) {
	$value = trim( (string) $value );
	return '' === $value ? null : hash( 'sha256', mb_strtolower( $value, 'UTF-8' ) );
}

function st_normalize_phone( $raw ) {
	$digits = preg_replace( '/\D+/', '', (string) $raw );
	if ( 0 === strpos( $digits, '00' ) ) {
		$digits = substr( $digits, 2 );
	} elseif ( '' !== ST_PHONE_CC && 0 === strpos( $digits, '0' ) ) {
		$digits = ST_PHONE_CC . substr( $digits, 1 );
	}
	return strlen( $digits ) >= 7 ? $digits : '';
}

/** Достаёт телефон, email и имя из пар «описание поля => значение», по ключу и по виду значения. */
function st_pick_contacts( array $flat ) {
	$out = array( 'ph' => '', 'em' => '', 'fn' => '' );
	foreach ( $flat as $key => $value ) {
		if ( is_array( $value ) ) {
			$value = implode( ' ', $value );
		}
		$value = trim( (string) $value );
		$key   = mb_strtolower( (string) $key, 'UTF-8' );
		if ( '' === $value || 0 === strpos( $key, 'st_' ) || 0 === strpos( $key, '_' ) ) {
			continue;
		}
		if ( ! $out['em'] && is_email( $value ) ) {
			$out['em'] = $value;
		} elseif ( ! $out['ph'] && ( preg_match( '/phone|tel|телеф|номер|whatsapp|viber/u', $key ) || preg_match( '/^\+?[\d\s\-()]{7,}$/', $value ) ) ) {
			$out['ph'] = st_normalize_phone( $value );
		} elseif ( ! $out['fn'] && preg_match( '/name|имя|ім.я/u', $key ) ) {
			$out['fn'] = preg_split( '/\s+/u', $value )[0];
		}
	}
	return $out;
}

function st_client_ip() {
	foreach ( array( 'HTTP_CF_CONNECTING_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR' ) as $h ) {
		if ( ! empty( $_SERVER[ $h ] ) ) {
			return trim( explode( ',', sanitize_text_field( wp_unslash( $_SERVER[ $h ] ) ) )[0] );
		}
	}
	return '';
}

function st_capi_send_form( array $flat ) {
	static $sent = array();

	$event_id = st_post( 'st_event_id' );
	if ( '' === $event_id ) {
		$event_id = 'st-srv-' . wp_generate_uuid4(); // JS не отработал — браузерного события не будет, дедуп не нужен
	}
	if ( isset( $sent[ $event_id ] ) ) {
		return;
	}
	$sent[ $event_id ] = true;

	$url = isset( $_POST['st_url'] ) ? esc_url_raw( wp_unslash( $_POST['st_url'] ) ) : (string) wp_get_referer();
	$path = (string) wp_parse_url( $url, PHP_URL_PATH );
	$event_name = 0 === strpos( $path, ST_WEBINAR_PATH ) ? 'CompleteRegistration' : 'Lead';

	$c = st_pick_contacts( $flat );
	$user_data = array_filter( array(
		'ph'                => $c['ph'] ? array( st_hash( $c['ph'] ) ) : null,
		'em'                => $c['em'] ? array( st_hash( $c['em'] ) ) : null,
		'fn'                => $c['fn'] ? array( st_hash( $c['fn'] ) ) : null,
		'client_ip_address' => st_client_ip(),
		'client_user_agent' => isset( $_SERVER['HTTP_USER_AGENT'] ) ? sanitize_text_field( wp_unslash( $_SERVER['HTTP_USER_AGENT'] ) ) : '',
		'fbc'               => st_post( 'st_fbc' ) ?: ( isset( $_COOKIE['_fbc'] ) ? sanitize_text_field( wp_unslash( $_COOKIE['_fbc'] ) ) : '' ),
		'fbp'               => st_post( 'st_fbp' ) ?: ( isset( $_COOKIE['_fbp'] ) ? sanitize_text_field( wp_unslash( $_COOKIE['_fbp'] ) ) : '' ),
	) );

	parse_str( st_post( 'st_utm' ), $utm );

	$event = array(
		'event_name'       => $event_name,
		'event_time'       => time(),
		'event_id'         => $event_id,
		'action_source'    => 'website',
		'event_source_url' => $url,
		'user_data'        => $user_data,
		'custom_data'      => array_filter( array(
			'content_name' => $path,
			'utm_source'   => $utm['utm_source'] ?? '',
			'utm_medium'   => $utm['utm_medium'] ?? '',
			'utm_campaign' => $utm['utm_campaign'] ?? '',
			'utm_content'  => $utm['utm_content'] ?? '',
		) ),
	);

	$body = array( 'data' => array( $event ) );
	if ( '' !== ST_TEST_CODE ) {
		$body['test_event_code'] = ST_TEST_CODE;
	}

	$resp = wp_remote_post(
		'https://graph.facebook.com/' . ST_GRAPH_VER . '/' . ST_PIXEL_ID . '/events?access_token=' . rawurlencode( ST_CAPI_TOKEN ),
		array(
			'timeout' => 4,
			'headers' => array( 'Content-Type' => 'application/json' ),
			'body'    => wp_json_encode( $body ),
		)
	);

	$log   = get_option( 'st_capi_log', array() );
	$log[] = array(
		'time'   => gmdate( 'c' ),
		'event'  => $event_name,
		'id'     => $event_id,
		'url'    => $url,
		'has_ph' => (bool) $c['ph'],
		'has_em' => (bool) $c['em'],
		'fbc'    => ! empty( $user_data['fbc'] ),
		'code'   => is_wp_error( $resp ) ? $resp->get_error_message() : wp_remote_retrieve_response_code( $resp ),
		'resp'   => is_wp_error( $resp ) ? '' : substr( wp_remote_retrieve_body( $resp ), 0, 300 ),
	);
	update_option( 'st_capi_log', array_slice( $log, -50 ), false );
}

// Contact Form 7: письмо отправлено = заявка принята
add_action( 'wpcf7_mail_sent', function () {
	$s = class_exists( 'WPCF7_Submission' ) ? WPCF7_Submission::get_instance() : null;
	st_capi_send_form( $s ? (array) $s->get_posted_data() : array() );
} );

// Elementor Pro Forms
add_action( 'elementor_pro/forms/new_record', function ( $record ) {
	$flat = array();
	foreach ( (array) $record->get( 'fields' ) as $id => $f ) {
		$flat[ $id . ' ' . ( $f['type'] ?? '' ) . ' ' . ( $f['title'] ?? '' ) ] = $f['value'] ?? '';
	}
	st_capi_send_form( $flat );
} );

// WPForms
add_action( 'wpforms_process_complete', function ( $fields ) {
	$flat = array();
	foreach ( (array) $fields as $f ) {
		$flat[ ( $f['type'] ?? '' ) . ' ' . ( $f['name'] ?? '' ) ] = $f['value'] ?? '';
	}
	st_capi_send_form( $flat );
} );

// Лог последних отправок в CAPI — только для админа (через пароль приложения).
add_action( 'rest_api_init', function () {
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
