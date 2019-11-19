#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 10:50:25 2019

@author: jonathan
"""

import numpy as np
import copy
from misc_functions import validate_adjacency_matrix as validate
from math import ceil

class graph:
    # Initializes a new computational graph with only an input node, an
    # output node, and a connection between the two
    def __init__(self):
        self.connections = np.array([[0, 1]])
        self.adjacency_matrix = np.array([[0, 1],
                                          [0, 0]])
        self.node_keys = {
                           'input' : 0,
                           'output' : 1,
                         }
        self.node_count = 2
       
    # Tries to randomly remove a connection from the graph without rendering
    # it incapable of being walked. If it can't, then it gives up
    def delete_random_connection(self):
        np.random.shuffle(self.connections)
        for i in range(self.connections.shape[0]):
            hypothetical_matrix = copy.deepcopy(self.adjacency_matrix)
            hypothetical_matrix[self.connections[i, 0], self.connections[i, 1]] = 0
            if validate(hypothetical_matrix):
                self.adjacency_matrix = hypothetical_matrix
                self.connections = np.delete(self.connections, i, axis = 0)
                return(True)
        return(False)
        
    # Randomly adds a connection that doesn't either double up on connections
    # or potentially allow for cyclic computation graphs
    def add_random_connection(self):
        arange_node = np.arange(self.node_count)
        mask = (arange_node.reshape(1, -1) > arange_node.reshape(-1, 1)) * (1 - self.adjacency_matrix)
        if mask.sum():
            shape = [1, self.node_count, self.node_count]
            coords_mask = np.concatenate([np.repeat(arange_node.reshape(-1, 1), self.node_count, axis = -1).reshape(shape),
                                          np.repeat(arange_node.reshape(1, -1), self.node_count, axis = 0).reshape(shape)])
            coords_possible = coords_mask.transpose([1, 2, 0])[mask == 1]
            coords = coords_possible[np.random.randint(coords_possible.shape[0])]
            self.connections = np.concatenate([self.connections, coords.reshape(1, 2)])
            self.adjacency_matrix[coords[0], coords[1]] = 1
            return(True)
        return(False)
      
    # Adds a new node to a computation graph by splitting an existing connection
    # in half, and putting a node in the center
    def add_random_node(self, name):
        split_index = np.random.randint(self.connections.shape[0])
        new_pos = ceil(self.connections[split_index].mean())
        self.node_count += 1
        for i in self.node_keys:
            self.node_keys[i] += self.node_keys[i] >= new_pos
        self.connections[self.connections >= new_pos] += 1
        self.node_keys[name] = new_pos
        self.adjacency_matrix = np.insert(np.insert(self.adjacency_matrix, new_pos, 0, axis = 1), new_pos, 0, axis = 0)
        old_connection = self.connections[split_index]
        new_connection_in = copy.deepcopy(old_connection)
        new_connection_out = copy.deepcopy(old_connection)
        new_connection_in[1] = new_pos
        new_connection_out[0] = new_pos
        self.connections = np.delete(self.connections, split_index, axis = 0)
        self.connections = np.concatenate([self.connections, new_connection_in.reshape(1, 2), new_connection_out.reshape(1, 2)])
        temp = [old_connection, new_connection_in, new_connection_out]
        for i in range(3):
            self.adjacency_matrix[temp[i][0], temp[i][1]] = float(i > 0)
        
        