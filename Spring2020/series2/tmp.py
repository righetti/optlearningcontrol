#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 22:03:08 2020

@author: y56
"""
import numpy as np
from numpy.linalg import matrix_rank


one=np.identity(5) * 0.1

print(one)
a=np.array([[2],[2],[float('inf')],[2],[2]])
print(a)
c=np.matmul(one,a)
print(c)
