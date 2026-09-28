# Данные для слайда (по состоянию на 27.09.2026; источники проверены 27 сентября 2026)

Строки ниже копировать как есть: неразрывные пробелы и формат чисел уже применены.

## Заголовок (полный; если не помещается в две строки — использовать короткий вариант ниже)

Число чипов не публикуется. В эквивалентах H100: OpenAI ≈ 1,7 млн, Anthropic ≈ 1,2 млн на конец 2025; сегодня, по нашей оценке, примерно в 2,5 раза больше у обеих. Деление между обучением и инференсом известно только в деньгах: в 2025 году 49/51 у OpenAI и 60/40 у Anthropic; в 2026 по плану OpenAI доля обучения 59–69 %, у Anthropic по сценариям 34–54 %.

**Короткий заголовок (≤ 2 строк):** Число чипов не публикуется. В эквивалентах H100: OpenAI ≈ 1,7 млн, Anthropic ≈ 1,2 млн на конец 2025, сегодня по нашей оценке ≈ в 2,5 раза больше. Деление между обучением и инференсом известно только в деньгах.

## Три ключевых сообщения (для понимания контекста; на слайд текстом не выносить — эти данные уже представлены в графиках)

1. Конец 2025 (сопоставимая точка): OpenAI ≈ 1,9 ГВт (раскрыто компанией) ≈ 1,74 млн эквивалентов H100 (оценка Epoch AI, 90 % интервал 1,25–2,19 млн); Anthropic ≈ 1,4 ГВт (оценка OpenAI) ≈ 1,19 млн (0,84–1,72 млн).
2. 27.09.2026 (наша модель, экстраполяция от Epoch AI): OpenAI ≈ 4,27 млн (3,00–6,08 млн) ≈ 4,6 ГВт; Anthropic ≈ 3,03 млн (1,95–4,70 млн) ≈ 3,3 ГВт.
3. Сплит расходов на вычисления «обучение и исследования / инференс»: OpenAI 71/29 (2024), 49/51 (2025), в 2026 по плану обучение 59–69 %; Anthropic 60/40 (2025), в 2026 по сценариям обучение 34–54 %.

## Левая часть: парк в эквивалентах H100 (4 столбика с усами интервала)

| Компания | Период | Медиана, млн | 90 % интервал, млн | Что это | Заливка | Подпись мощности под столбиком |
|---|---|---|---|---|---|---|
| OpenAI | конец 2025 | 1,74 | 1,25–2,19 | оценка Epoch AI; Epoch AI, AI Chip Users, 09.09.2026 | сплошная | 1,9 ГВт — раскрыто компанией (блог OpenAI (финансовый директор Сара Фрайар), 18.01.2026) |
| OpenAI | 27.09.2026 | 4,27 | 3,00–6,08 | наша оценка (экстраполяция); наша модель на основе Epoch AI | штриховка | ≈ 4,6 ГВт (3,3–6,6) — наша оценка |
| Anthropic | конец 2025 | 1,19 | 0,84–1,72 | оценка Epoch AI; Epoch AI, AI Chip Users, 09.09.2026 | сплошная | ≈ 1,4 ГВт — оценка OpenAI (конкурента) (Bloomberg, меморандум OpenAI инвесторам, 09.04.2026) |
| Anthropic | 27.09.2026 | 3,03 | 1,95–4,70 | наша оценка (экстраполяция); наша модель на основе Epoch AI | штриховка | ≈ 3,3 ГВт (2,1–5,1) — наша оценка |

Ось Y: «млн эквивалентов H100», от 0 до 7,5. Усы — 5-й и 95-й процентили; подпись медианы — над верхней засечкой уса, по центру столбика. Под каждым столбиком четыре строки: компания / период / подпись мощности / статус словами; источники под столбики не выносить — они в подвале.

Расшифровки одной строкой под графиком (обе обязательны): «Эквивалент H100 — вычислительная мощность одного NVIDIA H100 (единица Epoch AI); один GB200 = 2,53 эквивалента, один Trainium2 = 0,66.» и «ГВт — потребление вычислительного оборудования (серверы и сеть), без охлаждения и потерь здания.». Числа 2,53 и 0,66 на слайд не выносить.

## Правая часть: доля расходов на вычисления — обучение и исследования / инференс (горизонтальные stacked-бары)

| Компания | Год | Обучение и исследования, % | Инференс, % | Что это | Заливка |
|---|---|---|---|---|---|
| OpenAI | 2024 | 71 | 29 | оценка Epoch AI по данным The Information; Epoch AI (по данным The Information), 10.10.2025 | сплошная |
| OpenAI | 2025 | 49 | 51 | оценка Epoch AI (The Information, Sacra); Epoch AI, методология AI Chip Users, сентябрь 2026; Sacra, 29.07.2026 | сплошная |
| OpenAI | 2026, план (сценарии) | 59–69 | 31–41 | сценарии по плану; The Information (через The Decoder), 21.02.2026; Bloomberg, показания Грега Брокмана, 05.05.2026 | обучение 0–max штриховкой цветом компании, на min — контурная отметка; инференс серый от max до 100 % |
| Anthropic | 2024 | не раскрыто | не раскрыто | не раскрыто; Epoch AI, методология AI Chip Users, сентябрь 2026 | контур 1 px серым #8f8e88 без заливки, внутри по центру текст «не раскрыто» тёмно-серым |
| Anthropic | 2025 | 60 | 40 | оценка: прогноз компании по The Information и расчёт Epoch AI; Epoch AI (по данным The Information), 04.02.2026 | сплошная |
| Anthropic | 2026, первое полугодие (сценарии) | 34–54 | 46–66 | сценарии по квартальным данным The Wall Street Journal; The Wall Street Journal, 20.05.2026 | обучение 0–max штриховкой цветом компании, на min — контурная отметка; инференс серый от max до 100 % |

Ось X: 0–100 %. Строки 2026 года: сегмент обучения от 0 до максимальной доли — штриховка цветом компании, на минимальной доле — контурная отметка (тонкая вертикальная линия); инференс — серый от максимальной доли до 100 %. Подписи процентов — снаружи бара тёмно-серым: слева «обучение 71 %», справа «инференс 29 %»; для 2026 — «59–69 %» и «31–41 %». Anthropic 2024 — контур 1 px серым без заливки и текст «не раскрыто» по центру.

## Легенда статусов (обязательна на слайде)

- факт (раскрыто компанией или подтверждено прессой): сплошная заливка
- оценка Epoch AI: сплошная заливка, усы — 90 % интервал
- наша оценка / сценарий: диагональная штриховка
- Цвет компании: OpenAI #2470cc, Anthropic #c9491a; инференс в stacked-барах — нейтральный #8f8e88.

## Две оговорки (по одной строке каждая, дословно или короче)

1. «Обучение» здесь — весь бюджет исследований и разработки (эксперименты, дообучение); финальный прогон одной модели — меньшая его часть.
2. Инференс на площадках партнёров (Amazon Bedrock, Google Vertex) учтён у Anthropic и не учтён у OpenAI (Microsoft Azure): сравнение парков на левом графике занижает OpenAI на 10–25 %.

## Подвал

Источники: блог OpenAI (финансовый директор Сара Фрайар), 18.01.2026; Epoch AI, AI Chip Users, 09.09.2026; Epoch AI, методология AI Chip Users, сентябрь 2026; Bloomberg, меморандум OpenAI инвесторам, 09.04.2026; Bloomberg, показания Грега Брокмана, 05.05.2026; The Information (через The Decoder), 21.02.2026; Sacra, 29.07.2026; Epoch AI (по данным The Information), 10.10.2025; Epoch AI (по данным The Information), 04.02.2026; The Wall Street Journal, 20.05.2026; Epoch AI, 23.03.2026. Все ссылки проверены 27 сентября 2026. Оценка на 27.09.2026 — 200 000 прогонов модели с интервалами.

## Числа про запас (использовать только если есть место; статус указан)

- Физических ускорителей, конец 2025: OpenAI ≈ 1,14 млн (0,84 млн–1,34 млн), Anthropic ≈ 1,25 млн (0,90 млн–1,76 млн) — наш расчёт по параметрам Epoch AI.
- Расходы на облачные вычисления 2025: OpenAI $16,3 млрд, Anthropic $6,8 млрд — Epoch AI по данным The Information.
- OpenAI 2024: обучение ≈ 5, инференс ≈ 2 (млрд $)
- OpenAI 2025: обучение ≈ 8, инференс 8,4 (млрд $)
- OpenAI 2026 план: обучение 32, инференс 14,1–22 (сценарии) (млрд $)
- Anthropic 2025: обучение 4,1, инференс ≈ 2,7 (млрд $)
- Anthropic 2026 I полугодие (сценарии): обучение 3,2–5,1, инференс 4,4–6,3 (млрд $)
- Темп роста в модели: OpenAI 2,5–4,5 раза (Epoch AI: «более чем утроится» за 2026; бюджет $50 млрд ≈ ×3); Anthropic 2,5–5 раз (вводы TPU, Trainium, Colossus 1, Azure; прогноз OpenAI 3–4 ГВт).
- Проверка по известным площадкам: OpenAI не меньше 2,00 млн (нижняя граница по каталогу ЦОД Epoch AI); Anthropic 2,53 млн (2,22 млн–2,84 млн).
- OpenAI (заявлено компаниями): 10 ГВт законтрактовано в США к апрелю 2026 (OpenAI, 29.04.2026); первые гигаватты во 2-м полугодии 2026 — AMD MI450 (пресс-релиз AMD, 06.10.2025), Broadcom (Broadcom, 13.10.2025). Письмо о намерениях с NVIDIA на 10 ГВт систем Vera Rubin (пресс-релиз NVIDIA, 22.09.2025) в договор не оформлено и заменено инвестицией $30 млрд (Financial Times (пересказ Business Standard), 20.02.2026); мощности по нему не планируются
- Anthropic (заявлено компаниями): «почти 1 ГВт» Trainium к концу 2026 (Anthropic, 20.04.2026), «значительно больше 1 ГВт» TPU в 2026 (Anthropic, 23.10.2025), до 1 ГВт Azure (Anthropic, 18.11.2025), Colossus 1 (~300 МВт) с июня 2026 (блог xAI (SpaceX) и Anthropic, 06.05.2026); прогноз OpenAI (оценка конкурента) — 3–4 ГВт (Bloomberg, меморандум OpenAI инвесторам, 09.04.2026)

## Чего на слайде быть не должно

- коды источников и статусов вроде [S07], [V2], [E]
- термины nowcast, H100e, R&D-compute, Δt, PUE без расшифровки
- любые числа, которых нет в этом пакете
- суммирование гигаватт из пресс-релизов как «парка»
- точечные утверждения о 2026 годе без слова «оценка» или «сценарий»

## Источники (полные)

| Издатель | Дата | Заголовок | Ссылка |
|---|---|---|---|
| OpenAI (Sarah Friar) | 2026-01-18 | A business that scales with the value of intelligence | https://openai.com/index/a-business-that-scales-with-the-value-of-intelligence/ |
| Epoch AI (Josh You) | 2026-09-09 | Introducing the AI Chip Users explorer | https://epoch.ai/latest/introducing-the-ai-chip-users-explorer |
| Bloomberg (Shirin Ghaffary); Key Context (Tae Kim) | 2026-04-09 | OpenAI tells investors it has computing advantage over Anthropic; memo 'Compute is the ballgame' | https://www.bloomberg.com/news/articles/2026-04-09/openai-tells-investors-it-has-computing-advantage-over-anthropic |
| Bloomberg | 2026-05-05 | OpenAI to spend $50 billion on computing in 2026, Brockman says | https://www.bloomberg.com/news/articles/2026-05-05/openai-to-spend-50-billion-on-computing-in-2026-brockman-says |
| The Decoder (по The Information) | 2026-02-21 | OpenAI adds $111 billion to its cash burn forecast | https://the-decoder.com/openai-adds-111-billion-to-its-cash-burn-forecast-as-ai-costs-spiral-beyond-projections/ |
| Epoch AI | 2026-02-04 | Compute accounts for the majority of expenses of AI companies | https://epoch.ai/data-insights/company-spending-breakdown |
| WSJ; Dealroom (SemiAnalysis); Zitron | 2026-05-20 | Mind-blowing growth is about to propel Anthropic into its first profitable quarter | https://www.wsj.com/tech/ai/mind-blowing-growth-is-about-to-propel-anthropic-into-its-first-profitable-quarter-7edbf2f4 |
| Epoch AI | 2026-09 | AI Chip Users — Methodology | https://epoch.ai/data/ai-chip-users-documentation/methodology |
| Sacra | 2026-07-29 | OpenAI revenue, valuation & funding | https://sacra.com/c/openai/ |
| Epoch AI | 2025-10-10 | Most of OpenAI's 2024 compute went to experiments | https://epoch.ai/data-insights/openai-compute-spend |
| Epoch AI | 2026-03-23 | Final training runs account for a minority of R&D compute spending | https://epoch.ai/gradient-updates/r-and-d-vs-training-compute |
| Epoch AI | 2026-09-24 | AI Data Centers explorer — Colossus 1/2, Rainier (New Carlisle), Stargate Abilene | https://epoch.ai/data/ai-data-centers |
| Bloomberg (Dina Bass); The Decoder | 2026-04-29 | Building the compute infrastructure for the Intelligence Age | https://openai.com/index/building-the-compute-infrastructure-for-the-intelligence-age/ |
| NVIDIA/OpenAI press release (mirror) | 2025-09-22 | OpenAI and NVIDIA announce strategic partnership to deploy 10 gigawatts | https://investor.nvidia.com/news/press-release-details/2025/OpenAI-and-NVIDIA-Announce-Strategic-Partnership-to-Deploy-10-Gigawatts-of-NVIDIA-Systems/default.aspx |
| Financial Times via Business Standard | 2026-02-20 | Nvidia $30bn OpenAI investment after shelving $100bn deal | https://www.business-standard.com/technology/tech-news/nvidia-30bn-openai-investment-after-shelving-100bn-deal-126022000503_1.html |
| AMD/OpenAI press release | 2025-10-06 | AMD and OpenAI announce strategic partnership to deploy 6 gigawatts of AMD GPUs | https://ir.amd.com/news-events/press-releases/detail/1260/amd-and-openai-announce-strategic-partnership-to-deploy-6-gigawatts-of-amd-gpus |
| Broadcom/OpenAI press release | 2025-10-13 | OpenAI and Broadcom announce strategic collaboration to deploy 10 gigawatts of OpenAI-designed AI accelerators | https://www.broadcom.com/company/news/product-releases/63631 |
| Anthropic; Amazon | 2026-04-20 | Anthropic and Amazon expand compute collaboration | https://www.anthropic.com/news/anthropic-amazon-compute |
| Anthropic | 2025-10-23 | Expanding our use of Google Cloud TPUs and Services | https://www.anthropic.com/news/expanding-our-use-of-google-cloud-tpus-and-services |
| Anthropic; Microsoft; NVIDIA | 2025-11-18 | Microsoft, NVIDIA, and Anthropic announce strategic partnerships | https://www.anthropic.com/news/microsoft-nvidia-anthropic-announce-strategic-partnerships |
| SpaceXAI; Anthropic; TechCrunch; SpaceX S-1 | 2026-05-06 | New Compute Partnership with Anthropic; Anthropic will pay xAI $1.25B per month | https://x.ai/news/anthropic-compute-partnership |
