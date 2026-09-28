%run -i gpu_fleet_review_out/calc_nowcast.py
md(open(OUT / 'results' / f'nowcast_{DATE_TAG}.md', encoding='utf-8').read())
