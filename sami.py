import os
import pandas as pd
import psycopg2 
# from mysql.connector import Error

def DBConnect(dbName=None):
    """
    Parameters
    ----------
    dbName :
        Default value = None)
    Returns
    -------
    """
    conn = psycopg2.connect(host='localhost', user='postgres', password='postgres', port=5433,
                         database=dbName)
    print("Connected Suceesfully")

    conn.autocommit = True
    cur = conn.cursor()
    return conn, cur

def emojiDB(dbName: str) -> None:
    conn, cur = DBConnect(dbName)
    dbQuery = f"ALTER DATABASE {dbName} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;"
    cur.execute(dbQuery)
    conn.commit()
    
    

def createDB(dbName: str) -> None:
    """
    Parameters
    ----------
    dbName :
        str:
    dbName :
        str:
    dbName:str :
    Returns
    -------
    """
    conn, cur = DBConnect()
    # cur.execute(f"CREATE DATABASE IF NOT EXISTS {dbName};")
    cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dbName}';")
    exists = cur.fetchone()

    # Create the database if it doesn't exist
    if not exists:
        cur.execute("CREATE DATABASE telecom;")
    conn.commit()
    cur.close()


def createTables(dbName: str, sql_file: str) -> None:
    """
    Parameters
    ----------
    dbName :
        str:
    dbName :
        str:
    dbName:str :
    Returns
    -------
    """
    conn, cur = DBConnect(dbName)
    sqlFile = sql_file #'day5_schema.sql'
    fd = open(sqlFile, 'r')
    readSqlFile = fd.read()
    fd.close()

    sqlCommands = readSqlFile.split(';')

    for command in sqlCommands:
        try:
            res = cur.execute(command)
        except Exception as ex:
            print("Command skipped: ", command)
            print(ex)
    conn.commit()
    cur.close()

    return

def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parameters
    ----------
    df :
        pd.DataFrame:
    df :
        pd.DataFrame:
    df:pd.DataFrame :
    Returns
    -------
    """
    columns = df.columns.to_list()
    # cols_2_drop = ['Unnamed: 0', 'timestamp', 'sentiment', 'possibly_sensitive', 'original_text']
    try:
        # df = df.drop(columns=cols_2_drop, axis=1)
        df = df.fillna(-1).itertuples()
        # df['favorite_count'] = df['favorite_count'].fillna("---")
        # df['lang'] = df['lang'].fillna("---")
    except KeyError as e:
        print("Error:", e)

    return df


# def insert_to_data_table(dbName: str, df: pd.DataFrame, table_name: str) -> None:
#     """
#     Parameters
#     ----------
#     dbName :
#         str:
#     df :
#         pd.DataFrame:
#     table_name :
#         str:
#     dbName :
#         str:
#     df :
#         pd.DataFrame:
#     table_name :
#         str:
#     dbName:str :
#     df:pd.DataFrame :
#     table_name:str :
#     Returns
#     -------
#     """
#     conn, cur = DBConnect(dbName)

#     # df = preprocess_df(df)
#     # df = df.astype(object).where(pd.notnull(df), None)
#     columns = df.columns.to_list()

#     str_list = [str(element) for element in columns]
#     # Join the elements with commas
#     joined_str = ','.join(str_list)
#     # Enclose the string with parentheses
#     column_names = '(' + joined_str + ')'

#     formatted_list = ['%s'] * len(columns)
#     # Join the elements with commas
#     joined_str = ', '.join(formatted_list)
#     # Enclose the string with parentheses
#     values = '(' + joined_str + ')'

#     # Replicate the elements L times and format as "row[i]"
#     formatted_list = ['row[{}]'.format(i) for i in range(len(columns))]
#     # Join the elements with commas
#     data = ', '.join(formatted_list)

#     for _, row in df.iterrows():
#         sqlQuery = f"""INSERT INTO {table_name} {column_names}
#              VALUES{values};"""
#         data = (data)

#         try:
#             # Execute the SQL command
#             cur.execute(sqlQuery, data)
#             # Commit your changes in the database
#             conn.commit()
#             print("Data Inserted Successfully")
#         except Exce
