from tinycrawler import TinyCrawler, Log, Statistics
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
import requests
from requests import Response
import logging
from urllib.parse import urlparse

import os
import json
import bs4
import pandas as pd


def html_sanitization(html: str) -> str:
    """Return sanitized html."""
    return html.replace("⌊", "")


def get_product_name(response: Response) -> str:
    """Return product name from given Response object."""
    name = bs4.BeautifulSoup(response.text).find("h1").get_text()
    return name


def parse_tables(html: str, path: str, strainer: SoupStrainer):
    """Parse table at given strained html object saving them as csv at given path."""
    for table in BeautifulSoup(html, "lxml", parse_only=strainer)("table"):
        df = pd.read_html(html_sanitization(str(table)))[0]
        table_name = df[0][0].lower().strip().replace(" ","_")
        df = df.drop(0)
        df = df.set_index(0)
        df.to_csv("{path}/{table_name}.csv".format(path=path, table_name=table_name))


def parse(response: Response):
    path = "{root}/{product}".format(
        root=urlparse(response.url).netloc, product=get_product_name(response))
    if not os.path.exists(path):
        os.makedirs(path)
    parse_tables(
        response.text, path,
        SoupStrainer(
            "table"))

def url_validator(url: str, logger: Log, statistics: Statistics)->bool:
    """Return a boolean representing if the crawler should parse given url."""
    return url.lower().startswith("https://www.cibo360.it/cgi-bin/db/") and "#" not in url


def file_parser(response: Response, logger: Log, statistics):
    if response.url.startswith("https://www.cibo360.it/cgi-bin/db/post_vn1.cgi?ID_UTENTE=&CODE="):
        try:
            parse(response)
        except:
            logger.error(response.url)


seed = "https://www.cibo360.it/cgi-bin/db/datafind1.cgi"
crawler = TinyCrawler(follow_robots_txt=False)
crawler.set_file_parser(file_parser)
crawler.set_url_validator(url_validator)

crawler.load_proxies("http://1.0.0.1", "proxies.json")

crawler.run(seed)
