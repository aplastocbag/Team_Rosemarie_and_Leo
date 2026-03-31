"""
Interface GUI pour la liste d'épicerie.

Objectifs:
- Afficher une liste d'articles à partir d'un fichier Markdown.
- Permettre l'ajout d'un nouvel article à la liste.
- Vérifier les meilleurs prix via PricesGUI.

Limites:
- Ce module utilise tkinter et FileManager.
- Le fichier de liste est 'GroceryList.md' par défaut.
"""
import tkinter as tk
import FileManager
import PricesGUI

# Nom du fichier markdown contenant la liste
list_to_edit = "GroceryList.md"


def bouton_active():
    """
    Ajouter l'item entré dans le fichier et l'interface.

    Entrée:
    - lecture dans le widget 'new_item_widget'.

    Effets:
    - Ajoute l'item au fichier list_to_edit.
    - Ajoute une case à cocher correspondante à la fenêtre.
    """
    item = new_item_widget.get()
    if not item or item == "item name":
        return

    # Append item to the markdown file
    with open(list_to_edit, "a", encoding="utf-8") as file:
        file.write("\n" + item)

    # Message court de confirmation
    print(f"tu as ajouté {item} à la liste")

    # Créer une variable dédiée pour la nouvelle case
    var = tk.IntVar()
    checkbox = tk.Checkbutton(
        root,
        text=item,
        variable=var,
        onvalue=1,
        offvalue=0
    )
    checkbox.pack(pady=2, padx=10, anchor="w")

    # Effacer l'entrée utilisateur après insertion
    new_item_widget.delete(0, tk.END)


# Création de la fenêtre principale
root = tk.Tk()
root.title("grocery list")
root.geometry("300x700")
root.resizable(False, False)

# Charger le contenu du fichier et créer les cases
grocery_list_content = FileManager.read_md_file(list_to_edit)
for item in grocery_list_content.split('\n'):
    text = item.strip()
    if not text:
        continue

    var = tk.IntVar()
    checkbox = tk.Checkbutton(
        root,
        text=text,
        variable=var,
        onvalue=1,
        offvalue=0
    )
    checkbox.pack(pady=2, padx=10, anchor="w")


def checked_items():
    """
    Récupérer la liste des items cochés.

    Retour:
    - liste de chaînes (textes des Checkbutton cochés).
    """
    checked = []
    for widget in root.winfo_children():
        if not isinstance(widget, tk.Checkbutton):
            continue

        # cget("variable") renvoie le nom de la var Tk
        var_name = widget.cget("variable")
        try:
            val = root.getvar(var_name)
        except Exception:
            continue

        try:
            if int(val) == 1:
                checked.append(widget.cget("text"))
        except Exception:
            if str(val).lower() in ("1", "true", "yes"):
                checked.append(widget.cget("text"))

    return checked


# Widget pour ajouter un nouvel item
new_item_widget = tk.Entry(root, width=30)
new_item_widget.insert(0, "item name")

# Bouton pour vérifier les prix des items cochés
check_prices_button = tk.Button(
    root,
    text="Check prices",
    command=lambda: PricesGUI.print_checked_items(checked_items())
)
check_prices_button.pack(side="bottom", pady=5)

# Bouton pour ajouter l'item au fichier et à l'UI
add_item_button = tk.Button(
    root,
    text="Ajouter à la liste",
    command=bouton_active
)
add_item_button.pack(side="bottom", pady=5)




# Placer l'entrée en bas
new_item_widget.pack(side="bottom", fill="x", padx=10, pady=(0, 10))

# Démarrer la boucle principale tkinter
root.mainloop()