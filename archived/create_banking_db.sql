
-- check if database exists or not
DROP DATABASE IF EXISTS banking;

-- create banking db
CREATE DATABASE banking;


-- check if tables exist or not
DROP TABLE IF EXISTS customer, account, customer_account;

-- create customer table
CREATE TABLE customer (
    customer_id serial PRIMARY KEY,
    first_name VARCHAR (50) NOT NULL,
    last_name VARCHAR (50)  NOT NULL,
    street_address VARCHAR (150)   NOT NULL,
    city VARCHAR (50),
    state VARCHAR (50),
    zip varchar(50)  NOT NULL,
    created_on TIMESTAMP NOT NULL
);

-- populate customer data from csv
COPY customer(customer_id,first_name,last_name,street_address,city,state,zip,created_on) 
FROM '/Users/liyuan/Desktop/Docker-hw/static/csv/customer.csv' DELIMITER ',' CSV HEADER;


CREATE TABLE account (
    account_id serial PRIMARY KEY,
    balance real NOT NULL,
    created_on TIMESTAMP NOT NULL
);

-- populate account data from csv
COPY account(account_id, balance, created_on)
FROM '/Users/liyuan/Desktop/Docker-hw/static/csv/account.csv' DELIMITER ',' CSV HEADER;


CREATE TABLE customer_account (
    customer_id integer NOT NULL,
    account_id integer NOT NULL,
    PRIMARY KEY (customer_id, account_id),
    CONSTRAINT customer_account_customer_id_fkey FOREIGN KEY (customer_id)   REFERENCES customer (customer_id),
    CONSTRAINT customer_account_account_id_fkey FOREIGN KEY (account_id)     REFERENCES account (account_id)
);

-- populate customer_account data from csv
COPY customer_account(customer_id, account_id)
FROM '/Users/liyuan/Desktop/Docker-hw/static/csv/customer_account.csv' DELIMITER ',' CSV HEADER;


-----------------
--  SQL query --
-----------------
-- Find the states having the 10 highest average customer balances
select c.state_, avg(a.balance) as average_balance
from customer c
join customer_account ca
on c.customer_id = ca.customer_id
join account a
on a.account_id = ca.account_id
group by c.state_
order by avg(a.balance) desc
limit 10;

-- Find the 10 customers with the highest total balances
select c.customer_id, c.first_name, c.last_name, sum(a.balance) as total_balance
from customer c
join customer_account ca
on ca.customer_id = c.customer_id
join account a
on a.account_id = ca.account_id
group by c.customer_id, c.first_name, c.last_name
order by sum(a.balance) desc 
limit 10;

-- Find the 10 customers with the lowest total balances
select c.customer_id, c.first_name, c.last_name, sum(a.balance) as total_balance
from customer c
join customer_account ca
on ca.customer_id = c.customer_id
join account a
on a.account_id = ca.account_id
group by c.customer_id, c.first_name, c.last_name
order by sum(a.balance) 
limit 10;

-- Operation Robinhood: transactionally transfer 10 percent of each of the top 10 customers largest account to the each of the bottom 10 customers
select t2.customer_id, t2.account_id, t2.min_balance + 0.1*(t1.max_balance) as new_balance
from
(select c.customer_id, a.account_id, max(a.balance) as max_balance
from customer c
join customer_account ca
on ca.customer_id = c.customer_id
join account a
on a.account_id = ca.account_id
group by c.customer_id, a.account_id
order by max(a.balance) desc 
limit 10) t1,
(select c.customer_id, a.account_id, min(a.balance) as min_balance
from customer c
join customer_account ca
on ca.customer_id = c.customer_id
join account a
on a.account_id = ca.account_id
group by c.customer_id, a.account_id
order by min(a.balance)
limit 10) t2;