%%writefile gpu_fleet_review_out/calc_chips.py
# -*- coding: utf-8 -*-
"""calc_chips.py — коэффициенты ГВт ↔ чипы ↔ H100e, число физических ускорителей, контрольные точки.
Только NumPy/pandas. Запуск: python calc_chips.py  |  из ноутбука: %run -i calc_chips.py
Импортирует распределения и модель OpenAI из calc_nowcast.py (тот же каталог)."""
import os, sys, json, math, datetime as dt
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
import calc_nowcast as CN
from calc_nowcast import lognorm_ci, norm_ci, pct, ru, ru_m, reproduce_openai, sample_openai_power

_g = globals()
NOWCAST_DATE = _g.get('NOWCAST_DATE') or CN.NOWCAST_DATE
SEED = int(_g.get('SEED') or CN.SEED); N_MC = int(_g.get('N_MC') or CN.N_MC); OUT = Path(_g.get('OUT') or CN.OUT)
DATE_TAG = NOWCAST_DATE.isoformat()

# ------------------------------------------------------------------ коэффициенты по чипам  [FACT S04, S10]
IT_OVERHEAD = 1.14                      # [FACT S04] медиана сервер -> IT
TPU_IT_OVERHEAD = 1.742                 # [FACT S04] overhead для TPU (перенесён с GB200 NVL72; у TPU нет публичных серверных спецификаций)
H100_FLOPS = 1.979e15                   # [FACT S10] знаменатель H100e (плотные 8-бит)
CHIP_ROWS = [  # chip, server_w_per_chip, overhead, it_w_per_chip, h100e_per_chip, source/note
    ('A100',      812.5,  IT_OVERHEAD, 812.5 * IT_OVERHEAD,   0.3153, 'Epoch S04 (DGX A100 6,5 кВт / 8)'),
    ('H100/H200', 1275.0, IT_OVERHEAD, 1275.0 * IT_OVERHEAD,  1.0,    'Epoch S04 (DGX H100 10,2 кВт / 8)'),
    ('GB200',     1833.3, IT_OVERHEAD, 1833.3 * IT_OVERHEAD,  2.5265, 'Epoch S04 (NVL72 132 кВт / 72)'),
    ('GB300',     1944.4, IT_OVERHEAD, 1944.4 * IT_OVERHEAD,  2.5265, 'Epoch S04 (NVL72 140 кВт / 72); H100e принят как у GB200 — пометка Epoch'),
    ('Trainium2', float('nan'), float('nan'), CN.T2_IT_W,      CN.T2_H100E, 'Epoch S04: ~500 Вт TDP × 1,74 = 871 Вт IT (привязка к Rainier 300k H100e / 398 МВт); 1299/1979 H100e'),
    ('Trainium3', float('nan'), float('nan'), float('nan'),    float('nan'), 'нет данных Epoch — не заполнено'),
    ('TPUv7 (Ironwood)', float('nan'), TPU_IT_OVERHEAD, 960 * TPU_IT_OVERHEAD, 4.614e15 / H100_FLOPS, 'Epoch S04/S10: TDP 960 Вт × 1,742; 4,614 PFLOP/s 8-бит → 2,33 H100e'),
]
rows = []
for chip, sw, ovh, itw, h, src in CHIP_ROWS:
    rows.append({'chip': chip, 'server_w_per_chip': sw, 'it_overhead': ovh, 'it_w_per_chip': itw, 'h100e_per_chip': h,
                 'chips_per_gw_it': (1e9 / itw) if itw == itw else float('nan'),
                 'h100e_per_gw_it': (1e9 / itw * h) if (itw == itw and h == h) else float('nan'), 'kind': 'chip', 'source': src})
# ------------------------------------------------------------------ строки «парки»  [FACT S04]
HOPPER_SHARE = 1.48 / 2.48; BLACKWELL_SHARE = 1 - HOPPER_SHARE           # Hopper : Blackwell = 1,48 : 1 по штукам  [FACT S04]
W_H, W_B = 1275.0 * IT_OVERHEAD, 1833.3 * IT_OVERHEAD
MIX_W = HOPPER_SHARE * W_H + BLACKWELL_SHARE * W_B                       # ≈ 1 710 Вт IT на чип
FLEETS = [
    ('NVIDIA-микс OpenAI, конец 2025 (Hopper:Blackwell 1,48:1)', MIX_W, 1e9 / MIX_W, 1e9 / MIX_W * (HOPPER_SHARE * 1.0 + BLACKWELL_SHARE * 2.5265), 'наш расчёт по Epoch S04 (Epoch: ~945 H100e/МВт, ~585 тыс. чипов/ГВт)'),
    ('Anthropic смешанный парк, конец 2025', float('nan'), float('nan'), 865.3e3, 'Epoch S04: 865 H100e/МВт (747–1 019)'),
    ('TPU-парк Google (v5e/v5p/v6e/v7), конец 2025', float('nan'), float('nan'), 1009e3, 'Epoch S04: ~1 009 H100e/МВт'),
    ('Trainium2-парк', CN.T2_IT_W, 1e9 / CN.T2_IT_W, CN.T2_PER_MW * 1e3, 'Epoch S04: 754 H100e/МВт'),
    ('1 ГВт объекта при PUE 1,3 → NVIDIA-микс OpenAI', MIX_W, 1e9 / 1.3 / MIX_W, 1e9 / 1.3 / MIX_W * (HOPPER_SHARE + BLACKWELL_SHARE * 2.5265), '[ASSUMPTION] PUE 1,3 — допущение внутри интервала Epoch 1,1–1,7'),
]
for name, itw, cpg, hpg, src in FLEETS:
    rows.append({'chip': name, 'server_w_per_chip': float('nan'), 'it_overhead': float('nan'), 'it_w_per_chip': itw, 'h100e_per_chip': float('nan'),
                 'chips_per_gw_it': cpg, 'h100e_per_gw_it': hpg, 'kind': 'fleet', 'source': src})
COEF = pd.DataFrame(rows)

# ------------------------------------------------------------------ Монте-Карло: физические ускорители
def chips_openai_2025_formula(n, rng):
    """N = P_IT / (w_H·1453 + w_B·2090), доля Blackwell по штукам ~ U(0,30; 0,50)  [ASSUMPTION]; P_IT — как у Epoch."""
    power, _, _ = sample_openai_power(n, rng)
    p_it = power[2025]
    w_b = rng.uniform(0.30, 0.50, n); w_h = 1 - w_b
    chips = p_it * 1e6 / (w_h * W_H + w_b * W_B)
    h100e = chips * (w_h * 1.0 + w_b * 2.5265)
    return {'chips': pct(chips), 'h100e': pct(h100e), 'blackwell_share_h100e': pct(w_b * 2.5265 / (w_h + w_b * 2.5265)), 'p_it_mw': pct(p_it)}

def chips_anthropic_2025(n, rng):
    """Trainium2 (871 Вт) по доле IT-мощности 35–70 % + NVIDIA/TPU при 1,4–1,7 кВт IT на чип  [ASSUMPTION: H100/GB200 в пропорции OpenAI ≈ 1,71 кВт; TPU v7 1,67; v6e 0,66; v5e 0,39]."""
    p = lognorm_ci(*CN.ANTH_POWER_GW_CI, n, rng) * 1e9   # ГВт -> Вт
    sh = norm_ci(*CN.TRAINIUM_SHARE_CI, n, rng, *CN.TRAINIUM_SHARE_CLIP)
    w_nt = rng.uniform(1400, 1700, n)
    t2 = sh * p / CN.T2_IT_W; nt = (1 - sh) * p / w_nt
    return {'chips': pct(t2 + nt), 'trainium2_chips': pct(t2), 'nvidia_tpu_chips': pct(nt)}

def chips_anthropic_mid2026(n, rng):
    """«По фактам»: ≥1 млн Trainium2 [V S25] + >220 тыс. GPU Colossus 1 [V S27] + диапазоны TPU / Azure-CoreWeave / Colossus 2 [ASSUMPTION]."""
    parts = {'Trainium2 (заявлено >1 млн, 20.04.2026)': rng.uniform(1_000_000, 1_200_000, n),   # [V S25] нижняя граница факт, верх — допущение
             'Colossus 1 (H100/H200/GB200)': np.full(n, 220_000.0),                               # [V S27]
             'TPU Google (ввод 2026, до 1 млн по сделке)': rng.uniform(200_000, 600_000, n),        # [ASSUMPTION] доля введённого к середине 2026
             'Azure / CoreWeave GPU': rng.uniform(0, 150_000, n),                                   # [ASSUMPTION]
             'доля Colossus 2 (GB200/GB300)': rng.uniform(0, 110_000, n)}                          # [ASSUMPTION] Epoch: Anthropic среди пользователей
    total = sum(parts.values())
    return {'chips': pct(total), 'parts': {k: pct(v) for k, v in parts.items()}}

# ------------------------------------------------------------------ контрольные точки
def control_points():
    cp = {}
    # Colossus 1: 150k H100 + 50k H200 + 30k GB200 (каталог Epoch)  [FACT S37]; анонс: >220 тыс. GPU, ~300 МВт  [FACT S27]
    n_h, n_gb = 200_000, 30_000
    h100e = n_h * 1.0 + n_gb * 2.5265; it_mw = (n_h * W_H + n_gb * W_B) / 1e6
    cp['Colossus 1'] = {'chips': n_h + n_gb, 'h100e_calc': h100e, 'h100e_epoch': 275_796, 'h100e_dev_%': 100 * (h100e / 275_796 - 1),
                        'it_mw_calc': it_mw, 'it_mw_epoch': 340, 'it_mw_dev_%': 100 * (it_mw / 340 - 1), 'announced_mw': '>300 (Anthropic, S27)',
                        'facility_mw_epoch': 425, 'kw_per_gpu_it_calc': it_mw * 1e3 / (n_h + n_gb),
                        'ok_15pct': abs(h100e / 275_796 - 1) < 0.15 and abs(it_mw / 340 - 1) < 0.15}
    # Абилин: 421 МВт IT (4 здания) -> GB200 -> H100e; Epoch: ~509 тыс. H100e  [FACT S37]; «>450 тыс. GB200 на ~1,2 ГВт» — план полной застройки (СМИ)
    it_mw = 421.0; gb200 = it_mw * 1e6 / W_B; h100e = gb200 * 2.5265
    full_it = 843.0; full_gb200 = full_it * 1e6 / W_B
    cp['Stargate Abilene'] = {'it_mw': it_mw, 'gb200_calc': gb200, 'h100e_calc': h100e, 'h100e_epoch': 509_348, 'h100e_dev_%': 100 * (h100e / 509_348 - 1),
                              'full_build_it_mw_epoch_2026-11': full_it, 'full_build_facility_mw_epoch': 1180, 'full_build_gb200_calc': full_gb200,
                              'full_build_h100e_epoch': 1_018_696, 'media_claim_gb200': 450_000, 'media_claim_it_mw_at_2090W': 450_000 * W_B / 1e6,
                              'media_vs_epoch_dev_%': 100 * (450_000 * W_B / 1e6 / full_it - 1),
                              'ok_15pct': abs(h100e / 509_348 - 1) < 0.15 and abs(450_000 * W_B / 1e6 / full_it - 1) < 0.15}
    return cp

def main(verbose=True):
    rng = np.random.default_rng(SEED)
    R = {'meta': {'date': DATE_TAG, 'seed': SEED, 'n_mc': N_MC},
         'coefficients': COEF.to_dict(orient='records'),
         'openai_end2025': {'formula_05_3': chips_openai_2025_formula(N_MC, rng)},   # ключ formula_05_3 — историческое имя формулы «IT-мощность ÷ средняя мощность чипа»
         'anthropic_end2025': chips_anthropic_2025(N_MC, rng),
         'anthropic_mid2026_by_facts': chips_anthropic_mid2026(N_MC, rng),
         'control_points': control_points()}
    oa = reproduce_openai(N_MC, rng)[2025]
    R['openai_end2025']['epoch_model_reproduced'] = {'chips': pct(oa['chips']), 'note': 'включает A100 (~10 % штук); лаг и overhead по приорам Epoch',
        'blackwell_share_chips': pct((oa['counts']['B200'] + oa['counts']['B300']) / oa['chips']),
        'hopper_share_chips': pct(oa['counts']['H100/H200'] / oa['chips']), 'a100_share_chips': pct(oa['counts']['A100'] / oa['chips'])}
    (OUT / 'data').mkdir(parents=True, exist_ok=True); (OUT / 'results').mkdir(parents=True, exist_ok=True)
    COEF.to_csv(OUT / 'data' / 'coefficients.csv', index=False)
    (OUT / 'results' / f'chips_{DATE_TAG}.json').write_text(json.dumps(R, ensure_ascii=False, indent=2, default=float), encoding='utf-8')
    if verbose:
        f = R['openai_end2025']['formula_05_3']['chips']; e = R['openai_end2025']['epoch_model_reproduced']['chips']
        print(f"OpenAI конец 2025, физ. ускорители: формула P_IT/⟨W⟩ → {f['p05']/1e6:.2f} / {f['p50']/1e6:.2f} / {f['p95']/1e6:.2f} млн ; "
              f"модель Epoch (с A100) → {e['p05']/1e6:.2f} / {e['p50']/1e6:.2f} / {e['p95']/1e6:.2f} млн")
        a = R['anthropic_end2025']['chips']; m = R['anthropic_mid2026_by_facts']['chips']
        print(f"Anthropic конец 2025: {a['p05']/1e6:.2f} / {a['p50']/1e6:.2f} / {a['p95']/1e6:.2f} млн ;  середина 2026 по фактам: {m['p05']/1e6:.2f} / {m['p50']/1e6:.2f} / {m['p95']/1e6:.2f} млн")
        for k, v in R['control_points'].items():
            print(f"Контрольная точка {k}: H100e расчёт/Epoch = {v['h100e_calc']/1e3:.0f}k / {v['h100e_epoch']/1e3:.0f}k ({v['h100e_dev_%']:+.1f} %) ; ±15 %: {'OK' if v['ok_15pct'] else 'FAIL'}")
    return R

if __name__ == '__main__':
    R_CHIPS = main()
