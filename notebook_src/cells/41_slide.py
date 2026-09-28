# ---------------------------------------------------------------- Блок 5: slide_data.json, slide_spec.md, slide.html
o, a = R_NOWCAST['openai'], R_NOWCAST['anthropic']; S = R_SPLIT['summary']
eo, ea = R_NOWCAST['reproduction']['OpenAI']['epoch'], R_NOWCAST['reproduction']['Anthropic']['epoch']
FOOTER_SOURCES = ['S01', 'S02', 'S11', 'S13', 'S15', 'S06', 'S29']
slide_data = {
    'as_of': DATE_TAG, 'accessed': ACCESSED,
    'title': f"Штуки не публикуются; в H100e OpenAI ≈ {ru(eo['p50']/1e6,1)} млн, Anthropic ≈ {ru(ea['p50']/1e6,1)} млн (конец 2025); "
             f"nowcast на {NOWCAST_DATE.strftime('%d.%m.%Y')} — ×{ru(o['multiplier_vs_end2025']['p50'],1)} и ×{ru(a['multiplier_vs_end2025']['p50'],1)}; сплит обучение/инференс 2025: 50/50 и 60/40; 2026 — обучение {100*S['openai_2026_rd_share_range'][0]:.0f}–{100*S['openai_2026_rd_share_range'][1]:.0f} % у OpenAI по плану, {100*S['anthropic_h1_2026_rd_share_range'][0]:.0f}–{100*S['anthropic_h1_2026_rd_share_range'][1]:.0f} % у Anthropic по сценариям",
    'bars_h100e': [
        {'company': 'OpenAI', 'period': 'конец 2025', 'p05': eo['p05'], 'p50': eo['p50'], 'p95': eo['p95'], 'status': 'E (Epoch)', 'source': 'S02'},
        {'company': 'OpenAI', 'period': f'nowcast {DATE_TAG}', 'p05': o['h100e']['p05'], 'p50': o['h100e']['p50'], 'p95': o['h100e']['p95'], 'status': 'E (наша модель)', 'source': 'calc_nowcast.py'},
        {'company': 'Anthropic', 'period': 'конец 2025', 'p05': ea['p05'], 'p50': ea['p50'], 'p95': ea['p95'], 'status': 'E (Epoch)', 'source': 'S02'},
        {'company': 'Anthropic', 'period': f'nowcast {DATE_TAG}', 'p05': a['h100e']['p05'], 'p50': a['h100e']['p50'], 'p95': a['h100e']['p95'], 'status': 'E (наша модель)', 'source': 'calc_nowcast.py'},
    ],
    'gw_labels': [
        {'company': 'OpenAI', 'period': 'конец 2025', 'label': '1,9 ГВт [V2]', 'source': 'S01'},
        {'company': 'OpenAI', 'period': f'nowcast {DATE_TAG}', 'label': f"≈{ru(o['gw_it_mw']['p50']/1e3,1)} ГВт IT ({ru(o['gw_it_mw']['p05']/1e3,1)}–{ru(o['gw_it_mw']['p95']/1e3,1)}) [E]", 'source': 'calc_nowcast.py'},
        {'company': 'Anthropic', 'period': 'конец 2025', 'label': '≈1,4 ГВт [V2, оценка OpenAI]', 'source': 'S11'},
        {'company': 'Anthropic', 'period': f'nowcast {DATE_TAG}', 'label': f"≈{ru(a['gw_it_mw']['p50']/1e3,1)} ГВт IT ({ru(a['gw_it_mw']['p05']/1e3,1)}–{ru(a['gw_it_mw']['p95']/1e3,1)}) [E]", 'source': 'calc_nowcast.py'},
    ],
    'split_bars': [
        {'company': 'OpenAI', 'year': '2024', 'rd_min': S['openai_2024']['rd_share'], 'rd_max': S['openai_2024']['rd_share'], 'inf_min': S['openai_2024']['inf_share'], 'inf_max': S['openai_2024']['inf_share'], 'status': 'V', 'source': 'S07'},
        {'company': 'OpenAI', 'year': '2025', 'rd_min': S['openai_2025']['rd_share'], 'rd_max': S['openai_2025']['rd_share'], 'inf_min': S['openai_2025']['inf_share'], 'inf_max': S['openai_2025']['inf_share'], 'status': 'V', 'source': 'S04;S16'},
        {'company': 'OpenAI', 'year': '2026 (план, сценарии)', 'rd_min': S['openai_2026_rd_share_range'][0], 'rd_max': S['openai_2026_rd_share_range'][1], 'inf_min': 1 - S['openai_2026_rd_share_range'][1], 'inf_max': 1 - S['openai_2026_rd_share_range'][0], 'status': 'E', 'source': 'S15;S13;S16'},
        {'company': 'Anthropic', 'year': '2024', 'rd_min': None, 'rd_max': None, 'inf_min': None, 'inf_max': None, 'status': '—', 'source': 'S04'},
        {'company': 'Anthropic', 'year': '2025', 'rd_min': S['anthropic_2025']['rd_share'], 'rd_max': S['anthropic_2025']['rd_share'], 'inf_min': S['anthropic_2025']['inf_share'], 'inf_max': S['anthropic_2025']['inf_share'], 'status': 'V/E', 'source': 'S06'},
        {'company': 'Anthropic', 'year': '2026 H1 (сценарии)', 'rd_min': S['anthropic_h1_2026_rd_share_range'][0], 'rd_max': S['anthropic_h1_2026_rd_share_range'][1], 'inf_min': 1 - S['anthropic_h1_2026_rd_share_range'][1], 'inf_max': 1 - S['anthropic_h1_2026_rd_share_range'][0], 'status': 'E', 'source': 'S29'},
    ],
    'footer_sources': FOOTER_SOURCES,
    'caveats': ['«Обучение» = весь R&D-compute (эксперименты, исследования); финальные прогоны — меньшая часть [S08].',
                'Сторонний инференс учтён в оценке Anthropic (Bedrock/Vertex, ≈10 %) и не учтён у OpenAI (Azure, до ~25 %) — сравнение смещено против OpenAI на 10–25 % [S04].'],
    'status_legend': {'факт': '[V]/[V2] — раскрыто компанией или подтверждено прессой', 'оценка': '[E] Epoch — медиана и 90 % ДИ', 'экстраполяция': '[E] наша модель — штриховка'},
}
save_json(slide_data, OUT / 'results' / 'slide_data.json')

# ---- slide_spec.md
spec = f"""# Спецификация слайда — as of {DATE_TAG}, источники проверены {ACCESSED}

**Заголовок‑ответ (одна строка, ≤ 2 строк на слайде).** {slide_data['title']}

**Слева (≈55 % ширины): «Парк в H100e».** Четыре столбика: OpenAI конец 2025 (Epoch), OpenAI nowcast {DATE_TAG}, Anthropic конец 2025 (Epoch), Anthropic nowcast. Высота — медиана; усы — 90 % ДИ (p05–p95). Подпись над столбиком — медиана в млн H100e; подпись под столбиком — ГВт со статусом: {' · '.join(g['label'] for g in slide_data['gw_labels'])}. Ось Y — «млн H100e» (0 … округление вверх от p95 nowcast OpenAI). Ось X — компания и период.

**Справа (≈45 %): «Сплит R&D / инференс, в деньгах».** Горизонтальные stacked‑бары по годам 2024, 2025, 2026 для каждой компании. Левый сегмент — R&D‑compute, правый — инференс. Для 2026 — диапазон (штриховка между мин. и макс. долей R&D); Anthropic 2024 — «не раскрыто». Значения: OpenAI {100*S['openai_2024']['rd_share']:.0f}/{100*S['openai_2024']['inf_share']:.0f} (2024), {100*S['openai_2025']['rd_share']:.0f}/{100*S['openai_2025']['inf_share']:.0f} (2025), R&D {100*S['openai_2026_rd_share_range'][0]:.0f}–{100*S['openai_2026_rd_share_range'][1]:.0f} % (2026 план); Anthropic {100*S['anthropic_2025']['rd_share']:.0f}/{100*S['anthropic_2025']['inf_share']:.0f} (2025), R&D {100*S['anthropic_h1_2026_rd_share_range'][0]:.0f}–{100*S['anthropic_h1_2026_rd_share_range'][1]:.0f} % (H1 2026 сценарии). Ось X — доля, 0–100 %.

**Цветовое кодирование.** Компания — цветом: OpenAI `#2470cc` (синий), Anthropic `#c9491a` (оранжевый). Статус — заливкой, не цветом: сплошная заливка — факт [V]/[V2] или оценка Epoch [E]; диагональная штриховка — наша экстраполяция/сценарий [E]. Текст — только нейтральные цвета (`#0b0b0b`, `#52514e`), никогда цветом серии. Инференс в stacked‑барах — нейтральный серый `#8f8e88`.

**Низ: строка статусов и источников.** «факт [V]/[V2] · оценка Epoch [E] · экстраполяция/сценарий [E, штриховка]». Источники: {', '.join(FOOTER_SOURCES)} (S01 — блог OpenAI 1,9 ГВт; S02 — Epoch AI Chip Users; S11 — Bloomberg/меморандум OpenAI 1,4 ГВт; S13 — Bloomberg, $50 млрд; S15 — The Information/The Decoder, $32 млрд; S06 — Epoch, расходы Anthropic; S29 — WSJ, кварталы Anthropic). Дата доступа: {ACCESSED}. Дата слайда: {DATE_TAG}.

**Две оговорки (по одной строке).**
1. {slide_data['caveats'][0]}
2. {slide_data['caveats'][1]}
"""
write_text(spec, OUT / 'results' / 'slide_spec.md')

# ---- slide.html: один экран 1280×720, inline SVG, без внешних зависимостей
def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
W, H = 1280, 720
COLH = {'OpenAI': '#2470cc', 'Anthropic': '#c9491a'}
# левая панель: столбики
Lx, Ly, Lw, Lh = 40, 120, 640, 420
ymax = math.ceil(max(b['p95'] for b in slide_data['bars_h100e']) / 1e6) + 0.5
def ypx(v): return Ly + Lh - (v / 1e6) / ymax * Lh
svg = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GPU-парк OpenAI и Anthropic">',
       '<defs><pattern id="hatchO" patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="rotate(45)"><rect width="8" height="8" fill="#2470cc" fill-opacity="0.18"/><line x1="0" y1="0" x2="0" y2="8" stroke="#2470cc" stroke-width="3"/></pattern>',
       '<pattern id="hatchA" patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="rotate(45)"><rect width="8" height="8" fill="#c9491a" fill-opacity="0.18"/><line x1="0" y1="0" x2="0" y2="8" stroke="#c9491a" stroke-width="3"/></pattern></defs>',
       f'<rect width="{W}" height="{H}" fill="var(--surface)"/>',
       *[f'<text x="40" y="{44 + 26*k}" class="title">{esc(line)}</text>' for k, line in enumerate(textwrap.wrap(slide_data['title'], 118)[:2])],
       f'<text x="{Lx}" y="{Ly-14}" class="h2">Парк в H100e: медиана и 90 % ДИ</text>',
       f'<text x="{Lx+Lw+40}" y="{Ly-14}" class="h2">Сплит R&amp;D-compute / инференс, в деньгах</text>']
for k in range(int(ymax) + 1):
    y = ypx(k * 1e6); svg.append(f'<line x1="{Lx}" y1="{y:.1f}" x2="{Lx+Lw}" y2="{y:.1f}" class="grid"/><text x="{Lx-6}" y="{y+4:.1f}" class="tick" text-anchor="end">{k}</text>')
svg.append(f'<text x="{Lx-28}" y="{Ly+Lh/2}" class="tick" transform="rotate(-90 {Lx-28} {Ly+Lh/2})" text-anchor="middle">млн H100e</text>')
bw, gap = 110, 40; x0 = Lx + 50
for i, b in enumerate(slide_data['bars_h100e']):
    x = x0 + i * (bw + gap) + (30 if i >= 2 else 0); col = COLH[b['company']]; hatched = 'nowcast' in b['period']
    fill = f'url(#hatch{"O" if b["company"]=="OpenAI" else "A"})' if hatched else col
    svg.append(f'<rect x="{x}" y="{ypx(b["p50"]):.1f}" width="{bw}" height="{Ly+Lh-ypx(b["p50"]):.1f}" fill="{fill}" stroke="{col}" stroke-width="1.5" rx="3"/>')
    svg.append(f'<line x1="{x+bw/2}" y1="{ypx(b["p05"]):.1f}" x2="{x+bw/2}" y2="{ypx(b["p95"]):.1f}" class="ci"/>'
               f'<line x1="{x+bw/2-12}" y1="{ypx(b["p05"]):.1f}" x2="{x+bw/2+12}" y2="{ypx(b["p05"]):.1f}" class="ci"/><line x1="{x+bw/2-12}" y1="{ypx(b["p95"]):.1f}" x2="{x+bw/2+12}" y2="{ypx(b["p95"]):.1f}" class="ci"/>')
    svg.append(f'<text x="{x+bw/2}" y="{ypx(b["p95"])-8:.1f}" class="val" text-anchor="middle">{esc(ru(b["p50"]/1e6,2))} млн</text>')
    svg.append(f'<text x="{x+bw/2}" y="{Ly+Lh+16}" class="lab" text-anchor="middle">{esc(b["company"])}</text>')
    svg.append(f'<text x="{x+bw/2}" y="{Ly+Lh+30}" class="lab" text-anchor="middle">{esc(b["period"])}</text>')
    gwl = slide_data['gw_labels'][i]['label']
    svg.append(f'<text x="{x+bw/2}" y="{Ly+Lh+46}" class="lab2" text-anchor="middle">{esc(gwl)}</text>')
    svg.append(f'<text x="{x+bw/2}" y="{Ly+Lh+60}" class="lab2" text-anchor="middle">{esc(b["status"])}</text>')
# правая панель: stacked-бары
Rx, Ry, Rw = Lx + Lw + 40, Ly + 10, 560
rowh, rgap = 34, 14
for i, sb in enumerate(slide_data['split_bars']):
    y = Ry + i * (rowh + rgap) + (16 if i >= 3 else 0); col = COLH[sb['company']]
    svg.append(f'<text x="{Rx}" y="{y+rowh/2+4}" class="lab">{esc(sb["company"])} {esc(sb["year"])}</text>')
    bx = Rx + 170; bwid = 215
    if sb['rd_min'] is None:
        svg.append(f'<rect x="{bx}" y="{y}" width="{bwid}" height="{rowh}" fill="#ecebe7" rx="3"/><text x="{bx+bwid/2}" y="{y+rowh/2+4}" class="lab2" text-anchor="middle">сплит не раскрыт [{esc(sb["source"])}]</text>'); continue
    lo, hi = sb['rd_min'], sb['rd_max']
    svg.append(f'<rect x="{bx}" y="{y}" width="{lo*bwid:.1f}" height="{rowh}" fill="{col}" rx="3"/>')
    if hi > lo: svg.append(f'<rect x="{bx+lo*bwid:.1f}" y="{y}" width="{(hi-lo)*bwid:.1f}" height="{rowh}" fill="url(#hatch{"O" if sb["company"]=="OpenAI" else "A"})" stroke="{col}" stroke-width="1"/>')
    svg.append(f'<rect x="{bx+hi*bwid+2:.1f}" y="{y}" width="{(1-hi)*bwid-2:.1f}" height="{rowh}" fill="#8f8e88" rx="3"/>')
    rd_txt = f'R&amp;D {100*lo:.0f}' + (f'–{100*hi:.0f}' if hi > lo else '') + ' %'; inf_txt = f'инференс {100*(1-hi):.0f}' + (f'–{100*(1-lo):.0f}' if hi > lo else '') + ' %'
    svg.append(f'<text x="{bx+6}" y="{y+rowh/2+4}" class="valw">{rd_txt}</text><text x="{bx+bwid+8}" y="{y+rowh/2+4}" class="val">{inf_txt} [{esc(sb["status"])}]</text>')
# низ: легенда статусов, оговорки, источники
fy = Ly + Lh + 84
svg.append(f'<rect x="{Lx}" y="{fy}" width="14" height="14" fill="#52514e"/><text x="{Lx+20}" y="{fy+12}" class="lab2">факт [V]/[V2] — сплошная заливка</text>')
svg.append(f'<rect x="{Lx+260}" y="{fy}" width="14" height="14" fill="#2470cc"/><text x="{Lx+280}" y="{fy+12}" class="lab2">оценка Epoch [E] — сплошная, 90 % ДИ усами</text>')
svg.append(f'<rect x="{Lx+600}" y="{fy}" width="14" height="14" fill="url(#hatchO)" stroke="#2470cc"/><text x="{Lx+620}" y="{fy+12}" class="lab2">экстраполяция / сценарий [E] — штриховка</text>')
svg.append(f'<text x="{Lx}" y="{fy+34}" class="cav">1. {esc(slide_data["caveats"][0])}</text>')
svg.append(f'<text x="{Lx}" y="{fy+52}" class="cav">2. {esc(slide_data["caveats"][1])}</text>')
svg.append(f'<text x="{Lx}" y="{H-14}" class="foot">Источники: {", ".join(FOOTER_SOURCES)} (реестр data/sources_2026-09-27.csv) · дата доступа {ACCESSED} · дата слайда {DATE_TAG} · nowcast: N(t)=N₂₀₂₅·g^Δt, Монте-Карло {ru(N_MC,0)} прогонов, seed {SEED}</text>')
svg.append('</svg>')
html = f"""<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>GPU-парк OpenAI и Anthropic</title>
<style>
:root {{ --surface:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --grid:#e6e5e0; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --surface:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --grid:#33332f; }} }}
:root[data-theme="dark"] {{ --surface:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --grid:#33332f; }}
html,body {{ margin:0; background:var(--surface); color:var(--ink); font-family: -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif; }}
.slide {{ width:100vw; height:100vh; display:flex; align-items:center; justify-content:center; padding:0 16px; box-sizing:border-box; }}
svg {{ max-width:100%; max-height:100vh; height:auto; }}
.title {{ font-size:18px; font-weight:600; fill:var(--ink); }}
.h2 {{ font-size:14px; font-weight:600; fill:var(--ink2); }}
.tick, .lab2, .foot {{ font-size:11px; fill:var(--ink2); }}
.lab {{ font-size:12px; fill:var(--ink); }}
.val {{ font-size:12px; font-weight:600; fill:var(--ink); }}
.valw {{ font-size:11px; font-weight:600; fill:#ffffff; }}
.cav {{ font-size:12px; fill:var(--ink); }}
.grid {{ stroke:var(--grid); stroke-width:1; }}
.ci {{ stroke:var(--ink); stroke-width:1.6; }}
</style></head>
<body><div class="slide">{''.join(svg)}</div></body></html>"""
write_text(html, OUT / 'results' / 'slide.html')
print('slide_data.json, slide_spec.md, slide.html записаны;', f"{len(html)/1024:.0f} КБ HTML, внешних зависимостей нет")
display(HTML(f'<div style="border:1px solid #ddd;max-width:1000px">{"".join(svg).replace("var(--surface)", "#fcfcfb").replace("var(--ink2)", "#52514e").replace("var(--ink)", "#0b0b0b").replace("var(--grid)", "#e6e5e0")}</div>'))
