import mysql.connector
import pandas as pd
import plotly.express as px
import networkx as nx
import plotly.graph_objects as go

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
ON player_id = p.id;
"""

df = pd.read_sql(query, connection)

country_coords = pd.read_sql(
    "SELECT country, latitude AS lat, longitude AS lon, name FROM tm_db.countries;", connection)

connection.close()

country_coords.set_index('country', inplace=True)

# Create graph

G = nx.DiGraph()

for _, row in df.iterrows():
    origin = row['country_left']
    destination = row['country_joined']
    if G.has_edge(origin, destination):
        G[origin][destination]['weight'] += 1
    else:
        G.add_edge(origin, destination, weight=1)


edge_trace = []
for edge in G.edges(data=True):
    origin = edge[0]
    destination = edge[1]
    weight = edge[2]['weight']

    edge_trace.append(
        go.Scattergeo(
            locationmode='ISO-3',
            lon=[country_coords.loc[origin, 'lon'],
                 country_coords.loc[destination, 'lon']],
            lat=[country_coords.loc[origin, 'lat'],
                 country_coords.loc[destination, 'lat']],
            mode='lines',
            line=dict(width=weight, color='blue'),
            opacity=0.6,
        )
    )

node_trace = go.Scattergeo(
    locationmode='ISO-3',
    lon=[country_coords.loc[country, 'lon'] for country in G.nodes],
    lat=[country_coords.loc[country, 'lat'] for country in G.nodes],
    mode='markers',
    marker=dict(size=10, color='red'),
    text=[country for country in G.nodes]
)

fig = go.Figure(data=edge_trace + [node_trace])

fig.update_layout(
    title = 'Teste',
    showlegend = False,
    geo = dict(showframe = False, showcoastlines = True, projection_type = 'equirectangular')
)

fig.show()