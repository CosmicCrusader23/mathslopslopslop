# Research Process Summary (Athanasiadis–Chapoton Conjecture 4.8)

## Path to the Proof

1. **Adversarial search for a counterexample (negative results):** Starting from Theorem 1.5(a) of `arXiv:2605.26916`, we initially searched for counterexamples to Conjecture 4.8 across structured preorder families: stars $\mathrm{Star}_{\mathrm{up}}(1; 1^k)$ up to $k = 160$, asymmetric equivalence-class blowups of stars, trees, chains, $K_{a,b}$, crowns $C_{2k}$, zig-zag posets $Z_n$, incidence posets (Fano plane, $K_{m,m}-M$, Boolean lattices), 3,376 random preorders with hill-climbing optimization, and the 8-element height-2 counterexample $P_3$ to Conjecture 5.3 together with its infinite family $P_k$ and asymmetric blowups. Every tested preorder was strictly magic positive.

2. **Sharpness comparison with non-transitive $Y$-type polytopes:** Dropping transitivity while preserving the matching condition $e \in I_e$ immediately produced magic-positivity failures at $n = 6$ ($c_5 = -1/6 < 0$) and $n = 7$ ($c_6 = -3/10 < 0$). Analyzing the derivative at $t = -1$ proved $c_{n-1} = \#\{e \in E : \mathcal{U}(e) = E\}/n \ge 0$ unconditionally for preorders, isolating transitivity (additivity of $f(F) = |F|$ on the order-filter lattice) as the mechanism enforcing positivity.

3. **Exact generating-function insight ($\mathrm{Star}_{\mathrm{up}}$ to general preorders):** Proving magic positivity for $\mathrm{Star}_{\mathrm{up}}(1;1^k)$ via the substitution $t+1 = 1/(1-y)$ uncovered the strictly positive formal power series $\Phi(w, y) = \exp\bigl(\sum_{m \ge 2} \frac{w^m}{m}(y + \dots + y^{m-1})\bigr)$. Expanding Theorem 1.5(a) in products of $\phi_{k_e}(y)$ produced coefficients $D_\tau(\mathbf{k}; y)$ that empirically evaluated identically to $1$ for every $\mathbf{k} \in P_{\tau^*}$ with $k_e \ne 1$.

4. **Proof of the Distributive-Lattice Vandermonde Theorem:** Rewriting $1 - k_e = w_e \in \mathbb{Z}$ reduced $D_\tau(\mathbf{k}; y) \equiv 1$ to a general Vandermonde identity on the distributive lattice $\mathcal{F}(\tau)$, which we proved cleanly via modularity of the surplus function $\Delta_{\mathbf{b}}$, unique minimum maximizers $H^*_F(\mathbf{b})$, decoupled factorization, and strong induction on $|F|$. The same identity immediately yielded the bivariate Master Formula for $\mathbb{E}_\tau(u, v)$, proving Conjectures 4.8, 7.2, 4.4, and Equation (22) of Conjecture 4.9 simultaneously.

## Verification

All identities, the inductive lemma $A_F(r) = 0$ on 120 random posets and non-poset preorders with signed integer weights, direct lattice-point counts $\#(m\mathcal{Q}_\tau \cap \mathbb{Z}^n)$ plus Lagrange interpolation vs. Theorem 1.5(a), Theorem 2 (Master Formula), Conjecture 4.4 word-descent enumeration, Conjecture 7.2 reciprocity, Conjecture 4.9 Eq. (22), the $P_3$ example, and the $n = 6$ non-transitive sharpness control are independently verified in exact rational arithmetic by `verify.py` (Python 3 standard library only).
