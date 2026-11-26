# Resolved Conjectures in Ehrhart Theory and Magic Positivity

This repository contains **AI-authored** `amsart` LaTeX manuscripts (`paper.tex`), compiled PDFs (`paper.pdf`), research process notes (`process.md`), and standalone exact-arithmetic Python verifiers (`verify.py`, standard library only) for two resolved conjectures on the magic positivity of generalized permutohedra.

**AI-Authorship & Review Notice:** Both manuscripts are explicitly classified as **AI-authored**. All mathematical discoveries, proofs, verification code, and LaTeX writing were produced by AI systems (**GPT-6.2 Sol** via ChatGPT and **Gemini 4 Neon** via Google Antigravity). **Edwin Chan** is listed as sole human author solely per archival submission conventions; his contribution was limited to problem selection, prompting, and research coordination. Neither manuscript has undergone independent human peer review or formal Lean certification, and neither represents official research conducted or endorsed by OpenAI or Google DeepMind.

| Status | Target Conjecture | AI Systems Credited | Manuscript (PDF / TeX) | Exact Verifier |
| --- | --- | --- | --- | --- |
| **Disproved** | Hill–Luo–Trinh–Vindas-Meléndez Conjecture 8.1 ([`arXiv:2607.15503`](https://arxiv.org/abs/2607.15503)) | GPT-6.2 Sol (ChatGPT), Gemini 4 Neon (Google Antigravity) | [`paper.pdf`](disproved/hill-luo-trinh-vindas-melendez-conj-8.1-counterexample/paper.pdf) · [`paper.tex`](disproved/hill-luo-trinh-vindas-melendez-conj-8.1-counterexample/paper.tex) | [`verify.py`](disproved/hill-luo-trinh-vindas-melendez-conj-8.1-counterexample/verify.py) |
| **Proved** | Athanasiadis–Chapoton Conjecture 4.8 (plus alternative proofs of Conjectures 7.2, 4.4, and 4.9 Eq. (22); [`arXiv:2605.26916`](https://arxiv.org/abs/2605.26916)) | Gemini 4 Neon (Google Antigravity) | [`paper.pdf`](proofs/athanasiadis-chapoton-conj-4.8-proof/paper.pdf) · [`paper.tex`](proofs/athanasiadis-chapoton-conj-4.8-proof/paper.tex) | [`verify.py`](proofs/athanasiadis-chapoton-conj-4.8-proof/verify.py) |

## Verification

Run both standalone exact verifiers (Python 3 standard library only):

```bash
python3 disproved/hill-luo-trinh-vindas-melendez-conj-8.1-counterexample/verify.py
python3 proofs/athanasiadis-chapoton-conj-4.8-proof/verify.py
```
