/* Cookie consent + lead form for growupgh.com. No jQuery dependency. */
(function () {
  'use strict';

  /* ---------------- cookie consent ---------------- */
  var KEY = 'gu_consent';          // "accepted" | "rejected"
  var HUBSPOT_SRC = '//js-eu1.hs-scripts.com/145440615.js';

  function getConsent() {
    try {
      var m = document.cookie.match(/(?:^|; )gu_consent=([^;]*)/);
      return m ? decodeURIComponent(m[1]) : null;
    } catch (e) { return null; }
  }
  function setConsent(v) {
    var d = new Date(); d.setTime(d.getTime() + 365 * 864e5);
    document.cookie = KEY + '=' + v + '; expires=' + d.toUTCString() + '; path=/; SameSite=Lax' +
      (location.protocol === 'https:' ? '; Secure' : '');
  }
  function loadHubSpot() {
    if (document.getElementById('hs-script-loader')) return;
    var s = document.createElement('script');
    s.type = 'text/javascript'; s.id = 'hs-script-loader'; s.async = true; s.defer = true;
    s.src = HUBSPOT_SRC;
    document.body.appendChild(s);
  }
  function hideBanner() {
    var b = document.getElementById('cookie-banner');
    if (b) b.classList.remove('is-visible');
  }
  function showBanner() {
    var b = document.getElementById('cookie-banner');
    if (!b) {
      b = document.createElement('div');
      b.id = 'cookie-banner';
      b.setAttribute('role', 'dialog');
      b.setAttribute('aria-live', 'polite');
      b.setAttribute('aria-label', 'Cookie consent');
      b.innerHTML =
        '<div class="cookie-banner__text">We use one analytics cookie set (HubSpot) to see how the site is used. ' +
        'It is switched on only if you accept. Essential cookies that remember your choice are always on. ' +
        '<a href="privacy.html#cookies">Privacy &amp; cookies policy</a></div>' +
        '<div class="cookie-banner__actions">' +
        '<button type="button" class="cookie-btn cookie-btn--reject" data-consent="rejected">Reject</button>' +
        '<button type="button" class="cookie-btn cookie-btn--accept" data-consent="accepted">Accept</button>' +
        '</div>';
      document.body.appendChild(b);
      b.addEventListener('click', function (e) {
        var btn = e.target.closest('[data-consent]');
        if (!btn) return;
        var v = btn.getAttribute('data-consent');
        setConsent(v);
        hideBanner();
        if (v === 'accepted') loadHubSpot();
      });
    }
    requestAnimationFrame(function () { b.classList.add('is-visible'); });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var c = getConsent();
    if (c === 'accepted') loadHubSpot();
    else if (c !== 'rejected') showBanner();

    // "Cookie settings" link in footer re-opens the banner
    document.addEventListener('click', function (e) {
      var a = e.target.closest('[data-cookie-settings]');
      if (!a) return;
      e.preventDefault();
      showBanner();
    });

    initLeadForm();
  });

  /* ---------------- lead form ---------------- */
  function initLeadForm() {
    var form = document.getElementById('lead-form');
    if (!form) return;
    var ts = form.querySelector('[name="ts"]');
    var status = form.querySelector('.lead-form__status');
    var btn = form.querySelector('button[type="submit"]');
    var pageField = form.querySelector('[name="page"]');
    if (pageField) pageField.value = location.pathname + location.hash;

    // stamp the moment the form is opened (anti-bot timing)
    document.addEventListener('click', function (e) {
      var t = e.target.closest('[data-popup-target="contacts"]');
      if (!t) return;
      if (ts) ts.value = Math.floor(Date.now() / 1000);
      var product = t.getAttribute('data-product') || productFromContext(t);
      var pf = form.querySelector('[name="product"]');
      if (pf) pf.value = product || '';
      resetForm();
      setTimeout(function () { var f = form.querySelector('[name="name"]'); if (f) f.focus(); }, 320);
    });

    function productFromContext(el) {
      var card = el.closest('.greenhouses-card__item');
      if (!card) return '';
      var h = card.querySelector('.greenhouse-card__title');
      return h ? h.textContent.trim() : '';
    }
    function setStatus(msg, kind) {
      if (!status) return;
      status.textContent = msg || '';
      status.className = 'lead-form__status' + (kind ? ' is-' + kind : '');
    }
    function resetForm() {
      setStatus('', '');
      form.classList.remove('is-sent');
      if (btn) btn.disabled = false;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var phone = form.querySelector('[name="phone"]').value.trim();
      var email = form.querySelector('[name="email"]').value.trim();
      if (!phone && !email) {
        setStatus('Please leave a phone number or an e-mail so we can reply.', 'error');
        return;
      }
      if (btn) btn.disabled = true;
      setStatus('Sending…', '');
      fetch('send.php', { method: 'POST', body: new FormData(form), credentials: 'same-origin' })
        .then(function (r) { return r.json().catch(function () { return { ok: false, message: 'Server error' }; }); })
        .then(function (data) {
          if (data.ok) {
            form.classList.add('is-sent');
            setStatus(data.message, 'ok');
            form.reset();
          } else {
            setStatus(data.message || 'Something went wrong. Please e-mail sales@growupgh.com', 'error');
            if (btn) btn.disabled = false;
          }
        })
        .catch(function () {
          setStatus('Network error. Please e-mail sales@growupgh.com', 'error');
          if (btn) btn.disabled = false;
        });
    });
  }
})();
