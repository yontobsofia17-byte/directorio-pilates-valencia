# Directorio Pilates Valencia

Directorio SEO de estudios de pilates en Valencia ciudad y alrededores (Paterna, Torrent, L'Eliana, Aldaia...). Sitio estático (HTML/CSS/JS puro), generado a partir de `data/estudios.json`.

## Estructura

```
index.html          -> página principal (directorio con buscador y filtros)
estudios/*.html      -> ficha individual de cada estudio (37 fichas)
css/style.css        -> sistema de diseño (paleta coral/terracota)
data/estudios.json   -> datos de los 37 estudios (fuente de verdad)
templates/           -> plantillas Jinja2 usadas para generar las páginas
scripts/
  build_data.py       -> genera data/estudios.json a partir del Excel de investigación
  generate.py         -> genera index.html y estudios/*.html a partir de data/estudios.json
```

## Cómo actualizar el contenido

1. Edita `data/estudios.json` (añade/edita estudios, precios, horarios, reseñas, inglés, etc.)
2. Regenera el sitio:
   ```bash
   pip install jinja2
   python3 scripts/generate.py
   ```
3. Esto sobrescribe `index.html` y todos los archivos de `estudios/`.

Si tienes un Excel nuevo de investigación con la misma estructura de columnas, puedes regenerar `data/estudios.json` con:
```bash
python3 scripts/build_data.py
```
(ajusta la ruta `SRC` al inicio del script).

## Pendientes / próximos pasos

- Completar precios "consultar" llamando a los centros.
- Confirmar clases en inglés (solo The Reform Valencia lo confirma explícitamente hoy).
- Añadir página de Fisiobienestar como estudio destacado/ancla, con foto, equipo y CTA propio de la marca.
- Añadir mapa, fotos reales de cada estudio, y formulario de contacto/leads.
- Monetización: listados premium, leads, afiliados (ver briefing original del proyecto).

## Despliegue (GitHub + Vercel)

1. Crea un repo nuevo en GitHub (por ejemplo `directorio-pilates-valencia`) y sube este contenido:
   ```bash
   git remote add origin https://github.com/<tu-usuario>/directorio-pilates-valencia.git
   git branch -M main
   git push -u origin main
   ```
2. Entra en [vercel.com](https://vercel.com), pulsa "Add New Project", importa el repo de GitHub.
3. Vercel detecta que es un sitio estático automáticamente (no hace falta build command). Pulsa "Deploy".
4. En unos segundos tendrás una URL tipo `directorio-pilates-valencia.vercel.app`. Más adelante puedes conectar el dominio `pilatesvalencia.es` o `reformervalencia.es` desde Project Settings → Domains.
