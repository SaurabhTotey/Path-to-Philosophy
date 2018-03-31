import htmlparser
import httpclient
import os
import sequtils
import strtabs
import strutils
import tables
import xmltree

## Takes in a page name and finds all sub pages for that
proc getSubPages(pageName: string): seq[string] =
    ## Defines a function that takes in a page name and formats it as a wikipedia URL
    proc urlOf(pageName: string): string =
        return r"https://en.wikipedia.org/wiki/" & pageName.splitWhitespace().join("_")
    # What allows content of the web page to be obtained
    let client = newHttpClient()
    # A sequence of all the subpages: initially empty
    var subpages: seq[string] = @[]
    # For each a element in the page's body's content div
    for link in parseHtml(client.getContent(urlOf(pageName))).findAll("body")[0].findAll("div").filter( proc(divTag: XmlNode): bool = divTag.attr("id") != "" and divTag.attrs["id"] == "content" )[0].findAll("a"):
        # Adds the link if it has a title attribute and it isn't ignored
        try:
            # A list of prefixes to not take links of
            let title = link.attrs["title"]
            if (subpages.contains(title)):
                discard "Link already was found"
                raise
            const prefixIgnores = ["Special", "wikisource", "Category", "Portal", "Help", "s"]
            for badPrefix in prefixIgnores:
                if (title.startsWith(badPrefix & ":")):
                    discard "Link is actually not useful as it has a prefix that is ignored!"
                    raise
            subpages.add(title)
        except:
            discard "Link is useless because it doesn't have a title!"
    return subpages.deduplicate

## Gets the page to start at as either a command line argument or otherwise a hardcoded constant
let startPage = if paramCount() > 0: paramStr(1) else: "Nim (programming language)"

## A list of pages to their subpages
var pageBranches: Table[string, seq[string]] = {startPage : getSubPages(startPage)}.toTable

while not pageBranches.hasKey("Philosophy"):
    for branch in pageBranches.keys:
        for subBranch in pageBranches[branch]:
            if (pageBranches.hasKey(subBranch)):
                continue
            try:
                pageBranches[subBranch] = getSubPages(subBranch)
            except:
                discard "RIP"
            if (pageBranches.hasKey("Philosophy")):
                break
        if (pageBranches.hasKey("Philosophy")):
            break
echo pageBranches
