# Projet : Liste d'épicerie et comparaison de prix

Résumé
-----
Outil simple pour maintenir une liste d'épicerie et comparer
les prix à partir d'un fichier Excel. L'application affiche le
meilleur prix trouvé et la feuille Excel d'origine.

Fonctionnalités
--------------
- Interface graphique minimaliste (tkinter) pour gérer la liste.
- Ajout / suppression d'articles dans `GroceryList.md`.
- Recherche du meilleur prix dans `prixEpicerie.xlsx`.
- Logging du prix le plus bas et du nom de la feuille source.

Installation
------------
1. Cloner ce dépôt sur votre machine Windows.
2. Créer et activer un environnement virtuel (optionnel).
3. Installer les dépendances :
   - pandas et openpyxl sont requis pour lire Excel.

Commandes pour windows :
```bash
python -m pip install --upgrade pip
python -m pip install pandas openpyxl
```

Fichiers importants
-------------------
- project_files/GroceryList.md
  - Liste d'articles utilisée par l'UI.
- project_files/prixEpicerie.xlsx
  - Exemple de fichier Excel contenant les prix.
- ListGUI.py
  - Interface principale (tkinter).
- FileManager.py
  - Fonctions utilitaires pour lire MD/Excel et chercher prix.


Utilisation
-----------
1. Placer/mettre à jour les fichiers dans `project_files/`.
2. Lancer l'interface :
```bash
python ListGUI.py
```
1. Ajouter des articles via l'UI ou modifier
   `GroceryList.md` manuellement.
2. Cocher les articles et cliquer sur "Check prices" pour voir
   le meilleur prix et la feuille source.

Format attendu pour l'Excel
---------------------------
- Un ou plusieurs onglets (feuilles).
- Une colonne contenant le nom de l'article.
- Une colonne voisine contenant le prix.
- Le module tente de convertir les valeurs en nombres.

Comportement et erreurs
-----------------------
- Si pandas n'est pas installé, les fonctions Excel
  renvoient un message d'erreur explicite.
- Si aucun prix valide n'est trouvé, un message clair est
  retourné/affiché.
- get_best_price() renvoie un dictionnaire :
  {'value': prix, 'sheet': nom_de_la_feuille}
