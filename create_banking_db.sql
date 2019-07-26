
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

CREATE TABLE account (
    account_id serial PRIMARY KEY,
    balance VARCHAR (255)  NOT NULL,
    created_on TIMESTAMP NOT NULL
);

CREATE TABLE customer_account (
    customer_id integer NOT NULL,
    account_id integer NOT NULL,
    PRIMARY KEY (customer_id, account_id),
    CONSTRAINT customer_account_customer_id_fkey FOREIGN KEY (customer_id)   REFERENCES customer (customer_id),
    CONSTRAINT customer_account_account_id_fkey FOREIGN KEY (account_id)     REFERENCES account (account_id)
);
