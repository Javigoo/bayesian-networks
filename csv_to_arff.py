

def divide(file):
    pass

def to_arff(file):
    for l in file.readlines():
        print(l)

if __name__ == "__main__":
    file = open("barca.csv","r")
    learn, evaluate = divide(file)
    arff_learn = to_arff(learn)
    arff_evaluate = to_arff(evaluate)