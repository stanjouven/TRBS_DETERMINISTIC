import networkx as nx
import numpy as np


def source_estimate(graph, obs_time, path_lengths):

    T = {}
    var_T = {}
    for node in list(graph.nodes()):
        T.setdefault(node, [])
        for obs in np.array(list(obs_time.keys())):
            T[node].append(obs_time[obs] - path_lengths[obs][node])
            print('T[', node, '] = ', T[node])
        var_T[node] = np.var(T[node])
        print('var T = ', var_T[node])

    min_var = np.min(list(var_T.values()))
    source_candidates = list()
    ### Finds nodes with maximum likelihood
    for src, value in var_T.items():
        if np.isclose(value, min_var, atol= 1e-08):
            source_candidates.append(src)
    print('source_candidates = ', source_candidates)
    return source_candidates, var_T
