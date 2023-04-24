import click
from .works import Works


@click.command(help="OpenAlex Institutions")
@click.argument("doi")
@click.option("-b", "bibtex_flag", is_flag=True, help="Output format: BibTeX")
@click.option("-r", "ris_flag", is_flag=True, help="Output format: RIS")
def main(doi, bibtex_flag, ris_flag):
    w = Works(doi)
    if bibtex_flag:
        print(w.bibtex)
    if ris_flag:
        print(w.ris)
