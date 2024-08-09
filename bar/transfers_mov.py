import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import matplotlib.patches as mpatches
from matplotlib.pyplot import figure

connection = mysql.connector.connect(
    host='localhost',
    user='user',
    password='user',
    database='tm_db',
    port=3307
)

query = """
SELECT COUNT(*) as qtd, c1.country as country_left, c1.name AS name
FROM transfers t
JOIN (SELECT clubs.id, cts.country, cts.name FROM clubs
		JOIN (SELECT l.id, c.country, c.name FROM leagues l
				JOIN countries c
                ON l.country_id = c.country) cts
		ON clubs.id_current_league = cts.id) c1
ON left_club_id = c1.id
JOIN (SELECT clubs.id, cts.country, cts.name FROM clubs
		JOIN (SELECT l.id, c.country, c.name FROM leagues l
				JOIN countries c
                ON l.country_id = c.country) cts
		ON clubs.id_current_league = cts.id) c2
ON joined_club_id = c2.id
JOIN players p
ON player_id = p.id
WHERE c1.country != c2.country
GROUP BY (c1.country)
ORDER BY (c1.country);
"""

query2 = """
SELECT COUNT(*) as qtd, c2.country as country_left, c2.name AS name
FROM transfers t
JOIN (SELECT clubs.id, cts.country, cts.name FROM clubs
		JOIN (SELECT l.id, c.country, c.name FROM leagues l
				JOIN countries c
                ON l.country_id = c.country) cts
		ON clubs.id_current_league = cts.id) c1
ON left_club_id = c1.id
JOIN (SELECT clubs.id, cts.country, cts.name FROM clubs
		JOIN (SELECT l.id, c.country, c.name FROM leagues l
				JOIN countries c
                ON l.country_id = c.country) cts
		ON clubs.id_current_league = cts.id) c2
ON joined_club_id = c2.id
JOIN players p
ON player_id = p.id
WHERE c1.country != c2.country
GROUP BY (c2.country)
ORDER BY (c2.country);
"""

df = pd.read_sql(query, connection)


connection.close()

# fig = px.bar(df, x='year', y='transfers')
# fig.show()

sns.set_theme(style="darkgrid")
sns.barplot(data=df, x='country_left', y='qtd')

#palette = sns.color_palette("mako", len(df['type'].unique()))

figure(num=None, figsize=(24,20), dpi=80, facecolor='w', edgecolor='r')
sns.barplot(data=df, y='name', x='qtd', hue='qtd', legend=False, palette='viridis')


plt.xlabel("Number of Transfers")  # X-axis label
plt.ylabel("Countries")  # Y-axis label
plt.title("Volume of Transfers Leaving Countries")

plt.savefig("LeavingTransfers.png")