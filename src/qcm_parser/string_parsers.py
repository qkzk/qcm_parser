import re

import markdown

EXTENSIONS = ["fenced_code", "codehilite", "tables"]


class StringParsers:
    """
    Baseclass for parsers of string or list of string.
    """

    @staticmethod
    def line(_: str) -> str:
        raise NotImplemented

    @staticmethod
    def bloc(_: list[str]) -> str:
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
    def bloc(bloc: list[str]) -> str:
        return markdown.markdown(
            "".join(
                bloc,
            ),
            extensions=EXTENSIONS,
        )


class PDFParsers(StringParsers):
    @staticmethod
    def line(line: str) -> str:
        return line

    @staticmethod
    def bloc(bloc: list[str]) -> str:
        return "".join(bloc)
