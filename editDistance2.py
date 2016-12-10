#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Graph utilities."""

import graph

def degreeSequenceEditDistance(Gm,Gd):
  maiorGrau = 0
  for node in Gm.nodes():
    gn = len(Gm[node])
    if(gn > maiorGrau):
      maiorGrau = gn
  for node in Gd.nodes():
    gn = len(Gd[node])
    if(gn > maiorGrau):
      maiorGrau = gn

  grau = 0
  delta_grau = 0
  while grau <= maiorGrau:
    qtdGrauGm = 0
    qtdGrauGd = 0
    for node in Gm.nodes():
      gn = len(Gm[node])
      if(gn == grau):
        qtdGrauGm +=1
    for node in Gd.nodes():
      gn = len(Gd[node])
      if(gn == grau):
        qtdGrauGd +=1
    delta_grau += abs(qtdGrauGm - qtdGrauGd)
    grau += 1

  return delta_grau



