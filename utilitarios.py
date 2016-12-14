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
  #G = removeArestasDuplicadasParaCriarArquivoDot(G)
  adjL = []
  GGT = gt.Graph(directed = False)
  vName = GGT.new_vertex_property("string")
  GGT.vp.vertex_name = vName
  for key,value in G.iteritems():
      v1 = procuraVerticeNoGrafo(GGT,key)
      if(not v1):
          v1 = GGT.add_vertex()
          GGT.vp.vertex_name[v1] = key
      for v in value:
        v2 = procuraVerticeNoGrafo(GGT,v)
        if(not v2):
            v2 = GGT.add_vertex()
            GGT.vp.vertex_name[v2] = v
        GGT.add_edge(v1, v2)
        adjL.append([key,v])
  return GGT

def criaArquivoDot(G):
  GG = removeArestasDuplicadasParaCriarArquivoDot(G)
  adjL = []
  dotFile = file("temp.dot", "w")
  dotFile.write("graph temp {\n")
  for key,value in GG.iteritems():
    for v in value:
        dotFile.write("\"" +str(key) + "\" -- \"" + str(v) + "\";\n")
        adjL.append([key,v])
  dotFile.write("}\n")
  dotFile.close()

def removeArestasDuplicadasParaCriarArquivoDot(G):
    GG = graph.Graph()
    for k,v in G.iteritems():
      l = []
      for vv in v:
        l.append(vv)
      GG[k] = l
    for v in GG.keys():
      for vizinhoDeV in GG[v]:
        if v in GG[vizinhoDeV]:
          GG[vizinhoDeV].remove(v)

    GG.make_consistent()
    return GG


def getDiameterAndAverageDistance(g):
  numVertex = g.num_vertices() 
  numEdges = g.num_edges() 
  print "Número de vértices de G:",numVertex
  print "Número de arestas de G:",numEdges
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
  print "Diâmetro:",diameter
  print "Distância média:",averageDistance
  return diameter, averageDistance
