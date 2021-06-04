"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr
from DISClib.DataStructures import mapentry as me
connections = "connections.csv"
countries = "countries.csv"
landing = "landing_points.csv"
datos = None
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\n")
    print("------------------------------------")
    print("------------------------------------")
    print("Bienvenido")
    print("1- Crear el catálogo")
    print("2- Cargar información en el catálogo")
    print("3- Identificar los clústeres de comunicación")
    print("4-  Identificar los puntos de conexión críticos de la red")
    print("5- La ruta de menor distancia ")
    print("6- Identificar la Infraestructura Crítica de la Red ")
    print("7- Análisis de fallas")
    print("8- Los mejores canales para transmitir")
    print("9-  La mejor ruta para comunicarme")
    print("10- Graficando los Grafos")
    print("0- Salir")
    print("------------------------------------")
    print("------------------------------------")


"""
Menu principal
"""

    

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("\nCreando el catálogo de datos ....")
        datos = controller.inicio()

    elif int(inputs[0]) == 2:
        print("\nCargando información de los archivos ....")
        controller.carga(datos, connections, countries, landing)
        nc = controller.totalcables(datos)
        nlp = controller.totalpoints(datos)
        np = controller.totalCountries(datos)
        print('Numero de landing points: ' + str(nlp))
        print('Numero de cables: ' + str(nc))
        print('Numero de paises: ' + str(np))

    elif int(inputs[0]) == 3:
        landinga = input("ingrese un landing point: ")
        landingb = input("ingrese un landing point: ")
        controller.req1(datos,landinga,landingb)

    elif int(inputs[0]) == 4:
        d=controller.req2(datos)
        for i in d:
            print('el vertice {0} tiene {1} cables coonectados'.format(i,d[i]))
    elif int(inputs[0]) == 5:
        pais_a = "Colombia"
        pais_b = 'Indonesia'
        controller.req3(datos,pais_a,pais_b)

    elif int(inputs[0]) == 6:
        pass

    elif int(inputs[0]) == 7:
        landingpoint='fortaleza'
        #landingpoint=input('ingresa el landing point que deseas consultar: ')
        x=controller.req5(datos,landingpoint)
        print('la cantidad de paises afectados es:{0} '.format(len(x)))
        print('la lista de paises afectados es : {0}'.format(x))
    elif int(inputs[0]) == 8:
        pass
    else:
        sys.exit(0)
sys.exit(0)
