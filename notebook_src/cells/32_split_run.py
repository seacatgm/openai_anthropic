%run -i gpu_fleet_review_out/calc_split.py
md(open(OUT / 'results' / f'split_{DATE_TAG}.md', encoding='utf-8').read())

# график: stacked-бары сплита 2024–2026 (для 2026 — диапазон)
S = R_SPLIT['summary']
fig, ax = plt.subplots(figsize=(9, 3.6))
items = [('OpenAI 2024', S['openai_2024']['rd_share'], S['openai_2024']['rd_share'], 'V'),
         ('OpenAI 2025', S['openai_2025']['rd_share'], S['openai_2025']['rd_share'], 'V'),
         ('OpenAI 2026 (сцен.)', *S['openai_2026_rd_share_range'], 'E'),
         ('Anthropic 2025', S['anthropic_2025']['rd_share'], S['anthropic_2025']['rd_share'], 'V/E'),
         ('Anthropic 2026 H1 (сцен.)', *S['anthropic_h1_2026_rd_share_range'], 'E')]
for i, (name, lo, hi, st) in enumerate(items):
    col = COL['OpenAI'] if name.startswith('OpenAI') else COL['Anthropic']
    ax.barh(i, lo, color=col, alpha=0.85, height=0.6)
    if hi > lo: ax.barh(i, hi - lo, left=lo, color=col, alpha=0.35, hatch='//', edgecolor=col, height=0.6)
    ax.barh(i, 1 - hi, left=hi, color='#8f8e88', height=0.6)
    ax.text(0.01, i, f'R&D {100*lo:.0f}' + (f'–{100*hi:.0f}' if hi > lo else '') + f' %  [{st}]', va='center', fontsize=9, color='white' if lo > 0.15 else '#222')
    ax.text(0.99, i, f'инференс {100*(1-hi):.0f}' + (f'–{100*(1-lo):.0f}' if hi > lo else '') + ' %', va='center', ha='right', fontsize=9, color='#222')
ax.set_yticks(range(len(items))); ax.set_yticklabels([x[0] for x in items]); ax.invert_yaxis(); ax.set_xlim(0, 1); ax.set_xticks([0, .25, .5, .75, 1]); ax.set_xticklabels(['0', '25 %', '50 %', '75 %', '100 %'])
ax.set_title('Сплит R&D-compute / инференс в деньгах (облачные расходы): факт 2024–2025, сценарные диапазоны 2026', fontsize=10); ax.grid(False)
plt.tight_layout(); plt.savefig(OUT / 'results' / f'split_{DATE_TAG}.png', dpi=130); plt.show()
