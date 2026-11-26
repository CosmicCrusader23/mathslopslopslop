# Resolved Conjectures in Ehrhart Theory and Magic Positivity

This repository contains **AI-authored** LaTeX manuscripts (`paper.tex`), compiled PDFs (`paper.pdf`), research process notes (`process.md`), and standalone exact-arithmetic Python verifiers (`verify.py`, standard library only) for two resolved conjectures on the magic positivity of generalized permutohedra.

**Authorship & Attribution:** All mathematical discoveries, proofs, verification scripts, and manuscripts in this repository were produced end to end by AI agents as credited in each paper. **Edwin Chan** served solely as the human submitter and research coordinator (selecting target conjectures, prompting and coordinating the agents, reviewing outputs, and managing publication).

| Status | Target Conjecture | Research Authors (AI) | Manuscript (PDF / TeX) | Exact Verifier |
| --- | --- | --- | --- | --- |
| **Disproved** | Hill–Luo–Trinh–Vindas-Meléndez Conjecture 8.1 ([`arXiv:2607.15503`](https://arxiv.org/abs/2607.15503)) | ChatGPT (OpenAI), Google Antigravity (Google DeepMind) | [`paper.pdf`](disproved/hill-luo-trinh-vindas-melendez-conj-8.1-counterexample/paper.pdf) · [`paper.tex`](disproved/hill-luo-trinh-vindas-melendez-conj-8.1-counterexample/paper.tex) | [`verify.py`](disproved/hill-luo-trinh-vindas-melendez-conj-8.1-counterexample/verify.py) |
| **Proved** | Athanasiadis–Chapoton Conjecture 4.8, plus Conjectures 7.2, 4.4, and 4.9 Eq. (22) ([`arXiv:2605.26916`](https://arxiv.org/abs/2605.26916)) | Google Antigravity (Google DeepMind) | [`paper.pdf`](proofs/athanasiadis-chapoton-conj-4.8-proof/paper.pdf) · [`paper.tex`](proofs/athanasiadis-chapoton-conj-4.8-proof/paper.tex) | [`verify.py`](proofs/athanasiadis-chapoton-conj-4.8-proof/verify.py) |

## Verification

Run both standalone exact verifiers (Python 3 standard library only):

```bash
python3 disproved/hill-luo-trinh-vindas-melendez-conj-8.1-counterexample/verify.py
python3 proofs/athanasiadis-chapoton-conj-4.8-proof/verify.py
```
