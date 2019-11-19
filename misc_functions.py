#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 13:23:01 2019

@author: jonathan
"""

import numpy as np
import copy
import datetime

def validate_adjacency_matrix(adj_mat):
    # Checks whether or not an adjancency matrix for a NEAT topology can 
    # produce a network where input eventually reaches the output.
    # Adjacency matrix is formatted like this:
    #
    #                      O
    #            I         u
    #            n 1 2 . n t
    #          ┌             ┐
    #      In  │ 0 c c . c c │
    #      1   │ 0 0 c . c c │
    # A =  2   │ 0 0 0 . c c │
    #      .   │ . . . . . . │
    #      n   │ 0 0 0 . 0 c │
    #      Out │ 0 0 0 . 0 0 │
    #          └             ┘
    # Where a c occupying position [i, j] represents a possible connection 
    # from node i to node j. By repeatedly multiplying the matrix by itself,
    # it can determine the existence of paths from the input to the output 
    # node.
    # Also checks to make sure that every node has at least one inputs and
    # one output.
    if (adj_mat[:, 1:].sum(0).min() > 0) and (adj_mat[:-1, :].sum(1).min() > 0):
        new_mat = copy.deepcopy(adj_mat)
        for i in range(adj_mat.shape[0] - 1):
            if new_mat[0, -1]:
                return(True)
            if not(new_mat.sum()):
                return(False)
            new_mat = np.matmul(adj_mat, new_mat)
    return(False)
    
def estimated_completion_clock_time(est_seconds_remaining):
    # Uses the number of seconds remaining to determine the time of day that
    # the algorithm will cease running.
    est_finish = datetime.datetime.now() + datetime.timedelta(seconds = est_seconds_remaining)
    est_finish = est_finish.replace(microsecond=0)
    est_finish = str(est_finish.time())
    return(est_finish)
    
def prepare_float(num, width = 10, decimals = 2):
    # Converts a floating point number to a right-justified string of constant
    # width, rounded to a given decimal's place
    string = ('{:.'+str(decimals)+'f}').format(num).rjust(width)
    return(string)