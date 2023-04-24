"""
This test file tests the basic info of one example.
"""
from s23openalex import Works


def test_str():
    """Test the __str__ method of the Works class."""
    work = Works("https://doi.org/10.1021/acscatal.5b00538")
    assert str(work) == "str"


def test_repr():
    """Test the __repr__ method of the Works class."""
    work = Works("https://doi.org/10.1021/acscatal.5b00538")
    assert isinstance(repr(work), str)


def test_related_works():
    """Test the related_works method of the Works class."""
    work = Works("https://doi.org/10.1021/acscatal.5b00538")
    assert isinstance(work.related_works(), list)


def test_references():
    """Test the references method of the Works class."""
    work = Works("https://doi.org/10.1021/acscatal.5b00538")
    assert isinstance(work.references(), list)


def test_citing_works():
    """Test the citing_works method of the Works class."""
    work = Works("https://doi.org/10.1021/acscatal.5b00538")
    assert isinstance(work.citing_works(), list)


def test_ris():
    """Test the ris method of the Works class."""
    work = Works("https://doi.org/10.1021/acscatal.5b00538")
    assert "ER  -" in work.ris
