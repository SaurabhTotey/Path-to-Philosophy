from bs4 import BeautifulSoup
from functools import reduce
import requests
import sys

startPage = sys.argv[1] if len(sys.argv) > 1 else "Python (programming language)"
pageBranches = {}


def subpages_of(page):
    def as_url(page_name):
        return "https://en.wikipedia.org/wiki/" + page_name.replace(" ", "_")

    return set(link.attrs["title"] for link in filter(lambda link: "title" in link.attrs, reduce(lambda all_a, current_p: (all_a if type(all_a) is list else [all_a]) + list(current_p.find_all("a")), BeautifulSoup(requests.get(as_url(page)).text, "lxml").body.find("div", id="content").find("div", id="bodyContent").find("div", id="mw-content-text").find_all("p"))))


print(subpages_of(startPage))
