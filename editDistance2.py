#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Graph utilities."""

import graph
import subtreePattern
import copy
from time import time
import sys

def degreeSequenceEditDistance(Gm,Gd,Vm,Vd,kk):

  graus = {}
  
  for node,v in Gm.iteritems():
    g = len(Gm[node])
    if(g not in graus):
      graus[g] = {}
      graus[g]['m'] = 0
      graus[g]['d'] = 0
    graus[g]['m'] += 1
  for node,v in Gd.iteritems():
    g = len(Gd[node])
    if(g not in graus):
      graus[g] = {}
      graus[g]['m'] = 0
      graus[g]['d'] = 0
    graus[g]['d'] += 1
  
  delta_grau = 0
  for k,v in graus.iteritems():
    qtdGrauGm = v['m']
    qtdGrauGd = v['d']

    delta_grau += abs(qtdGrauGm - qtdGrauGd)


  return delta_grau,Vm,Vd,kk

def retiraVerticesDeOutrasCamadas(A,maxCamada):

  if(maxCamada >= len(A) - 1):
    return A

  vertices = []
  maiorId = 0
  for k in A:
    for v in k:
      if(v.label > maiorId):
        maiorId = v.label

  vetor_marcacao = [0] * (maiorId + 1)

  tamOriginal = len(A)
  A_n = copy.deepcopy(A)
  
  

  #print "Tamanho antigo da árvore:",tamOriginal

  contCamada = maxCamada + 1
  while(contCamada < tamOriginal):
    for v in A_n[contCamada]:
      vetor_marcacao[v.label] = 1
    contCamada += 1

  contCamada = maxCamada + 1
  while(contCamada < tamOriginal):
    A_n.pop()
    contCamada += 1

  # Última camada vazia
  A_n.append([])

  
  #print "Novo tamanho da árvore:",len(A_n)

  for k in A_n:
    for v in k:
      vet_f = []
      for f in v.filhos:
        if(vetor_marcacao[f] == 0):
          vet_f.append(f)
      v.filhos = vet_f
      v.qtdFilhos = len(vet_f)

  return A_n


def apenasApagaCamadas(A,maxCamada):

  if(maxCamada >= len(A) - 1):
    return A


  tamOriginal = len(A)
  A_n = copy.deepcopy(A)
  
  

  #print "Tamanho antigo da árvore:",tamOriginal


  contCamada = maxCamada + 1
  while(contCamada < tamOriginal):
    A_n.pop()
    contCamada += 1

  # Última camada vazia
  A_n.append([])

  
  #print "Novo tamanho da árvore:",len(A_n)

  return A_n


def buscaMaiorId(A):
  maiorId = 0
  for k in A:
    for v in k:
      if(v.label > maiorId):
        maiorId = v.label

  return maiorId

def calculaDeltas(Am,Ad):

  t0 = time()

  #Am = apenasApagaCamadas(Am,maxCamada)
  #Ad = apenasApagaCamadas(Ad,maxCamada)

  v1 = Am[0][0].label
  v2 = Ad[0][0].label

  #subtreePattern.printArvore(Am)
  #subtreePattern.printArvore(Ad)

  maxCamadaComum = max(len(Am),len(Ad))

  delta_grau = 0
  deltas_graus = {}

  filhos_na_camada_m_a = []
  filhos_na_camada_d_a = []

  maiorIdm = buscaMaiorId(Am)
  maiorIdd = buscaMaiorId(Ad)

  #print " "
  #print "MaxCamada",maxCamada,"Vértices",v1,v2

  camada = 0
  while (camada < maxCamadaComum):

    graus = set()
    # Grau de vértices sem filhos
    graus.add(0)

    filhos_na_camada_m = []
    filhos_na_camada_d = []
    vertices_na_camada_m = [0] * (maiorIdm + 1)
    vertices_na_camada_d = [0] * (maiorIdd + 1)

    try:
      f = []
      vs = []
      for v in Am[camada]:
        graus.add(v.qtdFilhos)
        filhos_na_camada_m.extend(v.filhos)
        vertices_na_camada_m[v.label] = 1

      f = []
      vs = []
      for v in Ad[camada]:
        graus.add(v.qtdFilhos)
        filhos_na_camada_d.extend(v.filhos)
        vertices_na_camada_d[v.label] = 1

    except IndexError:
      pass

    dm = {}
    dd = {}
    for g in graus:
      dm[g] = 0
      dd[g] = 0

    try:
      for v in Am[camada]:
        dm[v.qtdFilhos] += 1
      for v in Ad[camada]:
        dd[v.qtdFilhos] += 1
    except IndexError:
      pass

    #print "Camada: ",camada

    if(camada > 0):
      qtd_v_zero_m = trataVerticesComZeroFilhos(filhos_na_camada_m_a,vertices_na_camada_m)
      qtd_v_zero_d = trataVerticesComZeroFilhos(filhos_na_camada_d_a,vertices_na_camada_d)
      filhos_na_camada_m_a = filhos_na_camada_m
      filhos_na_camada_d_a = filhos_na_camada_d

      dm[0] = qtd_v_zero_m
      dd[0] = qtd_v_zero_d

    #print "-"
    #print dm
    #print dd

    for g in graus:
      vm = dm[g]
      vd = dd[g]
      delta_grau += abs(vm - vd)

    deltas_graus[camada] = delta_grau

    camada += 1

  t1 = time()
  print 'Tempo do cálculo de similaridade - vértices: ',v1,v2,': {}s'.format((t1-t0))
  #print "Delta",delta_grau
  #print "-----"

  return deltas_graus,v1,v2




def trataVerticesComZeroFilhos(filhos_na_camada,vertices_na_camada):
  try:
    qtd_vertices_zero_filhos = len(diff2(filhos_na_camada,vertices_na_camada))
  except IndexError:
    qtd_vertices_zero_filhos = 0
     
  return qtd_vertices_zero_filhos

def diff(a, b):
  b_c = list(b)
  diff = []
  for aa in a:
    if aa not in b_c:
      diff.append(aa)
    else:
      b_c.remove(aa)
  return diff

def diff2(a, b):
  diff = []
  for aa in a:
    if b[aa] == 0:
      diff.append(aa)
    else:
      b[aa] = 0
  return diff





