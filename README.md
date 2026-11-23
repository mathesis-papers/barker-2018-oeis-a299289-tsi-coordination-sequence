# Prism-stack shell bounds and proofs of Barker's and Spezia's conjectures

**Authors:** Haobo Ma, Wenlin Zhang

Extending Deza and Shtogrin's scale-two metric description (1999/2000, Tables 3-4) to exact shell enumeration, we prove Colin Barker's conjectures in the formula block of OEIS A299289, revision 16 (formulas dated February 11, 2018), and Stefano Spezia's conjectured exponential generating function in the same block (June 8, 2024), by expressing distance in the alternating-prism tiling as layer distance plus distance to an integer rectangle. The shell counts are a(0)=1 and 2a(n)=13n^2+4 for positive even n, or 13n^2+3 for odd n. They imply all of Barker's partial-sum conjectures in A299290, revision 10, formula block (February 11, 2018). For arbitrary stacks of square-faced triangular-prism slabs, the metric gives sharp shell bounds; a nonalternating stack can have the same coordination sequence at one center but a different sequence at another.

- PDF: [frozen public file](paper.pdf)
- DOI: [https://doi.org/10.5281/zenodo.24482895](https://doi.org/10.5281/zenodo.24482895)
- Concept DOI: [https://doi.org/10.5281/zenodo.24482894](https://doi.org/10.5281/zenodo.24482894)
- License: CC-BY-4.0
- Version: 2
- Mathesis record: [barker-2018-oeis-a299289-tsi-coordination-sequence](https://mathesis-omega-research.apps.chrono-ai.fun/papers/barker-2018-oeis-a299289-tsi-coordination-sequence?version=2)

## How to cite

Haobo Ma, Wenlin Zhang (2026). Prism-stack shell bounds and proofs of Barker's and Spezia's conjectures. Mathesis, version 2. https://doi.org/10.5281/zenodo.24482895

## Statement progress

| Statement | Formalization status | Source | Verification basis |
|---|---|---|---|
| Theorem (s1) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/StatisticalMechanics/TsiCoordinationSequence.lean) | No public receipt |
| Corollary (s2) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/StatisticalMechanics/TsiCoordinationSequence.lean) | No public receipt |
| Corollary (s3) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/StatisticalMechanics/TsiCoordinationSequence.lean) | No public receipt |
| Corollary (s4) | preparing | [Lean source](https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/StatisticalMechanics/TsiCoordinationSequence.lean) | No public receipt |

## Contributions

Original authors are listed above. Formalization contributors and attribution are retained in `formalization/nodes.json`; repository pull requests do not confer verification or credit. Submit formalization attempts through the Mathesis attempt path described in [CONTRIBUTING.md](CONTRIBUTING.md).
