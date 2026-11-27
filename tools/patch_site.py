#!/usr/bin/env python3
"""Site-wide patch: lead form in the modal, cookie consent, GTM removal, footer links.
Idempotent — safe to re-run. Edits every *.html (except redirects) and tools/layout.html.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {"story.html", "garden-beds.html", "garden-pavilions.html", "additional goods.html",
        "catalog-gardenbeds.html"}

MODAL = '''	<div class="modal-form" data-popup-open="contacts">
		<div class="modal-head">
			Get a price offer
			<div class="close-modal"></div>
		</div>
		<div class="modal-body">
			<form id="lead-form" class="lead-form" action="send.php" method="post" novalidate>
				<p class="lead-form__intro">Leave your contact and we will come back with prices and lead times, usually within one working day.</p>
				<input type="text" name="name" placeholder="Your name *" required autocomplete="name" maxlength="100">
				<input type="tel" name="phone" placeholder="Phone (with country code)" autocomplete="tel" maxlength="40">
				<input type="email" name="email" placeholder="E-mail" autocomplete="email" maxlength="120">
				<textarea name="message" rows="3" placeholder="What are you interested in? Range, size, quantity, delivery country…" maxlength="2000"></textarea>
				<input type="hidden" name="product" value="">
				<input type="hidden" name="page" value="">
				<input type="hidden" name="ts" value="">
				<div class="lead-form__hp" aria-hidden="true"><label>Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
				<button type="submit">Send request</button>
				<p class="lead-form__status" role="status"></p>
				<p class="lead-form__legal">Your data controller is Czyste Pole sp. z o.o. We use the details above only to answer this request. <a href="privacy.html">Privacy policy</a>.</p>
				<p class="lead-form__alt">Or contact us directly: <a href="tel:+48572094244">+48 572 094 244</a> · <a href="mailto:sales@growupgh.com">sales@growupgh.com</a></p>
			</form>
		</div>
	</div>
'''

GTM_HEAD = re.compile(r'\s*<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->', re.S)
GTM_BODY = re.compile(r'\s*<!-- Google Tag Manager \(noscript\) -->.*?<!-- End Google Tag Manager \(noscript\) -->', re.S)
HUBSPOT = re.compile(r'\s*<!-- Start of HubSpot Embed Code -->.*?<!-- End of HubSpot Embed Code -->', re.S)
MODAL_RE = re.compile(r'\t<div class="modal-form" data-popup-open="contacts">.*?\n\t</div>\n(?=\t<div class="overlay">)', re.S)

FOOTER_OLD = '<span class="footer__copy"><a href="conf.html">Confidential policy</a></span>'
FOOTER_NEW = ('<span class="footer__copy"><a href="privacy.html">Privacy &amp; cookies</a> · '
              '<a href="#" data-cookie-settings>Cookie settings</a></span>')


def patch(path: pathlib.Path) -> bool:
    s = path.read_text(encoding="utf-8")
    o = s
    s = GTM_HEAD.sub("", s)
    s = GTM_BODY.sub("", s)
    s = HUBSPOT.sub("", s)
    s = MODAL_RE.sub(lambda m: MODAL, s)
    s = s.replace(FOOTER_OLD, FOOTER_NEW)
    if 'css/catalog-2027.css' not in s:
        s = s.replace('<link rel="stylesheet" type="text/css" href="css/style.css">',
                      '<link rel="stylesheet" type="text/css" href="css/style.css">\n\t<link rel="stylesheet" href="css/catalog-2027.css">')
    if 'js/site.js' not in s:
        s = s.replace('<script src="js/main.js"></script>', '<script src="js/main.js"></script>\n\t<script src="js/site.js"></script>')
    if s != o:
        path.write_text(s, encoding="utf-8")
    return s != o


if __name__ == "__main__":
    files = [p for p in ROOT.glob("*.html") if p.name not in SKIP] + [ROOT / "tools" / "layout.html"]
    changed = [p.name for p in files if patch(p)]
    print("patched:", ", ".join(changed) or "nothing")
    for p in files:
        s = p.read_text(encoding="utf-8")
        missing = [k for k in ("lead-form", "js/site.js", "privacy.html") if k not in s]
        if missing or "GTM-" in s or "hs-scripts" in s:
            print("CHECK", p.name, missing, "GTM" if "GTM-" in s else "", "HS" if "hs-scripts" in s else "")
