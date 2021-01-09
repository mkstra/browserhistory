import os
import pandas as pd
from itertools import product
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--dir", help="directory with csv to merge")

def merge_csv_in_dir(dir_path):
    for dirpath, _, fnames in os.walk(dir_path):
        fpaths = (["/".join(t) for t in [*product([dirpath], fnames)]])
        dfs = [pd.read_csv(fpath) for fpath in fpaths]
        
        print(dfs[0].columns)
        pd.concat(dfs).to_csv("merged.csv", index = False, header=True)
        

if __name__ == "__main__":
    args = parser.parse_args()
    merge_csv_in_dir(args.dir)

