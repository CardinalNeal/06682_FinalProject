"""
This test file test work.ris function is correct or not
"""
from s23openalex import Works

ref_bibtex = """@article{kitchin-2015-examples-effective,
 author = {John R. Kitchin},
 doi = {10.1021/acscatal.5b00538},
 journal = {ACS Catalysis},
 number = {6},
 pages = {3894-3899},
 title = {Examples of Effective Data Sharing in Scientific Publishing},
 url = {https://doi.org/10.1021/acscatal.5b00538},
 volume = {5},
 year = {2015}
}"""


def test_bibtex():
    w = Works("https://doi.org/10.1021/acscatal.5b00538")
    assert True
