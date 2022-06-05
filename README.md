# QCM parser

It's a basic and quite strict QCM (Multiple Choices Questions) parser.

It parses a file .md file into Python objects. 
That's all.

There's no rendering, no export. It must be done separetaly.

## Installation

It requires python>=3.7 and `markdown` package.

```bash
$ pip install qcm_parser
```

## Usage

In your script :

```python
from qcm_parser.parser import ParseQCM

qcm = ParseQCM.from_file("my_qcm_file.md")

print(qcm)
```

Will display your QCM as a text.

In memory, you `qcm` object is represented as a tree which holds parts.

Those parts holds questions, holding answers.

It is then easy to navigate through it like this :


```
print(qcm.title)
for part in qcm.parts:
    print(part.title)
    for question in part.questions:
        print(question.question_title)
        print(question.text)
        for answer in question.answers:
            print(answer.answer)
```

## Modes

There's 2 modes : 

* for web export (`qcm_part.from_file(filename, mode="web")`), the default one, `mode` named parameter can be ommitted.
* for pdf export (`qcm_part.from_file(filename, mode="pdf")`).

The `mode=web` should be used if you want to serve a QCM like I do here.

It replaces `markdown` syntax with `html` syntax using `markdown` module.

The `mode=pdf` can be used to create a randomized QCM in a .md file, then to export it with pandoc.

## QCM file description

**Files should be utf-8 encoded text files with .md extensions.**

They should respect the [example](./example/example.md) format :

```markdown

# title

## part

### question with multiple choices

optional sub text. Can contains code, latex, whatever

- [x] right answer
- [ ] wrong answer a
- [ ] wrong answer b

### question with text allowed 

- [t]
```

## Known limitations

Only a little subset of markdown is supported.

1. A title must be found
2. title, parts and questions can't have empty string after `#`, `##` or `###` tag

    ```mardown
    ## valid part

    ## 
    wrong part
    ```
3. Code blocks with triple backticks are supported not `~~~`. Those will creates bugs.

    ~~~markdown
    # title
    
    ## part

    ### question

    ```python
    # comment
    def f():
        return 1
    ```
    ~~~

    is valid.

    but :

    ```markdown
    # title
    
    ## part

    ### question

    ~~~python
    # comment
    def f():
        return 1
    ~~~
    
    ```

    **is not valid.**

    The `# comment` line will be interpreted as a new title etc.
