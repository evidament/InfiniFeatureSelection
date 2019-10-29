import numpy as np
import itertools
import signal
import sys
import time
import logging

# rows = 3000
# cols = 300

def generate_data(rows, cols):
    logging.info("Generating data...")
    a = np.random.random(size=(rows, cols)).astype(np.float32)

    logging.info("Generated data")
    logging.info(f"{cols*(cols-1)//2} combinations")
    return a

def benchmark(func, args, iter_count=None):
    logging.info("Running benchmark...")
    start = time.time()
    res = func(*args)
    duration = time.time()-start
    logging.info(f"{iter_count} iters in {duration:.2f} s at {iter_count/duration:.2f} it/s")

if __name__=="__main__":
    a = generate_data(rows, cols)

    logging.info("Compiling...")
    from activity_score import activity_score
    logging.info("Compiled\n")

    benchmark(activity_score, (a, a), cols*(cols-1)//2)



