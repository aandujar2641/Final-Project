'''
Final Project - Virus Spread Containment Simulation
CISC 489-012 
Authors: Anthony Andujar, Tabetha Chubb
'''
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

network = nx.read_edgelist('networkfile.mtx', create_using=nx.Graph(), nodetype=int)
infectednodes = np.loadtxt('infectedfile.mtx', dtype=int)
