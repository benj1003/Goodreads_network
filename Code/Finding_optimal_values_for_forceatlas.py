import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as pltcolors
from fa2 import ForceAtlas2
import sys



G = nx.read_gpickle('optimal values for forceatlas\pos_books_graph.pcl')

d = dict(G.degree)
d_between = dict(nx.betweenness_centrality(G))
d_eigen = dict(nx.eigenvector_centrality(G))

total = pd.DataFrame(data = {'Name' : list(d.keys()), 
                             'Degree' : list(d.values()),
                             'Betweenness_centrality' : list(d_between.values()),
                             'Eigenvector_centrality' : list(d_eigen.values())})

genre = set(nx.get_node_attributes(G,'genre').values()) 
colors_tmp = list(pltcolors._colors_full_map.values())[0:len(genre)]
cmap = dict(zip(genre, colors_tmp))
nodes = G.nodes()
colors = [cmap.get(G.node[n]['genre']) for n in nodes]

# Plotting network with node size = total degree
gravity = 0
scalingRatio = 0
N = 1

for measure in ['Degree']: #, 'Betweenness_centrality', 'Eigenvector_centrality']
    if measure == 'Degree':
        scale = 20
    else:
        scale = 1000

    for i in range(N):
        gravity = 0
        scalingRatio += 1
        
        for j in range(10):
            gravity += 0.2
            
            forceatlas2 = ForceAtlas2(
                                # Behavior alternatives
                                outboundAttractionDistribution=True,  # Dissuade hubs
                                linLogMode=False,  # NOT IMPLEMENTED
                                adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
                                edgeWeightInfluence=0,

                                # Performance
                                jitterTolerance=1.0,  # Tolerance
                                barnesHutOptimize=True,
                                barnesHutTheta=1.2,
                                multiThreaded=False,  # NOT IMPLEMENTED

                                # Tuning
                                scalingRatio=scalingRatio,
                                strongGravityMode=False,
                                gravity=gravity,

                                # Log
                                verbose=False)
            
            
            plt.figure(figsize=(30, 15))
            plt.title(f"scalingRatio = {scalingRatio} and gravity = {gravity}", fontsize = 20)
            positions = forceatlas2.forceatlas2_networkx_layout(G, pos=None, iterations=200)
            nx.draw(G, positions, node_size=(total[measure]+1)*scale, with_labels=False, width = 0.35, node_color=colors, alpha=0.9)
            plt.savefig(f'Figures\scaline = {scalingRatio} and gravity = {gravity}.png')
            print(f'Nået {(i+j)/N}')
  