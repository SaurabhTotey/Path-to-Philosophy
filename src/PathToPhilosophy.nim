import os
import strutils
import tables

## Defines a function that takes in a page name and formats it as a wikipedia URL
proc urlOf(pageName: string): string = 
    return r"https://en.wikipedia.org/wiki/" & pageName.splitWhitespace().join("_")

## Gets the page to start at as either a command line argument or otherwise a hardcoded constant
let startPage = if paramCount() > 0: paramStr(1) else: "Nim (programming language)"

## A list of pages to their subpages
var pageBranches = Table[string, seq[string]]()
