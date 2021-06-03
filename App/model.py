﻿"""
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from sys import meta_path
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def inicio():
    datos = {
                'pais': None,
                'landing': None,
                'pais_cable': None,
                'capacidad': None,
                'cables': None,
                }
    datos['pais'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=comparemap)

    datos['pais_cable'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=comparemap)    

    datos['capacidad'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=comparemap)

    datos['landing'] = mp.newMap(numelements=1400,
                                     maptype='PROBING',
                                     comparefunction=comparemap)

    datos['cables'] = gr.newGraph(datastructure='ADJ_LIST',
                                    directed=True,
                                    size=14000,
                                    comparefunction=comparegrafo)

    return datos

# Funciones para agregar informacion al catalogo
def agregarLanding(datos, dic):
    mp.put(datos["landing"], int(dic["landing_point_id"]), dic)
    return datos
    
def agregarconexion(datos, dic):
    cable = dic["cable_name"]
    origin = formatVertex(datos, dic['\ufefforigin'], cable)
    destination = formatVertex(datos, dic["destination"], cable)
    d = dic["cable_length"].replace(" km", "")
    if 'n.a.' in d:
        distance = 0
    else:
        distance = float(d.replace(",", ""))
    agregarPoint(datos, origin)
    agregarPoint(datos, destination)
    agregarcable(datos, origin, destination, distance)
    connection = origin + destination + cable
    capacity = float(dic["capacityTBPS"])
    agregarCapacity(datos, connection, capacity)
    agregarCountrypoint(datos, dic, destination, connection, capacity)
    return datos

def agregarpais(datos, dic):
    mp.put(datos["pais"], dic["CountryName"], dic)
    return datos

# Funciones de interacción entre estructuras
def PointInfo(datos, lpid):
    map = datos['landing']
    a = mp.get(map, int(lpid))
    info = me.getValue(a)
    return info 

# Funciones para creacion de datos
def formatVertex(datos, landingpoint, cable):
    lpinfo = PointInfo(datos, landingpoint)
    name = lpinfo["id"]
    name = name + '-' + cable
    return name

def agregarPoint(datos, landingpoint):
    if not gr.containsVertex(datos["cables"], landingpoint):
        gr.insertVertex(datos["cables"], landingpoint)
    return datos

def agregarcable(datos, origen, destino, distancia):
    edge = gr.getEdge(datos['cables'], origen, destino)
    if edge is None:
        gr.addEdge(datos['cables'], origen, destino, distancia)
    return datos

def agregarCapacity(datos, conexion, capacidad):
    mp.put(datos["capacidad"], conexion, capacidad)
    return datos

def agregarCountrypoint(datos, landingpoint, lpvertex, connection, capacity):
    lpinfo = PointInfo(datos, landingpoint["destination"])
    lpname = lpinfo["name"].split(",")
    namesize = len(lpname)
    
    if namesize == 3:
        country = lpname[2].lower().replace(" ", "")
    elif namesize == 2:
        country = lpname[1].lower().replace(" ", "")
    else:
        country = "No identified"
    if mp.contains(datos['pais_cable'], country):
        a = mp.get(datos['pais_cable'], country)
        countrylist = me.getValue(a)
    else:
        countrylist = lt.newList(datastructure= 'ARRAY_LIST')
    lt.addLast(countrylist, {"name": connection, "capacity": capacity, "vertex": lpvertex})

    min = 1000000000000000
    for i in lt.iterator(countrylist):
        if i["capacity"] < min:
            min = i["capacity"]

    for i in lt.iterator(countrylist):         
        if i["vertex"] != lpvertex:
            agregarcable(datos, lpvertex, i["vertex"], 0.1)
            connection = lpvertex + i["vertex"] + "IC"
            agregarCapacity(datos, connection, min)

    mp.put(datos['pais_cable'], country, countrylist)

    return datos

# Funciones de consulta
def totalpoints(datos):
    return gr.numVertices(datos['cables'])

def totalcables(datos):
    return gr.numEdges(datos['cables'])

def totalCountries(datos):
    return mp.size(datos['pais'])

# Funciones utilizadas para comparar elementos dentro de una lista
def comparegrafo(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def comparemap(val1, val2):
    if (val1 == val2):
        return 1
    else:
        return 0

def compareCapacity(lp1, lp2):
    if lp1["capacity"] > lp2["capacity"]:
        return True
    else:
        return False

# Funciones de ordenamiento
def sort(lst, comparefunction):
    sorted_list = sa.sort(lst, comparefunction)
    return sorted_list

# requerimientoss
def req1(datos,a,b):
    clusteres = gr.numEdges(datos['cables'])
    try:
        p = gr.getEdge(datos['cables'],a,b)
    except:
        p = "los  landing point no se encuentran en el mismo clúster"

    return (clusteres,p)

def req2(datos):
    vertices = gr.vertices(datos['cables'])
    tamano = lt.size(vertices)
    p=0 
    respuesta = {}
    while p < int(tamano):
        b=lt.getElement(vertices,p)
        numero = gr.degree(datos['cables'],b)
        respuesta[b]= numero
        p+=1
    return respuesta

def req3(datos):
    print('entro')

def req5(datos,landingpoint):
    vertices = gr.vertices(datos['cables'])
    tamano = lt.size(vertices)
    p=0 
    paises =  mp.keySet(datos['pais'])
    numero = 0
    while p < int(tamano):
        b=lt.getElement(vertices,p)
        if landingpoint in b:
            j = gr.adjacents(datos['cables'],b)
            l=0
            while l < lt.size(j):
                l+=1
                y=lt.getElement(j,l)
                input(y)
            numero +=1
        p+=1