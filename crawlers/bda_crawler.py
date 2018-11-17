from tinycrawler import TinyCrawler, Log, Statistics
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
import requests
from requests import Response
from urllib.parse import urlparse
import os
import json
import bs4
import re
import pandas as pd


def html_sanitization(html: str) -> str:
    """Return sanitized html."""
    [s.extract() for s in html.find_all("table")]
    return str(html)


def get_product_name(response: Response) -> str:
    """Return product name from given Response object."""
    name = BeautifulSoup(response.text, "lxml", parse_only=SoupStrainer("td", attrs={
        "class": "titolo",
        "colspan": "5"
    })).find().get_text().lower()

    name = re.sub("^[\d\s]+", "", name)
    name = name.split("  ")[0]

    return name.strip()


def get_product_category(soup: BeautifulSoup) -> str:
    """Return product category from given BeautifulSoup object."""
    return soup.get_text().lower().strip()


def parse_tables(html: str, path: str, strainer: SoupStrainer):
    """Parse table at given strained html object saving them as csv at given path."""
    for i, table in enumerate(BeautifulSoup(
            html, "html5lib").find_all(strainer)):
        df = pd.read_html(html_sanitization(table))[0].drop(0)
        df.to_csv("{path}/{table_name}.csv".format(
            path=path, table_name=i))


def parse_metadata(html: str, path: str, strainer: SoupStrainer):
    """Parse metadata from given strained html and saves them as json at given path."""
    with open("{path}/metadata.json".format(path=path), "w") as f:
        json.dump({
            "category":
            get_product_category(
                BeautifulSoup(html, "lxml", parse_only=strainer).find(strainer))
        }, f)


def parse(response: Response):
    path = "../raw/{root}/{product}".format(
        root=urlparse(response.url).netloc, product=get_product_name(response))
    if not os.path.exists(path):
        os.makedirs(path)
    parse_tables(
        response.text, path,
        SoupStrainer("table", attrs={"id": "tblComponenti"}))

    parse_metadata(
        response.text, path,
        SoupStrainer(
            "td",
            attrs={
                "class": "testonormale",
                "valign": "top",
                "colspan": "6"
            }))


def url_validator(url: str, logger: Log, statistics: Statistics)->bool:
    """Return a boolean representing if the crawler should parse given url."""
    return re.match(r"http://www\.bda-ieo\.it/test/ComponentiAlimento\.aspx\?Lan=Ita&foodid=[\d_]+", url)


def file_parser(response: Response, logger: Log, statistics):
    if re.match(r"http://www\.bda-ieo\.it/test/ComponentiAlimento\.aspx\?Lan=Ita&foodid=[\d_]+", response.url):
        parse(response)


seed = "http://www.bda-ieo.it/test/Alphabetical.aspx?Lan=Ita&FL=%"
crawler = TinyCrawler(follow_robots_txt=False)
crawler.set_file_parser(file_parser)
crawler.set_url_validator(url_validator)

crawler.load_proxies("http://1.0.0.1", "proxies.json")

crawler.run(seed)
