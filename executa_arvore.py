#!/usr/bin/env python
# -*- coding: utf-8 -*-

import graph
import algoritmos
import subtreePattern
import editDistance2

import argparse

parser = argparse.ArgumentParser(description='Executa testes arvores.')
parser.add_argument('--grafo1', nargs='?', required=True,
                      help='Input graph file')
parser.add_argument('--grafo2', nargs='?', required=True,
                      help='Input graph file')
parser.add_argument('--deepth', nargs='?', required=True,type=int,
                      help='Deepth')

args = parser.parse_args()

print (" - Carregando matriz de adjacência para Grafo (na memória)...")
G1 = graph.load_adjacencylist(args.grafo1,undirected=True)
print (" - Carregando matriz de adjacência para Grafo (na memória)...")
G2 = graph.load_adjacencylist(args.grafo2,undirected=True)
print (" - Convertendo grafo para Dict (na memória)...")
dictG1 = G1.gToDict()
dictG2 = G2.gToDict()

print ("Criando árvore...")
a1,v1 = subtreePattern.criaArvore(dictG1,1)
a2,v2 = subtreePattern.criaArvore(dictG2,1)


print ("Arvore a1:")
subtreePattern.printArvore(a1)

print ("Arvore a2:")
subtreePattern.printArvore(a2)


r = editDistance2.calculaDeltas(a1,a2)

for k,d in r[0].iteritems():
	print "editDistance:",d,"Altura:",k


