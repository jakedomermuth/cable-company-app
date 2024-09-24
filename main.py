from database import create_tables, add_customers, delete_customers, customer_exist


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


create_tables()


# PROMPT FUNCTIONS
def add_remove_customers_prompt():
    choice = input(ADD_OR_REMOVE_SELECTION )
    return choice


def get_customer_information():
    customer_name = input('What is the users name? ')
    customer_number = input('What is the users phone number (xxx-xxx-xxxx) ')
    customer_card_number = input('What is the users card number? ')
    customer_name = format_input(customer_name)
    return customer_name, customer_number, customer_card_number


def get_customer_to_delete():
    customer_name = input('What is the name of the customer would you like to remove? ')
    customer_name = format_input(customer_name)
    return customer_name


def confirm_del_user():
    delete_choice = input(f'Are you sure you want to delete {cust_name_to_delete}? (Y/N)')
    delete_choice = format_input(delete_choice)
    return delete_choice

# Utility Functions--------------------------------------------------------------------------------
def format_input(name):
    clean_name = name.strip().upper()
    return clean_name


# def adding_customer(customer_name, customer_number, customer_card_number):
#     #customer_name, customer_number, customer_card_number = get_customer_information()
#     if customer_exist(customer_name):
#         print("This user already exist")
#         return None
#     else:
#         add_customers(customer_name, customer_number, customer_card_number)
#         ### print(f'{name} has been added to the database. Their user ID is {id}.')

# Main
def main():
    (user_choice := input(INTERFACE_PROMPT)) != '6'
    while user_choice != '6':
        if user_choice == '1':
            pass
        elif user_choice == '2':
            add_or_remove = add_remove_customers_prompt()
            if add_or_remove == '1':
                customer_name, customer_number, customer_card_number = get_customer_information()
                if customer_exist(customer_name):
                     print("This user already exist")
                else:
                    add_customers(customer_name, customer_number, customer_card_number)
                    print(f'{customer_name} has been added to the database.')
            elif add_or_remove == '2':
                cust_name_to_delete = get_customer_to_delete()
                if customer_exist(cust_name_to_delete):
                    delete_choice = input(f'Are you sure you want to delete {cust_name_to_delete}? (Y/N)')
                    # looking to delete(need to get variable in confirm del function)
                    if delete_choice == 'Y':
                        delete_customers(cust_name_to_delete)
                        print(f'{cust_name_to_delete} has been removed.')
                    else:
                        print('User has not been deleted.')
                else:
                    print("User is not in the database.")
            else:
                break
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
