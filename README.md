### Introduction

Ruffle helps you make annotated bibliographies with LaTeX by making links
between each article and the articles it cites and is cited by in the output
PDF. To use Ruffle, you need Python 2.7 and LaTeX 2e. I also recommend using
AUCTeX in Emacs; this makes it easy to add cite keys.

### Use

An example is in the `example` directory. If you do,

    ruffle
    pdflatex annotated-bibliography
    bibtex annotated-bibliography
    pdflatex annotated-bibliography
    pdflatex annotated-bibliography

Ruffle will generate some helper files and then LaTeX will turn the TeX files
plus the helper files into a PDF. Ruffle does two things:

1. Ruffle finds any TeX files in the current directory and tells the file
`annotated-bibliography.tex` to input them.
2. Ruffle inserts a bibentry for each reference, and, after each bibentry, it
has a list of the references this reference cites, and a list of the references
this reference is cited by.

To add your own references, copy
`lit-template.tex` and edit it. Change the <cite-key> in

    \bibentry{ruffle-files/<cite-key>.ruf}

to the cite key for the article you want to discuss. To link to other articles,
make any line that starts with `%ruffle` and has one or more regular `\cite`
commands referring to the other articles. Repeat this for other articles; it
doesn't matter if they're all in one file or in multiple files. Ruffle will
find any new files you make in have them input by `annotated-bibliography.tex`.
When you add new references, just run ruffle and then run
`annotated-bibliography.tex` through LaTeX as usual.

### Installation

In the main `ruffle` directory, do,

    python setup.py install

You may need to append a --prefix=/path/to/python/modules option to place this
module in your home directory if you do not have administrator rights.

### How Ruffle works.

One of the TeX files is `Computation.tex`, and the really useful part of it is,

    \input{ruffle-files/Caputo-2005p2271.ruf}
    %ruffle \cite{Shao-1998p2423} \cite{Lawrence-1991p2840}

This tells Ruffle to make bibentry item for Caputo-2005p2271, and that
Caputo-2005 cites Shao-1998p2423 and Lawrence-1991p2840. Running Ruffle
generates the helper file, `ruffle-files/Caputo-2005p2271.ruf`,

    \noindent\bibentry{Caputo-2005p2271}
    \vspace{\baselineskip}

    \begin{itemize}
    \item \textbf{Cited by}: 
    \item \textbf{Cites}: \cite{Shao-1998p2423}, \cite{Lawrence-1991p2840}
    \end{itemize}

which explicitly has the bibentry line, as well as citation links for the
related articles. The LaTeX package, bibentry, allows you to pull full
bibliograpic information into the text, as opposed to just partial citation
information. The hyperref project allows you to make links between parts of a
document, kind of like HTML links. It's not clear if this is a bug or a
feature, but hyperref automatically makes a link out of a `\cite` command, and
makes this citation refer to either its bibitem in the bibliography or to its
in-text bibentry (if present). LaTeX does not like this and emits warnings, but
this works fine.

#### Identifying references

The text about each reference begins with the 

    \input{ruffle-files/<cite-key>.ruf}

line. Ruffle will start saving information about another reference when it sees
the next `\input{ruffle-files/...` line.

#### Identifying citation relationships

After an `\input{ruffle-files/...` line, Ruffle looks for any lines that begin
with `%ruffle`, and grabs any citation information from them. Ruffle picks up
anything that looks like a cite key and puts these cite keys into a Cites
list. Note that Ruffle does not automatically find citations in lines of text
not beginning with `%ruffle`. Ruffle is generous in pulling cite keys from
lines starting with `%ruffle`: you probably want your cite keys to be comma or
space delimited, either bare or in `\cite{...}` commands, but you could have a
}-delimited list of cite keys and Ruffle would find those, anyway.

### Notes on use in Emacs with AUCTeX

I use Emacs with AUCTeX to edit my LaTeX files, and so there are some hacks
built into Ruffle to accommodate this. 

The killer feature of AUCTeX, for me, is in-line preview of equations. This
does not work properly with hyperref. In order for AUCTeX to be able to find
the right header for a subfile in a multiple-file LaTeX document, each subfile
needs lines like,

    %%% Local Variables: 
    %%% mode: latex
    %%% TeX-master: "annotated-bibliography-fake"
    %%% End:

The file, `annotated-bibliography-fake.tex` is the same as
`annotated-bibliography.tex`, except that hyperref is not used. This keeps
AUCTeX from fighting with hyperref, while keeping hyperref in the generated
LaTeX document.

Also, reftex-citation makes it easy to add citations. I use this to grab the
cite key to put in the `\input{ruffle-files/...}` line. (I actually kill the
line, run it through this sed command,

    sed 's|\\cite{\(.*\)}|\\input{ruffle/\1.ruf}|'

via TextExpander, which then yanks in the new input line. There is a better way
to do this purely in Emacs.)
