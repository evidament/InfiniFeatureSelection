import numpy as np
from benchmark import generate_data, benchmark
import sys
import logging

if __name__=="__main__":
    logging.info("Compiling activity function...")
    try:
        from activity_score import activity_score
    except ModuleNotFoundError:
        logging.warning("Writing module not compiled. Compiling...")

        from compile_writer import compile_writer
        compile_writer()
        from activity_score import activity_score
        
    logging.info("Compiled\n")
    logging.info("Calculating...")
    if sys.argv[1]=="benchmark":
        logging.root.setLevel(logging.INFO)
        logging.info("Starting benchmark")
        rows = 3000
        cols = 1000
        a = generate_data(rows, cols)
        benchmark(activity_score, (a, a), cols*(cols-1)//2)
    else:
        activity_score(a, a)
        logging.info("Calculated\n")