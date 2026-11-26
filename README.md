# Resolved Conjectures in Ehrhart Theory and Magic Positivity

This repository contains complete mathematical write-ups and standalone exact-arithmetic Python verifiers (standard library only, zero floating-point arithmetic) for two conjectures on the magic positivity of generalized permutohedra.

| Status | Target Conjecture | Paper | Directory |
| --- | --- | --- | --- |
| **Disproved** | Magic positivity of generalized parking-function polytopes $\mathfrak{X}_n(\mathbf{b})$ for $n \ge 3$ (**Conjecture 8.1**) | Hill, Luo, Trinh, Vindas-Meléndez ([`arXiv:2607.15503`](https://arxiv.org/abs/2607.15503)) | [`disproved/hill-luo-trinh-vindas-melendez-conj-8.1-counterexample/`](disproved/hill-luo-trinh-vindas-melendez-conj-8.1-counterexample/README.md) |
| **Proved** | Magic positivity of preorder polytopes $\mathcal{Q}_\tau$ (**Conjecture 4.8**), plus **Conjectures 7.2, 4.4, and 4.9 Eq. (16)** | Athanasiadis, Chapoton ([`arXiv:2605.26916`](https://arxiv.org/abs/2605.26916)) | [`proofs/athanasiadis-chapoton-conj-4.8-proof/`](proofs/athanasiadis-chapoton-conj-4.8-proof/README.md) |

## Highlights

- **Disproved (`arXiv:2607.15503`, Conjecture 8.1):**
  - In dimension $n = 14$, $\mathbf{b} = (1^5, 287, 1^3, 287, 1^4)$ has second magic coefficient $\mu_2 = -\frac{8337823}{11025} < 0$, driven by the Ehrhart-negative Minkowski sum $U_5 + U_9 \subset \mathbb{R}^{14}$ ($[t^2]\operatorname{ehr}_{U_5+U_9}(t) = -\frac{36952721}{3880800} < 0$).
  - Further exact certificates include Ehrhart negativity at $n = 14$ ($\mathbf{b} = (1^5, 318, 1^3, 318, 1^4)$), unequal minimal-entry counterexamples ($\max b_i = 228$), and a binary $\{1, 2\}$-parameter counterexample in $n = 20$ ($\mathbf{b} = (1^7, 2, 1^5, 2, 1^6)$).
- **Proved (`arXiv:2605.26916`, Conjectures 4.8, 7.2, 4.4, and 4.9 Eq. (16)):**
  - A **Distributive-Lattice Vandermonde Theorem** on the order-filter lattice $\mathcal{F}(\tau)$ yields a closed-form Master Formula for the double Ehrhart polynomial $\mathbb{E}_\tau(u, v)$, which simultaneously proves magic positivity (with $n!\, M_\tau(y) \in \mathbb{Z}_{\ge 0}[y]$), real-rootedness of $h^*(\mathcal{Q}_\tau, t)$, double Ehrhart reciprocity, the word-descent formula for $h^*$, and $\mathcal{Z}(P_\tau, -1) = (-1)^n \#\operatorname{Max}(P_\tau)$.
  - A 6-element non-transitive matched $Y$-type generalized permutohedron ($c_5 = -1/6 < 0$) confirms that transitivity is essential.

## Verification

Run both standalone exact verifiers (Python 3 standard library only):

```bash
python3 disproved/hill-luo-trinh-vindas-melendez-conj-8.1-counterexample/verify.py
python3 proofs/athanasiadis-chapoton-conj-4.8-proof/verify.py
```
