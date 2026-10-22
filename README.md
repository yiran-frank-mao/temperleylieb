# temperleylieb — Temperley–Lieb diagrams in LaTeX

A LaTeX package (built on TikZ and expl3) that draws diagrams of the Temperley–Lieb algebra
\(TL_n(\delta)\) from words written the way you write them in mathematics:

```latex
\usepackage{temperleylieb}
...
\[ \TL{5}{e_1 e_4 e_3 e_2} \times \TL{5}{e_2 e_4 e_3}
   = \TL{5}{e_1 e_4 e_3 e_2 e_2 e_4 e_3}
   = \TL[reduce]{5}{e_1 e_4 e_3 e_2 e_2 e_4 e_3} \]
```

The last diagram is computed: the package traces the strands, removes closed loops and prints
\(\delta\) (or \(\delta^k\)) in front of the reduced diagram.

## Features

- **Composition**: `\TL{n}{e_i e_j ...}` glues the generators into one diagram (loops are drawn).
  `e_0` and `1` are the identity, and `e_{12}` works for two-digit indices.
- **Reduction**: `reduce` draws the resulting basis element with its power of \(\delta\).
  `\TLlastloops` gives the number of loops.
- **Side by side, not composed**: `separate` draws each generator on its own. Braces group
  generators that should still be composed (`{e_1 e_2}`). In the default mode, `|` splits a word
  into separate factors. `separator=\times` places a symbol between them, and `\TLgenerators{n}`
  draws \(1, e_1, \dots, e_{n-1}\).
- **Horizontal or vertical**: `horizontal` (the default, left to right) or `vertical`
  (top to bottom). `reverse` flips the direction.
- **Extras**: `names` (generator names under the diagram), `labels` (strand numbers),
  `boundaries` (dashed seams), `box=frame|fill|none`, `strand sep`, `length`, `scale`,
  `strand style`, `loop value`, and TikZ styles (`tl strand`, `tl box`, …) for full control.

```latex
\TLgenerators[names]{5}
\TL[separate, reduce, names]{3}{1 e_2 e_1 {e_1 e_2} {e_2 e_1}}   % the basis of TL_3
\TL[separator=\times]{5}{e_1 e_4 e_3 e_2 | e_2 e_4 e_3}
\TL[vertical, labels]{4}{e_1 e_2 e_3}
\tlset{box=fill, strand style={line width=1.3pt}}               % Wikipedia look
```

See [`temperleylieb-doc.pdf`](temperleylieb-doc.pdf) for the full manual and
[`examples/wikipedia.pdf`](examples/wikipedia.pdf) for a reproduction of the figures from the
Wikipedia article.

## Installation

Copy `temperleylieb.sty` next to your document, or into your local `texmf` tree
(for example `~/texmf/tex/latex/temperleylieb/`). It requires a LaTeX kernel from 2020-10
or newer and TikZ, and works with pdfLaTeX, XeLaTeX and LuaLaTeX.

## Building the documentation and running tests

```sh
make            # builds temperleylieb-doc.pdf and examples/wikipedia.pdf
make test       # cross-checks the reduction against a Python reference on random words
```

On Debian/Ubuntu the required TeX packages are
`texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-pictures`.

## Files

| File | Purpose |
| --- | --- |
| `temperleylieb.sty` | the package |
| `temperleylieb-doc.tex` / `.pdf` | user manual with live examples |
| `examples/wikipedia.tex` / `.pdf` | the Wikipedia figures redrawn with the package |
| `tests/check_reduce.py` | randomized test of the composition/reduction algorithm |
| `tests/test.tex` | visual smoke test |

Licensed under the LaTeX Project Public License 1.3c.
