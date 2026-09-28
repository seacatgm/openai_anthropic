# Сколько GPU у OpenAI и Anthropic и как они делят их между обучением и инференсом

*Версия 2 (исправленный исходный документ). Дата слайда: 27.09.2026. Источники проверены 2026-09-27 (реестр — Приложение E, `data/sources_2026-09-27.csv`). Статусы: [V] первоисточник, [V2] надёжная вторичная пресса, [E] оценка или модель, [N] не проверено. Расчёты воспроизводимы: `calc_nowcast.py`, `calc_chips.py`, `calc_split.py` (seed 20260927, 200 000 прогонов).*

## Ответ в трёх строках

1. **Штуки не публикуются — считаем в ГВт и H100e.** Конец 2025: OpenAI ≈ 1,9 ГВт [S01][V2] ≈ 1,74 млн H100e (90 % ДИ 1,25 млн–2,19 млн) [S02][E]; Anthropic ≈ 1,4 ГВт (оценка конкурента) [S11][V2] ≈ 1,19 млн H100e (0,84 млн–1,72 млн) [S02][E]. Физических ускорителей — ≈ 1,1 млн у OpenAI и ≈ 1,3 млн у Anthropic [E].
2. **На 27.09.2026 (nowcast, наша модель) [E]:** OpenAI ≈ 4,27 млн H100e (90 % ДИ 3,00 млн–6,08 млн) ≈ 4,6 ГВт IT; Anthropic ≈ 3,03 млн (1,95 млн–4,70 млн) ≈ 3,3 ГВт IT; приоры роста 2,5–4,5× и 2,5–5×/год.
3. **Сплит есть только в деньгах.** 2025: OpenAI 49/51 R&D/инференс [S04][V]; Anthropic 60/40 [S06][E]. 2026 — сценарии [E]: у OpenAI по плановым цифрам доля R&D растёт до 59–69 % [S15][V], [S13][V2] (план, вероятно, недооценивает инференс: в 2025 он вырос ×4 [S14][V2]); у Anthropic доля R&D падает до 34–54 % [S29][V2].

## 1. Как считать и почему не в штуках

Ни одна из компаний не публикует число чипов и не раскрывает сплит; есть гигаватты, утечки инвесторских документов и модели Epoch [E]. Единственная твёрдая цифра — мощность OpenAI: 0,2 / 0,6 / ~1,9 ГВт на конец 2023 / 2024 / 2025 (блог CFO, 18.01.2026) [S01][V2]; 1,9 ГВт — ретроспективная цифра (в сентябре 2025 Альтман ожидал «более 2 ГВт», The Information — 2,4 ГВт) [S32][V2]. Epoch с вероятностью 90 % считает её IT‑мощностью; если это мощность объекта, оценка падает до ~1,0–1,1 млн H100e [S04][V]. Единица сравнения — H100‑эквивалент (пиковые плотные 8‑битные FLOP/s относительно H100) [S10][V]: GB200 = 2,53 H100e, Trainium2 = 0,66, TPUv7 ≈ 2,3 [S04][V]. Один гигаватт IT — это ≈ 690 тыс. Hopper, ≈ 480 тыс. GB200 или ≈ 1,15 млн Trainium2 [E, Приложение C], поэтому «штуки» между парками несопоставимы. Оценки Epoch — используемый (в основном арендуемый) compute без учёта утилизации [S04][V]; гигаватты пресс‑релизов пересекаются и относятся к 2026–2031 годам, суммировать их как парк нельзя [S19][V].

## 2. Парк на конец 2025

| Параметр | OpenAI | Anthropic | Статус |
|---|---|---|---|
| Мощность | ~1,9 ГВт, раскрыто [S01][V2] | ~1,4 ГВт, оценка OpenAI; IT или объект — неизвестно [S11][V2] | [V2] |
| H100e, Epoch (медиана; 90 % ДИ) | 1,743 млн (1,251 млн–2,185 млн) [S02][V] | 1,190 млн (0,842 млн–1,717 млн) [S02][V] | [E] |
| Место среди лабораторий | 1‑е; интервал перекрывается с Google DeepMind (1,58 млн) [S02][V] | 3‑е [S02][V] | [E] |
| Физ. ускорители | ≈ 1,14 млн (90 % ДИ 0,84 млн–1,34 млн); Hopper ≈ 60 % штук, Blackwell ≈ 62 % мощности [S04][V] | ≈ 1,25 млн (0,90 млн–1,76 млн): ~0,8 млн Trainium2 + NVIDIA/TPU [S04][V] | [E] |
| Состав парка | Hopper : Blackwell ≈ 1,48 : 1 по штукам [S04][V] | Trainium2 ≈ 52 % IT‑мощности (35–70 %) [S04][V]; заявлено «более 1 млн Trainium2» (04.2026) [S25][V] | [E]/[V] |
| Сторонний инференс | не учтён: Azure‑хостинг — до ~25 % парка [S04][V] | учтён: Bedrock/Vertex/Foundry ≈ 10 % compute [S04][V] | [E] |
| Облачные расходы на compute, 2025 | $16,3 млрд [S04][V] | $6,8 млрд [S06][V] | [V] |
| Доля мирового AI‑compute | ~10–15 % (мир ≈ 20 млн H100e) [S05][V] | — | [E] |

Асимметрия учёта: Anthropic платит за железо партнёрских API и учитывает выручку по валу — Epoch включает этот compute; OpenAI до апреля 2026 получала 20 % выручки от Microsoft и за Azure‑хостинг не платила — Epoch его исключает [S04][V], [S35][V2]. Сравнение 1,74 против 1,19 млн H100e смещено против OpenAI на 10–25 % [S04][E]. С 27.04.2026 Microsoft не платит OpenAI долю выручки, лицензия неэксклюзивна, продажи возможны в любом облаке [S21][V].

## 3. Nowcast на 27.09.2026

Модель [E]: `N(t) = N_2025 · g^Δt`, `Δt` = 0,74 г.; `N_2025` — распределение Epoch [S02][V]; `g` — лог‑нормальный приор 2,5–4,5×/год для OpenAI (Epoch: compute «более чем утроится» за 2026 [S04][V]; бюджет $50 млрд ≈ 3× [S13][V2]) и 2,5–5,0× для Anthropic (вводы TPU [S43][V], Trainium [S25][V], Colossus 1 [S27][V], Azure [S44][V]; прогноз OpenAI 3–4 ГВт [S11][V2]); перевод в ГВт — по 945 и 950 H100e/МВт для новых вводов (Приложение C) [E].

| | OpenAI | Anthropic |
|---|---|---|
| H100e: медиана (50 % / 90 % интервал) [E] | 4,27 млн (3,69 млн–4,93 млн / 3,00 млн–6,08 млн) | 3,03 млн (2,53 млн–3,63 млн / 1,95 млн–4,70 млн) |
| ГВт IT: медиана (90 %) [E] | 4,6 ГВт (3,3 ГВт–6,6 ГВт) | 3,3 ГВт (2,1 ГВт–5,1 ГВт) |
| Множитель к концу 2025 [E] | ×2,45 | ×2,55 |
| Проверка «по вводам», каталог ЦОД Epoch [S37][E] | ≥ 2,00 млн — нижняя граница: Абилин 509 тыс. H100e при 421 МВт IT; Azure, Oracle вне Абилина, CoreWeave не итемизированы; расхождение с медианой −53 % | 2,53 млн (2,22 млн–2,84 млн): Rainier +214 тыс., Colossus 1 +276 тыс. H100e, TPU/Azure/Colossus 2 — диапазоны; расхождение −16 % |
| Чувствительность [E] | 1,9 ГВт как мощность объекта (PUE 1,3): 3,28 млн; g = 2,5 / 4,5: 3,43 млн / 5,30 млн | 1,4 ГВт как мощность объекта: 2,33 млн; g = 2,5 / 5,0: 2,34 млн / 3,92 млн |

Исходный документ давал «3–5 ГВт и 2–3 млн ускорителей» без модели (L46); nowcast того же порядка в ГВт, но выше в H100e: новый ввод идёт в основном на Blackwell (2,53 H100e на чип) [E]. В штуках у Anthropic к середине 2026 «по фактам» ≈ 1,8 млн ускорителей (1,6 млн–2,1 млн): >1 млн Trainium2 [S25][V], >220 тыс. GPU Colossus 1 [S27][V], TPU и Azure — диапазоны [E].

## 4. Сплит обучение / инференс 2024–2026 (в деньгах, облачный базис)

| Компания | 2024 | 2025 | 2026 (сценарии) [E] |
|---|---|---|---|
| OpenAI | 71/29: ~$5 млрд R&D / ~$2 млрд инференс [S07][V] | 49/51: ~$8 / $8,4 млрд из $16,3 млрд [S04][V], [S16][V2] | 59–69 % R&D: обучение $32 млрд [S15][V], инференс $14,1–22 млрд по сценариям A–D [S16][V2], [S13][V2] |
| Anthropic | не раскрыт; compute $2,5 млрд [S04][V] | 60/40: $4,1 / ~$2,7 млрд из $6,8 млрд [S06][E] | 34–54 % R&D (I полугодие; центр 42/58): compute 0,71 и 0,56 на $1 выручки при $4,8 / $10,9 млрд [S29][V2], маржа инференса 60–72 % [E] |

«Обучение» здесь — весь R&D‑compute; финальные прогоны — меньшая его часть [S08][V]. Винтажи прогнозов OpenAI на 2026 различаются ($14,1 млрд — до февраля [S16][V2]; $32 млрд — февраль [S15][V]; $50 млрд — май [S13][V2]), а инференс в 2025 вырос в 4 раза [S14][V2], поэтому план может быть занижен в пользу R&D [E]. Маржа инференса Anthropic не раскрыта; сценарии с R&D < $1 млрд/квартал (2025: $4,1 млрд/год [S06][V]) отброшены [E]. Другие базисы не смешиваем (Приложение D): WSJ «$13–25 млрд обучения 2025 в зависимости от учёта» [S31][V2]; аудированная отчётность 2025 — платежи Microsoft $10,59 млрд по R&D и $6,05 млрд по cost of revenue (≈ 64/36), отдельной строки инференс/обучение нет [S34][V]. Gartner (инференс $23,3 млрд > обучение $19 млрд в 2026) описывает рынок AI‑optimized IaaS в $42 млрд — меньше бюджета одной OpenAI — и на лаборатории не переносится [S30][V].

## 5. Что изменится к концу 2026

- **OpenAI:** 10 ГВт законтрактовано в США (04.2026) [S12][V2]; Абилин 421 МВт IT → ~843 МВт / ~1,02 млн H100e к ноябрю [S37][E]; первые ГВт MI450 [S40][V] и стоек Broadcom [S41][V2] — 2‑е полугодие 2026; письмо о намерениях с NVIDIA на 10 ГВт (Vera Rubin, первый ГВт — 2H 2026 [S18][V]) в договор не оформлено и заменено инвестицией $30 млрд [S17][V2] — в план вводов не входит; PORTS‑Pike: 4,25 ГВт IT твёрдо + опцион 3,75 ГВт IT (итого до 8 ГВт IT), ≥10 ГВт генерации — с 2028 [S24][V], [S62][V]; риск сроков — force majeure Oracle по Project Jupiter [S58][V].
- **Anthropic:** «почти 1 ГВт» Trainium2/3 [S25][V] и «значительно больше 1 ГВт» TPU [S43][V] к концу 2026; до 1 ГВт Azure [S44][V]; Colossus 1 (~300 МВт) с июня [S27][V]; CoreWeave — конец 2026 [S28][V]; прогноз OpenAI — 3–4 ГВт [S11][V2].
- **Обе:** доля инференса растёт (агенты, reasoning‑модели); аудированные строки cost of revenue и R&D появятся в публичных S‑1 (подачи объявлены 08.06 и 01.06.2026) [S22][V].

---

## Приложения

### A. Контракты и площадки OpenAI (статус на 2026-09-27)

| Партнёр / проект | Параметры | Дата | Статус |
|---|---|---|---|
| Microsoft Azure | обязательство $250 млрд Azure (реструктуризация 10.2025); поправка 27.04.2026: лицензия неэксклюзивна до 2032, продажи в любом облаке, Microsoft не платит долю выручки, OpenAI платит 20 % до 2030 с потолком [S21][V], [S23][V/V2] | 2025-10 / 2026-04-27 | действует |
| Stargate (Oracle, SoftBank, MGX) | 23.09.2025: пять новых площадок, «почти 7 ГВт», >$400 млрд [S19][V]; Абилин — единственный работающий кампус, расширение отклонено, UK — пауза, Норвегия — выход [S12][V2] | 2025-09-23 | Абилин работает |
| Oracle OCI | до 4,5 ГВт (07.2025); ~$300 млрд за 5 лет [S19][V], [S23][V/V2] | 2025-07 | стройка |
| NVIDIA | LOI ≥10 ГВт, первый ГВт — 2H 2026 на Vera Rubin; до $100 млрд поэтапно [S18][V]; LOI не оформлен, заменён инвестицией $30 млрд в раунде $110 млрд (27.02.2026) [S17][V2]; обязательств по поставке мощностей нет | 2025-09-22 / 2026-02-27 | инвестиция закрыта |
| AMD | 6 ГВт MI450, первый ГВт — 2H 2026; варрант до 160 млн акций [S40][V] | 2025-10-06 | развёртывание |
| Broadcom | 10 ГВт стоек с собственным ускорителем OpenAI, 2H 2026 – конец 2029 [S41][V2]; Sacra: чип Jalapeño [S16][V2] | 2025-10-13 | старт 2H 2026 |
| AWS | $38 млрд (11.2025) + $100 млрд за 8 лет; ~2 ГВт Trainium3/4 с 2027; Amazon инвестирует $50 млрд [S20][V] | 2026-02-27 | контракт |
| CoreWeave | ~$22,4 млрд контрактов до 2029 [S23][V/V2] | 2025 | работает |
| Google Cloud | облачная сделка, включая TPU [S42][V2] | 2025-06-10 | работает |
| Cerebras | 750 МВт инференс‑мощности до 2028, >$10 млрд; MRA и варрант — 12.2025, заём $1 млрд — 01.2026 [S23][V/V2] | 2025-12 | развёртывание |
| PORTS‑Pike (Огайо, SB Energy) | 20‑летняя аренда: 4,25 ГВт IT твёрдо + опцион 3,75 ГВт IT (итого до 8 ГВт IT), первая очередь ~800 МВт — 2028; NVIDIA — $1,5 млрд в SB Energy и кредитная поддержка первой фазы [S24][V], [S62][V]; потолок гарантий NVIDIA $105 млрд — по SEC‑отчётности [S63][V2]; ≥10 ГВт новой генерации [S62][V] | 2026-08-17 | аренда подписана |
| Firmus (Малайзия) | многолетний договор, две площадки, Vera Rubin; объём не раскрыт [S59][V2] | 2026-09-08 | контракт |
| Итог «secured» / планы | 10 ГВт в США законтрактовано, >3 ГВт за 90 дней, 2 ГВт — Amazon [S12][V2]; меморандум 08.04.2026: «low double‑digit» ГВт в 2027, 30 ГВт к 2030, ещё 14 ГВт идентифицировано [S11][V2]; compute до 2030: ~$600 млрд (02.2026) [S14][V2], ~$856 млрд (презентация партнёрам, 09.2026) [S50][V2] | 2026-04-30 | — |

### B. Контракты и площадки Anthropic (статус на 2026-09-27)

| Партнёр / проект | Параметры | Дата | Статус |
|---|---|---|---|
| AWS / Project Rainier | Rainier запущен 29.10.2025 (~500 тыс. Trainium2) [S47][V]; 20.04.2026: до 5 ГВт, >$100 млрд за 10 лет, >1 млн Trainium2, «почти 1 ГВт» Trainium2/3 к концу 2026; Amazon инвестирует $5 + до $20 млрд [S25][V] | 2025-10-29 / 2026-04-20 | работает, расширяется |
| Google Cloud, TPU | до 1 млн TPU, «значительно больше 1 ГВт» в 2026, «десятки миллиардов долларов» [S43][V] | 2025-10-23 | ввод в 2026 |
| Google + Broadcom | «несколько ГВт» TPU с 2027; ~3,5 ГВт по 8‑K Broadcom [S26][V] | 2026-04-06 | контракт |
| Microsoft Azure + NVIDIA | $30 млрд Azure, до 1 ГВт (Grace Blackwell, Vera Rubin); NVIDIA до $10 млрд, Microsoft до $5 млрд [S44][V] | 2025-11-18 | развёртывание |
| SpaceX / Colossus 1 | вся мощность Colossus 1: >220 тыс. GPU, ~300 МВт; $1,25 млрд/мес до 05.2029, выход за 90 дней (S‑1 SpaceX 20.05.2026) [S27][V]; Epoch: ≈ 276 тыс. H100e, плюс часть Colossus 2 [S37][E]; Colossus 1+2 ≈ 1,0 ГВт на 31.03.2026 [S04][V] | 2026-05-06 | работает |
| Fluidstack | $50 млрд в собственные ЦОД (Техас, Нью‑Йорк), ввод в течение 2026 [S45][V] | 2025-11-12 | стройка |
| CoreWeave | многолетний договор, ввод с конца 2026, объём не раскрыт [S28][V] | 2026-04-10 | развёртывание |
| Nscale (Monarch, Западная Вирджиния) | GPU‑сервисы до ~$44,6 млрд, Vera Rubin NVL72, ввод — конец 2027 (S‑1 Nscale 18.09.2026) [S52][V2] | 2026-08-25 | контракт |
| Финансирование стройки | ≈ $50 млрд долга: $34,5 млрд — >1 ГВт TPU Google (три транша, $30 млрд с поддержкой Broadcom); ~$15,2 млрд — пять ЦОД Fluidstack на 1,43 ГВт IT; финансирование — не ближайший ограничитель [S46][V] | 2026-08-12 | — |
| Сумма сделок / прогнозы | The Information: $517 млрд compute‑сделок за 11 месяцев [S36][V2], 14,8 ГВт новой ёмкости с 10.2025 [S51][V2]; прогноз OpenAI: 3–4 ГВт к концу 2026, 7–8 ГВт к концу 2027 [S11][V2] | 2026-09 | — |

### C. Коэффициенты пересчёта ГВт ↔ чипы ↔ H100e (база — Epoch [S04][V], [S10][V]; строки «наш расчёт» — [E])

| Коэффициент | IT‑Вт на чип | H100e на чип | чипов на 1 ГВт IT | H100e на 1 ГВт IT | База |
|---|---|---|---|---|---|
| A100 | 926 Вт | 0,32 | 1 080 тыс. | 340 тыс. | Epoch S04 (DGX A100 6,5 кВт / 8) |
| H100/H200 | 1 453 Вт | 1,00 | 688 тыс. | 688 тыс. | Epoch S04 (DGX H100 10,2 кВт / 8) |
| GB200 | 2 090 Вт | 2,53 | 478 тыс. | 1 209 тыс. | Epoch S04 (NVL72 132 кВт / 72) |
| GB300 | 2 217 Вт | 2,53 | 451 тыс. | 1 140 тыс. | Epoch S04 (NVL72 140 кВт / 72); H100e принят как у GB200 — пометка Epoch |
| Trainium2 | 871 Вт | 0,66 | 1 148 тыс. | 754 тыс. | Epoch S04: ~500 Вт TDP × 1,74 = 871 Вт IT (привязка к Rainier 300k H100e / 398 МВт); 1299/1979 H100e |
| Trainium3 | — | — | — | — | нет данных Epoch — не заполнено |
| TPUv7 (Ironwood) | 1 672 Вт | 2,33 | 598 тыс. | 1 394 тыс. | Epoch S04/S10: TDP 960 Вт × 1,742; 4,614 PFLOP/s 8-бит → 2,33 H100e |
| NVIDIA-микс OpenAI, конец 2025 (Hopper:Blackwell 1,48:1) | 1 710 Вт | — | 585 тыс. | 945 тыс. | наш расчёт по Epoch S04 (Epoch: ~945 H100e/МВт, ~585 тыс. чипов/ГВт) |
| Anthropic смешанный парк, конец 2025 | — | — | — | 865 тыс. | Epoch S04: 865 H100e/МВт (747–1 019) |
| TPU-парк Google (v5e/v5p/v6e/v7), конец 2025 | — | — | — | 1 009 тыс. | Epoch S04: ~1 009 H100e/МВт |
| Trainium2-парк | 871 Вт | — | 1 148 тыс. | 754 тыс. | Epoch S04: 754 H100e/МВт |
| 1 ГВт объекта при PUE 1,3 → NVIDIA-микс OpenAI | 1 710 Вт | — | 450 тыс. | 727 тыс. | [ASSUMPTION] PUE 1,3 — допущение внутри интервала Epoch 1,1–1,7 |

Пояснения: IT‑мощность на чип = мощность сервера на чип × 1,14 (IT‑overhead, 5–95 %: 1,00–1,35) [S04][V]. «Мощность объекта / IT ≈ 1,3×» — допущение внутри интервала PUE 1,1–1,7 Epoch [S04][E]; каталог ЦОД Epoch по умолчанию берёт PUE 1,2 для гиперскейлеров и 1,4 для остальных [S61][V]. «Абилин >450 тыс. GB200 на ~1,2 ГВт» — план полной застройки (1,2 ГВт — мощность объекта); на 2026-09-27 — 421 МВт IT ≈ 201 тыс. GB200 ≈ 509 тыс. H100e [S37][E]. Контрольные точки: Colossus 1 (150 тыс. H100 + 50 тыс. H200 + 30 тыс. GB200) → 276 тыс. H100e и 353 МВт IT против 276 тыс. и 340 МВт у Epoch (-0 % / +4 %) [S37][E], [S27][V]; Абилин 421 МВт → 509 тыс. H100e против 509 тыс. (-0 %) [E].

### D. Методология и оговорки

- **Единицы.** H100e — по пиковым плотным 8‑битным FLOP/s (для чипов без 8‑бит — 16‑бит) [S10][V]. Оценки Epoch — Монте‑Карло, центральное значение — медиана, интервал — 5‑й и 95‑й процентили; авторы называют оценки «более предварительными», чем обычные данные Epoch [S03][V].
- **Nowcast** [E]: `N(t) = N_2025 · g^Δt`; `N_2025` — лог‑нормальное по медиане и 90 % ДИ Epoch; `g` — лог‑нормальное с 90 % интервалом 2,5–4,5 (OpenAI) и 2,5–5,0 (Anthropic); 200 000 прогонов, seed 20260927. Перевод в ГВт: база — по эффективности парка Epoch (894 и 865 H100e/МВт), прирост — по 945 и 950 H100e/МВт [E]. Ограничение: данные о фактически работающих мощностях после конца 2025 не публикуются; всё после этой даты — модель.
- **Сплит** [E]: только в деньгах, базис — облачные расходы на compute; «обучение» = весь R&D‑compute, финальные прогоны — меньшая часть [S08][V]; строки другого базиса (WSJ [S31][V2], лизк отчётности [S34][V]) не смешиваются; валовая маржа инференса Anthropic не раскрыта, сценарии 2026 — сетка 50–72 %.
- **Сторонний инференс.** Учтён у Anthropic (≈ 10 %) и не учтён у OpenAI (до ~25 %) — сравнение смещено против OpenAI на 10–25 % [S04][E].
- **1,4 ГВт Anthropic** — оценка заинтересованной стороны [S11][V2]; Epoch моделирует 1,0–1,9 ГВт IT [S04][V].
- **Аудированная отчётность OpenAI 2025** (лизк, подтверждён FT): выручка $13,07 млрд, расходы $34 млрд, убыток $38,5 млрд; платежи Microsoft $10,59 млрд (R&D) + $6,05 млрд (cost of revenue) — другой базис (GAAP, только Microsoft), сплит на облачном базисе не заменяет [S34][V]. Дата публикации — 15.06.2026, а не 26.09.2026, как в пакете [X].
- **Утечки и вторичные данные.** Расходы на обучение и инференс приходят через The Information, WSJ, Sacra и Epoch [S15][V], [S16][V2], [S29][V2], [S06][V]; цифра «$9,4 млрд на обучение 2025» из исходного документа (L9, L56, L110) не подтверждается ни одним источником и удалена [X].
- **Отраслевые пропорции.** Gartner — рынок AI‑optimized IaaS ($42 млрд в 2026, инференс 55 %) [S30][V]; Deloitte: инференс ≈ 2/3 всего AI‑compute в 2026 (треть в 2023, половина в 2025) [S53][V]; Lenovo (CES 2026): 80/20 в пользу инференса [S54][V2] — рыночные пропорции, не лабораторий. DeepSeek: 2,788 млн H800 GPU‑часов на всё обучение V3 (2,664 млн — предобучение) [S48][V]; RL для R1 — ~147 тыс. GPU‑часов, ≈ $294 тыс. (≈ 5 %) [S49][V]; RL генерирует rollouts, то есть инференс‑подобную нагрузку — граница обучение/инференс на уровне железа размывается [E].
- **Отменённые и изменённые планы.** LOI NVIDIA $100 млрд заменён инвестицией $30 млрд [S17][V2]; отказ от расширения Абилина, пауза UK, выход из Норвегии [S12][V2]; «ГВт по контрактам» — верхняя граница, не прогноз ввода [E].
- **Свежие публикации после 20.09.2026, учтённые в реестре:**
  - 2026-09-25 · Tom's Hardware (зеркало Yahoo); TeslaNorth; пост Маска в X: SpaceXAI to add another 660,000 AI GPUs this year, nearing 1.44 million in operation [S56][V2]
  - 2026-09-24 · Epoch AI: AI Data Centers explorer — Colossus 1/2, Rainier (New Carlisle), Stargate Abilene [S37][E]
  - 2026-09-24 · TechCrunch (по Bloomberg): Oracle sends force majeure notice on its New Mexico Stargate data center [S58][V]
  - 2026-09-19 · Reuters по FT (зеркало GVWire): OpenAI forecasts cash burn near $280 billion by 2030, FT reports [S50][V2]
  - 2026-09-18 · Nscale Form S-1 (SEC); Pulse2; TechCrunch: Nscale IPO filing: Anthropic GPU services agreements up to ~$44.6B [S52][V2]
  - 2026-09-18 · CNBC (зеркало RuntimeWire): Anthropic and OpenAI hunt for smaller data center deals [S57][V2]
  - 2026-09-16 · Epoch AI: We're scaling our AI Data Centers research [S60][V]
  - 2026-09-09 · Epoch AI (Josh You): Introducing the AI Chip Users explorer [S02][V]
  - 2026-09-09 · Epoch AI: Data on AI chip users (explorer, CSV, ZIP) [S03][V]
  - 2026-09-08 · Quartz (зеркало Yahoo Finance): OpenAI signs multi-year compute deal with Firmus in Malaysia [S59][V2]
  - 2026-09-06 · The Information (Valida Pau): How Anthropic Clinched $517 Billion in Compute Deals in 11 Months [S36][V2]
  - 2026-09-06 · Dealroom; 24/7 Wall St (пересказ The Information): How Anthropic clinched $517 billion in compute deals — details [S51][V2]
  - 2026-09 · Epoch AI: AI Chip Users — Methodology [S04][V]
  - 2026-09 · Epoch AI: AI Data Centers — Methodology [S61][V]
  - 2026-08-27 · Epoch AI: Data on AI Chip Sales (H100e definition) [S10][V]

### E. Источники (дата доступа — 2026-09-27)

| id | дата | издатель | заголовок | URL | статус | дата доступа |
|---|---|---|---|---|---|---|
| S01 | 2026-01-18 | OpenAI (Sarah Friar) | A business that scales with the value of intelligence | https://openai.com/index/a-business-that-scales-with-the-value-of-intelligence/ | [V2] | 2026-09-27 |
| S02 | 2026-09-09 | Epoch AI (Josh You) | Introducing the AI Chip Users explorer | https://epoch.ai/latest/introducing-the-ai-chip-users-explorer | [V] | 2026-09-27 |
| S03 | 2026-09-09 | Epoch AI | Data on AI chip users (explorer, CSV, ZIP) | https://epoch.ai/data/ai-chip-users | [V] | 2026-09-27 |
| S04 | 2026-09 | Epoch AI | AI Chip Users — Methodology | https://epoch.ai/data/ai-chip-users-documentation/methodology | [V] | 2026-09-27 |
| S05 | 2026-05-20 | Epoch AI (Josh You) | Frontier labs don't use most AI compute (yet) | https://epoch.ai/gradient-updates/frontier-labs-dont-use-most-ai-compute | [V] | 2026-09-27 |
| S06 | 2026-02-04 | Epoch AI | Compute accounts for the majority of expenses of AI companies | https://epoch.ai/data-insights/company-spending-breakdown | [V] | 2026-09-27 |
| S07 | 2025-10-10 | Epoch AI | Most of OpenAI's 2024 compute went to experiments | https://epoch.ai/data-insights/openai-compute-spend | [V] | 2026-09-27 |
| S08 | 2026-03-23 | Epoch AI | Final training runs account for a minority of R&D compute spending | https://epoch.ai/gradient-updates/r-and-d-vs-training-compute | [V] | 2026-09-27 |
| S09 | 2026-01-28 | Epoch AI | Can AI companies become profitable? | https://epoch.ai/gradient-updates/can-ai-companies-become-profitable | [V] | 2026-09-27 |
| S10 | 2026-08-27 | Epoch AI | Data on AI Chip Sales (H100e definition) | https://epoch.ai/data/ai-chip-sales | [V] | 2026-09-27 |
| S11 | 2026-04-09 | Bloomberg (Shirin Ghaffary); Key Context (Tae Kim) | OpenAI tells investors it has computing advantage over Anthropic; memo 'Compute is the ballgame' | https://www.bloomberg.com/news/articles/2026-04-09/openai-tells-investors-it-has-computing-advantage-over-anthropic | [V2] | 2026-09-27 |
| S12 | 2026-04-29 | Bloomberg (Dina Bass); The Decoder | Building the compute infrastructure for the Intelligence Age | https://openai.com/index/building-the-compute-infrastructure-for-the-intelligence-age/ | [V2] | 2026-09-27 |
| S13 | 2026-05-05 | Bloomberg | OpenAI to spend $50 billion on computing in 2026, Brockman says | https://www.bloomberg.com/news/articles/2026-05-05/openai-to-spend-50-billion-on-computing-in-2026-brockman-says | [V2] | 2026-09-27 |
| S14 | 2026-02-20 | Reuters | OpenAI expects compute spend of around $600 billion through 2030 | https://finance.yahoo.com/news/openai-sees-compute-spend-around-223950561.html | [V2] | 2026-09-27 |
| S15 | 2026-02-21 | The Decoder (по The Information) | OpenAI adds $111 billion to its cash burn forecast | https://the-decoder.com/openai-adds-111-billion-to-its-cash-burn-forecast-as-ai-costs-spiral-beyond-projections/ | [V] | 2026-09-27 |
| S16 | 2026-07-29 | Sacra | OpenAI revenue, valuation & funding | https://sacra.com/c/openai/ | [V2] | 2026-09-27 |
| S17 | 2026-02-20 | Financial Times via Business Standard | Nvidia $30bn OpenAI investment after shelving $100bn deal | https://www.business-standard.com/technology/tech-news/nvidia-30bn-openai-investment-after-shelving-100bn-deal-126022000503_1.html | [V2] | 2026-09-27 |
| S18 | 2025-09-22 | NVIDIA/OpenAI press release (mirror) | OpenAI and NVIDIA announce strategic partnership to deploy 10 gigawatts | https://investor.nvidia.com/news/press-release-details/2025/OpenAI-and-NVIDIA-Announce-Strategic-Partnership-to-Deploy-10-Gigawatts-of-NVIDIA-Systems/default.aspx | [V] | 2026-09-27 |
| S19 | 2025-09-23 | OpenAI | OpenAI, Oracle, and SoftBank expand Stargate with five new AI data center sites | https://openai.com/index/five-new-stargate-sites/ | [V] | 2026-09-27 |
| S20 | 2026-02-27 | OpenAI/Amazon (Business Wire) | OpenAI and Amazon Announce Strategic Partnership | https://secure.businesswire.com/news/home/20260227557827/en/OpenAI-and-Amazon-Announce-Strategic-Partnership | [V] | 2026-09-27 |
| S21 | 2026-04-27 | OpenAI | The next phase of the Microsoft OpenAI partnership | https://openai.com/index/next-phase-of-microsoft-partnership | [V] | 2026-09-27 |
| S22 | 2026-06-08 | OpenAI; CNBC; Fortune | Confidential submission of draft S-1 | https://openai.com/index/openai-submits-confidential-s-1/ | [V] | 2026-09-27 |
| S23 | 2026-04 | Cerebras S-1 (SEC); DCD | Cerebras Form S-1; OpenAI CFO says company ended 2025 with 1.9GW | https://www.sec.gov/Archives/edgar/data/2021728/000162828026025762/cerebras-sx1april2026.htm | [V/V2] | 2026-09-27 |
| S24 | 2026-08-17 | OpenAI; NVIDIA; CNBC; SiliconANGLE | OpenAI joins PORTS-Pike project | https://openai.com/index/openai-joins-ports-pike-project/ | [V] | 2026-09-27 |
| S25 | 2026-04-20 | Anthropic; Amazon | Anthropic and Amazon expand compute collaboration | https://www.anthropic.com/news/anthropic-amazon-compute | [V] | 2026-09-27 |
| S26 | 2026-04-06 | Anthropic; TNW; Broadcom 8-K | Anthropic expands partnership with Google and Broadcom for multiple gigawatts | https://anthropic.com/news/google-broadcom-partnership-compute | [V] | 2026-09-27 |
| S27 | 2026-05-06 | SpaceXAI; Anthropic; TechCrunch; SpaceX S-1 | New Compute Partnership with Anthropic; Anthropic will pay xAI $1.25B per month | https://x.ai/news/anthropic-compute-partnership | [V] | 2026-09-27 |
| S28 | 2026-04-10 | CoreWeave | CoreWeave Announces Multi-Year Agreement With Anthropic | https://coreweave.com/news/coreweave-announces-multi-year-agreement-with-anthropic | [V] | 2026-09-27 |
| S29 | 2026-05-20 | WSJ; Dealroom (SemiAnalysis); Zitron | Mind-blowing growth is about to propel Anthropic into its first profitable quarter | https://www.wsj.com/tech/ai/mind-blowing-growth-is-about-to-propel-anthropic-into-its-first-profitable-quarter-7edbf2f4 | [V2] | 2026-09-27 |
| S30 | 2026-08-10 | Gartner | Gartner Forecasts Worldwide AI-Optimized IaaS Spending to Grow 96% in 2026 | https://www.gartner.com/en/newsroom/press-releases/2026-08-10-gartner-forecasts-worldwide-artificial-intelligence-optimized-iaas-spending-to-grow-96-percent-in-2026 | [V] | 2026-09-27 |
| S31 | 2026-04-05 | Wall Street Journal (Berber Jin, Nate Rattner) | An Inside Look at OpenAI and Anthropic's Finances Ahead of Their IPOs | https://www.wsj.com/tech/ai/openai-anthropic-ipo-finances-04b3cfb9 | [V2] | 2026-09-27 |
| S32 | 2025-09-25 | Fortune | I met Sam Altman in Texas: the race for AI is a gigawatt arms race | https://fortune.com/2025/09/25/i-met-sam-altman-in-texas-hes-turning-the-race-for-ai-into-a-gigawatt-arms-race | [V2] | 2026-09-27 |
| S33 | 2026-07-27 | DCD | Anthropic to use all of SpaceX-xAI's Colossus 1 data center compute | https://www.datacenterdynamics.com/en/news/anthropic-to-use-all-of-spacex-xais-colossus-1-data-center-compute/ | [V2] | 2026-09-27 |
| S34 | 2026-06-15 | Ed Zitron (wheresyoured.at); FT via Reuters | Exclusive: OpenAI Losses Increased Nearly 8X in 2025, With Spending Hitting $34 Billion | https://www.wheresyoured.at/exclusive-openai-financials/ | [V] | 2026-09-27 |
| S35 | 2026-04-10 | Semafor | Anthropic is gaining on OpenAI's revenue but hasn't yet eclipsed it | https://www.semafor.com/article/04/10/2026/anthropic-is-gaining-on-openais-revenue-but-hasnt-yet-eclipsed-it | [V2] | 2026-09-27 |
| S36 | 2026-09-06 | The Information (Valida Pau) | How Anthropic Clinched $517 Billion in Compute Deals in 11 Months | https://www.theinformation.com/articles/anthropic-clinched-517-billion-compute-deals-11-months | [V2] | 2026-09-27 |
| S37 | 2026-09-24 | Epoch AI | AI Data Centers explorer — Colossus 1/2, Rainier (New Carlisle), Stargate Abilene | https://epoch.ai/data/ai-data-centers | [E] | 2026-09-27 |
| S38 | 2026-06-05 | CNBC | Google to pay SpaceX $920 million a month for xAI compute capacity | https://www.cnbc.com/2026/06/05/google-to-pay-spacex-920-million-a-month-for-xai-compute-capacity.html | [V2] | 2026-09-27 |
| S39 | 2025-07-20 | Sam Altman (X) | Post on crossing 'well over 1 million GPUs' by end of 2025 | https://x.com/sama/status/1947057625780396512 | [V] | 2026-09-27 |
| S40 | 2025-10-06 | AMD/OpenAI press release | AMD and OpenAI announce strategic partnership to deploy 6 gigawatts of AMD GPUs | https://ir.amd.com/news-events/press-releases/detail/1260/amd-and-openai-announce-strategic-partnership-to-deploy-6-gigawatts-of-amd-gpus | [V] | 2026-09-27 |
| S41 | 2025-10-13 | Broadcom/OpenAI press release | OpenAI and Broadcom announce strategic collaboration to deploy 10 gigawatts of OpenAI-designed AI accelerators | https://www.broadcom.com/company/news/product-releases/63631 | [V2] | 2026-09-27 |
| S42 | 2025-06-10 | Reuters | Exclusive: OpenAI taps Google in unprecedented cloud deal despite AI rivalry, sources say (Reuters) | https://www.cnbc.com/2025/06/10/openai-taps-google-in-unprecedented-cloud-deal-despite-ai-rivalry-sources-say.html | [V2] | 2026-09-27 |
| S43 | 2025-10-23 | Anthropic | Expanding our use of Google Cloud TPUs and Services | https://www.anthropic.com/news/expanding-our-use-of-google-cloud-tpus-and-services | [V] | 2026-09-27 |
| S44 | 2025-11-18 | Anthropic; Microsoft; NVIDIA | Microsoft, NVIDIA, and Anthropic announce strategic partnerships | https://www.anthropic.com/news/microsoft-nvidia-anthropic-announce-strategic-partnerships | [V] | 2026-09-27 |
| S45 | 2025-11-12 | Anthropic | Anthropic invests $50 billion in American AI infrastructure | https://www.anthropic.com/news/anthropic-invests-50-billion-in-american-ai-infrastructure | [V] | 2026-09-27 |
| S46 | 2026-08-12 | Epoch AI (Campbell Hutcheson) | Will financing bottleneck AI compute? An Anthropic case study | https://epoch.ai/gradient-updates/will-financing-bottleneck-ai-compute | [V] | 2026-09-27 |
| S47 | 2025-10-29 | Amazon/AWS | AWS activates Project Rainier: One of the world's largest AI compute clusters comes online | https://www.aboutamazon.com/news/aws/aws-project-rainier-ai-trainium-chips-compute-cluster | [V] | 2026-09-27 |
| S48 | 2024-12-27 | DeepSeek-AI (arXiv 2412.19437) | DeepSeek-V3 Technical Report | https://arxiv.org/abs/2412.19437 | [V] | 2026-09-27 |
| S49 | 2025-09-17 | Nature 645, 633–638 (DeepSeek-AI) | DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning | https://www.nature.com/articles/s41586-025-09422-z | [V] | 2026-09-27 |
| S50 | 2026-09-19 | Reuters по FT (зеркало GVWire) | OpenAI forecasts cash burn near $280 billion by 2030, FT reports | https://gvwire.com/2026/09/19/openai-forecasts-cash-burn-near-280-billion-by-2030-ft-reports/ | [V2] | 2026-09-27 |
| S51 | 2026-09-06 | Dealroom; 24/7 Wall St (пересказ The Information) | How Anthropic clinched $517 billion in compute deals — details | https://dealroom.co/news/info-iclajk-how-anthropic-clinched-517-billion-in-compute-deals-in-11-months/ | [V2] | 2026-09-27 |
| S52 | 2026-09-18 | Nscale Form S-1 (SEC); Pulse2; TechCrunch | Nscale IPO filing: Anthropic GPU services agreements up to ~$44.6B | https://pulse2.com/nscale-ipo-filing-reveals-103-4-billion-in-active-and-contracted-ai-infrastructure-agreements/ | [V2] | 2026-09-27 |
| S53 | 2025-11-17 | Deloitte Insights, TMT Predictions 2026 | More compute for AI, not less | https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/compute-power-ai.html | [V] | 2026-09-27 |
| S54 | 2026-01-08 | Computerworld (Maria Korolov) | CES 2026: AI compute sees a shift from training to inference | https://www.computerworld.com/article/4114579/ces-2026-ai-compute-sees-a-shift-from-training-to-inference.html | [V2] | 2026-09-27 |
| S55 | 2026-08-04 | SpaceX (SEC, earnings release Q2 2026); Motley Fool (стенограмма) | SpaceX Q2 2026 results: nameplate compute 1.4 GW | https://www.sec.gov/Archives/edgar/data/1181412/000162828026052515/earningsreleaseq22608042.htm | [V] | 2026-09-27 |
| S56 | 2026-09-25 | Tom's Hardware (зеркало Yahoo); TeslaNorth; пост Маска в X | SpaceXAI to add another 660,000 AI GPUs this year, nearing 1.44 million in operation | https://tech.yahoo.com/ai/articles/elon-musks-spacexai-add-another-154000947.html | [V2] | 2026-09-27 |
| S57 | 2026-09-18 | CNBC (зеркало RuntimeWire) | Anthropic and OpenAI hunt for smaller data center deals | https://www.cnbc.com/2026/09/18/anthropic-openai-small-ai-data-center-deals.html | [V2] | 2026-09-27 |
| S58 | 2026-09-24 | TechCrunch (по Bloomberg) | Oracle sends force majeure notice on its New Mexico Stargate data center | https://techcrunch.com/2026/09/24/oracle-sends-force-majeure-notice-on-its-new-mexico-stargate-data-center/ | [V] | 2026-09-27 |
| S59 | 2026-09-08 | Quartz (зеркало Yahoo Finance) | OpenAI signs multi-year compute deal with Firmus in Malaysia | https://finance.yahoo.com/technology/ai/articles/openai-signs-multi-compute-deal-140329941.html | [V2] | 2026-09-27 |
| S60 | 2026-09-16 | Epoch AI | We're scaling our AI Data Centers research | https://epoch.ai/latest/scaling-ai-data-centers-research | [V] | 2026-09-27 |
| S61 | 2026-09 | Epoch AI | AI Data Centers — Methodology | https://epoch.ai/data/data-centers-documentation/methodology | [V] | 2026-09-27 |
| S62 | 2026-08-17 | NVIDIA newsroom | NVIDIA guarantees SB Energy's PORTS-Pike Technology Campus in Ohio to exclusively host NVIDIA AI compute | https://nvidianews.nvidia.com/news/nvidia-guarantees-sb-energy-s-ports-pike-technology-campus-in-ohio-to-exclusively-host-nvidia-ai-compute | [V] | 2026-09-27 |
| S63 | 2026-08-17 | CNBC; Data Center Knowledge | Nvidia will provide up to $105 billion in financing for OpenAI Ohio data center, filing shows | https://www.cnbc.com/2026/08/17/nvidia-financing-open-ai-data-center-ohio.html | [V2] | 2026-09-27 |
