import numpy as np
import networkx as nx
import operator

import TRBS.source_estimation as se
'''
def trbs(graph, obs_time, distribution):

    path_lengths = {}
    paths = {}

    obs = np.array(list(obs_time.keys()))
    for o in obs:
        path_lengths[o], paths[o] = nx.single_source_dijkstra(graph, o)

    ### Run the estimation
    s_est, likelihoods = se.source_estimate(graph, obs_time, paths, path_lengths)

    ranked = sorted(likelihoods.items(), key=operator.itemgetter(1), reverse=True)
    print('ranked', ranked)

    return (s_est, ranked)
'''

def trbs(graph, obs_time, distribution):

    path_lengths = {}
    obs = np.array(list(obs_time.keys()))
    for o in obs:
        path_lengths[o] = preprocess(o, graph, distribution)
    ### Run the estimation
    s_est, likelihoods = se.source_estimate(graph, obs_time)


def preprocess(observer, graph, distr):
    ### Initialization of the edge delay
    edges = graph.edges()
    for (u, v) in edges:
        graph[u][v]['weight'] = abs(distr.rvs())

    ### Computation of the shortest paths from every observer to all other nodes
    path_lengths = nx.single_source_dijkstra_path_length(graph, observer)

    return path_lengths
