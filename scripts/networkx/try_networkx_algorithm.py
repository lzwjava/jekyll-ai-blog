import networkx as nx

# Create a graph
G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (3, 5), (4, 6), (5, 6)])

# Find all simple paths between two nodes
print("All paths from 1 to 6:", list(nx.all_simple_paths(G, 1, 6)))

# Minimum spanning tree
T = nx.minimum_spanning_tree(G)
print("Edges in MST:", T.edges())

# Community detection (requires python-louvain package)
# pip install python-louvain
try:
    import community as community_louvain

    partition = community_louvain.best_partition(G)
    print("Community partition:", partition)
except ImportError:
    print("Install python-louvain for community detection")
