import networkx as nx
import matplotlib.pyplot as plt
# Define the DFA
dfa = {
    'q0': {'a': 'q6', 'b': 'q1'},
    'q1': {'a': 'q2', 'b': 'q4'},
    'q2': {'a': 'q5', 'b': 'q3'},
    'q3': {'a': 'q8', 'b': 'q3'},
    'q4': {'a': 'q6', 'b': 'q8'},
    'q5': {'a': 'q2', 'b': 'q3'},
    'q6': {'a': 'q4', 'b': 'q7'},
    'q7': {'a': 'q8', 'b': 'q7'},
    'q8': {'a': 'q7', 'b': 'q4'},
    'q9': {'a': 'q10', 'b': 'q8'},
    'q10': {'a': 'q3', 'b': 'q9'},
}

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
