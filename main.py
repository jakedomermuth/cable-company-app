from database import create_tables, add_customers, delete_customers


INTERFACE_PROMPT = """
Hello!
What would you like to do?
1. View Customer Information 
2. Add Or Remove Customers
3. Update Customer Services or Equipment
4. Update or Add Billing
5. Add, Remove, And Edit Services or Equipment
6. Exit
Please Enter the Number For Your Desired Option:
"""

ADD_OR_REMOVE_SELECTION = """
What would you like to do?
1. Add a Customer
2. Remove a Customer
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
    return customer_name, customer_number, customer_card_number


def get_customer_to_delete():
    customer_id = input('What is the id number of the customer would you like to remove?')
    return customer_id

# Utility Functions



# Main
def main():
    user_choice = input(INTERFACE_PROMPT)
    while user_choice != '6':
        if user_choice == '1':
            pass
        elif user_choice == '2':
            add_or_remove = add_remove_customers_prompt()
            if add_or_remove == '1':
                customer_name, customer_number, customer_card_number = get_customer_information()
                add_customers(customer_name, customer_number, customer_card_number)
                # print inication that the user was added
            elif add_or_remove == '2':
                cust_id_to_delete = get_customer_to_delete()
                #return user and ask if they still want to delete
                delete_customers(cust_id_to_delete)
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
