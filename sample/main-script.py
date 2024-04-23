import mysql.connector as mysql

bioinf = mysql.connect(host="localhost", user="root", passwd="test123", db="bioinf")
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


