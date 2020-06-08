#!/usr/bin/env python3

import os
import sys
import random
from shutil import copyfile

def divide_dataset(data_file):
    random.seed(33543)  # Ultimos 5 digitos del DNI de un miembro del grupo

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
    process_attribute(tmp, csv_file)

    # @DATA - Procesamos los valores de los atributos para cada instancia
    process_data(tmp, csv_file)

    # Por ultimo copiamos los datos en el archivo deseado y eliminamos el archivo temporal
    tmp.close()
    copyfile("tmp",csv_file)
    os.remove("tmp")


def process_data(tmp, file):
    with open(file, 'r') as f:
        attributes = f.readline().strip().split(",") # Obtenemos la primera linea con el nombre de los atributos
        tmp.write("@DATA\n")
        for row in f:
            tmp.write(set_data(row,attributes)+"\n")


def set_data(data_row, attributes):
    # Procesa un registro de entrada para cada atributo en funcion de su tipo de datos
    data = []
    raw_data = data_row.strip().split(",")
    for element in zip(raw_data, attributes):
        data.append(get_corresponding_value(element[0],element[1]))

    return ",".join(data)


def get_corresponding_value(value, attribute):
    # Modifica los valores reales para asignarles un rango discreto
    if get_type(value) == "REAL":
        return get_discrete_value(value, attribute)
    # Modifica las cadenas de texto para aportar un formato correcto
    elif get_type(value) == "STRING":
        return  "'"+value+"'"

    return value


def get_type(element):
    # Esto metodo devuelve el tipo de datos de un atributo al que se corresponde con el tipo de datos que utiliza Weka
    if element.isdigit():
        return "INTEGER"
    elif element.replace(".", "", 1).isdigit():
        return "REAL"
    else:
        return "STRING"


def get_discrete_value(value, attribute):
    unit = value.split(".")[0]
    decimal = value.split(".")[1]

    if attribute in attributes_discrete_range_decimals:
        decimal_range_for_an_attribute = attributes_discrete_range_decimals[attribute]
        decimal = decimal[:decimal_range_for_an_attribute]
        return unit+"."+decimal

    return unit

def process_attribute(tmp, file):
    # Obtiene el nombre del atributo y sus posibles valores
    attributes_discrete_set = get_values_for_an_attribute(file)

    tmp.write("\n")
    for attribute in attributes_discrete_set.items():
        attribute_name = attribute[0]
        attribute_values = ",".join(attribute[1])
        attribute_datatype = get_type(attribute[1][0]) # Primer valor para el atributo

        if attribute_datatype == "STRING" or attribute_name == class_variable:
            tmp.write("@ATTRIBUTE " + attribute_name + " {" + attribute_values + "}\n")
        else:
            tmp.write("@ATTRIBUTE " + attribute_name + " " + attribute_datatype + "\n")

    tmp.write("\n")


def get_values_for_an_attribute(file):
    # Este metodo devuelve todos los posibles valores que le corresponden a un atributo
    attribute_values = {}

    with open(file, 'r') as f:
        attributes = f.readline().strip().split(",")

    # Recorremos todos los atributos
    for attribute_column in range(len(attributes)):
        values_for_attribute = []
        current_attribute = attributes[attribute_column]
        with open(file, 'r') as f:
            f.readline() # Descartamos el nombre de los atributos
            # Para cada atributo guardamos sus valores
            for value in f:
                # Aqui pasar a un rango discreto
                raw_value = value.strip().split(",")[attribute_column] # Valor que se corresponde con la columna del atributo
                value = get_corresponding_value(raw_value, current_attribute)

                if value not in values_for_attribute:
                    values_for_attribute.append(value)

            # Guardamos para el atributo actual su conjunto de valores
            attribute_values[current_attribute] = values_for_attribute

    return attribute_values


def main():
    global relation_name, class_variable, percentage_for_learning, attributes_discrete_range_decimals

    # Variables globales
    relation_name = "AirBnB"
    class_variable = "overall_satisfaction"
    percentage_for_learning = 75
    attributes_discrete_range_decimals = {"overall_satisfaction":1, "latitude":3, "longitude":3}

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
