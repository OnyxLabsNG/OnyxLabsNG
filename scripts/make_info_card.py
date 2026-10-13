"""
Onyx Labs -- painel estilo neofetch com quem somos, serviços e stack.

Build a neofetch-style info card SVG (Andrew6rant style) to sit to the RIGHT of
the ASCII portrait: colored key/value rows for work experience, tech stack, and
highlights -- NOT GitHub stats (the contribution graph covers those).

Static content, hand-authored below. Lines fade/slide in on a short stagger so
it feels like the panel is printing alongside the portrait. STATIC=1 emits the
frozen state for Quick Look previews.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 480, 432
PAD = 20
TITLEBAR_H = 30
KEY_X = PAD
VAL_X = PAD + 92
LINE_H = 20.5

# paleta Onyx Labs: ônix/grafite/prata + ciano só como acento
BG = "#0B0B0D"
BG2 = "#17181C"
FRAME = "#3A3D44"
MUTED = "#6B6F77"
INK = "#E3E5E8"
KEY = "#A9ADB5"      # chaves em prata
SECTION = "#5EC8F2"  # títulos de seção em ciano
GREEN = "#F4F5F7"    # (nome herdado) cor do usuário no cabeçalho e dos marcadores
ACCENT = "#5EC8F2"

# ===========================================================================
#  EDITE AQUI -- o painel se reorganiza sozinho; se ficar alto demais, aumente
#  H acima (e o width= no README do perfil).
#
#  tipos de linha:
#    ("host",)              -> cabeçalho "onyx@github" + linha
#    ("kv", chave, valor)   -> chave prata + valor claro
#    ("sec", título)        -> "— título —" em ciano
#    ("bul", texto)         -> marcador + texto
#    ("gap",)               -> um respiro vertical
# ===========================================================================
HOST = "onyx"   # aparece como  onyx@github  no cabeçalho

ROWS = [
    ("host",),
    ("kv", "Empresa", "Onyx Labs · estúdio digital"),
    ("kv", "Foco", "Tecnologia para negócios locais e PMEs"),
    ("kv", "Base", "Alto Tietê · Grande SP"),
    ("kv", "Equipe", "3 sócios"),
    ("kv", "Contato", "onyxlabsng@gmail.com"),
    ("gap",),
    ("sec", "Serviços"),
    ("kv", "Web", "Sites · Landing pages · E-commerce"),
    ("kv", "Sistemas", "Sob medida · Automação (RPA)"),
    ("kv", "Mobile", "Apps iOS e Android"),
    ("gap",),
    ("sec", "Stack"),
    ("kv", "Front", "Astro, Tailwind CSS, JavaScript"),
    ("kv", "Back", "PHP, SQL, APIs REST"),
    ("kv", "Apps", "React Native, Expo"),
    ("kv", "Infra", "Linux, Proxmox, Cloudflare"),
    ("gap",),
    ("bul", "O ônix só mostra o brilho depois de lapidado."),
]


def esc(s):
    return html.escape(s)


def rise(inner, i):
    """fade + slight upward slide, staggered by row index; freezes visible."""
    if STATIC:
        return f"<g>{inner}</g>"
    delay = 0.15 + i * 0.06
    return (f'<g opacity="0" transform="translate(0,5)">{inner}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.4s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" '
            f'begin="{delay:.2f}s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>')


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>'
    f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
             f'text-anchor="middle">{esc(HOST)}@github: ~$ neofetch</text>')

y = TITLEBAR_H + 30
for i, row in enumerate(ROWS):
    kind = row[0]
    if kind == "gap":
        y += LINE_H * 0.5
        continue
    if kind == "host":
        host = esc(HOST)
        rule_x = KEY_X + (len(HOST) + 7) * 8 + 8
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" font-size="14" font-weight="700">'
                 f'<tspan fill="{GREEN}">{host}</tspan><tspan fill="{MUTED}">@</tspan>'
                 f'<tspan fill="{ACCENT}">github</tspan></text>'
                 f'<line x1="{rule_x}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
                 f'stroke="{FRAME}" stroke-opacity="0.8"/>')
    elif kind == "sec":
        title = esc(row[1])
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{SECTION}" font-size="12.5" font-weight="700">'
                 f'&#8212; {title}</text>'
                 f'<line x1="{KEY_X + 12 + len(row[1])*8}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
                 f'stroke="{FRAME}" stroke-opacity="0.8"/>')
    elif kind == "kv":
        key, val = esc(row[1]), esc(row[2])
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{KEY}" font-size="12.5" font-weight="700">{key}</text>'
                 f'<text x="{VAL_X}" y="{y:.1f}" fill="{INK}" font-size="12.5">{val}</text>')
    elif kind == "bul":
        txt = esc(row[1])
        inner = (f'<circle cx="{KEY_X+3}" cy="{y-4:.1f}" r="2.5" fill="{GREEN}"/>'
                 f'<text x="{KEY_X+14}" y="{y:.1f}" fill="{INK}" font-size="12.5">{txt}</text>')
    else:
        continue
    parts.append(rise(inner, i))
    y += LINE_H

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print("wrote", OUT, len(svg), "bytes;", W, "x", H, "content_bottom", round(y))
