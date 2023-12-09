'''
Final Project - Virus Spread Containment Simulation
CISC 489-012 
Authors: Anthony Andujar, Tabetha Chubb
'''
import networkx as nx
import matplotlib.pyplot as plt
import random
import argparse

# Takes in the filename of a given network and then returns it as a 
# list of edges with each node's values
def readNetworkFile(filename):
    edges = []
    with open(filename, 'r') as file:
        for line in file:
            source, target, probability = map(float, line.split())
            edges.append((source, target, {'probability': probability}))
    return edges

# Takes in the filename of a given list of infected nodes and then returns it as 
# a set of infected nodes
def readInfectedFile(filename):
    with open(filename, 'r') as file:
        infected_nodes = [int(line) for line in file.read().splitlines()]
    return set(infected_nodes)

# Takes in a graph, list of infected nodes, spread probability, and the recovered nodes
# it checks and adds nodes to a set of newly infected nodes then combines it with the full infected node set
def virusSpreadSim(graph, infectedNodes, spreadProbability, immunizedNodes):
    newlyInfected = set()
    for node in infectedNodes:
        neighbors = set(graph.neighbors(node))
        susceptibleNeighbors = neighbors - infectedNodes - immunizedNodes
        for neighbor in susceptibleNeighbors:
            if random.random() < spreadProbability:
                newlyInfected.add(neighbor)
    return newlyInfected, infectedNodes.union(newlyInfected)

# This function detects communities in the given network and then randomly splits the B amount
# of vaccinations to B communities. After this it will immunize the selected nodes 
# and then update and return the set of nodes
def communityImmunizationSim(graph, immunizedNodes, B):
    communities = list(nx.community.greedy_modularity_communities(graph))
    nodesPerCommunity = max(1, B // len(communities))
    chosenCommunities = random.sample(communities, min(len(communities), B))
    newlyImmunizedNodes = set()
    for community in chosenCommunities:
        listOfCommunities = list(community)
        immunizeCount = min(nodesPerCommunity, len(listOfCommunities))
        newlyImmunizedNodes.update(random.sample(listOfCommunities, immunizeCount))
    immunizedNodes = immunizedNodes.union(newlyImmunizedNodes)
    return newlyImmunizedNodes, immunizedNodes

# This function simulates the function of L and M. 
# It looks to see if the nodes in the sets have an iteration count have values above M and L
# If they do then it then takes it out of the immunized or infected group and puts them in the susceptible set
# It returns the newly altered sets after the merging of the new susceptible list and recovered nodes
def infectionDynamicsSim(infectedNodes, recoveredNodes, immunizedNodes, iterationCount, M, L):
    newlySusceptibleNodes = set()
    for node in immunizedNodes.copy():
        if node in iterationCount and iterationCount[node] >= M:
            newlySusceptibleNodes.add(node)
            immunizedNodes.remove(node)
            iterationCount.pop(node, None)
    for node in infectedNodes.copy():
        if node in iterationCount and iterationCount[node] >= L:
            newlySusceptibleNodes.add(node)
            infectedNodes.remove(node)
            iterationCount.pop(node, None)
    recoveredNodes.update(newlySusceptibleNodes)
    return infectedNodes, recoveredNodes, iterationCount


# Plots the infected, susceptible, and immunized node counts on the graph
# it also handles it so there are no negative numbers
def plotSim(iterations, infectedValuess, susceptibleValues, immunizedValues):
    susceptibleValuesNN = [max(0, count) for count in susceptibleValues]
    plt.plot(iterations, infectedValuess, label='Infected Nodes')
    plt.plot(iterations, susceptibleValuesNN, label='Susceptible Nodes')
    plt.plot(iterations, immunizedValues, label='Immunized Nodes')
    plt.xlabel('Iteration Count')
    plt.ylabel('Amount of Nodes')
    plt.legend()
    plt.title('Virus Spread Containment Simulation')
    plt.show()

def main():
    # This part takes care of the different arguments that 
    # will be inputted from the command line to run the program
    parser = argparse.ArgumentParser(description='Virus Spread and Immunization Simulation')
    parser.add_argument('-networkfile', type=str, help='Network file path/name')
    parser.add_argument('-infectedfile', type=str, help='Infected file path/name')
    parser.add_argument('-T', type=int, default=500, help='Amount of iterations')
    parser.add_argument('-L', type=int, default=5, help='L')
    parser.add_argument('-M', type=int, default=10, help='M')
    parser.add_argument('-B', type=int, default=50, help='B')
    args = parser.parse_args()

    # This part reads the files into variables which are used to create graphs to be plotted
    edges = readNetworkFile(args.networkfile)
    infected_nodes = readInfectedFile(args.infectedfile)
    infectedGraph = nx.Graph()
    infectedGraph.add_edges_from(edges)

    # These are all the variables used during the simulation
    # DO NOT RENAME - It ends up giving an error with the way the dynamics sim function handles returns
    probability_of_spread = 0.1
    iterations = []
    infected_counts = []
    susceptible_counts_vsi = []
    susceptible_counts_ii = []
    immunized_counts = []
    infected_nodes_set = infected_nodes.copy()
    immunized_nodes = set()
    recovered_nodes = set()
    immunized_iteration_counter = {}

    # This loop calls all of the above functions for each VSI and II
    # It will update the infected and immunized node sets accordingly
    # to account for the changes in susceptible nodes during VSI and II 
    # it will use a slightly different equation for each
    # After all the updating is done it will print out the seperate values for each VSI and II
    for iteration in range(0, args.T):
        total_nodes = len(infectedGraph.nodes)
        # DO NOT DELETE new_infected - It causes an error with the dynamics simulator once again
        new_infected, infected_nodes_set = virusSpreadSim(infectedGraph, infected_nodes_set, probability_of_spread, immunized_nodes)
        new_immunized_nodes, immunized_nodes = communityImmunizationSim(infectedGraph, immunized_nodes, args.B)
        infected_nodes_set, recovered_nodes, immunized_iteration_counter = infectionDynamicsSim(infected_nodes_set, recovered_nodes, immunized_nodes, immunized_iteration_counter, args.M, args.L)
        iterations.append(iteration)
        infected_counts.append(len(infected_nodes_set))
        current_susceptible_vsi = max(total_nodes - len(infected_nodes_set) - len(immunized_nodes), 0)
        current_susceptible_ii = max(total_nodes - len(infected_nodes_set) - len(new_immunized_nodes), 0)
        susceptible_counts_vsi.append(current_susceptible_vsi)
        susceptible_counts_ii.append(current_susceptible_ii)
        immunized_counts.append(len(immunized_nodes))
        print(f'VSI: {len(infected_nodes_set)} {current_susceptible_vsi} {len(immunized_nodes)}')
        print(f'II: {len(infected_nodes_set)} {current_susceptible_ii} {len(immunized_nodes)}')

    plotSim(iterations, infected_counts, susceptible_counts_vsi, immunized_counts)

if __name__ == "__main__":
    main()