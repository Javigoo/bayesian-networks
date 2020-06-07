#!/usr/bin/env python3

import csv
import pandas
import os
import sys
import random

def divide_dataset(dataset):
    random.seed(33543)  # Ultimos 5 digitos del DNI de algun miembro del grupo

    training = open(training_file, "w")
    validation = open(validation_file, "w")

    with open(dataset, 'r') as f:
        atributos = f.readline()

        training.write(atributos)
        validation.write(atributos)

        for linea in f:
            if random.randint(1,100) <= 75:
                training.write(linea)
            else:
                validation.write(linea)

    training.close()
    validation.close()

    # Falta dividir dataset en 2, aletoriamente con la seed. 75% para training y 25% validation

def parse_to_arff(csv_dataset_file):
    # Falta trasformar atributos a valor discreto
    data = pandas.read_csv(csv_dataset_file)
    print("\n",data)

def main():
    divide_dataset(dataset_file)
    parse_to_arff(training_file)
    parse_to_arff(validation_file)

if __name__ == "__main__":
    # Temporal
    print("usage example: ./arff-parser.py barca.csv files-arff/training.arff files-arff/validation.arff")

    if len(sys.argv) < 4:
        sys.exit("Use: %s <csv-dataset-file> <arff-training-file> <arff-validation-file>" % sys.argv[0])

    if not os.path.isfile(sys.argv[1]):
        sys.exit("Error! %s not found" % sys.argv[1])

    dataset_file = os.path.abspath(sys.argv[1])
    training_file = sys.argv[2]
    validation_file = sys.argv[3]

    main()
