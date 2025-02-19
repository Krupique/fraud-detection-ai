# Python and SQL - Data Loading Pipeline

# Imports
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

# Create the connection engine (PAY ATTENTION TO THE CONNECTION STRING BELOW!!!!!!)
engine = create_engine('postgresql+psycopg2://admin:admin1010@localhost:5553/transactiondb')

print("Starting the Data Loading Process!")

# Function to load data from CSV files into PostgreSQL in the specified schema
def load_data(csv_file, table_name, schema):

    # try/except block
    try:
        # Read the file csv
        df = pd.read_csv(csv_file)

        # Execute SQL from Pandas dataframe
        df.to_sql(table_name, engine, schema = schema, if_exists = 'append', index = False)
        print(f"Data from file {csv_file} has been inserted into table {schema}.{table_name}.")

    except Exception as e:
        print(f"Error inserting data from file {csv_file} into table {schema}.{table_name}: {e}")

# Loading data into the 'projectdb' schema
load_data('data/customers.csv', 'customers', 'projectdb')
load_data('data/properties.csv', 'properties', 'projectdb')
load_data('data/financial_transactions.csv', 'financial_transactions', 'projectdb')
load_data('data/transactions_history.csv', 'transactions_history', 'projectdb')

print("Load Successfully Executed! Use pgAdmin to Check the Data If You Want!")
