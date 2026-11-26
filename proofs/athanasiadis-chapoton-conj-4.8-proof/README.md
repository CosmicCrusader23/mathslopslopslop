# Magic positivity of preorder polytopes

The paper proves Conjecture 4.8 of Christos A. Athanasiadis and Frédéric Chapoton. A signed Vandermonde identity gives a formula for the double Ehrhart polynomial and a cancellation-free formula for the magic coefficients. The paper recovers double reciprocity and applies the original authors’ implications for the word-descent and zeta identities.

[Manuscript (PDF)](paper.pdf) · [LaTeX](paper.tex) · [Original conjecture](https://arxiv.org/abs/2605.26916v1)

## Reproduce

From this directory, run `python3 verify.py` with Python 3.10 or later. The verifier checks formal identities in bounded degree, compares polynomial formulas with exact lattice counts on selected preorders, and checks the stated examples, including the polynomials and real-root counts for Patel’s poset.

[Exact verifier](verify.py) · [Coverage and expected output](../../VERIFICATION.md#preorder-polytopes)

## Research record

Gemini 4 Neon developed the signed Vandermonde proof and wrote the original manuscript and verifier. GPT-6.2 independently investigated the conjecture and derived a related cancellation-free formula. Edwin Chan selected the problem, prompted the systems, and coordinated the work.

[Research log](process.md) · [aiXiv metadata](aixiv.json)
