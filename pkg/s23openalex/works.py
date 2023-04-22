import requests
import base64
from IPython.display import display, HTML

import matplotlib.pyplot as plt
from IPython.core.pylabtools import print_figure


class Works:
    def __init__(self, oaid):
        self.oaid = oaid
        self.req = requests.get(f"https://api.openalex.org/works/{oaid}")
        self.data = self.req.json()

    def __str__(self):
        return "str"

    def __repr__(self):
        _authors = [au["author"]["display_name"]
                    for au in self.data["authorships"]]
        if len(_authors) == 1:
            authors = _authors[0]
        else:
            authors = ", ".join(_authors[0:-1]) + " and" + _authors[-1]

        title = self.data["title"]

        journal = self.data["host_venue"]["display_name"]
        volume = self.data["biblio"]["volume"]

        issue = self.data["biblio"]["issue"]
        if issue is None:
            issue = ", "
        else:
            issue = ", " + issue

        pages = "-".join(
            [self.data["biblio"]["first_page"], self.data["biblio"]["last_page"]]
        )
        year = self.data["publication_year"]
        citedby = self.data["cited_by_count"]

        oa = self.data["id"]
        s = f'{authors}, {title}, {volume}{issue}{pages}, ({year}), {self.data["doi"]}. cited by: {citedby}. {oa}'
        return s

    def _repr_markdown_(self):
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
            [self.data["biblio"]["first_page"], self.data["biblio"]["last_page"]]
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
        uri = f'<pre>{ris}</pre><br><a href="data:text/plain;base64,{ris64}" download="ris">Download RIS</a>'

        display(HTML(uri))
        return ris
