import json, os, re, sys, shutil, datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "templates"))
from icons import ICONS
from jinja2 import Environment, FileSystemLoader

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATES = os.path.join(ROOT, "templates")
DATA = os.path.join(ROOT, "data", "estudios.json")
SITE_URL = "https://pilatesvalencia.es"

env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=False)

with open(DATA, encoding="utf-8") as f:
    studios = json.load(f)

# extraer numero de resenas para JSON-LD
def resenas_num(s):
    if not s.get("resenas"):
        return None
    m = re.search(r"\d+", str(s["resenas"]))
    return int(m.group()) if m else None

for s in studios:
    s["resenas_num"] = resenas_num(s)

municipios = sorted(set(s["municipio"] for s in studios))

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

year = datetime.date.today().year

# ---- Index ----
tpl = env.get_template("index.html")
html = tpl.render(
    title="Directorio de Estudios de Pilates en Valencia | Precios, Reformer, Fisioterapia",
    description="Encuentra el mejor estudio de pilates en Valencia y alrededores: reformer, suelo, fisioterapia, precios, horarios, niveles y clases en inglés. Comparativa actualizada de 37 centros.",
    canonical=f"{SITE_URL}/index.html",
    root="",
    active="home",
    icons=ICONS,
    studios=studios,
    municipios=municipios,
    year=year,
)
write("index.html", html)

# ---- Fichas de estudio ----
tpl = env.get_template("estudio.html")
for s in studios:
    desc_bits = [s["equipamiento_label"]]
    if s["fisioterapia"]:
        desc_bits.append("fisioterapia")
    if s["zona"]:
        desc_bits.append(f"en {s['zona']}, {s['municipio']}")
    else:
        desc_bits.append(f"en {s['municipio']}")
    description = f"{s['nombre']}: pilates {', '.join(desc_bits)}. Precios, horarios, niveles y contacto."

    html = tpl.render(
        title=f"{s['nombre']} | Pilates en {s['municipio']} - Directorio Pilates Valencia",
        description=description,
        canonical=f"{SITE_URL}/estudios/{s['slug']}.html",
        root="../",
        active="estudio",
        icons=ICONS,
        s=s,
        year=year,
    )
    write(f"estudios/{s['slug']}.html", html)

print(f"Generadas {len(studios)+1} páginas ({len(studios)} fichas + index).")
