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
 

cvsFile = file(sys.argv[1], "r")
lines = cvsFile.readlines()


print "Iniciando geração da matriz de adjacencia..."

vs = {}


for v in lines:
	vv = v.split(",")
	if(vv[0] not in vs):
		vs[vv[0]] = []
	ver = vv[1][:-1]
	if(ver not in vs[vv[0]]):
		vs[vv[0]].append(ver)

cvsFile.close()
adjFile = file(sys.argv[2], "w")

for k,v in vs.iteritems():
	line = k+" "
	for vv in v:
		line += vv+" "
	line = line[:-1]
	line += "\n"
	adjFile.write(line);

adjFile.close()