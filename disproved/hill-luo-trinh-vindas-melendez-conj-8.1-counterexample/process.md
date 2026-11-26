# Research Process Summary (Hill–Luo–Trinh–Vindas-Meléndez Conjecture 8.1)

## Path to the Counterexamples

1. **Exhaustive symbolic checks in low dimensions (negative results):** Exact multivariate polynomial interpolation in shifted parameters $x_i = b_i - 1$ verified symbolic magic positivity for all admissible positive integer vectors $\mathbf{b} \in \mathbb{Z}_{>0}^n$ across dimensions $3 \le n \le 10$ (352,716 nonzero symbolic terms in $n = 10$, while correctly detecting the $n = 2$ exception $PF_2$).

2. **Geometric reformulation and mixed-volume analysis:** Translating $\mathfrak{X}_n(\mathbf{b})$ by $-\mathbf{1}$ yielded the polymatroid Minkowski decomposition $P(\mathbf{x}) = P_0 + \sum_{r=1}^n x_r U_{n-r+1}$. Khovanskii–Pukhlikov Todd-operator analysis established positivity of the top three parameter-degree layers $|\alpha| \ge n - 2$, pushing any potential counterexample toward lower $y$-degrees (such as $y^2$ and $y^3$) in higher dimension.

3. **Discovery of negative mixed coefficients and Ehrhart-negative Minkowski sum:** Searching aggregate mixed weights uncovered a negative mixed cubic coefficient $[x_7 x_{11} x_{12} y^3] M_{14} = -125057/450 < 0$ (via $a U_3 + b U_4 + c U_8 \subset \mathbb{R}^{14}$), and reducing to two uniform-matroid independence polytopes isolated the Ehrhart-negative sum $Q = U_5 + U_9 \subset \mathbb{R}^{14}$ with $[t^2]\mathrm{ehr}_Q(t) = -36952721/3880800 < 0$.

4. **Explicit refutation and sharper certificates:** Evaluating along the ray $\mathbf{b}(m) = (1^5, 1+m, 1^3, 1+m, 1^4)$ yielded the exact quadratic $\mu_2(m)$ turning negative at $m = 286$ ($\mu_2 = -8337823/11025 < 0$). Further analysis using the closed-form $e_1, e_2$ formulas derived from Theorem 5.9 produced Ehrhart-negative examples in $n = 14$ ($m = 317$), unequal minimal-entry examples ($\max b_i = 228$ for $\mu_2 < 0$, $253$ for $e_2 < 0$), a $\{1, 3\}$-vector in $n = 18$, a binary $\{1, 2\}$-vector in $n = 20$, and the earlier $n = 13$ multivariate negative coefficient $[x_6 x_{10} y^2] M_{13} = -842231/69300 < 0$.

## Verification

All rational certificates are independently verified with zero floating-point arithmetic by `verify.py` (Python 3 standard library only), cross-checking exact integer dynamic programming from the defining inequalities (Theorem 2.2) plus Newton interpolation against the closed-form draconian evaluation of Theorem 5.9.
