#!/usr/bin/env python
# -*- coding: utf-8 -*-

import graph
import algoritmos
import calculos

import argparse

parser = argparse.ArgumentParser(description='Executa testes arvores.')
parser.add_argument('--grafo1', nargs='?', required=True,
                      help='Input graph file')
parser.add_argument('--grafo2', nargs='?', required=True,
                      help='Input graph file')

args = parser.parse_args()

print (" - Carregando matriz de adjacência para Grafo (na memória)...")
G1 = graph.load_adjacencylist(args.grafo1,undirected=True)
print (" - Carregando matriz de adjacência para Grafo (na memória)...")
G2 = graph.load_adjacencylist(args.grafo2,undirected=True)
print (" - Convertendo grafo para Dict (na memória)...")
dictG1 = G1.gToDict()
dictG2 = G2.gToDict()

print ("Criando listas...")
l1,v1 = calculos.geraListas(dictG1,1)
l2,v2 = calculos.geraListas(dictG2,1)


print ("Listas v1:")
calculos.printDataVertice(l1)

print ("Listas v2:")
calculos.printDataVertice(l2)

deltas = calculos.calculaDistancia(l1,l2,v1,v2)

for k,d in deltas[0].iteritems():
	print "Altura:",k,"distancia:",d


