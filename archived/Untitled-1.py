import pyodbc
from faker import Faker
import random

class Test:
    def __init__(self, num_of_cust=1000, max_accnts_per_cust=10):
        self.conn = pyodbc.connect(dsn="my_driver")
        self.crsr = self.conn.cursor()

        self.num_of_cust = num_of_cust
        self.max_accnts_per_cust = max_accnts_per_cust
        self.num_of_accnt = 500  
        self.max_custs_per_accnt = 5

        self.fake = Faker() 
        self.fake.seed(4321)
        random.seed(0)
    
    def generate_date(self):
        print(random.randint(1, 10))


T = Test()
print(T.generate_date())

