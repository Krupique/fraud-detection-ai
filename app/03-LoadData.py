# Python and SQL - Data Loading Pipeline

# Imports
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

# Create the connection engine (PAY ATTENTION TO THE CONNECTION STRING BELOW!!!!!!)
engine = create_engine('postgresql+psycopg2://adming:adming1010@localhost:5553/transactiondb')

print("\nStarting the Data Loading Process!\n")

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
load_data('clients.csv', 'clientes', 'projectdb')
load_data('properties.csv', 'imoveis', 'projectdb')
load_data('financial_transactions.csv', 'financial_transactions', 'projectdb')
load_data('transactions_history.csv', 'transactions_history', 'projectdb')

print("\nLoad Successfully Executed! Use pgAdmin to Check the Data If You Want!\n")
print("\nStarting the Data Analysis Process with AI. Be Patient and Wait for the Excellent Result That Will Be Delivered to You!\n")




