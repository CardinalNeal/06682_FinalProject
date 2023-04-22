"""
This test file test work.ris function is correct or not
"""
from s23oa import Works


ref_ris = """TY  - JOUR
AU  - John R. Kitchin
PY  - 2015
TI  - Examples of Effective Data Sharing in Scientific Publishing
JO  - ACS Catalysis
VL  - 5
IS  - 6
SP  - 3894
EP  - 3899
DO  - https://doi.org/10.1021/acscatal.5b00538
ER  -"""


def test_ris():
    w = Works("https://doi.org/10.1021/acscatal.5b00538")
    assert ref_ris == w.ris
