import os
import os.path

os.sys.path.append(os.path.dirname("../src/qcm_parser/"))
from parser import ParseQCM


def test_parser_web():
    expected_string = """## Un exemple avec une image

### Qui est-ce ?

![personne](https://media.vogue.fr/photos/5d8c8e536f878f000880cbd5/16:9/w_1920%2Cc_limit/000_ARP4090096.jpg)

- [x] Jacques Chirac
- [ ] Raymond Barre
- [ ] François Mitterand
- [ ] Valery Giscard d'Estaing

## maths : un exemple avec du LaTeX

### Calculer $2^3$

- [x] 8
- [ ] 6
- [ ] 4

## info : des exemples avec du code

### Évaluer `2 + 2 == 4`

- [x] `True`
- [ ] Vrai
- [ ] `TypeError`

### Évaluer `s` après l'exécution du code suivant :

```python
s = 0
for i in range(5):
  s += i
```

- [x] 10
- [ ] 15
- [ ] 0

## Français

### Un exemple avec une zone de texte

Écrire un sonnet.

- [t]

"""
    qcm = ParseQCM.from_file("../example/example.md", mode="web")
    assert repr(qcm) == expected_string, "Parsing example failed"

    assert qcm.title == "Exemple de QCM", "wrong title"

    assert qcm.parts[0].title == "Un exemple avec une image", "wrong part title"
    assert (
        qcm.parts[0].questions[0].question_title == "Qui est-ce ?"
    ), "wrong question title"
    assert (
        qcm.parts[0].questions[0].text
        == """<p><img alt="personne" src="https://media.vogue.fr/photos/5d8c8e536f878f000880cbd5/16:9/w_1920%2Cc_limit/000_ARP4090096.jpg" /></p>"""
    ), "wrong question text"

    assert qcm.parts[-2].title == "info : des exemples avec du code"
    assert (
        qcm.parts[-2].questions[1].question_title
        == "Évaluer <code>s</code> après l'exécution du code suivant :"
    )
    assert (
        qcm.parts[-2].questions[1].text
        == """<div class="codehilite"><pre><span></span><span class="n">s</span> <span class="o">=</span> <span class="mi">0</span>
<span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">5</span><span class="p">):</span>
  <span class="n">s</span> <span class="o">+=</span> <span class="n">i</span>
</pre></div>"""
    )

    assert qcm.parts[-1].questions[-1].is_text_question, "didn't detect text question"
    answers = qcm.parts[0].questions[0].answers
    assert answers[0].is_valid, "answer should be valid"
    assert answers[0].text == "Jacques Chirac", "didn't parse right correctly"
    assert answers[1].text == "Raymond Barre", "didn't parse wrong answer correctly"


def test_parser_pdf():
    qcm = ParseQCM.from_file("../example/example.md", mode="pdf")

    assert qcm.title == """Exemple de QCM""", "wrong title"
    assert qcm.parts[0].title == "Un exemple avec une image\n", "wrong part title"
    assert (
        qcm.parts[1].questions[0].question_title == "Calculer $2^3$\n"
    ), "wrong question title"
    assert qcm.parts[1].questions[0].answers[0].is_valid, "this answer should be valid"
    assert qcm.parts[1].questions[0].answers[0].text == " 8\n", "wrong question text"
    assert (
        qcm.parts[-2].questions[-1].text
        == """
```python
s = 0
for i in range(5):
  s += i
```

"""
    ), "wrong question text"


def test_all():
    test_parser_web()
    test_parser_pdf()


if __name__ == "__main__":
    test_all()
