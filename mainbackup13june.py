#SALEM AHMED ABDULLAH BA SUHAI
#TP073526
CODE = 0
DESCRIPTION = 1
CATEGORY = 2
UNIT = 3
PRICE = 4
QUANTITY = 5
MINIMUM = 6

UserData = []
with open("UserData.txt", "r") as file:
    for line in file:
        record = line.split(", ")
        record[2] = record[2][:-1]
        UserData.append(record)

#motherlist
inventoryBig = []
with open("inventory.txt", "r") as file:
    for line in file:
        record = line.split(", ")
        record[MINIMUM] = record[MINIMUM][:-1]
        inventoryBig.append(record)
#to transfer data from the motherlist(inventorybig), to the inventory.txt file.
def updateinventory():
    stringinventory = []
    for record in inventoryBig:
        recordstring = ""
        for data in record:
            recordstring += str(data)
            recordstring += ", "
        stringinventory.append(recordstring[:-2] + "\n" )
    with open("inventory.txt", "w") as file:
        file.writelines(stringinventory)
        file.close()

def itemdisplay(array):
    try:
        arr = [[array[j][i] for i in range(len(array[0]))] for j in range(len(array))] 
        #arr = array behaves as a pointer and so arr is edited and applies that data to array, 
        # thereby editing the original array, messing up the format and text. 
        # this line is a double for loop that copies the original array into arr, without impacting the original array.
        titles = ['Code','Description','Category','Unit','Price','Quantity','Minimum']
        arr.insert(0,titles)
        maximums = []
        #step 1
        for col in range(7):
            max = 0
            for row in arr:
                if len(row[col]) > max:
                    max = len(row[col])
            maximums.append(max)
        # print(maximums)
        # step 2
        for col in range(7):
            for row in arr:
                    if len(row[col]) < maximums[col]:
                        # print("found less")
                        remainder = maximums[col] - len(row[col])
                        # print(f"it needs {remainder} spaces")
                        for i in range(remainder):
                            row[col] += " "
        # step 3
        liner = "\n"
        for i in range(sum(maximums)+7):
            liner += "_"
        print(liner,end='')
        for record in arr:
            for cell in record:
                if arr.index(record) == 1 and record.index(cell) == 0:
                    print(liner)
                    print(f"{cell}",end="|")
                else:
                    if record.index(cell) == 0:
                        print(f"\n{cell}",end="|")
                    else:
                        print(cell,end="|")
        print("\n")
        del arr
    except:
        with open("inventory.txt", "r") as file:
            print(file.read())
#insert new item function
def insertitem():
    item_code = input("Enter item code: ")
    description = input("Enter item description: ")
    category = input("Enter item category: ")
    unit = input("Enter item unit: ")
    price = float(input("Enter item price: "))
    quantity = int(input("Enter item quantity: "))
    minimum = int(input("Enter item minimum threshold: "))
    itemdata = f"{item_code}, {description}, {category}, {unit}, {price}, {quantity}, {minimum}"
    with open("inventory.txt", "a") as file:
        file.write(itemdata + "\n")
        file.close()

#to remove items, pop to remove the list of item from motherlist
def removeitem():
    code = input("Enter the code of the item you wish to remove: ")
    index = 0
    found = False
    for record in inventoryBig:
        if record[CODE] == code:
            inventoryBig.pop(index)
            found = True
        index += 1
    if not found:
        print("This item does not exist.")
    else:
        updateinventory()
        print("item removed successfully.")

#accepts input only! edits items within the list, by matching through code, verifiying existence of item and then typing new details into field!
def edititem(code, field, newdetails):
    found = False
    for record in inventoryBig:
        if record[CODE] == code:
            found = True
            print("Found an item with a matching code!")
            record[field] = newdetails
    if not found:
        print("This item does not exist.")
    else:
        updateinventory()
        print("item updated successfully.")

#prompts for code of the item, verifies its existence then outputs the quantity of the item, prompts user for confirmation of quantity and the option to update it.
def stocktake(): #INVENTORYCHECKER
    code = input("Enter the code of the item: ")
    for record in inventoryBig:
         if record[CODE] == code:
            quantity = record[QUANTITY]
            print(f"Found an item with a matching code! The quantity for the item {record[DESCRIPTION]}, is {record[QUANTITY]}")
    while True:
        inp = input("Type c if you want to confirm, or u if you want to update the quantity.")
        if inp.lower() == "c":
            break
        elif inp.lower() == "u":
            newdetail = input("Please enter the new quantity of the item: ")
            edititem(code, QUANTITY, newdetail)
    
#Compares the values of minimum threshold and quantity within the array and if the quantity is equal to or less than minimum threshold the item will be displayed.
def replenishlist(): #PURCHASER
    print("The items that need to be replenished: ")
    result = []
    for record in inventoryBig:
        if int(record[QUANTITY]) < int(record[MINIMUM]):
            result.append(record)
    itemdisplay(result)

#prompts user for item code, after validation, if the item is found it will display the item's code and current quantity, 
# it then prompts the user for either new quantity data to be inserted or ending the process.
#DEVNOTE: I think it should add the newly purchased items with the current quantity to update it, not completely write a new number. READ NOW!!!!!!!!!!!!!!
def restock(): #PURCHASER
    replenishlist()
    code = input("Enter the code of the item you wish to restock: ")
    for record in inventoryBig:
        if record[CODE] == code:
            print(f"Found an item with a matching code!,the quantity for the item, {record[DESCRIPTION]}, is {record[QUANTITY]}")
            index = inventoryBig.index(record)

    while True:
        inp = input("Type replenish if you want to replenish the quantity of the item, or type exit to end this process: ")
        if inp.lower() == "exit":
            break
        elif inp.lower() == "replenish":
           value = int(input("Enter the amount of items you would like to restock: "))
           quantity = int(inventoryBig[index][QUANTITY]) + value
           inventoryBig[index][QUANTITY] = quantity
           updateinventory()
           print(f"The replenished quantity of {inventoryBig[index][DESCRIPTION]} is now {inventoryBig[index][QUANTITY]}")
           break
        else:
            print("Invalid input. Please type replenish if you want to restock the item, or exit if you want to end this process.")

#this search function searches in 4 ways, by description, code range, category, and price range. and then outputs an array of the found result, it also verifies the existence of the item. 
def search(searchtype): #INVENTORYCHECKER, PURCHASER
    results = []
    
    if searchtype == 1:
        tag = input("Please type the description of the item: ")
        for record in inventoryBig:
            if tag.lower() in record[DESCRIPTION].lower():
                results.append(record)

    elif searchtype == 2:
        codestart = input("The start of the code range: ")
        codeend = input("The end of the code range: ")
        for record in inventoryBig:
            code = record[CODE]
            if code >= codestart and code <= codeend:
                results.append(record)
        
    elif searchtype == 3:
        category = []
        for record in inventoryBig:
            if record[CATEGORY].lower() not in category:
                category.append(record[CATEGORY].lower())
        for choice in category:
            print(choice)
        while True:
            tag = input("Please choose a category from above. ")
            if tag.lower() in category:
                break
            else:
                print("Invalid category. Please try again.")
        for record in inventoryBig:
            if record[CATEGORY].lower() == tag:
                results.append(record)
#if you finished and still got stuff to add try adding autocorrect feature to category list.
    elif searchtype == 4:
        pricestart = float(input("The start of the price range: "))
        priceend = float(input("The end of the price range: "))
        for record in inventoryBig:
            price = float(record[PRICE])
            if price >= pricestart and price <= priceend:
                results.append(record)
    if len(results) == 0:
        print("Couldn't find any results.")
    else:
        itemdisplay(results)
#this function is for the main selection menu interface, you pick from the base functions, and it redirects to the previous functions or it exits the program.
def adduser():
    roles = ["admin", "inventory-checker", "purchaser"]
    User = input("Please enter the new user's username:")
    Password = input("Please enter the new user's password:")
    print("Roles: \nadmin \ninventory-checker \npurchaser")
    Role = input("Please choose and type the role of the new user: ")
    if Role not in roles:
        print("Invalid choice. Please try again.")
    else:
        print("User has been added successfully.")
    userinfo= f"{User}, {Password}, {Role}"
    with open("Userdata.txt", "a") as file:
        file.write(userinfo + "\n")


def menu(verify, role):
    running = True
    while verify == True: #to loop the menu screen without relogging in after every function
        if not running:
            break
        if role == "admin":
            print("""Choose a function within the system.
0. Add new user
1. Display inventory
2. Insert New Item
3. Update Item
4. Delete Item
5. Stock Taking
6. View Replenish List
7. Stock Replenishment
8. Search items
9. Exit system""")
        elif role == "inventory-checker":
            print("""Choose a function within the system.
1. Display inventory
2. Stock Taking
3. Search items
4. Exit system""")       
        elif role == "purchaser":
            print("""Choose a function within the system.
1. Display inventory
2. View Replenish List
3. Stock Replenishment
4. Search items 
5. Exit system""")
        else:
            print("Invalid role assigned.")
            break
        functchoice = int(input("Type a number to choose a function from above: "))
        if role == "admin" and functchoice == 0:
            adduser()
        elif functchoice == 1:
            itemdisplay(inventoryBig)
        elif role == "admin" and functchoice == 2:
            insertitem()
        elif role == "admin" and functchoice == 3:
            code = input("Enter the code of the item you wish to update: ")
            print("""Edit Options:
1. Edit code
2. Edit description
3. Edit category
4. Edit unit
5. Edit price
6. Edit quantity
7. Edit minimum""")
            inp = int(input("Type a number to choose the search method: ")) - 1
            after = input("please type the NEW details of the item: ")
            edititem(code, inp, after)
        elif role == "admin" and functchoice == 4:
            removeitem()
        elif role == "admin" and functchoice == 5 or role == "inventory-checker" and functchoice == 2:
            stocktake()
        elif role == "admin" and functchoice == 6 or role == "purchaser" and functchoice == 2:
            replenishlist()
        elif role == "admin" and functchoice == 7 or role == "purchaser" and functchoice == 3:
            restock()

        elif role == "admin" and functchoice == 8 or role == "inventory-checker" and functchoice == 3 or role == "purchaser" and functchoice == 4:
            print("""Search Options: 
1. Search by description
2. Search by code range
3. Search by category
4. Search by price range """)
                    #change the print that includes multiple lines into triple quotes
            inp = int(input("Type a number to choose the search method: "))
            if inp >= 1 and inp <= 4:
                search(inp)    
            else:
                print("Invalid number. Pick a number from 1-4")
        elif role == "admin" and functchoice == 9 or role == "inventory-checker" and functchoice == 4 or role == "purchaser" and functchoice == 5:  
            running = False
            print("Thank you for using this program. Goodbye.♥")
            break
        elif functchoice > 9:
            print("Invalid input. Please type an existing number from the list above.")

           # print("Invalid number chosen, please type an existing number from the list above.")
def login():
    print("Welcome to the inventory system.")
    found = True
    verify = False
    while True:
        if not found:  #to loop until login authenticates.
            print("Invalid username or password, try again.")
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        for record in UserData:
            if record[0] == username and record[1] == password:
                print(f"User has been verified. User's type is {record[2]}.")
                role = record[2]
                verify = True
                menu(verify, role)
            else:
                found = False
        if verify == True: # to break loop after exit and login authentication.
            break
        
    



login()
