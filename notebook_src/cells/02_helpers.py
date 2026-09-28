# ---------------------------------------------------------------- хелперы (общие для всех блоков)
Z90 = 1.6448536269514722   # 95-й процентиль N(0,1): 90 % интервал = [p05, p95]

def lognorm_ci(lo, hi, n, rng):
    """Лог-нормальное с 5-м = lo и 95-м = hi процентилем (аналог squigglepy `to(lo, hi)`, которым пользуется Epoch)."""
    mu = (math.log(lo) + math.log(hi)) / 2
    sigma = (math.log(hi) - math.log(lo)) / (2 * Z90)
    return np.exp(rng.normal(mu, sigma, n))

def lognorm_med_ci(med, lo, hi, n, rng):
    """Лог-нормальное по медиане и 90 % ДИ (sigma — из отношения p95/p05; медиана фиксируется точно)."""
    sigma = (math.log(hi) - math.log(lo)) / (2 * Z90)
    return np.exp(rng.normal(math.log(med), sigma, n))

def norm_ci(lo, hi, n, rng, lclip=None, rclip=None):
    """Нормальное с 90 % интервалом [lo, hi], с обрезкой (аналог squigglepy `norm(lo, hi, lclip, rclip)`)."""
    x = rng.normal((lo + hi) / 2, (hi - lo) / (2 * Z90), n)
    if lclip is not None: x = np.maximum(x, lclip)
    if rclip is not None: x = np.minimum(x, rclip)
    return x

def pct(x, qs=(5, 25, 50, 75, 95)):
    """Словарь процентилей p05…p95."""
    v = np.percentile(np.asarray(x), qs)
    return {f'p{q:02d}': float(a) for q, a in zip(qs, v)}

def ru(x, nd=2):
    """Число в русской записи: запятая как десятичный разделитель, тонкий пробел между тысячами."""
    if x is None or (isinstance(x, float) and math.isnan(x)): return '—'
    s = f'{x:,.{nd}f}'.replace(',', ' ').replace('.', ',')
    return s

def ru_m(x, nd=2):   return ru(x / 1e6, nd) + ' млн'      # H100e / чипы → «1,74 млн»
def ru_k(x, nd=0):   return ru(x / 1e3, nd) + ' тыс.'     # → «509 тыс.»
def ru_gw(x, nd=1):  return ru(x / 1000, nd) + ' ГВт'     # МВт → «1,9 ГВт»
def ru_b(x, nd=1):   return '$' + ru(x, nd) + ' млрд'    # млрд USD

def save_json(obj, path):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=float), encoding='utf-8')
    return path

def write_text(text, path):
    Path(path).write_text(text, encoding='utf-8'); return path

def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def md(text):
    display(Markdown(text))

print('helpers ok')
