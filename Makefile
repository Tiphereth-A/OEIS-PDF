lang = zh-hans en
latexmk = latexmk -cd -xelatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error -outdir=out -time
filter = python filter.py -l DEBUG
texgen = python tex-gen.py -l DEBUG

all: gentex pdf
.PHONY: gentex pdf $(lang) clean

pdf: $(lang)

gentex:
	$(filter) clean
	$(texgen) gen

clean:
	-rm -rf data
	-rm tex/oeis.tex
	-mkdir data
	-mkdir data/detail
	-touch data/.gitkeep
	-touch data/detail/.gitkeep
	cd tex && (latexmk -C -outdir=out *.tex; cd ..)

$(lang): % : tex/oeis-pdf-%.tex
	$(latexmk) $<
