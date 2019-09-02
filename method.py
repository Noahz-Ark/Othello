# import numpy as np
# import random
# import time
# import sys
# import socket
# import threading

def int2tuple(n):
    (i,j) = (n//10, n%10)
    return (i,j)

def tuple2int(t):
    (i,j) = t
    n = i * 10 + j
    return n

def decode_result(n):
    wel = n // 10000
    (b,w) = ((n//100)%100, n%100)
    return (wel, b, w)

def encode_result(t):
    n = t[0] * 10000 + t[1] * 100 + t[2]
    return n