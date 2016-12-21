#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime
from time import time
from collections import deque
import numpy as np
import math

def geraListas(g, root, dist):
   

    listas = []

    t0 = time()

    # cria vetor de marcação
    vetor_marcacao = [0] * (max(g) + 1)

    # Marcar s e inserir s na fila Q
    queue = [root]
    vetor_marcacao[root] = 1
    
    l = deque()
    
    ## Variáveis de controle de distância
    depth = 0
    pendingDepthIncrease = 0
    timeToDepthIncrease = 1

    while queue:
        vertex = queue.pop(0)
        timeToDepthIncrease -= 1

        l.append(len(g[vertex]))

        #print "size",sys.getsizeof(l)


        for v in g[vertex]:
            if(vetor_marcacao[v] == 0):
                vetor_marcacao[v] = 1
                queue.append(v)
                pendingDepthIncrease += 1    


        if(timeToDepthIncrease == 0):
            l = sorted(l)

            listas.append(l)
            l = deque()

            depth += 1
            timeToDepthIncrease = pendingDepthIncrease
            pendingDepthIncrease = 0


    t1 = time()
    print 'Tempo da BFS - vertice: ',root,': {}s'.format((t1-t0))


    return listas,root,dist

def printList(l):
    print "[",
    for i in l:
        print i ,
    print "]"

def printDataVertices(d):
    for v in d:
        print "Vértice:",v[1]
        cont = 0
        for c in v[0]:
            print "Camada",cont
            printList(c)
            cont +=1
        print "-"

def printDataVertice(d):
    cont = 0
    for c in d:
        print "Camada:",cont
        printList(c)
        cont +=1
    print "-"


def calculaDistancia(lm,ld,vm,vd,dist = None):

    delta = 0
    deltas = {}

    maxCamada = max(len(lm),len(ld))

    camada = 0
    #print "Distância",dist,vm,vd
    while(camada < maxCamada):
        #print " - Camada:",camada,
        try:
            delta += DTWDistance(lm[camada],ld[camada])
        except IndexError:
            delta = -1
        #print "Delta:",delta,
        deltas[camada] = delta
        camada += 1
    #print "---"

    return deltas,vm,vd,dist



def DTWDistance(s, t):
    s = deque(s)
    t = deque(t)
    n = len(s)
    m = len(t)

    s.append("x")
    s.rotate(1)
    t.append("x")
    t.rotate(1)
    #print s,t

    #print n,m,"n m"
    DTW = np.full((n + 1, m + 1),np.inf)

    DTW[0, 0] = 0

    for i in range(1,n+1):
      for j in range(1,m+1):
        cost = custo(s[i], t[j])
        #print i,j,cost
        DTW[i, j] = cost + min(DTW[i-1, j  ],    # insertion
                                   DTW[i  , j-1],   # deletion
                                   DTW[i-1, j-1])   # match
    #print DTW
    return DTW[n, m]

def custo(a,b):
    m = max(a,b)
    mi = min(a,b)

    return math.log((m * 1.0 ) / mi)

def verticesDistanciaK(g, root, k):


    vetor_marcacao = [0] * (max(g) + 1)

    queue = [root]
    vetor_marcacao[root] = 1
    

    depth = 0
    pendingDepthIncrease = 0
    timeToDepthIncrease = 1

    while queue:
        vertex = queue.pop(0)
        timeToDepthIncrease -= 1


        for v in g[vertex]:
            if(vetor_marcacao[v] == 0):
                vetor_marcacao[v] = 1
                queue.append(v)
                pendingDepthIncrease += 1    


        if(timeToDepthIncrease == 0):
            depth += 1
            if(depth == k):
                return queue
            timeToDepthIncrease = pendingDepthIncrease
            pendingDepthIncrease = 0

    return queue

















