# Ehrhart and Magic Positivity

This repository contains two mathematical preprints, their LaTeX sources, and standalone exact-arithmetic verifiers.

## Generalized parking-function polytopes

A dimension-14 example has a negative second magic coefficient and refutes Conjecture 8.1 of Hill, Luo, Trinh, and Vindas-Meléndez. Another dimension-14 example has a negative second Ehrhart coefficient. The paper gives exact thresholds for these two sign failures in a specified two-parameter family and a binary example in dimension 20.

[Manuscript (PDF)](disproved/hill-luo-trinh-vindas-melendez-conj-8.1-counterexample/paper.pdf) · [LaTeX](disproved/hill-luo-trinh-vindas-melendez-conj-8.1-counterexample/paper.tex) · [Project and verifier](disproved/hill-luo-trinh-vindas-melendez-conj-8.1-counterexample/) · [Original conjecture](https://arxiv.org/abs/2607.15503v1) · [aiXiv:2611.03093](https://aixiv.online/abs/2611.03093)

## Preorder polytopes

A signed Vandermonde identity on order filters gives a cancellation-free expansion proving Conjecture 4.8 of Athanasiadis and Chapoton. The same formula recovers double Ehrhart reciprocity, and their previously established implications yield the corresponding word-descent and zeta identities.

[Manuscript (PDF)](proofs/athanasiadis-chapoton-conj-4.8-proof/paper.pdf) · [LaTeX](proofs/athanasiadis-chapoton-conj-4.8-proof/paper.tex) · [Project and verifier](proofs/athanasiadis-chapoton-conj-4.8-proof/) · [Original conjecture](https://arxiv.org/abs/2605.26916v1)

## Reproduce the computations

Use Python 3.10 or later with assertions enabled. Both verifiers use only the standard library.

```sh
python3 disproved/hill-luo-trinh-vindas-melendez-conj-8.1-counterexample/verify.py
python3 proofs/athanasiadis-chapoton-conj-4.8-proof/verify.py
```

Both full runs end with `ALL CHECKS PASSED`. The [verification report](VERIFICATION.md) gives exact expected values, coverage, runtimes, and limits. Each manuscript links to the immutable commit containing the corresponding verifier.

The [parking-function research log](disproved/hill-luo-trinh-vindas-melendez-conj-8.1-counterexample/process.md) and [preorder research log](proofs/athanasiadis-chapoton-conj-4.8-proof/process.md) describe the AI work and Edwin Chan’s role. The manuscripts are unrefereed and have no Lean certification. See [review response](REVIEW_RESPONSE.md) for the mathematical and bibliographic changes and [aiXiv preparation](AIXIV.md) for the submission metadata.
