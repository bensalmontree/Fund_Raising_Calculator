import pandas

def num_check(question, error, num_type):
    
    valid=False
    while not valid:
        # Ask user for number and check it is valid
        try:
            response=num_type(input(question))
            if response<=0:
                print(error)
            else:
                return response
        except ValueError:
            print(error)

def not_blank(question, error):

    valid = False
    while not valid:
        response = input(question)

        if response == "":
            print("{}. \nPlease try again.\n".format(error))

        return response

# currency formatting function
def currency(x):
    return "${:.2f}".format(x)

# Get expenses, reutnr list which has the dataframe and subtotal
def get_expenses(var_fixed):
    # Set up dictionaries and lists

    item_list = []
    quantity_list = []
    price_list = []

    variable_dict = {
        "Item": item_list,
        "Quantity": quantity_list,
        "Price": price_list
    }

    # loop to get component, quantity and price
    item_name = ""
    while item_name.lower() != "xxx":
        
        print()
        # get name, quantity and item
        item_name = not_blank("Item name: ", "The component name...")
        if item_name.lower() == "xxx":
            break

        if item_name.lower() == "xxx":
            break

        else:
            quantity = 1
        
        price = num_check("How much for a single item? $", "The price must be a number <more than 0>", float)
 
        # add item, quantity and price to lists
        item_list.append(item_name)
        quantity_list.append(quantity)
        price_list.append(price)

    expense_frame = pandas.DataFrame(variable_dict)
    expense_frame = expense_frame.set_index('Item')

    # Calculate cost of each component
    expense_frame['Cost'] = expense_frame['Quantity'] * expense_frame

    # Find sub total
    sub_total = expense_frame['Cost'].sum()

    # Currency Formatting (uses currency function)
    add_dollars = ['Price', 'Cost']
    for item in add_dollars:
        expense_frame[item] = expense_frame[item].apply(currency)

    return[expense_frame, sub_total]

# *** Main routine starts here ***

# Get product name
fixed_expenses = get_expenses("fixed")
fixed_frame = fixed_expenses[0]
fixed_sub = fixed_expenses[1]

# *** Printing Area ***

print()
print(fixed_frame[['Cost']])
print()

print("Fixed Costs: ${:.2f}".format(fixed_sub))

#  (+)(+)                     
# /      \  
# \ -==- / 
#  \    / 
# <\/\/\/> 
# /      \
