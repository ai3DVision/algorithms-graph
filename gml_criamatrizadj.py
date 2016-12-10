# -*- coding: utf-8 -*-

"""
Simple demo of a scatter plot.
"""
import numpy as np
import networkx as nx
import sys

def verificaLista(v,l):
	for ll in l:
		if(set(v) == set(ll)):
			return True
	return False

print "Carregando arquivo..."
 

g = nx.read_gml(sys.argv[1])

txtFile = file(sys.argv[2], "w")


print "Iniciando geração da matriz de adjacencia..."

ver = []
listaAd = g.adjacency_list()
listaVertices = g.nodes()
qtdVertices = g.number_of_nodes()

for v in listaVertices:
	line = str(v) + " "
	for vv in listaAd[v]:
		line += str(vv) + " "
	line = line[:-1]
	line += "\n"
	txtFile.write(line);


txtFile.close()

tFile = file(sys.argv[2], "r")

l = tFile.readlines()
print len(l)
for i in l:
	print i

tFile.close()