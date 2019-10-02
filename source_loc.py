import numpy as np
import networkx as nx
import operator

import TRBS.source_estimation as se

def trbs(graph, obs_time, distribution):

    path_lengths = {}
    paths = {}
    iso_nodes = []
    isolates = nx.isolates(graph)
    for node in list(graph.nodes()):
        if node in isolates:
            iso_nodes.append(node)
    obs = np.array(list(obs_time.keys()))
    i = 0
    print('******************** isolates ', iso_nodes)
    print('OBS', len(obs))
    print('nodes', len(list(graph.nodes())))
    for o in obs:
        path_lengths[o] = nx.single_source_dijkstra_path_length(graph, o)
        temp = []
        for l in path_lengths[o].values() :
            temp.append(len(l))
        print('path_lengths', o, ' = ', np.mean(temp))
        #print('path_lengths tab', sorted(path_lengths[o].items(), key=operator.itemgetter(0), reverse=True))
        #print('mean', np.min(path_lengths[o]))
        i = i+1
        print("current obs :", o)
    print('ITERATIONS = ', i)


    ### Run the estimation
    s_est, likelihoods = se.source_estimate(graph, obs_time, path_lengths)

    ranked = sorted(likelihoods.items(), key=operator.itemgetter(1), reverse=True)

    return (s_est, ranked)

'''
def trbs(graph, obs_time, distribution):

    path_lengths = {}
    obs = np.array(list(obs_time.keys()))
    for o in obs:
        path_lengths[o] = preprocess(o, graph, distribution)
    ### Run the estimation
    s_est, likelihoods = se.source_estimate(graph, obs_time, path_lengths)

    ranked = sorted(likelihoods.items(), key=operator.itemgetter(1), reverse=True)
    print('ranked', ranked)

    return (s_est, ranked)

def preprocess(observer, graph, distr):
    ### Initialization of the edge delay
    edges = graph.edges()
    for (u, v) in edges:
        graph[u][v]['weight'] = abs(distr.rvs())

    ### Computation of the shortest paths from every observer to all other nodes
    return  nx.single_source_dijkstra_path_length(graph, observer)
'''
