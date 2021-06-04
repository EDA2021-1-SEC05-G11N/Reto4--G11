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

from sys import meta_path
import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def inicio():
    datos = model.inicio()
    return datos

# Funciones para la carga de datos
def carga(datos, connections, countries, landing):
    cargaLanding(datos, landing)
    cargaConnections(datos, connections)
    cargaCountries(datos, countries)

def cargaLanding(datos, landing):
    cfile = cf.data_dir + landing
    file = csv.DictReader(open(cfile, encoding="utf-8"),
                                delimiter=",")

    a = True
    for i in file:
        if a:
            print(i)
            a = False
        model.agregarLanding(datos, i)

def cargaConnections(datos, connections):
    cfile = cf.data_dir + connections
    file = csv.DictReader(open(cfile, encoding="utf-8"),
                                delimiter=",")

    a = True
    for i in file:
        if a:
            print(i)
            a = False
        model.agregarconexion(datos, i)

def cargaCountries(datos, countrie):
    cfile = cf.data_dir + countrie
    file = csv.DictReader(open(cfile, encoding="utf-8"),
                                delimiter=",")

    for i in file:
        model.agregarpais(datos, i)


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def totalpoints(datos):
    return model.totalpoints(datos)


def totalcables(datos):
    return model.totalcables(datos)

def totalCountries(datos):
    return model.totalCountries(datos)

def req1(datos,landinga,landingb):
    return model.req1(datos,landinga,landingb)

def req2(datos):
    return model.req2(datos)

def req3(datos,pais_a,pais_b):
    return model.req3(datos,pais_a,pais_b)

def req5(datos,landingpoint):
    return model.req5(datos,landingpoint)