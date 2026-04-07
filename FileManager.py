from typing import Iterable, List, Dict, Any, Optional
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def _resolve_path(path: Optional[str], default: str) -> Path:
    """Resolve a path string to an absolute Path.

    Rules:
    - If path is falsy, return BASE_DIR/default.
    - If path is absolute, return it.
    - If a relative path exists relative to cwd, use that.
    - Otherwise resolve relative to BASE_DIR.
    """
    if not path:
        return BASE_DIR.joinpath(default).resolve()

    # accept pathlib.Path as input
    if isinstance(path, Path):
        p = path
    else:
        p = Path(path)
        print("using relative path: " + str(p))

    if p.is_absolute():
        return p.resolve()

    # prefer path relative to current working directory if it exists
    cwd_candidate = Path.cwd().joinpath(p)
    if cwd_candidate.exists():
        return cwd_candidate.resolve()

    # fallback: project-base relative path
    return BASE_DIR.joinpath(p).resolve()


def read_md_file(filepath: Optional[str] = None) -> str:
    """Lire le contenu d'un fichier Markdown dans une chaîne.

    Objectif:
    - Lire un fichier Markdown et retourner son contenu sous
      forme de chaîne.
    - Si la première ligne non vide commence par '#' elle est
      retirée.
    - Les marqueurs '**' sont retirés et le texte est mis en
      minuscules.

    Entrée:
    - filepath (str|None): chemin du fichier Markdown. Si None,
      on utilise 'project_files/GroceryList.md' relatif au projet.

    Sortie:
    - str: contenu traité ou message d'erreur.
    """
    path = _resolve_path(filepath, "project_files/GroceryList.md")
    try:
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # find the first non-empty line
        index = 0
        while index < len(lines) and lines[index].strip() == "":
            index += 1

        # if that line is a Markdown heading, remove it
        if index < len(lines) and lines[index].lstrip().startswith("#"):
            del lines[index]

        content = "".join(lines)
        content = content.replace("**", "")
        content = content.lower()
        return content
    except FileNotFoundError:
        return f"Error: The file at {path} was not found."
    except Exception as e:
        return f"An error occurred: {e}"


def find_item_in_excel(filepath: str, item: str,
                       item_col: Optional[Any] = None,
                       value_col: Optional[Any] = None):
    """Rechercher un élément dans un fichier Excel et retourner
    les valeurs correspondantes avec le nom de la feuille.

    filepath may be absolute or relative to the project root.
    """
    try:
        import pandas as pd
    except ImportError:
        return ("Error: pandas library is not installed. "
                "Please install it to use Excel lookups.")

    path = _resolve_path(filepath, "project_files/prixEpicerie.xlsx")
    try:
        # read all sheets into a dict: {sheet_name: DataFrame}
        sheets = pd.read_excel(path, sheet_name=None)
    except FileNotFoundError:
        return f"Error: The file at {path} was not found."
    except Exception as e:
        return f"An error occurred while reading Excel: {e}"

    search = str(item).strip().lower()
    results: List[Dict[str, Any]] = []

    def get_value(df, row_idx: int, col_idx: int):
        try:
            val = df.iat[row_idx, col_idx]
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
                col_series = (
                    excel_file.iloc[:, col_idx]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                )
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
                            val = get_value(
                                excel_file, row_idx,
                                excel_file.columns.get_loc(value_col)
                            )
                        else:
                            val = None
                else:
                    val = (
                        get_value(excel_file, row_idx, col_idx + 1)
                        if col_idx + 1 < len(excel_file.columns) else None
                    )

                try:
                    if val is not None:
                        val = float(val)
                except Exception:
                    pass

                results.append({"sheet": sheet_name, "value": val})

    return results


def get_best_price(item: str):
    """Obtenir le meilleur prix pour un article donné."""
    results = find_item_in_excel("project_files/prixEpicerie.xlsx", item)
    if isinstance(results, str):
        return results  # error message

    if not results:
        return f"No price found for '{item}'."

    candidates = []
    for res in results:
        val = res.get("value")
        sheet = res.get("sheet")
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
        if float(best_price).is_integer():
            best_price = int(best_price)
        return (best_price, best_sheet)
    except Exception as e:
        return f"An error occurred while determining the best price: {e}"


def print_checked_items(checked_items: Iterable[str]) -> None:
    """Affiche le meilleur prix pour chaque article sélectionné."""
    try:
        for item in checked_items:
            best_item = get_best_price(item)

            if isinstance(best_item, str):
                print(item + ": " + best_item)
                continue

            if isinstance(best_item, dict):
                val = best_item.get("value")
                sheet = best_item.get("sheet")
            elif isinstance(best_item, (list, tuple)) and len(best_item) >= 2:
                val, sheet = best_item[0], best_item[1]
            else:
                print(item + ": No price information available.")
                continue

            if val is None:
                print(item + ": No price found.")
                continue

            try:
                if isinstance(val, float) and val.is_integer():
                    val = int(val)
                print("The best price for " + item + " is "
                      + str(val) + "$ at " + str(sheet))
            except Exception:
                print(item + ": Invalid price value (" + str(val) + ")"
                      + " from sheet " + str(sheet))
    except Exception as e:
        print("An error occurred: " + str(e))


# write previous best prices using project-relative paths
best_prices = []
for list_item in read_md_file().split("\n"):
    item = list_item.strip()
    if item:
        best_item_price = get_best_price(item)
        best_prices.append((item, best_item_price))

out_path = _resolve_path(
    "project_files/previous_best_prices.txt",
    "project_files/previous_best_prices.txt"
)
try:
    with open(out_path, "w", encoding="utf-8") as file:
        for item, price_info in best_prices:
            if isinstance(price_info, str):
                file.write(f"{item}: {price_info}\n")
            elif isinstance(price_info, (list, tuple)) and len(price_info) >= 2:
                val, sheet = price_info[0], price_info[1]
                file.write(f"{item}: {val}$ at {sheet}\n")
            else:
                file.write(f"{item}: No price information available.\n")
except Exception:
    # non fatal for module import
    pass