#!/usr/bin/env python
# -*- coding: utf-8 -*-

### arquivos utilizados
import graph, editDistance2, algoritmos, graficos, utilitarios, calculos
from multiprocessing.pool import ThreadPool
from concurrent.futures import ProcessPoolExecutor, as_completed
import collections

######
import argparse,random,math,pickle
import graph_tool.all as gt
from time import time

def escolhaDoisVertices():
	v1 = rand.choice(G.keys())
	v2 = rand.choice(G.keys())
	while v1 == v2:
		v2 = rand.choice(G.keys())
	return v1,v2

def escolhaDoisVerticesDistanciaK(k):
	print "Chamou vértices a distância",k
	v1 = rand.choice(G.keys())
	vizinhos_distancia_k = calculos.verticesDistanciaK(dictG,v1,k)
	while(not vizinhos_distancia_k):
		k -= 1
		vizinhos_distancia_k = calculos.verticesDistanciaK(dictG,v1,k)

	#print "Vértice",v1
	#print "Vizinhos a distância",k,":",vizinhos_distancia_k
	v2 = rand.choice(vizinhos_distancia_k)
	return v1,v2

def montaListas(v1,v2,dist):

	futures = []
	with ProcessPoolExecutor(max_workers=10) as executor:

		futures.append(executor.submit(calculos.geraListas, dictG, v1, dist))
		futures.append(executor.submit(calculos.geraListas, dictG, v2, dist))
			
		resultados = []
		for f in as_completed(futures):
			res = f.result()
			resultados.append(res)

	resultadosConsolidados = []
	for r in resultados:
		resultadosConsolidados.append({'label': r[1], 'listas': r[0], 'dist': r[2]})

	
	return resultadosConsolidados

rand=random.Random()

parser = argparse.ArgumentParser(description='Criar bolas por vértices.')
parser.add_argument('--grafo', nargs='?', required=True,
                      help='Input graph file')
parser.add_argument('--qtdPares', default=2, type=int, required=True,
                      help='Quantidade de pares')
parser.add_argument('--listDist', type=str, required=False,
                      help='Distancia')

args = parser.parse_args()

d_list = args.listDist.split(',') # ['1','2','3','4']
#d_list = map(int, d_list)

print " - Carregando matriz de adjacência para Grafo (na memória)..."
G = graph.load_adjacencylist(args.grafo,undirected=True)
print " - Convertendo grafo para Dict (na memória)..."
dictG = G.gToDict()

#print " - Criando arquivo .dot temporário..."
utilitarios.criaArquivoDot(G)

#print " - Carregando arquivo .dot para o GraphTools..."
GGT = gt.load_graph("temp.dot")
diameter, averageDistance = utilitarios.getDiameterAndAverageDistance(GGT)
del GGT


#gt.graph_draw(GGT,vertex_text=GGT.vp.vertex_name,font_size=14,pen_width=0,output="rede.png")
#k = args.k


print " - Gerando listas..."
t0 = time()

listas = []
futures = []
with ProcessPoolExecutor(max_workers=10) as executor:
	for qtd in range(0, args.qtdPares):

		if(d_list):
			for d in d_list:
				if(d == "aleatorio"):
					v1,v2 = escolhaDoisVertices()
				else:
					v1,v2 = escolhaDoisVerticesDistanciaK(int(d))
				futures.append(executor.submit(montaListas,v1,v2,d))
				print "----> Iniciando criação de árvores para o par",v1,v2,"para dist = ",d

resultados = []
for f in as_completed(futures):
	res = f.result()
	resultados.append(res)

for r in resultados:
	listas.append(r)

del G
del dictG
	
t1 = time()
print ('Listas geradas em {}m'.format((t1-t0)/60))
#raw_input("Press Enter to continue...")


print " - Calculando distâncias..."
t0 = time()
futures = []
resultados = []
with ProcessPoolExecutor(max_workers=4) as executor:
	for l in listas:
		futures.append(executor.submit(calculos.calculaDistancia,l[0]['listas'],l[1]['listas'],l[0]['label'],l[1]['label'],l[0]['dist']))

	for f in as_completed(futures):
		res = f.result()
		resultados.append(res)


print "Cálculos terminados."

dadosGrafico = {}
for r in resultados:
	if((r[3]) not in dadosGrafico):
		dadosGrafico[r[3]] = {}
	for k,v in r[0].iteritems():
		if(v != -1):
			if(k not in dadosGrafico[r[3]]):
				dadosGrafico[r[3]][k] = {}
				dadosGrafico[r[3]][k]['valores'] = 0
				dadosGrafico[r[3]][k]['cont'] = 0
			dadosGrafico[r[3]][k]['valores'] += v
			dadosGrafico[r[3]][k]['cont'] += 1

delta_medio = {}
cont = {}
for dist,dados in dadosGrafico.iteritems():
	delta_medio[dist] = {}
	print "Distancia entre vértices d = ",dist
	for k,d in dados.iteritems():
		delta_medio[dist][k] = d['valores'] / d['cont']
		print "Delta média (calculada pelo DTW) para k = ",k,":",delta_medio[dist][k]
		

graficoParVertices = {}
for dist,v in delta_medio.iteritems():
	graficoParVertices[dist] = {}
	graficoParVertices[dist]['xs'] = []
	graficoParVertices[dist]['ys'] = []
	for k,d in v.iteritems():
		graficoParVertices[dist]['xs'].append(k)
		graficoParVertices[dist]['ys'].append(d)
graficoParVertices = collections.OrderedDict(sorted(graficoParVertices.items()))
t1 = time()
print ('Calculos realizados em {}m'.format((t1-t0)/60))

print " - Gerando gráfico..."
graficos.plotaGraficoMedias(graficoParVertices,averageDistance,diameter)











