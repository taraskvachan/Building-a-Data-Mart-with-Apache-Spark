import pandas as pd
import numpy as np

date_range = pd.date_range(start='2024-01-01', end='2025-01-27')
campaign_ids = range(1, 101)

data = {
    "date": [],
    "campaign_id": [],
    "costs": [],
    "clicks": [],
    "views": []
}

for date in date_range:
    for campaign_id in campaign_ids:
        data["date"].append(date)
        data["campaign_id"].append(campaign_id)
        data["costs"].append(round(np.random.uniform(0, 1000), 2))  
        data["clicks"].append(np.random.randint(0, 100))            
        data["views"].append(np.random.randint(0, 1000))            

df = pd.DataFrame(data)

df.to_csv("costs_postgresql.csv", index=False)

print("Data saved to campaign_data.csv")