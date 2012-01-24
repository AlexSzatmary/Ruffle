#!/usr/bin/env python

import glob
import sys
import re
import os, os.path
from collections import defaultdict


def find_tex_files():
    tex_files = glob.glob('*.tex')
    with open('exclude.txt') as hin:
        for i in hin.readlines():
            if i[:-1] in tex_files:
                tex_files.remove(i[:-1])
    return tex_files


def write_input_list(tex_files):
    hout = open('input-list.ruf', 'w')
    for f in tex_files:
        hout.write('\\input{' + f + '}\n')
    hout.close()


def gather_cites_lists(tex_files):
    cites = {}

    for f in tex_files:
        with open(f) as hin:
            for l in hin.readlines():
                m = re.search(r'input{ruffle-files/(.*)\.ruf}', l)
                if m:
                    this_node = m.group(1)
                    cites[this_node] = []
                    ruffling = True
                if '%ruffle' in l:
                    cites[this_node].extend(
                        l.replace('%ruffle', '').replace('\\cite', ' ')
                        .replace(',', ' ').replace('{', ' ')
                        .replace('}', ' ').split())
    # Remove duplicate citations
    for k in cites:
        deduped = []
        [deduped.append(i) for i in cites[k] if i not in deduped]
        cites[k] = deduped

    return cites


def make_citedby_lists(cites):
    citedby = defaultdict(list)
    for k in cites:
        for this_node in cites[k]:
            citedby[this_node].append(k)
    return citedby


def write_rufs(cites, citedby):
    for k in cites:
        with open(os.path.join('ruffle-files', k + '.ruf'), 'w') as hout:
            hout.write('\\noindent\\bibentry{' + k + '}\n')
            hout.write('\\vspace{\\baselineskip}\n')
            hout.write('\n')
            hout.write('\\begin{itemize}\n')
            if citedby[k]:
                hout.write('\\item \\textbf{Cited by}: \\cite{')
                hout.write('}, \\cite{'.join(citedby[k]))
                hout.write('}\n')
            else:
                hout.write('\\item \\textbf{Cited by}: \n')
            if cites[k]:
                hout.write('\\item \\textbf{Cites}: \\cite{')
                hout.write('}, \\cite{'.join(cites[k]))
                hout.write('}\n')
            else:
                hout.write('\\item \\textbf{Cites}: \n')
            hout.write('\\end{itemize}\n')


def main(argv=None):
    if argv is None:
        argv = sys.argv

    tex_files = find_tex_files()
    write_input_list(tex_files)
    cites = gather_cites_lists(tex_files)
    citedby = make_citedby_lists(cites)
    write_rufs(cites, citedby)


if __name__ == "__main__":
    sys.exit(main())
