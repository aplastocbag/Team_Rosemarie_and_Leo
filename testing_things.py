# small place to test things

def New_Best_Price(filepath):
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
        return content
    except FileNotFoundError:
        return f"Error: The file at {filepath} was not found."
    except Exception as e:
        return f"An error occurred: {e}"

# changer le nom du file plus facilement

Grocery_List_Price = New_Best_Price("Grocery_List_Price_test.md")

# Example usage: ignore the title (first heading) when reading the file
file_content = Grocery_List_Price
print(file_content)
text = file_content
words = text.replace(","," ")
print(words)

