#!/usr/bin/env python3
import csv
import pandas
import arff
import os

def divide(file):
    seed = 33543 
    df = pandas.read_csv(file)
    print(df)
    #75% - 25%
    percent = len(df.index)
    dl = de = pandas.DataFrame( )
    #75% para Learn.
    for i in range(int(percent*0.75)):
        row =  df.sample(n=1, random_state=seed)
        print(row)
        dl = dl.append(row)
        df = df.drop(row.index)
    #25% para Evaluate.
    for i in range(int(percent*0.25)):
        row = df.sample(n=1, random_state=seed)
        print(row)
        de = de.append(row)
        df = df.drop(row.index)
    #Por si queda uno, debido a la
    #forma en que tratamos los %.
    if len(df.index) == 1:
        row = df.sample(n=1)
        print(row)
        de = de.append(row)
        df = df.drop(row.index)
    print("\nFILE:   ",df)
    print("\nLEARN:  ",dl)
    print("\nEVALUATE:   ",de)
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
