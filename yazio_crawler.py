from tinycrawler import TinyCrawler, Log, Statistics
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
from requests import Response
from urllib.parse import urlparse
import os
import json


def html_sanitization(html: str) -> str:
    """Return sanitized html."""
    return html.replace("⌊", "")


def get_product_name(response: Response) -> str:
    """Return product name from given Response object."""
    return response.url.split("/")[-1].split(".html")[0]


def get_product_category(soup: BeautifulSoup) -> str:
    """Return product category from given BeautifulSoup object."""
    return soup.find_all("span")[-2].get_text()


def parse_tables(html: str, path: str, strainer: SoupStrainer):
    """Parse table at given strained html object saving them as csv at given path."""
    for table in BeautifulSoup(
            html, "lxml", parse_only=strainer).find_all("table"):
        df = pd.read_html(html_sanitization(str(table)))[0].drop(0)
        table_name = df.columns[0]
        df.set_index(table_name, inplace=True)
        df.to_csv("{path}/{table_name}.csv".format(
            path=path, table_name=table_name))


def parse_metadata(html: str, path: str, strainer: SoupStrainer):
    """Parse metadata from given strained html and saves them as json at given path."""
    with open("{path}/metadata.json".format(path=path), "w") as f:
        json.dump({
            "category":
            get_product_category(
                BeautifulSoup(html, "lxml", parse_only=strainer))
        }, f)


def parse(response: Response):
    path = "{root}/{product}".format(
        root=urlparse(response.url).netloc, product=get_product_name(response))
    if not os.path.exists(path):
        os.makedirs(path)
    parse_tables(
        response.text, path,
        SoupStrainer(
            "table",
            attrs={"class": "table table-hover table-condensed table-fixed"}))

    parse_metadata(
        response.text, path,
        SoupStrainer(
            "ol",
            attrs={
                "itemscope": True,
                "itemtype": "http://schema.org/BreadcrumbList"
            }))


def url_validator(url: str, logger: Log, statistics: Statistics)->bool:
    """Return a boolean representing if the crawler should parse given url."""
    return url.startswith("https://www.yazio.com/it/alimenti")


def file_parser(response: Response, logger: Log, statistics):
    if response.url.endswith(".html"):
        parse(response)


seed = "https://www.yazio.com/it/alimenti"
crawler = TinyCrawler(follow_robots_txt=False)
crawler.set_file_parser(file_parser)
crawler.set_url_validator(url_validator)

crawler.load_proxies("http://1.0.0.1", "proxies.json")

crawler.run(seed)
