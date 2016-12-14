#!/usr/bin/env python
# -*- coding: utf-8 -*-

import graph
import algoritmos
import subtreePattern
import editDistance2


import argparse

parser = argparse.ArgumentParser(description='Executa testes arvores.')
parser.add_argument('--grafo', nargs='?', required=True,
                      help='Input graph file')
parser.add_argument('--deepth', nargs='?', required=True,type=int,
                      help='Deepth')

args = parser.parse_args()

print " - Carregando matriz de adjacência para Grafo (na memória)..."
G1 = graph.load_adjacencylist(args.grafo,undirected=True)
print " - Convertendo grafo para Dict (na memória)..."
dictG1 = G1.gToDict()


print "Criando árvore..."
a1 = subtreePattern.criaArvore(dictG1,6795,args.deepth)
a2 = subtreePattern.criaArvore(dictG1,8020,args.deepth)

#print "Arvore a1:"
#subtreePattern.printArvore(a11)

#print "Arvore a2:"
#subtreePattern.printArvore(a21)



r = editDistance2.degreeSequenceEditDistanceComArvores(a1,a2,1,1,args.deepth)
print "Diferença",r[0]

