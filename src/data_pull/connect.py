import psycopg2
import pandas as pd
import hidden
import json

def connection(time_out = 3, func = hidden.secrets()):
    secrets = func

    conn = psycopg2.connect(host=secrets['host'],
            port=secrets['port'],
            database=secrets['database'], 
            user=secrets['user'], 
            password=secrets['pass'], 
            connect_timeout= time_out)

    try:
        cursor = conn.cursor()
        print("Connected to Redshift successfully.")
        return cursor, conn
    except Exception as e:
        print("Error connecting to Redshift:", e)
        return None

def execute_query(cursor, sql_query):
    sql = sql_query
    cursor.execute(sql)
    rows = cursor.fetchall()
    print('Fetching all rows is complete.')

    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    return df

def exeute(cursor, sql_query):
    sql = sql_query
    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]
    return data


def closure(cursor, conn):
    if cursor:
        cursor.close()
    if conn:
        conn.close()