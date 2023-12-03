'''
Final Project - Virus Spread Containment Simulation
CISC 489-012 
Authors: Anthony Andujar, Tabetha Chubb
'''
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import argparse
import networkx as nx
import matplotlib.pyplot as plt

# Reads the network file into a graph variable
def readNetworkFile(network):
    graph = nx.Graph()
    with open(network, 'r') as file:
        for line in file:
            source, target, probability = map(float, line.split())
            graph.add_edge(int(source), int(target), probability=probability)
    return graph

# Reads the infected nodes file into a variable
def readInfectedFile(infectedFile):
    with open(infectedFile, 'r') as file:
        infectedNodes = {int(line.strip()) for line in file}
    return infectedNodes

def virus_spread_iteration(graph, infected_nodes, L):
    # Implement virus spread iteration
    pass

def immunization_iteration(graph, B, M):
    # Implement immunization iteration
    pass

def main(network_file, infected_file, T, L, M, B):
    # Read input files
    network = read_network_file(network_file)
    initial_infected_nodes = read_infected_file(infected_file)

    # Initialize graph and infected nodes
    graph = nx.Graph(network)
    infected_nodes = set(initial_infected_nodes)

    # Simulation loop
    for iteration in range(1, T + 1):
        if iteration % 2 == 1:
            # Virus Spread Iteration
            infected_nodes = virus_spread_iteration(graph, infected_nodes, L)
        else:
            # Immunization Iteration
            immunization_iteration(graph, B, M)

        # Output current status
        #print(f"{['VSI', 'II'][iteration % 2 - 1]}: {len(infected_nodes)} {len(graph.nodes) - len(infected_nodes)} {len(immunized_nodes)}")

    # Generate and save the plot
    # Implement code for plotting

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Virus Spread Containment Simulation")
    parser.add_argument("-networkfile", type=str, help="Path to the network configuration file")
    parser.add_argument("-infectedfile", type=str, help="Path to the initial infected nodes file")
    parser.add_argument("-T", type=int, help="Total number of iteration pairs")
    parser.add_argument("-L", type=int, help="Infection duration")
    parser.add_argument("-M", type=int, help="Immunization duration")
    parser.add_argument("-B", type=int, help="Number of antivirus shots")
    
    args = parser.parse_args()
    main(args.networkfile, args.infectedfile, args.T, args.L, args.M, args.B)
