# QCM parser

```bash
$ qcm_parser qcm.md 10
```

génère 10 exemplaires du QCM avec les questions mélangées, appelle pandoc dessus pour en faire
un pdf

- [x] lire/parser les arguments
- [x] lire le doc et repérer les balises {qcm}
- [x] mélanger les réponses
- [x] générer les x exemplaires avec ordre aléatoire des questions et des réponses
- [x] appeler pandoc sur le source généré

## `read_qcm`

Un QCM est constitué de :

* Entête

  ```markdown
  ---
  title: "Exemple de QCM"
  subtitle: "pour tester l'application"
  author: "qkzk"
  date: "2021/05/23"
  theme: "metropolis"
  geometry: "margin=1.5cm"
  header-includes: |
      \usepackage{tcolorbox}
      \newtcolorbox{myquote}{colback=teal!10!white, colframe=teal!55!black}
      \renewenvironment{Shaded}{\begin{myquote}}{\end{myquote}}

  ---
  ```

* Partie : `## partie truc` 
* Question : `### Combien font 2+2 ?` puis bloc de texte `Choisissez la bonne réponse`
* Réponses :

  ```md
  - [x] bonne réponse
  - [ ] mauvaise réponse

  ```


## Attention

* L'entête doit contenir un champ `title: "blablabla"` qui partira dans l'entête,
* Idéalement le QCM fait une page
