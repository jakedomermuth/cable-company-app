import sqlite3

# SQL

CREATE_TABLES = """




"""

INSERT_CUSTOMERS = "INSERT INTO customers  "
#How do I intert Id's aswell?

REMOVE_CUSTOMERS = "DELETE FROM ? WHERE equipment = ?;"
# What column to delete from?

SELECT_CUSTOMERS_AND_LAST_PAYMENT = ""
# option to select by name or location

SELECT_LATE_CUSTOMERS = ""

UPDATE_PAYMENT = ""
# only the last payment

ADD_SERVICES = "INSERT INTO services (service_id, service, service_cost) VALUES (?, ?, ?)"
# how do I get the ID?

ADD_EQUIPMENT = "INSERT INTO equipment (equipment_id, equipment, equipment_cost) VALUES (?, ?, ?)"
# how do I get the ID?

REMOVE_SERVICES = "DELETE FROM services WHERE service = ?;"

REMOVE_EQUIPMENT = "DELETE FROM equipment WHERE equipment = ?;"

UPDATE_SERVICE_COST = "UPDATE service SET service_cost = ? WHERE service = ?"

UPDATE_EQUIPMENT_COST = "UPDATE equipment SET equipment_cost = ? WHERE equipment = ?"

UPDATE_BILL_AMOUNT = ""


 # <-----------------------------------------------------------------------------------------

connection = sqlite3.connect("cable.db")

