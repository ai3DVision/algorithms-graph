#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Graph utilities."""

import graph

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


def degreeSequenceEditDistanceComArvores(Am,Ad,Vm,Vd,kk):

  graus = {}
  
  for k,v in Am.iteritems():
    g = len(v['filhos'])
    camada = v['camada']
    if(camada not in graus):
      graus[camada] = {}
    if(g not in graus[camada]):
      graus[camada][g] = {}
      graus[camada][g]['m'] = 0
      graus[camada][g]['d'] = 0
    graus[camada][g]['m'] += 1
  for k,v in Ad.iteritems():
    g = len(v['filhos'])
    camada = v['camada']
    if(camada not in graus):
      graus[camada] = {}
    if(g not in graus[camada]):
      graus[camada][g] = {}
      graus[camada][g]['m'] = 0
      graus[camada][g]['d'] = 0
    graus[camada][g]['d'] += 1
  
  delta_grau = 0
  for camada,graus_da_camada in graus.iteritems():
    for grau,v in graus_da_camada.iteritems():
      qtdGrauGm = v['m']
      qtdGrauGd = v['d']
      #print "Camada",camada,"Grau",grau,"Grau Am",qtdGrauGm,"Grau Ad",qtdGrauGd

      delta_grau += abs(qtdGrauGm - qtdGrauGd)


  return delta_grau,Vm,Vd,kk


def degreeSequenceEditDistanceComArvoresSemCamadas(Am,Ad,Vm,Vd,kk):

  graus = {}
  
  for k,v in Am.iteritems():
    g = len(v['filhos'])
    if(g not in graus):
      graus[g] = {}
      graus[g]['m'] = 0
      graus[g]['d'] = 0
    graus[g]['m'] += 1
  for k,v in Ad.iteritems():
    g = len(v['filhos'])
    if(g not in graus):
      graus[g] = {}
      graus[g]['m'] = 0
      graus[g]['d'] = 0
    graus[g]['d'] += 1
  
  delta_grau = 0
  for grau,v in graus.iteritems():
    qtdGrauGm = v['m']
    qtdGrauGd = v['d']
    #print "Camada",camada,"Grau",grau,"Grau Am",qtdGrauGm,"Grau Ad",qtdGrauGd

    delta_grau += abs(qtdGrauGm - qtdGrauGd)


  return delta_grau,Vm,Vd,kk



