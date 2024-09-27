from database import (create_tables, add_customers, delete_customers, customer_exist, get_billing_by_name,
                      get_billing_by_location, get_all_late_customers, add_services, add_equipment, del_services,
                      del_equipment, update_equipment, update_services, equipment_exist, service_exist
                      )


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

UPDATE_ADD_REMOVE_S_E = """
What would you like to do?
1. Add a service?
2. Remove a service?
3. Add equipment?
4. Remove equipment?
5. Update service information?
6. Update equipment Information?
7. Exit?
Please enter the number for your desired option:
"""

create_tables()
# Nested Menus----------------------------------------------------------------------------------------------------------
def add_and_remove_prompt():
    add_or_remove = add_remove_customers_prompt()
    if add_or_remove == '1':
        add_user()
    elif add_or_remove == '2':
        del_user()
    else:
        pass


def lookup_prompt():
    cust_info_selection = customer_info_selection_prompt()
    if cust_info_selection == '1':
        lookup_by_name()
    elif cust_info_selection == '2':
        lookup_by_location()
    elif cust_info_selection == '3':
        lookup_late_customers()


def add_del_or_update_prompt():
    update_add_or_del = update_add_or_del_prompt()
    if update_add_or_del == '1':
        add_service_func()
    elif update_add_or_del == '2':
        remove_service()
    elif update_add_or_del == '3':
        add_equipment_func()
    elif update_add_or_del == '4':
        remove_equipment()
    elif update_add_or_del == '5':
        update_services_func()
    elif update_add_or_del == '6':
        update_equipment_func()


# PROMPT FUNCTIONS------------------------------------------------------------------------------------------------------
def add_remove_customers_prompt():
    choice = input(ADD_OR_REMOVE_SELECTION )
    return choice

def update_add_or_del_prompt():
    user_choice= input(UPDATE_ADD_REMOVE_S_E)
    return user_choice


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


def add_a_service_or_equipment_prompt(entity):
    service_or_equipment = input(f'What is the name of the {entity} ? ')
    cost = input(f'How much does this {entity} cost? ')
    return service_or_equipment, cost


def del_a_service_or_equipment_prompt(entity):
    service_or_equipment = input(f'What is the name of the {entity} ? ')
    return service_or_equipment


def update_service_or_equipment_prompt(entity):
    initial_name = input(f'What is the name of the {entity} you would like to update? ')
    name = input(f'What would you like the {entity} to be named? ')
    cost = input(f'How much does the {entity} cost? ')
    return initial_name, cost, name

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

def lookup_by_name():
        lookup_name = get_name_prompt()
        customer_info = get_billing_by_name(lookup_name)
        if customer_info:
            for col in customer_info:
                print(f'Billing ID: {col[0]} Billing Amount: {col[1]} Payment Due Date: {col[2]} User ID: {col[4]}')
        else:
            print(f"No information can be found for {lookup_name}")


def lookup_by_location():
    location_name = get_location_prompt()
    location = get_billing_by_location(location_name)
    if location:
        for col in location:
            print(f'Billing ID: {col[0]} Billing Amount: {col[1]} Payment Due Date: {col[2]} Name: {col[4]}')
    else:
        print(f"No information can be found for {location_name}")


def lookup_late_customers():
    late_customers = get_all_late_customers()
    if late_customers:
        for col in late_customers:
            print(f'Customer ID: {col[0]} Customer Name: {col[1]} Billing ID: {col[4]} Billing Amount: {col[5]} '
                  f'Payment Due Date: {col[6]} User ID: {col[8]}')
    else:
        print("All Customers are up to date!")
# 5--------------------------------------------------------------------------------------------------------------------


def add_service_func():
    # adding a service
    service_add_name, service_cost = add_a_service_or_equipment_prompt('service')
    service_add_name = format_input(service_add_name)
    if service_exist(service_add_name):
        print("This service already exist")
    else:
        add_services(service_add_name, service_cost)
        print(f'{service_add_name} has been added')


def remove_service():
    # removing a service
    service_remove_name = del_a_service_or_equipment_prompt('service')
    service_remove_name = format_input(service_remove_name)
    if service_exist(service_remove_name):
        del_services(service_remove_name)
        print(f'{service_remove_name} has been removed')
    else:
        print("This service does not exist")


def add_equipment_func():
    # adding equipment
    equipment_name, equipment_cost = add_a_service_or_equipment_prompt('equipment')
    equipment_name = format_input(equipment_name)
    if equipment_exist(equipment_name):
        print("This equipment already exist")
    else:
        add_equipment(equipment_name, equipment_cost)
        print(f'{equipment_name} has been added')


def remove_equipment():
    # removing Equipment
    del_equipment_name = del_a_service_or_equipment_prompt('equipment')
    del_equipment_name = format_input(del_equipment_name)
    if equipment_exist(del_equipment_name):
        del_equipment(del_equipment_name)
        print(f'{del_equipment_name} has been removed')
    else:
        print('This equipment does not exist')


def update_services_func():
    # update service
    initial_service_name, service_cost, service_name = update_service_or_equipment_prompt('service')
    initial_service_name = format_input(initial_service_name)
    service_name = format_input(service_name)
    if service_exist(initial_service_name):
        update_services(service_name, service_cost, initial_service_name)
        print(f'{initial_service_name} has been updated')
    else:
        print(f'{initial_service_name} does not exist')


def update_equipment_func():
    # update equipment
    initial_equipment_name, equipment_cost, equipment_name = update_service_or_equipment_prompt('equipment')
    initial_equipment_name = format_input(initial_equipment_name)
    equipment_cost = format_input(equipment_cost)
    if equipment_exist(initial_equipment_name):
        update_equipment(equipment_name, equipment_cost, initial_equipment_name)
        print(f'{initial_equipment_name} has been updated')
    else:
        print(f'{initial_equipment_name} does not exist')

# Main------------------------------------------------------------------------------------------------------------------


def main():
    while (user_choice := input(INTERFACE_PROMPT)) != '6':
        if user_choice == '1':
            lookup_prompt()
        elif user_choice == '2':
            add_and_remove_prompt()
        elif user_choice == '3':
            pass
        elif user_choice == '4':
            pass
        elif user_choice == '5':
            add_del_or_update_prompt()
        else:
            print("Invalid Selection! Please choose a number 1-6")
    print("Application Closed. Thank You!")
main()
