import csv
import pandas

def divide(file):
    df = pandas.read_csv(file)
    print(df)

def to_arff(file):
    for l in file.readlines():
        print(l)

if __name__ == "__main__":
    file = "barca.csv"
    learn, evaluate = divide(file)
    arff_learn = to_arff(learn)
    arff_evaluate = to_arff(evaluate)