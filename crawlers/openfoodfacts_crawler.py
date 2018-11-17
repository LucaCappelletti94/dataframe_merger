from tinycrawler import TinyCrawler, Log, Statistics
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
import requests
from requests import Response
from urllib.parse import urlparse
import re
import os
import json
import bs4
import pandas as pd


def html_sanitization(html: str) -> str:
    """Return sanitized html."""
    return html.replace(" — ", " - ")


def get_product_name(response: Response) -> str:
    """Return product name from given Response object."""
    return response.url.split("/")[-1]


def parse_tables(html: str, path: str, strainer: SoupStrainer):
    """Parse table at given strained html object saving them as csv at given path."""
    for table in BeautifulSoup(
            html, "lxml", parse_only=strainer).find_all("table"):
        df = pd.read_html(html_sanitization(str(table)))[0].drop(0)
        table_name = df.columns[0]
        df.set_index(table_name, inplace=True)
        df.to_csv("{path}/{table_name}.csv".format(
            path=path, table_name=table_name))


def parse_metadata(html: str, path: str):
    """Parse metadata from given strained html and saves them as json at given path."""
    data_retrieval = {
        "name": ("h1", {
            "property": "food:name",
            "itemprop": "name"
        }),
        "barcode": ("span", {
            "property": "food:code",
            "itemprop": "gtin13"
        }),
        "ingredients": ("div", {
            "id": "ingredients_list",
            "property": "food:ingredientListAsText"
        }),
        "additives": ("ul", {
            "style": "display:block;float:left;"
        }),
        "nova": ("a", {
            "href": "/nova"
        })
    }

    data = {
        key: BeautifulSoup(
            html, "lxml",
            parse_only=SoupStrainer(e, attrs=attrs)).get_text().strip()
        for key, (e, attrs) in data_retrieval.items()
    }

    additional_data = {
        p.find(SoupStrainer(
            "span", attrs={"class": "field"})).get_text().strip().strip(":"):
        p.get_text().split(":")[1]
        for p in BeautifulSoup(
            html,
            "lxml",
            parse_only=SoupStrainer(
                "div",
                attrs={
                    "class": "medium-12 large-8 xlarge-8 xxlarge-8 columns"
                })).find().find_all("p")
    }

    with open("{path}/metadata.json".format(path=path), "w") as f:
        json.dump({**data, **additional_data}, f)


def parse(response: Response):
    path = "../raw/{root}/{product}".format(
        root=urlparse(response.url).netloc, product=get_product_name(response))
    if not os.path.exists(path):
        os.makedirs(path)
    parse_tables(
        response.text, path,
        SoupStrainer(
            "table",
            attrs={
                "class": "data_table",
                "id": "nutrition_data_table"
            }))

    parse_metadata(response.text, path)


def url_validator(url: str, logger: Log, statistics: Statistics)->bool:
    """Return a boolean representing if the crawler should parse given url."""
    return url.startswith("https://it.openfoodfacts.org/") and ((
        "categoria" in url and url.count(
            "/") == 4 and not re.findall("/[a-z]{2}:", url)
    ) or (
        "prodotto" in url and url.count("/") == 5
    )) and "#" not in url


def file_parser(response: Response, logger: Log, statistics):
    if re.match(r"https://it\.openfoodfacts\.org/prodotto/\d+/[\w-]+", response.url):
        parse(response)


seed = "https://it.openfoodfacts.org/"
crawler = TinyCrawler(follow_robots_txt=False)
crawler.set_file_parser(file_parser)
crawler.set_url_validator(url_validator)

crawler.load_proxies("http://1.0.0.1", "proxies.json")

crawler.run(seed)
