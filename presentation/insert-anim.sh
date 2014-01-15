cd alg/anim/slides/; pdflatex anim.tex

cd ../../..; pdftk A=presentation.pdf B=alg/anim/slides/anim.pdf cat A1-132 B A133-end output presentation-anim.pdf
