import argparse
import networkx as nx
import matplotlib.pyplot as plt
import random


def read_network_file(filename):
    edges = []
    with open(filename, 'r') as file:
        for line in file:
            source, target, probability = map(float, line.split())
            edges.append((source, target, {'probability': probability}))
    return edges

def read_infected_file(filename):
    with open(filename, 'r') as file:
        infected_nodes = [int(line) for line in file.read().splitlines()]
    return set(infected_nodes)

def simulate_virus_spread(graph, infected_nodes, probability_of_spread, L):
    new_infected = set()

    for node in infected_nodes:
        neighbors = set(graph.neighbors(node))
        susceptible_neighbors = neighbors - infected_nodes

        for neighbor in susceptible_neighbors:
            if random.random() < probability_of_spread:
                new_infected.add(neighbor)

    return new_infected, infected_nodes.union(new_infected)

def simulate_immunization(graph, immunized_nodes, B, M):
    nodes_list = list(set(graph.nodes) - immunized_nodes)

    # Check if B is greater than or equal to the length of nodes_list
    if B >= len(nodes_list):
        new_immunized_nodes = set(nodes_list)
    else:
        new_immunized_nodes = set(random.sample(nodes_list, B))
    
    return new_immunized_nodes, immunized_nodes.union(new_immunized_nodes)


def plot_simulation(iterations, infected_counts, susceptible_counts, immunized_counts):
    plt.plot(iterations, infected_counts, label='Infected Nodes')
    plt.plot(iterations, susceptible_counts, label='Susceptible Nodes')
    plt.plot(iterations, immunized_counts, label='Immunized Nodes')
    plt.xlabel('Iteration')
    plt.ylabel('Node Count')
    plt.legend()
    plt.title('Virus Spread and Immunization Simulation')
    plt.show()

def main():
    # Read network and infected node files
    edges = read_network_file('infectedgraph.edges')
    infected_nodes = read_infected_file('infectednodes.txt')

    # Create a graph from the network file
    G = nx.Graph()
    G.add_edges_from(edges)

    # Simulation parameters
    probability_of_spread = 0.1
    iterations = []
    infected_counts = []
    susceptible_counts = []
    immunized_counts = []

    for iteration in range(1, 500 + 1):
        # Virus Spread Iteration
        new_infected, infected_nodes = simulate_virus_spread(G, infected_nodes, probability_of_spread, 5)
        # Immunization Iteration
        immunized_nodes, infected_nodes = simulate_immunization(G, infected_nodes, 50, 10)
        # Update counts
        iterations.append(iteration)
        infected_counts.append(len(infected_nodes))
        susceptible_counts.append(len(G.nodes) - len(infected_nodes) - len(immunized_nodes))
        immunized_counts.append(len(immunized_nodes))

        # Print output for the current iteration
        print(f'VSI: {len(infected_nodes)} {len(G.nodes) - len(infected_nodes) - len(immunized_nodes)} {len(immunized_nodes)}')

    # Plot the simulation
    plot_simulation(iterations, infected_counts, susceptible_counts, immunized_counts)

if __name__ == "__main__":
    main()


