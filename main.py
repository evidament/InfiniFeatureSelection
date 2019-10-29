import numpy as np
from benchmark import generate_data, benchmark
import sys
import logging

if __name__=="__main__":
    logging.info("Compiling...")
    try:
        from utils import activity_score
    except ModuleNotFoundError:
        logging.critical("Writing module not compiled. Run `python compile_writer.py` first")
        sys.exit(-1)
        
    logging.info("Compiled\n")
    logging.info("Calculating...")
    if sys.argv[1]=="benchmark":
        rows = 3000
        cols = 2000
        a = generate_data(rows, cols)
        benchmark(activity_score, (a, a), cols*(cols-1)//2)
    else:
        activity_score(a, a)
        logging.info("Calculated\n")