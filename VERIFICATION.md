# Verification coverage

The [parking-function verifier](disproved/hill-luo-trinh-vindas-melendez-conj-8.1-counterexample/verify.py) and [preorder verifier](proofs/athanasiadis-chapoton-conj-4.8-proof/verify.py) require Python 3.10 or later and the standard library. Run them without `-O` or `PYTHONOPTIMIZE`. Polynomial coefficients, counts, and root certificates use integers or exact fractions.

## Parking-function polytopes

| Certificate | Lattice-count check | Algebraic check |
| --- | --- | --- |
| Affine e₁ and both bivariate quadratics | Count from the defining inequalities at dilates 0 through 14 for six unisolvent parameter pairs. Also check (2, 2). | Extract e₁ and e₂ from Theorem 5.9 of Hill et al. Use the monomial-to-magic identity to obtain μ₂. Compare all polynomial coefficients. |
| All four dimension-14 rows in Table 1 | Evaluate the interpolated family polynomials at the displayed parameter pairs. | Extract the coefficients at each actual vector and assert both rational values. |
| Dimension-18 and dimension-20 rows | Count directly at each displayed vector for every dilate from 0 through the dimension, then interpolate. | Extract e₁ and e₂ separately and assert both reported coefficients and their signs. |
| The dimension-14 uniform-matroid sum | Count from the uniform rank bounds and interpolate. | Extract e₂ from the homogeneous quadratic part of the draconian formula. |
| Mixed coefficients in dimensions 13 and 14 | Interpolate the appropriate Ehrhart coefficient of each uniform-matroid sum and take inclusion–exclusion. | Extract the homogeneous coefficients from the draconian formula using supports of size at most two and three, respectively. |
| Minimum largest entries 228 and 253 | The input quadratics are independently recovered by small-parameter interpolation. | Exhaust the integer boxes immediately below and at each threshold. Assert the minima, their attaining pairs, and the two negative witness values. |

The direct count processes coordinate values in decreasing order. A state records the number of assigned coordinates and their sum. Concavity of the sorted-prefix bounds permits a shortcut when all remaining coordinates could equal the current bound without violating the total-sum inequality. In the worst case with dimension `n`, largest one-coordinate bound `B1`, and total-sum bound `Bn`, a dilation uses O((B1+1) n² (Bn+1)) integer operations and O(n (Bn+1)) states, ignoring the cost of large-integer arithmetic. Support-two extraction uses at most O(n⁴) rational operations. Support-three extraction visits the weak compositions of the dimension into the eight Venn regions of three sets.

The final run takes about 17–19 seconds on the tested machine. Direct counting at the four large-entry dimension-14 vectors was avoided because lattice bounds grow with the largest weight and the dilation. Small-parameter interpolation determines the full quadratics and thus supplies a second check at those actual vectors. The two minimality results concern the signs of the indicated second coefficients within the specified two-parameter family. The least dimension of a positive-integer counterexample and the signs of mixed coefficients in dimensions 11 and 12 are outside the verified scope.

Check the output for these lines.

```text
Bivariate e_1, e_2 and mu_2: direct interpolation and draconian extraction agree
Minimum max(b_i) for mu_2 < 0 in the two-parameter family: 228
Minimum max(b_i) for e_2 < 0 in the two-parameter family: 253
Uniform sum [t^2] Ehr(U_5 + U_9) = -36952721/3880800 (both methods)
Dimension 13 mixed coefficient = -842231/69300 (both methods)
Dimension 14 mixed coefficient = -125057/450 (both methods)
ALL CHECKS PASSED
```

The original diagonal interpolation values of μ₂ at shifts 0, 1, and 2 are also asserted: 29211/4, 38762683049/3880800, and 2046289519/161700.

## Preorder polytopes

| Claim or example | Check |
| --- | --- |
| Formal-series identities | Exact coefficients through degree 12 for the two series and binomial expansions. Exact bivariate polynomial comparison for the reciprocity of P(W; u, v) through W = 9. |
| Signed Vandermonde identity | Signed weights on 120 seeded preorders plus four fixed boundary cases. Compare the restricted binomial sum and test the inductive vanishing for the short ranges specified in the script. |
| Master formula, magic positivity, and consequences | Direct counts through the dimension, Lagrange interpolation, and exact polynomial comparison on 12 nonempty preorders and the empty case. Check the word-descent formula by enumeration and the zeta value via the dual Ehrhart evaluation. |
| Running example (Figure 1 of Athanasiadis–Chapoton) | Assert 13 contributing vectors and both displayed polynomials. |
| Patel’s eight-element poset | Count every interpolation dilate from 0 through 8 using Patel’s upper-subset inequalities. Compare to the full ideal system through dilate 3. Assert the displayed polynomials and use exact Sturm sequences for both root counts. |
| Non-transitive matched example | The draconian sum gives the complete magic polynomial, with c₅ = −1/6. This example uses a single exact enumeration method. |

The final run takes about 1.5–1.6 seconds on the tested machine. Order-filter enumeration and lattice-point backtracking can grow exponentially with the ground set, and word enumeration can grow factorially. The verifier runs the fixed fixtures listed above. The general theorem statements rest on the written proofs. The zeta check uses the original authors’ duality. Direct interpolation of the zeta polynomial from multichains is outside its scope.

Check the output for these lines.

```text
[OK] Empty, zero-weight, and signed zero-total boundary cases
[OK] Verified A_F(r) = 0 and S(tau, w, m) = binom(W_E, m) on 120 random
[OK] Direct lattice counts for m=0..8 match and all seven h* roots are real
[OK] c_5 = -1/6 < 0 for the matched non-transitive example
ALL CHECKS PASSED
```

## Build the PDFs

The standalone sources use AMS-LaTeX theorem and equation environments with Libertinus Serif and Libertinus Math. Build with Tectonic and its TeX bundle. For inspection, rasterize the resulting PDF with Poppler. Run these commands from either project directory.

```sh
tectonic --keep-logs paper.tex
pdftoppm -r 116 -png paper.pdf page
```

Builds were tested using Tectonic 0.17.0. The final exact verifier runs were performed with CPython 3.12.14 and 3.14.0 on macOS arm64.
