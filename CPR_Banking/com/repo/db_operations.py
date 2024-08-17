import mysql.connector
from CPR_Banking.com.service.constants import *

def db_connect():
    try:
        # Establish database connection
        conn = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        return conn

    except mysql.connector.Error as err:
        print("Database Connection Error: ", err)
        print()



def insert_data(table_name, **kwargs):

    # establishing connection
    conn = db_connect()
    cursor = conn.cursor()

    try:

        # inserting data into flm_users table
        if table_name == "cpr_users":
            sql = ("INSERT INTO cpr_users (first_name, last_name, email, dob, salt, password) "
                   "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(dob)s, %(salt)s, %(password)s)")

        # inserting data into flm_accounts table
        elif table_name == "cpr_accounts":
            sql = ("INSERT INTO cpr_accounts (user_id, account_number, balance, is_active) "
                   "VALUES (%(user_id)s, %(account_number)s, %(balance)s, %(is_active)s)")

        # inserting data into flm_transactions table
        elif table_name == "cpr_transactions":
            sql = (
                "INSERT INTO cpr_transactions (user_id, account_id, amount, from_account, to_account, trans_date, trans_type) "
                "VALUES (%(user_id)s, %(account_id)s, %(amount)s, %(from_account)s, %(to_account)s, NOW(), %(trans_type)s)")
        else:
            raise ValueError("Invalid table name")

        # executing insert query
        cursor.execute(sql, kwargs)
        conn.commit()
        return

    except mysql.connector.Error as err:
        print("Error in inserting data into database: ", err)
        conn.rollback() # Rollback in case of any error
        return

    finally:
        conn.commit()
        cursor.close()
        conn.close()



def fetch_data(table_name, **kwargs):
    # Establishing the connection
    conn = db_connect()
    cursor = conn.cursor()

    try:
        base_sql = f"SELECT * FROM {table_name}"

        # Construct WHERE clause based on provided filters
        filters = " AND ".join([f"{key}=%({key})s" for key in kwargs])

        if filters:
            sql = f"{base_sql} WHERE {filters}"
        else:
            sql = base_sql

        cursor.execute(sql, kwargs)

        # fetching all data based on where clause
        results = cursor.fetchall()
        #print(type(results))
        return results

    except mysql.connector.Error as err:
        print("Error:", err)
        return []

    finally:
        cursor.close()
        conn.close()


def fetch_column_data(table_name, column_name):

    # Establishing the connection
    conn = db_connect()
    cursor = conn.cursor()

    try:
        sql = f"SELECT {column_name} FROM {table_name}"
        cursor.execute(sql)
        results = cursor.fetchall()
        return [row[0] for row in results]  # Extracting column values from the result rows

    except mysql.connector.Error as err:
        print("Error:", err)
        return False

    finally:
        cursor.close()
        conn.close()


def update_data(table_name, values, conditions):
    # Establishing  the connection
    conn = db_connect()
    cursor = conn.cursor()

    try:
        # Construct the SET clause for the UPDATE statement
        set_clause = ", ".join([f"{key}=%({key})s" for key in values])

        # Construct the WHERE clause for the UPDATE statement
        where_clause = " AND ".join([f"{key}=%({key})s" for key in conditions])

        sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

        # Merge the values and conditions dictionaries for parameter substitution
        params = {**values, **conditions}

        cursor.execute(sql, params)
        conn.commit()

    except mysql.connector.Error as err:
        print("Error:", err)
        conn.rollback()  # Rollback in case of any error

    finally:
        conn.commit()
        cursor.close()
        conn.close()


def delete_data(table_name, conditions):
    # Establish the connection
    conn = db_connect()
    cursor = conn.cursor()

    try:
        # Construct the WHERE clause for the DELETE statement
        where_clause = " AND ".join([f"{key}=%({key})s" for key in conditions])

        sql = f"DELETE FROM {table_name} WHERE {where_clause}"

        cursor.execute(sql, conditions)
        conn.commit()

    except mysql.connector.Error as err:
        print("Error:", err)
        conn.rollback()  # Rollback in case of any error

    finally:
        cursor.close()
        conn.close()



def update_last_login_by_email(user_mail):
    try:
        # Connect to the MySQL database
        conn = db_connect()

        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        # Update the lastlogin_date for the user with the given user_id
        update_query = """
            UPDATE cpr_users
            SET lastlogin_date = NOW()
            WHERE email = %s
        """

        cursor.execute(update_query, (user_mail,))

        # Commit the changes to the database
        conn.commit()
        # Close the cursor and the database connection
        cursor.close()
        conn.close()
        return

    except mysql.connector.Error as e:
        print("Error in updating last login time: ", e)
        return

