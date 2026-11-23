"""Genera los SVG animados del perfil Jesa198707.

Uso:
    python render_svgs.py <carpeta_salida> [--only stats] [--stats <stats.json>]
"""
import argparse, os, sys

_ap = argparse.ArgumentParser()
_ap.add_argument("out")
_ap.add_argument("--only", nargs="*", help="hero stack architecture stats")
_ap.add_argument("--stats", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "stats.json"))
ARGS = _ap.parse_args()
OUT = ARGS.out

BG, PANEL, LINE = "#141321", "#1C1A2E", "#2E2A47"
FG, MUTED = "#FFF6EC", "#9A92B8"
# Tema "radical" + atardecer. CYAN = texto radical, VIOLET = amarillo, MAGENTA = rosa, GREEN = naranja
CYAN, VIOLET, MAGENTA, GREEN, RED = "#A9FEF7", "#F8D847", "#FE428E", "#FF8A4C", "#FF4D6D"
YELLOW, PINK, ORANGE, NIGHT = VIOLET, MAGENTA, GREEN, "#1B1030"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

STYLE = f"""<style>
    .sans {{ font-family: {SANS}; }}
    .mono {{ font-family: {MONO}; }}
  </style>"""

GLOW = """<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow-strong" x="-20%" y="-50%" width="140%" height="200%">
      <feGaussianBlur stdDeviation="10" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>"""

GRID = f"""<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0 L0 0 0 40" fill="none" stroke="#1D1B30" stroke-width="1"/>
    </pattern>"""


def head(w, h, title, desc, defs=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{desc}</desc>
  {STYLE}
  <defs>
    {GLOW}
    {GRID}
    <clipPath id="frame"><rect width="{w}" height="{h}" rx="24"/></clipPath>
    {defs}
  </defs>
  <g clip-path="url(#frame)">
  <rect width="{w}" height="{h}" fill="{BG}"/>
  <rect width="{w}" height="{h}" fill="url(#grid)"/>
"""


def foot(w, h):
    return f"""  </g>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="24" fill="none" stroke="{LINE}"/>
</svg>
"""


def packet(path_id, color, dur, begin, r=4):
    return (f'<circle r="{r}" fill="{color}" filter="url(#glow)">'
            f'<animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" rotate="auto">'
            f'<mpath xlink:href="#{path_id}"/></animateMotion></circle>')


def pulse(cx, cy, r0, r1, color, dur, begin=0):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r0}" fill="none" stroke="{color}" stroke-width="2">'
            f'<animate attributeName="r" values="{r0};{r1}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.9;0" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
            f'</circle>')


# ---------------------------------------------------------------- hero
def hero():
    W, H = 1200, 470
    defs = f"""<linearGradient id="name-grad" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="640" y2="0" spreadMethod="repeat">
      <stop offset="0" stop-color="{FG}"/>
      <stop offset="0.33" stop-color="{YELLOW}"/>
      <stop offset="0.66" stop-color="{ORANGE}"/>
      <stop offset="1" stop-color="{FG}"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="0 0;640 0" dur="6s" repeatCount="indefinite"/>
    </linearGradient>
    <radialGradient id="aura" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{VIOLET}" stop-opacity="0.35"/>
      <stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="aura2" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{CYAN}" stop-opacity="0.18"/>
      <stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="fade" x1="0" x2="1">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset="0.08" stop-color="#fff" stop-opacity="1"/>
      <stop offset="0.92" stop-color="#fff" stop-opacity="1"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <mask id="ticker-mask"><rect x="0" y="400" width="{W}" height="70" fill="url(#fade)"/></mask>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{NIGHT}"/>
      <stop offset="0.35" stop-color="#3D1C4F"/>
      <stop offset="0.62" stop-color="#8A2E5B"/>
      <stop offset="0.80" stop-color="#D9534F"/>
      <stop offset="0.95" stop-color="#F79A4A"/>
    </linearGradient>
    <radialGradient id="sun" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#FFF0B8"/>
      <stop offset="0.7" stop-color="#FFC56B"/>
      <stop offset="1" stop-color="#FF9F4A"/>
    </radialGradient>
    <radialGradient id="sun-halo" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#FFC56B" stop-opacity="0.55"/>
      <stop offset="1" stop-color="#FFC56B" stop-opacity="0"/>
    </radialGradient>"""
    s = head(W, H, "Jesa — Desarrollo multiplataforma, sistemas Linux y ciberseguridad",
             "Cabecera animada: el nombre JESA con un degradado neón en movimiento, una terminal que escribe "
             "los roles Desarrollador DAM, Linux, Docker y Nginx, Ciberseguridad y VPNs, y Java, Python y Node.js. "
             "A la derecha, una red en vivo: un equipo de desarrollo conectado por un túnel WireGuard a un VPS "
             "con Nginx, Docker y Samba. Abajo, una cinta con el stack tecnológico.", defs)

    # cielo de atardecer
    s += f'  <rect width="{W}" height="404" fill="url(#sky)"/>\n'
    # estrellas que titilan
    for i, (sx, sy) in enumerate([(140, 90), (260, 60), (420, 110), (520, 70), (640, 40), (760, 95),
                                  (880, 55), (1010, 85), (1130, 50), (340, 150), (600, 140), (980, 160)]):
        s += (f'  <circle cx="{sx}" cy="{sy}" r="{1.6 if i % 3 else 2.2}" fill="{FG}" opacity="0.7">'
              f'<animate attributeName="opacity" values="0.15;0.9;0.15" dur="{2.2 + (i % 4) * 0.7:.1f}s" '
              f'begin="-{i * 0.37:.2f}s" repeatCount="indefinite"/></circle>\n')
    # sol con halo que respira
    s += (f'  <circle cx="590" cy="318" r="150" fill="url(#sun-halo)">'
          f'<animate attributeName="r" values="140;170;140" dur="6s" repeatCount="indefinite"/></circle>\n')
    s += f'  <circle cx="590" cy="318" r="66" fill="url(#sun)"/>\n'
    # cordilleras en capas
    s += ('  <path d="M0 300 L120 255 L230 290 L340 240 L460 285 L560 252 L680 292 L800 245 L930 280 '
          'L1040 238 L1200 285 V404 H0 Z" fill="#7A2B57"/>\n')
    s += ('  <path d="M0 338 L90 312 L200 342 L310 302 L430 346 L560 318 L690 352 L820 312 L950 346 '
          'L1080 306 L1200 336 V404 H0 Z" fill="#4A1C45"/>\n')
    import math
    near = lambda x: 372 - 22 * math.sin(x / 1200 * 2 * math.pi * 1.5)
    pts = " ".join(f"L{x} {near(x):.0f}" for x in range(0, 1201, 40))
    tp = ""
    for x, h in [(30, 58), (70, 40), (118, 70), (180, 46), (330, 52), (372, 34), (760, 44), (800, 66),
                 (850, 38), (1120, 62), (1160, 44)]:
        y = near(x) + 4
        tp += f"M{x} {y-h:.0f} L{x+h*0.3:.0f} {y:.0f} L{x-h*0.3:.0f} {y:.0f} Z "
    s += f'  <path d="M0 404 {pts} V404 Z {tp}" fill="#22112E"/>\n'

    # status bar
    s += f"""  <g class="mono" font-size="16">
    <circle cx="62" cy="48" r="6" fill="{GREEN}"><animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/></circle>
    {pulse(62, 48, 6, 16, GREEN, 1.6)}
    <text x="80" y="54" fill="{GREEN}" font-weight="700" letter-spacing="2">ONLINE</text>
    <text x="164" y="54" fill="{MUTED}">jesa@secure-shell · tty1 · cifrado extremo a extremo</text>
  </g>
"""
    s += f'  <text x="60" y="128" class="mono" font-size="22" fill="{YELLOW}">&gt; whoami</text>\n'
    # nombre con sombra dura
    s += (f'  <text x="59" y="259" class="sans" font-size="150" font-weight="800" letter-spacing="6" '
          f'fill="{NIGHT}" opacity="0.8">JESA</text>\n')
    s += (f'  <text x="52" y="252" class="sans" font-size="150" font-weight="800" letter-spacing="6" '
          f'fill="url(#name-grad)">JESA</text>\n')
    # fondo de la línea de terminal para que se lea sobre el cielo
    s += f'  <rect x="44" y="276" width="500" height="52" rx="10" fill="{NIGHT}" opacity="0.65"/>\n'

    # typing roles
    roles = ["Desarrollador DAM", "Linux · Docker · Nginx", "Ciberseguridad & VPNs", "Java · Python · Node.js"]
    CW, X0, Y = 18, 98, 314
    CYCLE = 16.0
    slot = CYCLE / len(roles)
    t_type, t_hold, t_del = 1.7, 1.5, 0.6
    clip_defs, texts = "", ""
    cursor_tl = []  # (t, x)
    for i, role in enumerate(roles):
        n = len(role)
        start = i * slot
        tl = [(0.0, 0)]
        for k in range(n + 1):
            tl.append((start + t_type * k / n, k * CW))
        hold_end = start + t_type + t_hold
        for k in range(n, -1, -1):
            tl.append((hold_end + t_del * (n - k) / n, k * CW))
        tl.append((CYCLE, 0))
        # dedupe, keep monotone times
        clean = []
        for t, v in tl:
            t = round(t, 4)
            if clean and t <= clean[-1][0]:
                clean[-1] = (clean[-1][0], v) if t == clean[-1][0] else clean[-1]
                continue
            clean.append((t, v))
        kt = ";".join(f"{t/CYCLE:.4f}" for t, _ in clean)
        vals = ";".join(str(v) for _, v in clean)
        clip_defs += (f'<clipPath id="role{i}"><rect x="{X0}" y="{Y-32}" width="0" height="44">'
                      f'<animate attributeName="width" values="{vals}" keyTimes="{kt}" dur="{CYCLE}s" '
                      f'calcMode="discrete" repeatCount="indefinite"/></rect></clipPath>')
        texts += (f'<text x="{X0}" y="{Y}" class="mono" font-size="30" fill="{FG}" textLength="{n*CW}" '
                  f'lengthAdjust="spacingAndGlyphs" clip-path="url(#role{i})">{role.replace("&", "&amp;")}</text>\n  ')
        cursor_tl += [(t, X0 + v) for t, v in clean if start - 0.01 <= t <= start + slot - 0.01]
    cursor_tl.sort()
    if cursor_tl[0][0] > 0:
        cursor_tl.insert(0, (0.0, X0))
    cursor_tl.append((CYCLE, X0))
    ck, cv = [], []
    for t, x in cursor_tl:
        if ck and round(t / CYCLE, 4) <= float(ck[-1]):
            cv[-1] = str(x)
            continue
        ck.append(f"{t/CYCLE:.4f}")
        cv.append(str(x))
    s += f"  <defs>{clip_defs}</defs>\n"
    s += f'  <text x="60" y="{Y}" class="mono" font-size="30" fill="{MAGENTA}">$</text>\n'
    s += "  " + texts + "\n"
    s += (f'  <rect x="{X0}" y="{Y-28}" width="15" height="34" fill="{CYAN}" filter="url(#glow)">'
          f'<animate attributeName="x" values="{";".join(cv)}" keyTimes="{";".join(ck)}" dur="{CYCLE}s" calcMode="discrete" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="1;0.15" dur="0.9s" calcMode="discrete" repeatCount="indefinite"/></rect>\n')
    s += (f'  <text x="60" y="362" class="sans" font-size="21" fill="{FG}">'
          f'Desarrollo multiplataforma · Sistemas Linux · Ciberseguridad</text>\n')

    # live network
    N = {"DEV": (700, 240), "WG": (835, 240), "VPS": (975, 240),
         "NGINX": (1090, 130), "DOCKER": (1112, 240), "SAMBA": (1090, 350)}
    s += '  <g id="network">\n'
    s += '  <defs>\n'
    s += f'    <path id="e-dev-wg" d="M{N["DEV"][0]+22} 240 L{N["WG"][0]-24} 240"/>\n'
    s += f'    <path id="e-wg-vps" d="M{N["WG"][0]+24} 240 L{N["VPS"][0]-36} 240"/>\n'
    s += f'    <path id="e-vps-ng" d="M995 214 Q 1030 140 {N["NGINX"][0]-20} 136"/>\n'
    s += f'    <path id="e-vps-dk" d="M1011 240 L{N["DOCKER"][0]-20} 240"/>\n'
    s += f'    <path id="e-vps-sb" d="M995 266 Q 1030 340 {N["SAMBA"][0]-20} 344"/>\n'
    s += '  </defs>\n'
    for e, col in [("e-vps-ng", CYAN), ("e-vps-dk", CYAN), ("e-vps-sb", CYAN)]:
        s += f'  <use xlink:href="#{e}" stroke="{col}" stroke-opacity="0.35" stroke-width="2" fill="none"/>\n'
    # tunnel: flowing dashes
    for e in ["e-dev-wg", "e-wg-vps"]:
        s += f'  <use xlink:href="#{e}" stroke="{MAGENTA}" stroke-opacity="0.25" stroke-width="8" fill="none"/>\n'
        s += (f'  <use xlink:href="#{e}" stroke="{MAGENTA}" stroke-width="2.5" fill="none" stroke-dasharray="8 8">'
              f'<animate attributeName="stroke-dashoffset" values="32;0" dur="0.8s" repeatCount="indefinite"/></use>\n')
    # packets
    for k in range(3):
        s += "  " + packet("e-dev-wg", MAGENTA, 1.2, -k * 0.4) + "\n"
        s += "  " + packet("e-wg-vps", MAGENTA, 1.2, -k * 0.4 - 0.2) + "\n"
    s += "  " + packet("e-vps-ng", CYAN, 1.6, 0) + "\n"
    s += "  " + packet("e-vps-ng", CYAN, 1.6, -0.8) + "\n"
    s += "  " + packet("e-vps-dk", CYAN, 1.1, -0.3) + "\n"
    s += "  " + packet("e-vps-sb", CYAN, 1.8, -0.5) + "\n"
    s += "  " + packet("e-vps-sb", CYAN, 1.8, -1.4) + "\n"
    # nodes
    vx, vy = N["VPS"]
    s += f'  <circle cx="{vx}" cy="{vy}" r="54" fill="none" stroke="{VIOLET}" stroke-width="1.5" stroke-dasharray="4 10">'
    s += f'<animateTransform attributeName="transform" type="rotate" values="0 {vx} {vy};360 {vx} {vy}" dur="12s" repeatCount="indefinite"/></circle>\n'
    s += "  " + pulse(vx, vy, 36, 70, VIOLET, 2.4) + "\n"
    s += f'  <circle cx="{vx}" cy="{vy}" r="36" fill="{PANEL}" stroke="{VIOLET}" stroke-width="2.5" filter="url(#glow)"/>\n'
    s += f'  <text x="{vx}" y="{vy+6}" class="mono" font-size="17" font-weight="700" fill="{FG}" text-anchor="middle">VPS</text>\n'
    wx, wy = N["WG"]
    s += "  " + pulse(wx, wy, 24, 46, MAGENTA, 1.8, -0.6) + "\n"
    s += f'  <circle cx="{wx}" cy="{wy}" r="24" fill="{PANEL}" stroke="{MAGENTA}" stroke-width="2.5" filter="url(#glow)"/>\n'
    # shield glyph
    s += (f'  <path d="M{wx} {wy-12} L{wx+10} {wy-8} L{wx+10} {wy} Q{wx+10} {wy+9} {wx} {wy+13} '
          f'Q{wx-10} {wy+9} {wx-10} {wy} L{wx-10} {wy-8} Z" fill="none" stroke="{MAGENTA}" stroke-width="2"/>\n')
    for name in ["DEV", "NGINX", "DOCKER", "SAMBA"]:
        x, y = N[name]
        s += f'  <circle cx="{x}" cy="{y}" r="20" fill="{PANEL}" stroke="{CYAN}" stroke-width="2"/>\n'
        s += (f'  <circle cx="{x}" cy="{y}" r="5" fill="{CYAN}"><animate attributeName="opacity" '
              f'values="1;0.3;1" dur="2s" begin="-{ord(name[1])%20/10}s" repeatCount="indefinite"/></circle>\n')
    labels = {"DEV": (700, 290, "middle"), "WG": (835, 296, "middle"), "VPS": (975, 322, "middle"),
              "NGINX": (1090, 92, "middle"), "DOCKER": (1112, 290, "middle"), "SAMBA": (1090, 400, "middle")}
    names = {"DEV": "dev", "WG": "wireguard", "VPS": "", "NGINX": "nginx", "DOCKER": "docker", "SAMBA": "samba"}
    for k, (x, y, a) in labels.items():
        if names[k]:
            col = YELLOW if k == "WG" else FG
            s += f'  <text x="{x}" y="{y}" class="mono" font-size="17" fill="{col}" text-anchor="{a}">{names[k]}</text>\n'
    s += '  </g>\n'

    # ticker
    items = ["Java", "Python", "C#", "SQL", "Node.js", "Express", "Linux", "Nginx", "Docker", "WireGuard", "Samba"]
    s += f'  <line x1="0" y1="404" x2="{W}" y2="404" stroke="{LINE}"/>\n'
    x, parts = 0, []
    for it in items:
        parts.append((x, it))
        x += len(it) * 13.5 + 70
    span = round(x)
    row = ""
    for off in (0, span):
        for px, it in parts:
            row += f'<text x="{px+off:.0f}" y="446" fill="{FG}">{it}</text>'
            row += f'<text x="{px+off+len(it)*13.5+29:.0f}" y="444" fill="{MAGENTA}" font-size="14">◆</text>'
    s += (f'  <g mask="url(#ticker-mask)"><g class="mono" font-size="22">{row}'
          f'<animateTransform attributeName="transform" type="translate" values="0 0;-{span} 0" dur="28s" repeatCount="indefinite"/>'
          f'</g></g>\n')
    s += foot(W, H)
    return s


# ---------------------------------------------------------------- stack
def stack():
    W, H = 1200, 400
    s = head(W, H, "Stack tecnológico",
             "Panel animado con cuatro columnas que se iluminan en ola. Lenguajes: Java, Python, C#, SQL. "
             "Backend y web: Node.js, Express, Nginx. Sistemas: Linux, Docker, Samba. "
             "Red y seguridad: WireGuard, TLS / HTTPS, bastionado.")
    s += f'  <text x="56" y="62" class="mono" font-size="22"><tspan fill="{CYAN}">&gt;</tspan><tspan fill="{FG}"> stack --list</tspan></text>\n'
    s += (f'  <text x="1144" y="62" class="mono" font-size="16" fill="{MUTED}" text-anchor="end">'
          f'<tspan fill="{GREEN}">●</tspan> 13 módulos cargados</text>\n')
    cols = [("LENGUAJES", CYAN, ["Java", "Python", "C#", "SQL"]),
            ("BACKEND · WEB", VIOLET, ["Node.js", "Express", "Nginx"]),
            ("SISTEMAS", GREEN, ["Linux", "Docker", "Samba"]),
            ("RED · SEGURIDAD", MAGENTA, ["WireGuard", "TLS / HTTPS", "Bastionado"])]
    CWID, GAP, X0 = 254, 24, 56
    idx = 0
    for c, (title, col, items) in enumerate(cols):
        x = X0 + c * (CWID + GAP)
        s += f'  <text x="{x}" y="118" class="mono" font-size="17" font-weight="700" letter-spacing="2" fill="{col}">{title}</text>\n'
        s += f'  <rect x="{x}" y="132" width="{CWID}" height="3" rx="1.5" fill="{col}" opacity="0.25"/>\n'
        s += (f'  <rect x="{x}" y="132" width="60" height="3" rx="1.5" fill="{col}" filter="url(#glow)">'
              f'<animate attributeName="x" values="{x};{x+CWID-60};{x}" dur="4s" begin="-{c*0.7}s" repeatCount="indefinite"/></rect>\n')
        for r, it in enumerate(items):
            y = 152 + r * 58
            d = idx * 0.25
            s += f'  <rect x="{x}" y="{y}" width="{CWID}" height="46" rx="10" fill="{PANEL}" stroke="{LINE}"/>\n'
            s += (f'  <rect x="{x}" y="{y}" width="{CWID}" height="46" rx="10" fill="{col}" fill-opacity="0.08" '
                  f'stroke="{col}" stroke-width="1.5" opacity="0" filter="url(#glow)">'
                  f'<animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;0.05;0.12;0.3;1" dur="5s" begin="{d}s" repeatCount="indefinite"/></rect>\n')
            s += f'  <circle cx="{x+22}" cy="{y+23}" r="5" fill="{col}"/>\n'
            s += f'  <text x="{x+40}" y="{y+31}" class="sans" font-size="23" font-weight="600" fill="{FG}">{it}</text>\n'
            idx += 1
    s += foot(W, H)
    return s


# ---------------------------------------------------------------- architecture
def architecture():
    W, H = 1200, 560
    s = head(W, H, "Arquitectura tipo de despliegue",
             "Diagrama animado. El tráfico de usuarios entra por HTTPS a Nginx y llega a la aplicación Node.js/Express. "
             "La administración viaja cifrada por un túnel WireGuard hasta Samba y SSH. "
             "Un escáner que intenta conectar al puerto 22 es bloqueado por el firewall y queda registrado en el log.")
    s += f'  <text x="56" y="62" class="mono" font-size="22"><tspan fill="{CYAN}">&gt;</tspan><tspan fill="{FG}"> trace --live despliegue</tspan></text>\n'

    def box(x, y, w, h, title, sub, col, sub_col=MUTED):
        return (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{PANEL}" stroke="{col}" stroke-width="1.8"/>\n'
                f'  <text x="{x+22}" y="{y+37}" class="sans" font-size="23" font-weight="700" fill="{FG}">{title}</text>\n'
                f'  <text x="{x+22}" y="{y+64}" class="mono" font-size="17" fill="{sub_col}">{sub}</text>\n')

    # VPS boundary + firewall
    s += f'  <rect x="480" y="100" width="672" height="420" rx="18" fill="{VIOLET}" fill-opacity="0.04" stroke="{VIOLET}" stroke-opacity="0.5" stroke-dasharray="6 6"/>\n'
    s += f'  <text x="508" y="132" class="mono" font-size="17" fill="{VIOLET}">VPS · Linux</text>\n'
    s += f'  <rect x="474" y="100" width="8" height="420" rx="4" fill="{RED}" opacity="0.55"/>\n'
    s += f'  <text x="478" y="92" class="mono" font-size="16" fill="{RED}" text-anchor="middle">firewall</text>\n'

    # left actors
    s += box(56, 140, 220, 84, "Usuario", "navegador · app", CYAN)
    s += box(56, 278, 220, 84, "Admin", "acceso remoto", MAGENTA)
    s += box(56, 416, 220, 84, "Escáner", "origen desconocido", RED, RED)

    # inside
    s += box(530, 150, 240, 84, "Nginx", "proxy · TLS", CYAN)
    s += box(840, 150, 280, 84, "Node.js / Express", "API + web · Docker", CYAN)
    s += box(530, 288, 240, 84, "wg0", "túnel cifrado", MAGENTA)
    s += box(840, 288, 280, 84, "Samba · SSH", "sin exposición pública", MAGENTA)

    # log panel
    s += f'  <rect x="530" y="420" width="590" height="70" rx="12" fill="#0A0F1C" stroke="{LINE}"/>\n'
    s += f'  <text x="552" y="452" class="mono" font-size="16" fill="{MUTED}">/var/log/firewall</text>\n'
    s += (f'  <text x="552" y="476" class="mono" font-size="17" fill="{RED}" opacity="0.35">'
          f'DROP  tcp/22  src=185.xxx.xxx.xxx  política: denegar'
          f'<animate attributeName="opacity" values="0.35;0.35;1;1;0.35" keyTimes="0;0.5;0.53;0.75;1" dur="3s" repeatCount="indefinite"/></text>\n')

    # paths
    s += f"""  <defs>
    <path id="a-u-ng" d="M276 182 L530 192"/>
    <path id="a-ng-app" d="M770 192 L840 192"/>
    <path id="a-ad-wg" d="M276 320 C 380 320, 420 330, 530 330"/>
    <path id="a-wg-sb" d="M770 330 L840 330"/>
    <path id="a-sc-fw" d="M276 458 L470 458"/>
  </defs>
"""
    for p in ["a-u-ng", "a-ng-app"]:
        s += f'  <use xlink:href="#{p}" stroke="{CYAN}" stroke-opacity="0.45" stroke-width="2" fill="none"/>\n'
    for p in ["a-ad-wg", "a-wg-sb"]:
        s += f'  <use xlink:href="#{p}" stroke="{MAGENTA}" stroke-opacity="0.22" stroke-width="10" fill="none"/>\n'
        s += (f'  <use xlink:href="#{p}" stroke="{MAGENTA}" stroke-width="2.5" fill="none" stroke-dasharray="8 8">'
              f'<animate attributeName="stroke-dashoffset" values="32;0" dur="0.8s" repeatCount="indefinite"/></use>\n')
    s += f'  <use xlink:href="#a-sc-fw" stroke="{RED}" stroke-opacity="0.35" stroke-width="2" fill="none" stroke-dasharray="3 7"/>\n'
    s += f'  <text x="300" y="172" class="mono" font-size="17" fill="{CYAN}">HTTPS :443</text>\n'
    s += f'  <text x="300" y="306" class="mono" font-size="17" fill="{MAGENTA}">WireGuard</text>\n'
    s += f'  <text x="300" y="358" class="mono" font-size="17" fill="{MAGENTA}" opacity="0.8">:51820/udp</text>\n'
    s += f'  <text x="300" y="446" class="mono" font-size="17" fill="{RED}">tcp :22</text>\n'

    for k in range(3):
        s += "  " + packet("a-u-ng", CYAN, 1.8, -k * 0.6) + "\n"
        s += "  " + packet("a-ad-wg", MAGENTA, 1.5, -k * 0.5) + "\n"
    s += "  " + packet("a-ng-app", CYAN, 0.6, 0) + "\n"
    s += "  " + packet("a-wg-sb", MAGENTA, 0.6, -0.3) + "\n"
    # attacker packet: travels in first half, then blocked
    s += (f'  <circle r="5" fill="{RED}" filter="url(#glow)">'
          f'<animateMotion dur="3s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;0.5;1" calcMode="linear">'
          f'<mpath xlink:href="#a-sc-fw"/></animateMotion>'
          f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="3s" repeatCount="indefinite"/></circle>\n')
    s += (f'  <circle cx="478" cy="458" r="6" fill="none" stroke="{RED}" stroke-width="3" opacity="0">'
          f'<animate attributeName="r" values="6;6;30;30" keyTimes="0;0.5;0.7;1" dur="3s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;0.5;0.52;0.7;1" dur="3s" repeatCount="indefinite"/></circle>\n')
    s += (f'  <g opacity="0" stroke="{RED}" stroke-width="4" stroke-linecap="round">'
          f'<line x1="440" y1="440" x2="456" y2="456"/><line x1="456" y1="440" x2="440" y2="456"/>'
          f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.5;0.52;0.8;1" dur="3s" repeatCount="indefinite"/></g>\n')
    s += (f'  <text x="448" y="500" class="mono" font-size="16" font-weight="700" fill="{RED}" text-anchor="middle" opacity="0">BLOCKED'
          f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.5;0.52;0.8;1" dur="3s" repeatCount="indefinite"/></text>\n')

    s += (f'  <text x="56" y="540" class="mono" font-size="16" fill="{MUTED}">'
          f'expuesto: <tspan fill="{CYAN}">443/tcp</tspan> · <tspan fill="{MAGENTA}">51820/udp</tspan>   ·   resto: <tspan fill="{RED}">DROP</tspan></text>\n')
    s += foot(W, H)
    return s


# ---------------------------------------------------------------- stats
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def fecha(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {MESES[int(m) - 1]} {y}"


def rango(a, b):
    if a == b:
        return fecha(a)
    ya, ma, da = a.split("-")
    yb, mb, db = b.split("-")
    if ya == yb and ma == mb:
        return f"{int(da)} – {fecha(b)}"
    return f"{fecha(a)} – {fecha(b)}"


def ring(cx, cy, r, color, dur=1.6):
    c = 2 * 3.14159 * r
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE}" stroke-width="7"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round" '
            f'stroke-dasharray="{c:.1f}" stroke-dashoffset="0" transform="rotate(-90 {cx} {cy})" filter="url(#glow)">'
            f'<animate attributeName="stroke-dashoffset" values="{c:.1f};0" dur="{dur}s" fill="freeze" '
            f'calcMode="spline" keySplines="0.3 0 0.2 1" keyTimes="0;1"/></circle>')


def fade_in(delay):
    k = delay / (delay + 0.6)
    return (f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;{k:.3f};1" dur="{delay + 0.6:.2f}s" fill="freeze"/>')


def stats():
    import json
    st = json.load(open(ARGS.stats, encoding="utf-8"))
    W, H = 1200, 340
    s = head(W, H, "Actividad en GitHub",
             f"Tarjeta de actividad. {st['total']} contribuciones y {st['commits']} commits desde "
             f"{fecha(st['first'])}, {st['repos']} repositorios ({st['private']} privados), "
             f"{st['active']} días con actividad. Racha actual: {st['current'][0]} días. "
             f"Racha más larga: {st['longest'][0]} días ({rango(st['longest'][1], st['longest'][2])}).")
    # dos paneles
    for x in (28, 612):
        s += f'  <rect x="{x}" y="28" width="560" height="284" rx="16" fill="{PANEL}" stroke="{LINE}"/>\n'

    # panel izquierdo: actividad
    s += f'  <text x="60" y="78" class="sans" font-size="24" font-weight="700" fill="{PINK}">Actividad en GitHub</text>\n'
    rows = [("Contribuciones", str(st["total"]), ""),
            ("Commits", str(st["commits"]), ""),
            ("Repositorios", str(st["repos"]), f"  ({st['private']} privados)"),
            ("Días con actividad", str(st["active"]), ""),
            ("En GitHub desde", f"{MESES[int(st['first'][5:7]) - 1]} {st['first'][:4]}", "")]
    for i, (lab, val, extra) in enumerate(rows):
        y = 124 + i * 40
        d = 0.15 + i * 0.12
        s += f'  <g>{fade_in(d)}\n'
        s += f'    <rect x="60" y="{y-14}" width="14" height="14" rx="3" fill="none" stroke="{YELLOW}" stroke-width="2.2"/>\n'
        s += f'    <text x="90" y="{y}" class="sans" font-size="19" font-weight="600" fill="{FG}">{lab}:</text>\n'
        s += (f'    <text x="282" y="{y}" class="sans" font-size="19" font-weight="700" fill="{CYAN}">{val}'
              f'<tspan fill="{MUTED}" font-weight="400" font-size="16">{extra}</tspan></text>\n  </g>\n')
    s += "  " + ring(488, 178, 58, PINK) + "\n"
    s += f'  <text x="488" y="186" class="sans" font-size="30" font-weight="800" fill="{FG}" text-anchor="middle">{st["commits"]}</text>\n'
    s += f'  <text x="488" y="210" class="mono" font-size="15" fill="{CYAN}" text-anchor="middle">commits</text>\n'

    # panel derecho: rachas
    cols = [(706, str(st["total"]), "Contribuciones", f"desde {fecha(st['first'])}", PINK, FG),
            (894, str(st["current"][0]), "Racha actual",
             fecha(st["current"][2]) if st["current"][0] else "—", FG, YELLOW),
            (1082, str(st["longest"][0]), "Racha más larga", rango(st["longest"][1], st["longest"][2]), PINK, FG)]
    s += f'  <line x1="800" y1="72" x2="800" y2="268" stroke="{LINE}"/>\n'
    s += f'  <line x1="988" y1="72" x2="988" y2="268" stroke="{LINE}"/>\n'
    for cx, num, lab, sub, ncol, lcol in cols:
        if cx == 894:
            s += "  " + ring(cx, 150, 52, ORANGE, 1.8) + "\n"
            # llama encima del anillo
            s += (f'  <rect x="{cx-16}" y="80" width="32" height="34" fill="{PANEL}"/>\n'
                  f'  <g transform="translate({cx} 98)"><path d="M0 -16 C 14 -2, 12 10, 0 14 C -12 10, -14 0, -4 -8 '
                  f'C -3 -1, 2 1, 0 -16 Z" fill="{ORANGE}" filter="url(#glow)">'
                  f'<animateTransform attributeName="transform" type="scale" values="1 1;1.08 0.94;0.95 1.06;1 1" '
                  f'dur="0.9s" repeatCount="indefinite"/>'
                  f'<animate attributeName="fill" values="{ORANGE};{YELLOW};{ORANGE}" dur="1.3s" repeatCount="indefinite"/></path></g>\n')
            s += f'  <text x="{cx}" y="166" class="sans" font-size="42" font-weight="800" fill="{ncol}" text-anchor="middle">{num}</text>\n'
            s += f'  <text x="{cx}" y="238" class="sans" font-size="18" font-weight="700" fill="{lcol}" text-anchor="middle">{lab}</text>\n'
            s += f'  <text x="{cx}" y="266" class="sans" font-size="16" fill="{MUTED}" text-anchor="middle">{sub}</text>\n'
        else:
            s += f'  <g>{fade_in(0.4)}\n'
            s += f'    <text x="{cx}" y="166" class="sans" font-size="46" font-weight="800" fill="{ncol}" text-anchor="middle">{num}</text>\n'
            s += f'    <text x="{cx}" y="212" class="sans" font-size="18" font-weight="600" fill="{lcol}" text-anchor="middle">{lab}</text>\n'
            s += f'    <text x="{cx}" y="240" class="sans" font-size="16" fill="{MUTED}" text-anchor="middle">{sub}</text>\n  </g>\n'
    s += foot(W, H)
    return s


for name, fn in [("hero.svg", hero), ("stack.svg", stack), ("architecture.svg", architecture), ("stats.svg", stats)]:
    if ARGS.only and name[:-4] not in ARGS.only:
        continue
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(fn())
print("ok")
