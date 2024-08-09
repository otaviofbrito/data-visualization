import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


connection = mysql.connector.connect(
    host='localhost',
    user='user',
    password='user',
    database='tm_db',
    port=3307
)

query = """
SELECT * FROM transfers
WHERE year > 1990 AND year <= 2024 AND transfer_fee != 0
ORDER BY(year);
"""

df = pd.read_sql(query, connection)


connection.close()

# fig = px.bar(df, x='year', y='transfers')
# fig.show()


plt.figure(figsize=(10, 6))
sns.boxplot(x='transfer_type', y='transfer_fee', data=df)
plt.title('Distribution of Transfer Fees')
plt.xlabel('Transfer Fee')

import numpy as np

# Add a new column with the log-transformed transfer fees
df['log_transfer_fee'] = np.log1p(df['transfer_fee'])

plt.figure(figsize=(10, 6))
sns.boxplot(x='transfer_type', y='log_transfer_fee', data=df)
plt.title('Distribution of Log-Transformed Transfer Fees by Transfer Type')
plt.xlabel('Transfer Type')
plt.ylabel('Log of Transfer Fee')


plt.savefig("output_plot.png")