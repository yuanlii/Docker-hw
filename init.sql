
-- check if database exists or not
DROP DATABASE IF EXISTS banking_db;
-- create banking db
CREATE DATABASE banking_db;

\connect banking_db;

-- check if tables exist or not
DROP TABLE IF EXISTS customer, account, customer_account;
-- create customer table
CREATE TABLE customer (
    customer_id serial PRIMARY KEY,
    first_name VARCHAR (50),
    last_name VARCHAR (50),
    street_address VARCHAR (150),
    city VARCHAR (50),
    -- Note: `state` been renamed to `state_`
    state_ VARCHAR (50),
    zip varchar(50),
    created_on TIMESTAMP
);

-- create account table
CREATE TABLE account (
    account_id serial PRIMARY KEY,
    balance numeric NOT NULL,
    created_on TIMESTAMP
);

-- create customer_account table
CREATE TABLE customer_account (
    customer_id integer NOT NULL,
    account_id integer NOT NULL,
    PRIMARY KEY (customer_id, account_id),
    CONSTRAINT customer_account_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
    CONSTRAINT customer_account_account_id_fkey FOREIGN KEY (account_id) REFERENCES account (account_id)
);

