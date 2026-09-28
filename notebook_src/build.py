"""Собирает gpu_fleet_review.ipynb из cells/*.md|*.py (по алфавиту имён); встроенные данные берутся из inputs/. Запуск: python3 notebook_src/build.py"""
import sys, re
from pathlib import Path
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
cells_dir = Path(__file__).parent / 'cells'
nb = new_notebook()
nb.metadata['kernelspec'] = {'name': 'python3', 'display_name': 'Python 3', 'language': 'python'}
nb.metadata['language_info'] = {'name': 'python'}
ROOT = Path(__file__).resolve().parents[1]
SUBS = {
    '{{SOURCES_CSV}}': (Path(__file__).parent / 'inputs' / 'sources_2026-09-27.csv').read_text(encoding='utf-8').strip(),
    '{{KEY_FIGURES_CSV}}': (Path(__file__).parent / 'inputs' / 'key_figures_2026-09-27.csv').read_text(encoding='utf-8').strip(),
    '{{DRAFT_ORIGINAL}}': (Path(__file__).parent / 'inputs' / 'draft_original.md').read_text(encoding='utf-8').strip(),
}
for name in ('UPDATES_EXTRA', 'NEW_ROWS'):
    p = cells_dir / f'{name}.py.txt'
    SUBS['{{' + name + '}}'] = p.read_text(encoding='utf-8').rstrip('\n') if p.exists() else ''
for f in sorted(cells_dir.iterdir()):
    if f.suffix not in ('.md', '.py'): continue
    src = f.read_text(encoding='utf-8').rstrip('\n')
    for k, v in SUBS.items():
        assert '"""' not in v, f'triple quotes inside {k}'
        src = src.replace(k, v)
    nb.cells.append(new_markdown_cell(src) if f.suffix == '.md' else new_code_cell(src))
out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'gpu_fleet_review.ipynb'
nbformat.write(nb, out)
print(f'{len(nb.cells)} cells -> {out}')
