# Python - Database Creation Pipeline

# Import
import psycopg2

# Function to execute SQL script
def execute_script_sql(filename):
    
    # Connect to the PostgreSQL database with the provided credentials
    conn = psycopg2.connect(
        dbname="transactiondb",
        user="admin",
        password="admin1010",
        host="localhost",
        port="5553"
    )

    # Opens a cursor to perform operations on the database
    cur = conn.cursor()

    # Read the contents of the SQL file
    with open(filename, 'r') as file:
        sql_script = file.read()

    try:
        # Execute the SQL script
        cur.execute(sql_script)

        # Commit changes to the database
        conn.commit()  
        print("\nScript executed successfully!\n")
    except Exception as e:
        # Revert changes on error
        conn.rollback()  
        print(f"Error executing script: {e}")
    finally:
        # Closes communication with the database
        cur.close()
        conn.close()

# Execute the SQL script
execute_script_sql('app/ProjectDatabase-Tables.sql')


