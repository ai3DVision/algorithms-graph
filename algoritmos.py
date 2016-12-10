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
        return converteBolaEmGrafo(b),[root]

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
                return converteBolaEmGrafo(b),verticesUltimaCamada
            timeToDepthIncrease = pendingDepthIncrease
            pendingDepthIncrease = 0
            verticesUltimaCamada = []

    #print "Depth:",(depth - 1)
    b = limitaBola(bola)
    return converteBolaEmGrafo(b),verticesUltimaCamada

def montaBolaComArestasUltimaCamada(g, root, maxDepth):
    bola, verticesUltimaCamada = montaBola(g, root, maxDepth)
    return bola

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
    return converteBolaEmGrafo(bola_nova)




def converteBolaEmGrafo(b):
    g = graph.Graph()
    for k,v in b.iteritems():
        g[k] = v
    return g

def limitaBola(bola):
	keys = set()
	new_bola = {}
	for key,value in bola.iteritems():
		keys.add(key)
	for key,value in bola.iteritems():
		s_value = list(set(value).intersection(keys))
		new_bola[key] = s_value

	return new_bola

