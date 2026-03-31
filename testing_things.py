
with open("Grocery_List_current_price_test.md", "r") as Grocery_list:
    with open("prixEpicerie.xlsx", "r") as Fichierexcel:
        content_grocery = Grocery_list.readlines()
        for line in content_grocery:
            item, price1 = line.split(',')
            print(f"Item: {item}, Price 1: {price1}")
            content_excel = Fichierexcel.readlines()
            for line in content_excel:
                item_excel, price_excel = line.split(',')
                if item == item_excel:
                    print(f"Item: {item}, Price Excel: {price_excel}")
                    break
                else:
                    Fichierexcel.write(f"{item},{price1}\n")
                