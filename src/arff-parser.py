#!/usr/bin/env python3

import os
import sys
import random
from shutil import copyfile


def divide_dataset(data_file):
    random.seed(33543)  # Ultimos 5 digitos del DNI de algun miembro del grupo

    learning = open(learning_file, "w")
    evaluation = open(evaluation_file, "w")

    with open(data_file, 'r') as data:
        atributos = data.readline()

        learning.write(atributos)
        evaluation.write(atributos)

        # Divide el dataset en funcion del porcentaje de registros de entrada que queremos destinar al aprendizaje
        for row in data:
            if random.randint(1,100) <= percentage_for_learning:
                learning.write(row)
            else:
                evaluation.write(row)

    learning.close()
    evaluation.close()


def parse_to_arff(csv_file):
    # Creamos un archivo temporal para guardar los datos trasformados a ARFF
    tmp = open("tmp", "w")

    # A continuacion definimos las distintas secciones que debe tener un archivo ARFF

    # @RELATION - Define el nombre de la relacion
    tmp.write("@RELATION "+ relation_name + "\n")

    # @ATTRIBUTE - Obtenemos el nombre del atributo y su tipo de datos
    set_attributes(tmp, get_attributes_type(csv_file))

    # @DATA - Procesamos los valores de los atributos para cada instancia
    with open(csv_file, 'r') as f:
        f.readline() # Descartamos la primera linea (Atributos)
        tmp.write("@DATA\n")
        for line in f:
            tmp.write(set_data(line)+"\n")

    # Por ultimo copiamos los datos en el archivo deseado y eliminamos el archivo temporal
    tmp.close()
    copyfile("tmp",csv_file)
    os.remove("tmp")


def get_attributes_type(file):
    # Con este metodo devolvemos el nombre de los atributos y su tipo de datos asociado
    attribute_name_type = {}
    with open(file, 'r') as f:
        # Para no asignar manualmente el tipo de datos de un atributo lo obtenemos
        # buscando en la primera fila los tipos de datos que tienen un valor para cada atributo
        attributes_name = f.readline().strip().split(",")
        first_row = f.readline().strip().split(",")
        for name_type in zip(attributes_name, first_row):
            attribute_name_type[name_type[0]] = get_type(name_type[1])

    return attribute_name_type


def get_type(element):
    # Esto metodo devuelve el tipo de datos de un atributo al que se corresponde con el tipo de datos que utiliza Weka
    if element.isdigit():
        return "INTEGER"
    elif element.replace(".", "", 1).isdigit():
        return "REAL"
    else:
        return "STRING"


def set_attributes(file, attributes):
    # Define el nombre del atributo y su tipo de datos
    file.write("\n")
    for attribute in attributes.items():
        file.write("@ATTRIBUTE " + attribute[0] + " " + attribute[1] + "\n")
    file.write("\n")


def set_data(data_row):
    # Procesa un registro de entrada para cada atributo en funcion de su tipo de datos
    data = []
    raw_data = data_row.strip().split(",")

    for element in raw_data:

        # Modifica los valores reales para asignarles un rango discreto
        if get_type(element) == "REAL":
            number = element.split(".")
            result_number = number[0]+"."+number[1][:discrete_range_decimals] # Numero de decimales que cogemos
            data.append(result_number)

        # Modifica las cadenas de texto para aportar un formato correcto
        elif get_type(element) == "STRING":
            data.append("'"+element+"'")

        else:
            data.append(element)

    data = ",".join(data)
    return data


def main():
    global relation_name, percentage_for_learning, discrete_range_decimals

    # Variables globales
    relation_name = "AirBnB"
    percentage_for_learning = 75
    discrete_range_decimals = 3

    divide_dataset(data_file)
    parse_to_arff(learning_file)
    parse_to_arff(evaluation_file)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Use: %s <csv-data-file> <arff-learning-file> <arff-evaluation-file>" % sys.argv[0])

    if not os.path.isfile(sys.argv[1]):
        sys.exit("Error! %s not found" % sys.argv[1])

    data_file = os.path.abspath(sys.argv[1])

    if len(sys.argv) < 4:
        learning_file = "learning.arff"
        evaluation_file = "evaluation.arff"
    else:
        learning_file = sys.argv[2]
        evaluation_file = sys.argv[3]

    main()
