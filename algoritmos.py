#!/usr/bin/env python
# -*- coding: utf-8 -*-

import graph

def bfs(g, root, maxDepth):
    visited, queue = [], [root]
    visited.append(root)
    pendingDepthIncrease = 0
    depth = 0
    timeToDepthIncrease = 1
    if(maxDepth == 0):
    	#print "Depth:",(depth)
        return visited
    while queue:
        vertex = queue.pop(0)

        timeToDepthIncrease -= 1
        l = list(set(g[vertex]) - set(visited))
        pendingDepthIncrease += len(l)
        print "Vizinhos V:",l,"V:",vertex,"timeToDepthIncrease:",timeToDepthIncrease,"pendingDepthIncrease:",pendingDepthIncrease

        visited, queue = adicionaVizinhos(g[vertex],visited,queue)

        if(timeToDepthIncrease == 0):
        	depth += 1
        	if(depth == maxDepth):
        		#print "Depth:",(depth)
        		return visited
        	timeToDepthIncrease = pendingDepthIncrease
        	pendingDepthIncrease = 0

        
        	#else:
        #print "Depth:",depth
        #print "-"
        #queue.remove(vertex)  
         
    return visited

def adicionaVizinhos(vv,visited,queue):
	for v in vv:
		if(v not in visited):
			visited.append(v)
			queue.append(v)
	return visited, queue

def montaBola(g, root, maxDepth):

    bola = {}

    visited, queue = [], [root]
    visited.append(root)
    bola[root] = []
    pendingDepthIncrease = 0
    depth = 0
    timeToDepthIncrease = 1
    if(maxDepth == 0):
        #print "Depth:",(depth)
        b = limitaBola(bola)
        return b,[root]

    verticesUltimaCamada = []

    while queue:
        vertex = queue.pop(0)

        timeToDepthIncrease -= 1
        l = list(set(g[vertex]) - set(visited))
        pendingDepthIncrease += len(l)
        #print "Vizinhos V:",l,"V:",vertex,"timeToDepthIncrease:",timeToDepthIncrease,"pendingDepthIncrease:",pendingDepthIncrease

        bola[vertex] = g[vertex]
        verticesUltimaCamada.append(vertex)

        visited, queue = adicionaVizinhos(g[vertex],visited,queue)

        if(timeToDepthIncrease == 0):
            depth += 1
            if(depth == (maxDepth + 1)):
                #print "Depth:",(depth - 1)
                b = limitaBola(bola)
                return b,verticesUltimaCamada
            timeToDepthIncrease = pendingDepthIncrease
            pendingDepthIncrease = 0
            verticesUltimaCamada = []

    #print "Depth:",(depth - 1)
    b = limitaBola(bola)
    return b,verticesUltimaCamada

def montaBolas(g, root, maxDepth):

    # Armazena todas as bolas de tamanho k (0 até maxDepth)
    bolas = {}

    bola = {}

    visited, queue = [], [root]
    visited.append(root)
    bola[root] = []
    pendingDepthIncrease = 0
    depth = 0
    timeToDepthIncrease = 1
    if(maxDepth == 0):
        #print "Depth:",(depth)
        bolas[depth] = limitaBola(bola)
        return bolas,[root]

    verticesUltimaCamada = []

    while queue:
        vertex = queue.pop(0)

        timeToDepthIncrease -= 1
        l = list(set(g[vertex]) - set(visited))
        pendingDepthIncrease += len(l)
        #print "Vizinhos V:",l,"V:",vertex,"timeToDepthIncrease:",timeToDepthIncrease,"pendingDepthIncrease:",pendingDepthIncrease

        bola[vertex] = g[vertex]
        verticesUltimaCamada.append(vertex)

        visited, queue = adicionaVizinhos(g[vertex],visited,queue)

        if(timeToDepthIncrease == 0):
            bolas[depth] = limitaBola(bola)
            depth += 1
            if(depth == (maxDepth + 1)):
                #print "Depth:",(depth - 1)
                return bolas,verticesUltimaCamada
            timeToDepthIncrease = pendingDepthIncrease
            pendingDepthIncrease = 0
            verticesUltimaCamada = []

    #print "Depth:",(depth - 1)
    bolas[depth] = limitaBola(bola)
    return bolas,verticesUltimaCamada

def montaBolaComArestasUltimaCamada(g, root, maxDepth):
    bola, verticesUltimaCamada = montaBola(g, root, maxDepth)
    return bola,root,maxDepth

def montaBolasComArestasUltimaCamada(g, root, maxDepth):
    bolas, verticesUltimaCamada = montaBolas(g, root, maxDepth)
    bolas = completaBola(bolas,maxDepth)
    return bolas,root,maxDepth

def completaBola(bolas,maxDepth):
    qtdBolas = len(bolas) - 1
    if(qtdBolas < maxDepth):
        cont = qtdBolas
        while(cont <= maxDepth):
            bolas[cont] = bolas[cont - 1]
            cont +=1
    return bolas



def montaBolaSemArestasUltimaCamada(g, root, maxDepth):
    bola, verticesUltimaCamada = montaBola(g, root, maxDepth)
    bola = removeVerticesUltimaCamada(bola,verticesUltimaCamada)
    return bola

def removeVerticesUltimaCamada(bola,vs):
    bola_nova = {}
    for k,ver in bola.iteritems():
        vss = []
        for v in ver:
            if(not all(x in vs for x in [k,v])):
                vss.append(v)
        bola_nova[k] = vss
    return bola_nova


def converteBolaEmGrafo(b):
    g = graph.Graph()
    for k,v in b.iteritems():
        g[k] = v
    return g

def limitaBola(bola):
    #return limitaBola2(bola)
    #######
    keys = set()
    new_bola = {}
    for key,value in bola.iteritems():
    	keys.add(key)
    for key,value in bola.iteritems():
    	s_value = list(set(value).intersection(keys))
    	new_bola[key] = s_value

    return new_bola

def limitaBola2(bola):
    keys = set()
    new_bola = {}
    for key,value in bola.iteritems():
        keys.add(key)
    for key,value in bola.iteritems():
        novos_valores = []
        s_value = list(set(value).intersection(keys))
        for v in value:
            if(v not in s_value):
                novos_valores.append('e')
            else:
                novos_valores.append(v)
        new_bola[key] = novos_valores

    return new_bola

