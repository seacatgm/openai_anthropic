# ---------------------------------------------------------------- Сводка: ответ в трёх строках, файлы, критерии приёмки
o, a = R_NOWCAST['openai'], R_NOWCAST['anthropic']; S = R_SPLIT['summary']; ro, ra = R_NOWCAST['reproduction']['OpenAI'], R_NOWCAST['reproduction']['Anthropic']
answer = f"""## Ответ в трёх строках (дата слайда {DATE_TAG}; источники проверены {ACCESSED})

1. **Штуки не публикуются → считаем в ГВт и H100e.** Конец 2025: OpenAI ≈ 1,9 ГВт [S01][V2] / {ru_m(ro['epoch']['p50'])} H100e (90 % ДИ {ru_m(ro['epoch']['p05'])}–{ru_m(ro['epoch']['p95'])}) [S02][E]; Anthropic ≈ 1,4 ГВт [S11][V2] / {ru_m(ra['epoch']['p50'])} H100e ({ru_m(ra['epoch']['p05'])}–{ru_m(ra['epoch']['p95'])}) [S02][E]. Физических ускорителей ≈ {ru_m(R_CHIPS['openai_end2025']['formula_05_3']['chips']['p50'])} и ≈ {ru_m(R_CHIPS['anthropic_end2025']['chips']['p50'])} [E].
2. **На {DATE_TAG} (nowcast, наша модель [E]):** OpenAI ≈ {ru_m(o['h100e']['p50'])} H100e (90 % ДИ {ru_m(o['h100e']['p05'])}–{ru_m(o['h100e']['p95'])}) ≈ {ru_gw(o['gw_it_mw']['p50'])} IT; Anthropic ≈ {ru_m(a['h100e']['p50'])} ({ru_m(a['h100e']['p05'])}–{ru_m(a['h100e']['p95'])}) ≈ {ru_gw(a['gw_it_mw']['p50'])} IT.
3. **Сплит есть только в деньгах.** 2025: OpenAI {100*S['openai_2025']['rd_share']:.0f}/{100*S['openai_2025']['inf_share']:.0f} R&D/инференс [S04][V]; Anthropic {100*S['anthropic_2025']['rd_share']:.0f}/{100*S['anthropic_2025']['inf_share']:.0f} [S06][V]/[E]. 2026 — сценарии [E]: OpenAI {100*S['openai_2026_rd_share_range'][0]:.0f}–{100*S['openai_2026_rd_share_range'][1]:.0f} % R&D по плану [S15][S13]; Anthropic {100*S['anthropic_h1_2026_rd_share_range'][0]:.0f}–{100*S['anthropic_h1_2026_rd_share_range'][1]:.0f} % R&D [S29]: по плану OpenAI доля обучения растёт (план, вероятно, недооценивает инференс), у Anthropic — падает.
"""
md(answer)

checks = [
    ('Блок 1', 'в реестре нет записей K; у V есть URL', (not (SRC['status'] == 'K').any()) and (SRC[SRC['status'] == 'V']['url'] != '').all()),
    ('Блок 2', 'воспроизведение медиан Epoch ±3 %', ro['within_3pct'] and ra['within_3pct']),
    ('Блок 2', 'JSON содержит openai/anthropic h100e p05/p50/p95, gw_it, sensitivity', all(k in R_NOWCAST['openai']['h100e'] for k in ('p05', 'p50', 'p95')) and 'sensitivity' in R_NOWCAST),
    ('Блок 3', 'контрольные точки Colossus 1 и Абилин ±15 %', all(v['ok_15pct'] for v in R_CHIPS['control_points'].values())),
    ('Блок 3', 'OpenAI конец 2025: 1,0–1,3 млн чипов, медиана ~1,15 млн', 1.0e6 <= R_CHIPS['openai_end2025']['formula_05_3']['chips']['p50'] <= 1.3e6),
    ('Блок 4', 'сплит 2024–2025 совпадает с ранее зафиксированным (70/30, ~50/50; 60/40)', abs(S['openai_2024']['rd_share'] - 0.71) < 0.03 and abs(S['openai_2025']['rd_share'] - 0.49) < 0.03 and abs(S['anthropic_2025']['rd_share'] - 0.60) < 0.02),
    ('Блок 6', 'основной текст draft_v2: проза ≤ ~900 слов (таблицы отдельно)', DRAFT_CHECK['prose_words'] <= 900),
    ('Блок 6', 'в draft_v2 нет числа без [S-nn]/статуса', DRAFT_CHECK['lines_without_ref'] == 0),
    ('Блок 5', 'slide_data.json валиден, интервалы у всех столбиков', all(b['p05'] < b['p50'] < b['p95'] for b in json.load(open(OUT / 'results' / 'slide_data.json'))['bars_h100e'])),
]
display(pd.DataFrame(checks, columns=['задание', 'критерий', 'выполнено']))
files = sorted(p.relative_to(OUT).as_posix() for p in OUT.rglob('*') if p.is_file() and not p.name.startswith('.'))
md('**Файлы в `' + OUT.as_posix() + '/`:**\n\n' + '\n'.join(f'- `{f}`' for f in files))
