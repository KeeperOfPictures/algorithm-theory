#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть словарь координат городов



# Составим словарь словарей расстояний между ними
# расстояние на координатной сетке - ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def get_distances():
    
    sites = {
        'Moscow': (550, 370),
        'London': (510, 510),
        'Paris': (480, 480),
    }
    distances = {}

    for firstSite in sites.keys():
        for secondSite in sites.keys():
            if(firstSite == secondSite):
                continue
            name = firstSite + "-" + secondSite
            distances[name] = ((sites[firstSite][0] - sites[secondSite][0]) ** 2 + (sites[firstSite][1] - sites[secondSite][1]) ** 2) ** 0.5

    return distances




