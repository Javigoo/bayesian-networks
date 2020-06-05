import csv
import pandas
import arff

def divide(file):
    df = pandas.read_csv(file)
    print(df)
    return df, df

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