"""
Gera a imagem-fonte (source-logo.png, escala de cinza) que o make_ascii_svg.py
converte no "retrato" ASCII da Onyx Labs: a gema hexagonal facetada da marca +
o wordmark ONYX LABS.

Convenção da imagem-fonte (herdada do template): PRETO = denso (caractere
cheio, aparece claro na tela) e BRANCO = vazio (fundo). Por isso aqui cada
faceta recebe um "brilho na tela" b (0..1) e é pintada com luminância 1 - b.

Uso:
    python scripts/make_logo_source.py                 # gema desenhada + wordmark
    python scripts/make_logo_source.py logo.png        # usa o logo oficial (PNG)

Com o logo oficial (prata sobre fundo preto, como no Instagram) a imagem é
invertida automaticamente; se o seu PNG for escuro sobre fundo claro, passe
--no-invert.
"""
import math
import os
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "source-logo.png")

SIZE = 1000                     # quadrado: 100x53 células de 8x15 px ~ 800x795
WORDMARK = "ONYX LABS"
WORDMARK_TRACKING = 0.10        # espaçamento entre letras (fração da altura)
FONT_CANDIDATES = [
    os.path.join(HERE, "..", "assets", "Sora-Bold.ttf"),       # se você colocar a Sora aqui
    "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]

# brilho de cada faceta na tela (luz vindo de cima/esquerda) -- "do bruto ao lapidado"
FACET_BRIGHTNESS = {
    "table": 0.50,   # mesa (hexágono interno)
    0: 0.92,         # faceta superior-esquerda
    1: 0.78,         # superior
    2: 0.58,         # superior-direita
    3: 0.30,         # inferior-direita
    4: 0.40,         # inferior
    5: 0.70,         # inferior-esquerda
}
GRADIENT = 0.12      # variação de brilho dentro de cada faceta (dá textura ao ASCII)
EDGE = 22            # largura (px) das arestas vazias entre facetas


def font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def hexagon(cx, cy, r, rot=-90):
    # rot=-90 -> vértice para cima (hexágono "em pé", como o logo)
    return [(cx + r * math.cos(math.radians(rot + 60 * i)),
             cy + r * math.sin(math.radians(rot + 60 * i))) for i in range(6)]


def shade_layer(poly, base, light=(-0.6, -0.8)):
    """máscara do polígono preenchida com um gradiente linear na direção da luz."""
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).polygon(poly, fill=255)
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    grad = Image.new("L", (SIZE, SIZE), 0)
    gpx = grad.load()
    lx, ly = light
    for y in range(int(y0), int(y1) + 1):
        for x in range(int(x0), int(x1) + 1):
            u = ((x - x0) / max(1, x1 - x0) - 0.5) * lx + ((y - y0) / max(1, y1 - y0) - 0.5) * ly
            b = max(0.0, min(1.0, base + GRADIENT * u))
            gpx[x, y] = int(255 * b)
    return ImageChops.multiply(grad, mask)


def draw_gem(cx, cy, r):
    bright = Image.new("L", (SIZE, SIZE), 0)       # brilho na tela, 0..255
    outer = hexagon(cx, cy, r)
    inner = hexagon(cx, cy, r * 0.50)
    for i in range(6):
        facet = [outer[i], outer[(i + 1) % 6], inner[(i + 1) % 6], inner[i]]
        bright = ImageChops.lighter(bright, shade_layer(facet, FACET_BRIGHTNESS[i]))
    bright = ImageChops.lighter(bright, shade_layer(inner, FACET_BRIGHTNESS["table"]))

    # arestas vazias separando as facetas (deixa a lapidação legível no ASCII)
    d = ImageDraw.Draw(bright)
    for i in range(6):
        d.line([outer[i], inner[i]], fill=0, width=EDGE)
    d.polygon(inner, outline=0, width=EDGE)
    return bright


def draw_wordmark(img, text, top, max_w):
    size = 200
    while size > 20:
        f = font(size)
        track = int(size * WORDMARK_TRACKING)
        widths = [f.getbbox(ch)[2] - f.getbbox(ch)[0] if ch != " " else size * 0.35 for ch in text]
        total = sum(widths) + track * (len(text) - 1)
        if total <= max_w:
            break
        size -= 4
    d = ImageDraw.Draw(img)
    x = (SIZE - total) / 2
    for ch, w in zip(text, widths):
        if ch != " ":
            bb = f.getbbox(ch)
            d.text((x - bb[0], top - bb[1]), ch, font=f, fill=250)
        x += w + track
    return size


def from_official_logo(path, invert=True):
    im = Image.open(path).convert("L")
    if invert:
        im = ImageOps.invert(im)
    im = ImageOps.pad(im, (SIZE, SIZE), color=255)
    return im


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        out = from_official_logo(args[0], invert="--no-invert" not in sys.argv)
    else:
        bright = draw_gem(SIZE / 2, SIZE * 0.35, SIZE * 0.31)
        draw_wordmark(bright, WORDMARK, int(SIZE * 0.715), int(SIZE * 0.92))
        out = ImageOps.invert(bright)                # brilho -> convenção do template
    out.save(OUT)
    print("wrote", OUT)
