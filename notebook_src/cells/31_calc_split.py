%%writefile gpu_fleet_review_out/calc_split.py
# -*- coding: utf-8 -*-
"""calc_split.py — сплит обучение (R&D-compute) / инференс, 2024–2026, базис облачных расходов; сценарии 2026.
Запуск: python calc_split.py  |  из ноутбука: %run -i calc_split.py"""
import os, sys, json, datetime as dt
from pathlib import Path
import pandas as pd

_g = globals()
NOWCAST_DATE = _g.get('NOWCAST_DATE') or dt.date.fromisoformat(os.environ.get('NOWCAST_DATE', dt.date.today().isoformat()))
OUT = Path(_g.get('OUT') or os.environ.get('OUT', Path(__file__).resolve().parent)); DATE_TAG = NOWCAST_DATE.isoformat()

def ru(x, nd=1): return f'{x:,.{nd}f}'.replace(',', ' ').replace('.', ',')

# ------------------------------------------------------------------ входы (млрд USD)
SPLIT_INPUTS = [  # company, period, rd_compute, inference, total, basis, status, source, note
    ('OpenAI', '2024', 5.0, 2.0, 6.8, 'cloud compute spend', 'V', 'S07;S04', 'обучение $3 млрд + исследования $1 млрд (амортиз.) ≈ $5 млрд R&D; инференс $1,8–2 млрд'),          # [FACT S07]
    ('OpenAI', '2025', 8.0, 8.4, 16.3, 'cloud compute spend', 'V/V2', 'S04;S16;S09', 'R&D «около половины» $16,3 млрд (Epoch); инференс >$8 млрд (The Information) / $8,4 млрд (Sacra); рост ×4'),  # [FACT S04, S16]
    ('OpenAI', '2026 план', 32.0, None, 50.0, 'cloud compute spend (план)', 'V2', 'S15;S13', 'обучение $32 млрд (The Information, февраль); бюджет $50 млрд (Брокман, май); инференс — сценарии'),  # [FACT S15, S13]
    ('OpenAI', '2027 план', 65.0, None, None, 'план', 'V2', 'S15', 'обучение ~$65 млрд'),
    ('OpenAI', '2025 (другой базис)', None, None, None, 'WSJ chart / лизк отчётности', 'N/V2', 'S31;S34', 'WSJ: обучение $13–25 млрд «в зависимости от учёта» (пересказ Substack) [N]; R&D-расходы $19 млрд с амортизацией [V2] — не сопоставимо'),
    ('OpenAI', '2025 (другой базис: платежи Microsoft, аудировано)', 10.59, 6.047, 17.2, 'GAAP, только Microsoft', 'V', 'S34', 'лизк аудированной отчётности (15.06.2026): $10,59 млрд по строке R&D (Зитрон: «most likely… cost of training»), $6,05 млрд по cost of revenue → ≈ 64/36; отдельной строки inference/training нет; не сопоставимо с облачным базисом'),
    ('Anthropic', '2024', None, None, 2.5, 'cloud compute spend', 'V', 'S04', 'сплит не раскрыт'),                                                                               # [FACT S04]
    ('Anthropic', '2025', 4.1, 2.7, 6.8, 'cloud compute spend', 'V/E', 'S06;S04', 'R&D $4,1 млрд — прогноз компании (декабрь); инференс $2,7 млрд — Epoch из 40 % валовой маржи при выручке $4,5 млрд'),  # [FACT S06]
    ('Anthropic', 'Q1 2026', None, None, round(0.71 * 4.8, 2), 'compute/revenue (WSJ)', 'V2/E', 'S29', '71 ¢ на $1 выручки × $4,8 млрд (включая обучение)'),                    # [FACT S29]
    ('Anthropic', 'Q2 2026 (прогноз)', None, None, round(0.56 * 10.9, 2), 'compute/revenue (WSJ)', 'V2/E', 'S29', '56 ¢ × $10,9 млрд (прогноз компании); Epoch: «около $6 млрд»'),
    ('Anthropic', '2028 (другой базис)', 30.0, None, None, 'WSJ chart', 'V2', 'S31', 'обучение ~$30 млрд (2028 или 2029 по разным пересказам) против ~$121 млрд у OpenAI в 2028 — график WSJ 05.04.2026 за пейволлом, цифры по пересказам'),
]
INPUTS = pd.DataFrame(SPLIT_INPUTS, columns=['company', 'period', 'rd_compute_bn', 'inference_bn', 'total_bn', 'basis', 'status', 'source', 'note'])

OPENAI_RD_2026 = 32.0                                   # [FACT S15]
OPENAI_TOTAL_2026 = 50.0                                # [FACT S13]
OPENAI_INF_SCEN = {'A. Февральский план (Sacra $14,1 млрд, старый винтаж)': 14.1,      # [FACT S16]
                   'B. Бюджет Брокмана: $50 − $32': OPENAI_TOTAL_2026 - OPENAI_RD_2026,  # [FACT S13, S15]
                   'C. Инференс догоняет (верхняя граница)': 22.0,                       # [ASSUMPTION]
                   'D. Инференс ×2 к 2025 ($8,4 млрд × 2)': 2 * 8.4}                       # [ASSUMPTION]
ANTH_QUARTERS = {'Q1 2026': {'revenue': 4.8, 'c': 0.71}, 'Q2 2026': {'revenue': 10.9, 'c': 0.56}}   # [FACT S29]
ANTH_MARGINS = [0.50, 0.60, 0.65, 0.72]                  # [ASSUMPTION] сетка валовой маржи инференса (2025 в среднем ~40 % по всему compute)
ANTH_MIN_RD_PER_Q = 1.0                                  # [ASSUMPTION] порог: R&D-compute 2025 = $4,1 млрд/год ≈ $1,0 млрд/квартал [S06]

def split(rd, inf):
    return rd / (rd + inf), inf / (rd + inf)

def main(verbose=True):
    R = {'meta': {'date': DATE_TAG, 'basis': 'cloud compute spend, USD bn'}, 'history': [], 'openai_2026': [], 'anthropic_2026': []}
    for r in INPUTS.itertuples():
        if r.rd_compute_bn and r.inference_bn and 'другой базис' not in r.period:
            s_rd, s_inf = split(r.rd_compute_bn, r.inference_bn)
            R['history'].append({'company': r.company, 'period': r.period, 'rd_bn': r.rd_compute_bn, 'inf_bn': r.inference_bn, 'total_bn': r.total_bn,
                                 'rd_share': s_rd, 'inf_share': s_inf, 'status': r.status, 'source': r.source, 'formula': 's_RD = C_RD / (C_RD + C_inf)'})
    for name, inf in OPENAI_INF_SCEN.items():
        s_rd, s_inf = split(OPENAI_RD_2026, inf)
        R['openai_2026'].append({'scenario': name, 'rd_bn': OPENAI_RD_2026, 'inf_bn': inf, 'total_bn': OPENAI_RD_2026 + inf, 'rd_share': s_rd, 'inf_share': s_inf,
                                 'status': 'E', 'formula': f'C_RD = 32 [S15]; C_inf = {inf:g}; s_RD = 32 / (32 + {inf:g})'})
    for q, d in ANTH_QUARTERS.items():
        total = d['c'] * d['revenue']
        for m in ANTH_MARGINS:
            inf = (1 - m) * d['revenue']; rd = total - inf
            ok = rd >= ANTH_MIN_RD_PER_Q
            s_rd, s_inf = split(rd, inf) if rd > 0 else (float('nan'), float('nan'))
            R['anthropic_2026'].append({'quarter': q, 'revenue_bn': d['revenue'], 'c_compute_to_revenue': d['c'], 'total_bn': total, 'inference_gross_margin': m,
                                        'inf_bn': inf, 'rd_bn': rd, 'rd_share': s_rd, 'inf_share': s_inf, 'accepted': ok,
                                        'status': 'E', 'formula': f'C_total = {d["c"]} × {d["revenue"]} [S29]; C_inf = (1 − {m}) × {d["revenue"]}; C_RD = C_total − C_inf'})
    # полугодие 2026 Anthropic по принятым сценариям (одна маржа на оба квартала)
    h1 = []
    for m in ANTH_MARGINS:
        rows = [x for x in R['anthropic_2026'] if x['inference_gross_margin'] == m]
        if all(x['accepted'] for x in rows):
            rd = sum(x['rd_bn'] for x in rows); inf = sum(x['inf_bn'] for x in rows)
            h1.append({'inference_gross_margin': m, 'rd_bn': rd, 'inf_bn': inf, 'rd_share': rd / (rd + inf), 'inf_share': inf / (rd + inf)})
    R['anthropic_h1_2026_accepted'] = h1
    acc_q = [x for x in R['anthropic_2026'] if x['accepted']]
    R['summary'] = {
        'openai_2024': next(x for x in R['history'] if x['company'] == 'OpenAI' and x['period'] == '2024'),
        'openai_2025': next(x for x in R['history'] if x['company'] == 'OpenAI' and x['period'] == '2025'),
        'anthropic_2025': next(x for x in R['history'] if x['company'] == 'Anthropic' and x['period'] == '2025'),
        'openai_2026_rd_share_range': (min(x['rd_share'] for x in R['openai_2026']), max(x['rd_share'] for x in R['openai_2026'])),
        'anthropic_2026_rd_share_range_quarters': (min(x['rd_share'] for x in acc_q), max(x['rd_share'] for x in acc_q)),
        'anthropic_h1_2026_rd_share_range': (min(x['rd_share'] for x in h1), max(x['rd_share'] for x in h1)),
        'anthropic_h1_2026_central_m65': next((x for x in h1 if x['inference_gross_margin'] == 0.65), None),
        'rejected_scenarios': [f"{x['quarter']}, маржа {100*x['inference_gross_margin']:.0f} %: R&D ${ru(x['rd_bn'],2)} млрд/кв. < ${ru(ANTH_MIN_RD_PER_Q,1)} млрд" for x in R['anthropic_2026'] if not x['accepted']],
    }
    (OUT / 'data').mkdir(parents=True, exist_ok=True); (OUT / 'results').mkdir(parents=True, exist_ok=True)
    INPUTS.to_csv(OUT / 'data' / 'split_inputs.csv', index=False)
    (OUT / 'results' / f'split_{DATE_TAG}.json').write_text(json.dumps(R, ensure_ascii=False, indent=2, default=float), encoding='utf-8')
    (OUT / 'results' / f'split_{DATE_TAG}.md').write_text(split_markdown(R), encoding='utf-8')
    if verbose:
        S = R['summary']
        print(f"OpenAI 2024: {100*S['openai_2024']['rd_share']:.0f}/{100*S['openai_2024']['inf_share']:.0f}  2025: {100*S['openai_2025']['rd_share']:.0f}/{100*S['openai_2025']['inf_share']:.0f}  "
              f"2026 (сценарии): R&D {100*S['openai_2026_rd_share_range'][0]:.0f}–{100*S['openai_2026_rd_share_range'][1]:.0f} %")
        print(f"Anthropic 2025: {100*S['anthropic_2025']['rd_share']:.0f}/{100*S['anthropic_2025']['inf_share']:.0f}  2026 по кварталам (принятые): R&D "
              f"{100*S['anthropic_2026_rd_share_range_quarters'][0]:.0f}–{100*S['anthropic_2026_rd_share_range_quarters'][1]:.0f} %; I полугодие: {100*S['anthropic_h1_2026_rd_share_range'][0]:.0f}–{100*S['anthropic_h1_2026_rd_share_range'][1]:.0f} %")
        print('Отброшено:', '; '.join(S['rejected_scenarios']) or '—')
    return R

def split_markdown(R):
    S = R['summary']; o24, o25, a25 = S['openai_2024'], S['openai_2025'], S['anthropic_2025']
    lines = [f"# Сплит обучение (R&D-compute) / инференс, базис — облачные расходы на compute ({R['meta']['date']})", '',
             '| Компания | Период | R&D-compute | Инференс | Всего | Сплит R&D / инф., % | Статус | Источник |', '|---|---|---|---|---|---|---|---|']
    for x in R['history']:
        lines.append(f"| {x['company']} | {x['period']} | ${ru(x['rd_bn'])} млрд | ${ru(x['inf_bn'])} млрд | ${ru(x['total_bn'])} млрд | {100*x['rd_share']:.0f} / {100*x['inf_share']:.0f} | [{x['status']}] | [{x['source'].replace(';', '], [')}] |")
    for x in R['openai_2026']:
        lines.append(f"| OpenAI | 2026, сценарий {x['scenario']} | ${ru(x['rd_bn'])} млрд | ${ru(x['inf_bn'])} млрд | ${ru(x['total_bn'])} млрд | {100*x['rd_share']:.0f} / {100*x['inf_share']:.0f} | [E] | [S15], [S13], [S16] |")
    for x in R['anthropic_2026']:
        tag = '' if x['accepted'] else ' — **отброшен** (R&D < $1 млрд/кв.)'
        lines.append(f"| Anthropic | {x['quarter']}, маржа инференса {100*x['inference_gross_margin']:.0f} %{tag} | ${ru(x['rd_bn'],2)} млрд | ${ru(x['inf_bn'],2)} млрд | ${ru(x['total_bn'],2)} млрд | {100*x['rd_share']:.0f} / {100*x['inf_share']:.0f} | [E] | [S29] |")
    for x in R['anthropic_h1_2026_accepted']:
        lines.append(f"| Anthropic | I полугодие 2026, маржа {100*x['inference_gross_margin']:.0f} % | ${ru(x['rd_bn'],2)} млрд | ${ru(x['inf_bn'],2)} млрд | ${ru(x['rd_bn']+x['inf_bn'],2)} млрд | {100*x['rd_share']:.0f} / {100*x['inf_share']:.0f} | [E] | [S29] |")
    lo_o, hi_o = S['openai_2026_rd_share_range']; lo_a, hi_a = S['anthropic_h1_2026_rd_share_range']; lo_q, hi_q = S['anthropic_2026_rd_share_range_quarters']
    lines += ['', '## Выводы', '',
        f"(а) **2025.** OpenAI делила облачные расходы на compute примерно поровну: ~${ru(o25['rd_bn'])} млрд R&D и ${ru(o25['inf_bn'])} млрд инференс из ${ru(o25['total_bn'])} млрд → {100*o25['rd_share']:.0f}/{100*o25['inf_share']:.0f} [S04][V], [S16][V2]; в 2024 — {100*o24['rd_share']:.0f}/{100*o24['inf_share']:.0f} (${ru(o24['rd_bn'])} / ${ru(o24['inf_bn'])} млрд) [S07][V]. Anthropic 2025: ${ru(a25['rd_bn'])} млрд R&D против ~${ru(a25['inf_bn'])} млрд инференса → {100*a25['rd_share']:.0f}/{100*a25['inf_share']:.0f} [S06][V]/[E] (инференс выведен Epoch из 40 % валовой маржи).",
        f"(б) **OpenAI 2026 — по плану {100*lo_o:.0f}–{100*hi_o:.0f} % R&D.** Обучение $32 млрд [S15][V2] при инференсе $14,1–22 млрд по сценариям A–D (бюджет $50 млрд [S13][V2]); винтажи прогнозов различаются (Sacra — до февральского пересмотра), а инференс в 2025 рос ×4, поэтому план может быть занижен в пользу R&D [E].",
        f"(в) **Anthropic 2026 — {100*lo_a:.0f}–{100*hi_a:.0f} % R&D по сценариям** (I полугодие; по кварталам {100*lo_q:.0f}–{100*hi_q:.0f} %); центральный сценарий (маржа инференса 65 %) — {100*S['anthropic_h1_2026_central_m65']['rd_share']:.0f}/{100*S['anthropic_h1_2026_central_m65']['inf_share']:.0f}. Сдвиг к инференсу против 60/40 в 2025 следует из падения compute/выручка с ~1,5 (2025) до 0,71 и 0,56 [S29][V2]. Отброшены сценарии с R&D < $1 млрд/квартал: " + '; '.join(S['rejected_scenarios']) + ' [E].',
        f"(г₀) **Проверка по аудированной отчётности.** В лизке отчётности OpenAI за 2025 [S34][V] нет строки инференс/обучение; ближайший аналог — платежи Microsoft: $10,59 млрд по R&D и $6,05 млрд по cost of revenue (≈ 64/36), но это GAAP-базис только по одному поставщику, поэтому оценка 50/50 на облачном базисе не заменяется.",
        "(г) **Оговорки.** «Обучение» = весь R&D-compute, финальные прогоны — меньшая часть [S08][V]; винтажи прогнозов OpenAI на 2026 не совпадают ($14,1 млрд — до февраля; $32 млрд — февраль; $50 млрд — май); валовая маржа инференса Anthropic в 2026 не раскрыта — сплит 2026 только сценарный; строки другого базиса (WSJ $13–25 млрд, R&D-расходы $19 млрд с амортизацией) не смешиваются с облачным базисом.", '']
    return '\n'.join(lines)

if __name__ == '__main__':
    R_SPLIT = main()
