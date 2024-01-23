%-*- coding: utf-8 -*-

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{oeiscommon}[2024/01/23 v0.1 Template class of Tifa's OEIS PDF]

\LoadClass[a4paper,10pt]{book}
\RequirePackage{hyperref}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{geometry}
\RequirePackage{seqsplit}
\RequirePackage{fancyhdr}
\RequirePackage{eulervm}
\RequirePackage{fontspec}
\RequirePackage{imakeidx}

\setlength{\parindent}{0mm}

\setmonofont{Fira Code}
\makeindex[columns=9,columnsep=.5em,columnseprule]

\newcommand{\repo}{https://github.com/Tiphereth-A/OEIS-PDF}
\newcommand{\oeis}{https://oeis.org/}
\newcommand{\oeislegaldoc}{https://oeis.org/wiki/Legal\_Documents}
