<?php
/**
 * Обработчик формы «Get price» на growupgh.com.
 * Принимает POST (fetch, JSON-ответ), шлёт письмо на sales@growupgh.com.
 * Защита: honeypot-поле, минимальное время заполнения, лимит по IP, валидация.
 * Персональные данные нигде не сохраняются — только письмо (RODO art. 6(1)(b)).
 */
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

const TO_EMAIL   = 'sales@growupgh.com';
const FROM_EMAIL = 'noreply@growupgh.com';
const SITE_NAME  = 'GrowUp Greenhouses';
const MIN_FILL_SECONDS = 3;       // быстрее человек форму не заполнит
const RATE_LIMIT_SECONDS = 60;    // не чаще одной заявки в минуту с одного IP

function respond(bool $ok, string $message, int $code = 200): void {
    http_response_code($code);
    echo json_encode(['ok' => $ok, 'message' => $message], JSON_UNESCAPED_UNICODE);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    respond(false, 'Method not allowed', 405);
}

// Только со своего сайта
$origin = $_SERVER['HTTP_ORIGIN'] ?? $_SERVER['HTTP_REFERER'] ?? '';
if ($origin !== '' && !preg_match('~^https?://(www\.)?growupgh\.com(/|$)~i', $origin)) {
    respond(false, 'Forbidden', 403);
}

$f = static fn(string $k, int $max): string =>
    mb_substr(trim(strip_tags((string)($_POST[$k] ?? ''))), 0, $max);

$name    = $f('name', 100);
$phone   = $f('phone', 40);
$email   = $f('email', 120);
$message = $f('message', 2000);
$product = $f('product', 120);     // что интересует (из карточки, если нажали там)
$page    = $f('page', 200);
$website = (string)($_POST['website'] ?? '');   // honeypot: должно быть пусто
$ts      = (int)($_POST['ts'] ?? 0);            // время открытия формы (unix)

// Антиспам
if ($website !== '') {
    respond(true, 'Thank you! We will contact you shortly.');   // боту отвечаем «успех»
}
if ($ts > 0 && (time() - $ts) < MIN_FILL_SECONDS) {
    respond(true, 'Thank you! We will contact you shortly.');
}
$ip = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
$lock = sys_get_temp_dir() . '/gu_lead_' . md5($ip);
if (is_file($lock) && (time() - (int)filemtime($lock)) < RATE_LIMIT_SECONDS) {
    respond(false, 'Please wait a minute before sending another request.', 429);
}

// Валидация
if ($name === '') {
    respond(false, 'Please enter your name.', 422);
}
if ($phone === '' && $email === '') {
    respond(false, 'Please leave a phone number or an e-mail so we can reply.', 422);
}
if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    respond(false, 'Please check the e-mail address.', 422);
}
if ($phone !== '' && !preg_match('/^[0-9+() \-.]{6,40}$/', $phone)) {
    respond(false, 'Please check the phone number.', 422);
}
foreach ([$name, $phone, $email] as $v) {        // против инъекции заголовков
    if (preg_match('/[\r\n]/', $v)) {
        respond(false, 'Invalid input.', 422);
    }
}

// Письмо
$subject = '[growupgh.com] Price request from ' . $name;
$lines = [
    'New price request from growupgh.com',
    '',
    'Name:     ' . $name,
    'Phone:    ' . ($phone !== '' ? $phone : '—'),
    'E-mail:   ' . ($email !== '' ? $email : '—'),
    'Interest: ' . ($product !== '' ? $product : '—'),
    '',
    'Message:',
    $message !== '' ? $message : '—',
    '',
    '---',
    'Page: ' . $page,
    'Time: ' . date('Y-m-d H:i:s T'),
    'IP:   ' . $ip,
];
$body = implode("\r\n", $lines);

$headers = [
    'From: ' . SITE_NAME . ' <' . FROM_EMAIL . '>',
    'Reply-To: ' . ($email !== '' ? $email : FROM_EMAIL),
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'X-Mailer: growupgh-form',
];

$encodedSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';
$sent = @mail(TO_EMAIL, $encodedSubject, $body, implode("\r\n", $headers), '-f' . FROM_EMAIL);

if ($sent) {
    @touch($lock);
    respond(true, 'Thank you! We will contact you shortly.');
}
respond(false, 'Sorry, the message could not be sent. Please e-mail us at sales@growupgh.com.', 500);
