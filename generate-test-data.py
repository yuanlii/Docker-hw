from faker import Faker
from faker.providers import internet

def create_test_data(cust_num = 1000, accnts_per_cust = 10):
    fake = Faker()
    fake.seed(4321)
    
    for _ in range(cust_num):
        print(fake.name())
    






# print(fake.address())
# print(fake.text())

# fake.random
# print(fake.random.getstate())