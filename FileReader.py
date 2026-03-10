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
        return content
    except FileNotFoundError:
        return f"Error: The file at {filepath} was not found."
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage: ignore the title (first heading) when reading the file
file_content = read_md_file("../GroceryList.md")
print(file_content)
