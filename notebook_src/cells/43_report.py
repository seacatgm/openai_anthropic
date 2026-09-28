# ---------------------------------------------------------------- отчёт для CTO: results/report_cto.html
o, a = R_NOWCAST['openai'], R_NOWCAST['anthropic']; ro, ra = R_NOWCAST['reproduction']['OpenAI'], R_NOWCAST['reproduction']['Anthropic']
S = R_SPLIT['summary']; C = R_CHIPS; cp = C['control_points']; so, sa = R_NOWCAST['sensitivity']['openai'], R_NOWCAST['sensitivity']['anthropic']
ch_o = C['openai_end2025']['formula_05_3']['chips']; ch_a = C['anthropic_end2025']['chips']; ch_a26 = C['anthropic_mid2026_by_facts']
cc_o, cc_a = o['cross_check_by_sites'], a['cross_check_by_sites']
DT = R_NOWCAST['meta']['delta_t_years']; DAYS = (NOWCAST_DATE - dt.date(2025, 12, 31)).days
lo_o, hi_o = S['openai_2026_rd_share_range']; lo_a, hi_a = S['anthropic_h1_2026_rd_share_range']; c65 = S['anthropic_h1_2026_central_m65']
MONTHS = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
MONTHS_N = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
def date_ru(s):
    s = str(s)
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', s): y, m, d = s.split('-'); return f'{int(d)} {MONTHS[int(m)-1]} {y}'
    if re.fullmatch(r'\d{4}-\d{2}', s): y, m = s.split('-'); return f'{MONTHS_N[int(m)-1]} {y}'
    return s
D_LONG = date_ru(NOWCAST_DATE.isoformat())            # «27 сентября 2026» — единый формат даты в отчёте
def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
def mln(x, nd=2): return ru(x / 1e6, nd) + ' млн'
def mr(lo, hi, nd=2): return f'{ru(lo / 1e6, nd)}–{ru(hi / 1e6, nd)} млн'      # диапазон, единица один раз
def gw(x, nd=1): return ru(x / 1000, nd) + ' ГВт'
def gr(lo, hi, nd=1): return f'{ru(lo / 1000, nd)}–{ru(hi / 1000, nd)} ГВт'
def tk(x): return ru(x / 1e3, 0) + ' тыс.'
def pc(x): return f'{100*x:.0f}'
def times(x, nd=2): return f'в {ru(x, nd)} раза'

# Имена издателей словами (без кодов) и оригинальные заголовки для всплывающих подсказок ссылок
PUB = {'S01': 'блог OpenAI, финансовый директор Сара Фрайар', 'S02': 'Epoch AI, обзор AI Chip Users', 'S03': 'Epoch AI, данные AI Chip Users', 'S04': 'Epoch AI, методология AI Chip Users',
       'S05': 'Epoch AI', 'S06': 'Epoch AI по данным The Information', 'S07': 'Epoch AI по данным The Information', 'S08': 'Epoch AI', 'S10': 'Epoch AI, данные о продажах чипов',
       'S11': 'Bloomberg и пересказ Key Context, меморандум OpenAI инвесторам', 'S12': 'пост OpenAI (цифры подтверждены The Decoder)', 'S13': 'Bloomberg, показания Грега Брокмана в суде по делу Musk v. Altman', 'S14': 'Reuters (перепечатка Yahoo Finance)',
       'S15': 'The Information (пересказ The Decoder)', 'S16': 'Sacra', 'S17': 'Financial Times (пересказ Business Standard)', 'S18': 'пресс-релиз NVIDIA', 'S19': 'OpenAI, объявление о пяти площадках Stargate', 'S20': 'OpenAI и Amazon (Business Wire)', 'S21': 'OpenAI',
       'S22': 'OpenAI', 'S23': 'проспект IPO Cerebras и Data Center Dynamics', 'S24': 'OpenAI', 'S25': 'Anthropic', 'S26': 'Anthropic и уведомление Broadcom Комиссии по ценным бумагам США', 'S27': 'блог xAI (SpaceX) и Anthropic', 'S28': 'CoreWeave',
       'S29': 'The Wall Street Journal', 'S30': 'Gartner', 'S31': 'The Wall Street Journal (график, по пересказам)', 'S32': 'Fortune', 'S34': 'Эд Зитрон, публикация аудированной отчётности OpenAI (подтверждена Financial Times)',
       'S35': 'Semafor', 'S36': 'The Information', 'S37': 'Epoch AI, каталог ЦОД', 'S40': 'пресс-релиз AMD', 'S41': 'Broadcom', 'S42': 'Reuters (перепечатка CNBC)', 'S43': 'Anthropic', 'S44': 'Anthropic',
       'S45': 'Anthropic', 'S46': 'Epoch AI', 'S47': 'Amazon', 'S48': 'DeepSeek, технический отчёт V3 (arXiv)', 'S49': 'DeepSeek, статья в Nature', 'S50': 'Reuters по материалу Financial Times (перепечатка GV Wire)',
       'S51': 'The Information (пересказ Dealroom)', 'S52': 'Pulse2 по проспекту IPO Nscale', 'S53': 'Deloitte, TMT Predictions 2026', 'S54': 'Lenovo на CES 2026 (по Computerworld)', 'S55': 'SpaceX, отчёт за II квартал 2026',
       'S56': 'Илон Маск в X (по Tom’s Hardware)', 'S57': 'CNBC', 'S58': 'TechCrunch (по Bloomberg)', 'S59': 'Quartz (перепечатка Yahoo Finance)', 'S60': 'Epoch AI', 'S61': 'Epoch AI, методология каталога ЦОД', 'S62': 'NVIDIA', 'S63': 'CNBC'}
TITLE = {'S10': 'Data on AI Chip Sales', 'S11': 'OpenAI Tells Investors It Has Computing Advantage Over Anthropic', 'S27': 'New Compute Partnership with Anthropic', 'S36': 'How Anthropic Clinched $517 Billion in Compute Deals in 11 Months',
         'S37': 'AI Data Centers explorer', 'S52': 'Nscale IPO Filing Reveals $103.4 Billion in Active and Contracted AI Infrastructure Agreements', 'S23': 'Cerebras Form S-1', 'S22': 'Confidential submission of draft S-1',
         'S03': 'Data on AI chip users', 'S29': 'Mind-blowing growth is about to propel Anthropic into its first profitable quarter', 'S34': 'Exclusive: OpenAI Losses Increased Nearly 8X in 2025, With Spending Hitting $34 Billion'}
NOTE = {'S01': 'страница закрыта для автоматического доступа; цитата о 0,2 / 0,6 / 1,9 ГВт подтверждена по CNBC (19 января 2026) и Sherwood News (20 января 2026), дата — по RSS OpenAI',
        'S12': 'текст поста недоступен без входа; цифры подтверждены по The Decoder (30 апреля 2026)', 'S31': 'статья за пейволлом; цифры графика — по пересказам SaaStr и Fast Company',
        'S36': 'статья за пейволлом; детали — по пересказу Dealroom', 'S13': 'статья за пейволлом; подтверждено по перепечатке Yahoo Finance', 'S29': 'статья за пейволлом; цифры подтверждены по Dealroom и SemiAnalysis'}
USED_SOURCES = []
def cite(sid):
    r = SRC[SRC['id'] == sid].iloc[0]
    if sid not in USED_SOURCES: USED_SOURCES.append(sid)
    inner = f'{esc(PUB.get(sid, r["publisher"]))}, {date_ru(r["date"])}'
    return f'<a class="src" href="{esc(r["url"])}" target="_blank" rel="noopener" title="{esc(TITLE.get(sid, r["title"]))}">{inner}</a>' if r['url'] else inner

# ---------- графики (inline SVG + подсказки)
COLR = {'OpenAI': 'var(--openai)', 'Anthropic': 'var(--anthropic)'}
def chart_fleet():
    W, H = 760, 345; L, T, PW, PH = 60, 28, 680, 250
    bars = [('OpenAI', 'конец 2025', ro['epoch'], 'оценка Epoch AI', False), ('OpenAI', D_LONG, o['h100e'], 'наша оценка', True),
            ('Anthropic', 'конец 2025', ra['epoch'], 'оценка Epoch AI', False), ('Anthropic', D_LONG, a['h100e'], 'наша оценка', True)]
    ymax = math.ceil(max(b[2]['p95'] for b in bars) / 1e6) + 0.5
    y = lambda v: T + PH - (v / 1e6) / ymax * PH
    s = [f'<svg class="chart" viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="aspect-ratio: {W} / {H}" role="img" aria-label="Парк в эквивалентах H100: конец 2025 и оценка на {D_LONG}">',
         '<defs><pattern id="hO" patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="rotate(45)"><rect width="8" height="8" fill="var(--openai)" fill-opacity="0.15"/><line x1="0" y1="0" x2="0" y2="8" stroke="var(--openai)" stroke-width="3"/></pattern>',
         '<pattern id="hA" patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="rotate(45)"><rect width="8" height="8" fill="var(--anthropic)" fill-opacity="0.15"/><line x1="0" y1="0" x2="0" y2="8" stroke="var(--anthropic)" stroke-width="3"/></pattern></defs>']
    for k in range(int(ymax) + 1):
        s.append(f'<line x1="{L}" y1="{y(k*1e6):.1f}" x2="{L+PW}" y2="{y(k*1e6):.1f}" class="grid"/><text x="{L-8}" y="{y(k*1e6)+4:.1f}" class="tick" text-anchor="end">{k}</text>')
    s.append(f'<text x="{L-8}" y="12" class="tick" text-anchor="start">млн эквивалентов H100</text>')
    bw, gap, x0 = 120, 44, L + 46
    for i, (lab, per, q, how, hatched) in enumerate(bars):
        x = x0 + i * (bw + gap) + (40 if i >= 2 else 0); col = COLR[lab]
        fill = f'url(#h{"O" if lab == "OpenAI" else "A"})' if hatched else col
        tip = f'{lab}, {per}: медиана {mln(q["p50"])}; 90 %: {mr(q["p05"], q["p95"])} ({how})'
        s.append(f'<g class="hit" data-tip="{esc(tip)}"><rect x="{x}" y="{y(q["p50"]):.1f}" width="{bw}" height="{T+PH-y(q["p50"]):.1f}" fill="{fill}" stroke="{col}" stroke-width="1.5" rx="3"/>'
                 f'<line x1="{x+bw/2}" y1="{y(q["p05"]):.1f}" x2="{x+bw/2}" y2="{y(q["p95"]):.1f}" class="ci"/><line x1="{x+bw/2-12}" y1="{y(q["p05"]):.1f}" x2="{x+bw/2+12}" y2="{y(q["p05"]):.1f}" class="ci"/><line x1="{x+bw/2-12}" y1="{y(q["p95"]):.1f}" x2="{x+bw/2+12}" y2="{y(q["p95"]):.1f}" class="ci"/>'
                 f'<text x="{x+bw/2}" y="{y(q["p95"])-8:.1f}" class="val" text-anchor="middle">{esc(mln(q["p50"]))}</text>'
                 f'<text x="{x+bw/2}" y="{T+PH+18}" class="lab" text-anchor="middle">{lab}</text><text x="{x+bw/2}" y="{T+PH+34}" class="lab2" text-anchor="middle">{esc(per)}</text><text x="{x+bw/2}" y="{T+PH+50}" class="lab2" text-anchor="middle">{how}</text></g>')
    s.append('</svg>')
    return ''.join(s)

def chart_split():
    rows = [('OpenAI', '2024', S['openai_2024']['rd_share'], S['openai_2024']['rd_share'], 'оценка Epoch AI по данным The Information'),
            ('OpenAI', '2025', S['openai_2025']['rd_share'], S['openai_2025']['rd_share'], 'оценка Epoch AI, The Information и Sacra'),
            ('OpenAI', '2026, план (сценарии)', lo_o, hi_o, 'наш расчёт по плановым цифрам OpenAI'),
            ('Anthropic', '2025', S['anthropic_2025']['rd_share'], S['anthropic_2025']['rd_share'], 'оценка: прогноз компании по данным The Information и расчёт Epoch AI'),
            ('Anthropic', '1-е полугодие 2026 (сценарии)', lo_a, hi_a, 'наш расчёт по квартальным данным The Wall Street Journal')]
    W, rowh, gapr, L, BW = 760, 34, 16, 250, 380; H = 16 + len(rows) * (rowh + gapr) + 10
    s = [f'<svg class="chart" viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="aspect-ratio: {W} / {H}" role="img" aria-label="Доля обучения и исследований в расходах на вычисления">']
    for i, (lab, yr, lo, hi, how) in enumerate(rows):
        yy = 16 + i * (rowh + gapr) + (10 if i >= 3 else 0); col = COLR[lab]
        rd = f'{pc(lo)}' + (f'–{pc(hi)}' if hi > lo else '') + ' %'; inf = f'{pc(1-hi)}' + (f'–{pc(1-lo)}' if hi > lo else '') + ' %'
        tip = f'{lab}, {yr}: обучение и исследования {rd}, инференс {inf} ({how})'
        s.append(f'<g class="hit" data-tip="{esc(tip)}"><text x="{L-10}" y="{yy+rowh/2+4}" class="lab" text-anchor="end">{lab} {esc(yr.split(" (")[0])}</text>'
                 f'<rect x="{L}" y="{yy}" width="{lo*BW:.1f}" height="{rowh}" fill="{col}" rx="3"/>')
        if hi > lo: s.append(f'<rect x="{L+lo*BW:.1f}" y="{yy}" width="{(hi-lo)*BW:.1f}" height="{rowh}" fill="url(#h{"O" if lab == "OpenAI" else "A"})" stroke="{col}" stroke-width="1"/>')
        s.append(f'<rect x="{L+hi*BW+2:.1f}" y="{yy}" width="{(1-hi)*BW-2:.1f}" height="{rowh}" fill="var(--neutral)" rx="3"/>'
                 f'<text x="{L+6}" y="{yy+rowh/2+4}" class="valw">обучение {rd}</text><text x="{L+BW+8}" y="{yy+rowh/2+4}" class="val">инференс {inf}</text></g>')
    s.append('</svg>')
    return ''.join(s)

# ---------- таблицы (с data-label для мобильной раскладки)
def table(head, rows):
    h = ''.join(f'<th>{c}</th>' for c in head)
    b = ''.join('<tr>' + ''.join(f'<td data-label="{esc(head[j])}">{c}</td>' for j, c in enumerate(r)) + '</tr>' for r in rows)
    return f'<div class="tw"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'

t_coef = table(['Чип', 'Потребляемая мощность на чип', 'Эквивалентов H100 на чип', 'Чипов на 1 ГВт', 'Эквивалентов H100 на 1 ГВт'], [
    ['H100/H200 (поколение Hopper)', '1 453 Вт', '1,00', '≈ 690 тыс.', '≈ 690 тыс.'],
    ['GB200 (поколение Blackwell)', '2 090 Вт', '2,53', '≈ 480 тыс.', '≈ 1,21 млн'],
    ['Trainium2 (Amazon)', '871 Вт', '0,66', '≈ 1,15 млн', '≈ 754 тыс.'],
    ['TPU v7 (Google)', '1 672 Вт', '2,33', '≈ 600 тыс.', '≈ 1,39 млн'],
])

t_fleet = table(['Показатель', 'OpenAI', 'Anthropic', 'Откуда число'], [
    ['Мощность парка, конец 2025', '≈ 1,9 ГВт (0,2 ГВт в 2023, 0,6 ГВт в 2024)', '≈ 1,4 ГВт',
     f'OpenAI — раскрыто компанией: {cite("S01")}. Anthropic — оценка конкурента из меморандума OpenAI инвесторам: {cite("S11")}; сама Anthropic мощность не раскрывает'],
    ['Парк в эквивалентах H100, конец 2025', f'{mln(ro["epoch"]["p50"])}; 90 %: {mr(ro["epoch"]["p05"], ro["epoch"]["p95"])}', f'{mln(ra["epoch"]["p50"])}; 90 %: {mr(ra["epoch"]["p05"], ra["epoch"]["p95"])}',
     f'модель Epoch AI по мощности парка: у OpenAI — раскрытой (1,9 ГВт), у Anthropic — оценённой OpenAI (Epoch AI берёт диапазон 1,0–1,9 ГВт, {cite("S04")}): {cite("S02")}. Мы пересчитали обе модели заново: медианы совпали с точностью {ru(abs(ro["median_deviation_%"]),1)} % и {ru(abs(ra["median_deviation_%"]),1)} %'],
    ['Физических ускорителей, конец 2025', f'≈ {mln(ch_o["p50"])} (90 %: {mr(ch_o["p05"], ch_o["p95"])}): при доле Blackwell 30–50 % чипов (состав, который принимает Epoch AI: Hopper : Blackwell ≈ 1,5 : 1) около 60 % чипов — H100/H200 (поколение Hopper), но около {pc(C["openai_end2025"]["formula_05_3"]["blackwell_share_h100e"]["p50"])} % вычислительной мощности дают GB200 (Blackwell)',
     f'≈ {mln(ch_a["p50"])} (90 %: {mr(ch_a["p05"], ch_a["p95"])}); из них ≈ {mln(C["anthropic_end2025"]["trainium2_chips"]["p50"],1)} Trainium2 на конец 2025; к апрелю 2026 компания заявила уже «более миллиона», что согласуется с темпом ввода кампуса Rainier',
     f'наш расчёт: мощность парка делим на среднюю мощность одного чипа при том составе парка, который принимает Epoch AI (состав и мощность на чип — {cite("S04")}). заявление Anthropic о «более чем миллионе Trainium2» (апрель 2026): {cite("S25")}'],
    ['Место среди лабораторий', '1-е (2-е — Google DeepMind, интервалы перекрываются)', '3-е (после OpenAI и Google DeepMind)', f'оценка Epoch AI: {cite("S02")}'],
    ['Расходы на облачные вычисления, 2025', '$16,3 млрд', '$6,8 млрд', f'OpenAI — {cite("S04")}. Anthropic — {cite("S06")}'],
    ['Инференс на площадках партнёров (Microsoft Azure у OpenAI; Amazon Bedrock и Google Vertex у Anthropic)', 'не входит в оценку; по Epoch AI — до ≈ 25 % её вычислений (верхняя оценка)', 'входит в оценку; ≈ 10 % её вычислений', f'методология Epoch AI: {cite("S04")}'],
])

untr = cc_a['untracked_ranges']
def tkr(lo, hi):
    return (f'{ru(lo/1e6,2)}–{ru(hi/1e6,2)}\u00a0млн' if lo >= 1e6 else f'{ru(lo/1e3,0)}–{ru(hi/1e3,0)}\u00a0тыс.')
def untr_txt(key_part):
    k = next(k for k in untr if key_part in k); lo, hi = untr[k]; return tkr(lo, hi) if lo > 0 else f'до {tk(hi)}'
rainier_d = next(r['delta'] for r in cc_a['tracked_sites'] if 'Carlisle' in r['site']); col1_d = next(r['delta'] for r in cc_a['tracked_sites'] if 'Colossus' in r['site'])
abil = next(r for r in cc_o['tracked_sites'] if 'Abilene' in r['site'])
t_now = table(['', 'OpenAI', 'Anthropic', 'Как получено'], [
    ['Парк в эквивалентах H100, медиана', f'{mln(o["h100e"]["p50"])}', f'{mln(a["h100e"]["p50"])}', f'наша модель: оценка Epoch AI на конец 2025 ({cite("S02")}), умноженная на темп роста за прошедшую часть года'],
    ['Половина прогонов попадает в интервал', f'{mr(o["h100e"]["p25"], o["h100e"]["p75"])}', f'{mr(a["h100e"]["p25"], a["h100e"]["p75"])}', '25-й и 75-й процентили 200 000 прогонов'],
    ['90 % прогонов попадают в интервал', f'{mr(o["h100e"]["p05"], o["h100e"]["p95"])}', f'{mr(a["h100e"]["p05"], a["h100e"]["p95"])}', '5-й и 95-й процентили'],
    ['То же в мощности оборудования (медиана; 90 % прогонов)', f'≈ {gw(o["gw_it_mw"]["p50"])} ({gr(o["gw_it_mw"]["p05"], o["gw_it_mw"]["p95"])})', f'≈ {gw(a["gw_it_mw"]["p50"])} ({gr(a["gw_it_mw"]["p05"], a["gw_it_mw"]["p95"])})',
     f'парк конца 2025 переведён по средней плотности парка в модели Epoch AI: {ru(R_NOWCAST["meta"]["priors"]["eta_2025_h100e_per_mw"]["OpenAI"],0)} эквивалентов H100 на мегаватт у OpenAI (медиана парка 1,74 млн ÷ медиана мощности в модели Epoch AI 1,95 ГВт: Epoch AI берёт раскрытые 1,9 ГВт с разбросом, и медиана распределения чуть выше) и 865 у Anthropic (публикует Epoch AI, {cite("S04")}). Прирост переведён по плотности новых поставок 945 и 950 на мегаватт — наше допущение: примерно пополам GB200 (1 210 эквивалентов H100 на мегаватт) и H100 / Trainium2 (690–754 на мегаватт)'],
    [f'Во сколько раз парк вырос с конца 2025 по {D_LONG}', times(o['multiplier_vs_end2025']['p50']), times(a['multiplier_vs_end2025']['p50']), 'медиана прогонов'],
    ['Проверка по известным площадкам', f'не меньше {mln(cc_o["lower_bound_facts_only"])}. Из площадок OpenAI каталог отслеживает по зданиям только Абилин (кампус Stargate в Техасе): там ≈ {tk(abil[f"h100e_{NOWCAST_DATE}"])} эквивалентов H100, из которых ≈ {tk(abil["h100e_end2025"])} работали уже на конец 2025, прирост +{tk(cc_o["tracked_delta"])} Площадки Azure, которые OpenAI арендует сама (в отличие от серверов Azure OpenAI Service, за которые платила Microsoft), Oracle вне Абилина и арендодателя CoreWeave по зданиям не разобраны, а именно через них шёл рост 2025 года, поэтому это нижняя граница',
     f'{mln(cc_a["total"]["p50"])} (90 %: {mr(cc_a["total"]["p05"], cc_a["total"]["p95"])}) = {mln(cc_a["base_epoch_2025"])} на конец 2025 + кампус Amazon Rainier (Индиана) +{tk(rainier_d)} + Colossus 1 (SpaceX, Мемфис) +{tk(col1_d)} + TPU Google {untr_txt("TPU")} + Microsoft Azure и CoreWeave {untr_txt("Azure")} + доля во втором кампусе SpaceX Colossus 2 {untr_txt("Colossus 2")}; три последних слагаемых — наши диапазоны в эквивалентах H100 (заданы как допущения, а не пересчитаны из штук). Проверка на {ru(abs(a["cross_check_gap_%"]),0)} % ниже медианы модели ({mln(cc_a["total"]["p50"])} против {mln(a["h100e"]["p50"])})',
     f'каталог ЦОД Epoch AI (спутниковые снимки, разрешения на строительство, данные о мощности): {cite("S37")}'],
    ['Если раскрытые гигаватты — мощность здания, а не оборудования', f'{mln(so["disclosed_is_facility_power_PUE1.3"]["h100e"]["p50"])}', f'{mln(sa["disclosed_is_facility_power_PUE1.3"]["h100e"]["p50"])}', f'мы делим парк на конец 2025 на 1,3 (OpenAI: 1,74 → ≈ 1,34 млн): мощность здания в 1,3 раза больше мощности оборудования — наше допущение внутри диапазона 1,1–1,7, который закладывает Epoch AI ({cite("S04")}). Сама Epoch AI при таком прочтении получает более низкие 1,0–1,1 млн, потому что закладывает и верхнюю часть диапазона до 1,7; с её числом наша оценка OpenAI была бы ≈ 2,5–2,7 млн. Для OpenAI Epoch AI оценивает вероятность такого прочтения в 10 %; для Anthropic эта неопределённость частично уже внутри диапазона 1,0–1,9 ГВт, поэтому реальный эффект меньше'],
    ['Если темп роста на краю диапазона', f'{mln(so["g_low"]["h100e"]["p50"])} при росте в 2,5 раза в год; {mln(so["g_high"]["h100e"]["p50"])} при росте в 4,5 раза', f'{mln(sa["g_low"]["h100e"]["p50"])} при росте в 2,5 раза; {mln(sa["g_high"]["h100e"]["p50"])} при росте в 5 раз', 'медиана при фиксированном темпе'],
])

sc = {x['scenario'][0]: x for x in R_SPLIT['openai_2026']}
h1 = R_SPLIT['anthropic_h1_2026_accepted']
t_split = table(['Компания, период', 'Обучение и исследования', 'Инференс', 'Доля обучения', 'Откуда число'], [
    ['OpenAI, 2024', f'≈ $5 млрд — оценка Epoch AI: все облачные расходы OpenAI за 2024 год ($6,8 млрд, {cite("S04")}; совпадение: столько же Anthropic потратила в 2025) минус ≈ $2 млрд инференса. The Information называет из них ≈ $3 млрд на обучение моделей и ≈ $1 млрд на исследовательские вычисления (с амортизацией); ещё ≈ $1 млрд — вычисления вне этих двух статей', '≈ $2 млрд', f'{pc(S["openai_2024"]["rd_share"])} %', f'{cite("S07")}'],
    ['OpenAI, 2025', '≈ $8 млрд («около половины» из $16,3 млрд)', '$8,4 млрд; рост в 4 раза за год', f'{pc(S["openai_2025"]["rd_share"])} %', f'деление «примерно поровну» — {cite("S02")}; $16,3 млрд — {cite("S04")}; $8,4 млрд — {cite("S16")}; рост в 4 раза — {cite("S14")}'],
    ['OpenAI, 2026 (сценарии по плану)', '$32 млрд', f'четыре сценария: ${ru(sc["A"]["inf_bn"],1)} млрд (прогноз OpenAI, сделанный до февральского пересмотра планов; по Sacra); ${ru(sc["B"]["inf_bn"],1)} млрд (остаток бюджета $50 млрд после $32 млрд на обучение); ${ru(sc["D"]["inf_bn"],1)} млрд (инференс 2025 $8,4 млрд, удвоенный); ${ru(sc["C"]["inf_bn"],1)} млрд (инференс 2025 × 2,6 — между удвоением и прошлогодним ростом вчетверо; верхняя граница)',
     f'{pc(lo_o)}–{pc(hi_o)} %: $32 млрд ÷ ($32 млрд + инференс по сценарию)',
     f'обучение $32 млрд — {cite("S15")}; бюджет $50 млрд — {cite("S13")}; ${ru(sc["A"]["inf_bn"],1)} млрд — {cite("S16")}. Сценарии и доли — наш расчёт'],
    ['Anthropic, 2024', 'не раскрыто', 'не раскрыто', '—', f'известны только общие расходы $2,5 млрд: {cite("S04")}'],
    ['Anthropic, 2025', '$4,1 млрд (прогноз компании в декабре 2025)', '≈ $2,7 млрд (Epoch AI: из валовой маржи 40 % по всей выручке $4,5 млрд)', f'{pc(S["anthropic_2025"]["rd_share"])} %', f'{cite("S06")}'],
    ['Anthropic, 2026 (первое полугодие, сценарии)', f'${ru(min(x["rd_bn"] for x in h1),1)}–{ru(max(x["rd_bn"] for x in h1),1)} млрд', f'${ru(min(x["inf_bn"] for x in h1),1)}–{ru(max(x["inf_bn"] for x in h1),1)} млрд', f'{pc(lo_a)}–{pc(hi_a)} % (центральный сценарий {pc(c65["rd_share"])} %)',
     f'выручка первого квартала — $4,8 млрд, из неё 71 % ушло на вычисления; второго квартала — $10,9 млрд (прогноз компании), 56 %: {cite("S29")}. Инференс = выручка × (1 − валовая маржа инференса); маржа инференса не раскрыта; The Wall Street Journal пишет о выходе на прибыльный квартал, поэтому берём 60, 65 и 72 % — выше прошлогодних 40 % по всей выручке. Обучение = все расходы на вычисления − инференс. Сценарий с маржой 50 % отброшен: во втором квартале он оставлял на обучение $0,65 млрд против ≈ $1 млрд в квартал в 2025. Наш расчёт'],
])

# ---------- контракты
def li(items): return '<ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'
openai_2026 = li([
    f'10 ГВт площадок законтрактовано в США к концу апреля 2026, из них более 3 ГВт добавлено за 90 дней, 2 ГВт — от Amazon: {cite("S12")}. Соглашения с NVIDIA, Broadcom и AMD на 10 + 10 + 6 ГВт — рамочные и частично лягут на эти же площадки.',
    f'Абилин (кампус Stargate в Техасе): сейчас 421 МВт и ≈ {tk(cp["Stargate Abilene"]["h100e_epoch"])} эквивалентов H100; ещё четыре здания (пятое–восьмое) ожидаются к ноябрю — итого ≈ 843 МВт и ≈ 1,02 млн эквивалентов H100: {cite("S37")}.',
    f'Первые гигаватты новых систем во втором полугодии 2026: AMD MI450 ({cite("S40")}) и стойки с собственным ускорителем OpenAI и Broadcom ({cite("S41")}).',
    f'NVIDIA: письмо о намерениях на 10 ГВт систем Vera Rubin с первым гигаваттом во втором полугодии 2026 ({cite("S18")}) в договор не оформлено и в феврале 2026 заменено прямой инвестицией NVIDIA $30 млрд в OpenAI ({cite("S17")}); обязательств по поставке мощностей под ним нет, поэтому эти 10 ГВт в план ввода не входят.',
    f'Кампус PORTS-Pike в Огайо: 4,25 ГВт вычислительной мощности законтрактовано твёрдо (первая фаза, с кредитной поддержкой NVIDIA), ещё 3,75 ГВт — опцион, итого до 8 ГВт вычислительной мощности; новой генерации на площадке — не менее 10 ГВт; 20-летняя аренда, первые 800 МВт в 2028: {cite("S24")}, {cite("S62")}. NVIDIA гарантирует обязательства по кампусу на сумму до $105 млрд — по регуляторной отчётности, о которой сообщил CNBC: {cite("S63")}.',
    f'Риск сроков: Oracle уведомила о форс-мажоре по площадке Stargate в Нью-Мексико (2,45 ГВт, цель — 2028): {cite("S58")}.',
    f'Расходы на вычисления до 2030 года в презентации партнёрам выросли до ≈ $856 млрд ({cite("S50")}) против ≈ $600 млрд в феврале ({cite("S14")}).'])
anthropic_2026 = li([
    f'Amazon: «почти 1 ГВт» Trainium2 и Trainium3 к концу 2026; договор до 5 ГВт и более $100 млрд за 10 лет: {cite("S25")}.',
    f'Google: до 1 млн TPU и «значительно больше 1 ГВт» в 2026: {cite("S43")}; ещё ≈ 3,5 ГВт TPU с 2027 через Broadcom: {cite("S26")}.',
    f'Microsoft Azure: до 1 ГВт систем NVIDIA, обязательство $30 млрд: {cite("S44")}.',
    f'Colossus 1 (SpaceX, Мемфис): более 220 тыс. GPU NVIDIA, ≈ 300 МВт, $1,25 млрд в месяц до мая 2029: {cite("S27")}; те же условия — в проспекте IPO SpaceX от 20 мая 2026 (форма S-1 — регистрационное заявление в Комиссию по ценным бумагам США).',
    f'Всего компания законтрактовала вычислений на $517 млрд за 11 месяцев ({cite("S36")}), по подсчёту The Information — не менее 14,8 ГВт новой мощности с октября 2025 ({cite("S51")}); в том числе до $44,6 млрд у Nscale в Западной Вирджинии (ввод — конец 2027): {cite("S52")}.',
    f'Прогноз OpenAI для Anthropic: 3–4 ГВт к концу 2026, 7–8 ГВт к концу 2027 (оценка конкурента, по пересказу меморандума): {cite("S11")}. Наша сентябрьская оценка ≈ {gw(a["gw_it_mw"]["p50"])} попадает в этот диапазон раньше срока: она учитывает арендованные мощности Colossus 1 и партнёрских облаков, которые в оценке OpenAI, вероятно, не учтены.'])

parts = ch_a26['parts']; pk = list(parts)
# ---------- сборка страницы
head_inner = f"""<title>GPU-парк OpenAI и Anthropic</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&amp;family=IBM+Plex+Serif:wght@600&amp;display=swap">
<style>
:root {{ color-scheme: light; --paper:#f7f8f6; --card:#eef0eb; --ink:#1a1c1e; --muted:#5b6169; --rule:#d7dbd3; --openai:#2470cc; --anthropic:#c9491a; --neutral:#8f8e88; --link:#1c5cab; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ color-scheme: dark; --paper:#16181a; --card:#1f2225; --ink:#f2f3f0; --muted:#b5bab0; --rule:#33372f; --openai:#2f6fc4; --anthropic:#c4491c; --neutral:#6b6e69; --link:#86b6ef; }} }}
:root[data-theme="dark"] {{ color-scheme: dark; --paper:#16181a; --card:#1f2225; --ink:#f2f3f0; --muted:#b5bab0; --rule:#33372f; --openai:#2f6fc4; --anthropic:#c4491c; --neutral:#6b6e69; --link:#86b6ef; }}
html {{ background: var(--paper); }}
body {{ margin:0; background: var(--paper); color: var(--ink); font-family: "IBM Plex Sans", -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-size: 16px; line-height: 1.5; padding-block: 32px 48px; padding-inline: 16px; font-variant-numeric: tabular-nums; }}
.wrap {{ max-width: 980px; margin: 0 auto; }}
h1 {{ font-family: "IBM Plex Serif", Georgia, "Times New Roman", serif; font-weight: 600; font-size: clamp(24px, 3.4vw, 34px); line-height: 1.2; margin: 0 0 8px; text-wrap: balance; }}
h2 {{ font-family: "IBM Plex Serif", Georgia, serif; font-weight: 600; font-size: 22px; margin: 44px 0 10px; text-wrap: balance; }}
h3 {{ font-size: 16px; font-weight: 600; margin: 22px 0 6px; }}
.meta {{ color: var(--muted); font-size: 14px; margin-bottom: 26px; }}
p, li {{ max-width: 72ch; }}
.answer {{ background: var(--card); border-left: 4px solid var(--ink); padding: 16px 20px; margin: 8px 0 12px; }}
.answer p {{ margin: 8px 0; }}
.answer strong {{ font-weight: 600; }}
.legend {{ display:flex; flex-wrap: wrap; gap: 8px 22px; color: var(--muted); font-size: 14px; margin: 6px 0 12px; }}
.legend span::before {{ content:""; display:inline-block; width:12px; height:12px; margin-right:6px; vertical-align:-1px; border-radius:2px; background: var(--sw); }}
.cap {{ color: var(--muted); font-size: 13px; margin: 2px 0 10px; }}
.tw {{ overflow-x: auto; margin: 12px 0 8px; }}
table {{ border-collapse: collapse; width: 100%; font-size: 14.5px; }}
th, td {{ text-align: left; vertical-align: top; padding: 9px 10px; border-bottom: 1px solid var(--rule); }}
th {{ font-weight: 600; color: var(--muted); font-size: 12.5px; text-transform: uppercase; letter-spacing: 0.04em; }}
td:first-child {{ font-weight: 500; min-width: 150px; }}
td:last-child {{ color: var(--muted); min-width: 220px; }}
@media (max-width: 640px) {{
  .tw table, .tw tbody, .tw tr, .tw td {{ display: block; width: 100%; box-sizing: border-box; }}
  .tw thead {{ display: none; }} .tw tr {{ border-bottom: 2px solid var(--rule); padding: 6px 0; }}
  .tw td {{ border: 0; padding: 4px 0; min-width: 0; }} .tw td::before {{ content: attr(data-label); display: block; font-size: 12px; text-transform: uppercase; letter-spacing: .04em; color: var(--muted); }}
  .tw td:first-child::before {{ display: none; }}
}}
@media (max-width: 711px) {{ .chart {{ min-width: 680px; }} }}
a.src {{ color: var(--link); text-decoration: underline; text-decoration-color: color-mix(in srgb, var(--link) 40%, transparent); text-underline-offset: 2px; }}
a.src:hover, a.src:focus {{ text-decoration-color: var(--link); outline: none; }}
a:focus-visible {{ outline: 2px solid var(--link); outline-offset: 2px; }}
.chart {{ width: 100%; max-width: 100%; height: auto; display:block; margin: 4px 0 0; }}
.tw:has(> .chart) {{ margin: 8px 0 0; }}
.chart .grid {{ stroke: var(--rule); stroke-width: 1; }} .chart .tick, .chart .lab2 {{ font-size: 11px; fill: var(--muted); }} .chart .lab {{ font-size: 12.5px; fill: var(--ink); }}
.chart .val {{ font-size: 12.5px; font-weight: 600; fill: var(--ink); }} .chart .valw {{ font-size: 12.5px; font-weight: 600; fill: #ffffff; }} .chart .ci {{ stroke: var(--ink); stroke-width: 1.6; }}
.chart .hit {{ cursor: default; }} .chart .hit:hover rect {{ filter: brightness(0.92); }}
#tip {{ position: fixed; pointer-events: none; background: var(--ink); color: var(--paper); padding: 8px 10px; border-radius: 4px; font-size: 13px; max-width: 320px; line-height: 1.35; opacity: 0; transition: opacity .12s; z-index: 10; }}
@media (prefers-reduced-motion: reduce) {{ #tip {{ transition: none; }} }}
ul {{ padding-left: 20px; }} li {{ margin: 4px 0; }}
.two {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px 32px; }}
.sources ul {{ padding-left: 18px; font-size: 14px; color: var(--muted); }}
code {{ font-family: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.92em; background: var(--card); padding: 1px 5px; border-radius: 3px; }}
ol {{ padding-left: 22px; }} .sources li {{ max-width: none; margin: 3px 0; }}
.foot {{ color: var(--muted); font-size: 13px; margin-top: 36px; border-top: 1px solid var(--rule); padding-top: 12px; }}
</style>"""

body_inner = f"""<div class="wrap">
<h1>Сколько GPU у OpenAI и Anthropic и как они делятся между обучением и инференсом</h1>
<div class="meta">Отчёт по состоянию на {D_LONG}. У каждого числа указан источник или способ расчёта; все ссылки проверены {date_ru(ACCESSED)}. Модельные оценки даны с интервалами.</div>

<div class="answer">
<p><strong>Число чипов ни одна компания не публикует, поэтому считаем в мощности и в эквивалентах H100.</strong> На конец 2025 года OpenAI располагала ≈ 1,9 ГВт мощности ({cite("S01")}). По оценке Epoch AI (независимой исследовательской группы, которая отслеживает вычислительные мощности ИИ-компаний) это {mln(ro["epoch"]["p50"])} эквивалентов H100 (интервал, в который попадают 90 % оценок: {mr(ro["epoch"]["p05"], ro["epoch"]["p95"])}; далее коротко «90 %: …») ({cite("S02")}). Anthropic — ≈ 1,4 ГВт по оценке OpenAI ({cite("S11")}) и {mln(ra["epoch"]["p50"])} эквивалентов H100 (90 %: {mr(ra["epoch"]["p05"], ra["epoch"]["p95"])}) по той же модели Epoch AI. В штуках это ≈ {mln(ch_o["p50"])} и ≈ {mln(ch_a["p50"])} ускорителей — наш пересчёт по составу парков, который принимает Epoch AI: у Anthropic чипов больше при меньшей мощности, потому что ≈ {mln(C["anthropic_end2025"]["trainium2_chips"]["p50"],1)} из них — Trainium2, каждый равен двум третям H100.</p>
<p><strong>На {D_LONG} наша оценка:</strong> OpenAI ≈ {mln(o["h100e"]["p50"])} эквивалентов H100 (90 % прогонов: {mr(o["h100e"]["p05"], o["h100e"]["p95"])}), то есть ≈ {gw(o["gw_it_mw"]["p50"])} мощности самого оборудования, без охлаждения и потерь здания (по 900–950 эквивалентов H100 на мегаватт при смеси H100 и GB200); Anthropic ≈ {mln(a["h100e"]["p50"])} (90 %: {mr(a["h100e"]["p05"], a["h100e"]["p95"])}), ≈ {gw(a["gw_it_mw"]["p50"])}. Это не отчётность компаний, а наша экстраполяция: оценку Epoch AI на конец 2025 мы умножили на годовой темп роста (2,5–4,5 раза у OpenAI, 2,5–5 у Anthropic) за прошедшие {ru(DT,2)} года, разыграв 200 000 вариантов парка и темпа.</p>
<p><strong>Деление между обучением и инференсом известно только в деньгах.</strong> В 2025 году OpenAI тратила на обучение и исследования и на инференс примерно поровну — {pc(S["openai_2025"]["rd_share"])} % на обучение и {pc(S["openai_2025"]["inf_share"])} % на инференс (оценка Epoch AI по данным The Information и Sacra); Anthropic — {pc(S["anthropic_2025"]["rd_share"])} % на {pc(S["anthropic_2025"]["inf_share"])} % в пользу обучения (прогноз компании по данным The Information и расчёт Epoch AI). На 2026 год мы построили сценарии: у OpenAI по её плановым цифрам ($32 млрд на обучение при бюджете $50 млрд) доля обучения растёт до {pc(lo_o)}–{pc(hi_o)} %, хотя инференс в 2025 рос вчетверо и план, вероятно, его недооценивает; у Anthropic по квартальным данным The Wall Street Journal за первое полугодие 2026 доля обучения падает до {pc(lo_a)}–{pc(hi_a)} %.</p>
</div>

<h2>Почему считаем в гигаваттах и эквивалентах H100</h2>
<p>Единственная твёрдая цифра на уровне компании — мощность OpenAI: 0,2 ГВт в 2023, 0,6 ГВт в 2024 и около 1,9 ГВт в 2025 году ({cite("S01")}). Epoch AI считает, что с вероятностью 90 % это мощность вычислительного оборудования, а не всего здания; если это мощность здания, её оценка парка падает до ≈ 1,0–1,1 млн эквивалентов H100 ({cite("S04")}). Гигаватты в оценках Epoch AI и в нашей модели — потребление серверов и сети, без охлаждения и потерь здания. Гигаватты из пресс-релизов, контрактов и чужих оценок (включая 1,4 ГВт Anthropic) приведены так, как их назвали источники; для многих из них тип мощности не раскрыт, а мощность площадки обычно в 1,1–1,7 раза больше мощности оборудования. Все остальные числа — оценки аналитиков, параметры контрактов или утечки инвесторских документов.</p>
<p>Штуки между парками несопоставимы: один чип GB200 по вычислительной мощности равен примерно 2,5 чипа H100, а один Trainium2 — двум третям H100. Поэтому парки сравнивают в эквивалентах H100 — по пиковой производительности в 8-битных операциях относительно H100 ({cite("S10")}). Один гигаватт вмещает разное число чипов:</p>
{t_coef}
<p class="cap">Параметры чипов — {cite("S04")}; мощность на чип включает сервер и сетевое оборудование. Деление — наше: чипов на гигаватт = 1 млрд Вт ÷ мощность на чип; эквивалентов H100 на гигаватт = чипов × эквивалент на чип. Числа посчитаны по неокруглённым параметрам Epoch AI, поэтому произведение округлённых колонок может отличаться на 1 %. Для GB300 Epoch AI принимает тот же эквивалент, что для GB200; по Trainium3 данных нет.</p>
<p>Гигаватты из пресс-релизов складывать нельзя: соглашения OpenAI с NVIDIA на 10 ГВт ({cite("S18")}; письмо о намерениях, в договор не оформлено и заменено инвестицией $30 млрд — {cite("S17")}), Broadcom на 10 ГВт ({cite("S41")}), AMD на 6 ГВт ({cite("S40")}) и Oracle на 4,5 ГВт ({cite("S19")}) частично описывают одни и те же площадки, а вводятся с 2026 года и до конца десятилетия (Broadcom — со второго полугодия 2026 до конца 2029). Оценки Epoch AI — это работающие мощности, включая арендованные; загрузка не учитывается ({cite("S04")}).</p>

<h2>Парк на конец 2025 года</h2>
{t_fleet}
<p>Важная асимметрия: Anthropic платит за серверы, на которых её модели работают в Amazon Bedrock и Google Vertex, и учитывает эту выручку полностью, поэтому Epoch AI включает эти мощности в её парк. OpenAI до апреля 2026 года получала от Microsoft 20 % выручки Azure OpenAI и за это железо не платила, поэтому в её оценку оно не входит ({cite("S04")}, {cite("S35")}). Сравнение {mln(ro["epoch"]["p50"])} против {mln(ra["epoch"]["p50"])} занижает OpenAI на 10–25 % — наша оценка влияния по методологии Epoch AI. С 27 апреля 2026 года соглашение с Microsoft изменено: лицензия стала неэксклюзивной, OpenAI может продавать модели в любом облаке, а Microsoft больше не делится с ней выручкой ({cite("S21")}). В нашу оценку на {D_LONG} серверы Azure OpenAI Service по-прежнему не включены: кто платит за них после апреля, публично не раскрыто.</p>

<h2>Оценка на {D_LONG}</h2>
<p>Данных о работающих мощностях после конца 2025 года компании не публикуют, поэтому текущий парк — модель. Мы берём распределение Epoch AI на конец 2025 года и умножаем его на годовой темп роста в степени {ru(DT,2)} — столько от года прошло к {D_LONG} ({DAYS} из 365 дней). Диапазоны темпа роста — наше допущение. Для OpenAI берём от 2,5 до 4,5 раз в год: центр диапазона (рост ≈ в 3,4 раза) близок к утроению, которого Epoch AI ждёт от OpenAI за 2026 год ({cite("S04")}), и к отношению бюджета на вычисления $50 млрд ({cite("S13")}) к $16,3 млрд облачных расходов 2025 года (× 3,1); края отражают риск сроков ввода и более плотные новые чипы. Для Anthropic — от 2,5 до 5 раз: в 2026 году вводятся TPU Google, Trainium Amazon, Colossus 1 и мощности Azure, а OpenAI прогнозирует ей 3–4 ГВт к концу года ({cite("S11")}) — это рост мощности в 2,1–2,9 раза, а в эквивалентах H100 больше, потому что новые TPU v7 и GB200 дают в 1,5–1,8 раза больше вычислений на мегаватт, чем Trainium2 и H100. В каждом из 200 000 прогонов парк и темп берутся случайно: 90 % значений темпа лежат внутри названных границ, чаще всего — около центра. Результат — медиана и интервалы этих 200 000 прогонов:</p>
<div class="legend"><span style="--sw:var(--openai)">OpenAI</span><span style="--sw:var(--anthropic)">Anthropic</span></div>
<div class="tw">{chart_fleet()}</div>
<p class="cap">Столбик — медиана; усы — 90 % интервал: у оценок Epoch AI — их собственный, у нашей оценки — по 200 000 прогонам. Штриховка — наша экстраполяция от оценки Epoch AI.</p>
{t_now}
<p>Оценка для OpenAI выше проверки по площадкам более чем вдвое, потому что каталог Epoch AI подробно отслеживает только один кампус OpenAI. Для Anthropic проверка по площадкам на {ru(abs(a["cross_check_gap_%"]),0)} % ниже медианы модели, что укладывается в интервал модели. По объявленным поставкам у Anthropic к {D_LONG} ≈ {mln(ch_a26["chips"]["p50"],1)} ускорителей (90 %: {mr(ch_a26["chips"]["p05"], ch_a26["chips"]["p95"], 1)}): {tkr(parts[pk[0]]["p05"], parts[pk[0]]["p95"])} Trainium2 (компания заявила «более миллиона», {cite("S25")}), более 220 тыс. GPU в Colossus 1 — по составу из поста Илона Маска ({cite("S56")}) это ≈ 200 тыс. H100/H200 и 30 тыс. GB200, то есть ≈ {tk(cp["Colossus 1"]["h100e_epoch"])} эквивалентов H100 ({cite("S27")}, {cite("S37")}), {tkr(parts[pk[2]]["p05"], parts[pk[2]]["p95"])} TPU Google (сделка до 1 млн, {cite("S43")}), до {tk(parts[pk[3]]["p95"])} GPU в Microsoft Azure и CoreWeave и до {tk(parts[pk[4]]["p95"])} GPU во втором кампусе SpaceX Colossus 2; три последних слагаемых — наши диапазоны в штуках, заданные независимо от диапазонов в эквивалентах H100 в таблице выше.</p>

<h2>Обучение и инференс</h2>
<p>Одни и те же чипы могут переключаться между обслуживанием пользователей и экспериментами, поэтому деление в чипах или GPU-часах компании не публикуют. Известно только деление расходов на облачные вычисления — из утечек инвесторских документов и оценок Epoch AI. Под «обучением» здесь понимается весь бюджет исследований и разработки: эксперименты, исследовательские прогоны и дообучение; финальное обучение одной модели — меньшая его часть ({cite("S08")}).</p>
<div class="legend"><span style="--sw:var(--openai)">обучение и исследования (OpenAI)</span><span style="--sw:var(--anthropic)">обучение и исследования (Anthropic)</span><span style="--sw:var(--neutral)">инференс</span></div>
<div class="tw">{chart_split()}</div>
<p class="cap">Доли расходов на облачные вычисления. Штриховка — диапазон наших сценариев на 2026 год.</p>
{t_split}
<p>Оговорки к 2026 году. Прогнозы OpenAI сделаны в разное время: ${ru(sc["A"]["inf_bn"],1)} млрд на инференс — до февральского пересмотра планов, $32 млрд на обучение — в феврале, $50 млрд всего — в мае; инференс в 2025 году вырос в четыре раза, так что план, вероятно, занижает его долю. По Anthropic валовая маржа инференса не раскрыта, поэтому доля обучения — только сценарии. В аудированной отчётности OpenAI за 2025 год отдельной строки «обучение / инференс» нет: платежи Microsoft составили $10,59 млрд по статье исследований и $6,05 млрд по себестоимости выручки ({cite("S34")}). Это бухгалтерская разбивка по статьям и только по одному поставщику: в «исследования» попадают и вычисления под продуктовую разработку, часть инференса идёт мимо Microsoft, а сумма $16,6 млрд чуть больше оценки Epoch AI $16,3 млрд, потому что аудированная отчётность считает начисления, а Epoch AI — расходы на облако по оценке The Information; поэтому эти ряды чисел мы не складываем и с долями 49 % / 51 % не сравниваем. Отраслевые пропорции описывают рынок в целом и на лаборатории не переносятся: по Gartner рынок облачной аренды под ИИ в 2026 году — $42 млрд, инференс $23,3 млрд против обучения $19 млрд ({cite("S30")}), то есть меньше бюджета одной OpenAI; по Deloitte инференс займёт две трети всех вычислений ИИ в 2026 году ({cite("S53")}).</p>

<h2>Что изменится к концу 2026 года</h2>
<div class="two"><div><h3>OpenAI</h3>{openai_2026}</div><div><h3>Anthropic</h3>{anthropic_2026}</div></div>
<p>В 2025 году инференс OpenAI вырос вчетверо за год и сравнялся с обучением по расходам. План OpenAI на 2026 год снова смещает бюджет к обучению, но из-за агентов и моделей с рассуждением фактическая доля инференса, скорее всего, окажется выше плановой. Первые аудированные строки себестоимости и расходов на исследования появятся в публичных проспектах IPO: OpenAI объявила о конфиденциальной подаче 8 июня 2026, Anthropic — 1 июня 2026 (обе даты — {cite("S22")}).</p>

<h2>Что нужно помнить, глядя на эти числа</h2>
<ul>
<li>Точку сравнения дают только данные на конец 2025 года. Всё после этой даты — модель с интервалами, а не отчётность.</li>
<li>1,4 ГВт Anthropic — оценка конкурента; неизвестно даже, мощность это здания или оборудования. Epoch AI закладывает диапазон 1,0–1,9 ГВт ({cite("S04")}).</li>
<li>Инференс на площадках партнёров учтён у Anthropic и не учтён у OpenAI: сравнение занижает OpenAI на 10–25 %.</li>
<li>Деление на обучение и инференс существует только в деньгах, и «обучение» там — весь бюджет исследований. В 2026 году это сценарии, а не факты.</li>
<li>Законтрактованные гигаватты — верхняя граница, а не прогноз ввода: OpenAI отказалась от расширения Абилина сверх строящихся восьми зданий ({cite("S37")}) и от площадки в Норвегии, а проект в Великобритании приостановила ({cite("S12")}); другие сроки сдвигаются.</li>
</ul>

<h2 class="sources">Все использованные ссылки</h2>
<div class="sources"><ul>{{SOURCES_LIST}}</ul></div>
<h2>Как воспроизвести числа</h2>
<p>Все числа отчёта считает один Jupyter-ноутбук <code>gpu_fleet_review.ipynb</code> из репозитория; входные данные (реестр источников, копии CSV Epoch AI, состав парков) встроены в него, сеть не обязательна. Порядок:</p>
<ol>
<li>Установить зависимости (Python 3.9 или новее): <code>pip install -r requirements.txt</code>.</li>
<li>Выполнить ноутбук целиком: <code>jupyter nbconvert --to notebook --execute --inplace gpu_fleet_review.ipynb</code> (около минуты) или открыть его в Jupyter и запустить все ячейки.</li>
<li>Результаты появятся в папке <code>gpu_fleet_review_out/</code>: этот отчёт (<code>results/report_cto.html</code>), расчёты в JSON и Markdown (<code>results/nowcast_*.json</code>, <code>chips_*.json</code>, <code>split_*.json</code>), реестр источников (<code>data/sources_2026-09-27.csv</code>) и подробный документ с приложениями (<code>draft_v2.md</code>).</li>
<li>Три расчётных скрипта можно запускать и отдельно: <code>python calc_nowcast.py</code>, <code>python calc_chips.py</code>, <code>python calc_split.py</code> из папки <code>gpu_fleet_review_out/</code>.</li>
</ol>
<p>Дата оценки зафиксирована как {D_LONG} (переменная окружения <code>NOWCAST_DATE</code> позволяет пересчитать на другую дату); генератор случайных чисел имеет фиксированное начальное значение, поэтому повторный запуск даёт те же числа. Модели Epoch AI пересчитаны заново и воспроизводят их медианы с точностью лучше 1 %.</p>
<div class="foot">Расчёты: 200 000 прогонов с фиксированным начальным значением генератора случайных чисел; источники проверены {date_ru(ACCESSED)}.</div>
</div>
<div id="tip" role="tooltip"></div>
<script>
(function(){{var t=document.getElementById('tip');function show(e){{var g=e.target.closest('.hit');if(!g)return;t.textContent=g.getAttribute('data-tip');t.style.opacity='1';move(e);}}
function move(e){{var x=e.clientX+14,y=e.clientY+14;var w=t.offsetWidth,h=t.offsetHeight;if(x+w>window.innerWidth-8)x=e.clientX-w-14;if(y+h>window.innerHeight-8)y=e.clientY-h-14;t.style.left=x+'px';t.style.top=y+'px';}}
function hide(e){{if(e.relatedTarget&&e.relatedTarget.closest&&e.relatedTarget.closest('.hit'))return;t.style.opacity='0';}}
document.querySelectorAll('.chart').forEach(function(c){{c.addEventListener('mouseover',show);c.addEventListener('mousemove',move);c.addEventListener('mouseout',hide);}});}})();
</script>"""
def src_item(sid):
    r = SRC[SRC['id'] == sid].iloc[0]; t = TITLE.get(sid, r['title'])
    link = f'<a class="src" href="{esc(r["url"])}" target="_blank" rel="noopener">{esc(t)}</a>' if r['url'] else esc(t)
    note = f' <span class="cap">({esc(NOTE[sid])})</span>' if sid in NOTE else ''
    return f'<li>{esc(PUB.get(sid, r["publisher"]))}, {date_ru(r["date"])} — {link}{note}</li>'
sources_list = ''.join(src_item(sid) for sid in sorted(USED_SOURCES, key=lambda s: SRC.loc[SRC['id'] == s, 'date'].iloc[0]))
body_inner = body_inner.replace('{SOURCES_LIST}', sources_list)
def _typo_text(t):
    t = re.sub(r'(\d)[ \u2009](\d{3})(?!\d)', '\\1\u202f\\2', t)
    t = re.sub(r'(\d) %', '\\1\u00a0%', t)
    t = t.replace('≈ ', '≈\u00a0')
    t = re.sub(r'(\d) (ГВт|МВт|млн|млрд|тыс\.|Вт|раза|раз\b)', '\\1\u00a0\\2', t)
    return t
def typo(h):
    """Неразрывные пробелы только в текстовых узлах и в подсказках data-tip; атрибуты вроде viewBox не трогаем."""
    out = []
    for part in re.split(r'(<[^>]+>)', h):
        if part.startswith('<'):
            out.append(re.sub(r'data-tip="([^"]*)"', lambda m: 'data-tip="' + _typo_text(m.group(1)) + '"', part))
        else:
            out.append(_typo_text(part))
    return ''.join(out)
body_inner = typo(body_inner)
report_full = f'<!DOCTYPE html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{head_inner}\n</head>\n<body>\n{body_inner}\n</body>\n</html>\n'
write_text(report_full, OUT / 'results' / 'report_cto.html')
write_text(head_inner + '\n' + body_inner, OUT / 'results' / 'report_cto_artifact.html')   # версия без обёртки документа — для публикации как артефакт
_txt = re.sub(r'<[^>]+>', '', body_inner.split('<h2 class="sources">')[0])
leftover = re.findall(r'\[S\d+\]|\[V2?\]|\[E\]|\[N\]|\[K\]|\[X\]|nowcast|H100e|R&amp;D-compute|Δt|ГВт IT|МВт IT|\d\.\d', _txt)
print(f"report_cto.html: {len(report_full)/1024:.0f} КБ; использовано источников: {len(USED_SOURCES)}; остатков кодов/обозначений/неверного формата чисел в тексте: {len(leftover)} {set(leftover) if leftover else ''}")
