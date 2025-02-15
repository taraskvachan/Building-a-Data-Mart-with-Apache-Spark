import pandas as pd
import numpy as np
import faker

fake = faker.Faker()

num_rows = 4000

submit_ids = np.random.randint(1, 10001, num_rows)

names = [fake.first_name() for _ in range(num_rows)]
phones = [f'+38{fake.msisdn()[4:]}' for _ in range(num_rows)]

data = {
    'submit_id': submit_ids,
    'name': names,
    'phone': phones
}
df = pd.DataFrame(data)

df.to_csv('submit_data.csv', index=False)

print(df.head())