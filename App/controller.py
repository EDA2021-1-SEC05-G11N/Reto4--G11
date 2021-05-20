"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    datos = model.newAnalyzer()
    return datos

# Funciones para la carga de datos

def loadData(datos, countries,landing_points_file,connectionsfile):
    loadCountrie(datos, countries)
    loadlanding(datos,landing_points_file)
    loadconnections(datos,connectionsfile)

def loadCountrie(datos, countriesfile):
    file = cf.data_dir + countriesfile
    input_file = csv.DictReader(open(file, encoding="utf-8"),
                                delimiter=",")

    for i in input_file:
        model.addCountry(datos, i)
def loadlanding(datos,landing_points_file):
    file = cf.data_dir + landing_points_file
    input_file = csv.DictReader(open(file, encoding="utf-8"),
                                delimiter=",")
    for i in input_file:
        model.addlanding(datos, i)
def loadconnections(datos,connectionsfile):
    
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
