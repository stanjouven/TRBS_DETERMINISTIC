import numpy as np
import networkx as nx
import operator

import TRBS.source_estimation as se

'''
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
        #print('path_lengths', o, ' = ', np.mean(list(path_lengths[o].values())))
        #print('path_lengths tab', sorted(path_lengths[o].items(), key=operator.itemgetter(0), reverse=True))
        #print('mean', np.min(path_lengths[o]))
        i = i+1
        print('path_lengths', o, ' = ', len(path_lengths[o]))
        print('path_lengths tab', sorted(path_lengths[o].items(), key=operator.itemgetter(0), reverse=True))
        #print('mean', np.min(path_lengths[o]))
        print("current obs :", o)
    print('ITERATIONS = ', i)


    ### Run the estimation
    s_est, likelihoods = se.source_estimate(graph, obs_time, path_lengths)

    ranked = sorted(likelihoods.items(), key=operator.itemgetter(1), reverse=True)

    return (s_est, ranked)
'''

def trbs(graph, obs_time, distribution):

    largest_graph_cc = graph.subgraph(max(nx.connected_components(graph), key=len))
    obs_time_filt = observer_filtering(obs_time, largest_graph_cc)
    obs_filt = np.array(list(obs_time.keys()))
    path_lengths = {}
    print("graph component", list(largest_graph_cc.nodes()))
    print("LENGTH COMPONENET", len(list(largest_graph_cc.nodes())))
    print("obs time", list(obs_time.keys()))
    print("obs time filt", obs_filt)

    for o in obs_filt:
        path_lengths[o] = preprocess(o, largest_graph_cc, distribution)
    ### Run the estimation
    s_est, likelihoods = se.source_estimate(largest_graph_cc, obs_time_filt, path_lengths)

    ranked = sorted(likelihoods.items(), key=operator.itemgetter(1), reverse=True)
    print('ranked', ranked)

    return (s_est, ranked)

'''
Apply the given distribution to the edge of the graph.
Return dictionnary: node -> time to go from that node to the given observer
'''
def preprocess(observer, graph, distr):
    ### Initialization of the edge delay
    edges = graph.edges()
    for (u, v) in edges:
        graph[u][v]['weight'] = abs(distr.rvs())

    ### Computation of the shortest paths from every observer to all other nodes
    return  nx.single_source_dijkstra_path_length(graph, observer)

'''
 Check if every observer is part of the largest graph component
 OBS_TIME: dictionnary: node -> time of infection
 LARGEST_GRAPH_CC: largest component of the graph
 RETURN the obs_time dictionnary without the ones that are not part of largest_graph_cc
'''
def observer_filtering(obs_time, largest_graph_cc):
    obs = np.array(list(obs_time.keys()))
    for o in obs:
        if not largest_graph_cc.has_node(o):
            obs_time.delete(o)
    return obs_time
