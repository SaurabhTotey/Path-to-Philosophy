from bs4 import BeautifulSoup
from functools import reduce
import requests
import sys

# A set of all found pages
foundPages = set()


class Page:
    """
    A class that represents a Wikipedia page; doesn't find children unless necessary
    """

    def __init__(self, name, parent):
        """
        Makes a Wikipedia page given its name and registers it in the global list of pages
        :param name: the name of the Wikipedia page: must exactly match
        :param parent: the parent Page to this page
        """
        global foundPages
        self.name = name
        self.parent = parent
        foundPages.add(self)

    def url(self):
        """
        Gets the URL of the page
        :return: the URL of this Wikipedia page
        """
        return "https://en.wikipedia.org/wiki/" + self.name.replace(" ", "_")

    def referenced_pages(self):
        """
        Gets the children of this Wikipedia page
        Will not re-pull children unless children have never been called for before (method is lazily evaluated)
        :return:
        """
        if not hasattr(self, "children"):
            try:
                self.children = {Page(link.attrs["title"], self) for link in filter(lambda link: "title" in link.attrs, reduce(lambda all_a, current_p: (all_a if type(all_a) is list else [all_a]) + list(current_p.find_all("a")), BeautifulSoup(requests.get(self.url()).text, "lxml").body.find("div", id="content").find("div", id="bodyContent").find("div", id="mw-content-text").find_all("p")))}
            except:
                self.children = None
        return self.children

    def __repr__(self):
        """
        Represents the page as a string so that the page can be prettily printed
        :return: The name of the page
        """
        return self.name


def found_philosophy():
    """
    A function that returns whether philosophy has been yet reached by any of the pages
    :return: a boolean on whether philosophy has been found
    """
    global foundPages
    return len(list(filter(lambda page: page.name == "Philosophy", foundPages))) > 0


# Gets the start page
startPage = Page(sys.argv[1] if len(sys.argv) > 1 else "Python (programming language)", None)

# Gets pages descending from the start page until Philosophy is found
while not found_philosophy():
    for page in foundPages.copy():
        page.referenced_pages()
        if found_philosophy():
            break

# Gets the path to the start page from Philosophy
pathToPhilosophy = [list(filter(lambda page: page.name == "Philosophy", foundPages))[0]]
while pathToPhilosophy[0] != startPage:
    pathToPhilosophy = [pathToPhilosophy[0].parent] + pathToPhilosophy
print(pathToPhilosophy)
