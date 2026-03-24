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
        with open("GroceryList_test.md", "r", encoding="utf-8") as f:
            for line in content2.splitlines():
                print(f"{item} in line: {line}")
                if item in line:
                    item,current_price,best_price = line.split(',')
                    del line
                    write_line = f"{item},{current_price},{min1}\n"
