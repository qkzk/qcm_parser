"""
title: qcm parser
author: qkzk
date: 2021/05/23

Parse a markdown file holding a QCM into multiple copies with shuffled
parts, questions and answsers.

Call it like that :

```bash
$ python qcm_parser.py "work/qcm.md"
```

It will generate "work/qcm_QUESTIONS.md" and "work/qcm_QUESTIONS.pdf" files.

It requires `pandoc`.
"""

import subprocess
import sys
from random import sample


class QCM_Content:
    """Holds the content of a QCM"""

    CONSTANT_HEADER = """
---
theme: "metropolis"
geometry: "margin=1.5cm"
header-includes:
- \\usepackage{fancyhdr}
- \\pagestyle{fancy}
- \\fancyhead[C]{QCM}
- \\fancyhead[LE,LO,RE,RO]{}
- \\fancyfoot[C]{\\thepage}
- \\thispagestyle{fancy}
- \\usepackage{tcolorbox}
- \\newtcolorbox{myquote}{colback=teal!10!white, colframe=teal!55!black}
- \\renewenvironment{Shaded}{\\begin{myquote}}{\\end{myquote}}

---

"""

    def __init__(self, lines: list[str]):
        self.lines = lines
        self.header, self.parts = self.separate_parts()

    def separate_parts(self) -> tuple[str, list["QCM_Part"]]:
        """Returns the header and the parts of the QCM"""
        end_header = self.find_end_header()
        start_end_parts = self.find_start_end_parts(end_header)
        # header = self.read_header(end_header)
        header = self.CONSTANT_HEADER
        return header, [self.read_part(start, end) for start, end in start_end_parts]

    def find_end_header(self) -> int:
        """Locate the end of the header ('---') in the markdown content"""
        for index, line in enumerate(self.lines):
            if index > 0 and line.startswith("---"):
                return index
        raise IndexError("No end of header found")

    def find_start_end_parts(self, end_header):
        """Locate the start and the end of the header in the file"""
        start_end_parts = []
        for index, line in enumerate(self.lines[end_header:], start=end_header):
            if line.startswith("## "):
                start = index
                if start_end_parts != []:
                    start_end_parts[-1].append(start)
                start_end_parts.append([start])
        start_end_parts[-1].append(len(self.lines) - 1)
        return start_end_parts

    def read_header(self, end_header) -> str:
        """Read the header of the markdown file"""
        return "".join(self.lines[: end_header + 1])
        # return self.CONSTANT_HEADER

    def read_part(self, start: int, end: int) -> "QCM_Part":
        """Returns a `QCM_Part` holding a part located between `start` and `end`"""
        return QCM_Part(self.lines[start:end])


class QCM_Part:
    """Holds a part of the QCM"""

    def __init__(self, lines: list[str]):
        self.lines = lines
        self.start_questions, self.title = self.read_title()
        self.questions_lines = self.read_questions()
        self.questions = [
            self.read_question(start, end) for start, end in self.questions_lines
        ]

    def __repr__(self):
        return "".join(self.lines)

    def read_title(self) -> tuple[int, str]:
        """Read the title of the part and returns its position and content"""
        for index, line in enumerate(self.lines):
            if line.startswith("## "):
                return index + 1, line
        raise ValueError(f"No title found for this part : {self}")

    def read_questions(self) -> list[tuple[int, int]]:
        """Returns a list of question as `QCM_Question` objects"""
        questions = []
        for index, line in enumerate(
            self.lines[self.start_questions :], start=self.start_questions
        ):
            if line.startswith("### "):
                start = index
                if questions != []:
                    questions[-1].append(start)
                questions.append([start])
        questions[-1].append(len(self.lines))
        return questions

    def read_question(self, start: int, end: int) -> "QCM_Question":
        """Read a single questions, returns a `QCM_Question` object"""
        return QCM_Question(self.lines[start:end])


class QCM_Question:
    """Holds a set of questions"""

    def __init__(self, lines: list[str]):
        self.lines = lines
        self.start_text, self.question_title = self.read_title()
        self.text, self.end_text = self.read_text()
        self.answers = self.read_answers()

    def __repr__(self):
        return "".join(self.lines)

    def read_title(self) -> tuple[int, str]:
        """read the title of the question from the string"""
        for index, line in enumerate(self.lines):
            if line.startswith("### "):
                return index + 1, line
        raise ValueError(f"No title found for this question : {self}")

    def read_text(self):
        """
        Read the 'text' of the question, the lines below the title and
        before the answer.
        """
        for index, line in enumerate(
            self.lines[self.start_text :], start=self.start_text
        ):
            if line.startswith("- ["):
                end = index
                return "".join(self.lines[self.start_text : end]), end
        raise ValueError(f"No text found for question {self}")

    def read_answers(self):
        """returns a list of answers from the content"""
        answers = []
        for line in self.lines[self.end_text :]:
            if line.startswith("- ["):
                answers.append("- [ ]" + line[5:])
        return answers


class QCM_Creator:
    """Holds the content of the QCM, exporting it to a new random set of questions"""

    def __init__(self, qcm: QCM_Content):
        self.qcm = qcm

    def export(self, first: bool = False) -> str:
        """shuffle the questions and anwsers, creating a set new QCM page"""
        string = self.qcm.header if first else ""
        parts = sample(self.qcm.parts, len(self.qcm.parts))
        for part in parts:
            string += part.title + "\n"
            questions = sample(part.questions, len(part.questions))
            for question in questions:
                string += question.question_title + "\n"
                string += question.text + "\n"
                answsers = sample(question.answers, len(question.answers))
                for answer in answsers:
                    string += answer
                string += "\n"
        string += "\n\n\\newpage\n\n"
        return string


def parse_args() -> tuple[str, int]:
    """parse the args, raising an exception there's not 2 given args"""
    if len(sys.argv) != 3:
        raise ValueError("I need a filename and and number")

    input_filename = sys.argv[1]
    nb_copy = int(sys.argv[2])
    return input_filename, nb_copy


def load_file(input_filename: str) -> list[str]:
    """open and read the file, returns its content"""
    with open(input_filename) as file_content:
        return file_content.readlines()


def read_qcm(file_content: list[str]) -> QCM_Content:
    """read and parse the content of the markdown file"""
    qcm = QCM_Content(file_content)
    return qcm


def generate_qcm(qcm_content: QCM_Content, nb_copy: int) -> str:
    """Generate the long string of questions to be writen"""
    string = ""
    for copy_nb in range(nb_copy):
        string += QCM_Creator(qcm_content).export(copy_nb == 0)
    return string


def write_qcm(output_content: str, input_filename: str) -> str:
    """write the questions to a file and returns its filename"""
    output_filename = input_filename[:-3] + "_QUESTIONS.md"
    with open(output_filename, "w") as output_file:
        output_file.write(output_content)
    return output_filename


def call_pandoc(output_filename: str):
    """call pandoc on the written file and convert it to pdf"""
    pdf_filename = output_filename[:-3] + ".pdf"
    args = ["pandoc", output_filename, "-o", pdf_filename]
    subprocess.check_call(args)


def main():
    """run the QCM converter against a file given in args"""
    input_filename, nb_copy = parse_args()
    input_content = load_file(input_filename)
    qcm_content = read_qcm(input_content)
    output_content = generate_qcm(qcm_content, nb_copy)
    output_filename = write_qcm(output_content, input_filename)
    call_pandoc(output_filename)


if __name__ == "__main__":
    main()
