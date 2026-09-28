# ---------------------------------------------------------------- параметры
import os, io, re, json, math, hashlib, textwrap, datetime as dt, urllib.request
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from IPython.display import Markdown, HTML, display

NOWCAST_DATE = dt.date.fromisoformat(os.environ.get('NOWCAST_DATE', '2026-09-27'))  # дата слайда (зафиксирована; переопределяется переменной окружения)
ACCESSED     = '2026-09-27'          # дата проверки источников (реестр собран и проверен в этот день)
SEED         = 20260927              # фиксированный seed всех Монте-Карло
N_MC         = 200_000               # прогонов Монте-Карло
ONLINE       = os.environ.get('ONLINE', '1') == '1'   # пытаться ли скачивать CSV Epoch
OUT          = Path('gpu_fleet_review_out')           # выходная папка (фиксирована: на неё ссылаются %%writefile)
for sub in ['data/epoch', 'results']:
    (OUT / sub).mkdir(parents=True, exist_ok=True)

DATE_TAG = NOWCAST_DATE.isoformat()
pd.set_option('display.max_colwidth', 120)
pd.set_option('display.width', 200)
plt.rcParams.update({'figure.dpi': 110, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.grid': True, 'grid.alpha': 0.25, 'font.size': 10})
print(f'NOWCAST_DATE = {NOWCAST_DATE}   ACCESSED = {ACCESSED}   SEED = {SEED}   N_MC = {N_MC:,}   ONLINE = {ONLINE}')
print(f'Выход: {OUT.resolve()}')
