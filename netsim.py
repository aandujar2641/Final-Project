'''
Final Project - Virus Spread Containment Simulation
CISC 489-012 
Authors: Anthony Andujar, Tabetha Chubb
'''
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

def simulate_virus_spread(graph, infected_nodes, probability_of_spread, L, recovered_nodes):
    new_infected = set()

    for node in infected_nodes:
        neighbors = set(graph.neighbors(node))
        susceptible_neighbors = neighbors - infected_nodes - recovered_nodes

        for neighbor in susceptible_neighbors:
            if random.random() < probability_of_spread:
                new_infected.add(neighbor)

    return new_infected, infected_nodes.union(new_infected)

def simulate_immunization_community(graph, immunized_nodes, B, M):
    communities = list(nx.community.greedy_modularity_communities(graph))
    
    # Exclude already immunized nodes from communities
    remaining_communities = [community - immunized_nodes for community in communities]
    
    immunized_communities = random.sample(remaining_communities, min(len(remaining_communities), B))

    # Flatten the selected communities and take the first M nodes
    new_immunized_nodes = set(node for community in immunized_communities for node in list(community)[:M])
    return new_immunized_nodes, immunized_nodes.union(new_immunized_nodes)

def simulate_infection_dynamics(infected_nodes, recovered_nodes, M):
    # Nodes that lost immunization are susceptible to reinfection
    lost_immunization_nodes = recovered_nodes.intersection(infected_nodes)
    # Ensure that the number of nodes to be reinfected does not exceed the total infected nodes
    num_reinfected = min(len(lost_immunization_nodes), M)
    new_infected = random.sample(list(lost_immunization_nodes), num_reinfected)
    
    recovered_nodes.difference_update(new_infected)
    infected_nodes.update(new_infected)
    
    return infected_nodes, recovered_nodes

def plot_simulation(iterations, infected_counts, susceptible_counts, immunized_counts):
    susceptible_counts_non_negative = [max(0, count) for count in susceptible_counts]
    plt.plot(iterations, infected_counts, label='Infected Nodes')
    plt.plot(iterations, susceptible_counts_non_negative, label='Susceptible Nodes')
    plt.plot(iterations, immunized_counts, label='Immunized Nodes')
    plt.xlabel('Iteration')
    plt.ylabel('Node Count')
    plt.legend()
    plt.title('Virus Spread and Immunization Simulation')
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Virus Spread and Immunization Simulation')
    parser.add_argument('-networkfile', type=str, help='Network file path')
    parser.add_argument('-infectedfile', type=str, help='Infected file path')
    parser.add_argument('-T', type=int, default=500, help='Number of iterations')
    parser.add_argument('-L', type=int, default=5, help='Parameter L')
    parser.add_argument('-M', type=int, default=10, help='Parameter M')
    parser.add_argument('-B', type=int, default=50, help='Parameter B')

    args = parser.parse_args()

    # Read network and infected node files
    edges = read_network_file(args.networkfile)
    infected_nodes = read_infected_file(args.infectedfile)

    # Create a graph from the network file
    G = nx.Graph()
    G.add_edges_from(edges)

    # Simulation parameters
    probability_of_spread = 0.1
    iterations = []
    infected_counts = []
    susceptible_counts = []
    immunized_counts = []
    infected_nodes_set = infected_nodes.copy()
    immunized_nodes = set()
    recovered_nodes = set()

    for iteration in range(1, args.T + 1):
        # Virus Spread Iteration
        new_infected, infected_nodes_set = simulate_virus_spread(G, infected_nodes_set, probability_of_spread, args.L, recovered_nodes)
        # Immunization Iteration
        new_immunized_nodes, immunized_nodes = simulate_immunization_community(G, immunized_nodes, args.B, args.M)
        # Infection Dynamics
        infected_nodes_set, recovered_nodes = simulate_infection_dynamics(infected_nodes_set, recovered_nodes, args.M)

        # Update counts
        iterations.append(iteration)
        infected_counts.append(len(infected_nodes_set))
        susceptible_counts.append(len(G.nodes) - len(infected_nodes_set) - len(immunized_nodes))
        immunized_counts.append(len(immunized_nodes))

        # Print output for the current iteration
        print(f'VSI: {len(infected_nodes_set)} {max(len(G.nodes) - len(infected_nodes_set) - len(immunized_nodes), 0)} {len(immunized_nodes)}')
        print(f'II: {len(new_immunized_nodes)} {max(len(G.nodes) - len(infected_nodes_set) - len(new_immunized_nodes), 0)} {len(immunized_nodes)}')

    # Plot the simulation
    plot_simulation(iterations, infected_counts, susceptible_counts, immunized_counts)

if __name__ == "__main__":
    main()
