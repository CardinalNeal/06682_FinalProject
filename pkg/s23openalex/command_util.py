"""
command_util.py: A command-line utility to fetch information for a DOI in BibTeX or RIS format
using OpenAlex Institutions.
"""


import click
from .works import Works


@click.command(
    help="OpenAlex Institutions: Fetch citation information for a DOI in BibTeX or RIS format."
)
@click.argument("doi")
@click.option("-b", "bibtex_flag", is_flag=True, help="Print BibTeX result")
@click.option("-r", "ris_flag", is_flag=True, help="Print RIS result")
def main(doi, bibtex_flag, ris_flag):
    """
    Fetches and prints the citation information for a given DOI in either BibTeX or RIS format.

    :param doi: Digital Object Identifier (DOI) of the work.
    :param bibtex_flag: Flag to specify print BibTeX result.
    :param ris_flag: Flag to specify print RIS result.
    """
    works = Works(doi)
    if bibtex_flag:
        print(works.bibtex)
    if ris_flag:
        print(works.ris)
