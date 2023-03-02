"""
 This code reads list of nodes and edges from csv file then draws the graph on a world map.
"""

import os
import pandas as pd
import numpy as np
import networkx as nx
from tqdm import tqdm
from pygal.maps.world import World


# read edges and nodes
edges = pd.read_csv("edges.csv", header=0)
nodes = pd.read_csv("nodes.csv", header=0)
nodes = nodes.drop_duplicates()

# create network graph
G = nx.from_pandas_edgelist(edges, 'source', 'target', edge_attr=[
            'weight'])

# add node attributes to graph
node_attr = nodes.set_index('Id').to_dict('index')
nx.set_node_attributes(G, node_attr)

data = pd.DataFrame(columns=['id','degree','country','continent'])

i=0
# create a dataframe from node ID's and degree
for n in tqdm(G.nodes(data = True), total=len(G.nodes)):
    i+=1
    if n[1] != {}:
        data.loc[len(data)] = [n[0], G.degree(n[0], weight='weight'), n[1]['country'], n[1]['continent']]

# Sort by countries
data.sort_values(by=['country'], inplace=True)
countries = data['country'].drop_duplicates()
continents = data['continent'].drop_duplicates()

# draw the map
wm = World()
wm.force_uri_protocol = 'http'
wm.title="Top Centers in World"

continent_list = pd.read_csv("continent list.csv", header=0)
country_codes = pd.read_csv("country codes.csv", header=0)

for c in continents:
    c = continent_list.loc[continent_list['name'] == c]['code'].values[0]
    agg_d = {'degree': 'sum'}
    y_groups = data.groupby(['country'], as_index=False).agg(agg_d)

    for i, y in y_groups.iterrows():
        code = country_codes.loc[country_codes['Country'] == y['country']]['code'].values[0]
        wm.add(c,{code: y['degree']})

wm.render_to_file('map.svg')
