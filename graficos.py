#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from random import sample
from itertools import permutations

def plotaGrafico(gpv,avgDistance,diameter):

    labels = []
    xmin = []; xmax = [] ; ymin = [] ; ymax = []
    cont = 0
    amount = len(gpv)
    Nlines = 200
    color_lvl = 8
    rgb = np.array(list(permutations(range(0,256,color_lvl),3)))/255.0
    colors = sample(rgb,amount)

    for k,v in gpv.iteritems():

        xmin.append(min(v['xs']))
        xmax.append(max(v['xs']))
        ymin.append(min(v['ys']))
        ymax.append(max(v['ys']))

        c = [float(cont)/float(amount), 0.0, float(amount-cont)/float(amount)]
        plt.plot(v['xs'],v['ys'], '-bo',color=colors[cont])
        cont += 1
        labels.append(r'(%i,%i)' % (k[0], k[1]))

    plt.legend(labels, ncol=4, loc='upper center', 
           bbox_to_anchor=(0.5, -0.1), 
           columnspacing=1.0, labelspacing=0.0,
           handletextpad=0.0, handlelength=1.5,
           fancybox=True, shadow=True)
    
    plt.ylabel('$\Delta(G_u^k,G_v^k)$')
    plt.xlabel('$k$')
    plt.grid()

    xmin = min(xmin); xmax = max(xmax); ymin = min(ymin); ymax = max(ymax)

    plt.axvline(x=avgDistance, color='blue', linestyle='--')
    plt.text(avgDistance+0.01,(ymax+1)-0.15,u'distância média',rotation=45,fontsize=8)
    plt.axvline(x=diameter, color='red', linestyle='--')
    plt.text(diameter+0.01,(ymax+1)-0.15,u'diâmetro',rotation=45,fontsize=8)

    plt.axis([xmin,xmax + 1,ymin,ymax + 1])
    plt.xticks(np.arange(xmin, xmax+1, 1.0))
    plt.savefig('deltas.png',bbox_inches='tight')
