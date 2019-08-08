from faker import Faker
import json 
from random import randint 

fake = Faker() 
fake.seed(4321)

def generate_customer_data(x): 
  
    # dictionary 
    cust_data ={} 
    for i in range(0, x): 
        
        id = randint(1, 1000) 
        first_name = fake.first_name()
        last_name = fake.last_name()

        address, city = fake.address().split('\n')
        city_name, state = city.split(',')
        state_name, zip_code = state.split()
        date = fake.date(pattern="%Y-%m-%d")



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




if __name__ == '__main__':   
    # Enter number of students 
    number_of_customers = 10  # For the above task make this 100 
    input_data(number_of_customers) 