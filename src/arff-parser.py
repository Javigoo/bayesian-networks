#!/usr/bin/env python3

import os
import sys
import random
from shutil import copyfile



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


def parse_to_arff(csv_file):
    # Falta trasformar atributos a valor discreto
    tmp = open("tmp", "w")

    tmp.write("@RELATION AirBnB\n")

    set_attributes(tmp, get_attributes_type(csv_file))

    with open(csv_file, 'r') as f:
        f.readline() # Descartamos la primera linea (Atributos)
        tmp.write("@DATA\n")
        for line in f:
            tmp.write(set_data(line)+"\n")

    tmp.close()
    copyfile("tmp",csv_file)
    os.remove("tmp")


def get_attributes_type(file):
    attribute_name_type = {}

    with open(file, 'r') as f:
        attributes_name = f.readline().strip().split(",")
        first_row = f.readline().strip().split(",")

        for item in zip(attributes_name, first_row):
            attribute_name_type[item[0]] = get_type(item[1])

    return attribute_name_type


def get_type(element):
    if element.isdigit():
        return "INTEGER"
    elif element.replace(".", "", 1).isdigit():
        return "REAL"
    else:
        return "STRING"


def set_attributes(file, attributes):
    file.write("\n")

    for attribute in attributes.items():
        file.write("@ATTRIBUTE " + attribute[0] + " " + attribute[1] + "\n")

    file.write("\n")


def set_data(data_row):
    data = []
    raw_data = data_row.strip().split(",")

    for element in raw_data:
        if get_type(element) == "REAL":
            number = element.split(".")
            result_number = number[0]+"."+number[1][:3]
            data.append(result_number)
        else:
            data.append(element)

    data = ",".join(data)
    return data


def main():
    divide_dataset(dataset_file)
    parse_to_arff(training_file)
    parse_to_arff(validation_file)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit("Use: %s <csv-dataset-file> <arff-training-file> <arff-validation-file>" % sys.argv[0])

    if not os.path.isfile(sys.argv[1]):
        sys.exit("Error! %s not found" % sys.argv[1])

    dataset_file = os.path.abspath(sys.argv[1])
    training_file = sys.argv[2]
    validation_file = sys.argv[3]

    main()
