from bs4 import BeautifulSoup
from functools import reduce
import requests
import sys

# A set of all found pages
foundPages = set()


def pages_with_name(name):
    """
    A function that returns all pages with the given name
    :param name: the name of the page to find
    :return: a list of pages with the given name
    """
    global foundPages
    return list(filter(lambda page: page.name == name, foundPages))


def found_page(name):
    """
    Returns whether the page with the given name has been found
    :return: whether the page with the given name has been found
    """
    return len(pages_with_name(name)) > 0


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
                # Yeah, this line is disgusting: gets the titles of all a tags within p tags within the content divs of the page
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


# Sets the start page and the end page
startPage = Page(sys.argv[1] if len(sys.argv) > 1 else "Python (programming language)", None)
endPage = "Philosophy"

# Gets pages descending from the start page until the end page is found
while not found_page(endPage):
    for page in foundPages.copy():
        page.referenced_pages()
        if found_page(endPage):
            break

# Gets the path to the start page from the end page
pathToEnd = [pages_with_name(endPage)[0]]
while pathToEnd[0] != startPage:
    pathToEnd = [pathToEnd[0].parent] + pathToEnd
print(pathToEnd)
