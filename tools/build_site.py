#!/usr/bin/env python3
"""Builds the catalogue section of growupgh.com from the 2027 greenhouse catalogue.

    python3 tools/build_site.py        (run from the repository root)

What it produces
  catalog.html                 catalogue hub: ranges, every model, comparison table
  catalog-greenhouses.html     Wooden · CASA
  catalog-greenhouses2.html    Metal Modular · M
  catalog-greenhouses3.html    Metal Solid · S
  catalog-addons.html          roof windows and accessories
  index.html                   "Catalogue 2027" block replaces the old slider card
  all *.html                   one identical header menu and footer
  story.html, garden-beds.html, garden-pavilions.html, "additional goods.html"
                               turned into redirects (old template pages)

Shared header/footer live in tools/layout.html. All product data is in this
file (MODELS, FAMILIES, RANGES, WINDOWS, ACCESSORIES) — edit and re-run.
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAYOUT = (ROOT / "tools" / "layout.html").read_text(encoding="utf-8")
HEAD, FOOT = LAYOUT.split("<!--MAIN-->")
IMG = "img/cat/2027/"
e = html.escape

# --------------------------------------------------------------------------- data

RANGES = {
    "casa": dict(
        page="catalog-greenhouses.html", code="01", short="Wooden", nav="Wooden · CASA",
        name="Wooden greenhouses CASA", hero="casa-2-15", photo_folder=IMG,
        h2="CASA, in impregnated pine",
        intro="Impregnated Swedish pine frame with a pitched roof and a roof window. The warm, "
              "classic look for a garden that is lived in.",
        chips=["Impregnated Swedish pine", "Steel fastenings at every joint",
               "Roof window for every width", "Height 2,32 m", "Polycarbonate 4 mm",
               "Full kit · clear instructions"],
        summary="3 widths · 1,8 – 2,6 m · lengths 2 – 6 m",
        delivery="Full kit with fastenings and instructions"),
    "modular": dict(
        page="catalog-greenhouses2.html", code="02", short="Metal Modular", nav="Metal Modular · M",
        name="Metal modular greenhouses M", hero="gaudi-m-4", photo_folder=IMG,
        h2="Modular arches, packed to travel",
        intro="Galvanized steel arches that bolt together from short sections and ship in one "
              "compact box — easy to carry to any plot and to assemble in a weekend.",
        chips=["Galvanized steel · 40×20", "Arch step 1 m or 0,67 m", "Polycarbonate 4 or 6 mm",
               "Lengths 2 – 14 m · +2 m extension", "Compact boxed delivery"],
        summary="7 forms · 2,1 – 4 m wide · lengths 2 – 14 m",
        delivery="One compact box"),
    "solid": dict(
        page="catalog-greenhouses3.html", code="03", short="Metal Solid", nav="Metal Solid · S",
        name="Metal solid greenhouses S", hero="gaudi-s-3", photo_folder=IMG,
        h2="One-piece arches, built to stand firm",
        intro="Each arch is a single bent steel profile — no joints along the curve, the most "
              "rigid frame in the range and the fastest to raise. Supplied on pallets.",
        chips=["Galvanized steel", "Profile 40×20 or 25×20 Light", "Arch step 1 m or 0,67 m",
               "Polycarbonate 4 or 6 mm", "Lengths 2 – 14 m · +2 m extension",
               "Delivered on pallets"],
        summary="5 forms · 2,1 – 3,5 m wide · lengths 2 – 14 m",
        delivery="On pallets"),
}

# Form families inside the metal ranges. Order here = order on the page.
FAMILIES = {
    "GAUDI": "Rounded arch — the classic, universal greenhouse form.",
    "GABLE": "Pointed, gable-style roof — sheds snow and rain, extra headroom at the ridge.",
    "FLORA": "Rounded roof on vertical walls — full standing height right up to the sides, "
             "room for shelves along the walls.",
    "CUCUMBER": "Narrow and tall — built for vining crops on a small plot.",
    "GAUDI SL": "Rounded arch in the lighter 25×20 profile — for smaller gardens and lighter kits.",
}

STEP = "1 m · 0,67 m"
POLY = "4 · 6 mm"
LEN_METAL = "2 · 4 · 6 · 8 · 10 · 12 · 14 m, +2 m extension"
MODULAR_TXT = ("Bolt-together galvanized arches shipped in one compact box. Choose the 1 m step "
               "for sheltered gardens, or the 0,67 m reinforced frame for mountain regions, "
               "heavy snow and exposed sites.")
SOLID_TXT = ("One-piece bent arches with no joints along the curve — the most rigid frame in "
             "the range. Choose the 1 m step for sheltered gardens, or the 0,67 m reinforced "
             "frame for heavy snow and wind.")


def model(rng, family, name, slug, w, h, lengths, profile=None, text="", photos=(), note=None,
          frame=None):
    params = [("Width", w), ("Height", h), ("Lengths", lengths)]
    if profile:
        params += [("Profile", profile), ("Arch step", STEP), ("Polycarbonate", POLY)]
    else:
        params += [("Frame", frame), ("Arch step", "1 m"), ("Polycarbonate", "4 mm")]
    return dict(range=rng, family=family, name=name, slug=slug, width=w, height=h,
                lengths=lengths, profile=profile or "pine", text=text, note=note,
                photos=[slug] + list(photos))


MODELS = [
    model("casa", "CASA", "CASA 1,8 m", "casa-1-8", "1,8 m", "2,32 m", "2 · 3 · 4 m",
          frame="Impregnated Swedish pine",
          text="The compact timber house for small plots and balconies-to-garden starts."),
    model("casa", "CASA", "CASA 2,15 m", "casa-2-15", "2,15 m", "2,32 m", "2 · 3 · 4 · 5 · 6 m",
          frame="Impregnated Swedish pine",
          text="A balanced mid-width house — two beds and a comfortable central path."),
    model("casa", "CASA", "CASA 2,6 m", "casa-2-6", "2,6 m", "2,32 m", "2 · 3 · 4 · 5 · 6 m",
          frame="Impregnated Swedish pine",
          text="The widest timber house, with room to hang vining crops along both walls."),

    model("modular", "GAUDI", "GAUDI M 4 m", "gaudi-m-4", "4 m", "2,3 m", LEN_METAL, "40×20",
          MODULAR_TXT, ("gaudi-m-4-detail",)),
    model("modular", "GAUDI", "GAUDI M 3,14 m", "gaudi-m-3-14", "3,14 m", "2,03 m", LEN_METAL,
          "40×20", MODULAR_TXT, ("gaudi-m-3-14-detail",)),
    model("modular", "GABLE", "GABLE M 2,75 m", "gable-m-2-75", "2,75 m", "2,12 m", LEN_METAL,
          "40×20", MODULAR_TXT, ("gable-m-2-75-detail",)),
    model("modular", "GABLE", "GABLE M 2,99 m", "gable-m-2-99", "2,99 m", "2,55 m", LEN_METAL,
          "40×20", MODULAR_TXT, ("gable-m-2-99-detail",)),
    model("modular", "FLORA", "FLORA M 2,64 m", "flora-m-2-64", "2,64 m", "2 m", LEN_METAL,
          "40×20", MODULAR_TXT, ("flora-m-2-64-detail",)),
    model("modular", "FLORA", "FLORA M 2,99 m", "flora-m-2-99", "2,99 m", "2,42 m", LEN_METAL,
          "40×20", MODULAR_TXT, ("flora-m-2-99-detail",)),
    model("modular", "CUCUMBER", "CUCUMBER M 2,1 m", "cucumber-m-2-1", "2,1 m", "2,3 m",
          LEN_METAL, "40×20", MODULAR_TXT, ("cucumber-m-2-1-detail",)),

    model("solid", "GAUDI", "GAUDI S 3 m", "gaudi-s-3", "3 m", "2,03 m", LEN_METAL, "40×20",
          SOLID_TXT, ("gaudi-s-3-detail",),
          note="2 m and 4 m lengths are supplied by full truck load only."),
    model("solid", "GAUDI", "GAUDI S 3,5 m", "gaudi-s-3-5", "3,5 m", "1,98 m", LEN_METAL, "40×20",
          SOLID_TXT, ("gaudi-s-3-5-box",)),
    model("solid", "GABLE", "GABLE S 2,75 m", "gable-s-2-75", "2,75 m", "2,15 m", LEN_METAL,
          "40×20", SOLID_TXT, ("gable-s-2-75-detail",)),
    model("solid", "GAUDI SL", "GAUDI SL 2,1 m", "gaudi-sl-2-1", "2,1 m", "2,03 m", LEN_METAL,
          "25×20 Light", SOLID_TXT, ("gaudi-sl-2-1-detail",)),
    model("solid", "GAUDI SL", "GAUDI SL 3 m", "gaudi-sl-3", "3 m", "2,03 m", LEN_METAL,
          "25×20 Light", SOLID_TXT, ("gaudi-sl-3-detail",)),
]

# Real production photos already on the site (img/cat/*.jpg), shown per range.
REAL_PHOTOS = {
    "casa": ["card-img13", "card-img14", "card-img2", "card-img3", "card-img5", "card-img6",
             "card-img7", "card-img8", "card-img", "card-img10", "card-img11", "card-img12"],
    "solid": ["card4-img0", "card4-img02", "card4-img01", "card4-img1", "card4-img4",
              "card4-img6", "card4-img7"],
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

HOW_TO_CHOOSE = [
    ("A", "Arch step", "1 m — standard frame for sheltered gardens. 0,67 m — reinforced frame "
                       "for mountain regions, heavy snow and strong wind."),
    ("B", "Polycarbonate", "4 mm — light and bright, the everyday choice. 6 mm — warmer and "
                           "tougher against hail."),
    ("C", "Profile", "40×20 — standard steel profile. 25×20 Light — lighter GAUDI SL frames "
                     "for smaller gardens."),
    ("D", "Length", "Metal greenhouses from 2 to 14 m. Extend any time with a 2 m extension "
                    "module."),
]
HOW_TO_ORDER = [
    ("Choose range, size & options", "Pick the range, width and length, then the arch step "
                                     "(1 m or 0,67 m) and polycarbonate (4 or 6 mm)."),
    ("Confirm & ship", "We confirm availability and kit contents. Your greenhouse ships "
                       "complete with fastenings and instructions."),
    ("Assemble & grow", "Follow the step-by-step guide. Most builds go up in a weekend."),
]

NAV = [("catalog.html", "Catalogue overview")] + \
      [(r["page"], r["nav"]) for r in RANGES.values()] + \
      [("catalog-addons.html", "Roof windows & add‑ons"), ("catalog-gardenbeds.html", "Garden Beds")]

# ----------------------------------------------------------------------- helpers


def slide(name, gallery, folder):
    return (f'\t\t\t\t\t\t\t\t\t<div class="swiper-slide">\n'
            f'\t\t\t\t\t\t\t\t\t\t<a href="{folder}{name}_b.jpg" data-fancybox="{gallery}">\n'
            f'\t\t\t\t\t\t\t\t\t\t<img src="{folder}{name}.jpg" alt="" loading="lazy"></a>\n'
            f'\t\t\t\t\t\t\t\t\t</div>\n')


def swiper(names, gallery, folder=IMG, cls="swiper-container1"):
    nav = ('\t\t\t\t\t\t\t\t<div class="swiper-button-next"></div>\n'
           '\t\t\t\t\t\t\t\t<div class="swiper-button-prev"></div>\n' if len(names) > 1 else "")
    return (f'\t\t\t\t\t\t\t<div class="swiper-container {cls}">\n'
            f'\t\t\t\t\t\t\t\t<div class="swiper-wrapper">\n'
            + "".join(slide(n, gallery, folder) for n in names)
            + f'\t\t\t\t\t\t\t\t</div>\n{nav}\t\t\t\t\t\t\t</div>\n')


def chips(items):
    return ('<ul class="spec-chips">' + "".join(f'<li>{e(i)}</li>' for i in items) + '</ul>')


def card(m):
    params = "".join(
        f'\t\t\t\t\t\t\t\t<div class="greenhouses-card__param">\n'
        f'\t\t\t\t\t\t\t\t\t<div class="greenhouses-card__key">{e(k)}</div>\n'
        f'\t\t\t\t\t\t\t\t\t<div class="greenhouses-card__value">{e(v)}</div>\n'
        f'\t\t\t\t\t\t\t\t</div>\n' for k, v in params_of(m))
    note = f'<br><br><em>{e(m["note"])}</em>' if m["note"] else ""
    return f'''					<div class="greenhouses-card__item" id="{m["slug"]}">
						<div class="card__img greenhouses-card__img">
{swiper(m["photos"], m["slug"])}						</div>
						<div class="greenhouses-card__info">
							<h3 class="card-item__title greenhouse-card__title">{e(m["name"])}</h3>
							<div class="greenhouses-card__parameters">
{params}							</div>
							<div class="card__descr greenhouses-card__descr">
								<p>{e(m["text"])}{note}</p>
							</div>
							<div class="card-link__box greenhouses-link__box">
								<a href="#" data-popup-target="contacts" class="card-link">Get price</a>
							</div>
						</div>
					</div>
'''


def params_of(m):
    p = [("Width", m["width"]), ("Height", m["height"]), ("Lengths", m["lengths"])]
    if m["profile"] == "pine":
        p += [("Frame", "Impregnated Swedish pine"), ("Arch step", "1 m"),
              ("Polycarbonate", "4 mm")]
    else:
        p += [("Profile", m["profile"]), ("Arch step", STEP), ("Polycarbonate", POLY)]
    return p


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


def write_page(filename, title, description, main, body_class="catalog-greenhouse"):
    head = HEAD.replace("{{TITLE}}", e(title)).replace("{{DESCRIPTION}}", e(description))
    (ROOT / filename).write_text(head + main.replace("{{BODY_CLASS}}", body_class) + FOOT,
                                 encoding="utf-8")


def catalog_main(current, label, h2, intro, body, chip_items=None):
    return f'''	<main class="page-body {{{{BODY_CLASS}}}}">
		<div class="container">
			<div class="catalog-intro">
				<span class="catalog-intro__label">{e(label)}</span>
				<h2 class="advantages__title catalog-intro__title">{e(h2)}</h2>
				<p class="catalog-intro__text">{e(intro)}</p>
				{chips(chip_items) if chip_items else ""}
			</div>
			<div class="greenhouses-box">
{aside(current)}				<div class="greenhouses-cards__wrapper">
{body}				</div>
			</div>
		</div>
	</main>
'''


def model_tile(m, link=True):
    rng = RANGES[m["range"]]
    spec = f'{m["width"]} × {m["height"]} · {m["profile"] if m["profile"] != "pine" else "pine"}'
    href = f'/{rng["page"]}#{m["slug"]}' if link else "#"
    return f'''						<li class="model-grid__item">
							<a href="{href}">
								<img src="{IMG}{m["slug"]}.jpg" alt="{e(m["name"])}" loading="lazy">
								<span class="model-grid__name">{e(m["name"])}</span>
								<span class="model-grid__spec">{e(spec)}</span>
							</a>
						</li>
'''

# ------------------------------------------------------------------ range pages


def range_page(key):
    r = RANGES[key]
    models = [m for m in MODELS if m["range"] == key]
    body = ""
    # family sections (metal) or plain list (wooden)
    fams = list(dict.fromkeys(m["family"] for m in models))  # keep MODELS order
    for f in fams:
        fm = [m for m in models if m["family"] == f]
        if key != "casa":
            body += (f'\t\t\t\t\t<div class="family-head" id="{f.lower().replace(" ", "-")}">\n'
                     f'\t\t\t\t\t\t<h3 class="family-head__name">{e(f)}</h3>\n'
                     f'\t\t\t\t\t\t<p class="family-head__text">{e(FAMILIES[f])}</p>\n'
                     f'\t\t\t\t\t</div>\n')
        body += "".join(card(m) for m in fm)
    if key in REAL_PHOTOS:
        body += f'''					<section class="real-photos">
						<h3 class="card-item__title greenhouse-card__title">From our production and customers' gardens</h3>
						<div class="card__img greenhouses-card__img real-photos__img">
{swiper(REAL_PHOTOS[key], "real-" + key, "img/cat/")}						</div>
					</section>
'''
    body += f'''					<div class="range-foot">
						<p>Not sure which form or width fits your plot? Tell us the site and the crops — we will suggest a kit.</p>
						<div class="card-link__box greenhouses-link__box">
							<a href="#" data-popup-target="contacts" class="card-link">Get price</a>
						</div>
					</div>
'''
    write_page(r["page"], f'{r["name"]} — GrowUp Greenhouses catalogue 2027', r["intro"],
               catalog_main(r["page"], f'Catalogue 2027 · {r["code"]} {r["short"]}', r["h2"],
                            r["intro"], body, r["chips"]))

# -------------------------------------------------------------------- hub page


def hub_page():
    ranges = "".join(f'''						<li class="range-card">
							<a href="/{r["page"]}" class="range-card__link">
								<img src="{IMG}{r["hero"]}.jpg" alt="{e(r["name"])}" loading="lazy">
								<span class="range-card__code">{r["code"]} · {e(r["short"])}</span>
								<span class="range-card__name">{e(r["h2"])}</span>
								<span class="range-card__summary">{e(r["summary"])}</span>
							</a>
						</li>
''' for r in RANGES.values())
    ranges += f'''						<li class="range-card">
							<a href="/catalog-addons.html" class="range-card__link">
								<img src="{IMG}roof-window.jpg" alt="Roof windows and add-ons" loading="lazy">
								<span class="range-card__code">04 · Add-ons</span>
								<span class="range-card__name">Roof windows and accessories</span>
								<span class="range-card__summary">windows for every width · auto-opener · tapes</span>
							</a>
						</li>
'''
    grid = ""
    for key, r in RANGES.items():
        grid += (f'\t\t\t\t\t<h3 class="card-item__title model-grid__title">'
                 f'<a href="/{r["page"]}">{r["code"]} · {e(r["name"])}</a></h3>\n'
                 f'\t\t\t\t\t<ul class="model-grid">\n'
                 + "".join(model_tile(m) for m in MODELS if m["range"] == key)
                 + '\t\t\t\t\t</ul>\n')
    rows = "".join(
        f'\t\t\t\t\t\t\t\t<tr><td><a href="/{RANGES[m["range"]]["page"]}#{m["slug"]}">{e(m["name"])}</a></td>'
        f'<td>{e(RANGES[m["range"]]["short"])}</td><td>{e(m["width"])}</td><td>{e(m["height"])}</td>'
        f'<td>{e(m["profile"] if m["profile"] != "pine" else "Pine")}</td>'
        f'<td>{e("2 – 6 m" if m["range"] == "casa" else "2 – 14 m, +2 m")}</td>'
        f'<td>{e(RANGES[m["range"]]["delivery"])}</td></tr>\n' for m in MODELS)
    choose = "".join(f'''						<li class="choose-grid__item">
							<span class="choose-grid__letter">{l}</span>
							<span class="choose-grid__name">{e(n)}</span>
							<span class="choose-grid__text">{e(t)}</span>
						</li>
''' for l, n, t in HOW_TO_CHOOSE)
    body = f'''					<ul class="range-cards">
{ranges}					</ul>
					<section class="hub-section">
						<h3 class="card-item__title greenhouse-card__title">Three ranges. Four decisions.</h3>
						<p class="hub-section__text">Every greenhouse in the catalogue is defined by the same four choices — pick the range first, then tune the frame to your climate and the glazing to your crops.</p>
						<ul class="choose-grid">
{choose}						</ul>
					</section>
					<section class="hub-section">
{grid}					</section>
					<section class="hub-section">
						<h3 class="card-item__title greenhouse-card__title">All models at a glance</h3>
						<div class="table-scroll">
							<table class="addons-table compare-table">
								<thead><tr><th>Model</th><th>Range</th><th>Width</th><th>Height</th><th>Profile</th><th>Lengths</th><th>Delivery</th></tr></thead>
								<tbody>
{rows}								</tbody>
							</table>
						</div>
						<p class="hub-section__note">Metal ranges: arch step 1 m or 0,67 m, polycarbonate 4 or 6 mm, galvanized steel. Wooden CASA: arch step 1 m, polycarbonate 4 mm, height 2,32 m. All dimensions in metres.</p>
						<div class="card-link__box greenhouses-link__box">
							<a href="#" data-popup-target="contacts" class="card-link">Get price list</a>
						</div>
					</section>
'''
    write_page("catalog.html", "Greenhouse catalogue 2027 — GrowUp Greenhouses",
               "Wooden CASA, metal modular M and metal solid S greenhouses, roof windows and "
               "accessories. 15 models from 1,8 to 4 m wide, produced near Warsaw.",
               catalog_main("catalog.html", "Greenhouse catalogue 2027", "Room to grow, season after season",
                            "Three ranges, one standard of care — timber, one-piece steel and modular "
                            "steel greenhouses, each delivered as a complete kit.", body))

# ------------------------------------------------------------------ add-ons page


def addons_page():
    rows = "".join(
        f'\t\t\t\t\t\t\t\t\t\t<tr><td>{w} · {kind}</td><td>●</td><td>{"●" if r else "—"}</td></tr>\n'
        for w, kind, r in WINDOWS)
    acc = "".join(f'''						<li class="addons-grid__item">
							<a href="{IMG}{s}_b.jpg" data-fancybox="addons"><img src="{IMG}{s}.jpg" alt="{e(n)}" loading="lazy"></a>
							<span class="addons-grid__name">{e(n)}</span>
							<span class="addons-grid__spec">{e(spec)}</span>
						</li>
''' for n, spec, s in ACCESSORIES)
    body = f'''					<section class="addons-block">
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
    write_page("catalog-addons.html", "Roof windows and accessories — GrowUp Greenhouses catalogue 2027",
               "Roof windows sized to every greenhouse width and arch step, auto-opener, "
               "polycarbonate tapes, U-profile and growing accessories.",
               catalog_main("catalog-addons.html", "Catalogue 2027 · 04 Add-ons", "Add-ons",
                            "Roof windows sized to every greenhouse width and arch step, plus finishing "
                            "and growing accessories.", body))

# ------------------------------------------------------------- index + headers


def index_block():
    ranges = "".join(f'''					<li class="range-card">
						<a href="/{r["page"]}" class="range-card__link">
							<img src="{IMG}{r["hero"]}.jpg" alt="{e(r["name"])}" loading="lazy">
							<span class="range-card__code">{r["code"]} · {e(r["short"])}</span>
							<span class="range-card__name">{e(r["h2"])}</span>
							<span class="range-card__summary">{e(r["summary"])}</span>
						</a>
					</li>
''' for r in RANGES.values())
    ranges += '''					<li class="range-card">
						<a href="/catalog-gardenbeds.html" class="range-card__link">
							<img src="img/cat/card3-img2.jpg" alt="Garden beds" loading="lazy">
							<span class="range-card__code">Garden beds</span>
							<span class="range-card__name">Wooden garden beds</span>
							<span class="range-card__summary">impregnated Swedish pine · 28 mm board</span>
						</a>
					</li>
'''
    steps = "".join(f'''					<li class="order-steps__item">
						<span class="order-steps__num">0{i}</span>
						<span class="order-steps__name">{e(n)}</span>
						<span class="order-steps__text">{e(t)}</span>
					</li>
''' for i, (n, t) in enumerate(HOW_TO_ORDER, 1))
    return f'''			<div class="home-catalog"> <!-- КАТАЛОГ 2027 -->
				<h2 class="advantages__title">What we are producing:</h2>
				<p class="home-catalog__text">Greenhouse catalogue 2027 — three ranges, 15 models from 1,8 to 4 m wide, roof windows and accessories. Every greenhouse ships as a complete kit with fastenings and instructions.</p>
				<ul class="range-cards range-cards--home">
{ranges}				</ul>
				<p class="home-catalog__links"><a href="/catalog.html">All models and comparison table</a> · <a href="/catalog-addons.html">Roof windows &amp; add‑ons</a></p>
			</div>
			<div class="home-order"> <!-- КАК ЗАКАЗАТЬ -->
				<h2 class="advantages__title">From first message to first harvest:</h2>
				<ul class="order-steps">
{steps}				</ul>
				<div class="link-btn__box">
					<a href="#" data-popup-target="contacts" class="link__btn">Get price</a>
				</div>
			</div>
'''


def update_index():
    p = ROOT / "index.html"
    s = p.read_text(encoding="utf-8")
    if '<div class="home-catalog">' in s:          # re-run: replace our own block
        start = s.index('\t\t\t<div class="home-catalog">')
    else:                                            # first run: replace old slider card
        start = s.index('\t\t\t<div class="greenhouses-cards__wrapper">')
    end = s.rindex('\t\t</div>', 0, s.index('\t</main>'))
    s = s[:start] + index_block() + s[end:]
    s = s.replace('<a href="/catalog-greenhouses.html" class="link__btn main-link__btn">Watch catalogue</a>',
                  '<a href="/catalog.html" class="link__btn main-link__btn">Watch catalogue</a>')
    if 'css/catalog-2027.css' not in s:
        s = s.replace('<link rel="stylesheet" href="css/swiper-bundle.min.css">',
                      '<link rel="stylesheet" href="css/swiper-bundle.min.css">\n\t<link rel="stylesheet" href="css/catalog-2027.css">')
    p.write_text(s, encoding="utf-8")


MENU = '''<ul class="menu header__menu">
						<li class="menu__item"><a href="/catalog.html" class="menu__link">CATALOGUE</a></li>
						<li class="menu__item"><a href="#" data-popup-target="contacts" class="menu__link">GET PRICE</a></li>
						<li class="menu__item"><a href="/media.html" class="menu__link">MEDIA</a></li>
						<li class="menu__item"><a href="/contacts.html" class="menu__link">CONTACTS</a></li>
						<li class="menu__item"><a href="https://www.facebook.com/profile.php?id=144515878738514" target="_blank" class="menu__link">FACEBOOK</a></li>
						<li class="menu__item mail"><a href="mailto:sales@growupgh.com" class="menu__link mail">sales@growupgh.com</a></li>
						<li class="menu__item phone"><a href="tel:+48572094244" class="menu__link phone">+48 572 094 244</a></li>
						<li class="menu__item"><a href="#" class="menu__link dealer" data-popup-target="contacts">REQUEST PRICE</a></li>
					</ul>'''

REDIRECTS = {
    "story.html": "media.html",
    "garden-beds.html": "catalog-gardenbeds.html",
    "garden-pavilions.html": "catalog.html",
    "additional goods.html": "catalog-addons.html",
}


def normalize_headers():
    for p in ROOT.glob("*.html"):
        if p.name in REDIRECTS:
            continue
        s = p.read_text(encoding="utf-8")
        s2 = re.sub(r'<ul class="menu header__menu">.*?</ul>', MENU, s, count=1, flags=re.S)
        s2 = s2.replace('<a href="/catalog-greenhouses.html" class="link__btn">Watch catalogue</a>',
                        '<a href="/catalog.html" class="link__btn">Watch catalogue</a>')
        if s2 != s:
            p.write_text(s2, encoding="utf-8")


def update_gardenbeds():
    p = ROOT / "catalog-gardenbeds.html"
    s = p.read_text(encoding="utf-8")
    s = re.sub(r'\t\t\t\t<aside class="aside">.*?</aside>\n', aside("catalog-gardenbeds.html"), s, count=1, flags=re.S)
    if 'css/catalog-2027.css' not in s:
        s = s.replace('<link rel="stylesheet" href="css/swiper-bundle.min.css">',
                      '<link rel="stylesheet" href="css/swiper-bundle.min.css">\n\t<link rel="stylesheet" href="css/catalog-2027.css">')
    p.write_text(s, encoding="utf-8")


def write_redirects():
    for src, dst in REDIRECTS.items():
        (ROOT / src).write_text(
            f'<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8">\n'
            f'<meta http-equiv="refresh" content="0; url=/{dst}">\n'
            f'<link rel="canonical" href="https://growupgh.com/{dst}">\n'
            f'<title>Redirecting…</title></head>\n'
            f'<body><a href="/{dst}">{dst}</a></body></html>\n', encoding="utf-8")


if __name__ == "__main__":
    for key in RANGES:
        range_page(key)
    hub_page()
    addons_page()
    update_index()
    update_gardenbeds()
    write_redirects()
    normalize_headers()
    print("built", len(MODELS), "models")
