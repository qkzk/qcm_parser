"""
title: QCM parser
author: qkzk
date: 2021/06/28
"""
from typing import List, Tuple, Type

from .string_parsers import StringParsers, WebParsers, PDFParsers


class ParseQCMError(Exception):
    """Exception raised when parsing went wrong."""


class ParseQCM:
    """
    Parse a QCM into a QCM class.
    Raise `ParseQCMError` if parsing went wrong.
    """

    def __init__(self, lines: list, mode="web"):
        self._parsers = self._define_string_parsers(mode)
        self._lines = lines
        self._title = self._read_title()
        self._parts = self._separate_parts()

    @property
    def title(self) -> str:
        """The QCM title"""
        return self._title

    @property
    def parts(self) -> List["QCM_Part"]:
        """The QCM parts"""
        return self._parts

    @staticmethod
    def _define_string_parsers(mode: str) -> Type[StringParsers]:
        """Define the function used to parse lines"""
        if mode == "web":
            return WebParsers
        elif mode == "pdf":
            return PDFParsers
        else:
            raise ParseQCMError(
                f"mode {mode} is unknown. Use 'web' for html export or 'pdf' to creates a markdown file."
            )

    def _read_title(self):
        title = ""
        is_code_block = False
        for line in self._lines:
            if line.startswith("```"):
                is_code_block = not is_code_block
            if not is_code_block and "title: " in line and not "subtitle" in line:
                start = line.index(":") + 2
                title = line[start:-1].strip().replace('"', "").replace("''", "")
            if not is_code_block and line.startswith("# "):
                title = self._parsers.line(line[2:])
        if not title:
            raise ParseQCMError("The QCM has no title.")
        return title

    def _separate_parts(self) -> list:
        """Returns  the parts of the QCM"""
        end_header = self._find_end_header()
        start_end_parts = self._find_start_end_parts(end_header)
        return [self._read_part(start, end) for start, end in start_end_parts]

    def _find_end_header(self) -> int:
        """Locate the end of the header ('---') in the markdown content"""
        end_header = 0
        for index, line in enumerate(self._lines):
            if index > 0 and line.startswith("---"):
                end_header = index
        return end_header

    def _find_start_end_parts(self, end_header) -> list:
        """Locate the start and the end of the header in the file"""
        start_end_parts = []
        is_code_block = False
        for index, line in enumerate(self._lines[end_header:], start=end_header):
            if line.startswith("```"):
                is_code_block = not is_code_block
            if line.startswith("## ") and not is_code_block:
                start = index
                if start_end_parts != []:
                    start_end_parts[-1].append(start)
                start_end_parts.append([start])
        if not start_end_parts:
            raise ParseQCMError("The QCM has no parts")
        start_end_parts[-1].append(len(self._lines))
        return start_end_parts

    def _read_header(self, end_header) -> str:
        """Read the header of the markdown file"""
        return "".join(self._lines[: end_header + 1])

    def _read_part(self, start: int, end: int) -> "QCM_Part":
        """Returns a `QCM_Part` holding a part located between `start` and `end`"""
        return QCM_Part(self._lines[start:end], self._parsers)

    @classmethod
    def from_file(cls, input_filename: str, mode="web") -> "ParseQCM":
        """
        Open and read an utf-8 encoded QCM file, returns a parsed QCM.
        Raise various kinds of errors if the QCM isn't encoded properly.
        """
        with open(input_filename, encoding="utf-8") as file_content:
            return cls(
                file_content.readlines(),
                mode=mode,
            )

    @classmethod
    def from_file_into_dict(cls, input_filename: str, return_dict: dict, **kwargs):
        """
        Parse a QCM using with given parameters.

        Try to parse `input_filename`.
            If the parsing is done correctly, stores it into `return_dict["qcm"]`
            Else, stores the Exception into `return_dict["error"]`

        This interface is there to allow parsing from a Process.
        """
        mode = kwargs.get("mode", "web")
        try:
            qcm = cls.from_file(input_filename, mode=mode)
            return_dict["qcm"] = qcm
        except (ParseQCMError, UnicodeDecodeError) as e:
            return_dict["error"] = e

    def __repr__(self):
        return "".join(map(repr, self._parts))


class QCM_PartError(ParseQCMError):
    """Exception raised when parsing a `QCM_Part` went wrong."""


class QCM_Part:
    """Holds a part of the QCM"""

    def __init__(self, lines: list, parsers: Type[StringParsers]):
        self._lines = lines
        self._parsers = parsers
        self._start_questions, self._title = self._read_title()
        self._questions_lines = self._read_questions()
        self._questions = [
            self._read_question(start, end) for start, end in self._questions_lines
        ]

    @property
    def title(self) -> str:
        """Part title"""
        return self._title

    @property
    def questions(self) -> List["QCM_Question"]:
        """Questions in this part"""
        return self._questions

    def __repr__(self):
        return "".join(self._lines)

    def _read_title(self) -> tuple:
        """Read the title of the part and returns its position and content"""
        for index, line in enumerate(self._lines):
            if line.startswith("## "):
                return index + 1, self._parsers.line(line[3:])
        raise QCM_PartError(f"No title found for this part : {self}")

    def _read_questions(self) -> list:
        """Returns a list of line indexes questions"""
        questions = []
        is_code_block = False
        for index, line in enumerate(
            self._lines[self._start_questions :], start=self._start_questions
        ):
            if line.startswith("```"):
                is_code_block = not is_code_block
            if line.startswith("### ") and not is_code_block:
                start = index
                if questions != []:
                    questions[-1].append(start)
                questions.append([start])
        if not questions:
            raise QCM_PartError("The part has no question.")
        questions[-1].append(len(self._lines))
        return questions

    def _read_question(self, start: int, end: int) -> "QCM_Question":
        """Read a single questions, returns a `QCM_Question` object"""
        return QCM_Question(self._lines[start:end], self._parsers)


class QCM_QuestionError(ParseQCMError):
    """Raised when parsing a question went wrong"""


class QCM_Question:
    """Holds a set of questions"""

    def __init__(self, lines: list, parsers: Type[StringParsers]):
        self._lines = lines
        self._parsers = parsers
        self._start_text, self._title = self._read_title()
        self._text, self._end_text = self._read_text()
        self._is_text_question = False
        self._answers = self._read_answers()
        self._reject_wrong_question()

    @property
    def title(self) -> str:
        """Question title"""
        return self._title

    @property
    def text(self) -> str:
        """Question sub text"""
        return self._text

    @property
    def answers(self) -> List["QCM_Answer"]:
        """Answers in this part"""
        return self._answers

    @property
    def is_text_question(self) -> bool:
        """Question sub text"""
        return self._is_text_question

    def _reject_wrong_question(self):
        """
        Raise QCM_QuestionError if the question has no valid answer and isn't a text question.
        """
        if not self._is_text_question and not self._has_valid_answers():
            raise QCM_QuestionError(
                "Question should be 'text question' or have at least one valid answers"
            )

    def _has_valid_answers(self) -> bool:
        """True iff there's at least one valid answer"""
        return len([answer for answer in self._answers if answer._is_valid]) > 0

    def __repr__(self):
        return "/n".join([self._title, self._text] + list(map(repr, self._answers)))

    def _read_title(self) -> tuple:
        """read the title of the question from the string"""
        for index, line in enumerate(self._lines):
            if line.startswith("### "):
                return index + 1, self._parsers.line(line[4:])
        raise QCM_QuestionError(f"The question has no title")

    def _read_text(self) -> Tuple[str, int]:
        """
        Read the 'text' of the question, the lines below the title and
        before the answer.
        """
        for index, line in enumerate(
            self._lines[self._start_text :], start=self._start_text
        ):
            if line.startswith("- ["):
                end = index
                return (
                    self._parsers.bloc(
                        self._lines[self._start_text : end],
                    ),
                    end,
                )
        raise QCM_QuestionError(f"No text found for question {self}")

    def _read_answers(self) -> List["QCM_Answer"]:
        """
        Returns a list of answers from the content.
        Set the `is_text_question` flag if it's a text question.

        if there's answers, it can't be a "text_question".
        """
        answers = []
        for line in self._lines[self._end_text :]:
            if line.startswith("- [t]"):
                self._is_text_question = True
                if answers:
                    raise QCM_QuestionError(
                        "Question can't be a `text_question` and have answers."
                    )
                return []
            elif line.startswith("- ["):
                answers.append(QCM_Answer.from_line(line, self._parsers))
        return answers


class QCM_Answer:
    """Holds an answer and a status, valid or not"""

    def __init__(self, title: str, is_valid: bool):
        self._title = title
        self._is_valid = is_valid

    @property
    def title(self) -> str:
        """Answer title"""
        return self._title

    @property
    def is_valid(self) -> bool:
        """Is this answer valid ?"""
        return self._is_valid

    @classmethod
    def from_line(cls, line: str, parsers: Type[StringParsers]) -> "QCM_Answer":
        """Creates an answer from a line starting with - [ ] or - [x]"""
        text = parsers.line(line[5:])
        is_valid = "[x]" in line[:5]
        return cls(text, is_valid)

    def __repr__(self):
        return f"    - [{'x' if self._is_valid else ' '}] {self._title}"
