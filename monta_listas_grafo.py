#!/usr/bin/env python
# -*- coding: utf-8 -*-

### arquivos utilizados
import graph, editDistance2, algoritmos, graficos, utilitarios, calculos
from multiprocessing.pool import ThreadPool
from concurrent.futures import ProcessPoolExecutor, as_completed

######
import argparse,random,math,pickle
from time import time
import sys


def montaArvores(G):

	calculosSimultaneos = 100

	if(len(G) < calculosSimultaneos):
		calculosSimultaneos = len(G)

	cont = 0

	resultados = []

	futures = []
	with ProcessPoolExecutor(max_workers=10) as executor:

		for v,vizinhos in G.iteritems():
			futures.append(executor.submit(calculos.geraListas, dictG, v))
			#cont += 1
			#if(cont >= calculosSimultaneos):
			#	for f in as_completed(futures):
				# 	res = f.result()
				# 	resultados.append(res)
				# cont = 0
				# futures = []

		for f in as_completed(futures):
			res = f.result()
			resultados.append(res)

	return resultados


sys.setrecursionlimit(100000)

rand=random.Random()

parser = argparse.ArgumentParser(description='Criar bolas por vértices.')
parser.add_argument('--grafo', nargs='?', required=True,
                      help='Input graph file')

args = parser.parse_args()

print " - Carregando matriz de adjacência para Grafo (na memória)..."
G = graph.load_adjacencylist(args.grafo,undirected=True)
print " - Convertendo grafo para Dict (na memória)..."
dictG = G.gToDict()



print " - Gerando listas..."
t0 = time()

r = montaArvores(dictG)
	
t1 = time()


for i in r:
	print "Vértice",i[1]
	cont = 0
	for c in i[0]:
		print "Camada",cont
		calculos.printList(c)
		cont +=1

print ('Listas geradas em {}m'.format((t1-t0)/60))
