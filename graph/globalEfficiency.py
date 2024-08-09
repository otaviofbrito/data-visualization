import mysql.connector
import pandas as pd
import plotly.express as px
import networkx as nx
import plotly.graph_objects as go
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
SELECT p.name, t.year, t.transfer_fee, t.transfer_type,
 c1.country AS country_left,
 c2.country AS country_joined
FROM transfers t
JOIN (SELECT clubs.id, cts.country FROM clubs
		JOIN (SELECT l.id, c.country FROM leagues l
				JOIN countries c
                ON l.country_id = c.country) cts
		ON clubs.id_current_league = cts.id) c1
ON left_club_id = c1.id
JOIN (SELECT clubs.id, cts.country FROM clubs
		JOIN (SELECT l.id, c.country FROM leagues l
				JOIN countries c
                ON l.country_id = c.country) cts
		ON clubs.id_current_league = cts.id) c2
ON joined_club_id = c2.id
JOIN players p
ON player_id = p.id
WHERE t.year >= 1905 AND t.year <= 2024;
"""

df = pd.read_sql(query, connection)

country_coords = pd.read_sql(
    "SELECT country, latitude AS lat, longitude AS lon, name FROM tm_db.countries;", connection)

connection.close()

country_coords.set_index('country', inplace=True)

years = df['year'].unique()
years = sorted(years)

globalEff = []
yrs = []

# create graph for each year
for i in range(len(years)):
    G = nx.Graph()

    year_data = df[df['year'] == years[i]]

    for _, row in year_data.iterrows():
        origin = row['country_left']
        destination = row['country_joined']
        if not G.has_edge(origin, destination):
            G.add_edge(origin, destination)

    yrs.append(years[i])
    eff = nx.global_efficiency(G)
    globalEff.append(eff)


dfres = pd.DataFrame({
    'Year': yrs,
    'Global Efficiency': globalEff
})

#df_filtered = dfres[dfres['Year'] % 10 == 0]
sns.set_theme(style="darkgrid")

# fig = px.line(dfres, x='Year', y='Global Efficiency', markers=True)
# fig.show()

sns.lineplot(data=dfres, x='Year', y='Global Efficiency', marker='o', markersize=4, palette='mako')

plt.savefig("output_plot.png")