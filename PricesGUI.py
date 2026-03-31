"""
Rosemarie Dalton et Leonard Lefebvre
Module PricesGUI

Objectif:
- Fournir une fonction utilitaire pour afficher le meilleur prix
  pour une liste d'articles sélectionnés.
- Gère les différents formats de retour de
  FileManager.get_best_price() et affiche des messages clairs.

Entrées / sorties:
- print_checked_items(checked_items)
    Entrée:
      checked_items -- itérable de chaînes (noms d'articles).
    Sortie:
      Aucun retour, affiche les résultats sur la sortie standard.
"""
from typing import Iterable
import FileManager


def print_checked_items(checked_items: Iterable[str]) -> None:
    """
    Affiche le meilleur prix pour chaque article sélectionné.

    Objectif:
    - Pour chaque article dans checked_items, appeler
      FileManager.get_best_price et afficher le résultat.
    - Gère les cas d'erreur et les différents formats de retour.

    Entrées:
    - checked_items: itérable de noms d'articles (str).

    Sorties:
    - None (affiche sur la console).
    """
    try:
        for item in checked_items:
            best_item = FileManager.get_best_price(item)

            # Si get_best_price renvoie un message d'erreur (str)
            if isinstance(best_item, str):
                print(item + ": " + best_item)
                continue

            # Support dict {'value','sheet'} ou tuple/list (value, sheet)
            if isinstance(best_item, dict):
                val = best_item.get('value')
                sheet = best_item.get('sheet')
            elif isinstance(best_item, (list, tuple)) and len(best_item) >= 2:
                val, sheet = best_item[0], best_item[1]
            else:
                print(item + ": No price information available.")
                continue

            if val is None:
                print(item + ": No price found.")
                continue

            try:
                # formater les nombres entiers sans décimales
                if isinstance(val, float) and val.is_integer():
                    val = int(val)
                # afficher le résultat
                print("The best price for " + item + " is " + str(val)
                      + "$ at " + str(sheet))
            except Exception:
                print(item + ": Invalid price value (" + str(val) + ")"
                      + " from sheet " + str(sheet))
    except Exception as e:
        print("An error occurred: " + str(e))