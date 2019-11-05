import numpy as np
import networkx as nx
import operator

import TRBS_DETERMINISTIC.source_estimation as se

'''
Enables to call functions to find the source estimation of the algorithm
PARAMETERS:
    graph: the nx graph used
    obs_time: dictionnary {node: time of the infection}
    distribution: distribution used
RETURN:
    s_est: estimation of the true source
    ranked: sorted(in decreasing order) list of tuple (node, value in which we do the estimation)
'''
def trbs_deterministic(graph, obs_time_filt, distribution):

    obs_filt = np.array(list(obs_time_filt.keys()))
    path_lengths = {}

    ### Computation of the shortest paths from every observer to all other nodes
    for o in obs_filt:
        path_lengths[o] = nx.single_source_dijkstra_path_length(graph, o)

    ### Run the estimation
    s_est, likelihoods = se.source_estimate(graph, obs_time_filt, path_lengths, distribution.mean())
    ranked = sorted(likelihoods.items(), key=operator.itemgetter(1), reverse=False)

    return (s_est, ranked)
