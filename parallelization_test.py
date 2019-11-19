#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 18:56:36 2019

@author: jonathan
"""

try:
    import torch
    import torch.multiprocessing as mp
except:
    pass
import time
import numpy as np

class Model(torch.nn.Module):
    def __init__(self, use_half = True):
        super(Model, self).__init__()
        
        self.half = use_half
        
        self.network = torch.nn.Sequential(
                torch.nn.Linear(50, 64),
                torch.nn.ReLU(),
                torch.nn.Linear(64, 64),
                torch.nn.ReLU(),
                torch.nn.Linear(64, 64),
                torch.nn.ReLU(),
                torch.nn.Linear(64, 64),
                torch.nn.ReLU(),
                torch.nn.Linear(64, 64),
                torch.nn.ReLU(),
                torch.nn.Linear(64, 64),
                torch.nn.ReLU(),
                torch.nn.Linear(64, 64),
                torch.nn.ReLU(),
                torch.nn.Linear(64, 64),
                torch.nn.ReLU(),
                torch.nn.Linear(64, 64),
                torch.nn.ReLU(),
                torch.nn.Linear(64, 64),
                torch.nn.ReLU(),
                torch.nn.Linear(64, 8)).to('cuda')
        
        if self.half:
            self.network = self.network.half()
        
    def forward(self, x):
        return(self.network(x))
        
class data:
    def __init__(self):
        self.x = torch.randn([500, 50], device = 'cuda')        

X_ = data()

num_models = 100

models = [Model(False) for i in range(num_models)]

def apply(model, x):
    out = np.array([model.forward(x.x).detach().sum() for i in range(1000)]).sum()
    return(out)
    
if __name__ == '__main__':
    try:
        mp.set_start_method('spawn')
    except:
        pass
    
    parallel_start = time.time()
    
    with mp.Pool(processes = 5) as pool:
        a = pool.starmap(apply, [(i, X_) for i in models])
    
    parallel_end = time.time()
    '''
    serial_start = time.time()
    b = [apply(i, X_) for i in models]
    serial_end = time.time()
    '''
    print(parallel_end - parallel_start)#, serial_end - serial_start)