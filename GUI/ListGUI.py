import tkinter as tk
import FileManager as list 

list_to_edit = "GroceryList.md"   
def bouton_active ():
    
    item = my_entry.get()
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
        my_entry.delete(0, tk.END)  # Clear the entry after adding the item


# Create the main window
root = tk.Tk()
root.title("grocery list")
root.geometry("300x700")
root.resizable(False, False)


# Create one Checkbutton per non-empty line in the file content
grocery_list_content = list.read_md_file(list_to_edit)
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

# Create a label to display the status


my_entry = tk.Entry(root, width=200)
my_entry.insert(0, "item name")
# Pack the add-button above the entry, then pack the entry at the bottom
bouton3 = tk.Button(root, text="Ajouter à la liste", command=bouton_active)
bouton3.pack(side='bottom', pady=5)
my_entry.pack(side='bottom', fill='x', padx=10, pady=(0, 10))
# Start the Tkinter event loop
root.mainloop()

