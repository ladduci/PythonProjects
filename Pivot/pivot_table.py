import pandas as pd
import numpy as np
import argparse
import os
import glob


parser = argparse.ArgumentParser(description="Build a Pivot table from Input data files")
parser.add_argument("inputDir",metavar="Dir", help="Input Directory") #all files in this dir will be read and concatenated in one data frame then used to build the pivot table
parser.add_argument("Index1",metavar="Index1", help="Column to use as first Index") #first parameter we want to build the pivot table on
parser.add_argument("Index2",metavar="Index2", help="Column to use as second Index") #second parameter we want to build the pivot table on
args = parser.parse_args()
path = args.inputDir



all_files = glob.glob(os.path.join(path, "*.csv"))  # os.path.join makes concatenation OS independent
all_data = pd.DataFrame()
for f in all_files:
    df = pd.read_csv(f,';')
    all_data = all_data.append(df,ignore_index=True)

FirstParam = all_data.columns[args.Index1]
SecondParam = all_data.columns[args.Index2]
pd.pivot_table(all_data,index=["FirstParam"])
  
pd.pivot_table(all_data,index=["FirstParam","SecondParam"])
pd.pivot_table(all_data,index=["FirstParam","SecondParam"],aggfunc=np.sum)
