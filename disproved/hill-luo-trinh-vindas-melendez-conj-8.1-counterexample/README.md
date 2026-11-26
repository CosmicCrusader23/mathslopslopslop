# Counterexamples to Hill–Luo–Trinh–Vindas-Meléndez Conjecture 8.1

**Paper:** Charlie Hill, Ambrose Luo, Vu Trinh, and Andrés R. Vindas-Meléndez, *"Lattice slices, Ehrhart polynomials, and magic positivity of generalized parking-function polytopes"*, [`arXiv:2607.15503`](https://arxiv.org/abs/2607.15503) (July 2026).

**Status:** **DISPROVED** (explicit exact counterexamples in dimensions $n = 14, 18, 20$, including a counterexample to Ehrhart positivity itself in $n = 14$ and a binary $\{1, 2\}$-parameter counterexample in $n = 20$).

---

## Conjecture Statement

For a positive integer vector $\mathbf{b} = (b_1, \dots, b_n) \in \mathbb{Z}_{>0}^n$, let $S_j = \sum_{r=1}^j b_r$ and $\Sigma_k = \sum_{j = n - k + 1}^n S_j$. By Theorem 2.2 of `arXiv:2607.15503` (citing `[BBCDDDLMMNV, Theorem 2.3(c)]`), the generalized parking-function polytope $\mathfrak{X}_n(\mathbf{b}) \subset \mathbb{R}^n$ is defined by
$$x_i \ge 1 \quad (1 \le i \le n), \qquad \sum_{i \in I} x_i \le \Sigma_{|I|} \quad (\emptyset \ne I \subseteq \{1, \dots, n\}).$$
Writing the Ehrhart polynomial in the standard and magic bases,
$$\operatorname{ehr}_{\mathfrak{X}_n(\mathbf{b})}(t) = \sum_{i=0}^n e_i\, t^i = \sum_{i=0}^n \mu_i\, t^i (t + 1)^{n - i},$$
we say $\mathfrak{X}_n(\mathbf{b})$ is *Ehrhart positive* if $e_i \ge 0$ for all $i$, and *magic positive* if $\mu_i \ge 0$ for all $i$. In particular,
$$\mu_2 = e_2 - (n - 1)\, e_1 + \binom{n}{2}.$$

**Conjecture 8.1 (`conj:magicgeneral`, `arXiv:2607.15503`):** *For every $n \ge 3$ and every $\mathbf{b} \in \mathbb{Z}_{>0}^n$, the polytope $\mathfrak{X}_n(\mathbf{b})$ is magic positive.*

---

## Main Counterexample ($n = 14$)

Take $n = 14$ and
$$\mathbf{b} = (1, 1, 1, 1, 1, 287, 1, 1, 1, 287, 1, 1, 1, 1).$$
Then the exact second magic coefficient of $\operatorname{ehr}_{\mathfrak{X}_{14}(\mathbf{b})}(t)$ is
$$\mu_2 = -\frac{8337823}{11025} \approx -756.2651 < 0,$$
**refuting Conjecture 8.1.**

### Geometric Mechanism and Exact Quadratic Family

Translating $\mathfrak{X}_n(\mathbf{b})$ by $-\mathbf{1}$ and setting $x_i = b_i - 1 \ge 0$, Theorem 2.2 yields the Minkowski decomposition
$$P(\mathbf{x}) := \mathfrak{X}_n(\mathbf{b}) - \mathbf{1} = P_0 + \sum_{i=1}^n x_i\, U_{n - i + 1},$$
where $P_0 = \mathfrak{X}_n(1, \dots, 1) - \mathbf{1}$ is the shifted classical parking-function polytope and $U_r = \{z \in [0, 1]^n : \sum_{j=1}^n z_j \le r\}$ is the $r$-th uniform-matroid independence polytope.

Along the one-parameter ray $\mathbf{b}(m) = (1^5, 1 + m, 1^3, 1 + m, 1^4)$ (so $x_6 = x_{10} = m$ and all other $x_i = 0$),
$$P(\mathbf{x}(m)) = P_0 + m(U_5 + U_9) \subset \mathbb{R}^{14}.$$
The polytope $Q = U_5 + U_9 \subset \mathbb{R}^{14}$ is itself **Ehrhart negative**: direct exact lattice-point counting of $\#(tQ \cap \mathbb{Z}^{14})$ for $t = 0, \dots, 14$ and Newton interpolation yield
$$[t^2]\operatorname{ehr}_{U_5 + U_9}(t) = -\frac{36952721}{3880800} \approx -9.52193 < 0.$$

By parameter polynomiality (Proposition 5.4 / Corollary 5.6 and Theorem 5.9 of `arXiv:2607.15503`), the coefficient $\mu_2(m)$ of $t^2(t+1)^{12}$ in $\operatorname{ehr}_{\mathfrak{X}_{14}(\mathbf{b}(m))}(t)$ is a polynomial in $m$ of degree at most $2$, with leading coefficient $[t^2]\operatorname{ehr}_{U_5 + U_9}(t)$. Computing $\operatorname{ehr}_{\mathfrak{X}_{14}(\mathbf{b}(m))}(t)$ by **direct lattice-point enumeration** from Theorem 2.2 for $m \in \{0, 1, 2\}$ ($t = 0, \dots, 14$) gives:

| $m$ | $\mu_2(m)$ (Direct lattice counting $=$ Theorem 5.9) |
| --- | --- |
| $0$ | $\dfrac{29211}{4}$ |
| $1$ | $\dfrac{38762683049}{3880800}$ |
| $2$ | $\dfrac{2046289519}{161700}$ |

Interpolating this degree-2 polynomial uniquely determines the exact formula for all $m \in \mathbb{Z}_{\ge 0}$:
$$\mu_2(m) = -\frac{36952721}{3880800}\, m^2 + \frac{149416051}{55440}\, m + \frac{29211}{4} = \frac{-36952721\, m^2 + 10459123570\, m + 28340512200}{3880800}.$$
Evaluating at $m = 285$ and $m = 286$ (and independently checking directly via the closed-form draconian expansion of Theorem 5.9):
- $m = 285$: $\mu_2(285) = \dfrac{102746219}{51744} \approx +1985.66 > 0$,
- $m = 286$: $\mu_2(286) = -\dfrac{8337823}{11025} \approx -756.27 < 0$.

Thus $m = 286$ ($\mathbf{b} = (1^5, 287, 1^3, 287, 1^4)$) is the smallest integer on this ray violating Conjecture 8.1.

---

## Stronger and Sharper Counterexamples

All of the following certificates are verified in exact rational arithmetic by `verify.py`:

| Dimension $n$ | Parameter vector $\mathbf{b}$ | $e_2$ | $\mu_2$ | Significance |
| --- | --- | --- | --- | --- |
| $14$ | $(1^5, 287, 1^3, 287, 1^4)$ | $> 0$ | $-\dfrac{8337823}{11025} \approx -756.27$ | Equal-weight magic-positivity counterexample |
| $14$ | $(1^5, 318, 1^3, 318, 1^4)$ | $-\dfrac{777669659}{3880800} \approx -200.39$ | $-\dfrac{11195736263}{117600} \approx -95201.84$ | Fails **Ehrhart positivity** itself ($e_2 < 0$) |
| $14$ | $(1^5, 187, 1^3, 228, 1^4)$ | $\dfrac{3101451036227}{50450400} \approx +61475.25$ | $-\dfrac{10491632153}{50450400} \approx -207.96$ | Minimal $\max b_i = 228$ in $n = 14$ for $\mu_2 < 0$ |
| $14$ | $(1^5, 208, 1^3, 253, 1^4)$ | $-\dfrac{5255462383}{5605600} \approx -937.54$ | $-\dfrac{35322635893}{509600} \approx -69314.43$ | Minimal $\max b_i = 253$ in $n = 14$ for $e_2 < 0$ |
| $18$ | $(1^6, 3, 1^5, 3, 1^5)$ | $\dfrac{22435315633}{6306300} \approx +3557.60$ | $-\dfrac{3708081001}{3153150} \approx -1175.99$ | Small-entry $\{1, 3\}$-vector with $e_2 > 0$, $\mu_2 < 0$ |
| $20$ | $(1^7, 2, 1^5, 2, 1^6)$ | $-\dfrac{10007742397957}{908107200} \approx -11020.44$ | $-\dfrac{260316261282989}{15437822400} \approx -16862.24$ | **Binary $\{1, 2\}$-vector** failing both $e_2 \ge 0$ and $\mu_2 \ge 0$ |

### Auxiliary Multivariate Certificates

For the shifted multivariate magic polynomial $M_n(\mathbf{x}, y) = (1 - y)^n \operatorname{ehr}_{P(\mathbf{x})}\!\bigl(\frac{y}{1 - y}\bigr)$ (where $x_i = b_i - 1$):
- **Dimension $n = 13$:** The mixed quadratic coefficient is already strictly negative,
  $$[x_6 x_{10} y^2] M_{13} = [t^2]\bigl(\operatorname{ehr}_{U_4 + U_8} - \operatorname{ehr}_{U_4} - \operatorname{ehr}_{U_8}\bigr) = -\frac{842231}{69300} < 0.$$
- **Dimension $n = 14$:** The mixed cubic coefficient satisfies
  $$[x_7 x_{11} x_{12} y^3] M_{14} = [abc]\,\#\bigl((a U_3 + b U_4 + c U_8) \cap \mathbb{Z}^{14}\bigr) = -\frac{125057}{450} < 0.$$

---

## Independent Verification

Run the standalone exact rational verifier (Python 3 standard library only, no external dependencies):

```bash
python3 verify.py
```

`verify.py` cross-checks:
1. Sanity checks against published examples in `arXiv:2607.15503` (Examples 4.2, 5.2, 5.12).
2. Direct lattice-point enumeration via exact integer dynamic programming from Theorem 2.2 for $Q = U_5 + U_9 \subset \mathbb{R}^{14}$, $a U_3 + b U_4 + c U_8 \subset \mathbb{R}^{14}$, $U_4 + U_8 \subset \mathbb{R}^{13}$, and the $n = 14$ family $\mathbf{b}(m)$ at $m = 0, 1, 2$.
3. Exact agreement between direct lattice-point interpolation and the independent closed-form draconian evaluation of Theorem 5.9 for all counterexamples in $n = 14, 18, 20$.

---

*Paper source retrieved via arXiv (`https://arxiv.org/abs/2607.15503`); subject to arXiv Terms of Use (`https://info.arxiv.org/help/api/index.html`) and the paper's individual arXiv license.*
