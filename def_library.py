def compare_prices():
    # Read both files
    with open("GroceryList_test_all_prices.md", "r") as file1:
        content1 = file1.read()
    with open("Grocery_List_Current_Price_test.md", "r") as file2:
        content2 = file2.read()
    
    # Parse first file (items with multiple prices)
    data1 = {}
    for line in content1.splitlines():
        if line.strip():
            parts = line.split(',')
            item = parts[0].strip()
            prices = [part.strip() for part in parts[1:] if part.strip()]
            if prices:  # Only add if there are prices
                data1[item] = [float(p) for p in prices]  # Convert to float
    
    # Parse second file (items with single price)
    data2 = {}
    for line in content2.splitlines():
        if line.strip():
            parts = line.split(',')
            item = parts[0].strip()
            prices = [part.strip() for part in parts[1:] if part.strip()]
            if prices:
                data2[item] = [float(p) for p in prices]
    
    # Find items that are in both files
    common_items = set(data1.keys()) & set(data2.keys())
    
    # Compare prices for common items
    for item in common_items:
        prices1 = data1[item]
        prices2 = data2[item]
        print(f"Item: {item}")
        print(f"  Prices from file 1: {prices1}")
        print(f"  Prices from file 2: {prices2}")
        
        # Example comparison: Find the lowest in each and compare
        min1 = min(prices1) if prices1 else None
        min2 = min(prices2) if prices2 else None
        if min1 is not None and min2 is not None:
            if min1 < min2:
                print(f"  Cheaper in file 1: {min1} vs {min2}")
            elif min2 < min1:
                print(f"  Cheaper in file 2: {min2} vs {min1}")
            else:
                print(f"  Same price: {min1}")
        print()  # Blank line for readability


def too_much_prices():
    with open("GroceryList_test_all_prices.md", "r") as file:
        content = file.read()
    
    for line in content.splitlines():
        if line.strip():
            parts = line.split(',')
            item = parts[1].strip()
            prices = [part.strip() for part in parts[1:] if part.strip()]
            if len(prices) > 30:  # Arbitrary threshold for "too many" prices
                print(f"Item '{item}' has too many prices: {prices}")

def first_price_removal():
    with open("GroceryList_test_all_prices.md", "r") as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        parts = [x.strip() for x in line.split(',')]
        if len(parts) > 1:
            # remove first price by dropping index 1
            new_line = parts[0] + ("," + ",".join(parts[2:]) if len(parts) > 2 else "")
            new_lines.append(new_line + "\n")
            print(f"Removed first price for item: {parts[0]}")
        else:
            new_lines.append(line)

    with open("GroceryList_test_all_prices.md", "w") as file:
        file.writelines(new_lines)

# Call the function
compare_prices()
too_much_prices()
first_price_removal()