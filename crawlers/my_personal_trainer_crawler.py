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
    return response.url.split("/")[-1].split(".htm")[0].lower().replace("-"," ")


def get_product_category(soup: BeautifulSoup) -> str:
    """Return product category from given BeautifulSoup object."""
    return soup.find_all("strong")[1].get_text().strip().lower()

def get_product_calories(soup: BeautifulSoup) -> str:
    """Return product calories from given BeautifulSoup object."""
    return soup.get_text().strip().lower()


def parse_tables(html: str, path: str, strainer: SoupStrainer):
    """Parse table at given strained html object saving them as csv at given path."""
    tables = pd.read_html(html_sanitization(html), decimal=",", thousands="")
    if len(tables) != 3:
        return
    for i, df in enumerate(tables):
        df.to_csv("{path}/{table_name}.csv".format(path=path, table_name=i))


def parse_metadata(html: str, path: str):
    """Parse metadata from given strained html and saves them as json at given path."""
    with open("{path}/metadata.json".format(path=path), "w") as f:
        json.dump({
            "category":
            get_product_category(
                BeautifulSoup(html, "lxml", parse_only=SoupStrainer("div", attrs={"class":"calorie"}))),
            "calories":
            get_product_calories(
                BeautifulSoup(html, "lxml", parse_only=SoupStrainer("strong", attrs={"id":"c_tro1"})))
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
            attrs={"class": "tabella"}))

    parse_metadata(
        response.text, path)


def url_validator(url: str, logger: Log, statistics: Statistics)->bool:
    """Return a boolean representing if the crawler should parse given url."""
    return url.lower().startswith("https://www.my-personaltrainer.it/tabelle") and "#" not in url


def file_parser(response: Response, logger: Log, statistics):
    if response.url.endswith(".htm") or response.url.endswith(".html"):
        try:
            parse(response)
        except:
            logger.error(response.url)


seed = "https://www.my-personaltrainer.it/tabelle-nutrizionali.htm"
crawler = TinyCrawler(follow_robots_txt=False)
crawler.set_file_parser(file_parser)
crawler.set_url_validator(url_validator)

crawler.load_proxies("http://1.0.0.1", "proxies.json")

crawler.run(seed)
