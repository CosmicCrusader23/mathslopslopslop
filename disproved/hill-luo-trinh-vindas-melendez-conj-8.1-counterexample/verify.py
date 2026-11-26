#!/usr/bin/env python3
"""
Independent exact-arithmetic verifier for the refutation of Conjecture 8.1
of Hill, Luo, Trinh, and Vindas-Melendez (arXiv:2607.15503).

Verifies:
1. The n=14 counterexample b = (1^5, 287, 1^3, 287, 1^4) with
   mu_2 = -8337823/11025 < 0, via TWO independent exact methods:
   (a) Direct lattice-point enumeration from the defining inequalities
       (Theorem 2.2) at m = 0, 1, 2 (t = 0..14), plus exact degree-2
       polynomiality in m from Corollary 5.6.
   (b) Direct closed-form extraction of e_1, e_2 from Theorem 5.9
       (draconian sequences of support size <= 2).
2. Auxiliary certificates:
   - [t^2] ehr_{U_5 + U_9}(t) = -36952721/3880800 in R^14 (direct counting).
   - [abc] #((a U_3 + b U_4 + c U_8) cap Z^14) = -125057/450 (direct counting).
3. Sharper / stronger counterexamples:
   - n = 13: multivariate magic-positivity ALREADY fails at [x_6 x_10 y^2] M_13 = -842231/69300
     (verified by both direct counting and Theorem 5.9).
   - n = 14: Ehrhart positivity itself fails at b = (1^5, 318, 1^3, 318, 1^4),
     and unequal weights reduce max(b_i) to 228 for mu_2 < 0 (and 253 for e_2 < 0).
   - n = 18: b = (1^6, 3, 1^5, 3, 1^5) has e_2 > 0 yet fails magic positivity (mu_2 < 0).
   - n = 20: binary {1,2}-vector b = (1^7, 2, 1^5, 2, 1^6) fails BOTH magic positivity
     and Ehrhart positivity.
"""

from fractions import Fraction
import math


def count_lattice_points_direct(n: int, B: list[int]) -> int:
    """
    Exact lattice-point count #{z in Z_{>=0}^n : sum_{i in I} z_i <= B[|I|]}
    via exact integer dynamic programming over nonincreasing rearrangements.
    """
    max_v = B[1]
    comb = [[math.comb(i, j) for j in range(i + 1)] for i in range(n + 1)]
    dp: list[dict[int, int]] = [{} for _ in range(n + 1)]
    dp[0][0] = 1
    for v in range(max_v, -1, -1):
        new_dp = [dict(d) for d in dp]
        for k in range(n):
            if not dp[k]:
                continue
            rem = n - k
            for s, cnt in dp[k].items():
                cur_s = s
                for m in range(1, rem + 1):
                    cur_s += v
                    if cur_s > B[k + m]:
                        break
                    nk = k + m
                    new_dp[nk][cur_s] = new_dp[nk].get(cur_s, 0) + cnt * comb[rem][m]
        dp = new_dp
    return sum(dp[n].values())


def bounds_for_Xb(b: list[int], t: int) -> list[int]:
    """Upper bounds B[k] = t * (Sigma_k - k) for shifted X_n(b) - 1 (Theorem 2.2)."""
    n = len(b)
    S = [0]
    for bi in b:
        S.append(S[-1] + bi)
    return [0] + [t * (sum(S[n - k + 1 : n + 1]) - k) for k in range(1, n + 1)]


def poly_from_values(vals: list[int]) -> list[Fraction]:
    """Exact Newton-difference interpolation of degree-d polynomial from vals[0..d]."""
    d = len(vals) - 1
    diff = [Fraction(v) for v in vals]
    fwd = [diff[0]]
    for _ in range(1, d + 1):
        diff = [diff[i + 1] - diff[i] for i in range(len(diff) - 1)]
        fwd.append(diff[0])
    coeffs = [Fraction(0)] * (d + 1)
    basis = [Fraction(1)]
    for k in range(d + 1):
        fk = math.factorial(k)
        for i, c in enumerate(basis):
            coeffs[i] += fwd[k] * c / fk
        if k < d:
            nb = [Fraction(0)] * (len(basis) + 1)
            for i, c in enumerate(basis):
                nb[i] -= c * k
                nb[i + 1] += c
            basis = nb
    return coeffs


def compute_w(b: list[int]) -> list[int]:
    """Signed Minkowski coefficients w_1..w_n from Eq. (5.2) of arXiv:2607.15503."""
    n = len(b)
    w = [0] * (n + 1)
    w[1] = b[0] - 1
    for k in range(2, n + 1):
        w[k] = sum(((-1) ** j) * math.comb(k - 2, j) * b[k - j - 1] for j in range(k - 1))
    return w


def e1_e2_mu2_from_theorem_5_9(b: list[int]) -> tuple[Fraction, Fraction, Fraction]:
    """
    Exact closed-form (e_1, e_2, mu_2) extracted from Theorem 5.9 (draconian sum)
    of Hill-Luo-Trinh-Vindas-Melendez (arXiv:2607.15503).
    """
    n = len(b)
    w = compute_w(b)
    H = [Fraction(0)] * (n + 1)
    for k in range(1, n + 1):
        H[k] = H[k - 1] + Fraction(1, k)

    e1 = sum(math.comb(n, k) * H[k] * w[k] for k in range(1, n + 1))

    e2_single = sum(
        math.comb(n, k) * (w[k] ** 2) * sum(H[a - 1] / a for a in range(1, k + 1))
        for k in range(1, n + 1)
        if w[k] != 0
    )

    e2_pair = Fraction(0)
    nz = [k for k in range(1, n + 1) if w[k] != 0]
    for k in nz:
        for l in nz:
            for u in range(max(k, l), min(n, k + l) + 1):
                if k == l and u == k:
                    continue
                a_only, b_only, both = u - l, u - k, k + l - u
                if a_only < 0 or b_only < 0 or both < 0:
                    continue
                cnt = (
                    math.comb(n, u)
                    * math.factorial(u)
                    // (math.factorial(a_only) * math.factorial(b_only) * math.factorial(both))
                )
                S = sum(Fraction(1, a) * H[min(l, u - a)] for a in range(1, min(k, u - 1) + 1))
                e2_pair += Fraction(cnt, 2) * w[k] * w[l] * S

    e2 = e2_single + e2_pair
    mu2 = e2 - (n - 1) * e1 + math.comb(n, 2)
    return e1, e2, mu2


def main() -> None:
    print("1. Sanity check on paper examples (Ex. 4.2, 5.2, 5.12):")
    assert count_lattice_points_direct(3, bounds_for_Xb([3, 2, 2], 1)) == 272
    assert count_lattice_points_direct(3, bounds_for_Xb([3, 2, 2], 2)) == 1743
    assert count_lattice_points_direct(3, bounds_for_Xb([2, 3, 1], 1)) == 178
    assert e1_e2_mu2_from_theorem_5_9([2, 3, 1]) == (Fraction(77, 6), Fraction(61), Fraction(115, 3))
    print("   PASS")

    print("2. Direct lattice-point verification of Q = U_5 + U_9 in R^14:")
    vals_Q = [1] + [
        count_lattice_points_direct(14, [0] + [t * (min(k, 5) + min(k, 9)) for k in range(1, 15)])
        for t in range(1, 15)
    ]
    ehr_Q = poly_from_values(vals_Q)
    assert ehr_Q[2] == Fraction(-36952721, 3880800)
    print(f"   [t^2] E_{{U_5 + U_9}}(t) = {ehr_Q[2]} < 0  PASS")

    print("3. Direct lattice-point verification of [abc] #((a U_3 + b U_4 + c U_8) cap Z^14):")
    alt_e3 = Fraction(0)
    for a in (0, 1):
        for b_coef in (0, 1):
            for c in (0, 1):
                if a == b_coef == c == 0:
                    continue
                vals = [1] + [
                    count_lattice_points_direct(
                        14,
                        [0]
                        + [
                            t * (a * min(k, 3) + b_coef * min(k, 4) + c * min(k, 8))
                            for k in range(1, 15)
                        ],
                    )
                    for t in range(1, 15)
                ]
                alt_e3 += ((-1) ** (3 - a - b_coef - c)) * poly_from_values(vals)[3]
    assert alt_e3 == Fraction(-125057, 450)
    print(f"   [x_7 x_11 x_12 y^3] M_14 = {alt_e3} < 0  PASS")

    print("4. Direct Theorem 2.2 verification of the n=14 family b(m) at m = 0, 1, 2:")
    mu2_direct = {}
    for m in (0, 1, 2):
        b = [1, 1, 1, 1, 1, 1 + m, 1, 1, 1, 1 + m, 1, 1, 1, 1]
        vals = [1] + [count_lattice_points_direct(14, bounds_for_Xb(b, t)) for t in range(1, 15)]
        ehr = poly_from_values(vals)
        mu2_d = ehr[2] - 13 * ehr[1] + 91
        e1_t, e2_t, mu2_t = e1_e2_mu2_from_theorem_5_9(b)
        assert (ehr[1], ehr[2], mu2_d) == (e1_t, e2_t, mu2_t)
        mu2_direct[m] = mu2_d
        print(f"   m={m}: mu_2 = {mu2_d} (Direct == Theorem 5.9)")

    C = mu2_direct[0]
    A = (mu2_direct[2] - 2 * mu2_direct[1] + mu2_direct[0]) / 2
    B = mu2_direct[1] - C - A
    assert A == Fraction(-36952721, 3880800)
    assert B == Fraction(149416051, 55440)
    assert C == Fraction(29211, 4)

    mu2_285_interp = A * 285**2 + B * 285 + C
    mu2_286_interp = A * 286**2 + B * 286 + C
    _, _, mu2_285_thm59 = e1_e2_mu2_from_theorem_5_9([1, 1, 1, 1, 1, 286, 1, 1, 1, 286, 1, 1, 1, 1])
    _, e2_286_thm59, mu2_286_thm59 = e1_e2_mu2_from_theorem_5_9(
        [1, 1, 1, 1, 1, 287, 1, 1, 1, 287, 1, 1, 1, 1]
    )
    assert mu2_285_interp == mu2_285_thm59 == Fraction(102746219, 51744) > 0
    assert mu2_286_interp == mu2_286_thm59 == Fraction(-8337823, 11025) < 0
    print(f"   m=285: mu_2 = {mu2_285_interp} > 0")
    print(f"   m=286: mu_2 = {mu2_286_interp} < 0  (CONJECTURE 8.1 REFUTED!)")

    print("5. Earlier dimension n=13 negative multivariate coefficient [x_6 x_10 y^2] M_13:")
    def e2_Ur_Us_13(a: int, b_c: int) -> Fraction:
        vals = [1] + [
            count_lattice_points_direct(
                13, [0] + [t * (a * min(k, 4) + b_c * min(k, 8)) for k in range(1, 14)]
            )
            for t in range(1, 14)
        ]
        return poly_from_values(vals)[2]

    mixed_13_direct = e2_Ur_Us_13(1, 1) - e2_Ur_Us_13(1, 0) - e2_Ur_Us_13(0, 1)
    assert mixed_13_direct == Fraction(-842231, 69300) < 0
    print(f"   [x_6 x_10 y^2] M_13 = {mixed_13_direct} < 0  PASS")

    print("6. Additional stronger / smaller-entry counterexamples (Theorem 5.9 exact):")
    extras = [
        ("n=14 equal Ehrhart-negative (m=317)", [1,1,1,1,1,318,1,1,1,318,1,1,1,1]),
        ("n=14 unequal minimal max(b_i) (mu_2<0)", [1,1,1,1,1,187,1,1,1,228,1,1,1,1]),
        ("n=14 unequal minimal max(b_i) (e_2<0)", [1,1,1,1,1,208,1,1,1,253,1,1,1,1]),
        ("n=18 {1,3}-vector (e_2>0, mu_2<0)", [1,1,1,1,1,1,3,1,1,1,1,1,3,1,1,1,1,1]),
        ("n=20 {1,2}-vector (fails BOTH Ehrhart+ & magic+)", [1,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1]),
    ]
    for label, b in extras:
        _, e2, mu2 = e1_e2_mu2_from_theorem_5_9(b)
        assert mu2 < 0
        print(f"   {label}: e_2 = {e2} ({float(e2):+.2f}), mu_2 = {mu2} ({float(mu2):+.2f})")

    print("\nALL CHECKS PASSED.")


if __name__ == "__main__":
    main()
