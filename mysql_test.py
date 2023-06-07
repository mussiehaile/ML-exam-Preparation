import pandas as pd
import pymysql

# Connect to the database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='12345678',
    database='database_name'
)

# Read data into a Pandas DataFrame
df = pd.read_sql('SELECT * FROM table_name', con=connection)

# Close the connection
connection.close()