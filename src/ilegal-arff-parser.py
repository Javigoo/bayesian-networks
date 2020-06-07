#!/usr/bin/env python3

import csv
import pandas
import arff
import os

def divide(file):
    df = pandas.read_csv(file)
    print(df)
    #75% - 25%
    percent = len(df.index)
    dl = de = pandas.DataFrame( )
    for i in range(int(percent*0.75)):
        row = df.sample(n=1)
        print(row)
        dl.append(row)
        df.drop(row.index)
    for i in range(int(percent*0.25)):
        row = df.sample(n=1)
        print(row)
        de.append(row)
        df.drop(row.index)
    print("FILE:   ",df)
    print("LEARN:  ",dl)
    print("EVALUATE:   ",de)
    return dl, de

def to_arff(df, filename):
    arff.dump(filename
      , df.values
      , relation='relation name'
      , names=df.columns)

if __name__ == "__main__":
    file = "barca.csv"
    pandas_learn, pandas_evaluate = divide(file)
    to_arff(pandas_learn, 'learn.arff')
    to_arff(pandas_evaluate, 'evaluate.arff')
    os.system("rm files-arff/ilegal/* & mv *.arff files-arff/ilegal/")
