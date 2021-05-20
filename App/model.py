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


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    analyzer = {'country': None,
                'landing': None
                }                
    analyzer['country'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareValue)
    analyzer['landing'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareValue)
    return analyzer

# Funciones para agregar informacion al catalogo

def addCountry(datos, dic):
    mapa = datos["country"]
    pais = dic["CountryName"]
    om.put(mapa, pais, dic)
    return datos
def addlanding(datos, dic):
    mapa = datos['landing']
    point_id = dic["landing_point_id"]
    om.put(mapa, point_id, dic)

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

def compareValue(val1, val2):
    if (val1 == val2):
        return 0
    elif (val1 > val2):
        return 1
    else:
        return -1

# Funciones de ordenamiento
