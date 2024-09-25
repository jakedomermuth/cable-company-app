from database import create_tables, add_customers, delete_customers, customer_exist, get_billing_by_name, get_billing_by_location


INTERFACE_PROMPT = """
Hello!
What would you like to do?
1. View Customer Information 
2. Add Or Remove Customers
3. Update Customer Services or Equipment
4. Update or Add Billing
5. Add, Remove, And Edit Services or Equipment
6. Exit
Please enter the number for your desired option:
"""

ADD_OR_REMOVE_SELECTION = """
What would you like to do?
1. Add a Customer
2. Remove a Customer
3. Exit
Please enter the number for your desired option:
"""

CUSTOMER_INFORMATION_SELECTION = """
What would you like to do?
1. View last billing cycle information by customer name?
2. View last billing cycle information by location?
3. View all late customers?
4. Exit
Please enter the number for your desired option:
"""

create_tables()


# PROMPT FUNCTIONS
def add_remove_customers_prompt():
    choice = input(ADD_OR_REMOVE_SELECTION )
    return choice

def customer_info_selection_prompt():
    choice = input(CUSTOMER_INFORMATION_SELECTION)
    return choice
def get_customer_information_prompt():
    customer_name = input('What is the users name? ')
    customer_number = input('What is the users phone number (xxx-xxx-xxxx) ')
    customer_card_number = input('What is the users card number? ')
    customer_name = format_input(customer_name)
    return customer_name, customer_number, customer_card_number

def get_name_prompt():
    name_input = input('What is the users name? ')
    name = format_input(name_input)
    return name

def get_location_prompt():
    location = input('What is the name of the location? ')
    loc = format_input(location)
    return loc
def get_customer_to_delete_prompt():
    customer_name = input('What is the name of the customer would you like to remove? ')
    customer_name = format_input(customer_name)
    return customer_name


def confirm_del_user_prompt(name):
    delete_choice = input(f'Are you sure you want to delete {name}? (Y/N)')
    delete_choice = format_input(delete_choice)
    return delete_choice

def add_and_remove_prompt():
    add_or_remove = add_remove_customers_prompt()
    if add_or_remove == '1':
        add_user()
    elif add_or_remove == '2':
        del_user()
    else:
        pass

# Utility Functions--------------------------------------------------------------------------------
def format_input(name):
    clean_name = name.strip().upper()
    return clean_name


def add_user():
    customer_name, customer_number, customer_card_number = get_customer_information_prompt()
    if customer_exist(customer_name):
        print("This user already exist")
    else:
        add_customers(customer_name, customer_number, customer_card_number)
        print(f'{customer_name} has been added to the database.')


def del_user():
    cust_name_to_delete = get_customer_to_delete_prompt()
    if customer_exist(cust_name_to_delete):
        if confirm_del_user_prompt(cust_name_to_delete) == 'Y':
            delete_customers(cust_name_to_delete)
            print(f'{cust_name_to_delete} has been removed.')
        else:
            print('User has not been deleted.')
    else:
        print("User is not in the database.")


def add_and_remove_prompt():
    add_or_remove = add_remove_customers_prompt()
    if add_or_remove == '1':
        add_user()
    elif add_or_remove == '2':
        del_user()
    else:
        pass


# Main------------------------------------------------------------------------------------------------------------------
def main():
    while (user_choice := input(INTERFACE_PROMPT)) != '6':
        if user_choice == '1':
            cust_info_selection = customer_info_selection_prompt()
            if cust_info_selection == '1':
                lookup_name = get_name_prompt()
                customer_info = get_billing_by_name(lookup_name)
                if customer_info:
                    for col in customer_info:
                        print(f'Billing ID: {col[0]} Billing Amount: {col[1]} Payment Due Date: {col[2]} Name: {col[4]}')
                else:
                    print(f"No information can be found for {lookup_name}")
            elif cust_info_selection == '2':
                location_name = get_location_prompt()
                location = get_billing_by_location(location_name)
                if location:
                    for col in location:
                        print(f'Billing ID: {col[0]} Billing Amount: {col[1]} Payment Due Date: {col[2]} Name: {col[3]}')
                else:
                    print(f"No information can be found for {location_name}")
        elif user_choice == '2':
            add_and_remove_prompt()
        elif user_choice == '3':
            pass
        elif user_choice == '4':
            pass
        elif user_choice == '5':
            pass
        else:
            print("Invalid Selection! Please choose a number 1-6")
    print("Application Closed. Thank You!")
main()
