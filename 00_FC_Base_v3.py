# import libraries
from numpy import product
import pandas

# *** Functions go here ***

# checks that input is either a float or an iteger that is more than zero. Takes in custom error messages
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

# Checks that user has entered yes / no to a question
def yes_no(question):
    error="Please answer yes / no"
    valid=False
    while not valid:
        # Ask question and put response in lowercase
        response=input(question).lower()
        if response=="yes"or response=="y":
            return"yes"
        elif response=="no"or response=="n":
            return"no"
        else: 
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

        if var_fixed == "variable":
            quantity = num_check("Quantity: ", "The amount must be a whole number", int)

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
    expense_frame['Cost'] = expense_frame['Quantity'] * expense_frame['Price']

    # Find sub total
    sub_total = expense_frame['Cost'].sum()

    # Currency Formatting (uses currency function)
    add_dollars = ['Price', 'Cost']
    for item in add_dollars:
        expense_frame[item] = expense_frame[item].apply(currency)

    return[expense_frame, sub_total]

# Prints expense frames
def expense_print(heading, frame, subtotal):
    print()
    print("**** {} Costs ****".format(heading))
    print(frame)
    print()
    print("{} Costs: ${:.2f}".format(heading, subtotal))

# work out profit goal and total sales required
def profit_goal(total_costs):

    # Initialise variables and error message
    error = "Please enter a valid profit goal\n"

    valid = False
    while not valid:

        # ask for profit goal...
        response = input ("What is your profit goal (eg $500 or 50%) ")

        # check if first character is $...
        if response[0] == "$":
            profit_type = "$"
            # Get amount (everything after the $)
            amount = response[1:]

        # check if last character is %
        elif response [-1] == "%":
            profit_type = "%"
            # Get amount (everything before the %)
            amount = response[:-1]
        
        else:
            # set response to amount for now
            profit_type = "unknown"
            amount = response

        try:
            # Check amount is a number more than zero...
            amount = float(amount)
            if amount <= 0:
                print(error)
                continue
        
        except ValueError:
            print(error)

        if profit_type == "unknown" and amount >= 100:
            dollar_type = yes_no("Do you mean ${:.2f}. ie {:.2f} dollars?, y / n".format(amount, amount))

            # Set profit type based on user answer above
            if dollar_type == "yes":
                profit_type = "$"
            else:
                profit_type = "%"

        elif profit_type == "unknown" and amount < 100:
            percent_type = yes_no("Do you mean {}%?, y / n".format(amount))
            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type = "$"
        
        # return profit goal to main routine
        if profit_type == "$":
            return amount
        else:
            goal = (amount / 100) * total_costs
            return goal


# *** Main routine starts here ***

# Get product name
product_name = not_blank("Product name: ", "The product name cannot be blank")

print()
print("Please enter you variable costs below...")

# Get variable costs
variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]

print()
have_fixed = yes_no("Do you have fixed costs (y / n)? ")

if have_fixed == "yes":
    # Get fixed costs
    fixed_expenses = get_expenses("fixed")
    fixed_frame = fixed_expenses[0]
    fixed_sub = fixed_expenses[1]
else:
    fixed_sub = 0

# work out total cost from profit target
all_costs = variable_sub + fixed_sub
profit_target = profit_goal(all_costs)

# Calculate recommended price
selling_price = 0

# Write data to file

# *** Printing Area ***

print()
print("**** Fund Raising - {} ****".format(product_name))
print()
expense_print("Variable", variable_frame, variable_sub)

if have_fixed == "yes":
    expense_print("Fixed", fixed_frame[['Cost']], fixed_sub)

print()
print("**** Total Costs: ${:.2f} ****".format(all_costs))
print()

print()
print("**** Profit & Sales Target ****")
print("Profit Target: ${:.2f} ****")
print("Total Sales: ${:.2f}".format(all_costs, profit_target))

print()
print("**** Recommended Selling Price: ${:.2F}".format(selling_price))

#  (+)(+)                     
# /      \  
# \ -==- / 
#  \    / 
# <\/\/\/> 
# /      \
