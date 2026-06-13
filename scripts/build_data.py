import json, re, unicodedata
import openpyxl

SRC = "/sessions/gifted-bold-archimedes/mnt/uploads/Directorio_Pilates_Valencia_Investigacion-8f1de197.xlsx"
OUT = "/sessions/gifted-bold-archimedes/mnt/outputs/site/data/estudios.json"

def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    s = re.sub(r"-+", "-", s)
    return s

def clean(v):
    if v is None:
        return None
    if isinstance(v, str):
        v = v.strip()
        if v in ("", "No disponible", "No especificado", "No publicado - consultar",
                  "No publicado - consultar planes", " "):
            return None
        return v
    return v

NA_PRICE = {"No publicado - consultar", "No publicado - consultar planes", None}

def equip_class(equip):
    if not equip:
        return "mixto"
    e = equip.lower()
    has_reformer = "reformer" in e
    has_suelo = "suelo" in e or "mat" in e
    other_machines = any(k in e for k in ["cadillac", "torre", "barril", "chair", "wall",
                                           "springboard", "aparatos", "maquinas", "máquinas",
                                           "fitball", "pared"])
    if "todas las maquinas" in e or "todas las máquinas" in e:
        return "mixto"
    if has_reformer and (has_suelo or other_machines):
        return "mixto"
    if has_reformer and not has_suelo and not other_machines:
        return "reformer"
    if has_suelo and not has_reformer and not other_machines:
        return "suelo"
    if other_machines:
        return "mixto"
    return "mixto"

EQUIP_LABELS = {
    "reformer": "Solo Reformer",
    "suelo": "Mat / Suelo",
    "mixto": "Todas las máquinas",
}

def fisio_class(val):
    if not val:
        return None
    v = val.strip().lower()
    if v.startswith("sin"):
        return False
    if v.startswith("si") or v.startswith("sí"):
        return True
    if v.startswith("no"):
        return False
    return None

def english_class(val):
    if not val:
        return "desconocido"
    v = val.strip().lower()
    if v.startswith("no especificado") or v.startswith("no solo"):
        return "no" if "no solo" in v else "desconocido"
    if v.startswith("si") or v.startswith("sí"):
        return "si"
    if v.startswith("bajo"):
        return "consultar"
    return "desconocido"

def has_price(val):
    if not val:
        return False
    if val in NA_PRICE:
        return False
    return True

def to_float(val):
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    try:
        return float(str(val).replace(",", ".").strip())
    except ValueError:
        return None

def to_int_str(val):
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return str(int(val))
    return str(val).strip()

def main():
    wb = openpyxl.load_workbook(SRC, data_only=True)
    ws = wb["Estudios Pilates Valencia"]
    rows = list(ws.iter_rows(values_only=True))
    headers = rows[0]
    studios = []
    seen_slugs = {}
    for row in rows[1:]:
        nombre = clean(row[0])
        if not nombre:
            continue
        equip_raw = clean(row[6])
        servicios = clean(row[8])
        fisio = fisio_class(row[7] if isinstance(row[7], str) else (str(row[7]) if row[7] else None))
        equipo = equip_class(equip_raw)

        precio_suelta = clean(row[11])
        bono = clean(row[12])
        mensualidad = clean(row[13])

        tarifas_tags = []
        if has_price(precio_suelta):
            tarifas_tags.append("Sesión suelta")
        if has_price(bono):
            tarifas_tags.append("Bonos")
        if has_price(mensualidad):
            tarifas_tags.append("Mensualidad")

        slug = slugify(nombre)
        if slug in seen_slugs:
            seen_slugs[slug] += 1
            slug = f"{slug}-{seen_slugs[slug]}"
        else:
            seen_slugs[slug] = 1

        telefono = row[4]
        if isinstance(telefono, (int, float)):
            telefono = str(int(telefono))
        telefono = clean(telefono)

        studio = {
            "slug": slug,
            "nombre": nombre,
            "zona": clean(row[1]),
            "municipio": clean(row[2]) or "Valencia",
            "direccion": clean(row[3]),
            "telefono": telefono,
            "web": clean(row[5]),
            "equipamiento_raw": equip_raw,
            "equipamiento_tipo": equipo,
            "equipamiento_label": EQUIP_LABELS[equipo],
            "fisioterapia": fisio,
            "servicios": servicios,
            "niveles": clean(row[9]),
            "ingles": english_class(row[10] if isinstance(row[10], str) else None),
            "precio_suelta": precio_suelta,
            "bono": bono,
            "mensualidad": mensualidad,
            "tarifas_tags": tarifas_tags,
            "horario": clean(row[14]).replace("\n", " / ").replace("\t", " ") if clean(row[14]) else None,
            "rating": to_float(row[15]) if clean(row[15]) else None,
            "resenas": to_int_str(clean(row[16])),
            "notas": clean(row[17]),
        }
        studios.append(studio)

    studios.sort(key=lambda s: (s["municipio"] != "Valencia", s["nombre"]))

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(studios, f, ensure_ascii=False, indent=2)

    print(f"{len(studios)} estudios escritos en {OUT}")
    for s in studios:
        print(f"- {s['nombre']} -> {s['slug']} | {s['equipamiento_label']} | fisio={s['fisioterapia']} | tarifas={s['tarifas_tags']}")

if __name__ == "__main__":
    main()
