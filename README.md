# 06682_FinalProject

[![Package Test](https://github.com/CardinalNeal/06682_FinalProject/actions/workflows/pkgtest-workflow.yaml/badge.svg?branch=main)](https://github.com/CardinalNeal/06682_FinalProject/actions/workflows/pkgtest-workflow.yaml)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CardinalNeal/06682_FinalProject/blob/main/project.ipynb)


The final project is to create a small Python package for OpenAlex based on what we have learned so far.


# OpenAlex API Works Module

The OpenAlex API Works module is a Python package for interacting with the OpenAlex API and retrieving information about academic works.

## Installation

To install the OpenAlex API Works module, run the following command:

```bash
pip install s23openalex
```

## Usage

Here's an example of how to use the Works class to retrieve information:

```python
from s23openalex import Works

work = Works('doi')
print(work)
work.related_works()
work.references()
work.citing_works()
work.ris
work.bibtex
```

You can replace `'doi'` with the actual OpenAlex ID of the work you want to retrieve information about.

The `Works` class provides the following methods:

- `__str__()`: Return a simple string representation of the work.
- `__repr__()`: Return a detailed string representation of the work.
- `_repr_markdown_()`: Return a Markdown representation of the work with a citation graph.
- `ris()`: Return a RIS formatted representation of the work.
- `related_works()`: Return a list of related works.
- `references()`: Return a list of referenced works.
- `citing_works()`: Return a list of citing works.

Simply call the appropriate method on the `Works` object to retrieve the desired information about the work.


## License

This is licensed under the MIT License. See the LICENSE file for details.
