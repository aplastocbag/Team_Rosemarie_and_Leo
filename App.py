import tkinter as tk
import FileReader as list 

        
def bouton_active ():
    print("tu as appuyer sur le bouton")
    item = my_entry.get()
    if item and item != "item name":
        with open("GroceryList_test.md", "a") as f:
            f.write("\n" + item )
        var = tk.IntVar()  # separate variable for the new checkbox
        checkbox = tk.Checkbutton(
            root,
            text=item,
            variable=var,
            command=lambda v=var, it=item: on_checkbox_toggle(v, it),
            onvalue=1,  # Value when checked
            offvalue=0  # Value when unchecked
        )
        checkbox.pack(pady=2, padx=10, anchor="w")  # Place the new checkbox in the window
        my_entry.delete(0, tk.END)  # Clear the entry after adding the item





def on_checkbox_toggle(var, item):
    # Update the status label for the specific item
    if var.get() == 1:
        status_label.config(text=f"{item}: checked")
    else:
        status_label.config(text=f"{item}: unchecked")

# Create the main window
root = tk.Tk()
root.title("grocery list")
root.geometry("300x800")
root.resizable(False, False)

padding = 0
# Create one Checkbutton per non-empty line in the file content
for item in list.file_content.split('\n'):
    text = item.strip()
    if text:
        var = tk.IntVar()  # separate variable per checkbox
        checkbox = tk.Checkbutton(
            root,
            text=text,
            variable=var,
            command=lambda v=var, it=text: on_checkbox_toggle(v, it),
            onvalue=1,  # Value when checked
            offvalue=0  # Value when unchecked
        )
        padding = 2
        checkbox.pack(pady=padding, padx=10, anchor="w")  # Place the checkbox in the window

# Create a label to display the status
status_label = tk.Label(root, text="Checkboxes are unchecked", fg="blue")
status_label.pack(pady=5)
"""
#creating columns

line1 = tk.Canvas(root, width=100, height=200)
line1.pack(pady=10)
line_id = line1.create_line(175, 0, 175, 180) 
line1.tag_raise(line_id)
"""
my_entry = tk.Entry(root,width=200)
my_entry.pack(pady= 10,anchor="s")
my_entry.insert(0,"item name")
bouton3 = tk.Button(root, text="ceci est un bouton", command=bouton_active)
bouton3.pack(pady=10,anchor="s")
# Start the Tkinter event loop
root.mainloop()

