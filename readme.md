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
* Partie : `##` 
* Question : `###` puis bloc de texte
* Réponses :

  ```md
  - [x] bonne réponse
  - [ ] mauvaise réponse

  ```
