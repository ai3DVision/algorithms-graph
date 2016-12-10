#!/usr/bin/env python
# -*- coding: utf-8 -*-

import graph
import algoritmos
import argparse
import numpy as np
from numpy import linalg as LA

parser = argparse.ArgumentParser(description='Criar bolas por vértices.')
parser.add_argument('--input', nargs='?', required=True,
                      help='Input graph file')
parser.add_argument('--deepth', nargs='?', required=True,type=int,
                      help='Deepth')

args = parser.parse_args()

G = graph.load_adjacencylist(args.input,undirected=True)

print "Com arestas:"

algoritmos.montaBolaComArestasUltimaCamada(G,3,args.deepth).printAdjList()

print "Sem arestas:"

algoritmos.montaBolaSemArestasUltimaCamada(G,3,args.deepth).printAdjList()
