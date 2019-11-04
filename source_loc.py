import numpy as np
import networkx as nx
import operator

import TRBS_DETERMINISTIC.source_estimation as se

'''
Enables to call functions to find the source estimation of the algorithm
PARAMETERS:
    graph: the nx graph used
    obs_time: dictionnary node -> time of the infection
    distribution: distribution used
'''
def trbs_deterministic(graph, obs_time_filt, distribution):

    #print('obs time', obs_time_filt)

    #largest_graph_cc = graph.subgraph(max(nx.connected_components(graph), key=len))
    #obs_time_filt = observer_filtering(obs_time, largest_graph_cc)
    obs_filt = np.array(list(obs_time_filt.keys()))
    path_lengths = {}

    for o in obs_filt:
        path_lengths[o] = preprocess(o, graph, distribution)
        #print('path_lengths', o, '= ', path_lengths[o])

    ### Run the estimation
    s_est, likelihoods = se.source_estimate(graph, obs_time_filt, path_lengths)
    ranked = sorted(likelihoods.items(), key=operator.itemgetter(1), reverse=False)

    return (s_est, ranked)

'''
Apply the given distribution to the edge of the graph.
PARAMETERS:
    observer: the observer node
    graph: the nx graph used
    distr: the distribution used
Return dictionnary: node -> time to go from that node to the given observer
'''
def preprocess(observer, graph, distr):
    ### Initialization of the edge delay
    edges = graph.edges()
    for (u, v) in edges:
        graph[u][v]['weight'] = abs(distr.rvs())
        #print('u: ',u, 'v: ', v, graph[u][v]['weight'])

    ### Computation of the shortest paths from every observer to all other nodes
    return  nx.single_source_dijkstra_path_length(graph, observer)

'''
 Check if every observer is part of the largest graph component
 PARAMETERS:
    OBS_TIME: dictionnary: node -> time of infection
    LARGEST_GRAPH_CC: largest component of the graph
 RETURN
    the obs_time dictionnary without the ones that are not part of largest_graph_cc
'''
def observer_filtering(obs_time, largest_graph_cc):
    obs = np.array(list(obs_time.keys()))
    for o in obs:
        if not largest_graph_cc.has_node(o):
            obs_time.delete(o)
    return obs_time
