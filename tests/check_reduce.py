"""Cross-check the package's reduction (matching + loop count) against a
straightforward Python implementation on random words.

Run from the repository root:  python3 tests/check_reduce.py
"""
import os
import random
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def reduce_word(n, word):
    """Return (matching, loops) for the product of generators in `word`.

    Uses the classical description: a diagram is a matching on the 2n
    boundary points L1..Ln, R1..Rn; multiplying glues R of the left factor
    to L of the right factor.
    """
    def gen(g):
        m = {}
        for j in range(1, n + 1):
            if g == 0 or j not in (g, g + 1):
                m[("L", j)] = ("R", j)
                m[("R", j)] = ("L", j)
        if g:
            m[("L", g)] = ("L", g + 1)
            m[("L", g + 1)] = ("L", g)
            m[("R", g)] = ("R", g + 1)
            m[("R", g + 1)] = ("R", g)
        return m

    def compose(a, b):
        # Middle points: R of a == L of b, labelled ("M", j).
        res, loops, seen = {}, 0, set()

        def follow(side_a, point):
            # point is in diagram a (side_a True) or b, we move until boundary.
            while True:
                diag = a if side_a else b
                q = diag[point]
                if side_a and q[0] == "R":
                    seen.add(q[1])
                    side_a, point = False, ("L", q[1])
                elif not side_a and q[0] == "L":
                    seen.add(q[1])
                    side_a, point = True, ("R", q[1])
                else:
                    return ("L", q[1]) if side_a else ("R", q[1])

        for j in range(1, n + 1):
            for side_a, start, label in ((True, ("L", j), ("L", j)),
                                         (False, ("R", j), ("R", j))):
                if label in res:
                    continue
                end = follow(side_a, start)
                res[label] = end
                res[end] = label
        for j in range(1, n + 1):
            if j in seen:
                continue
            loops += 1
            side_a, point = True, ("R", j)
            while True:
                seen.add(point[1])
                diag = a if side_a else b
                q = diag[point]
                side_a = not side_a
                point = ("L", q[1]) if side_a is False else ("R", q[1])
                seen.add(q[1])
                if q[1] == j and side_a:
                    break
        return res, loops

    total = gen(0)
    loops = 0
    for g in word:
        total, k = compose(total, gen(g))
        loops += k
    return total, loops


def tex_word(word):
    return " ".join("e_{%d}" % g for g in word)


def main():
    random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    cases = []
    for _ in range(150):
        n = random.randint(1, 7)
        length = random.randint(0, 10)
        cases.append((n, [random.randint(0, n - 1) for _ in range(length)]))

    lines = [
        r"\documentclass{article}",
        r"\usepackage{temperleylieb}",
        r"\ExplSyntaxOn",
        r"\iow_new:N \g_test_iow",
        r"\iow_open:Nn \g_test_iow { \jobname.out }",
        r"\cs_gset_eq:NN \test_old_reduced: \__tldiag_reduced_factor:",
        r"\cs_gset_protected:Npn \__tldiag_reduced_factor:",
        r"  {",
        r"    \iow_now:Ne \g_test_iow",
        r"      {",
        r"        \int_use:N \l__tldiag_loops_int ;",
        r"        \int_step_function:nN { \l__tldiag_n_int } \test_pair:n",
        r"      }",
        r"    \test_old_reduced:",
        r"  }",
        r"\cs_new:Npn \test_pair:n #1",
        r"  {",
        r"    \prop_item:Nn \l__tldiag_match_prop { L #1 } ,",
        r"    \prop_item:Nn \l__tldiag_match_prop { R #1 } ,",
        r"  }",
        r"\ExplSyntaxOff",
        r"\begin{document}",
    ]
    for n, word in cases:
        lines.append(r"\TL[reduce]{%d}{%s}" % (n, tex_word(word)))
    lines.append(r"\end{document}")

    with tempfile.TemporaryDirectory() as tmp:
        tex = os.path.join(tmp, "rnd.tex")
        with open(tex, "w") as fh:
            fh.write("\n".join(lines))
        env = dict(os.environ, TEXINPUTS=ROOT + "//:")
        proc = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "rnd.tex"],
            cwd=tmp, env=env, capture_output=True, text=True)
        if proc.returncode != 0:
            print(proc.stdout[-3000:])
            sys.exit("pdflatex failed")
        with open(os.path.join(tmp, "rnd.out")) as fh:
            out = [l.strip() for l in fh if l.strip()]

    assert len(out) == len(cases), (len(out), len(cases))
    failures = 0
    for (n, word), line in zip(cases, out):
        loops_s, rest = line.split(";", 1)
        items = [x.strip() for x in rest.split(",") if x.strip()]
        got = {}
        for j in range(1, n + 1):
            got[("L", j)] = (items[2 * j - 2][0], int(items[2 * j - 2][1:]))
            got[("R", j)] = (items[2 * j - 1][0], int(items[2 * j - 1][1:]))
        exp, loops = reduce_word(n, word)
        if got != exp or int(loops_s) != loops:
            failures += 1
            print("MISMATCH", n, word, "\n  tex:", int(loops_s), got,
                  "\n  py: ", loops, exp)
    print("%d cases, %d failures" % (len(cases), failures))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
