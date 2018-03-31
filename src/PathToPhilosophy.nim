import htmlparser
import httpclient
import os
import sequtils
import strtabs
import strutils
import tables
import xmltree

## Defines a function that takes in a page name and formats it as a wikipedia URL
proc urlOf(pageName: string): string =
    return r"https://en.wikipedia.org/wiki/" & pageName.splitWhitespace().join("_")

## Gets the page to start at as either a command line argument or otherwise a hardcoded constant
let startPage = if paramCount() > 0: paramStr(1) else: "Nim (programming language)"

## A list of pages to their subpages
var pageBranches = Table[string, seq[string]]()

## Takes in a page name and finds all sub pages for that
proc getSubPages(pageName: string): seq[string] =
    # What allows content of the web page to be obtained
    let client = newHttpClient()
    # A sequence of all the subpages: initially empty
    var subpages: seq[string] = @[]
    # For each a element in the page's body's content div
    for link in parseHtml(client.getContent(urlOf(pageName))).findAll("body")[0].findAll("div").filter( proc(divTag: XmlNode): bool = divTag.attr("id") != "" and divTag.attrs["id"] == "content" )[0].findAll("a"):
        # Adds the link if it has a title attribute and it isn't ignored
        try:
            # A list of prefixes to not take links of
            const prefixIgnores = ["Special", "wikisource", "Category", "Portal", "Help", "s"]
            for badPrefix in prefixIgnores:
                if (link.attrs["title"].startsWith(badPrefix & ":")):
                    discard "Link is actually not useful as it has a prefix that is ignored!"
                    raise
            subpages.add(link.attrs["title"])
        except:
            discard "Link is useless because it doesn't have a title!"
    return subpages.deduplicate

echo getSubPages(startPage)
