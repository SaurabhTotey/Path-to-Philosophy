from bs4 import BeautifulSoup
from functools import reduce
import requests
import sys
from threading import Thread


def subpages_of(page):
    """
    Gets all the subpages or referenced pages from a given page name
    :param page: the name of the page to find the subpages of
    :return: a set of all the names of referenced pages
    """
    def as_url(page_name):
        return "https://en.wikipedia.org/wiki/" + page_name.replace(" ", "_")

    try:
        return {link.attrs["title"] for link in filter(lambda link: "title" in link.attrs, reduce(lambda all_a, current_p: (all_a if type(all_a) is list else [all_a]) + list(current_p.find_all("a")), BeautifulSoup(requests.get(as_url(page)).text, "lxml").body.find("div", id="content").find("div", id="bodyContent").find("div", id="mw-content-text").find_all("p")))}
    except:
        return None


startPage = sys.argv[1] if len(sys.argv) > 1 else "Python (programming language)"
pageBranches = {startPage: subpages_of(startPage)}
while "Philosophy" not in pageBranches:
    for page in list(pageBranches):
        for referenced in pageBranches[page]:
            if referenced in pageBranches:
                continue
            def add_pages():
                pageBranches[referenced] = subpages_of(referenced)
            Thread(target=add_pages())
    print(pageBranches)
