#!/usr/bin/env python3
"""
Standalone exact verifier for the proof of Athanasiadis-Chapoton's
Conjectures 4.8 (magic positivity), 7.2 (double Ehrhart reciprocity),
4.4 (h*-polynomial word formula), and 4.9 eq. (16) (zeta at -1)
from arXiv:2605.26916 ("Polytopes and posets associated to preorders").

Uses ONLY Python standard library exact integer and Fraction arithmetic.

Verifies:
  1. Distributive-Lattice Vandermonde Theorem and its inductive core lemma
     A_F(r) = 0 on structured and random preorders with arbitrary signed
     integer weight vectors w in Z^E satisfying sum_{e in F} w_e >= 0.
  2. Formal power series identities for psi_k(u) and phi_k(y):
     - strict nonnegativity of phi_k(y) and integrality of k! * phi_k(y),
     - symmetry psi_k(-u) = (-1)^k * psi_k(u - 1),
     - binomial expansion binom(u + a - 1, a) = sum_k binom(1 - k, a - k) u^{a-k} psi_k(u),
     - reciprocity P(W; -u, -v) = (-1)^W * P(W; u - 1, v - 1).
  3. Master Formula for biE_tau(u, v) and Ehr(Q_tau, t) checked independently
     against:
     (a) direct lattice-point counting of m * Q_tau from raw order-ideal
         inequalities + exact Lagrange polynomial interpolation,
     (b) Theorem 1.5(a) / eq. (17) draconian formula,
     (c) Conjecture 4.4 direct word-descent enumeration over W_tau,
     (d) Conjecture 4.9 eq. (16) (-1)^n Ehr(Q_{tau*}, -2) = #Max(P_tau).
  4. Analysis of the 8-element height-2 counterexample P_3 to Conjecture 5.3
     (non-real-rooted support polynomial h(P_3, t)), confirming P_3 satisfies
     Conjecture 4.8 with strictly positive magic polynomial M_{P_3}(y) and
     real-rooted h*(Q_{P_3}, t), verified by direct lattice-point counting.
  5. Sharpness negative control: a 6-element non-transitive matched Y-type
     generalized permutohedron failing magic positivity (c_5 = -1/6 < 0),
     confirming that transitivity (the distributive lattice of order filters)
     is essential.
"""

from fractions import Fraction
import itertools
import math
import random


# ============================================================================
# Exact univariate and bivariate rational polynomial arithmetic
# ============================================================================

def poly_trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p if p else [Fraction(0)]


def poly_add(a, b):
    n = max(len(a), len(b))
    out = [Fraction(0)] * n
    for i, v in enumerate(a):
        out[i] += v
    for i, v in enumerate(b):
        out[i] += v
    return poly_trim(out)


def poly_sub(a, b):
    n = max(len(a), len(b))
    out = [Fraction(0)] * n
    for i, v in enumerate(a):
        out[i] += v
    for i, v in enumerate(b):
        out[i] -= v
    return poly_trim(out)


def poly_mul(a, b):
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, va in enumerate(a):
        if va == 0:
            continue
        for j, vb in enumerate(b):
            if vb != 0:
                out[i + j] += va * vb
    return poly_trim(out)


def poly_scale(a, c):
    return poly_trim([v * c for v in a])


def poly_pow(a, e):
    res = [Fraction(1)]
    base = list(a)
    while e > 0:
        if e & 1:
            res = poly_mul(res, base)
        base = poly_mul(base, base)
        e >>= 1
    return res


def poly_eval(a, x):
    acc = Fraction(0)
    for c in reversed(a):
        acc = acc * x + c
    return acc


def poly_compose(a, q):
    """Evaluate polynomial a(q(x))."""
    acc = [Fraction(0)]
    for c in reversed(a):
        acc = poly_add(poly_mul(acc, q), [c])
    return poly_trim(acc)


def poly_lagrange(points):
    """Exact Lagrange interpolation from list of (x_i, y_i) Fraction pairs."""
    res = [Fraction(0)]
    for i, (xi, yi) in enumerate(points):
        num = [Fraction(1)]
        den = Fraction(1)
        for j, (xj, _) in enumerate(points):
            if i == j:
                continue
            num = poly_mul(num, [-xj, Fraction(1)])
            den *= (xi - xj)
        res = poly_add(res, poly_scale(num, yi / den))
    return poly_trim(res)


def gen_binom(w, b):
    """Generalized binomial coefficient binom(w, b) for integer w and b >= 0."""
    if b < 0:
        return 0
    num = 1
    den = 1
    for j in range(b):
        num *= (w - j)
        den *= (j + 1)
    assert num % den == 0
    return num // den


def rising_binom_poly(a):
    """Polynomial binom(u + a - 1, a) in Q[u]."""
    p = [Fraction(1)]
    for j in range(a):
        p = poly_mul(p, [Fraction(a - 1 - j), Fraction(1)])
    return poly_scale(p, Fraction(1, math.factorial(a)))


def falling_binom_poly(a, shift=0):
    """Polynomial binom(u + shift, a) in Q[u]."""
    p = [Fraction(1)]
    for j in range(a):
        p = poly_mul(p, [Fraction(shift - j), Fraction(1)])
    return poly_scale(p, Fraction(1, math.factorial(a)))


def bipoly_add(a, b):
    res = dict(a)
    for k, v in b.items():
        nv = res.get(k, Fraction(0)) + v
        if nv == 0:
            res.pop(k, None)
        else:
            res[k] = nv
    return res


def bipoly_mul(a, b):
    res = {}
    for (i1, j1), v1 in a.items():
        for (i2, j2), v2 in b.items():
            k = (i1 + i2, j1 + j2)
            nv = res.get(k, Fraction(0)) + v1 * v2
            if nv == 0:
                res.pop(k, None)
            else:
                res[k] = nv
    return res


def bipoly_from_u(p):
    return {(i, 0): c for i, c in enumerate(p) if c != 0}


def bipoly_from_v(p):
    return {(0, j): c for j, c in enumerate(p) if c != 0}


def bipoly_subst_linear(p, au, bu, av, bv):
    """Substitute u -> au*u + bu, v -> av*v + bv into bivariate polynomial."""
    u_lin = bipoly_from_u([Fraction(bu), Fraction(au)])
    v_lin = bipoly_from_v([Fraction(bv), Fraction(av)])
    # Precompute powers
    max_i = max((i for i, _ in p.keys()), default=0)
    max_j = max((j for _, j in p.keys()), default=0)
    u_pows = [{(0, 0): Fraction(1)}]
    for _ in range(max_i):
        u_pows.append(bipoly_mul(u_pows[-1], u_lin))
    v_pows = [{(0, 0): Fraction(1)}]
    for _ in range(max_j):
        v_pows.append(bipoly_mul(v_pows[-1], v_lin))
    res = {}
    for (i, j), c in p.items():
        term = bipoly_mul(u_pows[i], v_pows[j])
        term = {k: val * c for k, val in term.items()}
        res = bipoly_add(res, term)
    return res


# ============================================================================
# Core proof building blocks: phi_k(y), psi_k(u), and P(W; u, v)
# ============================================================================

def build_phi_and_psi(max_k):
    """
    Compute phi_k(y) = [w^k] exp(sum_{m>=2} (w^m / m) * (y + ... + y^{m-1}))
    and psi_k(u) = (1 + u)^k * phi_k(u / (1 + u))
                 = [w^k] exp(sum_{m>=2} (w^m / m) * sum_{r=1}^{m-1} u^r (1+u)^{m-r}).
    """
    phi = [[Fraction(0)] for _ in range(max_k + 1)]
    phi[0] = [Fraction(1)]
    for m in range(2, max_k + 1):
        acc = [Fraction(0)]
        for j in range(2, m + 1):
            # y + y^2 + ... + y^{j-1}
            pj = [Fraction(0)] + [Fraction(1)] * (j - 1)
            acc = poly_add(acc, poly_mul(phi[m - j], pj))
        phi[m] = poly_scale(acc, Fraction(1, m))

    psi = []
    for k in range(max_k + 1):
        pk = [Fraction(0)]
        for j, c in enumerate(phi[k]):
            if c != 0:
                term = poly_mul([Fraction(0)] * j + [c], poly_pow([Fraction(1), Fraction(1)], k - j))
                pk = poly_add(pk, term)
        psi.append(pk)
    return phi, psi


def build_P_bipoly(W):
    """P(W; u, v) = sum_{m=0}^W binom(W, m) * binom(v + W - m, W - m) * u^m."""
    res = {}
    for m in range(W + 1):
        c = Fraction(math.comb(W, m))
        # binom(v + W - m, W - m) as polynomial in v
        pv = falling_binom_poly(W - m, shift=W - m)
        term = bipoly_mul({(m, 0): c}, bipoly_from_v(pv))
        res = bipoly_add(res, term)
    return res


# ============================================================================
# Preorder utilities
# ============================================================================

def preorder_closure(n, edges):
    up = [1 << i for i in range(n)]
    for u, v in edges:
        up[u] |= (1 << v)
    for k in range(n):
        for i in range(n):
            if (up[i] >> k) & 1:
                up[i] |= up[k]
    return up


def get_filters(n, up):
    fs = []
    for mask in range(1 << n):
        cl = 0
        for i in range(n):
            if (mask >> i) & 1:
                cl |= up[i]
        if cl == mask:
            fs.append(mask)
    return fs


def get_ideals(n, up):
    down = [0] * n
    for x in range(n):
        for z in range(n):
            if (up[z] >> x) & 1:
                down[x] |= (1 << z)
    ids = []
    for mask in range(1 << n):
        cl = 0
        for i in range(n):
            if (mask >> i) & 1:
                cl |= down[i]
        if cl == mask:
            ids.append(mask)
    return ids, down


def topo_order_by_masks(n, masks):
    """Order elements placing elements whose mask has no other classes first."""
    order = []
    used = [False] * n
    while len(order) < n:
        progressed = False
        for v in range(n):
            if not used[v]:
                if all((not ((masks[v] >> w) & 1)) or masks[w] == masks[v] or used[w] for w in range(n)):
                    for w in range(n):
                        if masks[w] == masks[v] and not used[w]:
                            order.append(w)
                            used[w] = True
                    progressed = True
                    break
        assert progressed
    return order


def enumerate_P_taustar(n, up):
    filters = [F for F in get_filters(n, up) if F != 0]
    order = topo_order_by_masks(n, up)
    pos = {v: i for i, v in enumerate(order)}
    f_at = [[] for _ in range(n)]
    for F in filters:
        elems = [i for i in range(n) if (F >> i) & 1]
        f_at[max(pos[v] for v in elems)].append((elems, len(elems)))
    pts = []
    A = [0] * n

    def bt(step, s):
        if step == n:
            pts.append(tuple(A))
            return
        v = order[step]
        ub = n - s
        for elems, cap in f_at[step]:
            rem = cap - sum(A[w] for w in elems if w != v)
            if rem < ub:
                ub = rem
        if ub < 0:
            return
        for av in range(ub + 1):
            A[v] = av
            bt(step + 1, s + av)
        A[v] = 0

    bt(0, 0)
    return pts


def count_mQ_tau_direct(n, up, m):
    """Direct lattice-point count #(m * Q_tau cap Z^n) from raw order-ideal inequalities."""
    ideals, down = get_ideals(n, up)
    ideals = [I for I in ideals if I != 0]
    order = topo_order_by_masks(n, down)
    pos = {v: i for i, v in enumerate(order)}
    id_at = [[] for _ in range(n)]
    for I in ideals:
        elems = [i for i in range(n) if (I >> i) & 1]
        id_at[max(pos[v] for v in elems)].append((elems, len(elems)))
    cnt = [0]
    X = [0] * n

    def bt(step):
        if step == n:
            cnt[0] += 1
            return
        v = order[step]
        ub = m * n
        for elems, sz in id_at[step]:
            rem = m * sz - sum(X[w] for w in elems if w != v)
            if rem < ub:
                ub = rem
        if ub < 0:
            return
        for xv in range(ub + 1):
            X[v] = xv
            bt(step + 1)
        X[v] = 0

    bt(0)
    return cnt[0]


def ehr_to_hstar(ehr, n):
    """Exact h*-polynomial from Ehrhart polynomial of degree n."""
    coeffs = []
    vals = [poly_eval(ehr, Fraction(m)) for m in range(n + 1)]
    for k in range(n + 1):
        ck = Fraction(0)
        for m in range(k + 1):
            ck += ((-1) ** (k - m)) * math.comb(n + 1, k - m) * vals[m]
        assert ck.denominator == 1
        coeffs.append(ck)
    return poly_trim(coeffs)


def ehr_to_magic(ehr, n):
    """Transform Ehr(t) = sum_i c_i t^i (1+t)^{n-i} -> M(y) = sum_i c_i y^i."""
    # M(y) = (1 - y)^n * Ehr(y / (1 - y)) = sum_{d=0}^n ehr[d] * y^d * (1 - y)^{n - d}
    M = [Fraction(0)]
    for d, c in enumerate(ehr):
        if c != 0:
            term = poly_mul([Fraction(0)] * d + [c], poly_pow([Fraction(1), Fraction(-1)], n - d))
            M = poly_add(M, term)
    return M


def magic_to_ehr(M, n):
    """Transform M(y) = sum_i c_i y^i -> Ehr(t) = sum_i c_i t^i (1 + t)^{n - i}."""
    ehr = [Fraction(0)]
    for i, c in enumerate(M):
        if c != 0:
            term = poly_mul([Fraction(0)] * i + [c], poly_pow([Fraction(1), Fraction(1)], n - i))
            ehr = poly_add(ehr, term)
    return ehr


def count_real_roots_sturm(coeffs_int):
    """Exact Sturm theorem count of distinct real roots of a square-free or general integer polynomial."""
    # Convert to Fractions and make square-free via p / gcd(p, p')
    p = poly_trim([Fraction(c) for c in coeffs_int])

    def deriv(a):
        if len(a) <= 1:
            return [Fraction(0)]
        return poly_trim([a[i] * i for i in range(1, len(a))])

    def prem_monic(a, b):
        a = list(a)
        db = len(b) - 1
        lb = b[-1]
        while len(a) - 1 >= db and not (len(a) == 1 and a[0] == 0):
            shift = len(a) - 1 - db
            factor = a[-1] / lb
            for i in range(db + 1):
                a[shift + i] -= factor * b[i]
            a = poly_trim(a)
        return a

    def gcd_poly(a, b):
        while not (len(b) == 1 and b[0] == 0):
            a, b = b, prem_monic(a, b)
        return poly_scale(a, Fraction(1) / a[-1])

    def exact_div(a, b):
        a = list(a)
        db = len(b) - 1
        lb = b[-1]
        q = [Fraction(0)] * (len(a) - db)
        while len(a) - 1 >= db and not (len(a) == 1 and a[0] == 0):
            shift = len(a) - 1 - db
            factor = a[-1] / lb
            q[shift] = factor
            for i in range(db + 1):
                a[shift + i] -= factor * b[i]
            a = poly_trim(a)
        assert a == [Fraction(0)]
        return poly_trim(q)

    g = gcd_poly(p, deriv(p))
    sf = exact_div(p, g)
    sturm = [sf, deriv(sf)]
    while len(sturm[-1]) > 1:
        r = prem_monic(sturm[-2], sturm[-1])
        if r == [Fraction(0)]:
            break
        sturm.append(poly_scale(r, Fraction(-1)))

    def sign_variations(signs):
        nz = [s for s in signs if s != 0]
        return sum(1 for i in range(len(nz) - 1) if nz[i] * nz[i + 1] < 0)

    signs_neg_inf = [(-1) ** (len(s) - 1) * (1 if s[-1] > 0 else -1) for s in sturm]
    signs_pos_inf = [(1 if s[-1] > 0 else -1) for s in sturm]
    distinct_real = sign_variations(signs_neg_inf) - sign_variations(signs_pos_inf)
    return distinct_real, len(sf) - 1, len(p) - 1


# ============================================================================
# SECTION 1: Verify formal power series identities
# ============================================================================

def verify_section_1():
    print("=" * 74)
    print("SECTION 1: Formal power series & polynomial identities (phi_k, psi_k, P)")
    print("=" * 74)
    MAXK = 12
    phi, psi = build_phi_and_psi(MAXK)

    # 1a. Nonnegativity of phi_k(y) and integrality of k! * phi_k(y)
    assert phi[0] == [Fraction(1)] and phi[1] == [Fraction(0)]
    for k in range(2, MAXK + 1):
        assert len(phi[k]) == k  # degree k - 1
        assert phi[k][0] == 0
        fact_k = math.factorial(k)
        for j in range(1, k):
            assert phi[k][j] > 0, f"phi_{k}[{j}] not strictly positive!"
            assert (phi[k][j] * fact_k).denominator == 1, f"k! * phi_{k}[{j}] not integer!"
            # Palindromic: phi_k[j] == phi_k[k - j]
            assert phi[k][j] == phi[k][k - j]
    print(f"  [OK] phi_k(y) strictly positive, palindromic, k!*phi_k in Z>=0[y] for k=0..{MAXK}")
    for k in range(2, 6):
        print(f"       phi_{k}(y) = " + " + ".join(f"({phi[k][j]})*y^{j}" for j in range(1, k)))

    # 1b. Symmetry psi_k(-u) == (-1)^k * psi_k(u - 1)
    for k in range(MAXK + 1):
        lhs = poly_compose(psi[k], [Fraction(0), Fraction(-1)])
        rhs = poly_scale(poly_compose(psi[k], [Fraction(-1), Fraction(1)]), Fraction((-1) ** k))
        assert lhs == rhs, f"psi symmetry failed at k={k}"
    print(f"  [OK] Symmetry psi_k(-u) = (-1)^k psi_k(u - 1) verified for k=0..{MAXK}")

    # 1c. Expansion binom(u + a - 1, a) == sum_{k in {0,2..a}} binom(1 - k, a - k) u^{a-k} psi_k(u)
    for a in range(MAXK + 1):
        lhs = rising_binom_poly(a)
        rhs = [Fraction(0)]
        for k in [0] + list(range(2, a + 1)):
            c = Fraction(gen_binom(1 - k, a - k))
            if c != 0:
                term = poly_mul([Fraction(0)] * (a - k) + [c], psi[k])
                rhs = poly_add(rhs, term)
        assert lhs == rhs, f"Rising binomial expansion failed at a={a}"
    print(f"  [OK] Exact identity binom(u+a-1, a) = sum_k binom(1-k, a-k) u^(a-k) psi_k(u) for a=0..{MAXK}")

    # 1d. Expansion binom(u + 1, a) == sum_{k in {0,2..a}} binom(1 - k, a - k) (u+1)^{a-k} psi_k(u)
    for a in range(MAXK + 1):
        lhs = falling_binom_poly(a, shift=1)
        rhs = [Fraction(0)]
        for k in [0] + list(range(2, a + 1)):
            c = Fraction(gen_binom(1 - k, a - k))
            if c != 0:
                term = poly_mul(poly_scale(poly_pow([Fraction(1), Fraction(1)], a - k), c), psi[k])
                rhs = poly_add(rhs, term)
        assert lhs == rhs, f"Falling binomial expansion failed at a={a}"
    print(f"  [OK] Exact identity binom(u+1, a) = sum_k binom(1-k, a-k) (u+1)^(a-k) psi_k(u) for a=0..{MAXK}")

    # 1e. Reciprocity P(W; -u, -v) == (-1)^W * P(W; u - 1, v - 1)
    for W in range(10):
        P = build_P_bipoly(W)
        lhs = bipoly_subst_linear(P, -1, 0, -1, 0)
        rhs_raw = bipoly_subst_linear(P, 1, -1, 1, -1)
        sign = Fraction((-1) ** W)
        rhs = {k: val * sign for k, val in rhs_raw.items()}
        assert lhs == rhs, f"P reciprocity failed at W={W}"
    print("  [OK] Exact reciprocity P(W; -u, -v) = (-1)^W P(W; u - 1, v - 1) for W=0..9")
    return phi, psi


# ============================================================================
# SECTION 2: Verify Distributive-Lattice Vandermonde Theorem & Lemma A_F(r)=0
# ============================================================================

def verify_section_2():
    print("\n" + "=" * 74)
    print("SECTION 2: Distributive-Lattice Vandermonde Theorem & Lemma A_F(r) = 0")
    print("=" * 74)

    def test_dlv(n, up, w):
        filters = get_filters(n, up)
        W = {F: sum(w[i] for i in range(n) if (F >> i) & 1) for F in filters}
        assert all(val >= 0 for val in W.values())
        WE = W[(1 << n) - 1]

        # Check A_F(r) == 0 for every nonempty filter F and r in W[F]+1..min(W[F]+3, 7)
        for F in filters:
            if F == 0:
                continue
            elems = [i for i in range(n) if (F >> i) & 1]
            subfilters = [H for H in filters if (H & F) == H and H != F]
            for r in range(W[F] + 1, min(W[F] + 4, 8)):
                tot = [0]
                bvec = [0] * n

                def enum_b(idx, rem):
                    if idx == len(elems) - 1:
                        bvec[elems[idx]] = rem
                        dF = r - W[F]
                        for H in subfilters:
                            if sum(bvec[i] - w[i] for i in range(n) if (H >> i) & 1) >= dF:
                                bvec[elems[idx]] = 0
                                return
                        p = 1
                        for e in elems:
                            p *= gen_binom(w[e], bvec[e])
                        tot[0] += p
                        bvec[elems[idx]] = 0
                        return
                    for val in range(rem + 1):
                        bvec[elems[idx]] = val
                        enum_b(idx + 1, rem - val)
                    bvec[elems[idx]] = 0

                enum_b(0, r)
                assert tot[0] == 0, f"A_F(r) != 0 for F={F}, r={r}, w={w}"

        # Check S(tau, w, m) == binom(W_E, m) for m = 0..WE+2
        for m in range(WE + 3):
            tot = [0]
            bvec = [0] * n

            def enum_all(idx, rem):
                if idx == n - 1:
                    bvec[idx] = rem
                    for F in filters:
                        if sum(bvec[i] for i in range(n) if (F >> i) & 1) > W[F]:
                            bvec[idx] = 0
                            return
                    p = 1
                    for e in range(n):
                        p *= gen_binom(w[e], bvec[e])
                    tot[0] += p
                    bvec[idx] = 0
                    return
                for val in range(rem + 1):
                    bvec[idx] = val
                    enum_all(idx + 1, rem - val)
                bvec[idx] = 0

            enum_all(0, m)
            assert tot[0] == gen_binom(WE, m)

    rng = random.Random(260526916)
    tested = 0
    for _ in range(120):
        n = rng.choice([3, 4, 5])
        up = [1 << i for i in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j and rng.random() < (0.18 if j < i else 0.55):
                    up[i] |= (1 << j)
        for k in range(n):
            for i in range(n):
                if (up[i] >> k) & 1:
                    up[i] |= up[k]
        filters = get_filters(n, up)
        for _ in range(60):
            w = [rng.randint(-3, 3) for _ in range(n)]
            if (all(sum(w[i] for i in range(n) if (F >> i) & 1) >= 0 for F in filters)
                    and sum(w) <= 5 and any(x < 0 for x in w)):
                test_dlv(n, up, w)
                tested += 1
                break
    print(f"  [OK] Verified A_F(r) = 0 and S(tau, w, m) = binom(W_E, m) on {tested} random")
    print("       preorders (posets & non-poset preorders) with signed integer weights w.")


# ============================================================================
# SECTION 3: Independent end-to-end verification on diverse preorders
# ============================================================================

def verify_section_3(phi, psi):
    print("\n" + "=" * 74)
    print("SECTION 3: Direct lattice counts == Thm 1.5(a) == Master Formula == Conj 4.4 / 7.2 / 4.9")
    print("=" * 74)

    cases = [
        ("Single element n=1", 1, []),
        ("Antichain n=4", 4, []),
        ("Single block n=4", 4, [(0, 1), (1, 2), (2, 3), (3, 0)]),
        ("V-poset n=3", 3, [(0, 1), (0, 2)]),
        ("Fig 1 running ex. n=5", 5, [(0, 1), (1, 0), (0, 4), (1, 4), (2, 4), (2, 3)]),
        ("K_{2,2} n=4", 4, [(0, 2), (0, 3), (1, 2), (1, 3)]),
        ("K_{2,3} n=5", 5, [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)]),
        ("Crown C_6 n=6", 6, [(0, 3), (0, 4), (1, 4), (1, 5), (2, 5), (2, 3)]),
        ("Grid C_3 x C_2 n=6", 6, [(0, 1), (2, 3), (4, 5), (0, 2), (1, 3), (2, 4), (3, 5)]),
        ("Blown-up V(1;2,2) n=5", 5, [(0, 1), (0, 3), (1, 2), (2, 1), (3, 4), (4, 3)]),
        ("Chain [2,2,1] n=5", 5, [(0, 1), (1, 0), (2, 3), (3, 2), (0, 2), (2, 4)]),
        ("Disjoint V + block2", 5, [(0, 1), (0, 2), (3, 4), (4, 3)]),
    ]

    for name, n, edges in cases:
        up = preorder_closure(n, edges)

        # (a) Direct lattice-point count + Lagrange interpolation
        direct_pts = [(Fraction(m), Fraction(count_mQ_tau_direct(n, up, m))) for m in range(n + 1)]
        ehr_direct = poly_lagrange(direct_pts)

        # (b) Theorem 1.5(a) & eq. (17) double Ehrhart polynomial
        pts = enumerate_P_taustar(n, up)
        ehr_15a = [Fraction(0)]
        biE_17 = {}
        for pt in pts:
            prod_u = [Fraction(1)]
            for a in pt:
                prod_u = poly_mul(prod_u, rising_binom_poly(a))
            ehr_15a = poly_add(ehr_15a, prod_u)
            a0 = n - sum(pt)
            pv = falling_binom_poly(a0, shift=a0)
            biE_17 = bipoly_add(biE_17, bipoly_mul(bipoly_from_u(prod_u), bipoly_from_v(pv)))

        # (c) Master Formula for M_tau(y) and biE_tau(u, v)
        M_master = [Fraction(0)]
        biE_master = {}
        for pt in pts:
            if 1 not in pt:
                prod_phi = [Fraction(1)]
                prod_psi = [Fraction(1)]
                for k in pt:
                    prod_phi = poly_mul(prod_phi, phi[k])
                    prod_psi = poly_mul(prod_psi, psi[k])
                M_master = poly_add(M_master, prod_phi)
                P_W = build_P_bipoly(n - sum(pt))
                biE_master = bipoly_add(biE_master, bipoly_mul(bipoly_from_u(prod_psi), P_W))
        ehr_master = magic_to_ehr(M_master, n)

        # (d) Conjecture 4.4 direct word-descent enumeration
        h_word_coeffs = [0] * n
        max_pts = [pt for pt in pts if sum(pt) == n]
        for pt in max_pts:
            letters = []
            for e, c in enumerate(pt):
                letters.extend([e] * c)
            for w in set(itertools.permutations(letters)):
                des = sum(1 for i in range(n - 1) if w[i] > w[i + 1])
                h_word_coeffs[n - 1 - des] += 1
        hstar_words = poly_trim([Fraction(c) for c in h_word_coeffs])
        hstar_direct = ehr_to_hstar(ehr_direct, n)

        # (e) Reciprocity (Conjecture 7.2) & Zeta at -1 (Conjecture 4.9 eq. (16))
        biE_neg = bipoly_subst_linear(biE_master, -1, 0, -1, 0)
        biE_shift = bipoly_subst_linear(biE_master, 1, -1, 1, -1)
        sign = Fraction((-1) ** n)
        biE_shift = {k: val * sign for k, val in biE_shift.items()}

        # Check all identities!
        assert ehr_direct == ehr_15a == ehr_master
        assert ehr_to_magic(ehr_direct, n) == M_master
        assert all(c >= 0 for c in M_master)
        assert all((c * math.factorial(n)).denominator == 1 for c in M_master)
        assert biE_17 == biE_master
        assert biE_neg == biE_shift
        assert hstar_direct == hstar_words
        assert ((-1) ** n) * poly_eval(ehr_direct, Fraction(-2)) == len(max_pts)

        print(f"  [OK] {name:22s} | M(y) >= 0 (deg {len(M_master)-1}) | Direct=1.5a=Master=Conj4.4=Conj7.2=Conj4.9(16)")


# ============================================================================
# SECTION 4: Patel's 8-element Conjecture 5.3 counterexample P_3
# ============================================================================

def verify_section_4(phi):
    print("\n" + "=" * 74)
    print("SECTION 4: 8-element Conjecture 5.3 counterexample P_3 vs Conjecture 4.8")
    print("=" * 74)
    # P_3: bottoms {0, 1, 2, 3}, tops {4, 5, 6, 7};
    # b_0 < t_1, t_2, t_3; b_1, b_2, b_3 < t_0; b_i < t_i for i=1,2,3 (b_0 </< t_0).
    n = 8
    edges = [(0, 5), (0, 6), (0, 7), (1, 4), (2, 4), (3, 4), (1, 5), (2, 6), (3, 7)]
    up = preorder_closure(n, edges)

    # Support polynomial h(P_3, t) from lattice points of Q_{P_3} (note P_3 is self-dual!)
    pts = enumerate_P_taustar(n, up)
    h_supp = [0] * (n + 1)
    for pt in pts:
        nz = sum(1 for x in pt if x > 0)
        h_supp[nz] += 1
    assert h_supp == [1, 17, 106, 303, 427, 303, 106, 17, 1]
    real_roots_h, sf_deg_h, deg_h = count_real_roots_sturm(h_supp)
    assert real_roots_h < sf_deg_h  # Strictly non-real-rooted!
    print(f"  Support polynomial h(P_3, t) = {h_supp}")
    print(f"  [OK] Sturm check: h(P_3, t) has {real_roots_h} distinct real roots out of degree {deg_h} -> VIOLATES Conj 5.3!")

    # Exact magic polynomial M_{P_3}(y) via Master Formula and Theorem 1.5(a)
    M_master = [Fraction(0)]
    ehr_15a = [Fraction(0)]
    for pt in pts:
        prod_u = [Fraction(1)]
        for a in pt:
            prod_u = poly_mul(prod_u, rising_binom_poly(a))
        ehr_15a = poly_add(ehr_15a, prod_u)
        if 1 not in pt:
            prod_phi = [Fraction(1)]
            for k in pt:
                prod_phi = poly_mul(prod_phi, phi[k])
            M_master = poly_add(M_master, prod_phi)

    ehr_master = magic_to_ehr(M_master, n)
    assert ehr_15a == ehr_master
    expected_M = [Fraction(1), Fraction(43, 12), Fraction(71, 12), Fraction(239, 48), Fraction(85, 48)]
    assert M_master == expected_M
    assert all(c > 0 for c in M_master)

    # Direct lattice-point count check for m = 0, 1, 2, 3
    for m in range(4):
        direct_c = count_mQ_tau_direct(n, up, m)
        assert direct_c == poly_eval(ehr_master, Fraction(m))

    hstar = ehr_to_hstar(ehr_master, n)
    hstar_ints = [int(c) for c in hstar]
    real_roots_hs, sf_deg_hs, deg_hs = count_real_roots_sturm(hstar_ints)
    assert real_roots_hs == deg_hs
    print(f"  Magic polynomial M_{{P_3}}(y) = " + " + ".join(f"{M_master[i]}*y^{i}" for i in range(len(M_master))))
    print(f"  h*(Q_{{P_3}}, t) = {hstar_ints}")
    print(f"  [OK] Direct lattice counts m=0..3 match; M_{{P_3}}(y) > 0; h* has all {real_roots_hs}/{deg_hs} roots real!")


# ============================================================================
# SECTION 5: Sharpness negative control (non-transitive matched Y-type polytope)
# ============================================================================

def verify_section_5():
    print("\n" + "=" * 74)
    print("SECTION 5: Sharpness control — non-transitive matched Y-type polytope fails magic positivity")
    print("=" * 74)
    # Q = sum_{e=0}^5 Delta_{I_e} in R^6 with e in I_e for all e, NOT transitively closed:
    sets = [5, 42, 45, 11, 22, 35]  # bitmasks of I_0..I_5
    n = 6
    for e in range(n):
        assert (sets[e] >> e) & 1  # matched: e in I_e

    # Union sizes |U_{e in S} I_e| for all S subset {0..5}
    union_sz = [0] * (1 << n)
    for mask in range(1, 1 << n):
        u = 0
        for i in range(n):
            if (mask >> i) & 1:
                u |= sets[i]
        union_sz[mask] = bin(u).count("1")

    # Enumerate draconian sequences (a_0, ..., a_5) with sum_{i in S} a_i <= |U_{i in S} I_i|
    ehr = [Fraction(0)]
    A = [0] * n

    def bt(step, s):
        nonlocal ehr
        if step == n:
            p = [Fraction(1)]
            for a in A:
                p = poly_mul(p, rising_binom_poly(a))
            ehr = poly_add(ehr, p)
            return
        ub = n - s
        for mask in range(1 << step):
            full = mask | (1 << step)
            rem = union_sz[full]
            for j in range(step):
                if (mask >> j) & 1:
                    rem -= A[j]
            if rem < ub:
                ub = rem
        if ub < 0:
            return
        for av in range(ub + 1):
            A[step] = av
            bt(step + 1, s + av)
        A[step] = 0

    bt(0, 0)
    M_y = ehr_to_magic(ehr, n)
    assert M_y == [Fraction(1), Fraction(59, 12), Fraction(439, 36), Fraction(2075, 144),
                   Fraction(335, 72), Fraction(-1, 6)]
    print(f"  Matched non-transitive Y-type sets (n=6): {[ [i for i in range(6) if (s>>i)&1] for s in sets ]}")
    print(f"  Magic polynomial M(y) = " + " + ".join(f"({M_y[i]})*y^{i}" for i in range(len(M_y))))
    print(f"  [OK] c_5 = {M_y[5]} < 0! Confirms transitivity (distributive lattice of filters) is essential.")


if __name__ == "__main__":
    phi, psi = verify_section_1()
    verify_section_2()
    verify_section_3(phi, psi)
    verify_section_4(phi)
    verify_section_5()
    print("\nALL VERIFICATION CHECKS PASSED WITH 100% EXACT RATIONAL ARITHMETIC.")
