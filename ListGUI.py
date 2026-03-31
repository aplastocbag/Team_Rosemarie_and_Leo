import tkinter as tk
import FileManager
import PricesGUI

list_to_edit = "GroceryList.md"   
def bouton_active ():
    
    item = new_item_widget.get()
    if item and item != "item name":
        with open(list_to_edit, "a") as file:
            file.write("\n" + item )
        file.close()
        print("tu as ajouté " + item + " à la liste")
        var = tk.IntVar()  # separate variable for the new checkbox
        checkbox = tk.Checkbutton(
            root,
            text=item,
            variable=var,
            onvalue=1,  # Value when checked
            offvalue=0  # Value when unchecked
        )
        checkbox.pack(pady=2, padx=10, anchor="w")  # Place the new checkbox in the window
        new_item_widget.delete(0, tk.END)  # Clear the entry after adding the item


# Create the main window
root = tk.Tk()
root.title("grocery list")
root.geometry("300x700")
root.resizable(False, False)


# Create one Checkbutton per non-empty line in the file content
grocery_list_content = FileManager.read_md_file(list_to_edit)
for item in grocery_list_content.split('\n'):
    text = item.strip()
    if text:
        var = tk.IntVar()  # separate variable per checkbox
        checkbox = tk.Checkbutton(
            root,
            text=text,
            variable=var,
            
            onvalue=1,  # Value when checked
            offvalue=0  # Value when unchecked
        )
        padding = 2
        checkbox.pack(pady=padding, padx=10, anchor="w")  # Place the checkbox in the window

def checked_items():
    checked = []
    for widget in root.winfo_children():
        if isinstance(widget, tk.Checkbutton):
            var_name = widget.cget("variable")  # retourne le nom de la variable Tk (ex: 'PY_VAR0')
            try:
                val = root.getvar(var_name)      # obtenir la valeur réelle de la variable
            except Exception:
                continue
            try:
                if int(val) == 1:
                    checked.append(widget.cget("text"))
            except Exception:
                if str(val).lower() in ("1", "true", "yes"):
                    checked.append(widget.cget("text"))
    return checked
# Create a label to display the status

new_item_widget = tk.Entry(root, width=200)
new_item_widget.insert(0, "item name")
# Pack the add-button above the entry, then pack the entry at the bottom
add_item_button = tk.Button(root, text="Ajouter à la liste", command=bouton_active)
add_item_button.pack(side='bottom', pady=5)
check_prices_button = tk.Button(root, text="Check prices", command=lambda: PricesGUI.print_checked_items(checked_items()))
check_prices_button.pack(side='bottom', pady=5)
new_item_widget.pack(side='bottom', fill='x', padx=10, pady=(0, 10))
# Start the Tkinter event loop
root.mainloop()