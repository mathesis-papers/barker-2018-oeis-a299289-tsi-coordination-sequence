# Prism-tiling conjectures of Barker and Spezia

The note proves the conjectural formula blocks in OEIS A299289 revision 16
and A299290 revision 10. It gives the exact graph metric, shell and ball
counts, ordinary and exponential generating functions, and recurrences.
The scale-two metric framework is credited to Deza and Shtogrin
(1999/2000); the note gives explicit coordinates and exact enumeration.
It also proves shell bounds for arbitrary square-faced triangular-prism
stacks, including nonperiodic stacks, and gives a period-four stack whose
origin coordination sequence agrees with the alternating tiling although
its radius-two shell has 26 vertices at another center rather than 28.
The constant-orientation specialization recovers the known `hex` shell
and ball formulas and series in OEIS A005897 and A005898, with attribution.

## Build

Build `note.tex` with Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively, run `pdflatex note.tex` twice. The bibliography is included
in the TeX source; no BibTeX database is required. An online first build
may download the TeX packages used by the engine.

## Exact finite checks

Python 3.10 or later, using the standard library:

```sh
python3 verify.py --output checks.json
```

The checker uses exact integers and rational numbers. At its default radius
32 it compares graph distance with the metric on every vertex of the ball,
checks the displayed OEIS prefixes, partial sums and both ordinary series
and recurrences through index 1000, and the exponential series through
index 100. It checks edges from the box `[-8,8]^3` and distances and shells
through radius 6 at three additional centers.

For arbitrary orientations it enumerates all 1024 direction assignments to
slabs -5 through 4, searches each graph through radius 5, and compares every
distance and shell with the formulas and bounds. The period-four example
is checked through index 1000. These are finite checks; the all-radius
statements have mathematical proofs in the note. Exact ranges and counts
are recorded in `checks.json`.

## Formal statement

The linked declaration
`D5.S3.StatisticalMechanics.TsiCoordinationSequence.result` proves the two
positive-radius origin shell formulas for `tsiGraph`:

https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/StatisticalMechanics/TsiCoordinationSequence.lean

The Euclidean identification, all-center statement, generating functions,
ball identities, arbitrary-stack bounds and nonuniqueness example have
written proofs in the note. They are not additional conjuncts of that
declaration.

Haobo Ma (ChronoAI Pte Ltd, Singapore), then Wenlin Zhang (National University
of Singapore; ChronoAI Pte Ltd, Singapore). CC BY 4.0; see `LICENSE.txt`.
