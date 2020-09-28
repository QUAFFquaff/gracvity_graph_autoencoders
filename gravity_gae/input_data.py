import networkx as nx
import scipy.sparse as sp
import numpy as np

from gravity_gae import make_data


def load_data(dataset):
    """ Load datasets from text files

    :param dataset: 'cora', 'citeseer' or 'google' graph dataset.
    :return: n*n sparse adjacency matrix and n*f node-level feature matrix

    Note: in this paper, all three datasets are assumed to be featureless.
    As a consequence, the feature matrix is the identity matrix I_n.
    """
    if dataset == 'cora':
        adj = nx.adjacency_matrix(nx.read_edgelist("../data/cora.cites",
                                                   delimiter='\t',
                                                   create_using=nx.DiGraph()))
        # Transpose the adjacency matrix, as Cora raw dataset comes with a
        # <ID of cited paper> <ID of citing paper> edgelist format.
        adj = adj.T

        features = sp.identity(adj.shape[0])

    elif dataset == 'citeseer':
        adj = nx.adjacency_matrix(nx.read_edgelist("../data/citeseer.cites",
                                                   delimiter='\t',
                                                   create_using=nx.DiGraph()))
        # Transpose the adjacency matrix, as Citeseer raw dataset comes with a
        # <ID of cited paper> <ID of citing paper> edgelist format.
        adj = adj.T
        features = sp.identity(adj.shape[0])

    elif dataset == 'google':
        adj = nx.adjacency_matrix(nx.read_edgelist("../data/GoogleNw.txt",
                                                   delimiter='\t',
                                                   create_using=nx.DiGraph()))
        features = sp.identity(adj.shape[0])
    elif dataset == 'mydata':

        graph,features, feature_arr = make_data.get_data()

        adj = nx.adjacency_matrix(nx.from_dict_of_lists(graph))
        if np.array_equal(adj,adj.T):
            print("symmetric")
        else:
            print('not symmetric')
        # np.savetxt('adj.txt', adj,fmt="%d")
        # features = sp.identity(adj.shape[0])
        # features = sp.identity(feature)

        # print(features-features1)
        return adj, features, graph, feature_arr

    else:
        raise ValueError('Undefined dataset!')
    return adj, features