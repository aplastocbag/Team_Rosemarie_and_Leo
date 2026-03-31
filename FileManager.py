from typing import Iterable

def read_md_file(filepath):
    """Lire le contenu d'un fichier Markdown dans une chaîne.

    Objectif:
    - Lire un fichier Markdown et retourner son contenu sous forme de chaîne.
    - Si la première ligne non vide commence par un marqueur de titre Markdown ('#'),
      cette ligne sera supprimée du contenu retourné.
    - Les marqueurs de gras '**' sont retirés et le texte est converti en minuscules.

    Entrées:
    - filepath (str): chemin vers le fichier Markdown à lire.

    Sorties:
    - str: contenu traité du fichier en minuscules, ou message d'erreur en cas de problème.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # find the first non-empty line
        index = 0
        while index < len(lines) and lines[index].strip() == "":
            index += 1
            # if that line is a Markdown heading, remove it
        if index < len(lines) and lines[index].lstrip().startswith('#'):
            del lines[index]

        content = ''.join(lines)
        # remove Markdown bold markers '**' from the content
        # simple approach: strip literal '**' occurrences
        content = content.replace('**', '')
        content = content.lower()
        file.close()
        return content
    except FileNotFoundError:
        return f"Error: The file at {filepath} was not found."
    except Exception as e:
        return f"An error occurred: {e}"


def find_item_in_excel(filepath, item, item_col=None, value_col=None):
    """Rechercher un élément dans un fichier Excel et retourner les valeurs correspondantes avec le nom de la feuille.

    Objectif:
    - Parcourir toutes les feuilles d'un fichier Excel pour trouver les cellules correspondant à `item` (recherche insensible à la casse).
    - Pour chaque occurrence trouvée, renvoyer la valeur adjacente (ou la colonne spécifiée) ainsi que le nom de la feuille.

    Entrées:
    - filepath (str): chemin vers le fichier Excel.
    - item (str): texte à rechercher (insensible à la casse).
    - item_col (str|int|None): nom ou index de la colonne où effectuer la recherche; si None, toutes les colonnes sont parcourues.
    - value_col (str|int|None): nom ou index de la colonne dont on souhaite récupérer la valeur; si None, la colonne immédiatement à droite de l'item est utilisée.

    Sorties:
    - list[dict]: liste de dictionnaires {'sheet': nom_de_la_feuille, 'value': valeur} pour chaque correspondance trouvée.
    - str: message d'erreur en cas de problème (par exemple pandas non installé ou fichier introuvable).
    """
    try:
        import pandas as pd
    except ImportError:
        return "Error: pandas library is not installed. Please install it to use Excel lookups."

    try:
        # read all sheets into a dict: {sheet_name: DataFrame}
        sheets = pd.read_excel(filepath, sheet_name=None)
    except FileNotFoundError:
        return f"Error: The file at {filepath} was not found."
    except Exception as e:
        return f"An error occurred while reading Excel: {e}"

    search = str(item).strip().lower()
    results = []

    def get_value(excel_file, row_idx, col_idx):
        try:
            val = excel_file.iat[row_idx, col_idx]
            if pd.isna(val):
                return None
            return val
        except Exception:
            return None

    for sheet_name, excel_file in sheets.items():
        # determine columns to search for this sheet
        if item_col is not None:
            if isinstance(item_col, int):
                cols_to_search = [item_col]
            else:
                if item_col in excel_file.columns:
                    cols_to_search = [excel_file.columns.get_loc(item_col)]
                else:
                    # skip this sheet if the requested item_col isn't present
                    continue
        else:
            cols_to_search = list(range(len(excel_file.columns)))

        for col_idx in cols_to_search:
            try:
                col_series = excel_file.iloc[:, col_idx].astype(str).str.strip().str.lower()
            except Exception:
                continue

            matches = col_series == search
            match_indices = [i for i, m in enumerate(matches) if m]
            for row_idx in match_indices:
                if value_col is not None:
                    if isinstance(value_col, int):
                        val = get_value(excel_file, row_idx, value_col)
                    else:
                        if value_col in excel_file.columns:
                            val = get_value(excel_file, row_idx, excel_file.columns.get_loc(value_col))
                        else:
                            val = None
                else:
                    val = get_value(excel_file, row_idx, col_idx + 1) if col_idx + 1 < len(excel_file.columns) else None

                # try to convert to int when possible, otherwise keep original
                try:
                    if val is not None:
                        val = float(val)
                except Exception:
                    pass

                results.append({'sheet': sheet_name, 'value': val})

    return results

def get_best_price(item):
    """Obtenir le meilleur prix pour un article donné à partir d'un fichier Excel.

    Objectif:
    - Rechercher l'article spécifié dans le fichier Excel "prixEpicerie.xlsx" et retourner le prix le plus bas trouvé
      ainsi que le nom de la feuille contenant ce prix.

    Entrées:
    - item (str): nom de l'article pour lequel on souhaite obtenir le meilleur prix.

    Sorties:
    - tuple: (prix_meilleur (int|float), nom_de_la_feuille (str)) si un prix valide est trouvé.
    - str: message d'erreur si l'article n'est pas trouvé ou en cas de problème.
    """
    results = find_item_in_excel("project_files/prixEpicerie.xlsx", item)
    if isinstance(results, str):
        return results  # return error message from find_item_in_excel

    if not results:
        return f"No price found for '{item}'."

    # collect numeric candidates as (value, sheet)
    candidates = []
    for res in results:
        val = res.get('value')
        sheet = res.get('sheet')
        if val is None:
            continue
        try:
            num = float(val)
            candidates.append((num, sheet))
        except Exception:
            continue

    if not candidates:
        return f"No valid price found for '{item}'."

    try:
        best_price, best_sheet = min(candidates, key=lambda x: x[0])
        # return int when it's a whole number
        if best_price.is_integer():
            best_price = int(best_price)
        return (best_price, best_sheet)
    except Exception as e:
        return f"An error occurred while determining the best price: {e}"
    
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
            best_item = get_best_price(item)

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
