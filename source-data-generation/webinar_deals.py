import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import faker

fake = faker.Faker()

num_rows = 2000

deal_ids = np.arange(1, num_rows + 1)

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 1, 27)
deal_dates = [start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days)) for _ in range(num_rows)]
deal_dates = [date.strftime('%Y-%m-%d') for date in deal_dates]

emails = [fake.email() for _ in range(num_rows)]

addresses = [fake.address().replace('\n', ', ') for _ in range(num_rows)]

fios = [fake.name() for _ in range(num_rows)]

df1 = pd.read_csv('submit_data.csv')
phones = df1.iloc[:, 2].tolist()
phones = ['+' + str(phone) for phone in np.random.choice(phones, num_rows)]

data = {
    'deal_id': deal_ids,
    'deal_date': deal_dates,
    'fio': fios,
    'phone': phones,
    'email': emails,
    'address': addresses
}

df = pd.DataFrame(data)

df.to_csv('deal_data.csv', index=False)

print(df.head())