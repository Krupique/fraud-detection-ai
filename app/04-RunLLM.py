# Python - Insights Extraction Pipeline with LLM

# Imports
import csv
# from tqdm import tqdm
import psycopg2
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms.ollama import Ollama

# Function to generate text based on PostgreSQL data
def generate_insights():

    # Connect to the PostgreSQL database with the provided credentials
    print('Create connection')
    conn = psycopg2.connect(
        dbname="transactiondb",
        user="admin",
        password="admin1010",
        host="localhost",
        port="5553"
    )

    # Create a cursor to execute SQL commands
    cursor = conn.cursor()

    # Define the SQL query to retrieve customer, property and transaction data
    query = """
        SELECT t.transaction_id     AS transaction_id, 
               c.name               AS customer_name, 
               i.description        AS property_description,
               t.value              AS value_property, 
               t.transaction_date   AS transaction_date, 
               t.transaction_type   AS transaction_type, 
               t.status             AS status, 
               h.modification_date  AS modification_date, 
               h.description        AS history_description
        FROM projectdb.financial_transactions t
        JOIN projectdb.customers c 
          ON t.customer_id = c.customer_id
        JOIN projectdb.properties i 
          ON t.property_id  = i.property_id
        JOIN projectdb.transactions_history h 
          ON t.transaction_id = h.transaction_id
        
        WHERE t.value > 1000000  -- high value may be indicative of fraud
           OR (t.status = 'Completed' AND h.description LIKE '%Canceled%')  -- cancellation after completion may be suspicious
           OR EXISTS (  -- checks if there are multiple transactions for the same property in a short period of time
                        SELECT 1 FROM projectdb.financial_transactions t2
                        WHERE t2.property_id = t.property_id
                          AND t2.transaction_id != t.transaction_id
                          AND ABS(EXTRACT(DAY FROM AGE(t2.transaction_date, t.transaction_date))) < 30)
        ORDER BY t.transaction_date DESC;
    """

    # Execute the SQL query
    cursor.execute(query)

    # Get all the results of the query
    rows = cursor.fetchall()

    # Initialize a list to store the insights
    insights = []

    # Creating the chatbot prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a specialized real estate analyst. Analyze data and provide feedback on detecting fraud in real estate financial transactions."),
            ("user", "question: {question}")
        ]
    )

    # Definition of execution chain: prompt -> LLM -> output_parser
    chain = prompt | llm | output_parser

    # Iterate over the result rows
    for row in rows:
        # Unpack the values ​​from each row
        transaction_id, client, property_description, property_value, transaction_date, transaction_type, status, modification_date, description_history = row
        # Create the prompt for LLM based on the data
        query = f"Transaction_ID {transaction_id} Client Name {client} Property Description {property_description} Property Value ${property_value:.2f} Transaction Date {transaction_date} Transaction Type {transaction_type} Status {status} Modification Date {modification_date} History Description {description_history}."
        # Generate the insight text using LLM
        response = chain.invoke({'question': query})
        # Add the generated text to the list of insights
        insights.append(response)


    # Close the database connection
    conn.close()

    # Salva os insights em um arquivo CSV
    with open('results/insights.md', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Insight"])
        for insight in insights:
            writer.writerow([insight])

    print('The insights were saved on results/insights.md')

    # Retorna a lista de insights
    return insights


# Instantiating LLM Llama3 through Ollama
llm = Ollama(model = "llama3")

# Creating the parser for the language model output
output_parser = StrOutputParser()

# Generate insights by calling the defined function
insights = generate_insights()
