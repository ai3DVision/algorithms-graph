#!/usr/bin/env python
# -*- coding: utf-8 -*-

import graph
import graph_tool.all as gt

def verificaParLista(v1,v2,lista):
  for x in lista:
    if(v1 == x[0] and v2 == x[1]):
      return True
    if(v1 == x[1] and v2 == x[0]):
      return True
  return False

def procuraVerticeNoGrafo(g,nome):
    r = gt.find_vertex(g, g.vp.vertex_name, nome)
    if(not r):
        return r
    else:
        return r[0]

def graphToGraphTool(G):
    adjL = []
    GGT = gt.Graph(directed = False)
    vName = GGT.new_vertex_property("string")
    GGT.vp.vertex_name = vName
    for key,value in G.iteritems():
        for v in value:
            if(not verificaParLista(key,v,adjL)):
                v1 = procuraVerticeNoGrafo(GGT,key)
                if(not v1):
                    v1 = GGT.add_vertex()
                    GGT.vp.vertex_name[v1] = key
                v2 = procuraVerticeNoGrafo(GGT,v)
                if(not v2):
                    v2 = GGT.add_vertex()
                    GGT.vp.vertex_name[v2] = v
                GGT.add_edge(v1, v2)
                adjL.append([key,v])
    return GGT


def getDiameterAndAverageDistance(g):
  numVertex = g.num_vertices() 
  sumSD = 0;
  print " - Executando método shortest_distance..."
  sD = gt.shortest_distance(g, directed=False)

  print " - Executando laço de cálculo da distância média e diâmetro..."
  x = 0;
  diameter = sD[0][0]
  sumSD = 0.0
  n_vertices = 0
  while x < numVertex:
    for d in sD[x]:
      if(d != 2147483647):
         sumSD = sumSD + d
         if(d > diameter):
           diameter = d
    x += 1

  averageDistance = sumSD / (numVertex*(numVertex-1)) 
  return diameter, averageDistance
