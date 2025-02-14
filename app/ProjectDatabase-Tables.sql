-- SQL - Database Creation

-- Delete the schema if it already exists
DROP SCHEMA IF EXISTS projectdb CASCADE;

-- Create the schema
CREATE SCHEMA projectdb AUTHORIZATION admin;


-- Creates the tables
CREATE TABLE projectdb.customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(2),
    zipcode VARCHAR(10)
);

CREATE TABLE projectdb.properties (
    property_id SERIAL PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zipcode VARCHAR(10),
    description TEXT
);

CREATE TABLE projectdb.financial_transactions (
    transaction_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    property_id INT NOT NULL,
    value DECIMAL(15, 2) NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_type VARCHAR(50),
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES projectdb.customers(customer_id),
    FOREIGN KEY (property_id) REFERENCES projectdb.properties(property_id)
);

CREATE TABLE projectdb.transactions_history (
    history_id SERIAL PRIMARY KEY,
    transaction_id INT NOT NULL,
    modification_date DATE NOT NULL,
    description TEXT,
    FOREIGN KEY (transaction_id) REFERENCES projectdb.financial_transactions(transaction_id)
);

