from bs4 import BeautifulSoup
import requests
import sys

startPage = sys.argv[1] if len(sys.argv) > 1 else "Python (programming language)"
pageBranches = {}

def getSubpages(page):
    def asURL(page):
        return "https://en.wikipedia.org/wiki/" + page.replace(" ", "_")
    return [link.attrs["title"] for link in filter(lambda link: "title" in link.attrs, BeautifulSoup(requests.get(asURL(page)).text, "lxml").body.find("div", id="content").find("div", id="bodyContent").find("div", id="mw-content-text").find_all("a"))]


print(getSubpages(startPage))
