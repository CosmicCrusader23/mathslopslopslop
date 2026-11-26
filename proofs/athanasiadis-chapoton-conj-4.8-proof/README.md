# Proof of Athanasiadis–Chapoton Conjecture 4.8 (and Conjectures 7.2, 4.4, and 4.9 Eq. (16))

**Paper:** Christos A. Athanasiadis and Frédéric Chapoton, *"Polytopes and posets associated to preorders"*, [`arXiv:2605.26916`](https://arxiv.org/abs/2605.26916) (May 2026).

**Status:** **PROVED** (unconditionally, for every finite preorder $\tau$).

---

## Summary of Results

Using only Theorem 1.5(a) and Proposition 7.1 (Equation (17)) already proved in `arXiv:2605.26916`, we establish a single closed-form expansion for the double Ehrhart polynomial $\mathbb{E}_\tau(u, v)$ of any finite preorder $\tau$ on an $n$-element set $E$:

$$\mathbb{E}_\tau(u, v) = \sum_{\substack{\mathbf{k} \in P_{\tau^*} \\ k_e \ne 1 \;\forall e \in E}} P\bigl(n - |\mathbf{k}|;\, u, v\bigr) \prod_{e \in E} \psi_{k_e}(u),$$

where $P(W; u, v) = \sum_{m=0}^{W} \binom{W}{m}\binom{v + W - m}{W - m} u^m$ and $\Psi(w, u) = \sum_{k \ge 0} \psi_k(u) w^k = \exp\!\left(\sum_{m \ge 2} \frac{w^m}{m}\sum_{r=1}^{m-1} u^r(1+u)^{m-r}\right)$.

From this single Master Formula, **four open conjectures** of `arXiv:2605.26916` follow immediately:

1. **Conjecture 4.8 (`conj:magic`):** The Ehrhart polynomial $\operatorname{Ehr}(\mathcal{Q}_\tau, t)$ is **magic positive** for every finite preorder $\tau$ — with explicit nonnegative expansion
   $$M_\tau(y) := (1 - y)^n \operatorname{Ehr}\!\left(\mathcal{Q}_\tau, \frac{y}{1 - y}\right) = \sum_{\substack{\mathbf{k} \in P_{\tau^*} \\ k_e \ne 1 \;\forall e \in E}} \prod_{e \in E} \phi_{k_e}(y) \in \mathbb{Q}_{\ge 0}[y],$$
   and in fact $n!\, M_\tau(y) \in \mathbb{Z}_{\ge 0}[y]$. By Brändén's theorem (`[Bra06, Theorem 4.2]`), it follows that $h^*(\mathcal{Q}_\tau, t)$ has only real roots.
2. **Conjecture 7.2 (`conj:double`):** $\mathbb{E}_\tau(-u, -v) = (-1)^n \mathbb{E}_\tau(u - 1, v - 1)$ for every finite preorder $\tau$ of size $n$.
3. **Conjecture 4.4 (`conj:h-ast`):** $h^*(\mathcal{Q}_\tau, t) = \sum_{w \in \mathcal{W}_\tau} t^{n - 1 - \operatorname{des}(w)}$ for every finite preorder $\tau$ on a totally ordered $n$-element set $E$.
4. **Conjecture 4.9, Equation (16) (`conj:zeta`):** $\mathcal{Z}(P_\tau, -1) = (-1)^n \#\operatorname{Max}(P_\tau)$ for every finite preorder $\tau$ of size $n$.

---

## Setup and Notation

Let $\tau$ be a finite preorder (reflexive, transitive binary relation) on an $n$-element set $E$, and let $\mathcal{F}(\tau)$ be the finite distributive lattice of all **order filters** (upward-closed subsets) of $\tau$, ordered by inclusion. Note that $\emptyset, E \in \mathcal{F}(\tau)$ and $\mathcal{F}(\tau)$ is closed under $\cup$ and $\cap$.

By definition, the preorder polytope is
$$\mathcal{Q}_\tau = \left\{ \mathbf{x} \in \mathbb{R}_{\ge 0}^E : \sum_{e \in \mathcal{I}} x_e \le |\mathcal{I}| \;\text{ for every order ideal } \mathcal{I} \text{ of } \tau \right\},$$
and the set of lattice points of the dual preorder polytope $\mathcal{Q}_{\tau^*}$ is
$$P_{\tau^*} = \left\{ \mathbf{a} \in \mathbb{N}^E : \sum_{e \in F} a_e \le |F| \;\text{ for every } F \in \mathcal{F}(\tau) \right\}.$$
For $r, s \in \mathbb{N}$, set $\mathcal{Q}_\tau(r, s) = r\mathcal{Q}_\tau + s\boldsymbol{\Delta}_E$. By Lemma 4.1, Theorem 1.5(a), and Proposition 7.1 (Equation (17)) of `arXiv:2605.26916`, the double Ehrhart polynomial $\mathbb{E}_\tau(u, v)$ (satisfying $\mathbb{E}_\tau(r, s) = \#(\mathcal{Q}_\tau(r, s) \cap \mathbb{Z}^E)$) is given by
$$\mathbb{E}_\tau(u, v) = \sum_{\mathbf{a} \in P_{\tau^*}} \binom{v + n - |\mathbf{a}|}{n - |\mathbf{a}|} \prod_{e \in E} \binom{u + a_e - 1}{a_e}, \qquad \operatorname{Ehr}(\mathcal{Q}_\tau, u) = \mathbb{E}_\tau(u, 0).$$

---

## Complete Proof

### 1. Distributive-Lattice Vandermonde Theorem

**Theorem 1.** *Let $\tau$ be a finite preorder on $E$, and let $\mathbf{w} = (w_e)_{e \in E} \in \mathbb{Z}^E$ be any integer vector such that $W_F := \sum_{e \in F} w_e \ge 0$ for every $F \in \mathcal{F}(\tau)$. Then for every integer $m \ge 0$,*
$$S(\tau, \mathbf{w}, m) := \sum_{\substack{\mathbf{b} \in \mathbb{N}^E, \; |\mathbf{b}| = m \\ \sum_{e \in F} b_e \le W_F \;\forall F \in \mathcal{F}(\tau)}} \prod_{e \in E} \binom{w_e}{b_e} = \binom{W_E}{m}.$$

*Proof.* For any $F \in \mathcal{F}(\tau)$ and any $\mathbf{b} \in \mathbb{N}^F$, define the surplus function
$$\Delta_{\mathbf{b}}(L) := \sum_{e \in L} (b_e - w_e), \qquad L \in \mathcal{F}(\tau|_F).$$
Because $F$ is upward-closed in $\tau$, a subset $L \subseteq F$ is an order filter of the restricted preorder $\tau|_F$ if and only if $L \in \mathcal{F}(\tau)$. Thus $\mathcal{F}(\tau|_F) = \{L \in \mathcal{F}(\tau) : L \subseteq F\}$ is a finite distributive lattice containing $\emptyset$ and $F$. For all $L_1, L_2 \in \mathcal{F}(\tau|_F)$, modularity holds pointwise:
$$\Delta_{\mathbf{b}}(L_1 \cup L_2) + \Delta_{\mathbf{b}}(L_1 \cap L_2) = \Delta_{\mathbf{b}}(L_1) + \Delta_{\mathbf{b}}(L_2).$$
Hence the set of maximizers $\mathcal{M}_F(\mathbf{b}) := \arg\max_{L \in \mathcal{F}(\tau|_F)} \Delta_{\mathbf{b}}(L)$ is closed under $\cup$ and $\cap$, and therefore has a **unique minimum** element
$$H^*(\mathbf{b}) := \bigcap_{L \in \mathcal{M}_F(\mathbf{b})} L \in \mathcal{M}_F(\mathbf{b}).$$

**Claim (Decoupled characterization of $H^*(\mathbf{b})$).** *For any fixed $H \in \mathcal{F}(\tau|_F)$ and $\mathbf{b} \in \mathbb{N}^F$, we have $H^*(\mathbf{b}) = H$ if and only if:*
1. *(Strict lower domination)* $\Delta_{\mathbf{b}}(K) < \Delta_{\mathbf{b}}(H)$ for every $K \in \mathcal{F}(\tau|_H)$ with $K \subsetneq H$; and
2. *(Weak upper domination)* $\Delta_{\mathbf{b}}(G) \le \Delta_{\mathbf{b}}(H)$ for every $G \in \mathcal{F}(\tau|_F)$ with $G \supseteq H$.

*Proof of Claim.* ($\Rightarrow$) is immediate from the definition of $H^*(\mathbf{b})$. Conversely, suppose (1) and (2) hold, and let $L \in \mathcal{F}(\tau|_F)$. Since $L \cup H \supseteq H$ and $L \cap H \subseteq H$, modularity yields
$$\Delta_{\mathbf{b}}(L) - \Delta_{\mathbf{b}}(H) = \bigl(\Delta_{\mathbf{b}}(L \cup H) - \Delta_{\mathbf{b}}(H)\bigr) + \bigl(\Delta_{\mathbf{b}}(L \cap H) - \Delta_{\mathbf{b}}(H)\bigr) \le 0,$$
with strict inequality whenever $L \cap H \subsetneq H$ (equivalently, $H \not\subseteq L$). Thus $H$ is the unique minimum maximizer of $\Delta_{\mathbf{b}}$ on $\mathcal{F}(\tau|_F)$.

Crucially, writing $\mathbf{b} = (\mathbf{b}_1, \mathbf{b}_2) \in \mathbb{N}^H \times \mathbb{N}^{F \setminus H}$, condition (1) depends **only on $\mathbf{b}_1$**, while condition (2) is $\Delta_{\mathbf{b}_2}(G \setminus H) \le 0$ for all $G \supseteq H$, which depends **only on $\mathbf{b}_2$**.

Now, for every nonempty filter $F \in \mathcal{F}(\tau)$ and every integer $r > W_F$, set
$$A_F(r) := \sum_{\substack{\mathbf{b} \in \mathbb{N}^F, \; |\mathbf{b}| = r \\ \Delta_{\mathbf{b}}(K) < \Delta_{\mathbf{b}}(F) \;\forall K \in \mathcal{F}(\tau|_F), \, K \subsetneq F}} \prod_{e \in F} \binom{w_e}{b_e}.$$
We prove **$A_F(r) = 0$ for every nonempty $F \in \mathcal{F}(\tau)$ and every $r > W_F$** by strong induction on $|F|$. Let $\Omega_{F, r} := \{\mathbf{b} \in \mathbb{N}^F : |\mathbf{b}| = r\}$. By the ordinary multivariate Vandermonde identity (expanding $\prod_{e \in F} (1 + x)^{w_e} = (1 + x)^{W_F}$ in $\mathbb{Z}[[x]]$), since $W_F \in \mathbb{Z}_{\ge 0}$ and $r > W_F$,
$$0 = \binom{W_F}{r} = \sum_{\mathbf{b} \in \Omega_{F, r}} \prod_{e \in F} \binom{w_e}{b_e}.$$
For every $\mathbf{b} \in \Omega_{F, r}$, we have $\Delta_{\mathbf{b}}(F) = r - W_F \ge 1 > 0 = \Delta_{\mathbf{b}}(\emptyset)$, so $H^*(\mathbf{b}) \ne \emptyset$. Partitioning $\Omega_{F, r}$ by $H = H^*(\mathbf{b}) \in \mathcal{F}(\tau|_F) \setminus \{\emptyset\}$ and applying the Claim:
- The summand $H = F$ equals $A_F(r)$.
- For each nonempty proper subfilter $H \subsetneq F$, condition (1) at $K = \emptyset$ forces $s := |\mathbf{b}_1| > W_H$ (and $s \le r$), so the contribution of $H$ factors as
  $$\sum_{s = W_H + 1}^{r} A_H(s) \cdot \left(\sum_{\substack{\mathbf{b}_2 \in \mathbb{N}^{F \setminus H}, \; |\mathbf{b}_2| = r - s \\ \Delta_{\mathbf{b}_2}(G \setminus H) \le 0 \;\forall G \in \mathcal{F}(\tau|_F), \, G \supseteq H}} \prod_{e \in F \setminus H} \binom{w_e}{b_{2, e}}\right) = 0,$$
  because $A_H(s) = 0$ by the induction hypothesis. (When $F$ is a minimal nonempty filter — e.g. a maximal equivalence class of $\tau$ — there are no nonempty proper subfilters $H \subsetneq F$, so the base case is included automatically.)

Hence $0 = A_F(r) + 0$, proving $A_F(r) = 0$.

Finally, for any integer $m \ge 0$, let $B_m := \{\mathbf{b} \in \mathbb{N}^E : |\mathbf{b}| = m,\; \max_{L \in \mathcal{F}(\tau)} \Delta_{\mathbf{b}}(L) \ge 1\}$ be the set of vectors violating at least one filter constraint. Then $\mathbf{b} \in B_m \iff H^*(\mathbf{b}) \ne \emptyset$. Partitioning $B_m$ by $H = H^*(\mathbf{b}) \in \mathcal{F}(\tau) \setminus \{\emptyset\}$ and $s = |\mathbf{b}_1| \ge W_H + 1$ gives
$$\sum_{\mathbf{b} \in B_m} \prod_{e \in E} \binom{w_e}{b_e} = \sum_{\emptyset \ne H \in \mathcal{F}(\tau)} \sum_{s = W_H + 1}^{m} \underbrace{A_H(s)}_{=\,0} \cdot \left(\sum_{\substack{\mathbf{b}_2 \in \mathbb{N}^{E \setminus H}, \; |\mathbf{b}_2| = m - s \\ \Delta_{\mathbf{b}_2}(G \setminus H) \le 0 \;\forall G \in \mathcal{F}(\tau), \, G \supseteq H}} \prod_{e \in E \setminus H} \binom{w_e}{b_{2, e}}\right) = 0.$$
Subtracting this from the unconstrained Vandermonde sum $\sum_{\mathbf{b} \in \mathbb{N}^E,\, |\mathbf{b}| = m} \prod_{e \in E} \binom{w_e}{b_e} = \binom{W_E}{m}$ yields $S(\tau, \mathbf{w}, m) = \binom{W_E}{m}$. $\blacksquare$

---

### 2. Magic-Basis Generating Series and Master Formula

Define $\Psi(w, u) = \sum_{k=0}^\infty \psi_k(u)\, w^k \in \mathbb{Q}[u][[w]]$ and $\Phi(w, y) = \sum_{k=0}^\infty \phi_k(y)\, w^k \in \mathbb{Q}[y][[w]]$ by
$$\Psi(w, u) := \exp\left(\sum_{m = 2}^{\infty} \frac{w^m}{m} \sum_{r = 1}^{m - 1} u^r (1 + u)^{m - r}\right), \qquad \Phi(w, y) := \exp\left(\sum_{m = 2}^{\infty} \frac{w^m}{m} \bigl(y + y^2 + \dots + y^{m - 1}\bigr)\right).$$

**Lemma 2.** *The polynomials $\phi_k(y)$ and $\psi_k(u)$ satisfy:*
1. $\psi_k(u) = (1 + u)^k \phi_k\!\left(\frac{u}{1 + u}\right)$ for all $k \ge 0$, with $\phi_0(y) = 1$, $\phi_1(y) = 0$, and $k!\,\phi_k(y) \in \mathbb{Z}_{\ge 0}[y]$ for every $k \ge 2$ (strictly positive on $y^1, \dots, y^{k-1}$).
2. $\psi_k(-u) = (-1)^k \psi_k(u - 1)$ for all $k \ge 0$.
3. For every integer $a \ge 0$,
   $$\binom{u + a - 1}{a} = \sum_{\substack{k \in \{0, 2, 3, \dots\} \\ k \le a}} \binom{1 - k}{a - k} u^{a - k} \psi_k(u).$$

*Proof.*
1. Replacing $w$ by $(1 + u) w$ and $y$ by $\frac{u}{1 + u}$ in $\Phi(w, y)$ transforms $w^m (y + \dots + y^{m-1})$ into $w^m \sum_{r=1}^{m-1} u^r(1+u)^{m-r}$, giving $\Psi(w, u) = \Phi\bigl((1+u)w, \frac{u}{1+u}\bigr)$. By the exponential formula for permutations, $k!\,\phi_k(y) = \sum_{\sigma \in D_k} \prod_{c \in \operatorname{cyc}(\sigma)} (y + \dots + y^{|c|-1})$, where $D_k \subset \mathfrak{S}_k$ is the set of derangements of $\{1, \dots, k\}$. Hence $\phi_0 = 1$, $\phi_1 = 0$, and $k!\,\phi_k(y) \in \mathbb{Z}_{\ge 0}[y]$.
2. Since $\sum_{r=1}^{m-1} u^r(1+u)^{m-r} = u(1+u)^m - (1+u)u^m$, summing over $m \ge 2$ gives (the $m=1$ linear terms cancel):
   $$\log \Psi(w, u) = (u + 1)\log(1 - u w) - u\log\bigl(1 - (u + 1)w\bigr) \in \mathbb{Q}[u][[w]].$$
   Substituting $(w, u) \mapsto (-w, -u)$ gives $\log \Psi(-w, -u) = u\log\bigl(1 - (u - 1)w\bigr) - (u - 1)\log(1 - u w) = \log \Psi(w, u - 1)$, whence $\Psi(-w, -u) = \Psi(w, u - 1)$ and $\psi_k(-u) = (-1)^k \psi_k(u - 1)$.
3. Substituting $w = \frac{z}{1 + u z} \in z\mathbb{Q}[u][[z]]$ yields $1 - u w = (1 + u z)^{-1}$ and $1 - (u + 1)w = (1 - z)(1 + u z)^{-1}$, so
   $$\log\left((1 + u z)\Psi\!\left(\frac{z}{1 + u z}, u\right)\right) = \log(1 + u z) - (u + 1)\log(1 + u z) - u\log(1 - z) + u\log(1 + u z) = -u\log(1 - z).$$
   Exponentiating in $\mathbb{Q}[u][[z]]$ and using $\psi_1(u) = 0$ gives
   $$\sum_{a=0}^\infty \binom{u + a - 1}{a} z^a = (1 - z)^{-u} = (1 + u z)\Psi\!\left(\frac{z}{1 + u z}, u\right) = \sum_{k \in \{0, 2, 3, \dots\}} \psi_k(u)\, z^k (1 + u z)^{1 - k}.$$
   Expanding $(1 + u z)^{1 - k} = \sum_{b \ge 0} \binom{1 - k}{b} u^b z^b$ and extracting $[z^a]$ gives (3). $\blacksquare$

**Theorem 2 (Master Formula).** *For every finite preorder $\tau$ on an $n$-element set $E$,*
$$\mathbb{E}_\tau(u, v) = \sum_{\substack{\mathbf{k} \in P_{\tau^*} \\ k_e \ne 1 \;\forall e \in E}} P\bigl(n - |\mathbf{k}|;\, u, v\bigr) \prod_{e \in E} \psi_{k_e}(u),$$
*where $P(W; u, v) := \sum_{m=0}^{W} \binom{W}{m} \binom{v + W - m}{W - m} u^m$.*

*Proof.* Substitute Lemma 2(3) for each $e \in E$ into Equation (17), set $b_e := a_e - k_e \ge 0$, and interchange summations (using that $P_{\tau^*}$ is a lower set in $\mathbb{N}^E$, so $\mathbf{k} + \mathbf{b} \in P_{\tau^*} \Rightarrow \mathbf{k} \in P_{\tau^*}$, and $|\mathbf{k}| + |\mathbf{b}| \le n$):
$$\mathbb{E}_\tau(u, v) = \sum_{\substack{\mathbf{k} \in P_{\tau^*} \\ k_e \ne 1 \;\forall e \in E}} \left(\prod_{e \in E} \psi_{k_e}(u)\right) \sum_{m=0}^{n - |\mathbf{k}|} \binom{v + n - |\mathbf{k}| - m}{n - |\mathbf{k}| - m} u^m \sum_{\substack{\mathbf{b} \in \mathbb{N}^E, \; |\mathbf{b}| = m \\ \mathbf{k} + \mathbf{b} \in P_{\tau^*}}} \prod_{e \in E} \binom{1 - k_e}{b_e}.$$
For each fixed $\mathbf{k} \in P_{\tau^*}$, set $w_e := 1 - k_e \in \mathbb{Z}$. For every $F \in \mathcal{F}(\tau)$, $W_F = |F| - \sum_{e \in F} k_e \ge 0$, and $\mathbf{k} + \mathbf{b} \in P_{\tau^*} \iff \sum_{e \in F} b_e \le W_F$ for all $F \in \mathcal{F}(\tau)$. By Theorem 1, the innermost sum equals $\binom{W_E}{m} = \binom{n - |\mathbf{k}|}{m}$, producing $P(n - |\mathbf{k}|; u, v)$. $\blacksquare$

---

### 3. Proofs of Conjectures 4.8, 7.2, 4.4, and 4.9 Eq. (16)

**Corollary 1 (Conjecture 4.8 — Magic Positivity).** *For every finite preorder $\tau$ of size $n$, $\operatorname{Ehr}(\mathcal{Q}_\tau, t)$ is magic positive, $n!\, c_i(\tau) \in \mathbb{Z}_{\ge 0}$ for all $0 \le i \le n$, and $h^*(\mathcal{Q}_\tau, t)$ has only real roots.*

*Proof.* Set $v = 0$ in Theorem 2. Since $P(W; u, 0) = \sum_{m=0}^W \binom{W}{m} u^m = (1 + u)^W$, we obtain
$$\operatorname{Ehr}(\mathcal{Q}_\tau, u) = \sum_{\substack{\mathbf{k} \in P_{\tau^*} \\ k_e \ne 1 \;\forall e \in E}} (1 + u)^{n - |\mathbf{k}|} \prod_{e \in E} \psi_{k_e}(u) = (1 + u)^n \sum_{\substack{\mathbf{k} \in P_{\tau^*} \\ k_e \ne 1 \;\forall e \in E}} \prod_{e \in E} \phi_{k_e}\!\left(\frac{u}{1 + u}\right),$$
so $M_\tau(y) = \sum_{\mathbf{k} \in P_{\tau^*},\, k_e \ne 1} \prod_{e \in E} \phi_{k_e}(y)$. By Lemma 2(1), every coefficient of $M_\tau(y)$ is nonnegative, and multiplying by $n!$ gives
$$n!\, M_\tau(y) = \sum_{\substack{\mathbf{k} \in P_{\tau^*} \\ k_e \ne 1 \;\forall e \in E}} \frac{n!}{\prod_{e \in E} k_e!} \prod_{e \in E} \bigl(k_e!\,\phi_{k_e}(y)\bigr) \in \mathbb{Z}_{\ge 0}[y],$$
since $|\mathbf{k}| \le n$ implies $\frac{n!}{\prod_e k_e!} = (n - |\mathbf{k}|)!\,\binom{n}{n - |\mathbf{k}|, (k_e)_{e \in E}} \in \mathbb{Z}_{\ge 1}$. Real-rootedness of $h^*(\mathcal{Q}_\tau, t)$ follows from magic positivity by Brändén's theorem (`[Bra06, Theorem 4.2]`). $\blacksquare$

**Corollary 2 (Conjecture 7.2 — Double Ehrhart Reciprocity).** *For every finite preorder $\tau$ of size $n$, $\mathbb{E}_\tau(-u, -v) = (-1)^n \mathbb{E}_\tau(u - 1, v - 1)$.*

*Proof.* For any integer $W \ge 0$, setting $j = W - m$, applying upper negation $\binom{-v + j}{j} = (-1)^j \binom{v - 1}{j}$, expanding $u^{W - j} = ((u - 1) + 1)^{W - j}$, and applying Chu–Vandermonde gives
$$\begin{aligned}
P(W; -u, -v)
&= \sum_{j = 0}^{W} \binom{W}{j} \binom{-v + j}{j} (-u)^{W - j}
= (-1)^W \sum_{j = 0}^{W} \binom{W}{j} \binom{v - 1}{j} \sum_{r = 0}^{W - j} \binom{W - j}{r} (u - 1)^r \\
&= (-1)^W \sum_{r = 0}^{W} \binom{W}{r} (u - 1)^r \sum_{j = 0}^{W - r} \binom{W - r}{W - r - j} \binom{v - 1}{j} \\
&= (-1)^W \sum_{r = 0}^{W} \binom{W}{r} \binom{v - 1 + W - r}{W - r} (u - 1)^r = (-1)^W P(W; u - 1, v - 1).
\end{aligned}$$
By Lemma 2(2), each $\mathbf{k}$-summand in Theorem 2 transforms under $(u, v) \mapsto (-u, -v)$ by $(-1)^{n - |\mathbf{k}|} \prod_{e \in E} (-1)^{k_e} = (-1)^n$ times the corresponding summand at $(u - 1, v - 1)$. Summing over $\mathbf{k}$ gives the result. $\blacksquare$

**Corollary 3 (Conjecture 4.4 and Conjecture 4.9 Eq. (16)).** *For every finite preorder $\tau$ of size $n$,*
$$h^*(\mathcal{Q}_\tau, t) = \sum_{w \in \mathcal{W}_\tau} t^{n - 1 - \operatorname{des}(w)} \qquad \text{and} \qquad \mathcal{Z}(P_\tau, -1) = (-1)^n \#\operatorname{Max}(P_\tau).$$

*Proof.* By Remark 7.3 of `arXiv:2605.26916`, setting $v = 0$ in Corollary 2 yields Conjecture 4.4. By Remark 4.10(a) of `arXiv:2605.26916`, Conjecture 4.4 implies Equation (16) of Conjecture 4.9. $\blacksquare$

---

## Relation to Conjecture 5.3 ($P_3$) and Sharpness Control

1. **8-element counterexample to Conjecture 5.3 ($P_3$):** Let $P_3$ be the height-2 poset on $\{b_0, b_1, b_2, b_3, t_0, t_1, t_2, t_3\}$ with relations $b_0 \prec t_1, t_2, t_3$, $b_1, b_2, b_3 \prec t_0$, and $b_i \prec t_i$ ($i = 1, 2, 3$). Its **support polynomial** (Conjecture 5.3) is
   $$h(P_3, t) = 1 + 17t + 106t^2 + 303t^3 + 427t^4 + 303t^5 + 106t^6 + 17t^7 + t^8,$$
   which has only 4 real roots (violating Conjecture 5.3). By contrast, in accordance with Corollary 1, its Ehrhart magic polynomial and $h^*$-polynomial are strictly positive and real-rooted:
   $$M_{P_3}(y) = 1 + \frac{43}{12} y + \frac{71}{12} y^2 + \frac{239}{48} y^3 + \frac{85}{48} y^4,$$
   $$h^*(\mathcal{Q}_{P_3}, t) = 1 + 1272t + 39969t^2 + 217034t^3 + 306464t^4 + 119943t^5 + 10737t^6 + 100t^7.$$

2. **Sharpness — Transitivity is essential:** Preorder polytopes are matched $Y$-type generalized permutohedra $\sum_{e \in E} \boldsymbol{\Delta}_{I_e}$ with $I_e = \mathscr{U}(e)$ transitively closed. Dropping transitivity while preserving $e \in I_e$ destroys the modularity of $f(F) = |F|$ on $\mathcal{F}(\tau)$, and magic positivity already fails at $n = 6$: for $I = (\{0,2\}, \{1,3,5\}, \{0,2,3,5\}, \{0,1,3\}, \{1,2,4\}, \{0,1,5\})$,
   $$M(y) = 1 + \frac{59}{12}y + \frac{439}{36}y^2 + \frac{2075}{144}y^3 + \frac{335}{72}y^4 - \frac{1}{6}y^5 \qquad \left(c_5 = -\frac{1}{6} < 0\right).$$

---

## Independent Verification

Run the standalone exact rational verifier (Python 3 standard library only, no external dependencies):

```bash
python3 verify.py
```

`verify.py` checks all identities in Lemma 2, Theorem 1 (and Lemma $A_F(r) = 0$ on 120 random posets and non-poset preorders with signed weights), direct lattice-point counting $\#(m\mathcal{Q}_\tau \cap \mathbb{Z}^n)$ + Lagrange interpolation against Theorem 1.5(a), Theorem 2, Conjecture 4.4 direct word enumeration, Conjecture 7.2 reciprocity, Conjecture 4.9 Eq. (16), the $P_3$ example, and the $n=6$ non-transitive sharpness control.

---

*Paper source retrieved via arXiv (`https://arxiv.org/abs/2605.26916`); subject to arXiv Terms of Use (`https://info.arxiv.org/help/api/index.html`) and the paper's individual arXiv license.*
