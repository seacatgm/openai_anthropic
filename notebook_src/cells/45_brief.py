# ---------------------------------------------------------------- пакет для дизайнера: results/slide_brief/
BRIEF = OUT / 'results' / 'slide_brief'; BRIEF.mkdir(parents=True, exist_ok=True)
o, a = R_NOWCAST['openai'], R_NOWCAST['anthropic']; ro, ra = R_NOWCAST['reproduction']['OpenAI'], R_NOWCAST['reproduction']['Anthropic']
S = R_SPLIT['summary']; C = R_CHIPS; cc_o, cc_a = o['cross_check_by_sites'], a['cross_check_by_sites']
lo_o, hi_o = S['openai_2026_rd_share_range']; lo_a, hi_a = S['anthropic_h1_2026_rd_share_range']; c65 = S['anthropic_h1_2026_central_m65']
D_RU = NOWCAST_DATE.strftime('%d.%m.%Y')
def mln(x, nd=2): return ru(x / 1e6, nd) + ' млн'
def gw(x, nd=1): return ru(x / 1000, nd) + ' ГВт'
def pc(x): return f'{100*x:.0f}'
def srow(sid):
    r = SRC[SRC['id'] == sid].iloc[0]; return {'publisher': r['publisher'], 'date': r['date'], 'title': r['title'], 'url': r['url'], 'accessed': r['accessed']}
def sname(sid):  # короткое имя источника словами (без кодов)
    return {'S01': 'блог OpenAI (финансовый директор Сара Фрайар), 18.01.2026', 'S02': 'Epoch AI, AI Chip Users, 09.09.2026', 'S04': 'Epoch AI, методология AI Chip Users, сентябрь 2026',
            'S11': 'Bloomberg, меморандум OpenAI инвесторам, 09.04.2026', 'S13': 'Bloomberg, показания Грега Брокмана, 05.05.2026', 'S15': 'The Information (через The Decoder), 21.02.2026',
            'S16': 'Sacra, 29.07.2026', 'S06': 'Epoch AI (по данным The Information), 04.02.2026', 'S07': 'Epoch AI (по данным The Information), 10.10.2025', 'S29': 'The Wall Street Journal, 20.05.2026',
            'S08': 'Epoch AI, 23.03.2026', 'S37': 'Epoch AI, каталог ЦОД, 24.09.2026', 'S25': 'Anthropic, 20.04.2026', 'S27': 'блог xAI (SpaceX) и Anthropic, 06.05.2026', 'S12': 'OpenAI, 29.04.2026', 'S18': 'пресс-релиз NVIDIA, 22.09.2025', 'S40': 'пресс-релиз AMD, 06.10.2025', 'S41': 'Broadcom, 13.10.2025', 'S43': 'Anthropic, 23.10.2025', 'S44': 'Anthropic, 18.11.2025', 'S16': 'Sacra, 29.07.2026', 'S17': 'Financial Times (пересказ Business Standard), 20.02.2026'}[sid]
SLIDE_SOURCES = ['S01', 'S02', 'S11', 'S13', 'S15', 'S06', 'S29', 'S04', 'S16', 'S07', 'S08', 'S37', 'S12', 'S18', 'S17', 'S40', 'S41', 'S25', 'S43', 'S44', 'S27']

content = {
    'as_of': NOWCAST_DATE.isoformat(), 'sources_checked_on': ACCESSED, 'language': 'ru', 'format': 'один слайд 16:9',
    'headline': f'Число чипов не публикуется. В эквивалентах H100: OpenAI ≈ {ru(ro["epoch"]["p50"]/1e6,1)} млн, Anthropic ≈ {ru(ra["epoch"]["p50"]/1e6,1)} млн на конец 2025; сегодня, по нашей оценке, примерно в 2,5 раза больше у обеих. Деление между обучением и инференсом известно только в деньгах: в 2025 году {pc(S["openai_2025"]["rd_share"])}/{pc(S["openai_2025"]["inf_share"])} у OpenAI и {pc(S["anthropic_2025"]["rd_share"])}/{pc(S["anthropic_2025"]["inf_share"])} у Anthropic; в 2026 по плану OpenAI доля обучения {pc(lo_o)}–{pc(hi_o)} %, у Anthropic по сценариям {pc(lo_a)}–{pc(hi_a)} %.',
    'headline_short': f'Число чипов не публикуется. В эквивалентах H100: OpenAI ≈ {ru(ro["epoch"]["p50"]/1e6,1)} млн, Anthropic ≈ {ru(ra["epoch"]["p50"]/1e6,1)} млн на конец 2025, сегодня по нашей оценке ≈ в 2,5 раза больше. Деление между обучением и инференсом известно только в деньгах.',
    'h100e_definition': 'Эквивалент H100 — вычислительная мощность одного NVIDIA H100 (единица Epoch AI); один GB200 = 2,53 эквивалента, один Trainium2 = 0,66.',
    'gw_definition': 'ГВт — потребление вычислительного оборудования (серверы и сеть), без охлаждения и потерь здания.',
    'key_messages_note': 'для понимания контекста; на слайд текстом не выносить — эти данные уже представлены в графиках',
    'key_messages': [
        f'Конец 2025 (сопоставимая точка): OpenAI ≈ 1,9 ГВт (раскрыто компанией) ≈ {mln(ro["epoch"]["p50"])} эквивалентов H100 (оценка Epoch AI, 90 % интервал {mr(ro["epoch"]["p05"], ro["epoch"]["p95"])}); Anthropic ≈ 1,4 ГВт (оценка OpenAI) ≈ {mln(ra["epoch"]["p50"])} ({mr(ra["epoch"]["p05"], ra["epoch"]["p95"])}).',
        f'{D_RU} (наша модель, экстраполяция от Epoch AI): OpenAI ≈ {mln(o["h100e"]["p50"])} ({mr(o["h100e"]["p05"], o["h100e"]["p95"])}) ≈ {gw(o["gw_it_mw"]["p50"])}; Anthropic ≈ {mln(a["h100e"]["p50"])} ({mr(a["h100e"]["p05"], a["h100e"]["p95"])}) ≈ {gw(a["gw_it_mw"]["p50"])}.',
        f'Сплит расходов на вычисления «обучение и исследования / инференс»: OpenAI {pc(S["openai_2024"]["rd_share"])}/{pc(S["openai_2024"]["inf_share"])} (2024), {pc(S["openai_2025"]["rd_share"])}/{pc(S["openai_2025"]["inf_share"])} (2025), в 2026 по плану обучение {pc(lo_o)}–{pc(hi_o)} %; Anthropic {pc(S["anthropic_2025"]["rd_share"])}/{pc(S["anthropic_2025"]["inf_share"])} (2025), в 2026 по сценариям обучение {pc(lo_a)}–{pc(hi_a)} %.',
    ],
    'left_chart': {
        'title': 'Парк в эквивалентах H100: медиана и 90 % интервал', 'y_axis': 'млн эквивалентов H100',
        'bars': [
            {'company': 'OpenAI', 'period': 'конец 2025', 'median_mln': round(ro['epoch']['p50'] / 1e6, 2), 'p05_mln': round(ro['epoch']['p05'] / 1e6, 2), 'p95_mln': round(ro['epoch']['p95'] / 1e6, 2), 'status': 'оценка Epoch AI', 'fill': 'сплошная', 'gw_label': '1,9 ГВт — раскрыто компанией', 'source': sname('S02'), 'gw_source': sname('S01')},
            {'company': 'OpenAI', 'period': D_RU, 'median_mln': round(o['h100e']['p50'] / 1e6, 2), 'p05_mln': round(o['h100e']['p05'] / 1e6, 2), 'p95_mln': round(o['h100e']['p95'] / 1e6, 2), 'status': 'наша оценка (экстраполяция)', 'fill': 'штриховка', 'gw_label': f'≈ {gw(o["gw_it_mw"]["p50"])} ({ru(o["gw_it_mw"]["p05"]/1000,1)}–{ru(o["gw_it_mw"]["p95"]/1000,1)}) — наша оценка', 'source': 'наша модель на основе Epoch AI'},
            {'company': 'Anthropic', 'period': 'конец 2025', 'median_mln': round(ra['epoch']['p50'] / 1e6, 2), 'p05_mln': round(ra['epoch']['p05'] / 1e6, 2), 'p95_mln': round(ra['epoch']['p95'] / 1e6, 2), 'status': 'оценка Epoch AI', 'fill': 'сплошная', 'gw_label': '≈ 1,4 ГВт — оценка OpenAI (конкурента)', 'source': sname('S02'), 'gw_source': sname('S11')},
            {'company': 'Anthropic', 'period': D_RU, 'median_mln': round(a['h100e']['p50'] / 1e6, 2), 'p05_mln': round(a['h100e']['p05'] / 1e6, 2), 'p95_mln': round(a['h100e']['p95'] / 1e6, 2), 'status': 'наша оценка (экстраполяция)', 'fill': 'штриховка', 'gw_label': f'≈ {gw(a["gw_it_mw"]["p50"])} ({ru(a["gw_it_mw"]["p05"]/1000,1)}–{ru(a["gw_it_mw"]["p95"]/1000,1)}) — наша оценка', 'source': 'наша модель на основе Epoch AI'},
        ],
        'y_max_suggested': math.ceil(max(o['h100e']['p95'], a['h100e']['p95']) / 1e6) + 0.5,
    },
    'right_chart': {
        'title': 'Доля расходов на вычисления: обучение и исследования / инференс', 'x_axis': '0–100 %',
        'bars': [
            {'company': 'OpenAI', 'year': '2024', 'training_pct': [round(100 * S['openai_2024']['rd_share']), round(100 * S['openai_2024']['rd_share'])], 'inference_pct': [round(100 * S['openai_2024']['inf_share']), round(100 * S['openai_2024']['inf_share'])], 'status': 'оценка Epoch AI по данным The Information', 'fill': 'сплошная', 'source': sname('S07')},
            {'company': 'OpenAI', 'year': '2025', 'training_pct': [round(100 * S['openai_2025']['rd_share']), round(100 * S['openai_2025']['rd_share'])], 'inference_pct': [round(100 * S['openai_2025']['inf_share']), round(100 * S['openai_2025']['inf_share'])], 'status': 'оценка Epoch AI (The Information, Sacra)', 'fill': 'сплошная', 'source': sname('S04') + '; ' + sname('S16')},
            {'company': 'OpenAI', 'year': '2026, план (сценарии)', 'training_pct': [round(100 * lo_o), round(100 * hi_o)], 'inference_pct': [round(100 * (1 - hi_o)), round(100 * (1 - lo_o))], 'status': 'сценарии по плану', 'fill': 'обучение 0–max штриховкой цветом компании, на min — контурная отметка; инференс серый от max до 100 %', 'source': sname('S15') + '; ' + sname('S13')},
            {'company': 'Anthropic', 'year': '2024', 'training_pct': None, 'inference_pct': None, 'status': 'не раскрыто', 'fill': 'контур 1 px серым #8f8e88 без заливки, внутри по центру текст «не раскрыто» тёмно-серым', 'source': sname('S04')},
            {'company': 'Anthropic', 'year': '2025', 'training_pct': [round(100 * S['anthropic_2025']['rd_share']), round(100 * S['anthropic_2025']['rd_share'])], 'inference_pct': [round(100 * S['anthropic_2025']['inf_share']), round(100 * S['anthropic_2025']['inf_share'])], 'status': 'оценка: прогноз компании по The Information и расчёт Epoch AI', 'fill': 'сплошная', 'source': sname('S06')},
            {'company': 'Anthropic', 'year': '2026, первое полугодие (сценарии)', 'training_pct': [round(100 * lo_a), round(100 * hi_a)], 'inference_pct': [round(100 * (1 - hi_a)), round(100 * (1 - lo_a))], 'status': 'сценарии по квартальным данным The Wall Street Journal', 'fill': 'обучение 0–max штриховкой цветом компании, на min — контурная отметка; инференс серый от max до 100 %', 'source': sname('S29')},
        ],
    },
    'legend': {'company_colors': {'OpenAI': '#2470cc', 'Anthropic': '#c9491a'}, 'inference_neutral': '#8f8e88',
               'status_encoding': {'факт (раскрыто компанией или подтверждено прессой)': 'сплошная заливка', 'оценка Epoch AI': 'сплошная заливка, усы — 90 % интервал', 'наша оценка / сценарий': 'диагональная штриховка'}},
    'caveats': ['«Обучение» здесь — весь бюджет исследований и разработки (эксперименты, дообучение); финальный прогон одной модели — меньшая его часть.',
                'Инференс на площадках партнёров (Amazon Bedrock, Google Vertex) учтён у Anthropic и не учтён у OpenAI (Microsoft Azure): сравнение парков на левом графике занижает OpenAI на 10–25 %.'],
    'footer': f'Источники: {"; ".join(sname(s) for s in ["S01", "S02", "S04", "S11", "S13", "S15", "S16", "S07", "S06", "S29", "S08"])}. Все ссылки проверены {date_ru(ACCESSED)}. Оценка на {D_RU} — 200 000 прогонов модели с интервалами.',
    'optional_numbers': {
        'physical_accelerators_end2025': {'OpenAI': f'≈ {mln(C["openai_end2025"]["formula_05_3"]["chips"]["p50"])} ({mln(C["openai_end2025"]["formula_05_3"]["chips"]["p05"])}–{mln(C["openai_end2025"]["formula_05_3"]["chips"]["p95"])})', 'Anthropic': f'≈ {mln(C["anthropic_end2025"]["chips"]["p50"])} ({mln(C["anthropic_end2025"]["chips"]["p05"])}–{mln(C["anthropic_end2025"]["chips"]["p95"])})', 'status': 'наш расчёт по параметрам Epoch AI'},
        'cloud_compute_spend_2025_bn_usd': {'OpenAI': 16.3, 'Anthropic': 6.8, 'status': 'Epoch AI по данным The Information'},
        'split_amounts_bn_usd': {'OpenAI 2024': 'обучение ≈ 5, инференс ≈ 2', 'OpenAI 2025': 'обучение ≈ 8, инференс 8,4', 'OpenAI 2026 план': 'обучение 32, инференс 14,1–22 (сценарии)', 'Anthropic 2025': 'обучение 4,1, инференс ≈ 2,7', 'Anthropic 2026 I полугодие (сценарии)': 'обучение ' + f"{ru(min(x['rd_bn'] for x in R_SPLIT['anthropic_h1_2026_accepted']),1)}–{ru(max(x['rd_bn'] for x in R_SPLIT['anthropic_h1_2026_accepted']),1)}" + ', инференс ' + f"{ru(min(x['inf_bn'] for x in R_SPLIT['anthropic_h1_2026_accepted']),1)}–{ru(max(x['inf_bn'] for x in R_SPLIT['anthropic_h1_2026_accepted']),1)}"},
        'growth_prior_per_year': {'OpenAI': '2,5–4,5 раза (Epoch AI: «более чем утроится» за 2026; бюджет $50 млрд ≈ ×3)', 'Anthropic': '2,5–5 раз (вводы TPU, Trainium, Colossus 1, Azure; прогноз OpenAI 3–4 ГВт)'},
        'cross_check_by_sites': {'OpenAI': f'не меньше {mln(cc_o["lower_bound_facts_only"])} (нижняя граница по каталогу ЦОД Epoch AI)', 'Anthropic': f'{mln(cc_a["total"]["p50"])} ({mln(cc_a["total"]["p05"])}–{mln(cc_a["total"]["p95"])})'},
        'end_2026_outlook': ['OpenAI (заявлено компаниями): 10 ГВт законтрактовано в США к апрелю 2026 (' + sname('S12') + '); первые гигаватты во 2-м полугодии 2026 — AMD MI450 (' + sname('S40') + '), Broadcom (' + sname('S41') + '). Письмо о намерениях с NVIDIA на 10 ГВт систем Vera Rubin (' + sname('S18') + ') в договор не оформлено и заменено инвестицией $30 млрд (' + sname('S17') + '); мощности по нему не планируются',
                             'Anthropic (заявлено компаниями): «почти 1 ГВт» Trainium к концу 2026 (' + sname('S25') + '), «значительно больше 1 ГВт» TPU в 2026 (' + sname('S43') + '), до 1 ГВт Azure (' + sname('S44') + '), Colossus 1 (~300 МВт) с июня 2026 (' + sname('S27') + '); прогноз OpenAI (оценка конкурента) — 3–4 ГВт (' + sname('S11') + ')'],
    },
    'sources': [dict(srow(sid), name=sname(sid)) for sid in SLIDE_SOURCES],
    'forbidden_on_slide': ['коды источников и статусов вроде [S07], [V2], [E]', 'термины nowcast, H100e, R&D-compute, Δt, PUE без расшифровки', 'любые числа, которых нет в этом пакете', 'суммирование гигаватт из пресс-релизов как «парка»', 'точечные утверждения о 2026 годе без слова «оценка» или «сценарий»'],
}
def _typo(x):
    if isinstance(x, str):
        x = re.sub(r'(\d)[ \u2009](\d{3})(?!\d)', '\\1\u202f\\2', x); x = re.sub(r'(\d) %', '\\1\u00a0%', x); x = x.replace('≈ ', '≈\u00a0'); x = re.sub(r'(\d) (ГВт|МВт|млн|млрд|тыс\.|Вт|раза|раз\b)', '\\1\u00a0\\2', x); return x
    if isinstance(x, list): return [_typo(v) for v in x]
    if isinstance(x, dict): return {k: _typo(v) for k, v in x.items()}
    return x
content = _typo(content)
save_json(content, BRIEF / 'slide_content.json')

# ---- slide_content.md: все факты и числа словами
lc, rc = content['left_chart'], content['right_chart']
md_lines = [f'# Данные для слайда (по состоянию на {D_RU}; источники проверены {date_ru(ACCESSED)})', '',
    'Строки ниже копировать как есть: неразрывные пробелы и формат чисел уже применены.', '',
    '## Заголовок (полный; если не помещается в две строки — использовать короткий вариант ниже)', '', content['headline'], '', '**Короткий заголовок (≤ 2 строк):** ' + content['headline_short'], '',
    '## Три ключевых сообщения (' + content['key_messages_note'] + ')', ''] + [f'{i+1}. {m}' for i, m in enumerate(content['key_messages'])] + ['',
    '## Левая часть: парк в эквивалентах H100 (4 столбика с усами интервала)', '',
    '| Компания | Период | Медиана, млн | 90 % интервал, млн | Что это | Заливка | Подпись мощности под столбиком |', '|---|---|---|---|---|---|---|'] + \
    [f'| {b["company"]} | {b["period"]} | {ru(b["median_mln"],2)} | {ru(b["p05_mln"],2)}–{ru(b["p95_mln"],2)} | {b["status"]}; {b["source"]} | {b["fill"]} | {b["gw_label"]}' + (f' ({b["gw_source"]})' if b.get('gw_source') else '') + ' |' for b in lc['bars']] + ['',
    f'Ось Y: «{lc["y_axis"]}», от 0 до {ru(lc["y_max_suggested"],1)}. Усы — 5-й и 95-й процентили; подпись медианы — над верхней засечкой уса, по центру столбика. Под каждым столбиком четыре строки: компания / период / подпись мощности / статус словами; источники под столбики не выносить — они в подвале.', '',
    'Расшифровки одной строкой под графиком (обе обязательны): «' + content['h100e_definition'] + '» и «' + content['gw_definition'] + '». Числа 2,53 и 0,66 на слайд не выносить.', '',
    '## Правая часть: доля расходов на вычисления — обучение и исследования / инференс (горизонтальные stacked-бары)', '',
    '| Компания | Год | Обучение и исследования, % | Инференс, % | Что это | Заливка |', '|---|---|---|---|---|---|'] + \
    [(f'| {b["company"]} | {b["year"]} | {b["training_pct"][0]}' + (f'–{b["training_pct"][1]}' if b['training_pct'][1] != b['training_pct'][0] else '') + f' | {b["inference_pct"][0]}' + (f'–{b["inference_pct"][1]}' if b['inference_pct'][1] != b['inference_pct'][0] else '') + f' | {b["status"]}; {b["source"]} | {b["fill"]} |') if b['training_pct'] else f'| {b["company"]} | {b["year"]} | не раскрыто | не раскрыто | {b["status"]}; {b["source"]} | {b["fill"]} |' for b in rc['bars']] + ['',
    'Ось X: 0–100 %. Строки 2026 года: сегмент обучения от 0 до максимальной доли — штриховка цветом компании, на минимальной доле — контурная отметка (тонкая вертикальная линия); инференс — серый от максимальной доли до 100 %. Подписи процентов — снаружи бара тёмно-серым: слева «обучение 71 %», справа «инференс 29 %»; для 2026 — «59–69 %» и «31–41 %». Anthropic 2024 — контур 1 px серым без заливки и текст «не раскрыто» по центру.', '',
    '## Легенда статусов (обязательна на слайде)', ''] + [f'- {k}: {v}' for k, v in content['legend']['status_encoding'].items()] + [
    f'- Цвет компании: OpenAI {content["legend"]["company_colors"]["OpenAI"]}, Anthropic {content["legend"]["company_colors"]["Anthropic"]}; инференс в stacked-барах — нейтральный {content["legend"]["inference_neutral"]}.', '',
    '## Две оговорки (по одной строке каждая, дословно или короче)', ''] + [f'{i+1}. {c}' for i, c in enumerate(content['caveats'])] + ['',
    '## Подвал', '', content['footer'], '',
    '## Числа про запас (использовать только если есть место; статус указан)', ''] + \
    [f'- Физических ускорителей, конец 2025: OpenAI {content["optional_numbers"]["physical_accelerators_end2025"]["OpenAI"]}, Anthropic {content["optional_numbers"]["physical_accelerators_end2025"]["Anthropic"]} — {content["optional_numbers"]["physical_accelerators_end2025"]["status"]}.',
     f'- Расходы на облачные вычисления 2025: OpenAI $16,3 млрд, Anthropic $6,8 млрд — {content["optional_numbers"]["cloud_compute_spend_2025_bn_usd"]["status"]}.'] + \
    [f'- {k}: {v} (млрд $)' for k, v in content['optional_numbers']['split_amounts_bn_usd'].items()] + \
    [f'- Темп роста в модели: OpenAI {content["optional_numbers"]["growth_prior_per_year"]["OpenAI"]}; Anthropic {content["optional_numbers"]["growth_prior_per_year"]["Anthropic"]}.',
     f'- Проверка по известным площадкам: OpenAI {content["optional_numbers"]["cross_check_by_sites"]["OpenAI"]}; Anthropic {content["optional_numbers"]["cross_check_by_sites"]["Anthropic"]}.'] + \
    [f'- {x}' for x in content['optional_numbers']['end_2026_outlook']] + ['',
    '## Чего на слайде быть не должно', ''] + [f'- {x}' for x in content['forbidden_on_slide']] + ['',
    '## Источники (полные)', '', '| Издатель | Дата | Заголовок | Ссылка |', '|---|---|---|---|'] + \
    [f'| {v["publisher"]} | {v["date"]} | {v["title"]} | {v["url"]} |' for v in content['sources']] + ['']
write_text(_typo('\n'.join(md_lines)), BRIEF / 'slide_content.md')
pd.DataFrame([{'publisher': v['publisher'], 'date': v['date'], 'title': v['title'], 'url': v['url'], 'accessed': v['accessed'], 'used_for': {
    'S01': 'мощность OpenAI 0,2/0,6/1,9 ГВт', 'S02': 'эквиваленты H100 на конец 2025 (медианы, интервалы)', 'S11': '1,4 ГВт Anthropic (оценка OpenAI)', 'S13': 'бюджет OpenAI $50 млрд на 2026',
    'S15': 'обучение OpenAI $32 млрд в 2026', 'S06': 'расходы Anthropic 2025: $4,1 / $2,7 млрд', 'S29': 'квартальные расходы Anthropic 2026', 'S04': 'методология Epoch AI, состав парков, сторонний инференс',
    'S16': 'инференс OpenAI $8,4 млрд (2025), $14,1 млрд (план)', 'S07': 'OpenAI 2024: $5 / $2 млрд', 'S08': 'финальные прогоны — меньшая часть R&D', 'S37': 'каталог ЦОД Epoch AI (проверка по площадкам)',
    'S12': '10 ГВт законтрактовано в США', 'S18': 'исходное письмо о намерениях NVIDIA на 10 ГВт (не оформлено)', 'S17': 'LOI NVIDIA не оформлен, заменён инвестицией $30 млрд', 'S40': 'AMD MI450: первый ГВт во 2H 2026', 'S41': 'Broadcom: 10 ГВт с 2H 2026', 'S25': 'Anthropic–Amazon: «почти 1 ГВт» к концу 2026', 'S43': 'Anthropic–Google: TPU >1 ГВт в 2026', 'S44': 'Anthropic–Microsoft: до 1 ГВт Azure', 'S27': 'Colossus 1: >220 тыс. GPU, ~300 МВт'}[k]}
    for k, v in zip(SLIDE_SOURCES, content['sources'])]).to_csv(BRIEF / 'sources.csv', index=False)

# ---- PROMPT.md
prompt = f"""# Задание дизайн-агенту: один слайд «GPU-парк OpenAI и Anthropic»

## Что нужно сделать
Сделать **ровно один слайд** формата 16:9 (1920×1080) для CTO по данным из этого пакета. Никаких дополнительных слайдов, приложений или заметок докладчика. Результат — файл слайда (предпочтительно PPTX с одним слайдом; допустимо SVG или PNG 1920×1080) и три строки о том, что где размещено.

## Кто смотрит и зачем
CTO. На слайд смотрят одну–две минуты. Он должен за один взгляд ответить на вопрос «Сколько GPU у OpenAI и Anthropic и как они делятся между обучением и инференсом» и показать, каким числам можно верить, а какие — оценка.

## Единственный источник данных
Все числа, формулировки, подписи и источники — в `slide_content.md` (для чтения) и `slide_content.json` (для скрипта). Использовать только их. Ничего не досчитывать, не округлять сильнее, чем в пакете, не добавлять чисел «по памяти». Если что-то не помещается, сокращать по приоритету из раздела «Если не помещается», а не менять значения.

## Композиция (сверху вниз)
1. **Заголовок-ответ** — не больше двух строк. Взять «Короткий заголовок» из `slide_content.md` дословно; полный вариант использовать только если он умещается в две строки при кегле заголовка.
2. **Левая половина (≈ 55 % ширины)** — столбиковая диаграмма с подзаголовком «Парк в эквивалентах H100: медиана и 90 % интервал»: четыре столбика (OpenAI конец 2025, OpenAI {D_RU}, Anthropic конец 2025, Anthropic {D_RU}); высота — медиана, усы с засечками — 90 % интервал; подпись медианы (например, «4,27 млн») — над верхней засечкой уса, по центру столбика. Под каждым столбиком ровно четыре строки: компания / период / подпись мощности / статус словами, например «OpenAI / конец 2025 / 1,9 ГВт — раскрыто компанией / оценка Epoch AI» и «OpenAI / {D_RU} / ≈ 4,6 ГВт (3,3–6,6) — наша оценка / наша оценка (экстраполяция)». Источники под столбики не выносить — они в подвале. Под графиком две строки-расшифровки из `slide_content.md` (эквивалент H100 и ГВт). Значения — таблица «Левая часть».
3. **Правая половина (≈ 45 %)** — горизонтальные stacked-бары с подзаголовком «Доля расходов на вычисления: обучение и исследования / инференс», шесть строк с подписями слева: «OpenAI 2024», «OpenAI 2025», «OpenAI 2026, план (сценарии)», «Anthropic 2024», «Anthropic 2025», «Anthropic 2026, первое полугодие (сценарии)». Строки с точным значением: обучение — сплошной цвет компании от 0 до доли, инференс — серый до 100 %. Строки 2026: обучение от 0 до максимальной доли — штриховка цветом компании, на минимальной доле — тонкая контурная отметка; инференс — серый от максимальной доли до 100 %. Anthropic 2024 — контур 1 px серым без заливки, внутри текст «не раскрыто». Подписи процентов — снаружи бара тёмно-серым: слева «обучение 71 %», справа «инференс 29 %»; для 2026 — «59–69 %» и «31–41 %». Значения — таблица «Правая часть».
4. **Легенда статусов** — одна строка через «·»: «факт (раскрыто компанией или подтверждено прессой) — сплошная заливка · оценка Epoch AI — сплошная заливка, усы — 90 % интервал · наша оценка / сценарий — диагональная штриховка».
5. **Две оговорки** — по одной строке каждая, текст из раздела «Две оговорки».
6. **Подвал** — текст из раздела «Подвал» (источники словами: издатель и дата; дата проверки). Мелко, но читаемо.

## Размеры
Слайд 1920 × 1080 px (13,33 × 7,5 дюйма, 1 pt = 2 px). Три кегля: заголовок 36–40 pt (72–80 px), подписи графиков и оговорки 14–16 pt (28–32 px), подвал и оси 11–12 pt (22–24 px). Поля не меньше 48 px.

## Правила оформления
- Цвет кодирует компанию: OpenAI — синий {content['legend']['company_colors']['OpenAI']}, Anthropic — оранжевый {content['legend']['company_colors']['Anthropic']}; инференс в stacked-барах — нейтральный серый {content['legend']['inference_neutral']}. Больше цветов не нужно.
- Статус числа кодируется **заливкой, не цветом**: сплошная — факт или оценка Epoch AI, диагональная штриховка — наша экстраполяция или сценарий. Интервалы — тонкими усами с засечками.
- Текст всегда нейтрального цвета (тёмно-серый на светлом фоне), никогда цветом серии. Строки из `slide_content.md` копировать как есть: неразрывные пробелы, запятая как десятичный разделитель и знак процента через пробел уже расставлены.
- Одна ось на график, начало оси Y в нуле, без 3D, теней, градиентов, иконок, логотипов компаний и стоковых картинок.
- Шрифты: одно семейство без засечек с кириллицей (например, IBM Plex Sans, Inter или системный); только три кегля из раздела «Размеры».
- Светлый фон (#fcfcfb или белый); ничего не должно упираться в край и не должно перекрываться.
- Каждое число на слайде должно нести статус словами или через заливку и легенду. Каждое число должно быть найдено в `slide_content.md`.

## Чего быть не должно
{chr(10).join('- ' + x for x in content['forbidden_on_slide'])}
- Перекрёстных ссылок («см. отчёт», сноски с номерами), номерных кодов источников, английских внутренних терминов.

## Если не помещается (порядок сокращений)
1. Убрать «числа про запас» (их на слайде по умолчанию нет).
2. Использовать «Короткий заголовок» из `slide_content.md`.
3. Сократить оговорки до половины строки каждая, не удаляя ни одну.
4. Убрать подписи мощности под столбиками {D_RU} (оставить под столбиками конца 2025) и вторую строку-расшифровку (про ГВт).
Нельзя: убирать интервалы, легенду статусов, подвал с источниками и датой проверки.

## Референс
`reference_slide.html` — черновая раскладка тех же данных (открыть в браузере). Это ориентир только по **расположению блоков**; типографику, сетку и отступы сделать заново. Текст, подписи и подвал референса не использовать: в нём остались внутренние обозначения; все формулировки брать только из `slide_content.md`.

## Чек-лист приёмки (проверить перед сдачей)
- [ ] Ровно один слайд 16:9.
- [ ] Все 4 столбика с усами интервалов и подписями медиан; все 6 строк сплита (Anthropic 2024 — «не раскрыто»).
- [ ] Каждое число совпадает с `slide_content.md` вплоть до формата.
- [ ] У каждого числа есть статус: словами или через заливку и легенду.
- [ ] Две оговорки и подвал с источниками и датой проверки {date_ru(ACCESSED)} присутствуют.
- [ ] Нет кодов, сносок, английских внутренних терминов, лишних цветов, 3D и градиентов.
- [ ] Ничего не обрезано и не перекрыто при просмотре в 100 %.
"""
write_text(_typo(prompt), BRIEF / 'PROMPT.md')
import shutil; shutil.copy(OUT / 'results' / 'slide.html', BRIEF / 'reference_slide.html')
write_text(f"""Пакет для дизайн-агента (собран {date_ru(ACCESSED)} из результатов ноутбука gpu_fleet_review.ipynb):
- PROMPT.md            — задание: композиция, правила, чек-лист приёмки
- slide_content.md     — все факты и числа для слайда со статусами и источниками (единственный источник данных)
- slide_content.json   — то же в машинном виде
- sources.csv          — источники слайда: издатель, дата, заголовок, ссылка, дата доступа, для чего использован
- reference_slide.html — черновая раскладка тех же данных (ориентир по расположению, не по стилю)
- reference_slide.png  — её снимок (если приложен)
""", BRIEF / 'README.md')
print('slide_brief/:', ', '.join(sorted(p.name for p in BRIEF.iterdir())))
