"""Generate the profile SVGs (hero, proof bar) in light + dark variants.

    python3 assets/build.py            # default theme (ink)
    python3 assets/build.py bronze     # or: verdigris

Backgrounds are transparent so the SVGs sit on GitHub's own canvas.
"""
import sys
from pathlib import Path

OUT = Path(__file__).parent

THEMES = {
    # name: {mode: (foreground, muted, hairline, accent)}
    "ink": {
        "dark": ("#E8E4DC", "#8B9098", "#2B3038", "#86A7C8"),
        "light": ("#1C1E21", "#676C73", "#D8D3C9", "#2F4F6F"),
    },
    "bronze": {
        "dark": ("#EAE4DA", "#8F8A83", "#2F2C28", "#C29B6C"),
        "light": ("#1E1C1A", "#6E6962", "#DDD5C8", "#8A6239"),
    },
    "verdigris": {
        "dark": ("#E6E6E0", "#8A918F", "#29302F", "#7FAAA0"),
        "light": ("#1B1E1D", "#666D6B", "#D6D6CE", "#3E6F66"),
    },
}

SERIF = "'Iowan Old Style','Charter','Source Serif Pro',Georgia,'Times New Roman',serif"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "ui-monospace,'SFMono-Regular','JetBrains Mono',Menlo,Consolas,monospace"

# Lines cycled by the hero's typed status row. Keep them short and concrete.
TYPED = [
    "RAG that cites its sources, or says it doesn't know.",
    "Agents with step budgets and a human escalation path.",
    "p95 latency and cost per request, tracked from day one.",
]


def hero(fg, muted, rule, accent):
    w, h = 880, 250
    cycle = 4.0 * len(TYPED)
    share = 100 / len(TYPED)
    char_w = 7.8  # ~0.6em at 13px monospace
    typed_css, typed_svg = [], []
    for i, line in enumerate(TYPED):
        full = len(line) * char_w + 4
        n = len(line)
        typed_css.append(
            f"@keyframes t{i}{{0%{{width:0}}{share*0.45:.2f}%{{width:{full:.0f}px}}"
            f"{share*0.92:.2f}%{{width:{full:.0f}px}}{share:.2f}%{{width:0}}100%{{width:0}}}}"
            f".c{i}{{width:0;animation:t{i} {cycle}s steps({n},end) {i*cycle/len(TYPED)}s infinite}}"
        )
        typed_svg.append(
            f'<clipPath id="k{i}"><rect class="c{i}" x="64" y="206" height="20"/></clipPath>'
            f'<text x="64" y="220" class="mono typed" clip-path="url(#k{i})">{line}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Areesha Amir. AI Product Architect. From fragile demo to production system.">
<style>
.mono{{font-family:{MONO};font-size:13px;letter-spacing:.02em}}
.eyebrow{{font-family:{MONO};font-size:12px;letter-spacing:.18em;fill:{muted}}}
.display{{font-family:{SERIF};font-size:44px;fill:{fg};letter-spacing:-.01em}}
.sub{{font-family:{SANS};font-size:16px;fill:{muted}}}
.typed{{fill:{fg}}}
.label{{fill:{muted}}}
.accent{{fill:{accent}}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
.dot{{animation:pulse 2.4s ease-in-out infinite}}
{''.join(typed_css)}
</style>
<text x="0" y="22" class="eyebrow">AREESHA AMIR <tspan class="accent">/</tspan> AI PRODUCT ARCHITECT</text>
<text x="0" y="86" class="display">From fragile demo</text>
<text x="0" y="138" class="display">to production system<tspan class="accent">.</tspan></text>
<text x="0" y="172" class="sub">LLM systems built to survive real users, real load, and real budgets.</text>
<line x1="0" y1="192" x2="{w}" y2="192" stroke="{rule}" stroke-width="1"/>
<circle cx="6" cy="216" r="4" fill="{accent}" class="dot"/>
<text x="18" y="220" class="mono label">live</text>
<text x="52" y="220" class="mono accent">›</text>
{''.join(typed_svg)}
</svg>
"""


PROOF = [
    ("20+", "products shipped"),
    ("6", "industries"),
    ("99.9%", "production uptime"),
    ("3.8", "GPA · Habib"),
    ("Full", "merit scholarship"),
]


def proof(fg, muted, rule, accent):
    w, h = 880, 96
    col = w / len(PROOF)
    cells = []
    for i, (num, label) in enumerate(PROOF):
        x = i * col
        if i:
            cells.append(f'<line x1="{x:.0f}" y1="14" x2="{x:.0f}" y2="82" stroke="{rule}"/>')
        pad = 0 if i == 0 else 22
        cells.append(
            f'<text x="{x+pad:.0f}" y="50" class="num">{num}</text>'
            f'<text x="{x+pad:.0f}" y="74" class="lbl">{label}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{' · '.join(f'{n} {l}' for n, l in PROOF)}">
<style>
.num{{font-family:{SERIF};font-size:34px;fill:{fg}}}
.lbl{{font-family:{MONO};font-size:11.5px;letter-spacing:.06em;fill:{muted}}}
</style>
<line x1="0" y1="0.5" x2="{w}" y2="0.5" stroke="{accent}" stroke-width="1"/>
{''.join(cells)}
<line x1="0" y1="{h-0.5}" x2="{w}" y2="{h-0.5}" stroke="{rule}"/>
</svg>
"""


def main():
    theme = THEMES[sys.argv[1] if len(sys.argv) > 1 else "ink"]
    for mode, colors in theme.items():
        (OUT / f"hero-{mode}.svg").write_text(hero(*colors))
        (OUT / f"proof-{mode}.svg").write_text(proof(*colors))


if __name__ == "__main__":
    main()
