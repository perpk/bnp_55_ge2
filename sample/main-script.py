import mysql.connector as mysql
from user_action import UserAction

bioinf = mysql.connect(host="localhost", user="root", passwd="test123", db="bioinf")
bioinf.autocommit = True
bioinfcur = bioinf.cursor()

# A. Create a table for hosting sequences

bioinfcur.execute("CREATE DATABASE IF NOT EXISTS BIOINF")
bioinfcur.execute("USE BIOINF")

sql_create_table_bioseq = """
CREATE TABLE IF NOT EXISTS BIOSEQ (
    ID BIGINT NOT NULL auto_increment,
    SEQ_TYPE VARCHAR(3) NOT NULL,
    SEQ LONGTEXT NOT NULL,
    CREATOR VARCHAR(512),
    CONSTRAINT CHK_SEQ_TYPE CHECK (SEQ_TYPE IN ('DNA', 'RNA')),
    PRIMARY KEY (ID)
)
"""
bioinfcur.execute(sql_create_table_bioseq)

command = ""

# Γ. Command Line Application to Create, Delete or Print an entry.
while "exit" != command.lower() or command == '4':
    print("""
    What action would you like to execute?
    
    1........Create new entry
    2........Delete existing entry
    3........Print an existing entry
    4........Exit
    """)

    command = input("Please enter the action... ")
    if command.lower() == "exit" or command == '4':
        print("Terminating...")
        break

    userAction = UserAction(bioinfcur)

    try:
        userAction.execute_action(command)
    except ValueError as ve:
        print(ve)
        continue

