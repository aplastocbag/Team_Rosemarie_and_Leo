

def read_md_file(filepath):
    """Reads the content of a Markdown file into a string.

    if the first non-empty line starts with
    a Markdown heading marker ('#'), that line will be removed from
    the returned content.
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

def read_excel_file(filepath):
    """Reads the content of an Excel file into a string."""
    try:
        import pandas as pd
        excel_file = pd.read_excel(filepath)
        content = excel_file.to_string(index=False)  # Convert DataFrame to string without index
        content = content.lower()  # Convert the content to lowercase for case-insensitive search
        content = content.strip()  # Remove leading and trailing whitespace
        excel_file.close()
        return content
    except FileNotFoundError:
        return f"Error: The file at {filepath} was not found."
    except ImportError:
        return "Error: pandas library is not installed. Please install it to read Excel files. To install pandas, run: python -m pip install pandas, then python -m pip install openpyxl"
    except Exception as e:
        return f"An error occurred: {e}"

def find_item_in_excel(filepath, item, item_col=None, value_col=None):
    """Find rows in an Excel file matching `item` and return the value(s)
    from the adjacent (or specified) column.

    - filepath: path to the Excel file
    - item: string to search for (case-insensitive)
    - item_col: column name or index to search in. If None, all columns are searched.
    - value_col: column name or index to return the value from. If None,
                 the column immediately to the right of the found item is used.

    Returns a list of matching values (may be empty) or an error string.
    """
    try:
        import pandas as pd
    except ImportError:
        return "Error: pandas library is not installed. Please install it to use Excel lookups."

    try:
        excel_file = pd.read_excel(filepath)
    except FileNotFoundError:
        return f"Error: The file at {filepath} was not found."
    except Exception as e:
        return f"An error occurred while reading Excel: {e}"

    search = str(item).strip().lower()
    results = []
    def _get_value(row_idx, col_idx):
        try:
            val = excel_file.iat[row_idx, col_idx]
            if pd.isna(val):
                return None
            return val
        except Exception:
            return None

    if item_col is not None:
        if isinstance(item_col, int):
            cols_to_search = [item_col]
        else:
            if item_col in excel_file.columns:
                cols_to_search = [excel_file.columns.get_loc(item_col)]
            else:
                return []
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
                    val = _get_value(row_idx, value_col)
                else:
                    if value_col in excel_file.columns:
                        val = _get_value(row_idx, excel_file.columns.get_loc(value_col))
                    else:
                        val = None
            else:
                val = _get_value(row_idx, col_idx + 1) if col_idx + 1 < len(excel_file.columns) else None
                
            val = int(val)
            results.append(val)

    return results

print(find_item_in_excel("prixEpicerie.xlsx", "apple"))

