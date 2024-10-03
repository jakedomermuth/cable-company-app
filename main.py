from database import (create_tables, add_customers, delete_customers, customer_exist, get_billing_by_name,
                      get_billing_by_location, get_all_late_customers, add_services, add_equipment, del_services,
                      del_equipment, update_equipment, update_services, equipment_exist, service_exist, add_location,
                      customer_exist_by_id, location_exist, update_location, add_billing, add_billing_services,
                      add_billing_equipment, service_id_exist, equipment_id_exist, lookup_unpaid_customer,
                      update_paid_status, billing_exist, update_customer_on_time)
import datetime

THIRTY_DAYS_IN_SECONDS = datetime.timedelta(days=30).total_seconds()
TODAYS_TIMESTAMP = datetime.datetime.today().timestamp()
TODAY_DATE = datetime.date.today()

INTERFACE_PROMPT = """
Hello!
What would you like to do?
1. View Customer Information 
2. Add Or Remove Customers
3. Add or Update Customer Addresses
4. Add Billing Cycle or Update Payment Satus
5. Add, Remove, or Update Services or Equipment
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
1. View last billing cycle information by customer name
2. View last billing cycle information by location
3. View all late customers
4. Exit
Please enter the number for your desired option:
"""

UPDATE_ADD_REMOVE_S_E = """
What would you like to do?
1. Add a service
2. Remove a service
3. Add equipment
4. Remove equipment
5. Update service information
6. Update equipment Information
7. Exit
Please enter the number for your desired option:
"""

ADD_OR_UPDATE_ADDY = """
What would you like to do?
1. Add an addresses
2. Update an addresses
3. Exit
Please enter the number for your desired option:
"""

ADD_OR_UPDATE_BILLING = """
What would you like to do?
1. Add a new billing cycle
2. Update billing status to paid
3. Exit
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


def add_or_update_billing_cycle_prompt():
    billing_choice = input(ADD_OR_UPDATE_BILLING)
    if billing_choice == '1':
        add_billing_cycle()
    elif billing_choice == '2':
        return_and_update_billing_cycle()


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


def add_or_update_prompt():
    update_or_add = add_or_update_addresses_prompt()
    if update_or_add == '1':
        add_location_func()
    elif update_or_add == '2':
        update_location_func()


# PROMPT FUNCTIONS------------------------------------------------------------------------------------------------------

def get_billing_info_prompt():
    amount = input('How much does the billing cost for this month? ')
    payment_date = input('What date is the payment due? (MM-DD-YYYY) ')
    customer_id = input('What is the customers ID number? ')
    return amount, payment_date, customer_id


def get_billing_services_prompt():
    # getting an id number and adding it to a list
    services = []
    while True:
        service = input("Enter each service ID: (type 'exit' to finish) ")
        if service.lower() == 'exit':
            break
        try:
            # error handling for non-number input
            service = int(service)
            if service_id_exist(service):  # checking if id exist to avoid foreign key error
                services.append(service)
            else:
                print('This id does not exist for a service')
        except ValueError:
            print("Invalid input. Please enter a valid service ID (an integer) or type 'exit' to finish.")
    return services


def get_billing_equipment_prompt():
    # getting an id number and adding it to a list
    equipment = []
    while True:
        equip = input("Enter each equipment ID: (type 'exit' to finish) ")
        if equip.lower() == 'exit':
            break
        try:
            # error handling for non-number input
            equip = int(equip)
            if equipment_id_exist(equip):  # checking if id exist to avoid foreign key error
                equipment.append(equip)
            else:
                print('This id does not exist for equipment')
        except ValueError:
            print("Invalid input. Please enter a valid equipment ID (an integer) or type 'exit' to finish.")
    return equipment


def user_adding_entity(entity):
    # argument is either service or equipment which allows for reduced amount of input functions
    user_choice = input(f'Does this billing cycle have any {entity} associated with it? (Y/N)')
    user_choice_formatted = format_input(user_choice)
    return user_choice_formatted


def add_remove_customers_prompt():
    # Menu Selection
    choice = input(ADD_OR_REMOVE_SELECTION)
    return choice


def update_add_or_del_prompt():
    # Menu Selection
    user_choice = input(UPDATE_ADD_REMOVE_S_E)
    return user_choice


def customer_info_selection_prompt():
    # Menu Selection
    choice = input(CUSTOMER_INFORMATION_SELECTION)
    return choice


def get_customer_information_prompt():
    customer_name = input('What is the users name? ')
    customer_number = input('What is the users phone number (xxx-xxx-xxxx) ')
    customer_card_number = input('What is the users card number? ')
    customer_name = format_input(customer_name) # standardizing input
    return customer_name, customer_number, customer_card_number


def get_name_prompt():
    name_input = input('What is the customers name? ')
    name = format_input(name_input) # standardizing input
    return name


def get_location_prompt():
    location = input('What is the name of the location? ')
    loc = format_input(location) # standardizing input
    return loc


def get_customer_to_delete_prompt():
    customer_name = input('What is the name of the customer would you like to remove? ')
    customer_name = format_input(customer_name) # standardizing input
    return customer_name


def confirm_del_user_prompt(name):
    delete_choice = input(f'Are you sure you want to delete {name}? (Y/N)')
    delete_choice = format_input(delete_choice) # standardizing input
    return delete_choice


def add_a_service_or_equipment_prompt(entity):
    # argument is either service or equipment which allows for reduced amount of input functions
    service_or_equipment = input(f'What is the name of the {entity} ? ')
    cost = input(f'How much does this {entity} cost? ')
    return service_or_equipment, cost


def del_a_service_or_equipment_prompt(entity):
    service_or_equipment = input(f'What is the name of the {entity} ? ')
    return service_or_equipment


def update_service_or_equipment_prompt(entity):
    # argument is either service or equipment which allows for reduced amount of input functions
    initial_name = input(f'What is the name of the {entity} you would like to update? ')
    name = input(f'What would you like the {entity} to be named? ')
    cost = input(f'How much does the {entity} cost? ')
    return initial_name, cost, name


def add_or_update_addresses_prompt():
    choice = input(ADD_OR_UPDATE_ADDY)
    return choice


def get_address_to_add_prompt():
    location_name = input('What is the name of the location? ')
    address = input('What is the address of the location? ')
    city = input('What is the city of the location? ')
    state = input('What is the state of the location? ')
    customer_id = input('What is the customer ID of the owner of the location? ')
    return location_name, address, city, state, customer_id


def get_address_to_update_prompt():
    lookup_location = input('What is the name of the location you would like to update? ')
    return lookup_location


def get_info_to_update_prompt():
    location_name = input('What is the new name of the location? ')
    address = input('What is the new address of the location? ')
    city = input('What is the new city of the location? ')
    state = input('What is the new state of the location? ')
    return location_name, address, city, state


def get_billing_by_id_prompt():
    while True:
        billing_id = input('What is the billing id for the bill the user would like to pay? (Type "quit" to exit) ')
        if billing_id.lower() == 'quit':
            break
        try:
            billing_id = int(billing_id)
            return billing_id
        except ValueError:
            print('The ID number must be an integer!')



# Utility Functions--------------------------------------------------------------------------------

def format_input(name):
    clean_name = name.strip().upper()  # removes whitespace and capitalizes text for standardization
    return clean_name


def add_user():
    customer_name, customer_number, customer_card_number = get_customer_information_prompt()
    if customer_exist(customer_name):
        # handing possible duplicate data
        print("This user already exist")
    else:
        add_customers(customer_name, customer_number, customer_card_number)  # adding new customer to database
        print(f'{customer_name} has been added to the database.')


def del_user():
    cust_name_to_delete = get_customer_to_delete_prompt()
    if customer_exist(cust_name_to_delete):  # handling error by checking if user exist
        if confirm_del_user_prompt(cust_name_to_delete) == 'Y':  # double check to avoid accidental deletions
            delete_customers(cust_name_to_delete)  # deletion customer from database
            print(f'{cust_name_to_delete} has been removed.')
        else:
            print('User has not been deleted.')
    else:
        print("User is not in the database.")


def lookup_by_name():
    lookup_name = get_name_prompt()
    customer_info = get_billing_by_name(lookup_name)
    if customer_info:  # handling bad input by checking if user exist
        for col in customer_info:  # printing out each row returned
            print(f'Billing ID: {col[0]} Billing Amount: {col[1]} Payment Due Date: {col[2]} User ID: {col[4]}')
    else:
        print(f"No information can be found for {lookup_name}")


def lookup_by_location():
    location_name = get_location_prompt()
    location = get_billing_by_location(location_name)
    if location:  # handling bad input by checking if location exist
        for col in location:  # printing out each row returned
            print(f'Billing ID: {col[0]} Billing Amount: {col[1]} Payment Due Date: {col[2]} Customer ID: {col[4]}')
    else:
        print(f"No information can be found for {location_name}")


# Needs to change !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def lookup_late_customers():
    late_customers = get_all_late_customers(TODAY_DATE)
    if late_customers:
        for col in late_customers:
            print(f'Customer ID: {col[0]}  | Customer Name: {col[1]}  | Billing ID: {col[4]} | Billing Amount: {col[5]} | '
                  f'Payment Due Date: {col[6]} \n')
    else:
        print("All Customers are up to date!")


def add_service_func():
    # adding a service
    service_add_name, service_cost = add_a_service_or_equipment_prompt('service')
    service_add_name = format_input(service_add_name)  # standardizing input
    if service_exist(service_add_name): # avoiding duplicates by checking if the service exist
        print("This service already exist")
    else:
        add_services(service_add_name, service_cost)  # adding service to database only if it does not already exist
        print(f'{service_add_name} has been added')


def remove_service():
    # removing a service
    service_remove_name = del_a_service_or_equipment_prompt('service')
    service_remove_name = format_input(service_remove_name) # standardizing input
    if service_exist(service_remove_name):
        del_services(service_remove_name)
        print(f'{service_remove_name} has been removed')  # removing service from database only if it already exists
    else:
        print("This service does not exist")


def add_equipment_func():
    # adding equipment
    equipment_name, equipment_cost = add_a_service_or_equipment_prompt('equipment')
    equipment_name = format_input(equipment_name)  # standardizing input
    if equipment_exist(equipment_name):
        print("This equipment already exist")
    else:
        add_equipment(equipment_name, equipment_cost) # adding equipment to database only if it does not already exist
        print(f'{equipment_name} has been added')


def remove_equipment():
    # removing Equipment
    del_equipment_name = del_a_service_or_equipment_prompt('equipment')
    del_equipment_name = format_input(del_equipment_name)  # standardizing input
    if equipment_exist(del_equipment_name):
        del_equipment(del_equipment_name)
        print(f'{del_equipment_name} has been removed')  # removing equipment from database only if it already exists
    else:
        print('This equipment does not exist')


def update_services_func():
    # update service
    initial_service_name, service_cost, service_name = update_service_or_equipment_prompt('service')
    initial_service_name = format_input(initial_service_name)
    service_name = format_input(service_name) # standardizing input
    if service_exist(initial_service_name):
        update_services(service_name, service_cost, initial_service_name)  # updating only if the service already exists
        print(f'{initial_service_name} has been updated')
    else:
        print(f'{initial_service_name} does not exist')


def update_equipment_func():
    # update equipment
    initial_equipment_name, equipment_cost, equipment_name = update_service_or_equipment_prompt('equipment')
    initial_equipment_name = format_input(initial_equipment_name)
    equipment_cost = format_input(equipment_cost) # standardizing input
    if equipment_exist(initial_equipment_name):
        update_equipment(equipment_name, equipment_cost, initial_equipment_name) # updating only if the equipment already exists
        print(f'{initial_equipment_name} has been updated')
    else:
        print(f'{initial_equipment_name} does not exist')


def add_location_func():
    add_location_name, add_address, add_city, add_state, add_customer_id = get_address_to_add_prompt()
    add_location_name = format_input(add_location_name)  # standardizing input
    if location_exist(add_location_name):  # check if location exists
        print('This location already exist')
    else:
        if customer_exist_by_id(add_customer_id): # check if customer exists to avoid foreign key constraints
            add_location(add_location_name, add_address, add_city, add_state, add_customer_id)
            print(f'{add_location_name} has been added')
        else:
            print('This customer does not exist')


def update_location_func():
    lookup_location = get_address_to_update_prompt()
    lookup_location = format_input(lookup_location) # standardizing input
    if location_exist(lookup_location):
        updated_location_name, updated_address, updated_city, updated_state = get_info_to_update_prompt()
        # getting updated info if the location exists
        updated_location_name = format_input(updated_location_name) # standardizing input
        update_location(updated_location_name, updated_address, updated_city, updated_state, lookup_location)
        # updating the location
        print(f'{lookup_location} has been updated')
    else:
        print('This location does not exist')
    # update an address


def time_conversion(database_date):
    date_object = datetime.datetime.strptime(database_date, "%m-%d-%Y")  # converts db time format to seconds
    payment_timestamp = date_object.timestamp()
    return payment_timestamp


def add_billing_cycle():
    billing_amount, payment_date, billing_cust_id = get_billing_info_prompt()
    billing_id = add_billing(billing_amount, payment_date, billing_cust_id)  # inserting new billing cycle
    print('Billing information has been added')
    add_services_to_billing(billing_id)
    add_equipment_to_billing(billing_id)


def add_services_to_billing(billing_id):
    add_services_choice = user_adding_entity('Services')
    if add_services_choice == 'Y':
        added_services = get_billing_services_prompt()  # returns a list of equipment
        for service in added_services:
            add_billing_services(billing_id, service)  # adding to composite table
        print('Services have been added')


def add_equipment_to_billing(billing_id):
    add_equipment_choice = user_adding_entity('Equipment')
    if add_equipment_choice == 'Y':
        added_equipment = get_billing_equipment_prompt()  # returns a list of equipment
        for equip in added_equipment:
            add_billing_equipment(billing_id, equip)  # adding to composite table
        print('Equipment has been added')


def update_billing_cycle():
    billing_update_id = get_billing_by_id_prompt()
    if billing_exist(billing_update_id):  # checking if the billing id exist
        updated_bill_date = update_paid_status(billing_update_id)  # updating to paid
        print(f'Billing cycle {billing_update_id} has been paid')
        updated_bill_date = time_conversion(updated_bill_date)  # converting date to seconds
        if updated_bill_date > TODAYS_TIMESTAMP:  # checking if payment was paid before the due date
            update_customer_on_time(billing_update_id)  # updating database to "On Time"
    else:
        print('This billing cycle does not exist')


def return_and_update_billing_cycle():
    customer_name = get_name_prompt()
    if customer_exist(customer_name):  # making sure customer exists
        billing_rows = lookup_unpaid_customer(customer_name)
        print(f'All unpaid billing cycles for {customer_name}:')
        for row in billing_rows:  # giving all billing cycles for provided name back to user
            print(f'Name: {row[1]:<10} | Billing Number: {row[4]:<5} | Billing Amount: {row[5]:<8} | Payment Date: {row[6]}')
        update_billing_cycle() # cals function that updates if customer exist
    else:
        print(f'{customer_name} does not exist in the database')

# Main------------------------------------------------------------------------------------------------------------------


def main():
    while (user_choice := input(INTERFACE_PROMPT)) != '6':
        if user_choice == '1':
            lookup_prompt()
        elif user_choice == '2':
            add_and_remove_prompt()
        elif user_choice == '3':
            add_or_update_prompt()
        elif user_choice == '4':
            add_or_update_billing_cycle_prompt()
        elif user_choice == '5':
            add_del_or_update_prompt()
        else:
            print("Invalid Selection! Please choose a number 1-6")
    print("Application Closed. Thank You!")
main()
