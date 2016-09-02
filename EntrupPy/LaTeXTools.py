'''
A collection of tools to help generate LaTeX files with Python.
'''

from datetime import date

latex_header = r'''\documentclass[
	fontsize=11pt,
	paper=a4,
	pagesize=auto,
	parskip=false,
	ngerman
]{scrartcl}

\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{enumerate}
\usepackage{babel}
\usepackage{lmodern}
\usepackage{microtype}

\begin{document}

'''


def get_latex_header():
    """Returns a string containing a LateX header."""
    return latex_header


class LaTeXFile:
    """Usage: with LaTeXFile('<filename>') as tex_file

    Create a text file to write LaTeX code to it.
    When used in a with statement the document is properly closed.
    """

    def __init__(self, filename):
        self.file = open(filename, 'w')

    def __enter__(self):
        self.file.write(latex_header)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.write('\n\\end{document}')
        self.file.close()

    def write_line(self, line):
        self.file.write(line + '\n')

    def make_title(self, title='Dokument', author=None, date=r'\today'):
        self.write_line(r'\title{%s}' % title)
        if author:
            self.write_line(r'\author{%s}' % author)
        if date:
            self.write_line(r'\date{%s}' % date)
        self.write_line(r'\maketitle' + '\n')


class LaTeXList:
    """Usage: withLaTeXList(LaTeXFile[, '<enumerator>']) as tex_list

    Create a list at the given LaTexFile.
    """

    def __init__(self, tex_file, enumerator=None):
        self.tex_file = tex_file
        self.enumerator = None
        if enumerator:
            self.enumerator = enumerator

    def __enter__(self):
        if self.enumerator:
            self.tex_file.write_line(r'\begin{enumerate}[%s]' % self.enumerator)
        else:
            self.tex_file.write_line(r'\begin{enumerate}')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tex_file.write_line(r'\end{enumerate}')

    def write_item(self, text):
        self.tex_file.write_line(r'\item ' + text)


def main():
    """Main function to test this modules"""
    with LaTeXFile('test.tex') as tex_file:
        tex_file.make_title('Ein Test', 'Michael Entrup')
        with LaTeXList(tex_file) as list:
            for _ in range(10):
                list.write_item('Dies ist ein Test.')
                with LaTeXList(tex_file, '(a)') as inner_list:
                    for _ in range(4):
                        inner_list.write_item('Ich bin ein Item.')


if __name__ == '__main__':
    main()
