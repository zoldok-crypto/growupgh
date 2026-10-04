#!/usr/bin/env python3
"""Generates the 2027 catalogue pages of growupgh.com from the data below.

Run from the repository root:  python3 tools/build_catalog_2027.py
Header, footer and contact modal are taken from catalog-greenhouses2.html's
original layout (stored in tools/layout.html) so all pages stay consistent.
Edit PRODUCTS / ADDONS below and re-run to change the catalogue.
"""
import html
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAYOUT = (ROOT / "tools" / "layout.html").read_text(encoding="utf-8")
HEAD, FOOT = LAYOUT.split("<!--MAIN-->")
IMG = "img/cat/2027/"

NAV = [
    ("catalog-greenhouses.html", "Wooden greenhouses · CASA"),
    ("catalog-greenhouses2.html", "Metal greenhouses · Modular M"),
    ("catalog-greenhouses3.html", "Metal greenhouses · Solid S"),
    ("catalog-addons.html", "Roof windows & add-ons"),
    ("catalog-gardenbeds.html", "Garden Beds"),
]

STEP = "1 m · 0,67 m"
POLY = "4 · 6 mm"
LEN_METAL = "2 – 14 m (2 m steps) + 2 m extension"
MODULAR_TXT = ("Bolt-together galvanized arches shipped in one compact box. Choose the 1 m step "
               "for sheltered gardens, or the 0,67 m reinforced frame for mountain regions, "
               "heavy snow and exposed sites.")
SOLID_TXT = ("One-piece bent arches with no joints along the curve — the most rigid frame in the "
             "range. Choose the 1 m step for sheltered gardens, or the 0,67 m reinforced frame "
             "for heavy snow and wind.")

OLD_METAL_PHOTOS = ["card4-img0", "card4-img02", "card4-img01", "card4-img1",
                    "card4-img4", "card4-img6", "card4-img7"]


def metal(name, slug, w, h, profile, text, extra=None, photos=("detail",), note=None):
    return dict(name=name, slug=slug, text=text, note=note, extra=extra or [],
                photos=[slug] + [f"{slug}-{p}" for p in photos],
                params=[("Width", w), ("Height", h), ("Lengths", LEN_METAL),
                        ("Profile", profile), ("Arch step", STEP), ("Polycarbonate", POLY)])


def casa(width, lengths, slug, text):
    return dict(name=f"CASA {width}", slug=slug, text=text, note=None, extra=[], photos=[slug],
                params=[("Width", width), ("Height", "2,32 m"), ("Lengths", lengths),
                        ("Frame", "Impregnated Swedish pine"), ("Arch step", "1 m"),
                        ("Polycarbonate", "4 mm")])


PAGES = {
    "catalog-greenhouses.html": dict(
        title="Wooden greenhouses CASA — catalogue 2027",
        h2="CASA, in impregnated pine",
        intro=("Impregnated Swedish pine frame with a pitched roof and a roof window. The warm, "
               "classic look for a garden that is lived in. Steel fastenings at every joint, "
               "roof window for every width, full kit with clear instructions."),
        products=[
            casa("1,8 m", "2 · 3 · 4 m", "casa-1-8",
                 "The compact timber house for small plots and balconies-to-garden starts."),
            casa("2,15 m", "2 · 3 · 4 · 5 · 6 m", "casa-2-15",
                 "A balanced mid-width house — two beds and a comfortable central path."),
            casa("2,6 m", "2 · 3 · 4 · 5 · 6 m", "casa-2-6",
                 "The widest timber house, with room to hang vining crops along both walls."),
        ]),
    "catalog-greenhouses2.html": dict(
        title="Metal modular greenhouses M — catalogue 2027",
        h2="Modular arches, packed to travel",
        intro=("Galvanized steel arches (profile 40×20) bolt together from shorter sections, so the "
               "whole greenhouse ships in a compact box and is easy to carry to any plot and to "
               "assemble in a weekend. Seven forms from 2,1 to 4 m wide."),
        products=[
            metal("GAUDI M 4 m", "gaudi-m-4", "4 m", "2,3 m", "40×20", MODULAR_TXT),
            metal("GAUDI M 3,14 m", "gaudi-m-3-14", "3,14 m", "2,03 m", "40×20", MODULAR_TXT),
            metal("GABLE M 2,75 m", "gable-m-2-75", "2,75 m", "2,12 m", "40×20", MODULAR_TXT),
            metal("GABLE M 2,99 m", "gable-m-2-99", "2,99 m", "2,55 m", "40×20", MODULAR_TXT),
            metal("FLORA M 2,64 m", "flora-m-2-64", "2,64 m", "2 m", "40×20", MODULAR_TXT),
            metal("FLORA M 2,99 m", "flora-m-2-99", "2,99 m", "2,42 m", "40×20", MODULAR_TXT),
            metal("CUCUMBER M 2,1 m", "cucumber-m-2-1", "2,1 m", "2,3 m", "40×20", MODULAR_TXT),
        ]),
    "catalog-greenhouses3.html": dict(
        title="Metal solid greenhouses S — catalogue 2027",
        h2="One-piece arches, built to stand firm",
        intro=("Each arch is a single bent galvanized steel profile — no joints along the curve, "
               "the most rigid frame in the range and the fastest to assemble. Supplied on "
               "pallets. Five forms from 2,1 to 3,5 m wide."),
        products=[
            metal("GAUDI S 3 m", "gaudi-s-3", "3 m", "2,03 m", "40×20", SOLID_TXT,
                  extra=OLD_METAL_PHOTOS,
                  note="2 m and 4 m lengths are supplied by full truck load only."),
            metal("GABLE S 2,75 m", "gable-s-2-75", "2,75 m", "2,15 m", "40×20", SOLID_TXT),
            metal("GAUDI SL 2,1 m", "gaudi-sl-2-1", "2,1 m", "2,03 m", "25×20 Light", SOLID_TXT),
            metal("GAUDI SL 3 m", "gaudi-sl-3", "3 m", "2,03 m", "25×20 Light", SOLID_TXT),
            metal("GAUDI S 3,5 m", "gaudi-s-3-5", "3,5 m", "1,98 m", "40×20", SOLID_TXT,
                  photos=("box",)),
        ]),
}

WINDOWS = [("4 m", "metal", True), ("3 m", "metal", True), ("2,75 m", "metal", True),
           ("2,1 m", "metal", True), ("2,6 m", "wooden", False), ("2,15 m", "wooden", False),
           ("1,8 m", "wooden", False)]
ACCESSORIES = [
    ("Rope for vegetables", "4 · 6 · 8 · 10 m", "rope"),
    ("U-profile 2,1 m", "For 4 mm or 6 mm polycarbonate", "u-profile"),
    ("Polycarbonate tape, breathable", "25 m · with air pass", "tape-breathable"),
    ("Polycarbonate tape, sealed", "10 m · vapour-tight", "tape-sealed"),
    ("Metal tape", "25 m", "metal-tape"),
    ("Auto-opener", "Full kit · opens with heat", "auto-opener"),
]

e = html.escape


def slide(name, gallery, folder=IMG):
    return (f'\t\t\t\t\t\t\t\t\t<div class="swiper-slide">\n'
            f'\t\t\t\t\t\t\t\t\t\t<a href="{folder}{name}_b.jpg" data-fancybox="{gallery}">\n'
            f'\t\t\t\t\t\t\t\t\t\t<img src="{folder}{name}.jpg" alt="" loading="lazy"></a>\n'
            f'\t\t\t\t\t\t\t\t\t</div>\n')


def card(p):
    slides = "".join(slide(n, p["slug"]) for n in p["photos"])
    slides += "".join(slide(n, p["slug"], "img/cat/") for n in p["extra"])
    params = "".join(
        f'\t\t\t\t\t\t\t\t<div class="greenhouses-card__param">\n'
        f'\t\t\t\t\t\t\t\t\t<div class="greenhouses-card__key">{e(k)}</div>\n'
        f'\t\t\t\t\t\t\t\t\t<div class="greenhouses-card__value">{e(v)}</div>\n'
        f'\t\t\t\t\t\t\t\t</div>\n' for k, v in p["params"])
    note = f'<br><br><em>{e(p["note"])}</em>' if p["note"] else ""
    nav = ('\t\t\t\t\t\t\t\t<div class="swiper-button-next"></div>\n'
           '\t\t\t\t\t\t\t\t<div class="swiper-button-prev"></div>\n'
           if len(p["photos"]) + len(p["extra"]) > 1 else "")
    return f'''				<!--{e(p["name"])}-->
					<div class="greenhouses-card__item" id="{p["slug"]}">
						<div class="card__img greenhouses-card__img">
							<div class="swiper-container swiper-container1">
								<div class="swiper-wrapper">
{slides}								</div>
{nav}							</div>
						</div>
						<div class="greenhouses-card__info">
							<h3 class="card-item__title greenhouse-card__title">{e(p["name"])}</h3>
							<div class="greenhouses-card__parameters">
{params}							</div>
							<div class="card__descr greenhouses-card__descr">
								<p>{e(p["text"])}{note}</p>
							</div>
							<div class="card-link__box greenhouses-link__box">
								<a href="#" data-popup-target="contacts" class="card-link">Get price</a>
							</div>
						</div>
					</div>
'''


def aside(current):
    items = []
    for href, label in NAV:
        if href == current:
            items.append(f'\t\t\t\t\t\t<li class="aside__item"><a href="#" class="aside__link current">'
                         f'{e(label)}<span class="aside-chevron"></span></a></li>')
        else:
            items.append(f'\t\t\t\t\t\t<li class="aside__item"><a href="/{href}" class="aside__link">'
                         f'{e(label)}</a></li>')
    return ('\t\t\t\t<aside class="aside">\n\t\t\t\t\t<ul class="aside__list">\n'
            + "\n".join(items) + '\n\t\t\t\t\t</ul>\n\t\t\t\t</aside>\n')


def page(filename, title, h2, intro, body):
    head = HEAD.replace("{{TITLE}}", e(title)).replace("{{DESCRIPTION}}", e(intro))
    main = f'''	<main class="page-body catalog-greenhouse">
		<div class="container">
			<div class="catalog-intro">
				<span class="catalog-intro__label">Greenhouse catalogue 2027</span>
				<h2 class="advantages__title catalog-intro__title">{e(h2)}</h2>
				<p class="catalog-intro__text">{e(intro)}</p>
			</div>
			<div class="greenhouses-box">
{aside(filename)}				<div class="greenhouses-cards__wrapper">
{body}				</div>
			</div>
		</div>
	</main>
'''
    (ROOT / filename).write_text(head + main + FOOT, encoding="utf-8")


def addons_body():
    rows = "".join(
        f'\t\t\t\t\t\t\t<tr><td>{w} · {kind}</td><td>●</td><td>{"●" if r else "—"}</td></tr>\n'
        for w, kind, r in WINDOWS)
    acc = "".join(
        f'''\t\t\t\t\t\t<li class="addons-grid__item">
							<a href="{IMG}{s}_b.jpg" data-fancybox="addons"><img src="{IMG}{s}.jpg" alt="{e(n)}" loading="lazy"></a>
							<span class="addons-grid__name">{e(n)}</span>
							<span class="addons-grid__spec">{e(spec)}</span>
						</li>
''' for n, spec, s in ACCESSORIES)
    return f'''					<section class="addons-block">
						<h3 class="card-item__title greenhouse-card__title">Roof windows, matched to your frame</h3>
						<div class="addons-windows">
							<a href="{IMG}roof-window_b.jpg" data-fancybox="addons" class="addons-windows__img"><img src="{IMG}roof-window.jpg" alt="Roof window" loading="lazy"></a>
							<div>
								<p>Each window is sized to the greenhouse width and its arch step — order by the width of your greenhouse.</p>
								<table class="addons-table">
									<thead><tr><th>Window for width</th><th>Step 1 m</th><th>Step 0,67 m</th></tr></thead>
									<tbody>
{rows}									</tbody>
								</table>
								<p>Every window ships as a full kit with hinges, seals and fixings. Pair it with the auto-opener for hands-free ventilation.</p>
							</div>
						</div>
					</section>
					<section class="addons-block">
						<h3 class="card-item__title greenhouse-card__title">Finishing and growing accessories</h3>
						<ul class="addons-grid">
{acc}						</ul>
						<div class="card-link__box greenhouses-link__box">
							<a href="#" data-popup-target="contacts" class="card-link">Get price</a>
						</div>
					</section>
'''


if __name__ == "__main__":
    for fn, d in PAGES.items():
        page(fn, d["title"], d["h2"], d["intro"], "".join(card(p) for p in d["products"]))
    page("catalog-addons.html", "Roof windows and accessories — catalogue 2027",
         "Add-ons", "Roof windows sized to every greenhouse width and arch step, plus finishing "
         "and growing accessories.", addons_body())
    print("done")
