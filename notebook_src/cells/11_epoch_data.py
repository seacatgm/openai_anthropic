# ---------------------------------------------------------------- Блок 2.1 данные Epoch: скачивание, SHA-256, сверка медиан
# Встроенная копия year_end (скачана 27.09.2026, файл «Generated on 2026-09-09 13:35»)  [FACT S03]
EPOCH_YEAR_END_EMBEDDED = """Name,Lab,Year,Date,h100e_p5,h100e_med,h100e_p95,Notes
OpenAI end-2023,OpenAI,2023,2023-12-31,70131.45706056355,102534.71096180622,136201.42880654646,Generated on 2026-09-09 13:35
Google DeepMind end-2024,Google DeepMind,2024,2024-12-31,214143.6362592907,420334.47667409095,775030.4133149517,Generated on 2026-09-09 13:35
Meta Superintelligence Labs end-2024,Meta Superintelligence Labs,2024,2024-12-31,123667.98345628983,247706.7361251794,480076.0743148279,Generated on 2026-09-09 13:35
OpenAI end-2024,OpenAI,2024,2024-12-31,276938.3521681225,386218.7101238488,486056.6393925586,Generated on 2026-09-09 13:35
Anthropic end-2024,Anthropic,2024,2024-12-31,145189.55328493097,208559.98299904328,298183.1495345837,Generated on 2026-09-09 13:35
SpaceXAI end-2024,SpaceXAI,2024,2024-12-31,171066.07146658262,203366.31755523162,237382.2215257479,Generated on 2026-09-09 13:35
Google DeepMind end-2025,Google DeepMind,2025,2025-12-31,1008220.4725750112,1583429.9538668268,2548755.702786412,Generated on 2026-09-09 13:35
Meta Superintelligence Labs end-2025,Meta Superintelligence Labs,2025,2025-12-31,606301.475799089,996228.0602346028,1637712.6527012342,Generated on 2026-09-09 13:35
OpenAI end-2025,OpenAI,2025,2025-12-31,1251477.0828997404,1743439.8493869188,2185142.3455992746,Generated on 2026-09-09 13:35
Anthropic end-2025,Anthropic,2025,2025-12-31,842241.6260268212,1189573.8857074357,1716534.7037994058,Generated on 2026-09-09 13:35
SpaceXAI end-2025,SpaceXAI,2025,2025-12-31,587268.4845382306,634792.6058833487,786632.5928349933,Generated on 2026-09-09 13:35
"""
# Встроенная копия intermediates — только строки OpenAI/Anthropic end-2025 (остальные лаборатории не нужны)  [FACT S03/S04]
EPOCH_INTERMEDIATES_EMBEDDED = """Name,Lab,Year,Step,Variable,Label,Kind,Units,Expression,value_p5,value_med,value_p95
OpenAI end-2025 · Disclosed end-2025 power,OpenAI,2025,1,disclosed_power,Disclosed end-2025 power,constant,MW,,1900.0,1900.0,1900.0
OpenAI end-2025 · Rounding adjustment (±),OpenAI,2025,2,rounding_jitter,Rounding adjustment (±),input,MW,rounded to 0.1 GW,-34.003894433445346,0.12985082437181106,34.306327323344114
OpenAI end-2025 · Power-definition factor (IT vs gross),OpenAI,2025,3,definition_factor,Power-definition factor (IT vs gross),input,ratio,IT (≈1) or gross ÷ PUE,0.727646055768521,0.9934338097402341,1.0495846451171673
OpenAI end-2025 · Figure-accuracy factor,OpenAI,2025,4,accuracy_factor,Figure-accuracy factor,input,ratio,,0.8986811665001545,1.0399247963364624,1.202058333176867
OpenAI end-2025 · Modelled end-2025 IT power,OpenAI,2025,5,total_power,Modelled end-2025 IT power,derived,MW,(Disclosed + Rounding) × definition × accuracy,1440.5682921877508,1949.8416202744538,2291.1816116511227
OpenAI end-2025 · Deployment lag behind Nvidia's sales mix,OpenAI,2025,6,lag_quarters,Deployment lag,input,quarters,,0.4912992143315901,0.9982480963753237,1.9760314743056575
OpenAI end-2025 · Server-to-IT power overhead,OpenAI,2025,7,it_overhead,Server-to-IT power overhead,input,ratio,,1.0,1.1376434290106785,1.3525402582250488
Anthropic end-2025 · Total IT power,Anthropic,2025,1,power_mw,Total IT power,input,MW,Leaked lab power (GW) × 1000,991.9050928270094,1377.2862752959536,1889.423316266424
Anthropic end-2025 · Trainium2 share of IT power,Anthropic,2025,2,trainium_share,Trainium2 share of IT power,input,share,,0.34827021435689287,0.522866215538526,0.7023341286481866
Anthropic end-2025 · Trainium2 fleet efficiency,Anthropic,2025,3,trainium2_per_mw,Trainium2 fleet efficiency,constant,H100e/MW,,753.7688442211055,753.7688442211055,753.7688442211055
Anthropic end-2025 · Trainium2 efficiency — uncertainty adjustment,Anthropic,2025,4,trainium_eff,Trainium2 efficiency adj.,input,ratio,,0.8540669834412655,1.0149197542925763,1.2067051833153541
Anthropic end-2025 · Nvidia + TPU fleet efficiency,Anthropic,2025,5,nontrainium_per_mw,Nvidia + TPU fleet efficiency,constant,H100e/MW,,977.0469244854683,977.0469244854683,977.0469244854683
Anthropic end-2025 · Nvidia + TPU efficiency — uncertainty adjustment,Anthropic,2025,6,nontrainium_eff,Nvidia + TPU efficiency adj.,input,ratio,,0.8011591733013402,0.9956539738551973,1.2594886275283812
Anthropic end-2025 · Blended fleet efficiency,Anthropic,2025,7,blended_per_mw,Blended fleet efficiency,derived,H100e/MW,share × 754 × adj + (1 − share) × 977 × adj,746.9439838245389,865.319339080004,1019.0792705146505
"""
EPOCH_FILES = {
    'ai_chip_users_year_end_by_lab.csv':      ('https://epoch.ai/data/ai_chip_users_year_end_by_lab.csv',
                                               'a42673451e91a9896ed285ec74f66442473c07f9fedc89695a75ef3e4701169c', EPOCH_YEAR_END_EMBEDDED),
    'ai_chip_users_intermediates_by_lab.csv': ('https://epoch.ai/data/ai_chip_users_intermediates_by_lab.csv',
                                               'c82052bebfae4ebfb344da71827af02366c49b22cbaa9f32b0c4a3b0f7345be5', EPOCH_INTERMEDIATES_EMBEDDED),
}
EPOCH_REPO = {'url': 'https://github.com/epoch-research/ai-compute-users',
              'commit': '15c608704dad74c7b7a956c77bbb4e8b602f6670', 'commit_date': '2026-09-09',
              'note': 'клонирован --depth 1 27.09.2026; ноутбуки notebooks/openai_power_model.ipynb, notebooks/anthropic_power_2025.ipynb; параметры lab_model_params.csv'}

epoch_log = []
for fname, (url, sha_ref, embedded) in EPOCH_FILES.items():
    dest = OUT / 'data' / 'epoch' / f'{Path(fname).stem}_{ACCESSED}.csv'
    src = 'embedded'
    if ONLINE:
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                dest.write_bytes(r.read()); src = 'download'
        except Exception as e:
            print(f'  ! {fname}: скачать не удалось ({type(e).__name__}); используем встроенную копию')
    if src == 'embedded':
        dest.write_text(embedded, encoding='utf-8')
    sha = sha256_file(dest)
    epoch_log.append({'file': dest.name, 'source': src, 'sha256': sha, 'sha256_ref_2026-09-27': sha_ref,
                      'unchanged_since_2026-09-27': (sha == sha_ref) if src == 'download' else None})
epoch_log_df = pd.DataFrame(epoch_log)
write_text(epoch_log_df.to_csv(index=False) + f"\n# repo,{EPOCH_REPO['url']},{EPOCH_REPO['commit']},{EPOCH_REPO['commit_date']}\n",
           OUT / 'data' / 'epoch' / 'SHA256SUMS.csv')
display(epoch_log_df)

# --- сверка медиан и ДИ с ранее зафиксированными значениями ------------------------------------------------------------
ye = pd.read_csv(OUT / 'data' / 'epoch' / f'ai_chip_users_year_end_by_lab_{ACCESSED}.csv')
ye = ye[ye['Lab'].isin(['OpenAI', 'Anthropic'])].sort_values(['Lab', 'Year'])
EPOCH_YE = {(r.Lab, int(r.Year)): (float(r.h100e_p5), float(r.h100e_med), float(r.h100e_p95)) for r in ye.itertuples()}
REF_02_03 = {('OpenAI', 2023): 103_000, ('OpenAI', 2024): 386_000, ('OpenAI', 2025): 1_743_000,   # [FACT S02]
             ('Anthropic', 2024): 209_000, ('Anthropic', 2025): 1_190_000}                          # [FACT S02]
rows = []
for (lab, yr), (p5, med, p95) in EPOCH_YE.items():
    ref = REF_02_03.get((lab, yr))
    dev = (med / ref - 1) if ref else float('nan')
    rows.append({'lab': lab, 'year': yr, 'p05': round(p5), 'median': round(med), 'p95': round(p95),
                 'ref_recorded': ref, 'deviation_%': round(100 * dev, 2) if ref else None, 'ok(<1%)': (abs(dev) < 0.01) if ref else None})
medians_check = pd.DataFrame(rows)
display(medians_check)
assert medians_check['ok(<1%)'].dropna().all(), 'Расхождение медиан Epoch с ранее зафиксированными больше 1 % — остановиться и записать'
print('Медианы Epoch совпадают с ранее зафиксированными в пределах 1 %.')
