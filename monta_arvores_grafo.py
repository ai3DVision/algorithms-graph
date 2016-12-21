#!/usr/bin/env python
# -*- coding: utf-8 -*-

### arquivos utilizados
import graph, editDistance2, algoritmos, graficos, utilitarios, subtreePattern
from multiprocessing.pool import ThreadPool
from concurrent.futures import ProcessPoolExecutor, as_completed

######
import argparse,random,math,pickle
from time import time


def geraArquivo(d):
	vFile = file("vertices/"+str(d[1])+".data", "w")
	vFile.write(str(d[1])+"\n");
	cont = 0
	for c in d[0]:
		vFile.write(str(cont)+": ");
		for v in c:
			vFile.write(str(v.label)+","+str(v.qtdFilhos)+","+str(v.filhos)+";");
		vFile.write("\n");
		cont += 1
	vFile.close()





def montaArvores(G):

	calculosSimultaneos = 100

	futures = []
	resultados = []

	files_left = len(G)
	files_iter = iter(sorted(G.iteritems()))

	with ProcessPoolExecutor(max_workers=10) as executor:

		while files_left:
			cont = 0
			for v in files_iter:
				futures.append(executor.submit(subtreePattern.criaArvore, dictG, v[0]))
				cont += 1
				if(cont > calculosSimultaneos):
					break


			for f in as_completed(futures):
				files_left -= 1
				res = f.result()
				resultados.append(res)
				del f

			print "Resultados processados. Iniciando geração de arquivos..."

			futures = []
			for r in resultados:
				geraArquivo(r)
			resultados = []

			print "Arquivos gerados."
			



	#resultadosConsolidados = []
	#for r in resultados:
	#	resultadosConsolidados.append({'label': r[1], 'arvore': r[0]})
	
	#return resultadosConsolidados

rand=random.Random()

parser = argparse.ArgumentParser(description='Criar bolas por vértices.')
parser.add_argument('--grafo', nargs='?', required=True,
                      help='Input graph file')

args = parser.parse_args()

print " - Carregando matriz de adjacência para Grafo (na memória)..."
G = graph.load_adjacencylist(args.grafo,undirected=True)
print " - Convertendo grafo para Dict (na memória)..."
dictG = G.gToDict()



print " - Gerando árvore..."
t0 = time()

montaArvores(dictG)
	
t1 = time()

print ('Árvores geradas em {}m'.format((t1-t0)/60))
