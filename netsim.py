import argparse
import networkx as nx
import matplotlib.pyplot as plt
import random


def read_network_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        edges = [tuple(map(float, line.split(" "))) for line in lines]
    return edges

def read_infected_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        infected_nodes = [float(line) for line in lines]
    return infected_nodes

def simulate_virus_spread(graph, infected_nodes, probability_of_spread, L):
    new_infected = set()

<<<<<<< HEAD
    for node in infected_nodes:
        neighbors = set(graph.neighbors(node))
        susceptible_neighbors = neighbors - infected_nodes
=======
def main(network_file, infected_file, T, L, M, B):
    # Read input files
    network = readNetworkFile(network_file)
    initial_infected_nodes = readInfectedFile(infected_file)
>>>>>>> c08c61b8b7878739c78f71b9da76f37b44e3b0f9

        for neighbor in susceptible_neighbors:
            if random.random() < probability_of_spread:
                new_infected.add(neighbor)

    return new_infected, infected_nodes

def simulate_immunization(graph, immunized_nodes, B, M):
    immunized_nodes = set(random.sample(set(graph.nodes) - immunized_nodes, B))
    return immunized_nodes, immunized_nodes

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
    '''
    parser = argparse.ArgumentParser(description='Virus Spread and Containment Simulation')
    parser.add_argument('-networkfile', type=str, default='infectedgraph.edges', help='Path to the network file')
    parser.add_argument('-infectedfile', type=str, default='infectednodes.txt', help='Path to the infected nodes file')
    #parser.add_argument('-T', type=int, required=True, help='Total number of iteration pairs')
    #parser.add_argument('-L', type=int, required=True, help='Duration of infection for each node')
    #parser.add_argument('-M', type=int, required=True, help='Duration of immunization for each node')
    #parser.add_argument('-B', type=int, required=True, help='Number of antivirus shots for immunization')
    args = parser.parse_args()
'''
    # Read network and infected node files
    edges = read_network_file("infectedgraph.edges")
    #args.networkfile
    infected_nodes = read_infected_file("infectednodes.txt")
    #args.infectedfile

    # Create a graph from the network file
    G = nx.Graph()
    G.add_edges_from(edges)

    # Simulation parameters
    probability_of_spread = 0.1
    iterations = []
    infected_counts = []
    susceptible_counts = []
    immunized_counts = []

    #(1, args.T + 1)
    for iteration in range(1, 500 + 1):
        # Virus Spread Iteration
        new_infected, infected_nodes = simulate_virus_spread(G, infected_nodes, probability_of_spread, 5)
        #args.L
        # Immunization Iteration
        immunized_nodes, immunized_nodes = simulate_immunization(G, immunized_nodes, 50, 10)
        #args.B, args.M
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

