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
    location_city TEXT, 
    location_state TEXT,
    customer_id INTEGER,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id));
    """

CREATE_BILLING_TABLE = """
    CREATE TABLE IF NOT EXISTS billing
    (billing_id INTEGER PRIMARY KEY AUTOINCREMENT,
    billing_amount REAL,
    payment_date BIGINT,
    on_time_or_late TEXT,
    customer_id INTEGER,
    customer_payed TEXT,
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

DELETE_CUSTOMERS = "DELETE FROM customers WHERE customer_name = ?;"


# Selecting Customer Information ---------------------------------------------------------------------------------------
SELECT_BILLING_BY_NAME = """SELECT b.* FROM billing b INNER JOIN customers c ON c.customer_id = b.customer_id WHERE c.customer_name = ?
AND b.payment_date =(SELECT MAX(payment_date) FROM billing b INNER JOIN customers c ON c.customer_id = b.customer_id
WHERE c.customer_name = ?);
"""


SELECT_BILLING_BY_LOCATION = """SELECT b.* FROM customers c INNER JOIN location l ON c.customer_id = l.customer_id 
INNER JOIN billing b ON c.customer_id = b.customer_id WHERE l.location_name = ? AND b.payment_date = (
    SELECT MAX(b.payment_date) FROM customers c INNER JOIN location l ON c.customer_id = l.customer_id INNER JOIN billing b 
    ON c.customer_id = b.customer_id WHERE l.location_name = ?)
"""


SELECT_LATE_CUSTOMERS = """SELECT * FROM customers c INNER JOIN billing b ON c.customer_id = b.customer_id 
WHERE on_time_or_late = '1' 
AND STRFTIME('%Y-%m-%d', SUBSTR(payment_date, 7, 4) || '-' || SUBSTR(payment_date, 1, 2) || '-' || SUBSTR(payment_date, 4, 2)) < ?;""" # formatting in SQL for speed optimization


# Inserting and Updating Addresses
INSERT_LOCATION = """INSERT INTO location (location_name, location_address, location_city, location_state, customer_id)
                    VALUES( ?, ?, ?, ?, ?)"""

UPDATE_LOCATION = """UPDATE location
                    SET location_name = ?, location_address = ?, location_city = ?, location_state = ?
                    WHERE location_name = ?"""


# Updating Billing Information -----------------------------------------------------------------------------------------
ADDING_NEW_BILLING_MONTH = """INSERT INTO billing(billing_amount, payment_date, on_time_or_late, customer_id, customer_payed)
                            VALUES (?, ?, '1', ?, 'FALSE' ) RETURNING billing_id"""


INSERT_BILLING_EQUIPMENT = """INSERT INTO billing_equipment_composite(billing_id, equipment_id)
                            VALUES( ?, ?)"""

INSERT_BILLING_SERVICES = """INSERT INTO billing_services_composite(billing_id, service_id)
                            VALUES( ?, ?)"""

UPDATE_CUSTOMER_PAYED = "UPDATE billing SET customer_payed = 'TRUE' WHERE billing_id = ? RETURNING payment_date"

UPDATE_CUSTOMER_ON_TIME = """UPDATE billing SET on_time_or_late = 0 WHERE billing_id = ?"""


# ADD and REMOVE SERVICES FOR CUSTOMER----------------------------------------------------------------------------------

ADD_CUSTOMER_SERVICE = "INSERT INTO billing_services_composite(billing_id, service_id) VALUES (?, ?)"

REMOVE_CUSTOMER_SERVICE = "DELETE FROM billing_services_composite WHERE billing_id = ? and service_id = ?"

ADD_CUSTOMER_EQUIPMENT = "INSERT INTO billing_equipment_composite(billing_id, equipment_id) VALUES (?, ?)"

REMOVE_CUSTOMER_EQUIPMENT = "DELETE FROM billing_equipment_composite WHERE billing_id = ? and equipment_id = ?"

# ADD, REMOVE, OR UPDATE SERVICES/EQUIPMENT-----------------------------------------------------------------------------
ADD_SERVICES = "INSERT INTO services (service_name, service_cost) VALUES (?, ?)"

ADD_EQUIPMENT = "INSERT INTO equipment (equipment_name, equipment_cost) VALUES (?, ?)"

REMOVE_SERVICES = "DELETE FROM services WHERE service_name = ?;"

REMOVE_EQUIPMENT = "DELETE FROM equipment WHERE equipment_name = ?;"

UPDATE_SERVICES = "UPDATE services SET service_cost = ?, service_name = ? WHERE service_name = ?"

UPDATE_EQUIPMENT = "UPDATE equipment SET equipment_cost = ?, equipment_name = ? WHERE equipment_name = ?"

# SUPPORTING SQL--------------------------------------------------------------------------------------------------------
SELECT_CUSTOMER = """SELECT * FROM customers WHERE customer_name = ?"""

SELECT_CUSTOMER_WITH_ID = """SELECT * FROM customers WHERE customer_id = ?"""

SELECT_LOCATION = """SELECT * FROM location WHERE location_name = ?"""

SELECT_SERVICE = """SELECT * FROM services WHERE service_name = ?"""

SELECT_EQUIPMENT = """SELECT * FROM equipment WHERE equipment_name = ?"""

SELECT_SERVICE_WITH_ID = """SELECT * FROM services WHERE service_id = ?"""

SELECT_EQUIPMENT_WITH_ID = """SELECT * FROM equipment WHERE equipment_id = ?"""

SELECT_UNPAID_CUSTOMER = """SELECT * FROM customers c
INNER JOIN billing b on c.customer_id = b.customer_id
WHERE customer_name = ?  and customer_payed = 'FALSE';
"""
SELECT_BILLING_BY_ID = """SELECT * FROM billing where billing_id = ?"""

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


def delete_customers(cust_name):
    with connection:
        connection.execute(DELETE_CUSTOMERS, (cust_name,))


def customer_exist(name):
    cursor = connection.cursor()
    cursor.execute(SELECT_CUSTOMER, (name,))
    return cursor.fetchall()


def service_id_exist(service_id):
    cursor = connection.cursor()
    cursor.execute(SELECT_SERVICE_WITH_ID, (service_id,))
    return cursor.fetchall()


def equipment_id_exist(equipment_id):
    cursor = connection.cursor()
    cursor.execute(SELECT_EQUIPMENT_WITH_ID, (equipment_id,))
    return cursor.fetchall()


def customer_exist_by_id(user_id):
    cursor = connection.cursor()
    cursor.execute(SELECT_CUSTOMER_WITH_ID, (user_id,))
    return cursor.fetchall()


def billing_exist(billing_id):
    cursor = connection.cursor()
    cursor.execute(SELECT_BILLING_BY_ID, (billing_id,))
    return cursor.fetchall()


def location_exist(location):
    cursor = connection.cursor()
    cursor.execute(SELECT_LOCATION, (location,))
    return cursor.fetchall()


def service_exist(name):
    cursor = connection.cursor()
    cursor.execute(SELECT_SERVICE, (name,))
    return cursor.fetchall()


def equipment_exist(name):
    cursor = connection.cursor()
    cursor.execute(SELECT_EQUIPMENT, (name,))
    return cursor.fetchall()


def get_billing_by_name(name):
    cursor = connection.cursor()
    cursor.execute(SELECT_BILLING_BY_NAME, (name, name))
    return cursor.fetchall()


def get_billing_by_location(location):
    cursor = connection.cursor()
    cursor.execute(SELECT_BILLING_BY_LOCATION, (location, location))
    return cursor.fetchall()


def get_all_late_customers(date):
    cursor = connection.cursor()
    cursor.execute(SELECT_LATE_CUSTOMERS, (date, ))
    return cursor.fetchall()


def add_equipment(equipment, cost):
    with connection:
        connection.execute(ADD_EQUIPMENT, (equipment, cost))


def add_services(service, cost):
    with connection:
        connection.execute(ADD_SERVICES, (service, cost))


def del_equipment(equipment):
    with connection:
        connection.execute(REMOVE_EQUIPMENT, (equipment,))


def del_services(service):
    with connection:
        connection.execute(REMOVE_SERVICES, (service, ))


def update_services(updated_name, cost, initial_name):
    with connection:
        connection.execute(UPDATE_SERVICES, (cost, updated_name, initial_name))


def update_equipment(updated_name, cost, initial_name):
    with connection:
        connection.execute(UPDATE_EQUIPMENT, (cost, updated_name, initial_name))


def add_location(location_name, location_address, location_city, location_state, customer_id):
    with connection:
        connection.execute(INSERT_LOCATION, (location_name, location_address, location_city, location_state, customer_id))


def update_location(updated_location_name, updated_address, updated_city, updated_state, lookup_location):
    with connection:
        connection.execute(UPDATE_LOCATION, (updated_location_name, updated_address, updated_city, updated_state, lookup_location))


def add_billing(billing_amount, payment_date, billing_cust_id):
    with connection:
        cursor = connection.cursor()
        cursor.execute(ADDING_NEW_BILLING_MONTH, (billing_amount, payment_date, billing_cust_id)) # returns id after inserting
        index_id = cursor.fetchone()[0]  # catching the id that was returned from the ADDING_NEW_BILLING_MONTH statement
    return index_id


def add_billing_services(billing_id, service_id):
    with connection:
        connection.execute(INSERT_BILLING_SERVICES, (billing_id, service_id))


def add_billing_equipment(billing_id, equipment_id):
    with connection:
        connection.execute(INSERT_BILLING_EQUIPMENT, (billing_id, equipment_id))


def update_paid_status(billing_id):
    with connection:
        cursor = connection.cursor()
        cursor.execute(UPDATE_CUSTOMER_PAYED, (billing_id, ))
        payment_date = cursor.fetchone()[0]  # catching the date that was returned from the ADDING_NEW_BILLING_MONTH statement
        return payment_date


def lookup_unpaid_customer(name):
    cursor = connection.cursor()
    cursor.execute(SELECT_UNPAID_CUSTOMER, (name,))
    return cursor.fetchall()


def update_customer_on_time(billing_id):
    with connection:
        connection.execute(UPDATE_CUSTOMER_ON_TIME, (billing_id, ))
