import argparse
from s23openalex.works import Works


def main():
    parser = argparse.ArgumentParser(description="Get RIS or bibtex entry for a DOI")
    parser.add_argument("doi", help="DOI of the work")
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        choices=["ris", "bibtex"],
        default="ris",
        help="Output infor",
    )
    args = parser.parse_args()

    work = Works(args.doi)

    if args.format == "ris":
        print(work.ris)
    else:
        print(work.bibtex)


if __name__ == "__main__":
    main()
