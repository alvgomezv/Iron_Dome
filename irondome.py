#!/goinfre/alvgomez/miniconda3/envs/42cyber-alvgomez/bin/python

import argparse
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description="Program that detects anomalous activity inside a critical zone")
    parser.add_argument("args", nargs='*')
    arg = parser.parse_args()
    return arg

if __name__ == "__main__":
    args = parse_arguments()
