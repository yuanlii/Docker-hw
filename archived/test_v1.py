import pyodbc
from faker import Faker
import random

# connect db
conn = pyodbc.connect(dsn="my_driver")
crsr = conn.cursor()

# parameter
num_of_cust = 100 # default = 1000
max_accnts_per_cust = 10
num_of_accnt = 500  # defualt = 500
max_custs_per_accnt = 5

# generate test data
fake = Faker() 
fake.seed(4321)
random.seed(0)


# TODO: can re-write into a function

customer_dct = {}
account_ids = []

for i in range(num_of_cust): 
    first_name = fake.first_name()
    last_name = fake.last_name()
    address = fake.address().split('\n')[0]
    city = fake.city()
    state = fake.state()
    zip_code = fake.zipcode()
    date = fake.date(pattern="%Y-%m-%d")

    # populate customer data
    crsr.execute("INSERT INTO customer (first_name, last_name, street_address, city, state_, zip, created_on) VALUES (?,?,?,?,?,?,?) RETURNING customer_id", (first_name, last_name, address, city, state, zip_code, date))
    # get customer_id returned
    customer_id = crsr.fetchone()[0]

    # for each customer, genenerate a radom number of accounts (up to the max_accnts_per_cust)
    accnts_per_cust = random.randint(1, max_accnts_per_cust)
    print('accnts_per_cust:',accnts_per_cust)

    # use dictionary to keep tract of the remaining number of accounts associated with each customer
    customer_dct[customer_id] = max_accnts_per_cust - accnts_per_cust

    print(customer_dct)
    
    for j in range(accnts_per_cust):   

        balance = random.random() * 5000
        accnt_date = fake.date(pattern="%Y-%m-%d")

        # populate account data
        crsr.execute("INSERT INTO account (balance, created_on) VALUES (?,?) RETURNING account_id", (balance, accnt_date))

        # get account_id returned
        account_id = crsr.fetchone()[0]
        print('account_id:',account_id)
        account_ids.append(account_id)

        # populate customer_account data
        crsr.execute("INSERT INTO customer_account (customer_id, account_id) VALUES (?,?)", (customer_id, account_id))


for accnt_id in account_ids:
    print(accnt_id) 
    # generate random number of customers associated with one account
    # note: minus 1 because of previously linked customer-account
    custs_per_accnt = random.randint(1, max_custs_per_accnt-1)

    # create linkages of account and each of its associated customer
    for j in range(custs_per_accnt):
        cust_id = random.randint(1, num_of_cust)

        # checking if still have storage
        if customer_dct[cust_id] > 0:
            try:
                crsr.execute("INSERT INTO customer_account (customer_id, account_id) VALUES (?,?)",(cust_id, accnt_id))
                print("successfully inserted!")

                # after creating one linkage, the "storage" of the customer will decrement 1
                customer_dct[cust_id] -= 1
        
            except:
                pass

        

conn.commit()
crsr.close()
conn.close()

