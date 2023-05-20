import networkx as nx
import matplotlib.pyplot as plt
# Define the DFA

transitions = {
    'p3': {'b': 'p3', 'a': 'p3'},
    'p1': {'b': 'p2', 'a': 'p1'},
    'p5': {'b': 'p2', 'a': 'p1'},
    'p2': {'b': 'p3', 'a': 'p4p0'},
    'p4p0': {'b': 'p4p0', 'a': 'p4p0'}}

# Create a directed graph
graph = nx.DiGraph()

# Add states as nodes
graph.add_nodes_from(dfa.keys())

# Add transitions as edges
for state, transitions in dfa.items():
    for symbol, next_state in transitions.items():
        graph.add_edge(state, next_state, label=symbol)

# Set layout for better visualization
pos = nx.spring_layout(graph)

# Draw nodes, edges, and labels
nx.draw_networkx_nodes(graph, pos)
nx.draw_networkx_edges(graph, pos)
nx.draw_networkx_labels(graph, pos)

# Add edge labels
edge_labels = {(n1, n2): d['label'] for n1, n2, d in graph.edges(data=True)}
nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

# Show the plot
plt.axis('off')
plt.show()
