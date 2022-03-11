from random import *

from math import *

# ____for drawing the graph.____
import networkx as nx
import matplotlib.pyplot as plt

# a function for conveniently calculating distance between nodes (lines would otherwise be very long)
def distn(i, j):
    N = T.nodes
    return sqrt((N[i][0] - N[j][0]) ** 2 + (N[i][1] - N[j][1]) ** 2)

K = nx.Graph()

class top_map:
    def __init__(self):
        self.nodes = []
        self.sensors = []
        self.inshadow = set()
        
    def generate_random(self, n_nodes, minxy, maxxy, n_sensors, shad_pos, shad_dir):
        self.nodes = []
        self.sensors = []
        self.inshadow = set()
        for i in range(n_sensors):
            self.sensors.append(randint(0, n_nodes-1))
        for i in range(n_nodes):
            self.nodes.append( (uniform(minxy, maxxy), uniform(minxy,maxxy) ))
            if (self.nodes[i][0] - shad_pos[0])*shad_dir[0] + (self.nodes[i][1] - shad_pos[1])*shad_dir[1] > 0:
                self.inshadow.add(i)
            #print(self.nodes[i])

    def generate_even(self, dist, minxy, maxxy, sensors, shad_pos, shad_dir):
        self.nodes = []
        self.sensors = []
        self.inshadow = set()
        x = minxy[0]
        while x <= maxxy[0]:
            y = minxy[1]+(x%(dist*2))/2
            while y <= maxxy[1]:
                if (x - shad_pos[0]) * shad_dir[0] + (y - shad_pos[1]) * shad_dir[1] > 0:
                    self.inshadow.add(len(self.nodes))
                self.nodes.append((x, y))
                y += dist
            x += dist
        for s in sensors:
            mindis = float('inf')
            minind = -1
            i = 0
            for n in self.nodes:
                dis = (s[0]-n[0])**2 + (s[1]-n[1])**2
                if dis < mindis:
                    mindis = dis
                    minind = i
                i += 1
            self.sensors.append(minind)


    """"
    def to_graph(self):
        G = dict()
        N = self.nodes
        for i in range(len(N)):
            G[i] = dict()
            for j in range(len(N)):
                if i != j:
                        #K.add_edge(i, j, color='gray', weight=0.1)
                    G[i][j] = sqrt((N[i][0]-N[j][0])**2 + (N[i][1]-N[j][1])**2)

                    # print(G[i][j])
        return G
    """
    def to_graph(self, edges):
        G = dict()
        N = self.nodes
        for e in edges:
            if e[0] not in G.keys():
                G[e[0]] = dict()
            if e[1] not in G.keys():
                G[e[1]] = dict()
            G[e[0]][e[1]] = sqrt((N[e[0]][0]-N[e[1]][0])**2 + (N[e[0]][1]-N[e[1]][1])**2)
            G[e[1]][e[0]] = sqrt((N[e[0]][0] - N[e[1]][0]) ** 2 + (N[e[0]][1] - N[e[1]][1]) ** 2)
        return G



""""
for i in range(20):
    for j in range(20):
        N = T.nodes
        if j in G[i] and random() > (8192 / ((N[i][0] - N[j][0]) ** 2 + (N[i][1] - N[j][1]) ** 2))**6:
            G[i].pop(j)
            G[j].pop(i)
"""
from voronoi import *


min_xy = 0  # minimum range of x,y
max_xy = 256   # maximum range of x,y

# given_nodes = [(random.uniform(min_xy, max_xy), random.uniform(min_xy, max_xy)) for i in range(10)]
T = top_map()
sensors = []

import json
with open('MSG.txt') as f:
    jdata = json.load(f)

#print(obsmap)

for i in range(4):
    sensors.append((random.uniform(min_xy, max_xy), random.uniform(min_xy, max_xy)))
# T.generate_random(20, min_xy, max_xy, 4, (180, 128), (1, -1))   # (number of nodes, min_xy, max_xy, number of sensors)
T.generate_even(32, (0, 0), (256, 256), sensors, (128, 128), (1, -1))
print(T.nodes)
print(T.inshadow)
print(T.sensors)
given_nodes = T.nodes
import traceback
try:
    E = get_edges_for_graph(given_nodes)
    print(E)
    i = 0
    while i < len(E):
        e = E[i]
        obsxind = math.floor(T.nodes[e[0]][0] / 256 * (len(jdata["obstacleMap"]) - 1))
        obsyind = math.floor(T.nodes[e[0]][1] / 256 * (len(jdata["obstacleMap"]) - 1))
        if jdata["obstacleMap"][obsxind][obsyind] != 0:
            E.remove(e)
        else:
            obsxind = math.floor(T.nodes[e[1]][0] / 256 * (len(jdata["obstacleMap"]) - 1))
            obsyind = math.floor(T.nodes[e[1]][1] / 256 * (len(jdata["obstacleMap"]) - 1))
            if jdata["obstacleMap"][obsxind][obsyind] != 0:
                E.remove(e)
            else:
                i += 1
    G = T.to_graph(E)
    visualise_voronoi(given_nodes, E)
except BaseException as e:
    print(traceback.format_exc())
    print("Error:", e)

