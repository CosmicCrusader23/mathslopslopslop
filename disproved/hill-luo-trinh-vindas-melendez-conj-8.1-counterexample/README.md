# Counterexamples to magic positivity of parking-function polytopes

The paper refutes Conjecture 8.1 of Charlie Hill, Ambrose Luo, Vu Trinh, and Andrés R. Vindas-Meléndez. In dimension 14 the stated examples have second coefficients μ₂ = −8337823/11025 and e₂ = −777669659/3880800, respectively. In the family with shifts at positions 6 and 10, the smallest possible largest entries for μ₂ < 0 and e₂ < 0 are 228 and 253.

[Manuscript (PDF)](paper.pdf) · [LaTeX](paper.tex) · [Original conjecture](https://arxiv.org/abs/2607.15503v1) · [aiXiv:2611.03093](https://aixiv.online/abs/2611.03093)

## Reproduce

From this directory, run `python3 verify.py` with Python 3.10 or later. The full run asserts all six table rows, the two finite-search thresholds, the coefficient of the uniform-matroid sum, and both mixed multivariate coefficients. It also counts lattice points directly for the dimension-18 and dimension-20 examples. The optional `--skip-large-direct` flag skips just those two counts and labels the run accordingly.

[Exact verifier](verify.py) · [Coverage and expected output](../../VERIFICATION.md#parking-function-polytopes)

## Research record

GPT-6.2 Sol found the headline counterexample and the negative mixed cubic coefficient. Gemini 4 Neon derived the low-degree formulas, found further examples, and prepared the original manuscript and verifier. Edwin Chan selected the problem, prompted the systems, and coordinated the work.

[Research log](process.md) · [aiXiv metadata](aixiv.json) · [Proposed v2 changelog](changelog-v2.txt)
