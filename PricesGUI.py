import tkinter as tk
import FileManager


def print_checked_items(checked_items):
    try:
        for item in checked_items:
            best_item = FileManager.get_best_price(item)

            # Si get_best_price renvoie un message d'erreur (str)
            if isinstance(best_item, str):
                print(f"{item}: {best_item}")
                continue

            # Support dict {'value','sheet'} ou tuple/list (value, sheet)
            if isinstance(best_item, dict):
                val = best_item.get('value')
                sheet = best_item.get('sheet')
            elif isinstance(best_item, (list, tuple)) and len(best_item) >= 2:
                val, sheet = best_item[0], best_item[1]
            else:
                print(f"{item}: No price information available.")
                continue

            if val is None:
                print(f"{item}: No price found.")
                continue

            try:
                # formater les nombres entiers sans décimales
                if isinstance(val, float) and val.is_integer():
                    val = int(val)
                print(f"The best price for {item} is {val}$ at {sheet}")
            except Exception:
                print(f"{item}: Invalid price value ({val}) from sheet {sheet}")
    except Exception as e:
        print(f"An error occurred: {e}")