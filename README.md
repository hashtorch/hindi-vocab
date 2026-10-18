# Hindi Vocabulary (`hindi-vocab`)

A minimal, curated, frequency-ranked dictionary of standard Hindi base headwords designed for language learning and natural language applications.

## Dataset Overview

* **File**: [`vocab.json`](file:///home/zenhome/Projects/hindi-vocab/vocab.json)
* **Total Entries**: 4,895 lemmatized single-word headwords
* **Order**: Ranked strictly from highest frequency to lowest frequency (implicit in sequential `id`)
* **Indexing**: Continuous, sequential IDs (`1` to `4895`)

## Schema

Each entry in [`vocab.json`](file:///home/zenhome/Projects/hindi-vocab/vocab.json) consists exclusively of:

```json
{
  "id": 1,
  "hi": "है",
  "en": "is"
}
```

* `id` *(integer)*: 1-indexed rank ordered strictly from highest frequency to lowest frequency.
* `hi` *(string)*: Standard Hindi headword in Devanagari script (pure single-word citation lemma).
* `en` *(string)*: Concise single English translation word (no markers or parenthetical clutter).

---

## Frequency Curve & Score Mapping

Raw frequency is deliberately omitted from [`vocab.json`](file:///home/zenhome/Projects/hindi-vocab/vocab.json) to keep the dataset minimal and clean. When approximate frequency counts or a normalized frequency score ($5.0 \to 0.1$) are needed, they can be computed on demand using the empirical corpus best-fit curves documented below.

### 1. Empirical Corpus Reference Anchors

Historical corpus frequency data ($f_1 = 38,292 \to f_{5012} \approx 2$) follows a standard Zipfian distribution:

| Rank ($r$) | Empirical Freq ($f$) | Calibrated Score ($s$) |
|:---:|:---:|:---:|
| **1** | 38,292 | **5.0** |
| **2** | 19,078 | **4.7** |
| **5** | 12,526 | **4.5** |
| **10** | 9,033 | **4.3** |
| **25** | 4,263 | **4.0** |
| **50** | 1,660 | **3.5** |
| **100** | 783 | **3.2** |
| **250** | 229 | **2.6** |
| **500** | 149 | **2.4** |
| **1,000** | 86 | **2.2** |
| **2,000** | 27 | **1.6** |
| **3,000** | 12 | **1.3** |
| **4,000** | 6 | **0.9** |
| **5,000** | 3 | **0.6** |

---

### 2. Log-Log Polynomial Best-Fit Model

For programmatic evaluation, a 4th-degree polynomial in log-log space provides an accurate fit ($R^2 = 0.9944$, $\text{MSE} = 0.012$):

$$\ln(\hat{f}) = a_4 x^4 + a_3 x^3 + a_2 x^2 + a_1 x + a_0$$

where $x = \ln(r)$, and the fitted coefficients are:

| Coefficient | Best-Fit Value |
|:---:|:---:|
| $a_4$ | `np.float64(-0.01312373)` |
| $a_3$ | `np.float64(0.23288160)` |
| $a_2$ | `np.float64(-1.39872769)` |
| $a_1$ | `np.float64(2.14802785)` |
| $a_0$ | `np.float64(9.40474351)` |

$$\hat{f}(r) = \exp\left(\sum_{k=0}^{4} a_k (\ln r)^k\right)$$

---

### 3. Frequency Score Formula ($5.0 \to 0.1$)

To compute a normalized frequency score ranging from `5.0` (most frequent) down to `0.1` (least frequent) in discrete multiples of `0.1`:

$$s(r) = \operatorname{round}\left(0.1 + \left(\frac{\ln(\hat{f}) - \ln(f_{\min})}{\ln(f_{\max}) - \ln(f_{\min})}\right) \times 4.9,\ 1\right)$$

where $\ln(f_{\max}) = \ln(38292) \approx 10.553$ and $\ln(f_{\min}) = \ln(1) = 0$.

#### Python Implementation

```python
import numpy as np

COEFFS = [-0.01312373, 0.23288160, -1.39872769, 2.14802785, 9.40474351]
LN_F_MAX = 10.55299  # ln(38292)
LN_F_MIN = 0.0       # ln(1)

def get_approx_freq(rank: int) -> float:
    ln_r = np.log(float(rank))
    ln_f = np.polyval(COEFFS, ln_r)
    return float(np.exp(ln_f))

def get_freq_score(rank: int) -> float:
    ln_f = np.log(max(get_approx_freq(rank), 1.0))
    raw = 0.1 + ((ln_f - LN_F_MIN) / (LN_F_MAX - LN_F_MIN)) * 4.9
    return max(0.1, min(5.0, round(round(raw * 10) / 10, 1)))
```

---

## Validation

To verify the integrity, schema conformance, and single-token constraints of [`vocab.json`](file:///home/zenhome/Projects/hindi-vocab/vocab.json):

```bash
python3 scripts/validate_vocab.py
```
