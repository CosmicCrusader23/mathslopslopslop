#!/usr/bin/env python3
"""Exact certificates for Conjecture 8.1 of arXiv:2607.15503 (Python 3.10+)."""

from argparse import ArgumentParser
from fractions import Fraction
from functools import cache
from itertools import product
import math


def count_lattice_points_direct(n: int, B: list[int]) -> int:
    """
    Exact lattice-point count #{z in Z_{>=0}^n : sum_{i in I} z_i <= B[|I|]}
    via exact integer dynamic programming over nonincreasing rearrangements.
    """
    comb = [[math.comb(i, j) for j in range(i + 1)] for i in range(n + 1)]
    dp: list[dict[int, int]] = [{} for _ in range(n + 1)]
    dp[0][0] = 1
    total = 0
    for v in range(B[1], -1, -1):
        next_dp: list[dict[int, int]] = [{} for _ in range(n + 1)]
        powers = [(v + 1) ** r for r in range(n + 1)]
        for k, states in enumerate(dp):
            remaining = n - k
            for s, count in states.items():
                # B is concave. If the line s + j*v is below B at the
                # two endpoints j=0 and j=remaining, every completion fits.
                if s + remaining * v <= B[n]:
                    total += count * powers[remaining]
                    continue
                partial_sum = s
                for copies in range(remaining):
                    used = k + copies
                    if partial_sum > B[used]:
                        break
                    target = next_dp[used]
                    target[partial_sum] = target.get(partial_sum, 0) + count * comb[remaining][copies]
                    partial_sum += v
        dp = next_dp
    return total


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
    return coefficients_from_weights(compute_w(b))


def coefficients_from_weights(w: list[int]) -> tuple[Fraction, Fraction, Fraction]:
    n = len(w) - 1
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


def parameter_vector(n: int, changes: dict[int, int]) -> list[int]:
    """Increase entries of the all-ones vector at the given one-based positions."""
    return [1 + changes.get(i, 0) for i in range(1, n + 1)]


def direct_coefficients(b: list[int]) -> tuple[Fraction, Fraction, Fraction]:
    n = len(b)
    counts = [count_lattice_points_direct(n, bounds_for_Xb(b, t)) for t in range(n + 1)]
    _, e1, e2, *_ = poly_from_values(counts)
    return e1, e2, e2 - (n - 1) * e1 + math.comb(n, 2)


def uniform_sum_coefficient(n: int, ranks: list[int], degree: int) -> Fraction:
    rank_bounds = [sum(min(k, r) for r in ranks) for k in range(n + 1)]
    counts = [count_lattice_points_direct(n, [t * b for b in rank_bounds]) for t in range(n + 1)]
    return poly_from_values(counts)[degree]


def uniform_weights(n: int, rank: int) -> list[int]:
    # Subtract the base weights to isolate the summand U_rank in the Minkowski decomposition.
    base = compute_w([1] * n)
    shifted = compute_w(parameter_vector(n, {n - rank + 1: 1}))
    return [w - w0 for w, w0 in zip(shifted, base)]


def compositions(total: int, parts: int):
    """Weak compositions of total into a specified number of parts."""
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            yield (first, *rest)


def cubic_draconian_coefficient(n: int, ranks: list[int]) -> Fraction:
    """Extract the product of three distinct parameters in [t^3] by Hall constraints."""
    assert len(ranks) == 3
    directions = list(zip(*(uniform_weights(n, rank) for rank in ranks)))
    scale = math.lcm(*range(1, n + 1))
    reciprocal = [0] + [scale // a for a in range(1, n + 1)]
    harmonic = [0] * (n + 1)
    second = [0] * (n + 1)
    third_prefix = [0] * (n + 1)
    pair_sum = 0
    # For support multiplicity a, the binomial factor is x/a times
    # product_{j<a}(1+x/j). Scale its x^j coefficient by scale^j.
    for a in range(1, n + 1):
        second[a] = reciprocal[a] * harmonic[a - 1]
        third_prefix[a] = third_prefix[a - 1] + reciprocal[a] * pair_sum
        pair_sum += second[a]
        harmonic[a] = harmonic[a - 1] + reciprocal[a]

    @cache
    def mixed_product(k: int, l: int, m: int) -> int:
        p, q, r = directions[k], directions[l], directions[m]
        return (
            p[0] * (q[1] * r[2] + q[2] * r[1])
            + p[1] * (q[0] * r[2] + q[2] * r[0])
            + p[2] * (q[0] * r[1] + q[1] * r[0])
        )

    factorial = [math.factorial(k) for k in range(n + 1)]
    supported_sizes = [k for k in range(1, n + 1) if any(directions[k])]
    one = sum(math.comb(n, k) * third_prefix[k] * mixed_product(k, k, k) for k in supported_sizes)
    two = 0
    for k, l in product(supported_sizes, repeat=2):
        mixed = mixed_product(k, k, l)
        if mixed == 0:
            continue
        for u in range(max(k, l), min(n, k + l) + 1):
            if k == l == u:
                continue
            ordered = factorial[n] // (
                factorial[n - u] * factorial[u - l] * factorial[u - k] * factorial[k + l - u]
            )
            weights = sum(second[a] * harmonic[min(l, u - a)] for a in range(1, min(k, u - 1) + 1))
            two += ordered * mixed * weights

    # Assign each ground-set element to one of the eight Venn regions of A, B, C.
    # The all-three and pairwise unions bound the allowed support multiplicities.
    three = 0
    for cells in compositions(n, 8):
        outside, a_only, b_only, c_only, ab, ac, bc, abc = cells
        k, l, m = a_only + ab + ac + abc, b_only + ab + bc + abc, c_only + ac + bc + abc
        u = n - outside
        u_ab, u_ac, u_bc = u - c_only, u - b_only, u - a_only
        if u_ab == k == l or u_ac == k == m or u_bc == l == m:
            continue
        mixed = mixed_product(k, l, m)
        if mixed == 0:
            continue
        weights = 0
        for a in range(1, k + 1):
            for b in range(1, min(l, u_ab - a) + 1):
                c_max = min(m, u_ac - a, u_bc - b, u - a - b)
                if c_max > 0:
                    weights += reciprocal[a] * reciprocal[b] * harmonic[c_max]
        ordered = factorial[n] // math.prod(factorial[cell] for cell in cells)
        three += ordered * mixed * weights
    # The two-set sum distinguishes the squared factor; the three-set sum orders all three sets.
    return Fraction(6 * (one + two) + three, 6 * scale**3)


def quadratic_coefficients(values: dict[tuple[int, int], Fraction]) -> tuple[Fraction, ...]:
    """Coefficients in the order a^2, ab, b^2, a, b, 1 from six samples."""
    constant = values[0, 0]
    aa = (values[2, 0] - 2 * values[1, 0] + constant) / 2
    bb = (values[0, 2] - 2 * values[0, 1] + constant) / 2
    ab = values[1, 1] - values[1, 0] - values[0, 1] + constant
    a = values[1, 0] - aa - constant
    b = values[0, 1] - bb - constant
    return aa, ab, bb, a, b, constant


DENOMINATOR = 50450400
E1_NUMERATORS = (0, 0, 0, 4613814, 3546355, 49189140)
E2_NUMERATORS = (4092523257, -7085907205, 2512998575, 84978997740, 65841116250, 453359907000)
MU2_NUMERATORS = (4092523257, -7085907205, 2512998575, 76581856260, 59386750150, 368426658600)


def evaluate(coefficients: tuple[int, ...], a: int, b: int) -> int:
    aa, ab, bb, la, lb, constant = coefficients
    return (aa * a + ab * b + la) * a + (bb * b + lb) * b + constant


def family_coefficients(a: int, b: int) -> tuple[Fraction, Fraction, Fraction]:
    return (
        Fraction(evaluate(E1_NUMERATORS, a, b), 360360),
        Fraction(evaluate(E2_NUMERATORS, a, b), DENOMINATOR),
        Fraction(evaluate(MU2_NUMERATORS, a, b), DENOMINATOR),
    )


def verify_bivariate_family() -> None:
    points = ((0, 0), (1, 0), (2, 0), (0, 1), (0, 2), (1, 1))
    checks = (
        (E1_NUMERATORS, 360360), (E2_NUMERATORS, DENOMINATOR), (MU2_NUMERATORS, DENOMINATOR)
    )
    samples = {}
    for a, b in (*points, (2, 2)):
        vector = parameter_vector(14, {6: a, 10: b})
        direct = direct_coefficients(vector)
        assert direct == e1_e2_mu2_from_theorem_5_9(vector) == family_coefficients(a, b)
        samples[a, b] = direct
    for index, (numerators, denominator) in enumerate(checks):
        observed = quadratic_coefficients({p: samples[p][index] for p in points})
        assert observed == tuple(Fraction(c, denominator) for c in numerators)
    assert samples[0, 0][2] == Fraction(29211, 4)
    assert samples[1, 1][2] == Fraction(38762683049, 3880800)
    assert samples[2, 2][2] == Fraction(2046289519, 161700)
    assert Fraction(sum(E1_NUMERATORS[3:5]), 360360) == Fraction(8160169, 360360)
    assert tuple(Fraction(x, DENOMINATOR) for x in (
        sum(MU2_NUMERATORS[:3]), sum(MU2_NUMERATORS[3:5]), MU2_NUMERATORS[5]
    )) == (Fraction(-36952721, 3880800), Fraction(149416051, 55440), Fraction(29211, 4))
    assert family_coefficients(285, 285)[2] == Fraction(102746219, 51744) > 0
    assert family_coefficients(316, 316)[1] == Fraction(688240969, 242550) > 0
    print("Bivariate e_1, e_2 and mu_2: direct interpolation and draconian extraction agree")


def verify_minimality() -> None:
    checks = (
        ("mu_2", MU2_NUMERATORS, 226, (186, 226), Fraction(653047639, 300300),
         (187, 227), Fraction(-15899536567, 50450400), (186, 227)),
        ("e_2", E2_NUMERATORS, 251, (207, 251), Fraction(12800604359, 7207200),
         (208, 252), Fraction(-516371122, 525525), (207, 252)),
    )
    for name, coefficients, bound, low_at, low, high_at, high, witness in checks:
        for limit, at, expected in ((bound, low_at, low), (bound + 1, high_at, high)):
            minimum, a, b = min(
                (evaluate(coefficients, a, b), a, b)
                for a, b in product(range(limit + 1), repeat=2)
            )
            assert (a, b) == at and Fraction(minimum, DENOMINATOR) == expected
        assert low > 0 > high and max(witness) == bound + 1
        assert evaluate(coefficients, *witness) < 0
        print(f"Minimum max(b_i) for {name} < 0 in the two-parameter family: {bound + 2}")


def verify_mixed_coefficients() -> None:
    weights = [a + b for a, b in zip(uniform_weights(14, 5), uniform_weights(14, 9))]
    direct = uniform_sum_coefficient(14, [5, 9], 2)
    assert direct == coefficients_from_weights(weights)[1] == Fraction(-36952721, 3880800) < 0
    print(f"Uniform sum [t^2] Ehr(U_5 + U_9) = {direct} (both methods)")

    for n, ranks, expected in (
        (13, [4, 8], Fraction(-842231, 69300)),
        (14, [3, 4, 8], Fraction(-125057, 450)),
    ):
        degree = len(ranks)
        direct = Fraction(0)
        draconian = Fraction(0)
        for included in product((0, 1), repeat=degree):
            subset = [rank for rank, use in zip(ranks, included) if use]
            if not subset:
                continue
            sign = (-1) ** (degree - len(subset))
            direct += sign * uniform_sum_coefficient(n, subset, degree)
            if degree == 2:
                weights = [sum(terms) for terms in zip(*(uniform_weights(n, rank) for rank in subset))]
                draconian += sign * coefficients_from_weights(weights)[1]
        if degree == 3:
            draconian = cubic_draconian_coefficient(n, ranks)
        assert direct == draconian == expected < 0
        print(f"Dimension {n} mixed coefficient = {direct} (both methods)")


def verify_table(skip_large_direct: bool) -> None:
    cases = (
        (14, {6: 286, 10: 286}, Fraction(3753767953, 44100), Fraction(-8337823, 11025)),
        (14, {6: 317, 10: 317}, Fraction(-777669659, 3880800), Fraction(-11195736263, 117600)),
        (14, {6: 186, 10: 227}, Fraction(3101451036227, 50450400), Fraction(-10491632153, 50450400)),
        (14, {6: 207, 10: 252}, Fraction(-5255462383, 5605600), Fraction(-35322635893, 509600)),
        (18, {7: 2, 13: 2}, Fraction(22435315633, 6306300), Fraction(-3708081001, 3153150)),
        (20, {8: 1, 14: 1}, Fraction(-10007742397957, 908107200), Fraction(-260316261282989, 15437822400)),
    )
    for n, shifts, expected_e2, expected_mu2 in cases:
        b = parameter_vector(n, shifts)
        coefficients = e1_e2_mu2_from_theorem_5_9(b)
        _, e2, mu2 = coefficients
        assert e2 == expected_e2 and mu2 == expected_mu2 < 0
        if n == 14:
            assert family_coefficients(*shifts.values()) == coefficients
            method = "draconian and direct family interpolation"
        elif skip_large_direct:
            method = "draconian; direct enumeration skipped by request"
        else:
            assert direct_coefficients(b) == coefficients
            method = "draconian and direct enumeration"
        print(f"n={n}, shifts={shifts}: e_2 = {e2}, mu_2 = {mu2} ({method})")


def main() -> None:
    if not __debug__:
        raise SystemExit("Run without Python optimization so every assertion is enabled.")
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--skip-large-direct", action="store_true", help="skip direct counting in dimensions 18 and 20")
    args = parser.parse_args()

    assert count_lattice_points_direct(3, bounds_for_Xb([3, 2, 2], 1)) == 272
    assert count_lattice_points_direct(3, bounds_for_Xb([3, 2, 2], 2)) == 1743
    assert count_lattice_points_direct(3, bounds_for_Xb([2, 3, 1], 1)) == 178
    example = (Fraction(77, 6), Fraction(61), Fraction(115, 3))
    assert direct_coefficients([2, 3, 1]) == e1_e2_mu2_from_theorem_5_9([2, 3, 1]) == example
    verify_bivariate_family()
    verify_minimality()
    verify_table(args.skip_large_direct)
    verify_mixed_coefficients()
    print("PASS with optional counts skipped" if args.skip_large_direct else "ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
