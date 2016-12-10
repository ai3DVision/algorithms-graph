#!/usr/bin/env python
# -*- coding: utf-8 -*-

import graph
import editDistance
import argparse
import numpy as np
from numpy import linalg as LA

parser = argparse.ArgumentParser(description='Criar bolas por vértices.')
parser.add_argument('--grafoModel', nargs='?', required=True,
                      help='Input graph file')
parser.add_argument('--grafoData', nargs='?', required=True,
                      help='Input graph file')

args = parser.parse_args()

Gm = graph.load_adjacencylist(args.grafoModel,undirected=True)
Gd = graph.load_adjacencylist(args.grafoData,undirected=True)

Am = editDistance.binaryMatrix(Gm)
Ad = editDistance.binaryMatrix(Gd)
Dm = editDistance.diagonalDegreeMatrixFromBinaryMatrix(Am)
Dd = editDistance.diagonalDegreeMatrixFromBinaryMatrix(Ad)
#d = graph.diagonalDegreeMatrix(m)
print "Matriz binária (Am)"
print Am
print "Matriz binária (Ad)"
print Ad
print "DiagonalDegreeMatrix (Dm)"
print Dm
print "DiagonalDegreeMatrix (Dd)"
print Dd


#print "TransitionProbabilityMatrix (d x a)"
#r = np.matrix(d)*np.matrix(mb)
#print r

print "Wm"
Wm = editDistance.calculaW(Dm,Am)
av, avet = LA.eig(Wm)
print Wm
print "Autovalores"
print av
print "Autovetores"
print avet

print "---------"
print "Wd"
Wd = editDistance.calculaW(Dd,Ad)
av, avet = LA.eig(Wd)
print Wm
print "Autovalores"
print av
print "Autovetores"
print avet

print "Criando phi_m..."
phi_m = editDistance.scaledLeadingEigenvector(Wm,Gm)
print "Criando phi_d..."
phi_d = editDistance.scaledLeadingEigenvector(Wd,Gd)
print "Caminhando no phi_m..."
Sm = editDistance.caminhaNoPhi(phi_m,Gm)
print "Caminhando no phi_d..."
Sd = editDistance.caminhaNoPhi(phi_d,Gd)

print "Criando lattice..."
lattice = editDistance.criaLattice(Sm,Sd,Gm,Gd,Wm,Wd)
print "Lattice:"
for ll in lattice:
	line = ""
	for l in ll:
		line += "("
		for l2 in l:
			try:
				line += '%.3f'%(l2)+", "
			except TypeError:
				line += l2+", "
		line += ") "
	print line 
	print "--"

