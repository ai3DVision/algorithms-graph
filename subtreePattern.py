#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
import sys

class No(object):

    def __init__(self,id,label,camada):
        self.id = id
        self.label = label
        self.camada = camada
        self.filhos = set()

    def adicionaFilhos(self,list):
        self.filhos.update(list)

    def dados(self):
        print "Id:",self.id,"Label:",self.label,"Camada:",self.camada
        if(self.filhos):
            print "Filhos:",
            for f in self.filhos:
                print "(Id:",f.id,"Label:",f.label,"Camada:",f.camada,") ",
            print ""

def criaNo(label,camada,arvore,cont_id):
    no = {}
    no['id'] = cont_id
    no['label'] = label
    no['camada'] = camada
    no['filhos'] = []
    cont_id += 1
    arvore[no['id']] = no
    return no,cont_id

def criaNos(lista,camada,arvore,cont):
    listaNo = []
    for l in lista:
        no,cont = criaNo(l,camada,arvore,cont)
        listaNo.append(no)
    return listaNo,cont

def procuraPrimeiroNoComLabel(label,arvore):

    for k,v in arvore.iteritems():
        if(v['label'] == label):
            return v

def adicionaFilhos(no,nos):
    # não verifica se possui filhos repetidos
    no['filhos'].extend(nos)

def criaArvores(g, root, maxDepth):

    # Armazena todas as arvores de tamanho k (0 até maxDepth)
    arvores = {}


    cont_id = 0
    arvore = {}

    bola = {}
    bola[root] = []

    visited, queue = [], [root]
    visited.append(root)
    
    depth = 0
    
    noC,cont_id = criaNo(root,depth,arvore,cont_id)

    pendingDepthIncrease = 0
    
    timeToDepthIncrease = 1
    if(maxDepth == 0):
        arvores[depth] = arvore
        return arvores


    while queue:
        vertex = queue.pop(0)

        no = procuraPrimeiroNoComLabel(vertex,arvore)

        bola[vertex] = g[vertex]

        timeToDepthIncrease -= 1
        l = list(set(g[vertex]) - set(visited))
        pendingDepthIncrease += len(l)

        nos,cont_id = criaNos(g[vertex],depth + 1,arvore,cont_id)

        adicionaFilhos(no,nos)


        visited, queue = adicionaVizinhos(g[vertex],visited,queue)

        if(timeToDepthIncrease == 0):

            b = limitaBola(bola)
            a = limitaArvore(arvore,b)
            arvores[depth] = a

            depth += 1
            if(depth == (maxDepth + 1)):
                
                return arvores

            timeToDepthIncrease = pendingDepthIncrease
            pendingDepthIncrease = 0

    b = limitaBola(bola)
    a = limitaArvore(a,b)
    arvores[depth] = a
    return arvores


def criaArvore(g, root, maxDepth):

    cont_id = 0
    arvore = {}
    bola = {}
    bola[root] = []

    visited, queue = [], [root]
    visited.append(root)
    
    depth = 0
    
    noC,cont_id = criaNo(root,depth,arvore,cont_id)

    pendingDepthIncrease = 0
    
    timeToDepthIncrease = 1
    if(maxDepth == 0):
        return arvore


    while queue:
        vertex = queue.pop(0)

        no = procuraPrimeiroNoComLabel(vertex,arvore)
        bola[vertex] = g[vertex]

        timeToDepthIncrease -= 1
        l = list(set(g[vertex]) - set(visited))
        pendingDepthIncrease += len(l)

        nos,cont_id = criaNos(g[vertex],depth + 1,arvore,cont_id)

        adicionaFilhos(no,nos)


        visited, queue = adicionaVizinhos(g[vertex],visited,queue)

        if(timeToDepthIncrease == 0):
            depth += 1
            if(depth == (maxDepth + 1)):
                b = limitaBola(bola)
                arvore = limitaArvore(arvore,b)
                return arvore

            timeToDepthIncrease = pendingDepthIncrease
            pendingDepthIncrease = 0

    b = limitaBola(bola)
    arvore = limitaArvore(arvore,b)
    return arvore

def criaArvoresComRetornos(g, root, maxDepth):
    arvs = criaArvores(g, root, maxDepth)
    arvs = completaBola(arvs,maxDepth)
    return arvs,root, maxDepth

def completaBola(bolas,maxDepth):
    qtdBolas = len(bolas) - 1
    if(qtdBolas < maxDepth):
        cont = qtdBolas
        while(cont <= maxDepth):
            bolas[cont] = bolas[cont - 1]
            cont +=1
    return bolas

def limitaBola(bola):
    keys = set()
    new_bola = {}
    for key,value in bola.iteritems():
        keys.add(key)
    for key,value in bola.iteritems():
        s_value = list(set(value).intersection(keys))
        new_bola[key] = s_value

    return new_bola

def listaVerticesBola(b):
    vertices = set()
    for k,v in b.iteritems():
        vertices.add(k)
        vertices.update(v)
    return vertices


def limitaArvore(arvore,b):

    vertices = listaVerticesBola(b)

    arv = {}

    cont_id = 0

    for k,v in arvore.iteritems():
        if(v['label'] in vertices):
            noC,cont_id = criaNo(v['label'],v['camada'],arv,cont_id)
            filhos_k = []
            if('filhos' in v):
                for f in v['filhos']:
                    if(f['label'] in vertices):
                        filhos_k.append(f)
                adicionaFilhos(noC,filhos_k)

    return arv

def adicionaVizinhos(vv,visited,queue):
    for v in vv:
        if(v not in visited):
            visited.append(v)
            queue.append(v)
    return visited, queue


def printArvore(arv):
    for k,v in arv.iteritems():
        tamObj = float(sys.getsizeof(v))/1024
        print "Tamanho do nó",v['label'],":",tamObj,"KB"
        printNo(v)
    print "--"

def printNo(no):
    print "Id:",no['id'],"Label:",no['label'],"Camada:",no['camada']
    if(no['filhos']):
        print "Filhos:",
        for f in no['filhos']:
            print "(Id:",f['id'],"Label:",f['label'],"Camada:",f['camada'],") ",
        print ""









