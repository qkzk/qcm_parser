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


## partie 1

### Calculer $1 +1$

- [x] 2
- [ ] 3
- [ ] 5

### Évaluer `2 ** 3`

- [x] 8
- [ ] 6
- [ ] 4

## partie 2

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

