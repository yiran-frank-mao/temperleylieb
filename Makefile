LATEX ?= pdflatex
LATEXFLAGS = -interaction=nonstopmode -halt-on-error
export TEXINPUTS := $(CURDIR)//:$(TEXINPUTS)

.PHONY: all doc examples test clean

all: doc examples

doc: temperleylieb-doc.pdf

examples: examples/wikipedia.pdf

temperleylieb-doc.pdf: temperleylieb-doc.tex temperleylieb.sty
	$(LATEX) $(LATEXFLAGS) $<
	$(LATEX) $(LATEXFLAGS) $<

examples/wikipedia.pdf: examples/wikipedia.tex temperleylieb.sty
	cd examples && $(LATEX) $(LATEXFLAGS) wikipedia.tex

test:
	python3 tests/check_reduce.py 1
	python3 tests/check_reduce.py 2

clean:
	rm -f *.aux *.log *.out *.toc examples/*.aux examples/*.log tests/*.aux tests/*.log
