import pandas as pd
import numpy as np
import argparse
import logging
import os
import glob


parser = argparse.ArgumentParser(description="Build a Pivot table from Input csv data files")
parser.add_argument("inputDir",metavar="Dir", help="Input Directory") #all files in this dir will be read and concatenated in one data frame then used to build the pivot table
parser.add_argument("Index1",metavar="Index1", help="Column to use as first Index") #first parameter we want to build the pivot table on
parser.add_argument("Index2",metavar="Index2", help="Column to use as second Index") #second parameter we want to build the pivot table on
args = parser.parse_args()
path = args.inputDir

# create logger with 'pivot_table'
logger = logging.getLogger('pivot_table')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('pivot.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info("The script to create a Pivot Table is now running")


all_files = glob.glob(os.path.join(path, "*.csv"))  # os.path.join makes concatenation OS independent
all_data = pd.DataFrame()
for f in all_files:
    df = pd.read_csv(f,';')
    all_data = all_data.append(df,ignore_index=True)
logger.info(f + " csv files have been found	")

FirstParam = all_data.columns[args.Index1]
SecondParam = all_data.columns[args.Index2]
logger.info("Here the first Pivot Table based on the first parameter")
pivot1 = pd.pivot_table(all_data,index=["FirstParam"])
  
pivot2 = pd.pivot_table(all_data,index=["FirstParam","SecondParam"])

logger.info("Here the second Pivot Table based on the first and second parameter")

pivot3= pd.pivot_table(all_data,index=["FirstParam","SecondParam"],aggfunc=np.sum)
logger.info("Here the third Pivot Table based on the first and second parameter and using sum as aggregate function on them")
