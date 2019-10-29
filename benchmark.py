import numpy as np
import itertools
import signal
import sys
import time

rows = 3000
cols = 300

def generate_data(rows, cols):
    print("\nGenerating data...")
    a = np.random.random(size=(rows, cols)).astype(np.float32)

    print("Generated data")
    print(cols*(cols-1)//2, "combinations\n")
    return a

def benchmark(func, args, iter_count=None):
    print("Running benchmark...")
    start = time.time()
    res = func(*args)
    duration = time.time()-start
    print(f"{iter_count} iters in {duration:.2f} s at {iter_count/duration:.2f} it/s")

if __name__=="__main__":
    a = generate_data(rows, cols)

    print("Compiling...")
    from utils import activity_score
    print("Compiled\n")

    benchmark(activity_score, (a, a), cols*(cols-1)//2)



