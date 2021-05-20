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
countries = "countries.csv"
landing_points_file = "landing_points.csv"
connectionsfile = "connections.csv"
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
        print("Cargando información de los archivos ....")
        datos = controller.init()
    elif int(inputs[0]) == 2:
        controller.loadData(datos,countries,landing_points_file,connectionsfile)

    else:
        sys.exit(0)
sys.exit(0)
