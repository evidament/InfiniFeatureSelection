import numpy as np
from benchmark import generate_data

if __name__=="__main__":
    rows = 3000
    cols = 1000
    a = generate_data(rows, cols)

    print("Compiling...")
    from utils import activity_score, activity_score_python
    print("Compiled\n")
    print("Calculating...")
    max_iqr, sp_coeff, res = activity_score(a, a)
    print("Calculated\n")

    print("Saving results...")
    save_data(max_iqr, sp_coeff, res, "test.csv")
    print("Results saved")