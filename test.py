import pyodbc
from faker import Faker
import random
import pandas as pd

class Test:
    def __init__(self, num_of_cust=1000, max_accnts_per_cust=10, max_custs_per_accnt=5):
        self.conn = pyodbc.connect(dsn="my_driver")
        self.crsr = self.conn.cursor()

        self.num_of_cust = num_of_cust
        # max number of accounts allowed for one customer
        self.max_accnts_per_cust = max_accnts_per_cust
        # max number of customers allowed for one account
        self.max_custs_per_accnt = max_custs_per_accnt

        self.fake = Faker() 
        self.fake.seed(4321)
        random.seed(0)

    def populate_test_data(self):
        customer_dct = {}
        account_ids = []

        for i in range(self.num_of_cust): 
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            address = self.fake.address().split('\n')[0]
            city = self.fake.city()
            state = self.fake.state()
            zip_code = self.fake.zipcode()
            date = self.fake.date(pattern="%Y-%m-%d")

            # populate customer data
            self.crsr.execute("INSERT INTO customer (first_name, last_name, street_address, city, state_, zip, created_on) VALUES (?,?,?,?,?,?,?) RETURNING customer_id", (first_name, last_name, address, city, state, zip_code, date))
            # get customer_id returned
            customer_id = self.crsr.fetchone()[0]

            # for each customer, genenerate a radom number of accounts (up to max_accnts_per_cust)
            accnts_per_cust = random.randint(1, self.max_accnts_per_cust)

            # use dictionary to keep tract of the remaining number of accounts associated with each customer
            customer_dct[customer_id] = self.max_accnts_per_cust - accnts_per_cust
            
            for j in range(accnts_per_cust):   
                balance = random.random() * 5000
                accnt_date = self.fake.date(pattern="%Y-%m-%d")

                # populate account data
                self.crsr.execute("INSERT INTO account (balance, created_on) VALUES (?,?) RETURNING account_id", (balance, accnt_date))

                # get account_id returned
                account_id = self.crsr.fetchone()[0]
                account_ids.append(account_id)

                # populate customer_account data
                self.crsr.execute("INSERT INTO customer_account (customer_id, account_id) VALUES (?,?)", (customer_id, account_id))


        for accnt_id in account_ids:
            # generate random number of customers for one account
            # need to exclude the originally linked customer, so minus 1
            custs_per_accnt = random.randint(1, self.max_custs_per_accnt - 1)

            for j in range(custs_per_accnt):
                cust_id = random.randint(1, self.num_of_cust)

                # checking if this customer_id have remaining "storage" to map account id
                if customer_dct[cust_id] > 0:
                    try:
                        self.crsr.execute("INSERT INTO customer_account (customer_id, account_id) VALUES (?,?)",(cust_id, accnt_id))

                        # after creating one linkage, the storage of the customer will reduce 1
                        customer_dct[cust_id] -= 1

                    # ignore if customer id has already linked to the account
                    except:
                        pass

        self.conn.commit()


    def execute_query(self):
        print('executing the first query.')

        # Find the states having the 10 highest average customer balances
        self.crsr.execute(
        """
        select c.state_, avg(a.balance) as average_balance 
        from customer c 
        join customer_account ca 
        on c.customer_id = ca.customer_id 
        join account a on a.account_id = ca.account_id 
        group by c.state_ 
        order by avg(a.balance) desc 
        limit 10;
        """
        )
        
        rows = self.crsr.fetchall() 
        for row in rows: 
            print (row.state_, row.average_balance)


        print('-------------------------------')
        print('executing the second query.')

        # Find the 10 customers with the highest total balances
        self.crsr.execute(
        """
        select c.customer_id, c.first_name, c.last_name, sum(a.balance) as total_balance
        from customer c
        join customer_account ca
        on ca.customer_id = c.customer_id
        join account a
        on a.account_id = ca.account_id
        group by c.customer_id, c.first_name, c.last_name
        order by sum(a.balance) desc 
        limit 10; 
        """
        )

        rows = self.crsr.fetchall() 
        for row in rows: 
            print (row.customer_id, row.first_name, row.last_name, row.total_balance)


        print('-------------------------------')
        print('executing the third query.')

        # Find the 10 customers with the lowest total balances
        self.crsr.execute(
        """
        select c.customer_id, c.first_name, c.last_name, sum(a.balance) as total_balance
        from customer c
        join customer_account ca
        on ca.customer_id = c.customer_id
        join account a
        on a.account_id = ca.account_id
        group by c.customer_id, c.first_name, c.last_name
        order by sum(a.balance) 
        limit 10;
        """
        )

        rows = self.crsr.fetchall() 
        for row in rows: 
            print (row.customer_id, row.first_name, row.last_name, row.total_balance)


        print('-------------------------------')
        print('executing the fourth query.')
        # Operation Robinhood: transactionally transfer 10 percent of each of the top 10 customers largest account to the each of the bottom 10 customers
        self.crsr.execute(
        """ 
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
        """
        )

        rows = self.crsr.fetchall() 
        for row in rows: 
            print (row.customer_id, row.account_id, row.new_balance)

        self.crsr.close()
        self.conn.close()


if __name__ == "__main__":

    # specify number of customers
    num_of_cust = 50
    # specify maximum number of accounts that can be associated with one single customer
    max_accnts_per_cust = 10
    # specify maximun number of customers that can be associated with one single account
    max_custs_per_accnt = 5

    T = Test(num_of_cust, max_accnts_per_cust, max_custs_per_accnt)
    print('start populating test data ...')
    T.populate_test_data()
    print('database finish loading data.')
    print('start executing queries ...')
    T.execute_query()