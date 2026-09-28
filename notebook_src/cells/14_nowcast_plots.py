# ---------------------------------------------------------------- Блок 2, графики: конец 2025 (Epoch) и nowcast с интервалами
COL = {'OpenAI': '#2470cc', 'Anthropic': '#c9491a'}   # категориальные цвета (слоты 1 и 2 палитры)
fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), gridspec_kw={'width_ratios': [1.1, 1]})
ax = axes[0]
labels, x = [], 0
for lab in ('OpenAI', 'Anthropic'):
    e = R_NOWCAST['reproduction'][lab]['epoch']; n = R_NOWCAST[lab.lower()]['h100e']
    for tag, (lo, mid, hi), hatch in (('конец 2025\n(Epoch)', (e['p05'], e['p50'], e['p95']), None),
                                      (f'{DATE_TAG}\n(nowcast)', (n['p05'], n['p50'], n['p95']), '//')):
        ax.bar(x, mid / 1e6, width=0.7, color=COL[lab], alpha=0.85 if hatch is None else 0.45, hatch=hatch, edgecolor=COL[lab], linewidth=1.2)
        ax.errorbar(x, mid / 1e6, yerr=[[(mid - lo) / 1e6], [(hi - mid) / 1e6]], fmt='none', ecolor='#333', capsize=5, lw=1.4)
        ax.text(x, hi / 1e6 + 0.12, ru(mid / 1e6, 2), ha='center', fontsize=9, color='#222')
        labels.append(f'{lab}\n{tag}'); x += 1
    x += 0.5
ax.set_xticks([0, 1, 2.5, 3.5]); ax.set_xticklabels(labels, fontsize=8.5)
ax.set_ylabel('млн H100e'); ax.set_title('Парк в H100e: конец 2025 (Epoch, 90 % ДИ) и nowcast (наша модель, 90 % ДИ) — всё [E]', fontsize=10)
ax = axes[1]
for lab in ('OpenAI', 'Anthropic'):
    s = R_NOWCAST['_samples'][f'{lab.lower()}_h100e'] / 1e6
    ax.hist(s, bins=80, range=(0, 12), density=True, color=COL[lab], alpha=0.55, label=f'{lab} nowcast')
    s0 = R_NOWCAST['_samples'][f'{lab.lower()}_rep_h100e'] / 1e6
    ax.hist(s0, bins=80, range=(0, 12), density=True, histtype='step', color=COL[lab], lw=1.6, label=f'{lab} конец 2025 (воспроизведение Epoch)')
ax.set_xlabel('млн H100e'); ax.set_ylabel('плотность'); ax.legend(fontsize=8); ax.set_title(f'Распределения: конец 2025 vs {DATE_TAG}', fontsize=10)
plt.tight_layout(); plt.savefig(OUT / 'results' / f'nowcast_{DATE_TAG}.png', dpi=130); plt.show()

# таблица чувствительности
rows = []
for lab in ('openai', 'anthropic'):
    S = R_NOWCAST['sensitivity'][lab]; base = R_NOWCAST[lab]['h100e']['p50']
    rows.append({'lab': lab, 'case': 'базовый', 'h100e_p50_млн': base / 1e6, 'ГВт IT p50': R_NOWCAST[lab]['gw_it_mw']['p50'] / 1e3})
    rows.append({'lab': lab, 'case': 'раскрытые ГВт — мощность объекта (PUE 1,3)', 'h100e_p50_млн': S['disclosed_is_facility_power_PUE1.3']['h100e']['p50'] / 1e6, 'ГВт IT p50': S['disclosed_is_facility_power_PUE1.3']['gw_it_mw']['p50'] / 1e3})
    rows.append({'lab': lab, 'case': f"g = {S['g_low']['g']} (нижняя граница)", 'h100e_p50_млн': S['g_low']['h100e']['p50'] / 1e6, 'ГВт IT p50': S['g_low']['gw_it_mw']['p50'] / 1e3})
    rows.append({'lab': lab, 'case': f"g = {S['g_high']['g']} (верхняя граница)", 'h100e_p50_млн': S['g_high']['h100e']['p50'] / 1e6, 'ГВт IT p50': S['g_high']['gw_it_mw']['p50'] / 1e3})
    k = [k for k in S if k.startswith('eta_new')][0]
    rows.append({'lab': lab, 'case': f'η новых вводов = {k.split("_")[-1]} H100e/МВт', 'h100e_p50_млн': base / 1e6, 'ГВт IT p50': S[k]['gw_it_mw']['p50'] / 1e3})
display(pd.DataFrame(rows).round(2))
