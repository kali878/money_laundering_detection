# src/graph_analysis.py

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def build_transaction_graph(transactions: pd.DataFrame):
    G = nx.DiGraph()
    for _, row in transactions.iterrows():
        G.add_edge(
            row['from_account'],
            row['to_account'],
            weight=row['amount'],
            timestamp=row['timestamp']
        )
    return G

def plot_transaction_graph(G):
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, k=0.3, iterations=20)
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]

    nx.draw_networkx_nodes(G, pos, node_size=600, node_color="skyblue")
    nx.draw_networkx_edges(G, pos, width=[w/1000 for w in edge_weights], alpha=0.6, arrows=True)
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

    plt.title("Transaction Network Graph", fontsize=14)
    plt.axis("off")
    plt.show()


def calculate_graph_features(G):
    features = {
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "density": nx.density(G),
        "avg_clustering": nx.average_clustering(G.to_undirected()),
        "degree_centrality": nx.degree_centrality(G),
        "betweenness_centrality": nx.betweenness_centrality(G),
    }
    return features
