"""
title: String Parsers
author: qkzk
date: 2022/06/06

Classes of string parsers used in the parser.

Those parsers are used to read some string and export them if need.
Two are defined :

# 1. for the web

Strings or list of strings are rendered from markdown strings into html strings

# 2. for a pdf

Strings aren't modified. Since the original document is a .md and the destination too, 
no need to edit them.

All StringParsers inherit from `StringParsers` and should have the same signature :

* non instanciable classes
* `line(str) -> str` method, for parsing single line,
* `bloc(list[str]) -> str` method, joining and formatting list of lines.


"""
from typing import List
import re

import markdown

EXTENSIONS = ["fenced_code", "codehilite", "tables"]


class StringParsers:
    """
    Baseclass for parsers of string or list of string.
    """

    def __new__(cls, *args, **kwargs):
        """This class should not be instanciated."""
        raise RuntimeError(f"{cls} should not be instantiated")

    @staticmethod
    def line(_: str) -> str:
        raise NotImplemented

    @staticmethod
    def bloc(_: List[str]) -> str:
        raise NotImplemented


class WebParsers(StringParsers):
    """
    Holds two static methods allowing the parsing
    of

    a single line, parsed as markdown
    a list of lines, joined and parsed as markdown with code hilite
    """

    @staticmethod
    def line(line: str) -> str:
        """
        Strip enclosing paragraph marks, <p> ... </p>,
        which markdown() forces, and which interfere with some jinja2 layout
        """
        return re.sub(
            "(^<P>|</P>$)",
            "",
            markdown.markdown(line, extensions=EXTENSIONS),
            flags=re.IGNORECASE,
        )

    @staticmethod
    def bloc(bloc: List[str]) -> str:
        """Join a list of strings into a markdowned string"""
        return markdown.markdown(
            "".join(
                bloc,
            ),
            extensions=EXTENSIONS,
        )


class PDFParsers(StringParsers):
    """
    Used for QCM which should be printed.
    Doesn't do much to the strings it receives.
    """

    @staticmethod
    def line(line: str) -> str:
        """Identity function. Returns the same string that was received."""
        return line

    @staticmethod
    def bloc(bloc: List[str]) -> str:
        """Join a list of str into a string."""
        return "".join(bloc)
