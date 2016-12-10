#!/usr/bin/env python
# -*- coding: utf-8 -*-

import graph
import editDistance2
import argparse

parser = argparse.ArgumentParser(description='Criar bolas por vértices.')
parser.add_argument('--grafoModel', nargs='?', required=True,
                      help='Input graph file')
parser.add_argument('--grafoData', nargs='?', required=True,
                      help='Input graph file')

args = parser.parse_args()

Gm = graph.load_adjacencylist(args.grafoModel,undirected=True)
Gd = graph.load_adjacencylist(args.grafoData,undirected=True)

print "degreeSequenceEditDistance:"
print editDistance2.degreeSequenceEditDistance(Gm,Gd)