"""
Interface combinée:
- gauche: gestion de la liste d'épicerie (checkboxes)
- droite: contrôle des feuilles Excel à ignorer et tableau
  affichant le meilleur prix pour les items cochés.

Objectifs:
- Conserver l'apparence précédente tout en regroupant
  les deux fenêtres en une seule.
- Permettre d'ignorer des feuilles et de rafraîchir le
  tableau sans bloquer l'UI.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Iterable

import FileManager

try:
    import pandas as pd
except Exception:
    pd = None


# chemin des fichiers (résolus par rapport au dossier du projet)
grocery_list = FileManager._resolve_path(
    "../GroceryList.md",
    "project_files/GroceryList.md"
)
xlsx_path = FileManager._resolve_path(
    "../prixEpicerie.xlsx",
    "project_files/prixEpicerie.xlsx"
)

# conservation des IntVar et widgets pour gestion fiable
_checkbox_vars = []  # list of (text, tk.IntVar, tk.Checkbutton)


def _create_checkbox(text: str, parent, pack=True):
    """Créer et attacher une case à cocher pour `text`."""
    var = tk.IntVar(value=0)
    cb = tk.Checkbutton(
        parent,
        text=text,
        variable=var,
        onvalue=1,
        offvalue=0,
        anchor="w",      # align widget contents to the left
        justify="left"  # align text to the left
    )
    if pack:
        cb.pack(pady=2, padx=6, anchor="w", fill="x")
    _checkbox_vars.append((text, var, cb))
    return cb


def add_item(entry_widget):
    """
    Ajouter l'item entré dans le fichier et l'interface.
    """
    item = entry_widget.get().strip()
    if not item or item == "item name":
        return

    try:
        with open(grocery_list, "a", encoding="utf-8") as file:
            file.write("\n" + item)
    except Exception as e:
        messagebox.showerror("Error", "Cannot write grocery file:\n" + str(e))
        return

    _create_checkbox(item, left_list_frame, pack=True)
    entry_widget.delete(0, tk.END)


def delete_checked_items():
    """Supprimer les items cochés de l'UI et du fichier."""
    to_remove = [t for (t, v, cb) in _checkbox_vars if v.get() == 1]
    if not to_remove:
        return

    # update file
    try:
        with open(grocery_list, "r", encoding="utf-8") as file:
            lines = [ln.rstrip("\n") for ln in file.readlines()]
        filtered = [ln for ln in lines if ln.strip() not in to_remove]
        with open(grocery_list, "w", encoding="utf-8") as file:
            file.write("\n".join(filtered))
    except Exception as e:
        messagebox.showerror("Error", "Cannot update file:\n" + str(e))
        return

    # remove widgets
    for text in to_remove:
        for tup in list(_checkbox_vars):
            if tup[0] == text:
                _, _, cb = tup
                cb.destroy()
                _checkbox_vars.remove(tup)


def checked_items() -> List[str]:
    """Retourne la liste des textes des Checkbutton cochés."""
    return [t for (t, v, _) in _checkbox_vars if v.get() == 1]


def _get_sheet_names(xlsx_path: str) -> List[str]:
    """Retourne la liste des feuilles d'un fichier Excel."""
    if pd is None:
        return []
    try:
        xls = pd.ExcelFile(xlsx_path)
        return list(xls.sheet_names)
    except Exception:
        return []


def _best_for_item_excluding(item: str, ignored: List[str]):
    """Retourne le meilleur prix pour item en excluant des sheets.

    Retourne:
    - dict {'value': prix, 'sheet': nom} si trouvé
    - None si aucun prix valide
    - str message d'erreur si problème
    """
    results = FileManager.find_item_in_excel(xlsx_path, item)
    if isinstance(results, str):
        return results

    candidates = []
    for res in results:
        if isinstance(res, dict):
            val = res.get("value")
            sheet = res.get("sheet")
        elif isinstance(res, (list, tuple)) and len(res) >= 2:
            val, sheet = res[0], res[1]
        else:
            continue

        if sheet in ignored:
            continue
        if val is None:
            continue
        try:
            num = float(val)
            candidates.append((num, sheet))
        except Exception:
            continue

    if not candidates:
        return None

    best_price, best_sheet = min(candidates, key=lambda x: x[0])
    if float(best_price).is_integer():
        best_price = int(best_price)
    return {"value": best_price, "sheet": best_sheet}


# --- création fenêtre principale ---
root = tk.Tk()
root.title("Grocery & Prices")
root.geometry("900x680")
root.minsize(700, 480)

# cadre gauche: liste d'épicerie et contrôles
left_frame = tk.Frame(root)
left_frame.pack(side="left", fill="both", expand=False, padx=6, pady=6)

tk.Label(left_frame, text="Grocery list").pack(anchor="w")

left_list_frame = tk.Frame(left_frame)
left_list_frame.pack(fill="both", expand=True, padx=2, pady=4)

# charger le contenu du fichier et créer les cases
try:
    content = FileManager.read_md_file(grocery_list)
except TypeError:
    content = FileManager.read_md_file()
except Exception:
    content = ""
for item in content.splitlines():
    text = item.strip()
    if not text:
        continue
    _create_checkbox(text, left_list_frame, pack=True)

# entry et boutons gauche
new_item_widget = tk.Entry(left_frame, width=28)
new_item_widget.insert(0, "item name")
new_item_widget.pack(side="bottom", fill="x", padx=6, pady=(4, 6))

add_item_button = tk.Button(
    left_frame, text="Add to list",
    command=lambda: add_item(new_item_widget)
)
add_item_button.pack(side="bottom", pady=4, padx=6, fill="x")

delete_items_button = tk.Button(
    left_frame, text="Delete checked items",
    command=delete_checked_items
)
delete_items_button.pack(side="bottom", pady=4, padx=6, fill="x")


# cadre droit: feuilles + tableau des prix
right_frame = tk.Frame(root)
right_frame.pack(side="right", fill="both", expand=True, padx=6, pady=6)

tk.Label(right_frame, text="Sheets to ignore").pack(anchor="w")

sheets_frame = tk.Frame(right_frame)
sheets_frame.pack(anchor="nw", fill="x", padx=2, pady=4)

# sheet vars
sheet_vars: Dict[str, tk.IntVar] = {}
sheet_names = _get_sheet_names(xlsx_path)
if pd is None:
    msg = ("pandas is required to read Excel files.\n"
           "Install pandas and openpyxl.")
    tk.Label(sheets_frame, text=msg, fg="red").pack(anchor="w")
else:
    for name in sheet_names:
        var = tk.IntVar(value=0)
        cb = tk.Checkbutton(
            sheets_frame,
            text=name,
            variable=var,
            onvalue=1,
            offvalue=0,
            anchor="w",      # align widget contents to the left
            justify="left"  # align text to the left
        )
        # pack to full width so text starts at the left edge
        cb.pack(anchor="w", fill="x", padx=2)
        sheet_vars[name] = var

# tableau (Treeview)
cols = ("item", "price", "sheet")
tree = ttk.Treeview(right_frame, columns=cols, show="headings", height=18)
tree.heading("item", text="Item")
tree.heading("price", text="Price")
tree.heading("sheet", text="Sheet")
tree.column("item", width=260, anchor="w")
tree.column("price", width=100, anchor="center")
tree.column("sheet", width=160, anchor="w")
tree.pack(fill="both", expand=True, padx=2, pady=6)

vsb = ttk.Scrollbar(right_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
vsb.pack(side="right", fill="y")

status_label = tk.Label(right_frame, text="")
status_label.pack(anchor="w", pady=(0, 6))


def _update_table():
    """Rafraîchit le tableau en fonction des items cochés et
    des feuilles ignorées."""
    ignored = [n for n, v in sheet_vars.items() if v.get() == 1]
    # vider le tableau
    for r in tree.get_children():
        tree.delete(r)

    items = checked_items()
    any_error = False
    for item in items:
        best = _best_for_item_excluding(item, ignored)
        if isinstance(best, str):
            tree.insert("", "end", values=(item, best, ""))
            any_error = True
            continue
        if best is None:
            tree.insert("", "end", values=(item, "No price", ""))
            continue
        val = best.get("value")
        sheet = best.get("sheet")
        tree.insert("", "end", values=(item, str(val) + "$", sheet))

    status = "Ignored: " + ", ".join(ignored) if ignored else ""
    if any_error:
        status = "Errors occurred. " + status
    status_label.config(text=status)


# boutons tableau
btn_frame = tk.Frame(right_frame)
btn_frame.pack(fill="x", pady=(0, 6))

refresh_btn = tk.Button(btn_frame, text="Check item prices", command=_update_table)
refresh_btn.pack(side="left", padx=(0, 6))

refresh_all_btn = tk.Button(
    btn_frame, text="Refresh all items",
    command=lambda: _update_table()
)
refresh_all_btn.pack(side="left", padx=(0, 6))

# initial fill
_update_table()

# démarrer la boucle principale tkinter
root.mainloop()