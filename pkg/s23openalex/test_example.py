"""
This test file test the basic info of one example
"""
import pytest
from s23openalex import Works


@pytest.fixture
def work():
    return Works("https://doi.org/10.1021/acscatal.5b00538")


def test_str(work):
    assert str(work) == "str"


def test_repr(work):
    assert isinstance(repr(work), str)


def test_related_works(work):
    assert isinstance(work.related_works(), list)


def test_references(work):
    assert isinstance(work.references(), list)


def test_citing_works(work):
    assert isinstance(work.citing_works(), list)


def test_ris(work):
    assert "ER  -" in work.ris
