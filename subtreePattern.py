#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime
from time import time

class No(object):
    def __init__(self,label,qtdFilhos=0,filhos=[]):
        self.label = label
        self.qtdFilhos = qtdFilhos
        self.filhos = filhos


def criaNo(label,qtdFilhos,filhos,arvore,camada):
    no = No(label,qtdFilhos,filhos)
        
    arvore[camada].append(no)

def trataG(g):
    d_g_para_novo_g = {}
    d_novo_g_para_g = {}
    cont = 0
    for k,v in g.iteritems():
        d_g_para_novo_g[k] = cont
        d_novo_g_para_g[cont] = k
        cont += 1
    cont = 0

    return d_g_para_novo_g,d_novo_g_para_g

def geraNovoG(rel_g,g):
    g_n = {}
    for k,vizinhos in g.iteritems():
        vec = []
        for v in vizinhos:
            vec.append(rel_g[v])
        g_n[rel_g[k]] = vec
    return g_n

def recuperaLabelsArvore(rel_g,a):
    a_n = []
    cont = 0
    for camada in a:
        a_n.append([])
        for v in camada:
            a_n[cont].append(rel_g[v.label])
        cont += 1

    return a_n

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

def criaArvore(g, root):
    #t0 = time()
    #rel_g_para_g_novo,rel_g_novo_para_g = trataG(g_a)
    #g = geraNovoG(rel_g_para_g_novo,g_a)
    #t1 = time()
    #print 'Tempo pra converter grafo: {}s'.format((t1-t0))
    

    arvore = []

    t0 = time()

    vetor_marcacao = [0] * (max(g) + 1)
    #print sys.getsizeof(vetor_marcacao)/1024,"KB"

    # Marcar s e inserir s na fila Q
    queue = [root]
    vetor_marcacao[root] = 1
    
    arvore.append([])

    depth = 0
    pendingDepthIncrease = 0
    timeToDepthIncrease = 1
    
    criaNo(root,len(g[root]),g[root],arvore,depth)

    arvore.append([])

    while queue:
        vertex = queue.pop(0)
        timeToDepthIncrease -= 1

        #no = procuraPrimeiroNoComLabel(vertex,arvore)
        #if(no == None):
        #    no = criaNo(vertex,depth,arvore)

        #no.qtdFilhos = len(g[vertex])
        #no.filhos = g[vertex]



        for v in g[vertex]:
            if(vetor_marcacao[v] == 0):
                vetor_marcacao[v] = 1
                queue.append(v)
                pendingDepthIncrease += 1
                criaNo(v,len(g[v]),g[v],arvore,depth + 1)
            #else:
            #    criaNo(v,0,[],arvore,depth + 1)     


        if(timeToDepthIncrease == 0):
            depth += 1
            arvore.append([])
            timeToDepthIncrease = pendingDepthIncrease
            pendingDepthIncrease = 0


    t1 = time()
    print 'Tempo da BFS - vertice: ',root,': {}s'.format((t1-t0))

    #t0 = time()
    #arvore = recuperaLabelsArvore(rel_g_novo_para_g,arvore)
    #t1 = time()
    #print 'Tempo pra converter grafo: {}s'.format((t1-t0))
    return arvore,root
    


def printArvore(arv):
    cont = 0
    filhos_a = [0]
    for camada in arv:
        #print camada
        if(camada or filhos_a):
            print "Camada:",cont

            nos = []
            filhos = []
            for v in camada:
                filhos.extend(v.filhos)
                printNo(v)
                nos.append(v.label)

            filhos_zero = diff(filhos_a,nos)

            if filhos_zero:
                print "Vértices com zero filhos:",filhos_zero

            filhos_a = filhos

            cont += 1
    print "--"

def printNo(no):
        print "Label:",no.label,"Qtd Filhos:",no.qtdFilhos,"Filhos:",no.filhos

def diff(a, b):
  b_c = list(b)
  diff = []
  for aa in a:
    if aa not in b_c:
      diff.append(aa)
    else:
      b_c.remove(aa)
  return diff
















