#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Graph utilities."""

import math
import random
from random import shuffle
import numpy as np
from scipy.linalg import fractional_matrix_power
from numpy import linalg as LA
import operator
import collections



def printBinaryMatrix(G):
  nodes = sorted(list(G.nodes()))
  matrixLines = ""
  od = collections.OrderedDict(sorted(G.items()))
  for key,value in od.iteritems():
    #line = str(key)+":\t"
    line = ""
    for node in nodes:
      if(node in value):
        line += "1 "
      else:
        line += "0 "
    line = line[:-1]
    line += "\n"
    matrixLines += line
  print matrixLines

def binaryMatrix(G):
  nodes = sorted(list(G.nodes()))
  matriz = np.zeros(shape=(len(nodes),len(nodes)))
  od = collections.OrderedDict(sorted(G.items()))
  for key,value in od.iteritems():
    #line = str(key)+":\t"
    line = []
    cont = 0
    for node in nodes:
      if(node in value):
        line.append(1)
      else:
        line.append(0)

    for n in nodes:
      if(n == key):
        break
      cont += 1
    matriz[cont] = line
  return matriz

def transitionProbabilityMatrix(G):
  matriz = {}
  nodes = sorted(list(G.nodes()))
  od = collections.OrderedDict(sorted(G.items()))
  for key,value in od.iteritems():
    m = {}
    s = len(value)
    for node in nodes:
      if(node in value):
        m[node] = (1.0/s)
    matriz[key] = m
  return matriz


def printTransitionProbabilityMatrix(m):
  nodes = sorted(m.keys())
  matrixLines = ""
  for key,value in m.iteritems():
    line = ""
    for node in nodes:
      if(node in value):
        line += '%.2f'%(value[node])+"\t"
      else:
        line += "0\t"
    line = line[:-1]
    line += "\n"
    matrixLines += line
  print matrixLines

def  diagonalDegreeMatrix(m):
  nodes = sorted(m.keys())
  matriz = np.zeros(shape=(len(nodes),len(nodes)))
  for key,value in m.iteritems():
    s = sum(value.values())
    if(s != 0):
      s = 1.0 / s
    cont = 0
    for n in nodes:
      if(n == key):
        matriz[cont,cont] = s
        break
      cont += 1
  return matriz

def  diagonalDegreeMatrixFromBinaryMatrix(m):
  matriz = np.zeros(shape=(len(m),len(m)))
  cont = 0
  for v in m:
    s = sum(v)
    if(s != 0):
      s = 1.0 / s
    matriz[cont,cont] = s
    cont += 1
  return matriz

def calculaW(d,a):
  d = np.matrix(d)
  a = np.matrix(a)
  dd = fractional_matrix_power(d,0.5)
  w = dd*a*dd
  return w

def scaledLeadingEigenvector(w,G):
  av, avet = LA.eig(w)
  nodes = sorted(list(G.nodes()))
  g_node = []
  for node in nodes:
    #print node, len(G[node])
    g_node.append(math.sqrt(len(G[node])))
  #print avet[0]
  phi_ = np.matrix(avet[0]) / np.matrix(g_node)
  return phi_

def trataPhi(phi,G):
  nodes_phi = {}
  nodes = sorted(list(G.nodes()))
  x = 0
  phi = phi.tolist()[0]
  for node in nodes:
    nodes_phi[node] = phi[x]
    x += 1
  return nodes_phi


def caminhaNoPhi(phi,G):
  phi = trataPhi(phi,G)
  print phi

  ## maior phi e seu nó
  maxNode = max(phi.iteritems(), key=operator.itemgetter(1))[0]

  path = [maxNode]
  visited = [maxNode]

  while len(visited) < len(G.nodes()):
    cur = path[-1]
    nosAVisitar = list(set(G[cur]) - set(visited))
    if nosAVisitar:
      proxNo = verificaMaiorVizinho(nosAVisitar,phi)
    else:
      print "Não tenho mais vizinho para visitar...saltando..."
      nosAVisitar = list(set(G.keys()) - set(visited))
      proxNo = verificaMaiorVizinho(nosAVisitar,phi)
    visited.append(proxNo)
    path.append(proxNo)

  print "Caminho percorrido:",path

  return path


def verificaMaiorVizinho(vizs,phi):

  phi_v = {}
  for key,value in phi.iteritems():
    if(key in vizs):
      phi_v[key] = value

  maxPhi = phi_v.itervalues().next()

  maxPhi_v = -1
  for key,value in phi_v.iteritems():
    if(value >= maxPhi):
      maxPhi = value
      maxPhi_v = key

  return maxPhi_v 

def buscaEmW(a,b,W,G):
  nodes = sorted(list(G.nodes()))

  cont1 = 0
  for n in W:
    if(nodes[cont1] == a):
      cont2 = 0
      for nn in n:
        if(nodes[cont2] == b):
          return nn
        cont2 += 1
    cont1 +=1    



def criaMatrisesOfCompatibilityWeights(Wm,Wd,Sm,Sd,Gm,Gd):
  Nm = sorted(list(Gm.nodes()))
  Nd = sorted(list(Gd.nodes()))

  Wm = Wm.tolist()
  Wd = Wd.tolist()

  if(len(Sm) > len(Sd)):
    tam = len(Sm)
  else:
    tam = len(Sd)
  Rm = np.zeros(shape=(tam,tam))
  Rd = np.zeros(shape=(tam,tam))

  tamSm = len(Sm)
  tamSd = len(Sd)

  cont1 = 0
  cont2 = 0
  while cont1 < tamSm:
    cont2 = 0
    while cont2 < tamSm:
      Rm[cont1][cont2] = buscaEmW(Sm[cont1],Sm[cont2],Wm,Gm)
      cont2 += 1
    cont1 += 1

  cont1 = 0
  cont2 = 0
  while cont1 < tamSd:
    cont2 = 0
    while cont2 < tamSd:
      Rd[cont1][cont2] = buscaEmW(Sd[cont1],Sd[cont2],Wd,Gd)
      cont2 += 1
    cont1 += 1

  pe = calculaPe(tamSm,tamSd)

  if(len(Wm[0]) < tam):
    diff = tam - len(Wm[0])
    cont1 = len(Wm[0])
    cont2 = 0
    while cont1 < tam:
      while cont2 < tam:
        Rm[cont2][cont1] = pe
        Rm[cont1][cont2] = pe
        cont2 += 1
      cont1 += 1

  if(len(Wd[0]) < tam):
    diff = tam - len(Wd[0])
    cont1 = len(Wd[0])
    cont2 = 0
    while cont1 < tam:
      while cont2 < tam:
        Rd[cont2][cont1] = pe
        Rd[cont1][cont2] = pe
        cont2 += 1
      cont1 += 1

  return Rm, Rd

def calculaPe(tamSm,tamSd):
  return (2.0 * abs(tamSm - tamSd)) / (tamSm + tamSd)

def beta(i,j,Gm,Gd):
  d_i = len(Gd[i])
  d_j = len(Gm[j])
  try:
    beta_ = math.exp( - (max(d_i,d_j) - min(d_i,d_j)) / max(d_i,d_j) )
  except ZeroDivisionError:
    beta_ = 0
  return beta_


def criaLattice(Sm,Sd,Gm,Gd,Wm,Wd):
  Rm, Rd = criaMatrisesOfCompatibilityWeights(Wm,Wd,Sm,Sd,Gm,Gd)
  print "Matrizes criadas"
  print "Rm:",Rm
  print "Rd:",Rd
  tam = len(Rm)
  matriz = []

  ### cria matriz vazia
  cont_d = 0
  cont_m = 0
  while cont_d < tam:
    cont_m = 0
    linha = []
    while cont_m < tam:
      m = []
      linha.append(m)
      cont_m += 1
    matriz.append(linha)
    cont_d += 1

  cont_d = 0
  cont_m = 0
  while cont_d < tam:
    cont_m = 0
    while cont_m < tam:
      x = calculaPesosArestasVertice(cont_m,cont_d,Sm,Sd,Gm,Gd,Rm,Rd)
      matriz[cont_d][cont_m] = x
      cont_m += 1
    cont_d += 1

  return matriz

def p_lattice(i_a,i_b,i_c,i_d,Gm,Gd,Rm,Rd,Sm,Sd):

  evitaBeta = False

  try:
    a = Sd[i_a]
  except IndexError:
    evitaBeta = True
  try:
    b = Sm[i_b]
  except IndexError:
    evitaBeta = True
  try:
    c = Sd[i_c]
  except IndexError:
    evitaBeta = True
  try:
    d = Sm[i_d]
  except IndexError:
    evitaBeta = True

  #print "Calculando transição ->","a:",a,"b:",b,"c:",c,"d:",d
  #print beta(a,b,Gm,Gd),beta(c,d,Gm,Gd),Rd[i_a,i_c],Rm[i_b,i_d]

  if(not evitaBeta):
    b = beta(a,b,Gm,Gd)*beta(c,d,Gm,Gd)*Rd[i_a,i_c]*Rm[i_b,i_d]
  else:
    b = Rd[i_a,i_c]*Rm[i_b,i_d]

  return b


def calculaPesosArestasVertice(cont_m,cont_d,Sm,Sd,Gm,Gd,Rm,Rd):

  pesos = []

  #print "Para os vértices:","a",Sd[cont_d],"b",Sm[cont_m]

  # Visita vértice da direita
  #print "Visita vértice da direita"
  if(cont_m == (len(Rm) - 1)):
    x = 'ne'
  else:
    x = p_lattice(cont_d,cont_m,cont_d,cont_m+1,Gm,Gd,Rm,Rd,Sm,Sd)
  pesos.append(x)

    # Visita vértice da direita inferior
  #print "Visita vértice da direita inferior"
  if(cont_m == (len(Rm) - 1) or cont_d == (len(Rd) - 1)):
    x = 'ne'
  else:
    x = p_lattice(cont_d,cont_m,cont_d+1,cont_m+1,Gm,Gd,Rm,Rd,Sm,Sd)
  pesos.append(x)

  # Visita vértice debaixo
  #print "Visita vértice debaixo"
  if(cont_d == (len(Rd) - 1)):
    x = 'ne'
  else:
    x = p_lattice(cont_d,cont_m,cont_d+1,cont_m,Gm,Gd,Rm,Rd,Sm,Sd)
  pesos.append(x)

  ################ visita uma cruz com o vértice no meio
  # Visita vértice de cima
  #print "Visita vértice de cima"
  # a = Sd[cont_d]
  # b = Sm[cont_m]
  # if(cont_d == 0):
  #   x = 'ne'
  # else:
  #   aa = Sd[cont_d-1]
  #   x = p_lattice(cont_d,cont_m,cont_d-1,cont_m,Gm,Gd,Rm,Rd,Sm,Sd)
  # pesos.append(x)

  # Visita vértice da esquerda
  #print "Visita vértice da esquerda"
  # a = Sd[cont_d]
  # b = Sm[cont_m]
  # if(cont_m == 0):
  #   x = 'ne'
  # else:
  #   bb = Sm[cont_m-1]
  #   x = p_lattice(cont_d,cont_m,cont_d,cont_m-1,Gm,Gd,Rm,Rd,Sm,Sd)
  # pesos.append(x)


  ################ visita um X com o vértice no meio
  # Visita vértice da esquerda superior
  #print "Visita vértice da esquerda superior"
  # a = Sd[cont_d]
  # b = Sm[cont_m]
  # if(cont_m == 0 or cont_d == 0):
  #   x = 'ne'
  # else:
  #   bb = Sm[cont_m-1]
  #   aa = Sm[cont_d-1]
  #   x = p_lattice(cont_d,cont_m,cont_d-1,cont_m-1,Gm,Gd,Rm,Rd,Sm,Sd)
  # pesos.append(x)

  # Visita vértice da esquerda inferior
  #print "Visita vértice da esquerda inferior"
  # a = Sd[cont_d]
  # b = Sm[cont_m]
  # if(cont_m == 0 or cont_d == (len(Sd) - 1)):
  #   x = 'ne'
  # else:
  #   bb = Sm[cont_m-1]
  #   aa = Sm[cont_d+1]
  #   x = p_lattice(cont_d,cont_m,cont_d+1,cont_m-1,Gm,Gd,Rm,Rd,Sm,Sd)
  # pesos.append(x)

  # Visita vértice da direita superior
  #print "Visita vértice da direita superior"
  # a = Sd[cont_d]
  # b = Sm[cont_m]
  # if(cont_m == (len(Sm) - 1) or cont_d == 0):
  #   x = 'ne'
  # else:
  #   bb = Sm[cont_m+1]
  #   aa = Sm[cont_d-1]
  #   x = p_lattice(cont_d,cont_m,cont_d-1,cont_m+1,Gm,Gd,Rm,Rd,Sm,Sd)
  # pesos.append(x)

  #print "Pesos:",pesos

  return pesos





















  








