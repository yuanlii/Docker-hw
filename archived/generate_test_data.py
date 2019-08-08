from faker import Faker
import random

# TODO: need to fix random seed

class GenerateTestData:
    def __init__(self, faker_seed = 4321, random_seed = 0):
        self.fake = Faker()
        self.fake.seed(faker_seed)

        self.random = random
        self.random.seed(random_seed)

        self.customer = {}
        self.customer_account = {}
        self.account = {}

    
    def generate_customer_data(self, cust_num = 1000, accnts_per_cust = 10):
        '''
        customer = {
            'customer_id':...
            'first_name': ...
            'last_name': ...
            'street_address':...
            'city': ...
            'state': ..
            'zip': ...
            'created_on': ...
        }
        '''
        f_names, l_names = self.generate_name(cust_num)
        self.customer['first_name'] = f_names
        self.customer['last_name'] = l_names

        addrs, cities, states, zip_codes = self.generate_street_address(cust_num)
        self.customer['street_address'] = addrs
        self.customer['city'] = cities
        self.customer['state'] = states
        self.customer['zip'] = zip_codes

        dates = self.generate_create_time(cust_num)
        self.customer['created_on'] = dates

        return self.customer


    def generate_name(self, cust_num = 1000):
        f_names = []
        l_names = []
        
        while len(f_names) < cust_num or len(l_names) < cust_num:
            try:
                f_names.append(self.fake.first_name())
                l_names.append(self.fake.last_name())
                
            except:
                pass

        return f_names, l_names

    
    def generate_street_address(self, cust_num = 1000):
        addrs = []
        cities = []
        states = []
        zip_codes = []
        
        while len(addrs) < cust_num or len(cities) < cust_num or len(states) < cust_num or len(zip_codes) < cust_num:
            try:
                addr, city = self.fake.address().split('\n')
                c_name, state = city.split(',')
                s_name, zip_code = state.split()
                
                # append later to make sure they are the same length
                addrs.append(addr)
                cities.append(c_name)
                states.append(s_name)
                zip_codes.append(zip_code)
                
            except:
                pass
            
        return addrs, cities, states, zip_codes
    

    def generate_create_time(self, cust_num = 1000):
        dates = []
        for _ in range(cust_num):
            date = self.fake.date(pattern="%Y-%m-%d")
            dates.append(date)
        return dates
    
    
    def generate_customer_account(self, cust_num = 1000, max_accnts_per_cust = 10):
        '''
        customer_account = {
            'customer_id':..
            'account_id':...
        }
        '''
        last_id = 0
        for i in range(cust_num):     
            # one customer can get up to max_accnts_per_cust, randomly assign how many accounts owned by one customer
            accnt_num = self.random.randint(1, max_accnts_per_cust)
            accnt = [list(range(last_id,last_id + accnt_num))]
            self.customer_account[i] = accnt
            
            # increament from the last id
            last_id = last_id + accnt_num
    
        return self.customer_account
        

    def generate_account_data(self, account_num):
        '''
        account = {
            'account_id':..
            'balance':...
            'create_on':...
        }
        '''
        balance_lst = self.generate_balance(account_num)
        self.account['balance'] = balance_lst

        dates = self.generate_accnt_create_time(account_num)
        self.account['created_on'] = dates
        
        return self.account
        
        
    def generate_balance(self, account_num):
        balance_lst = []
        # number of accounts is based on customer and customer_account data
        for _ in range(account_num):
            balance = random.random() * 5000
            balance_lst.append(balance)
        return balance_lst


    def generate_accnt_create_time(self, account_num):
        dates = []
        for _ in range(account_num):
            date = self.fake.date(pattern="%Y-%m-%d")
            dates.append(date)
        return dates

        

if __name__ == '__main__':
    gtd = GenerateTestData()
    
    # customer table - ok
    customer = gtd.generate_customer_data()
    customer_df = pd.DataFrame(customer)
    customer_df = customer_df.reset_index()
    customer_df = customer_df.rename(columns={'index':'customer_id'})
    customer_df.head()
    # customer_df.to_csv('static/csv/customer.csv', index = False)

    # customer_account table - ok
    customer_account = gtd.generate_customer_account()
    # format as dataframe
    customer_account_df = pd.DataFrame(customer_account)
    customer_account_df = customer_account_df.transpose()
    customer_account_df = customer_account_df.reset_index()
    customer_account_df = customer_account_df.rename(columns={0:'account_id','index':'customer_id'})

    # Explode/Split column into multiple rows
    customer_account_df = pd.DataFrame(customer_account_df.account_id.tolist(), index= customer_account_df.customer_id).stack()
    customer_account_df = customer_account_df.reset_index([0, 'customer_id'])
    customer_account_df.columns = ['customer_id', 'account_id']
    customer_account_df = customer_account_df.astype('int')
    customer_account_df.head()

    # customer_account_df.to_csv('static/csv/customer_account.csv', index = False)

    # account table - ok
    account_num = len(customer_account_df)
    account = gtd.generate_account_data(account_num)
    account_df = pd.DataFrame(account)
    account_df.head()

    account_df = account_df.reset_index().rename(columns = {'index':'account_id'})
    account_df.head()
    # account_df.to_csv('static/csv/account.csv', index = False)










# ----------
# reference:
# ----------
# generate random number: https://www.pythonforbeginners.com/random/how-to-use-the-random-module-in-python

# How to use the random module in Python: https://www.pythonforbeginners.com/random/how-to-use-the-random-module-in-python

