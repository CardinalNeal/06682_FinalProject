"""
This module contains the Works class to interact with the OpenAlex API, retrieve
information about academic works, and display the work metadata in various formats.

Example usage:

    work = Works(oaid)
    print(work)
    work.related_works()
    work.references()
    work.citing_works()
"""

import time
import bibtexparser
import base64
import matplotlib.pyplot as plt
from IPython.core.pylabtools import print_figure
import requests
from IPython.display import display, HTML


class Works:
    """
    A class to represent works and interact with the OpenAlex API.

    Attributes:
        oaid (str): OpenAlex ID of the work.
        req (requests.Response): HTTP response from the API request.
        data (dict): JSON data of the work retrieved from the API.

    Methods:
        __str__(): Return a simple string representation of the work.
        __repr__(): Return a detailed string representation of the work.
        _repr_markdown_(): Return a Markdown representation of the work with a citation graph.
        ris(): Return a RIS formatted representation of the work.
        related_works(): Return a list of related works.
        references(): Return a list of referenced works.
        citing_works(): Return a list of citing works.
    """

    def __init__(self, oaid):
        """
        Initialize the Works object by fetching data from the OpenAlex API.

        Args:
            oaid (str): OpenAlex ID of the work.
        """
        self.oaid = oaid
        self.req = requests.get(f"https://api.openalex.org/works/{oaid}")
        self.data = self.req.json()

    def __str__(self):
        """
        Return a simple string representation of the work.
        """
        return "str"

    def __repr__(self):
        """
        Return a detailed string representation of the work.
        """
        _authors = [au["author"]["display_name"] for au in self.data["authorships"]]
        if len(_authors) == 0:
            authors = ""
        elif len(_authors) == 1:
            authors = _authors[0]
        else:
            authors = ", ".join(_authors[0:-1]) + " and" + _authors[-1]

        title = self.data["title"]

        journal = self.data["host_venue"]["display_name"]
        volume = self.data["biblio"]["volume"]
        if volume is None:
            volume = ""
        else:
            volume = ", " + volume

        issue = self.data["biblio"]["issue"]
        if issue is None:
            issue = ""
        else:
            issue = ", " + issue

        # pages = '-'.join([self.data['biblio'].get('first_page', '') or '',
        #                   self.data['biblio'].get('last_page', '') or ''])

        fp = self.data["biblio"]["first_page"]
        lp = self.data["biblio"]["first_page"]
        if fp is not None and lp is not None:
            pages = ", " + "-".join([fp, lp])
        else:
            if fp is None:
                fp = ""
            if lp is None:
                lp = ""
            pages = fp + lp
        if pages != "":
            pages = pages + ", "

        year = self.data["publication_year"]
        citedby = self.data["cited_by_count"]

        oa = self.data["id"]
        s = f'{authors}, {title}{volume}{issue}{pages}({year}), {self.data["doi"]}. cited by: {citedby}. {oa}'
        return s

    def _repr_markdown_(self):
        """
        Return a Markdown representation of the work with a citation graph.
        """
        _authors = [
            f'[{au["author"]["display_name"]}]({au["author"]["id"]})'
            for au in self.data["authorships"]
        ]
        if len(_authors) == 1:
            authors = _authors[0]
        else:
            authors = ", ".join(_authors[0:-1]) + " and " + _authors[-1]

        title = self.data["title"]

        journal = f"[{self.data['host_venue']['display_name']}]({self.data['host_venue']['id']})"
        volume = self.data["biblio"]["volume"]

        issue = self.data["biblio"]["issue"]
        if issue is None:
            issue = ", "
        else:
            issue = ", " + issue

        pages = "-".join(
            [
                self.data["biblio"].get("first_page", "") or "",
                self.data["biblio"].get("last_page", "") or "",
            ]
        )
        year = self.data["publication_year"]
        citedby = self.data["cited_by_count"]

        oa = self.data["id"]

        # Citation counts by year
        years = [e["year"] for e in self.data["counts_by_year"]]
        counts = [e["cited_by_count"] for e in self.data["counts_by_year"]]

        fig, ax = plt.subplots()
        ax.bar(years, counts)
        ax.set_xlabel("year")
        ax.set_ylabel("citation count")
        data = print_figure(fig, "png")  # save figure in string
        plt.close(fig)

        b64 = base64.b64encode(data).decode("utf8")
        citefig = f"![img](data:image/png;base64,{b64})"

        s = f'{authors}, *{title}*, **{journal}**, {volume}{issue}{pages}, ({year}), {self.data["doi"]}. cited by: {citedby}. [Open Alex]({oa})'

        s += "<br>" + citefig
        return s

    @property
    def ris(self):
        """
        Return a RIS formatted representation of the work.
        """
        fields = []
        if self.data["type"] == "journal-article":
            fields += ["TY  - JOUR"]
        else:
            raise Exception("Unsupported type {self.data['type']}")

        for author in self.data["authorships"]:
            fields += [f'AU  - {author["author"]["display_name"]}']

        fields += [f'PY  - {self.data["publication_year"]}']
        fields += [f'TI  - {self.data["title"]}']
        fields += [f'JO  - {self.data["host_venue"]["display_name"]}']
        fields += [f'VL  - {self.data["biblio"]["volume"]}']

        if self.data["biblio"]["issue"]:
            fields += [f'IS  - {self.data["biblio"]["issue"]}']

        fields += [f'SP  - {self.data["biblio"]["first_page"]}']
        fields += [f'EP  - {self.data["biblio"]["last_page"]}']
        fields += [f'DO  - {self.data["doi"]}']
        fields += ["ER  -"]

        ris = "\n".join(fields)
        ris64 = base64.b64encode(ris.encode("utf-8")).decode("utf8")
        uri = f'<pre>{ris}<pre><br><a href="data:text/plain;base64,{ris64}" download="ris">Download RIS</a>'

        display(HTML(uri))
        return ris

    def related_works(self):
        """
        Retrieve and return a list of related works.
        """
        rworks = []
        for rw_url in self.data["related_works"]:
            rw = Works(rw_url)
            rworks += [rw]
            time.sleep(0.101)
        return rworks

    def references(self):
        """
        Retrieve and return a list of referenced works.
        """
        rworks = []
        for rw_url in self.data["referenced_works"]:
            rw = Works(rw_url)
            rworks += [rw]
            time.sleep(0.101)
        return rworks

    def citing_works(self):
        """
        Retrieve and return a list of citing works.
        """
        url = self.data["cited_by_api_url"]
        try:
            url_data = requests.get(url).json()
        except:
            print("Can not get the data from the url!")
            return
        rworks = []
        for item in url_data["results"]:
            rw = Works(item["id"])
            rworks.append(rw)
            time.sleep(0.101)
        return rworks

    @property
    def bibtex(self):
        """
        Return a BibTeX entry for the work.
        """
        doi = self.data["doi"].replace("https://doi.org/", "")
        for au in self.data["authorships"]:
            if au["author_position"] == "first":
                ds_au = au["author"]["display_name"]
                ds_au = ds_au.split()[-1].lower()
        id_title = self.data["title"].lower().split()[:3:2]
        id_title = "-".join(id_title)
        entry = {
            "ENTRYTYPE": "article",
            "ID": f"{ds_au}-{str(self.data['publication_year'])}-{id_title}",
            "author": " and ".join(
                [au["author"]["display_name"] for au in self.data["authorships"]]
            ),
            "title": self.data["title"],
            "journal": self.data["host_venue"]["display_name"],
            "volume": self.data["biblio"]["volume"],
            "number": self.data["biblio"]["issue"],
            "pages": f"{self.data['biblio']['first_page']}-{self.data['biblio']['last_page']}",
            "year": str(self.data["publication_year"]),
            "doi": doi,
            "url": f"https://doi.org/{doi}",
        }
        bibtex_db = bibtexparser.bibdatabase.BibDatabase()
        bibtex_db.entries = [entry]
        result = bibtexparser.dumps(bibtex_db)
        encoder = base64.b64encode(result.encode("utf-8")).decode("utf8")
        uri = f'<pre>{result}<pre><br><a href="data:text/plain;base64,{encoder}" download="bibtex">Download bibtex</a>'
        display(HTML(uri))
        return result
