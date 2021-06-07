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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """



from math import acos , cos ,sin ,radians
from requests.models import parse_header_links
from DISClib.DataStructures.chaininghashtable import get
from sys import meta_path
import config as cf
import requests as re  
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import dijsktra as di
from DISClib.Algorithms.Graphs import bellmanford as be
from DISClib.ADT import stack as st
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
    remplazar = dic["id"]
    nombre = dic["name"]
    dic["name"]= nombre.replace(' ','')
    dic["id"]= remplazar.replace('-','')
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

def distancia_puntos(punto1,punto2):
    punto1 = (radians(float(punto1[0])),radians(float(punto1[1])))
    punto2 = (radians(float(punto2[0])),radians(float(punto2[1])))
    distancia = acos(sin(punto1[0])*sin(punto2[0])+cos(punto1[0])*cos(punto2[0])*cos(punto1[1]-punto2[1]))
    respuesta = distancia * 6371.01
    return respuesta

def totalpoints(datos):
    return gr.numVertices(datos['cables'])

def totalcables(datos):
    return gr.numEdges(datos['cables'])

def totalCountries(datos):
    return mp.size(datos['pais'])

# Funciones utilizadas para comparar elementos dentro de una lista
def esta(pais,lista,final):
    for i in lista:
        if (pais in i):
            if pais not in final:
                final.append(pais)
            break
    


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

def req3(datos,pais_a,pais_b):
    
    a= mp.get(datos['pais'],pais_a)
    b = mp.get(datos['pais'],pais_b)
    #capitala = (a['value']['CapitalName']).lower() es bogota pero no esta en el archivo
    capitalb = (b['value']['CapitalName']).lower()
    vertices = gr.vertices(datos['cables'])
    tamano = lt.size(vertices)
    p=0 
    mirar = {}
    pasar_funcion = []
    while p < int(tamano):
        x=lt.getElement(vertices,p)
        ciudad= x.split('-')
        ciudad_comparar = ciudad[0]
        if capitalb in ciudad_comparar.lower():
            mirar[ciudad_comparar]=x
        if ('tolu' in ciudad_comparar.lower()):
            mirar[ciudad_comparar]=x
        p+=1
    for i in mirar:
        pasar_funcion.append(mirar[i])
    
    vertice1 = 'jakartaindonesia-Matrix Cable System'
    vertice2 = 'tolucolombia-Colombian Festoon'
    #vertice1 = pasar_funcion[0]
    #vertice2 = pasar_funcion[1]
    distancia_vertices = {}
    t=di.Dijkstra(datos['cables'],vertice1)
    distancia_total= di.distTo(t,vertice2)
    pila_camino= di.pathTo(t,vertice2)
    h = 0
    while h< st.size(pila_camino):
        D=st.pop(pila_camino)
        verta = D['vertexA']
        vertb =  D['vertexB']
        U = di.Dijkstra(datos['cables'],verta)
        distancia = di.distTo(U,vertb)
        distancia_vertices[h]=(verta,vertb,distancia)
        h+=1
    
    return (distancia_vertices,distancia_total)

def req4(datos):
    print('entro')
    
def req5(datos,landingpoint):
    vertices = gr.vertices(datos['cables'])
    tamano = lt.size(vertices)
    p=0 
    e = 0
    final= []
    paises =  mp.keySet(datos['pais'])
    pais= []
    numero = 0
    while p < int(tamano):
        b=lt.getElement(vertices,p)
        if landingpoint in b:
            j = gr.adjacents(datos['cables'],b)
            l=0
            while l < lt.size(j):
                l+=1
                y=lt.getElement(j,l)
                x = y.split('-')
                if x[0] not in pais:
                    pais.append(x[0])
            numero +=1
        p+=1
    while e < lt.size(paises):
        w=(lt.getElement(paises,e).lower()).replace(' ','')
        esta(w,pais,final)
        e+=1
    return final


def req7(datos,ip1,ip2):
    vertices = gr.vertices(datos['cables'])
    ayuda = 0 
    base = 'http://ip-api.com/json/'
    ip_1 = base+ip1
    ip_2 = base+ip2
    mayor_ip1 = 1000000000000000000000000000000000000000000000000000000000
    mayor_ip2 = 1000000000000000000000000000000000000000000000000000000000
    vertice1 = ''
    vertice2 = ''
    posiblesip1 = []
    posiblesip2 = []
    distancia_ip1 = {}
    distancia_ip2 = {}
    info_ip1 = re.get(ip_1).json()
    info_ip2 = re.get(ip_2).json()
    ubicacion_ip1 = (info_ip1['lat'],info_ip1['lon'])
    ubicacion_ip2 = (info_ip2['lat'],info_ip2['lon'])
    l = mp.keySet(datos['landing'])
    o = 0
    while o < lt.size(l):
        identificador = lt.getElement(l,o)
        x = mp.get(datos['landing'],identificador)
        comparar = x['value']['id']
        if ((info_ip1['country']).replace(' ','')).lower() in comparar:
            posiblesip1.append(x['value'])
        elif ((info_ip2['country']).replace(' ','')).lower() in comparar:
            posiblesip2.append(x['value'])
        o+=1
    for i in posiblesip1:
        ubicion = (i['latitude'],i['longitude'])
        respuesta = distancia_puntos(ubicion,ubicacion_ip1)
        distancia_ip1[i['id']] = (i,respuesta)
    for jk in posiblesip2:
        ubicion1 = (jk['latitude'],jk['longitude'])
        respuesta1 = distancia_puntos(ubicion1,ubicacion_ip2)
        distancia_ip2[jk['id']] = (jk,respuesta1)

    for gh in distancia_ip1:
        if mayor_ip1 >  distancia_ip1[gh][1]:
            mayor_ip1 = distancia_ip1[gh][1]
            vertice1 = distancia_ip1[gh][0]
    for lk in distancia_ip2:
        if mayor_ip2 >  distancia_ip2[lk][1]:
            mayor_ip2 = distancia_ip2[lk][1]
            vertice2 = distancia_ip2[lk][0]
    vertice1= vertice1['id']
    vertice2= vertice2['id']
    while ayuda < lt.size(vertices):
        ojala = lt.getElement(vertices,ayuda)
        kfj = ((lt.getElement(vertices,ayuda).replace('-','')).replace(' ','')).lower()
        if vertice1 in kfj:
            vertice1 = ojala
        if vertice2 in kfj:
            vertice2 = ojala
        ayuda+=1
    
    grafo = datos['cables']
    khi = di.Dijkstra(grafo,vertice1)
    pila = di.pathTo(khi,vertice2)
    try:
        tamano = st.size(pila)
        respuesta = pila
        
    except:
        tamano = 0
        respuesta = 'no hay un camino entre las direcciones ip'
    return tamano,respuesta