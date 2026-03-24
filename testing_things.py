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
    output_lines = []
    for item in common_items:
        prices1 = data1[item]
        prices2 = data2[item]
        
        # Find best (lowest) price across both files
        best_price = min(min(prices1), min(prices2)) if prices1 and prices2 else None
        
        # Get current price (from file2, first price)
        current_price = prices2[0] if prices2 else 0
        
        # Write as: item, current_price, best_price
        output_lines.append(f"{item}, {current_price}, {best_price}\n")
    
    # Write to file
    with open("Grocery_List_Current_Price_test.md", "w", encoding="utf-8") as f:
        f.writelines(output_lines)