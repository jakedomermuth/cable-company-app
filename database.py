import sqlite3


# Creating Database ---------------------------------------------------------------------------------------------------
CREATE_CUSTOMER_TABLE = """
    CREATE TABLE IF NOT EXISTS customers
    (customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    customer_number TEXT,
    card_on_file TEXT); 
    """

CREATE_LOCATION_TABLE = """
    CREATE TABLE IF NOT EXISTS location
    (location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_name TEXT,
    location_address TEXT,
    customer_id INTEGER,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id));
    """

CREATE_BILLING_TABLE = """
    CREATE TABLE IF NOT EXISTS billing
    (billing_id INTEGER PRIMARY KEY AUTOINCREMENT,
    billing_amount REAL,
    payment_date TEXT,
    on_time_or_late TEXT,
    customer_id INTEGER,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id));    
    """
# NEED TO MAKE DECISION ON PAYMENT_DATE datatype

CREATE_EQUIPMENT_TABLE = """
    CREATE TABLE IF NOT EXISTS equipment
    (equipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_name TEXT,
    equipment_cost REAL);
    """

CREATE_SERVICES_TABLE = """
    CREATE TABLE IF NOT EXISTS services
    (service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT,
    service_cost REAL);
    """

CREATE_BILLING_EQUIPMENT_TABLE = """
    CREATE TABLE IF NOT EXISTS billing_equipment_composite
    (billing_id INTEGER,
    equipment_id INTEGER,
    FOREIGN KEY(billing_id) REFERENCES billing(billing_id),
    FOREIGN KEY(equipment_id) REFERENCES equipment(equipment_id))
    """

CREATE_BILLING_SERVICES_TABLE = """
    CREATE TABLE IF NOT EXISTS billing_services_composite
    (billing_id INTEGER,
    service_id INTEGER,
    FOREIGN KEY(billing_id) REFERENCES billing(billing_id),
    FOREIGN KEY(service_id) REFERENCES services(service_id))
    """


# Adding and Deleting customers ----------------------------------------------------------------------------------------
INSERT_CUSTOMERS = "INSERT INTO customers (customer_name, customer_number, card_on_file) VALUES (?, ?, ?) "

DELETE_CUSTOMERS = "DELETE FROM customers WHERE customer_id = ?;"


# Selecting Customer Information ---------------------------------------------------------------------------------------
SELECT_BILLING_BY_NAME = """SELECT b.* FROM billing b INNER JOIN customers c ON c.customer_id = b.customer_id WHERE b.payment_date =
    (SELECT MAX(payment_date) FROM billing b INNER JOIN customers c ON c.customer_id = b.customer_id WHERE b.customer_id = ?;)
"""
# maybe take out customer_id

SELECT_BILLING_BY_LOCATION = """SELECT b.* FROM customers c INNER JOIN location l ON c.customer_id = l.customer_id INNER JOIN billing b ON c.customer_id = b.customer_id WHERE b.payment_date = (
    SELECT MAX(b.payment_date) FROM customers c INNER JOIN location l ON c.customer_id = l.customer_id INNER JOIN billing b ON c.customer_id = b.customer_id WHERE l.location_name = ?)
"""
# maybe take out customer_id

SELECT_LATE_CUSTOMERS = "SELECT * FROM customers c INNER JOIN billing b ON c.customer_id = b.customer_id WHERE on_time_or_late = '1'"


# Updating Billing Information -----------------------------------------------------------------------------------------
ADDING_NEW_BILLING_MONTH = ""
# only the last payment

UPDATE_LAST_ON_TIME_OR_LATE = ""

UPDATE_BILL_AMOUNT = "UPDATE billing SET billing_amount = ? WHERE customer_id = ?"


# ADD and REMOVE SERVICES FOR CUSTOMER----------------------------------------------------------------------------------

ADD_CUSTOMER_SERVICE = "INSERT INTO billing_services_composite(billing_id, service_id) VALUES (?, ?)"

REMOVE_CUSTOMER_SERVICE = "DELETE FROM billing_services_composite WHERE billing_id = ? and service_id = ?"

ADD_CUSTOMER_EQUIPMENT = "INSERT INTO billing_equipment_composite(billing_id, equipment_id) VALUES (?, ?)"

REMOVE_CUSTOMER_EQUIPMENT = "DELETE FROM billing_equipment_composite WHERE billing_id = ? and equipment_id = ?"

# ADD, REMOVE, OR UPDATE SERVICES/EQUIPMENT-----------------------------------------------------------------------------
ADD_SERVICES = "INSERT INTO services (service, service_cost) VALUES (?, ?)"

ADD_EQUIPMENT = "INSERT INTO equipment (equipment, equipment_cost) VALUES (?, ?)"

REMOVE_SERVICES = "DELETE FROM services WHERE service = ?;"

REMOVE_EQUIPMENT = "DELETE FROM equipment WHERE equipment = ?;"

UPDATE_SERVICE_COST = "UPDATE service SET service_cost = ? WHERE service = ?"

UPDATE_EQUIPMENT_COST = "UPDATE equipment SET equipment_cost = ? WHERE equipment = ?"


# PYTHON <--------------------------------------------------------------------------------------------------------------

connection = sqlite3.connect("cable.db")
connection.execute('PRAGMA foreign_keys = ON')

def create_tables():
    with connection:
        connection.execute(CREATE_CUSTOMER_TABLE)
        connection.execute(CREATE_LOCATION_TABLE)
        connection.execute(CREATE_BILLING_TABLE)
        connection.execute(CREATE_EQUIPMENT_TABLE)
        connection.execute(CREATE_SERVICES_TABLE)
        connection.execute(CREATE_BILLING_EQUIPMENT_TABLE)
        connection.execute(CREATE_BILLING_SERVICES_TABLE)




def add_customers(name, number, card):
    with connection:
        connection.execute(INSERT_CUSTOMERS, (name, number, card))

def delete_customers(cust_id):
    with connection:
        connection.execute(DELETE_CUSTOMERS, (cust_id,))


