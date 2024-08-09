import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


connection = mysql.connector.connect(
    host='localhost',
    user='user',
    password='user',
    database='tm_db',
    port=3307
)

query = """
SELECT 
    year,
    club_id,
    SUM(incoming) AS total_incoming,
    SUM(outgoing) AS total_outgoing
FROM (
    -- Count incoming transfers for each club and year
    SELECT 
        year,
        joined_club_id AS club_id,
        COUNT(*) AS incoming,
        0 AS outgoing
    FROM 
        transfers
    GROUP BY 
        year, joined_club_id

    UNION ALL

    -- Count outgoing transfers for each club and year
    SELECT 
        year,
        left_club_id AS club_id,
        0 AS incoming,
        COUNT(*) AS outgoing
    FROM 
        transfers
    GROUP BY 
        year, left_club_id
) AS transfers_summary
WHERE club_id = 631
GROUP BY 
    year
ORDER BY 
    year;
"""

df = pd.read_sql(query, connection)

bins = [1904, 1914, 1924, 1934, 1944, 1954, 2004, 2014, 2024]
labels = ["1905-1914", "1915-1924", "1925-1934", "1935-1944", "1945-1954", "1955-2004", "2005-2014", "2015-2024"]

# Create the 'year_interval' column
df['year_interval'] = pd.cut(df['year'], bins=bins, labels=labels, right=True)


connection.close()

df_melted = df.melt(
    id_vars=['year_interval', 'club_id'],
    value_vars=['total_incoming', 'total_outgoing'],
    var_name='transfer_type',
    value_name='count'
)

figure(num=None, figsize=(14, 6), dpi=80, facecolor='w', edgecolor='r')

sns.set_theme(style="dark")

# Create the bar plot
sns.barplot(
    data=df_melted,
    x='year_interval',
    y='count',
    hue='transfer_type',
    palette='muted'
)

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Number of Transfers')
plt.title('Incoming vs. Outgoing Transfers per Club by Year')
plt.savefig("test.png")