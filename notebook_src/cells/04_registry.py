# ---------------------------------------------------------------- Блок 1: реестр источников
SOURCES_ORIGINAL_CSV = r"""{{SOURCES_CSV}}"""
SRC_ORIG = pd.read_csv(io.StringIO(SOURCES_ORIGINAL_CSV), dtype=str).fillna('')

# Результаты проверки первоисточников 27.09.2026 и свежие публикации. Только URL, которые реально открывались.
UPDATES = {
    # --- K -> V/V2: первоисточники найдены и открыты
    'S39': dict(date='2025-07-20', url='https://x.com/sama/status/1947057625780396512', status='V',
                note='текст поста подтверждён дословно через официальный oEmbed X (сам x.com отдаёт 402): «we will cross well over 1 million GPUs brought online by the end of this year… how to 100x that»'),
    'S40': dict(date='2025-10-06', url='https://ir.amd.com/news-events/press-releases/detail/1260/amd-and-openai-announce-strategic-partnership-to-deploy-6-gigawatts-of-amd-gpus', status='V',
                note='дословно: «6 gigawatts of AMD GPUs»; «Initial 1 gigawatt… MI450… starting in 2H 2026»; «warrant for up to 160 million shares»; копия на amd.com/newsroom открыта'),
    'S41': dict(date='2025-10-13', url='https://www.broadcom.com/company/news/product-releases/63631', status='V2',
                note='заголовок, дата и «10 gigawatts» подтверждены на broadcom.com и в RSS OpenAI (pubDate 13.10.2025); формулировка «2H 2026 – конец 2029» на первоисточнике не открылась (JS-рендер / 403), подтверждена только сниппетами investors.broadcom.com'),
    'S42': dict(date='2025-06-10', title='Exclusive: OpenAI taps Google in unprecedented cloud deal despite AI rivalry, sources say (Reuters)',
                url='https://www.cnbc.com/2025/06/10/openai-taps-google-in-unprecedented-cloud-deal-despite-ai-rivalry-sources-say.html', status='V2',
                note='reuters.com не открывается (401); текст Reuters подтверждён по синдикации CNBC (10.06.2025) и Investing.com; заголовок в реестре исправлен'),
    'S43': dict(date='2025-10-23', title='Expanding our use of Google Cloud TPUs and Services', url='https://www.anthropic.com/news/expanding-our-use-of-google-cloud-tpus-and-services', status='V',
                note='дословно: «up to one million TPUs»; «well over a gigawatt of capacity online in 2026»; «tens of billions of dollars»'),
    'S44': dict(date='2025-11-18', title='Microsoft, NVIDIA, and Anthropic announce strategic partnerships', url='https://www.anthropic.com/news/microsoft-nvidia-anthropic-announce-strategic-partnerships', status='V',
                note='дословно: «$30 billion of Azure compute capacity»; «up to one gigawatt… Grace Blackwell and Vera Rubin»; «NVIDIA and Microsoft… up to $10 billion and up to $5 billion»'),
    'S45': dict(date='2025-11-12', title='Anthropic invests $50 billion in American AI infrastructure', url='https://www.anthropic.com/news/anthropic-invests-50-billion-in-american-ai-infrastructure', status='V',
                note='дословно: «$50 billion investment… data centers with Fluidstack in Texas and New York»; «sites coming online throughout 2026»; дата 12.11.2025. TechTimes 05.09.2026: Fluidstack закрыл раунд $1,5 млрд при оценке $18 млрд, площадки Anthropic «coming online throughout 2026»'),
    'S47': dict(date='2025-10-29', title="AWS activates Project Rainier: One of the world's largest AI compute clusters comes online", url='https://www.aboutamazon.com/news/aws/aws-project-rainier-ai-trainium-chips-compute-cluster', status='V',
                note='дословно: «nearly half a million Trainium2 chips»; «more than 1 million Trainium2 chips… by the end of the year»; метаданные страницы: published 2025-06-24 (старая статья по тому же URL), modified 2025-10-29'),
    'S18': dict(url='https://investor.nvidia.com/news/press-release-details/2025/OpenAI-and-NVIDIA-Announce-Strategic-Partnership-to-Deploy-10-Gigawatts-of-NVIDIA-Systems/default.aspx', status='V',
                note='первоисточник (investor.nvidia.com) открыт: «at least 10 gigawatts… millions of GPUs»; «up to $100 billion… as each gigawatt is deployed»; «first gigawatt… second half of 2026 on… Vera Rubin»; это письмо о намерениях (LOI); nvidianews и openai.com — 403'),
    'S01': dict(date='2026-01-18', status='V2',
                note='дата 18.01.2026 (воскресенье) подтверждена по RSS OpenAI; сама страница отдаёт 403; фраза «0.2 GW in 2023, 0.6 GW in 2024, and ~1.9 GW in 2025» — по цитатам Sherwood News (20.01.2026) и CNBC (19.01.2026)'),
{{UPDATES_EXTRA}}
}
NEW_ROWS = [
{{NEW_ROWS}}
]

SRC = SRC_ORIG.copy()
changes = []
for sid, upd in UPDATES.items():
    i = SRC.index[SRC['id'] == sid][0]
    old = SRC.loc[i, 'status']
    for k, v in upd.items():
        if k == 'note' and SRC.loc[i, 'note']:
            SRC.loc[i, 'note'] = SRC.loc[i, 'note'] + ' | ' + v
        else:
            SRC.loc[i, k] = v
    changes.append({'id': sid, 'status': f"{old} → {SRC.loc[i, 'status']}", 'url_added': bool(upd.get('url')) and not SRC_ORIG.loc[i, 'url'], 'what': (upd.get('note') or '')[:110]})
for r in NEW_ROWS:
    SRC = pd.concat([SRC, pd.DataFrame([r])], ignore_index=True); changes.append({'id': r['id'], 'status': f"new → {r['status']}", 'url_added': bool(r.get('url')), 'what': r['title'][:110]})
SRC['accessed'] = ACCESSED
SRC = SRC[['id', 'date', 'publisher', 'title', 'url', 'supports', 'status', 'note', 'accessed']].fillna('')
SRC.to_csv(OUT / 'data' / f'sources_{ACCESSED}.csv', index=False)

def src_status(sid):  return SRC.loc[SRC['id'] == sid, 'status'].iloc[0] if (SRC['id'] == sid).any() else '?'
def src_url(sid):     return SRC.loc[SRC['id'] == sid, 'url'].iloc[0] if (SRC['id'] == sid).any() else ''

assert not (SRC['status'] == 'K').any(), 'в реестре остались записи K'
no_url = SRC[(SRC['status'].str.startswith('V')) & (SRC['url'] == '')]
print(f'Реестр: {len(SRC)} записей; изменено/добавлено {len(changes)}; статусы: ' + ', '.join(f'{k}={v}' for k, v in SRC['status'].value_counts().sort_index().items()))
print('Записи V/V2 без URL:', ', '.join(no_url['id']) or 'нет')
display(pd.DataFrame(changes))
