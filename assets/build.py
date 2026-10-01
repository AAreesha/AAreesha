"""Generate every animated SVG used by the profile README, in light + dark.

    python3 assets/build.py            # default theme (ink)
    python3 assets/build.py bronze     # or: verdigris

Edit the content blocks below (PROJECTS, STEPS, ...) and re-run.
Backgrounds are transparent so the SVGs sit on GitHub's own canvas.
"""
import sys
from html import escape
from pathlib import Path

OUT = Path(__file__).parent

THEMES = {
    # mode: (text, muted, hairline, accent, surface, rose, berry)
    "ink": {
        "dark": ("#E8E4DC", "#8B9098", "#2B3038", "#86A7C8", "#151A21", "#E8A3BC", "#D9578A"),
        "light": ("#1C1E21", "#676C73", "#D8D3C9", "#2F4F6F", "#F6F4EF", "#B5577D", "#9C2358"),
    },
    "bronze": {
        "dark": ("#EAE4DA", "#8F8A83", "#2F2C28", "#C29B6C", "#1A1816", "#E3A6B4", "#D25A84"),
        "light": ("#1E1C1A", "#6E6962", "#DDD5C8", "#8A6239", "#F7F3EC", "#A9566E", "#962552"),
    },
    "verdigris": {
        "dark": ("#E6E6E0", "#8A918F", "#29302F", "#7FAAA0", "#141A19", "#E6A4BA", "#D65889"),
        "light": ("#1B1E1D", "#666D6B", "#D6D6CE", "#3E6F66", "#F3F5F2", "#AE5878", "#982456"),
    },
}

SANS = "'Inter','Segoe UI','Helvetica Neue',-apple-system,BlinkMacSystemFont,Roboto,Arial,sans-serif"
MONO = "ui-monospace,'SFMono-Regular','JetBrains Mono',Menlo,Consolas,monospace"

# ---------------------------------------------------------------- content

TYPED = [
    "Ideas into products people rely on.",
    "Built for real users, not just demos.",
    "Fast, affordable, and always on.",
]

STATS = [
    ("20+", "products shipped"),
    ("6", "industries"),
    ("99.9%", "uptime"),
    ("3.8", "GPA"),
    ("Full", "scholarship"),
]

# (slug, tag, title, description, outcome, motif)
PROJECTS = [
    ("helpwise", "AI assistant", "Cited Support Chatbot",
     "Answers customer questions from help articles, and links the exact sources behind every answer.",
     "40% faster resolution", "chat"),
    ("careroute", "Healthcare", "Safe Triage Assistant",
     "Handles first-line patient intake and hands off to a clinician whenever it isn't sure.",
     "A third fewer front-desk calls", "shield"),
    ("skillpath", "Education", "Adaptive Learning Platform",
     "Reshapes every lesson and quiz around what each learner still needs to practise.",
     "Completion up from 35% to 78%", "grid"),
    ("callcadence", "Voice agent", "Voice Booking Agent",
     "Calls prospects, holds a natural conversation, and books the meeting straight into a calendar.",
     "3x more meetings booked", "wave"),
    ("autolens", "Computer vision", "Used-Car Price Estimator",
     "Prices a used car from its listing photos, even from a single exterior shot.",
     "Within 8% of the final sale price", "gauge"),
    ("roamplan", "Travel", "Trip Itinerary Planner",
     "Turns travel dates and interests into day-by-day plans that re-plan as you move a pin.",
     "About 5 hours saved per trip", "pin"),
]

STEPS = [
    ("Listen", "Understand the people and the real problem."),
    ("Design", "Plan the simplest thing that will hold up."),
    ("Build", "Ship early, test often, improve every week."),
    ("Care", "Launch, watch closely, keep it running."),
]

SKILLS = [
    ("AI assistants", "Chat and search tools that answer with sources.", "chat"),
    ("Automation", "Agents that handle the busywork safely.", "flow"),
    ("Full products", "Web apps from first sketch to launch.", "grid"),
    ("Reliability", "Systems that stay fast, affordable, online.", "shield"),
]

# (when, role, where, one line) — newest first
JOURNEY = [
    ("Now", "AI Product Architect", "Self-employed",
     "Turning stalled AI demos into products that hold up with real users and real costs."),
    ("2024–25", "AI Consultant", "Independent",
     "Shipped a learning platform, voice agents and a triage assistant for education, HR and healthcare."),
    ("2025", "AI/ML Engineer", "JBS (Jaffar Brothers)",
     "A year of end-to-end machine learning, from data pipelines to models in production."),
    ("2025", "AI/ML Engineer", "Vettio",
     "AI features for hiring and job-seeking software."),
    ("2025", "Research Intern", "AI @ Dartmouth",
     "Built a resume screening tool and a programming elective the university now teaches."),
    ("2025", "Frontend Engineer", "Securiti",
     "Product interfaces built with a careful eye for design."),
    ("2021–25", "BS Computer Science", "Habib University",
     "Full scholarship, 3.8 GPA, Dean's and President's Lists."),
]

SECTIONS = [
    ("built", "01", "Things I've built"),
    ("work", "02", "How I work"),
    ("skills", "03", "What I'm good at"),
    ("journey", "04", "My journey"),
    ("activity", "05", "On GitHub"),
    ("talk", "06", "Let's talk"),
]

BUTTONS = [
    ("portfolio", "Portfolio"),
    ("resume", "Resume"),
    ("email", "Email"),
    ("contact", "Contact"),
    ("linkedin", "LinkedIn"),
]

# ---------------------------------------------------------------- helpers


def wrap(text, width):
    lines, cur = [], ""
    for word in text.split():
        if cur and len(cur) + 1 + len(word) > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + [cur] if cur else lines


def svg(w, h, label, style, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">'
        f"<style>{style}</style>{body}</svg>\n"
    )


def base_css(c):
    fg, muted, rule, accent, surface, rose, berry = c
    return (
        f".sans{{font-family:{SANS}}}.mono{{font-family:{MONO}}}"
        f".fg{{fill:{fg}}}.muted{{fill:{muted}}}.accent{{fill:{accent}}}.rose{{fill:{rose}}}.berry{{fill:{berry}}}"
        "@keyframes up{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}"
        ".up{opacity:0;animation:up .8s cubic-bezier(.2,.7,.2,1) forwards}"
        "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}"
        ".pulse{animation:pulse 2.4s ease-in-out infinite}"
        "@keyframes ring{0%{r:5;opacity:.7}100%{r:16;opacity:0}}"
        "@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}"
        ".float{animation:float 4s ease-in-out infinite}"
        "@media (prefers-reduced-motion:reduce){.up{opacity:1;animation:none}.pulse,.float{animation:none}}"
    )


def icon(kind, x, y, c, s=1.0):
    """Small animated line-art motifs, drawn in a 48x48 box at (x, y)."""
    fg, muted, rule, accent, surface, rose, berry = c
    g = f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke-linecap="round" stroke-linejoin="round">'
    if kind == "chat":
        g += (
            f'<rect x="2" y="6" width="30" height="20" rx="6" stroke="{fg}" stroke-width="1.6"/>'
            f'<path d="M10 26 l-2 7 l8 -7" stroke="{fg}" stroke-width="1.6"/>'
            f'<rect x="18" y="20" width="28" height="18" rx="6" stroke="{accent}" stroke-width="1.6" fill="{surface}"/>'
        )
        for i in range(3):
            g += (f'<circle cx="{26+i*6}" cy="29" r="1.8" fill="{accent}" stroke="none" '
                  f'class="pulse" style="animation-delay:{i*.3}s"/>')
    elif kind == "flow":
        g += (f'<path d="M8 12 H24 V36 H40" stroke="{rule}" stroke-width="1.6"/>'
              f'<circle cx="8" cy="12" r="5" stroke="{fg}" stroke-width="1.6"/>'
              f'<circle cx="24" cy="24" r="5" stroke="{fg}" stroke-width="1.6"/>'
              f'<circle cx="40" cy="36" r="5" stroke="{accent}" stroke-width="1.6"/>'
              f'<circle r="2.4" fill="{accent}" stroke="none">'
              '<animateMotion dur="2.6s" repeatCount="indefinite" path="M8 12 H24 V36 H40"/></circle>')
    elif kind == "shield":
        g += (f'<path d="M24 4 L41 10 V23 C41 34 33 41 24 44 C15 41 7 34 7 23 V10 Z" stroke="{fg}" stroke-width="1.6"/>'
              f'<path d="M16 24 l6 6 l11 -12" stroke="{accent}" stroke-width="2" pathLength="1" '
              'stroke-dasharray="1" stroke-dashoffset="1">'
              '<animate attributeName="stroke-dashoffset" values="1;0;0;1" keyTimes="0;.35;.8;1" dur="3.2s" repeatCount="indefinite"/></path>')
    elif kind == "gauge":
        g += (f'<path d="M6 34 A18 18 0 0 1 42 34" stroke="{rule}" stroke-width="3"/>'
              f'<path d="M6 34 A18 18 0 0 1 32 18" stroke="{accent}" stroke-width="3"/>'
              f'<g><line x1="24" y1="34" x2="24" y2="20" stroke="{fg}" stroke-width="1.8"/>'
              '<animateTransform attributeName="transform" type="rotate" values="-50 24 34;40 24 34;-50 24 34" dur="4s" repeatCount="indefinite"/></g>'
              f'<circle cx="24" cy="34" r="3" fill="{fg}" stroke="none"/>')
    elif kind == "grid":
        for i in range(4):
            gx, gy = 6 + (i % 2) * 20, 6 + (i // 2) * 20
            col = accent if i == 3 else fg
            g += (f'<rect x="{gx}" y="{gy}" width="16" height="16" rx="4" stroke="{col}" stroke-width="1.6" '
                  f'class="pulse" style="animation-delay:{i*.4}s;animation-duration:3.2s"/>')
    elif kind == "wave":
        for i, (lo, hi) in enumerate([(8, 18), (12, 30), (6, 22), (14, 34), (8, 20), (10, 26)]):
            bx = 5 + i * 7.5
            col = rose if i in (1, 3) else fg
            g += (f'<line x1="{bx}" x2="{bx}" y1="{24-lo/2}" y2="{24+lo/2}" stroke="{col}" stroke-width="2.4">'
                  f'<animate attributeName="y1" values="{24-lo/2};{24-hi/2};{24-lo/2}" dur="{1.1+i*.17:.2f}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="y2" values="{24+lo/2};{24+hi/2};{24+lo/2}" dur="{1.1+i*.17:.2f}s" repeatCount="indefinite"/></line>')
    elif kind == "pin":
        g += (f'<ellipse cx="24" cy="41" rx="12" ry="3.5" stroke="{rule}" stroke-width="1.4"/>'
              f'<ellipse cx="24" cy="41" rx="4" ry="1.2" stroke="{rose}" stroke-width="1.4">'
              '<animate attributeName="rx" values="4;14" dur="2.2s" repeatCount="indefinite"/>'
              '<animate attributeName="ry" values="1.2;4.5" dur="2.2s" repeatCount="indefinite"/>'
              '<animate attributeName="opacity" values="1;0" dur="2.2s" repeatCount="indefinite"/></ellipse>'
              f'<path d="M24 40 C24 40 12 27 12 18 A12 12 0 0 1 36 18 C36 27 24 40 24 40 Z" stroke="{fg}" stroke-width="1.6"/>'
              f'<circle cx="24" cy="18" r="4" stroke="{accent}" stroke-width="1.6"/>')
    return g + "</g>"


# ---------------------------------------------------------------- components


def hero(c):
    fg, muted, rule, accent, surface, rose, berry = c
    w, h = 880, 300
    cycle = 4.0 * len(TYPED)
    share = 100 / len(TYPED)
    css = [base_css(c),
           ".name{font-size:50px;font-weight:700;letter-spacing:-.02em}",
           ".lead{font-size:19px}.pill{font-size:12px;letter-spacing:.06em}.typed{font-size:15px}"]
    typed = []
    for i, line in enumerate(TYPED):
        full = len(line) * 9.1 + 6
        css.append(
            f"@keyframes t{i}{{0%{{width:0}}{share*.45:.2f}%{{width:{full:.0f}px}}"
            f"{share*.92:.2f}%{{width:{full:.0f}px}}{share:.2f}%{{width:0}}100%{{width:0}}}}"
            f".c{i}{{width:0;animation:t{i} {cycle}s steps({len(line)},end) {i*cycle/len(TYPED)+1.2}s infinite}}")
        typed.append(f'<clipPath id="k{i}"><rect class="c{i}" x="22" y="222" height="24"/></clipPath>'
                     f'<text x="22" y="240" class="mono typed fg" clip-path="url(#k{i})">{escape(line)}</text>')
    cx, cy = 735, 150
    orbit = (f'<g opacity=".95">'
             f'<circle cx="{cx}" cy="{cy}" r="110" fill="none" stroke="{rule}" stroke-dasharray="2 6"/>'
             f'<circle cx="{cx}" cy="{cy}" r="78" fill="none" stroke="{rule}"/>'
             f'<circle cx="{cx}" cy="{cy}" r="44" fill="none" stroke="{rule}"/>'
             f'<circle cx="{cx}" cy="{cy}" r="22" fill="{accent}" opacity=".18" class="pulse"/>'
             f'<circle cx="{cx}" cy="{cy}" r="9" fill="{accent}"/>')
    for r, dur, size, col, start in [(44, 7, 4, berry, 0), (78, 13, 5, accent, 120), (78, 13, 4, rose, 300), (110, 21, 4, accent, 200)]:
        orbit += (f'<g><circle cx="{cx + r}" cy="{cy}" r="{size}" fill="{col}"/>'
                  f'<animateTransform attributeName="transform" type="rotate" from="{start} {cx} {cy}" '
                  f'to="{start+360} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/></g>')
    orbit += "</g>"
    body = (
        orbit +
        f'<g class="up" style="animation-delay:.1s"><rect x="0" y="18" width="232" height="30" rx="15" fill="{surface}" stroke="{rule}"/>'
        f'<circle cx="18" cy="33" r="4.5" class="rose pulse"/>'
        f'<text x="32" y="37.5" class="sans pill fg">OPEN TO OPPORTUNITIES</text></g>'
        f'<text x="0" y="118" class="sans name fg up" style="animation-delay:.3s">Hi, I\'m Areesha Amir<tspan class="rose">.</tspan></text>'
        f'<text x="0" y="158" class="sans lead muted up" style="animation-delay:.55s">I turn AI ideas into products people can rely on.</text>'
        f'<line x1="0" y1="190" x2="520" y2="190" stroke="{rule}"/>'
        f'<line x1="0" y1="190" x2="520" y2="190" stroke="{accent}" stroke-width="2" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1">'
        '<animate attributeName="stroke-dashoffset" from="1" to="0" begin=".8s" dur="1.4s" fill="freeze"/></line>'
        f'<text x="0" y="240" class="mono typed accent">›</text>' + "".join(typed)
    )
    return svg(w, h, "Hi, I'm Areesha Amir. I turn AI ideas into products people can rely on.", "".join(css), body)


def stats(c):
    fg, muted, rule, accent, surface, rose, berry = c
    w, h, gap = 880, 124, 12
    tw = (w - gap * (len(STATS) - 1)) / len(STATS)
    css = base_css(c) + ".num{font-size:34px;font-weight:700;letter-spacing:-.02em}.lbl{font-size:13px}"
    body = ""
    for i, (num, label) in enumerate(STATS):
        x = i * (tw + gap)
        d = i * .15
        body += (f'<g class="up" style="animation-delay:{d:.2f}s">'
                 f'<rect x="{x+.5:.1f}" y=".5" width="{tw-1:.1f}" height="{h-1}" rx="14" fill="{surface}" stroke="{rule}"/>'
                 f'<text x="{x+20:.1f}" y="58" class="sans num fg">{escape(num)}</text>'
                 f'<text x="{x+20:.1f}" y="84" class="sans lbl muted">{escape(label)}</text>'
                 f'<rect x="{x+20:.1f}" y="100" width="{tw-40:.1f}" height="3" rx="1.5" fill="{rule}"/>'
                 f'<rect x="{x+20:.1f}" y="100" width="0" height="3" rx="1.5" fill="{(accent, rose, berry)[i % 3]}">'
                 f'<animate attributeName="width" from="0" to="{tw-40:.1f}" begin="{d+.4:.2f}s" dur="1.2s" fill="freeze" '
                 'calcMode="spline" keySplines=".2 .7 .2 1"/></rect></g>')
    return svg(w, h, " · ".join(f"{n} {l}" for n, l in STATS), css, body)


def section(c, num, title):
    fg, muted, rule, accent, surface, rose, berry = c
    w, h = 880, 60
    css = base_css(c) + ".n{font-size:13px;letter-spacing:.1em}.t{font-size:24px;font-weight:700;letter-spacing:-.01em}"
    tx = 52
    lx = tx + len(title) * 13.5 + 24
    body = (f'<text x="0" y="38" class="mono n berry">{num}</text>'
            f'<text x="{tx}" y="40" class="sans t fg">{escape(title)}</text>'
            f'<line x1="{lx:.0f}" y1="32" x2="{w}" y2="32" stroke="{rule}" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1">'
            '<animate attributeName="stroke-dashoffset" from="1" to="0" dur="1.2s" fill="freeze"/></line>'
            f'<circle cy="32" r="3" fill="{rose}"><animate attributeName="cx" values="{lx:.0f};{w-4};{lx:.0f}" '
            'dur="9s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.5;1" keySplines=".5 0 .5 1;.5 0 .5 1"/></circle>')
    return svg(w, h, f"{num} {title}", css, body)


def card(c, tag, title, desc, outcome, motif):
    fg, muted, rule, accent, surface, rose, berry = c
    w, h = 432, 250
    css = base_css(c) + (".tag{font-size:11px;letter-spacing:.08em}.title{font-size:20px;font-weight:700}"
                         ".desc{font-size:14px}.out{font-size:13.5px;font-weight:600}.more{font-size:12.5px}")
    lines = wrap(desc, 50)[:3]
    tag_w = len(tag) * 7.6 + 24
    body = (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="{surface}" stroke="{rule}"/>'
            f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="none" stroke="{rose}" pathLength="1" '
            'stroke-dasharray=".12 .88" stroke-dashoffset="0" opacity=".9">'
            '<animate attributeName="stroke-dashoffset" from="0" to="-1" dur="7s" repeatCount="indefinite"/></rect>'
            f'<g class="float">{icon(motif, 24, 22, c)}</g>'
            f'<rect x="{w-24-tag_w:.0f}" y="26" width="{tag_w:.0f}" height="24" rx="12" fill="none" stroke="{berry}" stroke-opacity=".7"/>'
            f'<text x="{w-24-tag_w/2:.0f}" y="42" text-anchor="middle" class="sans tag muted">{escape(tag.upper())}</text>'
            f'<text x="24" y="104" class="sans title fg">{escape(title)}</text>')
    for i, line in enumerate(lines):
        body += f'<text x="24" y="{132 + i*21}" class="sans desc muted">{escape(line)}</text>'
    body += (f'<circle cx="30" cy="{h-30}" r="4" class="rose pulse"/>'
             f'<text x="42" y="{h-25}" class="sans out accent">{escape(outcome)}</text>'
             f'<text x="{w-24}" y="{h-25}" text-anchor="end" class="sans more muted">View →</text>')
    return svg(w, h, f"{title}. {desc} {outcome}.", css, body)


def steps(c):
    fg, muted, rule, accent, surface, rose, berry = c
    w, h = 880, 190
    n = len(STEPS)
    xs = [70 + i * (w - 140) / (n - 1) for i in range(n)]
    css = base_css(c) + ".st{font-size:17px;font-weight:700}.sd{font-size:13.5px}.sn{font-size:12px;font-weight:700}"
    body = (f'<line x1="{xs[0]:.0f}" y1="40" x2="{xs[-1]:.0f}" y2="40" stroke="{rule}" stroke-width="2"/>'
            f'<line x1="{xs[0]:.0f}" y1="40" x2="{xs[-1]:.0f}" y2="40" stroke="{rose}" stroke-width="2" pathLength="1" '
            'stroke-dasharray=".18 .82"><animate attributeName="stroke-dashoffset" from=".18" to="-1" dur="4s" repeatCount="indefinite"/></line>')
    for i, ((title, desc), x) in enumerate(zip(STEPS, xs)):
        d = i * .25
        body += (f'<g class="up" style="animation-delay:{d:.2f}s">'
                 f'<circle cx="{x:.0f}" cy="40" r="22" fill="{surface}" stroke="{accent if i == n-1 else fg}" stroke-width="1.6"/>'
                 f'<text x="{x:.0f}" y="44.5" text-anchor="middle" class="sans sn fg">0{i+1}</text>'
                 f'<text x="{x:.0f}" y="96" text-anchor="middle" class="sans st fg">{escape(title)}</text>')
        for j, line in enumerate(wrap(desc, 24)):
            body += f'<text x="{x:.0f}" y="{122 + j*19}" text-anchor="middle" class="sans sd muted">{escape(line)}</text>'
        body += "</g>"
    body += (f'<circle cx="{xs[-1]:.0f}" cy="40" r="5" fill="none" stroke="{accent}">'
             '<animate attributeName="r" values="22;34" dur="2.4s" repeatCount="indefinite"/>'
             '<animate attributeName="opacity" values=".8;0" dur="2.4s" repeatCount="indefinite"/></circle>')
    return svg(w, h, " → ".join(f"{t}: {d}" for t, d in STEPS), css, body)


def skills(c):
    fg, muted, rule, accent, surface, rose, berry = c
    w, h, gap = 880, 200, 14
    tw = (w - gap * (len(SKILLS) - 1)) / len(SKILLS)
    css = base_css(c) + ".kt{font-size:16.5px;font-weight:700}.kd{font-size:13.5px}"
    body = ""
    for i, (title, desc, motif) in enumerate(SKILLS):
        x = i * (tw + gap)
        body += (f'<g class="up" style="animation-delay:{i*.15:.2f}s">'
                 f'<rect x="{x+.5:.1f}" y=".5" width="{tw-1:.1f}" height="{h-1}" rx="16" fill="{surface}" stroke="{rule}"/>'
                 f'<g class="float" style="animation-delay:{i*.6:.1f}s">{icon(motif, x+20, 22, c, .9)}</g>'
                 f'<text x="{x+20:.1f}" y="104" class="sans kt fg">{escape(title)}</text>')
        for j, line in enumerate(wrap(desc, 24)):
            body += f'<text x="{x+20:.1f}" y="{130 + j*19}" class="sans kd muted">{escape(line)}</text>'
        body += "</g>"
    return svg(w, h, " · ".join(f"{t}: {d}" for t, d, _ in SKILLS), css, body)


def journey(c):
    fg, muted, rule, accent, surface, rose, berry = c
    row, top = 78, 20
    w, h = 880, top + row * len(JOURNEY)
    lx = 132
    css = base_css(c) + (".jy{font-size:12px;letter-spacing:.08em;font-weight:700}"
                         ".jr{font-size:17px;font-weight:700}.jw{font-size:15px;font-weight:600}.jd{font-size:13.5px}")
    body = (f'<line x1="{lx}" y1="{top+8}" x2="{lx}" y2="{h-row+28}" stroke="{rule}" stroke-width="2"/>'
            f'<line x1="{lx}" y1="{top+8}" x2="{lx}" y2="{h-row+28}" stroke="{berry}" stroke-width="2" pathLength="1" '
            'stroke-dasharray="1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" from="1" to="0" dur="2.6s" fill="freeze"/></line>')
    for i, (when, role, where, desc) in enumerate(JOURNEY):
        y = top + i * row
        now = i == 0
        body += (f'<g class="up" style="animation-delay:{i*.3:.2f}s">'
                 f'<text x="{lx-26}" y="{y+13}" text-anchor="end" class="sans jy {"rose" if now else "muted"}">{escape(when.upper())}</text>'
                 f'<circle cx="{lx}" cy="{y+8}" r="7" fill="{rose if now else surface}" stroke="{rose if now else accent}" stroke-width="2"/>'
                 f'<text x="{lx+28}" y="{y+14}" class="sans jr fg">{escape(role)}'
                 f'<tspan class="muted" style="font-weight:400">  ·  </tspan><tspan class="jw berry">{escape(where)}</tspan></text>'
                 f'<text x="{lx+28}" y="{y+38}" class="sans jd muted">{escape(desc)}</text></g>')
    body += (f'<circle cx="{lx}" cy="{top+8}" r="7" fill="none" stroke="{rose}">'
             '<animate attributeName="r" values="7;20" dur="2.4s" repeatCount="indefinite"/>'
             '<animate attributeName="opacity" values=".8;0" dur="2.4s" repeatCount="indefinite"/></circle>')
    return svg(w, h, " · ".join(f"{a}: {r}, {wh}" for a, r, wh, _ in JOURNEY), css, body)


def cta(c):
    fg, muted, rule, accent, surface, rose, berry = c
    w, h = 880, 190
    css = base_css(c) + ".big{font-size:32px;font-weight:700;letter-spacing:-.02em}.sub{font-size:16px}"
    body = (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20" fill="{surface}" stroke="{rule}"/>'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20" fill="none" stroke="{rose}" stroke-width="1.5" pathLength="1" '
            'stroke-dasharray=".2 .8"><animate attributeName="stroke-dashoffset" from="0" to="-1" dur="8s" repeatCount="indefinite"/></rect>'
            f'<text x="{w/2:.0f}" y="84" text-anchor="middle" class="sans big fg up">Let\'s build something that lasts<tspan class="rose">.</tspan></text>'
            f'<text x="{w/2:.0f}" y="118" text-anchor="middle" class="sans sub muted up" style="animation-delay:.25s">'
            'Open to graduate scholarships, research, and AI product roles.</text>'
            f'<g class="up" style="animation-delay:.5s"><circle cx="{w/2-92:.0f}" cy="148" r="4.5" class="rose pulse"/>'
            f'<text x="{w/2-80:.0f}" y="152.5" class="mono muted" style="font-size:12.5px">xmireesha@gmail.com</text></g>')
    return svg(w, h, "Let's build something that lasts. Open to graduate scholarships, research, and AI product roles.", css, body)


def button(c, label):
    fg, muted, rule, accent, surface, rose, berry = c
    w, h = 150, 46
    css = base_css(c) + ".b{font-size:14.5px;font-weight:600}"
    body = (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="23" fill="{surface}" stroke="{accent}" stroke-width="1.3"/>'
            f'<text x="{w/2-6:.0f}" y="28.5" text-anchor="middle" class="sans b fg" dx="-6">{escape(label)}</text>'
            f'<text x="{w-36}" y="28.5" class="sans b rose">→<animate attributeName="x" values="{w-38};{w-33};{w-38}" '
            'dur="1.8s" repeatCount="indefinite"/></text>')
    return svg(w, h, label, css, body)


def main():
    theme = THEMES[sys.argv[1] if len(sys.argv) > 1 else "ink"]
    for d in ("cards", "sections", "buttons"):
        (OUT / d).mkdir(exist_ok=True)
    for mode, c in theme.items():
        (OUT / f"hero-{mode}.svg").write_text(hero(c))
        (OUT / f"stats-{mode}.svg").write_text(stats(c))
        (OUT / f"steps-{mode}.svg").write_text(steps(c))
        (OUT / f"skills-{mode}.svg").write_text(skills(c))
        (OUT / f"journey-{mode}.svg").write_text(journey(c))
        (OUT / f"cta-{mode}.svg").write_text(cta(c))
        for slug, *rest in PROJECTS:
            (OUT / "cards" / f"{slug}-{mode}.svg").write_text(card(c, *rest))
        for slug, num, title in SECTIONS:
            (OUT / "sections" / f"{slug}-{mode}.svg").write_text(section(c, num, title))
        for slug, label in BUTTONS:
            (OUT / "buttons" / f"{slug}-{mode}.svg").write_text(button(c, label))


if __name__ == "__main__":
    main()
