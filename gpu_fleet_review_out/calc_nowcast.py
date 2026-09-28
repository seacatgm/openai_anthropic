# -*- coding: utf-8 -*-
"""calc_nowcast.py — воспроизведение оценок Epoch (OpenAI, Anthropic; конец 2025) и nowcast на дату слайда.

Только NumPy/pandas. Константы помечены `# [FACT S-nn]` (реестр data/sources_2026-09-27.csv) или `# [ASSUMPTION]`.
Запуск отдельно:  python calc_nowcast.py           (NOWCAST_DATE, SEED, N_MC — через переменные окружения)
Из ноутбука:      %run -i calc_nowcast.py          (переменные берутся из ноутбука)
Детерминирован: один seed -> один результат.
"""
import os, io, sys, json, math, datetime as dt
from pathlib import Path
import numpy as np
import pandas as pd

# ------------------------------------------------------------------ параметры (из ноутбука или окружения)
_g = globals()
NOWCAST_DATE = _g.get('NOWCAST_DATE') or dt.date.fromisoformat(os.environ.get('NOWCAST_DATE', dt.date.today().isoformat()))
SEED  = int(_g.get('SEED')  or os.environ.get('SEED', 20260927))
N_MC  = int(_g.get('N_MC')  or os.environ.get('N_MC', 200_000))
OUT   = Path(_g.get('OUT')  or os.environ.get('OUT', Path(__file__).resolve().parent))
ACCESSED = _g.get('ACCESSED', '2026-09-27')
DATE_TAG = NOWCAST_DATE.isoformat()
Z90 = 1.6448536269514722

# ------------------------------------------------------------------ распределения (аналоги squigglepy, которыми пользуется Epoch)
def lognorm_ci(lo, hi, n, rng):
    """to(lo, hi): лог-нормальное с 5-м = lo и 95-м = hi процентилем."""
    mu = (math.log(lo) + math.log(hi)) / 2; sigma = (math.log(hi) - math.log(lo)) / (2 * Z90)
    return np.exp(rng.normal(mu, sigma, n))

def lognorm_med_ci(med, lo, hi, n, rng):
    """Лог-нормальное по медиане и 90 % ДИ: медиана точная, sigma из отношения p95/p05."""
    sigma = (math.log(hi) - math.log(lo)) / (2 * Z90)
    return np.exp(rng.normal(math.log(med), sigma, n))

def norm_ci(lo, hi, n, rng, lclip=None, rclip=None):
    x = rng.normal((lo + hi) / 2, (hi - lo) / (2 * Z90), n)
    if lclip is not None: x = np.maximum(x, lclip)
    if rclip is not None: x = np.minimum(x, rclip)
    return x

def pct(x, qs=(5, 25, 50, 75, 95)):
    v = np.percentile(np.asarray(x), qs); return {f'p{q:02d}': float(a) for q, a in zip(qs, v)}

def ru(x, nd=2):
    return f'{x:,.{nd}f}'.replace(',', ' ').replace('.', ',')
def ru_m(x, nd=2):  return ru(x / 1e6, nd) + ' млн'
def ru_gw(x, nd=1): return ru(x / 1000, nd) + ' ГВт'

# ------------------------------------------------------------------ факты Epoch: итоги по годам (H100e)
EPOCH_YEAR_END_FALLBACK = {        # [FACT S02/S03] ai_chip_users_year_end_by_lab.csv (Generated 2026-09-09)
    ('OpenAI', 2023): (70131.457, 102534.711, 136201.429),
    ('OpenAI', 2024): (276938.352, 386218.710, 486056.639),
    ('OpenAI', 2025): (1251477.083, 1743439.849, 2185142.346),
    ('Anthropic', 2024): (145189.553, 208559.983, 298183.150),
    ('Anthropic', 2025): (842241.626, 1189573.886, 1716534.704),
}
def load_epoch_year_end():
    """Берём скачанный CSV, если он есть в data/epoch/, иначе встроенные значения."""
    files = sorted((OUT / 'data' / 'epoch').glob('ai_chip_users_year_end_by_lab_*.csv')) if (OUT / 'data' / 'epoch').exists() else []
    if files:
        df = pd.read_csv(files[-1]); df = df[df['Lab'].isin(['OpenAI', 'Anthropic'])]
        return {(r.Lab, int(r.Year)): (float(r.h100e_p5), float(r.h100e_med), float(r.h100e_p95)) for r in df.itertuples()}, files[-1].name
    return dict(EPOCH_YEAR_END_FALLBACK), 'embedded'
EPOCH_YE, EPOCH_YE_SRC = load_epoch_year_end()

# ------------------------------------------------------------------ модель OpenAI «по мощности» (Epoch, notebooks/openai_power_model.ipynb)
DISCLOSED_MW = {2023: 200.0, 2024: 600.0, 2025: 1900.0}     # [FACT S01] 0,2 / 0,6 / ~1,9 ГВт (блог CFO, январь 2026)
CHIPS = ['A100', 'H100/H200', 'B200', 'B300']
SERVER_W = {'A100': 812.5, 'H100/H200': 1275.0, 'B200': 1833.3, 'B300': 1944.4}   # [FACT S04] мощность сервера на GPU, Вт (DGX / NVL72)
H100E_PER = {'A100': 0.3153, 'H100/H200': 1.0, 'B200': 2.5265, 'B300': 2.5265}    # [FACT S04, S10] H100e на чип (GB300 = GB200 у Epoch)
IT_OVERHEAD_CI, IT_OVERHEAD_FLOOR = (0.963, 1.3495), 1.0    # [FACT S04] сервер -> IT: медиана 1,14, 5–95 % 1,00–1,35
LAG_QUARTERS_CI = (0.5, 2.0)                                # [FACT S04] лаг развёртывания за миксом продаж NVIDIA (кварталы)
P_GROSS, PUE_CI, IF_IT_CI = 0.10, (1.1, 1.7), (0.95, 1.05)  # [FACT S04] P(раскрыта мощность объекта) = 0,1; PUE 1,1–1,7
ACCURACY_CI, ROUNDING_MW = (0.9, 1.2), 50.0                 # [FACT S04] точность внутренней цифры; округление ±50 МВт
# Кумулятивный парк NVIDIA у Microsoft по типам чипов, медианы штук (Epoch AI Chip Owners, cumulative_by_chip_type.csv, 27.09.2026)  [FACT S04/S10]
MICROSOFT_UNITS_CSV = """End date,A100,H100/H200,B200,B300
2022-03-31,46839,0,0,0
2022-06-30,97887,0,0,0
2022-09-30,146521,1342,0,0
2022-12-31,174086,10027,0,0
2023-03-31,190247,25357,0,0
2023-06-30,207773,66319,0,0
2023-09-30,222882,137133,0,0
2023-12-31,227034,235326,0,0
2024-03-31,227034,368963,0,0
2024-06-30,227034,534139,0,0
2024-09-30,227034,733776,0,0
2024-12-31,227034,917002,55416,0
2025-03-31,227034,1003644,189645,0
2025-06-30,227034,1059443,295327,50463
2025-09-30,227034,1088658,374249,171630
2025-12-31,227034,1093460,459481,323881
2026-03-31,227034,1093460,483597,366189
"""
MS = pd.read_csv(io.StringIO(MICROSOFT_UNITS_CSV), parse_dates=['End date']).set_index('End date')
YEARS = [2023, 2024, 2025]
YEAR_END = {y: pd.Timestamp(f'{y}-12-31') for y in YEARS}

def sample_openai_power(n, rng):
    """IT-мощность парка OpenAI по годам: (раскрыто ± округление) × фактор определения (IT/объект) × фактор точности."""
    is_gross = rng.random(n) < P_GROSS
    definition = np.where(is_gross, 1.0 / lognorm_ci(*PUE_CI, n, rng), lognorm_ci(*IF_IT_CI, n, rng))
    accuracy = lognorm_ci(*ACCURACY_CI, n, rng)
    return {y: (DISCLOSED_MW[y] + rng.triangular(-ROUNDING_MW, 0.0, ROUNDING_MW, n)) * definition * accuracy for y in YEARS}, definition, accuracy

def _ms_power_series(overhead_median):
    w = {c: SERVER_W[c] * overhead_median for c in CHIPS}
    return (MS * pd.Series(w) / 1e6)     # МВт IT по типам чипов у Microsoft

def openai_chip_power_shares(lag_quarters, overhead_median):
    """Доля IT-мощности парка OpenAI по типам чипов на конец каждого года при заданном лаге (векторно по прогонам)."""
    msp = _ms_power_series(overhead_median)
    start = msp.index[0]; days = np.array([(d - start).days for d in msp.index], float)
    lag_days = lag_quarters * 365.25 / 4
    cum = {y: {c: np.interp((YEAR_END[y] - start).days - lag_days, days, msp[c].values) for c in CHIPS} for y in YEARS}
    added_mix, prev = {}, None
    for y in YEARS:
        add = {c: (np.maximum(cum[y][c], 0.0) if prev is None else np.maximum(cum[y][c] - cum[prev][c], 0.0)) for c in CHIPS}
        tot = sum(add.values()); added_mix[y] = {c: add[c] / tot for c in CHIPS}; prev = y
    carried, shares, p_prev = {c: 0.0 for c in CHIPS}, {}, 0.0
    for y in YEARS:
        p_add = DISCLOSED_MW[y] - p_prev; p_prev = DISCLOSED_MW[y]
        for c in CHIPS: carried[c] = carried[c] + p_add * added_mix[y][c]
        tot = sum(carried.values()); shares[y] = {c: carried[c] / tot for c in CHIPS}
    return shares

def reproduce_openai(n, rng):
    """Воспроизведение модели Epoch: возвращает по годам H100e, штуки и штуки по типам чипов (массивы прогонов)."""
    overhead = np.maximum(lognorm_ci(*IT_OVERHEAD_CI, n, rng), IT_OVERHEAD_FLOOR)
    overhead_med = float(np.median(overhead))
    lag = lognorm_ci(*LAG_QUARTERS_CI, n, rng)
    power, definition, accuracy = sample_openai_power(n, rng)
    shares = openai_chip_power_shares(lag, overhead_med)
    out = {'power_mw': power, 'definition': definition, 'accuracy': accuracy, 'lag_q': lag, 'overhead': overhead}
    for y in YEARS:
        counts = {c: power[y] * shares[y][c] * 1e6 / (SERVER_W[c] * overhead) for c in CHIPS}
        h100e = {c: counts[c] * H100E_PER[c] for c in CHIPS}
        out[y] = {'counts': counts, 'h100e': h100e, 'chips': sum(counts.values()), 'H100e': sum(h100e.values())}
    return out

# ------------------------------------------------------------------ модель Anthropic (Epoch, notebooks/anthropic_power_2025.ipynb)
ANTH_POWER_GW_CI = (1.0, 1.9)             # [FACT S04] 90 % ДИ IT-мощности вокруг 1,4 ГВт из меморандума OpenAI [S11]
TRAINIUM_SHARE_CI, TRAINIUM_SHARE_CLIP = (0.35, 0.70), (0.10, 0.90)   # [FACT S04] доля Trainium2 в IT-мощности (медиана 52 %)
NONTRAINIUM_EFF_CI, TRAINIUM_EFF_CI = (0.80, 1.25), (0.85, 1.20)     # [FACT S04] множители неопределённости эффективности
T2_H100E = 1299 / 1979                    # [FACT S04/S10] Trainium2 = 0,656 H100e (плотные 8-бит FLOP/s)
T2_REF_H100E, T2_REF_IT_MW = 300_000, 398 # [FACT S04/S37] Rainier, снимок середины 2025: 300 тыс. H100e при 398 МВт IT
T2_IT_W = T2_H100E / (T2_REF_H100E / T2_REF_IT_MW) * 1e6            # -> 871 Вт IT на чип
T2_PER_MW = T2_H100E / T2_IT_W * 1e6                                # -> 754 H100e/МВт
NVIDIA_MIX_PER_MW, TPU_MIX_PER_MW = 945.0, 1009.0                   # [FACT S04] NVIDIA-микс OpenAI 2025 и TPU-парк Google (v5+)
NONTRAINIUM_PER_MW = (NVIDIA_MIX_PER_MW + TPU_MIX_PER_MW) / 2       # 977 (Epoch: Nvidia ≈ TPU, берётся середина)

def reproduce_anthropic(n, rng):
    power_mw = lognorm_ci(*ANTH_POWER_GW_CI, n, rng) * 1000.0
    share = norm_ci(*TRAINIUM_SHARE_CI, n, rng, *TRAINIUM_SHARE_CLIP)
    nt_eff = lognorm_ci(*NONTRAINIUM_EFF_CI, n, rng); t_eff = lognorm_ci(*TRAINIUM_EFF_CI, n, rng)
    blended = share * T2_PER_MW * t_eff + (1 - share) * NONTRAINIUM_PER_MW * nt_eff
    return {'power_mw': power_mw, 'trainium_share': share, 'blended_per_mw': blended,
            'H100e': power_mw * blended, 'trainium2_chips': share * power_mw * 1e6 / T2_IT_W}

# ------------------------------------------------------------------ nowcast
GROWTH_CI = {'OpenAI': (2.5, 4.5), 'Anthropic': (2.5, 5.0)}   # [ASSUMPTION] годовой множитель g, 90 % интервал (обоснование — в заголовке блока 2)
ETA_2025 = {'OpenAI': 1743439.85 / 1949.84, 'Anthropic': 865.32}   # [FACT S04] H100e/МВт парка на конец 2025 (Epoch: медианы)
ETA_NEW = {'OpenAI': 945.0, 'Anthropic': 950.0}                     # [ASSUMPTION] эффективность новых вводов 2026 (см. заголовок блока)
ETA_NEW_ALT = {'OpenAI': 1209.0, 'Anthropic': 1009.0}               # [ASSUMPTION] альтернатива: чистый GB200 / TPU-парк
P_IT_2025 = {'OpenAI': 1949.84, 'Anthropic': 1377.29}               # [FACT S04] медианы IT-мощности 2025, МВт (intermediates CSV)
P_DISCLOSED_2025 = {'OpenAI': 1900.0, 'Anthropic': 1400.0}          # [FACT S01], [FACT S11]

def delta_t_years(date):
    return (date - dt.date(2025, 12, 31)).days / 365.0

def nowcast(lab, n, rng, date=None, g_ci=None, n2025_samples=None, eta_new=None):
    """N(t) = N_2025 · g^Δt. N_2025 — лог-нормальное по медиане и 90 % ДИ Epoch (или переданные прогоны)."""
    date = date or NOWCAST_DATE; g_ci = g_ci or GROWTH_CI[lab]; eta_new = eta_new or ETA_NEW[lab]
    p5, med, p95 = EPOCH_YE[(lab, 2025)]
    n2025 = n2025_samples if n2025_samples is not None else lognorm_med_ci(med, p5, p95, n, rng)
    g = lognorm_ci(*g_ci, n, rng)
    dtv = delta_t_years(date)
    n_t = n2025 * g ** dtv
    gw_it = n2025 / ETA_2025[lab] + (n_t - n2025) / eta_new       # МВт: база по η_2025, прирост по η_new
    return {'n2025': n2025, 'g': g, 'dt': dtv, 'h100e': n_t, 'gw_it_mw': gw_it}

# ------------------------------------------------------------------ перекрёстная проверка «по вводам» (каталог ЦОД Epoch, 27.09.2026)  [FACT S37]
SITE_TIMELINES_CSV = """site,lab,date,it_mw,facility_mw,h100e,kind
OpenAI Stargate Abilene,OpenAI,2025-09-26,105,147,127337,observed
OpenAI Stargate Abilene,OpenAI,2025-12-24,211,295,254674,observed
OpenAI Stargate Abilene,OpenAI,2026-05-23,421,590,509348,observed
OpenAI Stargate Abilene,OpenAI,2026-11-01,843,1180,1018696,forecast
Anthropic-Amazon New Carlisle (Rainier),Anthropic,2025-06-23,398,478,300152,observed
Anthropic-Amazon New Carlisle (Rainier),Anthropic,2025-12-23,626,751,471450,observed
Anthropic-Amazon New Carlisle (Rainier),Anthropic,2026-03-23,910,1092,685912,observed
Anthropic-Amazon New Carlisle (Rainier),Anthropic,2026-10-19,1037,1244,818428,forecast
Amazon Madison Mega Site,Anthropic,2025-06-23,284,341,214348,observed
Amazon Madison Mega Site,Anthropic,2027-03-01,284,478,300087,forecast
Colossus 1 (Anthropic с 06.2026),Anthropic,2026-06-01,340,425,275796,observed
Colossus 1 (Anthropic с 06.2026),Anthropic,2025-01-01,0,0,0,observed
"""
SITES = pd.read_csv(io.StringIO(SITE_TIMELINES_CSV), parse_dates=['date'])
# Диапазоны для вводов, которых нет в каталоге Epoch (равномерные на интервале)  [ASSUMPTION]
ANTH_UNTRACKED_H100E = {'TPU Google (ввод 2026, до 1 ГВт)': (300_000, 800_000),     # [K/V S43] «well over a gigawatt» в 2026; доля введённого к дате
                        'Azure / CoreWeave GPU (до 1 ГВт Azure)': (0, 300_000),      # [K S44], [V S28]
                        'доля Colossus 2 (Anthropic — пользователь с 06.2026)': (0, 300_000)}  # [FACT S37] каталог Epoch: Anthropic среди пользователей
OPENAI_UNTRACKED_NOTE = ('Azure Fairwater, Oracle вне Абилина, CoreWeave, Google Cloud, Cerebras — в каталоге ЦОД Epoch не итемизированы; '
                         'в 2025 прирост OpenAI (+1,36 млн H100e) шёл в основном через Azure, поэтому сумма по площадкам — жёсткая нижняя граница')

def site_value_at(site_df, date):
    d = site_df[site_df['date'] <= pd.Timestamp(date)]
    return float(d.sort_values('date')['h100e'].iloc[-1]) if len(d) else 0.0

def cross_check(lab, n, rng, date=None):
    date = date or NOWCAST_DATE
    base = EPOCH_YE[(lab, 2025)][1]
    rows = []
    for site, sdf in SITES[SITES['lab'] == lab].groupby('site', sort=False):
        v0 = site_value_at(sdf, dt.date(2025, 12, 31)); v1 = site_value_at(sdf, date)
        rows.append({'site': site, 'h100e_end2025': v0, f'h100e_{date}': v1, 'delta': v1 - v0, 'status': 'E (каталог Epoch)'})
    tracked = sum(r['delta'] for r in rows)
    untracked = {}
    total = np.full(n, base + tracked)
    if lab == 'Anthropic':
        for name, (lo, hi) in ANTH_UNTRACKED_H100E.items():
            s = rng.uniform(lo, hi, n); untracked[name] = (lo, hi); total = total + s
    return {'base_epoch_2025': base, 'tracked_sites': rows, 'tracked_delta': tracked, 'lower_bound_facts_only': base + tracked,
            'untracked_ranges': untracked, 'total': pct(total)}

# ------------------------------------------------------------------ чувствительность
def sensitivity(lab, n, rng):
    res = {}
    p5, med, p95 = EPOCH_YE[(lab, 2025)]
    # (а)/(б): раскрытая мощность — мощность объекта, PUE 1,3 -> IT-мощность и H100e ниже в 1,3 раза  [ASSUMPTION] микс чипов тот же
    scale = 1 / 1.3
    r = nowcast(lab, n, rng, n2025_samples=lognorm_med_ci(med * scale, p5 * scale, p95 * scale, n, rng))
    res['disclosed_is_facility_power_PUE1.3'] = {'h100e_2025_median': med * scale, 'h100e': pct(r['h100e']), 'gw_it_mw': pct(r['gw_it_mw'])}
    # (в): g на границах приора (фиксированный)
    for tag, g in (('g_low', GROWTH_CI[lab][0]), ('g_high', GROWTH_CI[lab][1])):
        n2025 = lognorm_med_ci(med, p5, p95, n, rng); n_t = n2025 * g ** delta_t_years(NOWCAST_DATE)
        res[tag] = {'g': g, 'h100e': pct(n_t), 'gw_it_mw': pct(n2025 / ETA_2025[lab] + (n_t - n2025) / ETA_NEW[lab])}
    # эффективность новых вводов: альтернативная η
    r = nowcast(lab, n, rng, eta_new=ETA_NEW_ALT[lab])
    res[f'eta_new_{int(ETA_NEW_ALT[lab])}'] = {'gw_it_mw': pct(r['gw_it_mw'])}
    return res

# ------------------------------------------------------------------ главный расчёт
def main(verbose=True):
    rng = np.random.default_rng(SEED)
    R = {'meta': {'nowcast_date': DATE_TAG, 'delta_t_years': delta_t_years(NOWCAST_DATE), 'seed': SEED, 'n_mc': N_MC,
                  'epoch_year_end_source': EPOCH_YE_SRC, 'accessed': ACCESSED,
                  'priors': {'growth_90ci': GROWTH_CI, 'eta_2025_h100e_per_mw': ETA_2025, 'eta_new_h100e_per_mw': ETA_NEW}}}
    # 1) воспроизведение Epoch
    oa = reproduce_openai(N_MC, rng); an = reproduce_anthropic(N_MC, rng)
    rep = {}
    for lab, samples in (('OpenAI', oa[2025]['H100e']), ('Anthropic', an['H100e'])):
        p5, med, p95 = EPOCH_YE[(lab, 2025)]; q = pct(samples)
        rep[lab] = {'reproduced': q, 'epoch': {'p05': p5, 'p50': med, 'p95': p95},
                    'median_deviation_%': 100 * (q['p50'] / med - 1), 'within_3pct': abs(q['p50'] / med - 1) < 0.03}
    rep['OpenAI'].update({'chips_2025': pct(oa[2025]['chips']), 'power_it_mw_2025': pct(oa['power_mw'][2025]),
                          'blackwell_share_of_chips': pct((oa[2025]['counts']['B200'] + oa[2025]['counts']['B300']) / oa[2025]['chips']),
                          'blackwell_share_of_h100e': pct((oa[2025]['h100e']['B200'] + oa[2025]['h100e']['B300']) / oa[2025]['H100e']),
                          'hopper_to_blackwell_count_ratio_median': float(np.median(oa[2025]['counts']['H100/H200'] / np.maximum(oa[2025]['counts']['B200'] + oa[2025]['counts']['B300'], 1.0))),
                          'a100_share_of_chips': pct(oa[2025]['counts']['A100'] / oa[2025]['chips']),
                          'by_year': {str(y): pct(oa[y]['H100e']) for y in YEARS}})
    rep['Anthropic'].update({'power_it_mw_2025': pct(an['power_mw']), 'trainium_share': pct(an['trainium_share']),
                             'blended_h100e_per_mw': pct(an['blended_per_mw']), 'trainium2_chips': pct(an['trainium2_chips'])})
    R['reproduction'] = rep
    # 2) nowcast
    for lab in ('OpenAI', 'Anthropic'):
        nc = nowcast(lab, N_MC, rng)
        nc_rep = nowcast(lab, N_MC, rng, n2025_samples=(oa[2025]['H100e'] if lab == 'OpenAI' else an['H100e']))
        R[lab.lower()] = {'h100e': pct(nc['h100e']), 'gw_it_mw': pct(nc['gw_it_mw']), 'gw_it': {k: v / 1000 for k, v in pct(nc['gw_it_mw']).items()},
                          'n2025_lognormal_fit': pct(nc['n2025']), 'g_prior': pct(nc['g']),
                          'multiplier_vs_end2025': pct(nc['h100e'] / nc['n2025']),
                          'h100e_if_n2025_from_reproduction': pct(nc_rep['h100e']),
                          'cross_check_by_sites': cross_check(lab, N_MC, rng),
                          'epoch_end2025': dict(zip(('p05', 'p50', 'p95'), EPOCH_YE[(lab, 2025)])),
                          'power_end2025': {'disclosed_or_leaked_mw': P_DISCLOSED_2025[lab], 'modelled_it_mw_median': P_IT_2025[lab]}}
        cc = R[lab.lower()]['cross_check_by_sites']
        R[lab.lower()]['cross_check_gap_%'] = 100 * (cc['total']['p50'] / R[lab.lower()]['h100e']['p50'] - 1)
    R['sensitivity'] = {lab.lower(): sensitivity(lab, N_MC, rng) for lab in ('OpenAI', 'Anthropic')}
    R['_samples'] = {'openai_h100e': nowcast('OpenAI', 20000, np.random.default_rng(SEED + 1))['h100e'],
                     'anthropic_h100e': nowcast('Anthropic', 20000, np.random.default_rng(SEED + 2))['h100e'],
                     'openai_rep_h100e': oa[2025]['H100e'][:20000], 'anthropic_rep_h100e': an['H100e'][:20000]}
    # 3) файлы
    (OUT / 'results').mkdir(parents=True, exist_ok=True)
    R_json = {k: v for k, v in R.items() if k != '_samples'}
    (OUT / 'results' / f'nowcast_{DATE_TAG}.json').write_text(json.dumps(R_json, ensure_ascii=False, indent=2, default=float), encoding='utf-8')
    (OUT / 'results' / f'nowcast_{DATE_TAG}.md').write_text(nowcast_markdown(R), encoding='utf-8')
    if verbose: print_summary(R)
    return R

def nowcast_markdown(R):
    o, a = R['openai'], R['anthropic']; ro, ra = R['reproduction']['OpenAI'], R['reproduction']['Anthropic']
    d = R['meta']['nowcast_date']; so, sa = R['sensitivity']['openai'], R['sensitivity']['anthropic']
    g_o, g_a = GROWTH_CI['OpenAI'], GROWTH_CI['Anthropic']
    return f"""# Nowcast парка на {d} — три абзаца для документа

Все числа ниже — оценки `[E]`. Приоры: `N_2025` — лог-нормальное по медиане и 90 % ДИ Epoch [S02] (OpenAI {ru_m(ro['epoch']['p50'])}, {ru_m(ro['epoch']['p05'])}–{ru_m(ro['epoch']['p95'])}; Anthropic {ru_m(ra['epoch']['p50'])}, {ru_m(ra['epoch']['p05'])}–{ru_m(ra['epoch']['p95'])}); годовой множитель `g` — лог-нормальное с 90 % интервалом {ru(g_o[0],1)}–{ru(g_o[1],1)} (OpenAI) и {ru(g_a[0],1)}–{ru(g_a[1],1)} (Anthropic); `Δt` = {ru(R['meta']['delta_t_years'],3)} года; Монте-Карло {ru(R['meta']['n_mc'],0)} прогонов, seed {R['meta']['seed']}.

**1. Воспроизведение Epoch.** Модели Epoch переписаны на NumPy и дают на конец 2025 медиану {ru_m(ro['reproduced']['p50'])} H100e для OpenAI (Epoch {ru_m(ro['epoch']['p50'])}; отклонение {ru(ro['median_deviation_%'],1).replace('-', '−')} %) и {ru_m(ra['reproduced']['p50'])} для Anthropic (Epoch {ru_m(ra['epoch']['p50'])}; {ru(ra['median_deviation_%'],1).replace('-', '−')} %) `[E]`. Воспроизведённые 90 % ДИ: {ru_m(ro['reproduced']['p05'])}–{ru_m(ro['reproduced']['p95'])} и {ru_m(ra['reproduced']['p05'])}–{ru_m(ra['reproduced']['p95'])}. Побочный результат модели OpenAI — число физических ускорителей на конец 2025: медиана {ru_m(ro['chips_2025']['p50'])} (90 % ДИ {ru_m(ro['chips_2025']['p05'])}–{ru_m(ro['chips_2025']['p95'])}), Blackwell ≈ {100*ro['blackwell_share_of_chips']['p50']:.0f} % штук и ≈ {100*ro['blackwell_share_of_h100e']['p50']:.0f} % вычислительной мощности, Hopper : Blackwell ≈ {ru(ro['hopper_to_blackwell_count_ratio_median'],2)} : 1 `[E]`.

**2. Nowcast на {d}.** OpenAI: медиана {ru_m(o['h100e']['p50'])} H100e, 50 % интервал {ru_m(o['h100e']['p25'])}–{ru_m(o['h100e']['p75'])}, 90 % интервал {ru_m(o['h100e']['p05'])}–{ru_m(o['h100e']['p95'])}; в IT-мощности ≈ {ru_gw(o['gw_it_mw']['p50'])} (90 % ДИ {ru_gw(o['gw_it_mw']['p05'])}–{ru_gw(o['gw_it_mw']['p95'])}) `[E]`. Anthropic: {ru_m(a['h100e']['p50'])} H100e ({ru_m(a['h100e']['p25'])}–{ru_m(a['h100e']['p75'])}; 90 %: {ru_m(a['h100e']['p05'])}–{ru_m(a['h100e']['p95'])}), ≈ {ru_gw(a['gw_it_mw']['p50'])} ({ru_gw(a['gw_it_mw']['p05'])}–{ru_gw(a['gw_it_mw']['p95'])}) `[E]`. Множитель к концу 2025 — медиана ×{ru(o['multiplier_vs_end2025']['p50'],2)} (OpenAI) и ×{ru(a['multiplier_vs_end2025']['p50'],2)} (Anthropic). Перевод в ГВт: база по эффективности парка Epoch ({ETA_2025['OpenAI']:.0f} и {ETA_2025['Anthropic']:.0f} H100e/МВт), прирост — по {ETA_NEW['OpenAI']:.0f} и {ETA_NEW['Anthropic']:.0f} H100e/МВт `[ASSUMPTION]`; при чистом GB200 (1 209) ГВт OpenAI были бы {ru_gw(so['eta_new_1209']['gw_it_mw']['p50'])}.

**3. Перекрёстная проверка и чувствительность.** Сумма «по вводам» из каталога ЦОД Epoch [S37]: OpenAI — {ru_m(o['cross_check_by_sites']['lower_bound_facts_only'])} H100e (1,74 млн + Абилин {ru_m(o['cross_check_by_sites']['tracked_delta'])}), это жёсткая нижняя граница ({OPENAI_UNTRACKED_NOTE}); расхождение с медианой nowcast {ru(o['cross_check_gap_%'],0).replace('-', '−')} %. Anthropic — {ru_m(a['cross_check_by_sites']['lower_bound_facts_only'])} по фактам каталога (Rainier, Colossus 1) плюс диапазоны TPU/Azure/Colossus 2 → медиана {ru_m(a['cross_check_by_sites']['total']['p50'])} ({ru_m(a['cross_check_by_sites']['total']['p05'])}–{ru_m(a['cross_check_by_sites']['total']['p95'])}); расхождение с nowcast {ru(a['cross_check_gap_%'],0).replace('-', '−')} %. Чувствительность: если 1,9 ГВт — мощность объекта (PUE 1,3), nowcast OpenAI падает до {ru_m(so['disclosed_is_facility_power_PUE1.3']['h100e']['p50'])} H100e; если 1,4 ГВт Anthropic — мощность объекта, до {ru_m(sa['disclosed_is_facility_power_PUE1.3']['h100e']['p50'])}; при `g` на границах приора медиана OpenAI — {ru_m(so['g_low']['h100e']['p50'])} / {ru_m(so['g_high']['h100e']['p50'])}, Anthropic — {ru_m(sa['g_low']['h100e']['p50'])} / {ru_m(sa['g_high']['h100e']['p50'])} `[E]`.
"""

def print_summary(R):
    print(f"Δt = {R['meta']['delta_t_years']:.3f} г.  |  источник year_end: {R['meta']['epoch_year_end_source']}")
    for lab in ('OpenAI', 'Anthropic'):
        r = R['reproduction'][lab]; q = r['reproduced']; e = r['epoch']
        print(f"[воспроизведение] {lab:9s} 2025: {q['p05']/1e6:.3f} / {q['p50']/1e6:.3f} / {q['p95']/1e6:.3f} млн  "
              f"(Epoch {e['p05']/1e6:.3f} / {e['p50']/1e6:.3f} / {e['p95']/1e6:.3f}; медиана {r['median_deviation_%']:+.2f} %, ±3 %: {'OK' if r['within_3pct'] else 'FAIL'})")
    for lab in ('openai', 'anthropic'):
        h, g = R[lab]['h100e'], R[lab]['gw_it_mw']
        print(f"[nowcast {R['meta']['nowcast_date']}] {lab:9s}: H100e p05/p25/p50/p75/p95 = "
              f"{h['p05']/1e6:.2f} / {h['p25']/1e6:.2f} / {h['p50']/1e6:.2f} / {h['p75']/1e6:.2f} / {h['p95']/1e6:.2f} млн ;  "
              f"ГВт IT = {g['p05']/1e3:.1f} / {g['p50']/1e3:.1f} / {g['p95']/1e3:.1f} ;  по вводам: {R[lab]['cross_check_by_sites']['total']['p50']/1e6:.2f} млн ({R[lab]['cross_check_gap_%']:+.0f} %)")

if __name__ == '__main__':
    R_NOWCAST = main()
