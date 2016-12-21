#!/usr/bin/env python
# -*- coding: utf-8 -*-

### arquivos utilizados
import graph, editDistance2, algoritmos, graficos, utilitarios, calculos
from multiprocessing.pool import ThreadPool
from concurrent.futures import ProcessPoolExecutor, as_completed

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

def montaListas(v1,v2):

	futures = []
	with ProcessPoolExecutor(max_workers=10) as executor:

		futures.append(executor.submit(calculos.geraListas, dictG, v1))
		futures.append(executor.submit(calculos.geraListas, dictG, v2))
			
		resultados = []
		for f in as_completed(futures):
			res = f.result()
			resultados.append(res)

	resultadosConsolidados = []
	for r in resultados:
		resultadosConsolidados.append({'label': r[1], 'listas': r[0]})

	
	return resultadosConsolidados

rand=random.Random()

parser = argparse.ArgumentParser(description='Criar bolas por vértices.')
parser.add_argument('--grafo', nargs='?', required=True,
                      help='Input graph file')
parser.add_argument('--qtdPares', default=2, type=int, required=True,
                      help='Quantidade de pares')
parser.add_argument('--dist', type=int, required=False,
                      help='Distancia')

args = parser.parse_args()

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
		
		#v1,v2 = escolhaDoisVertices(args.dist)
		if(args.dist):
			v1,v2 = escolhaDoisVerticesDistanciaK(args.dist)
		else:
			v1,v2 = escolhaDoisVertices()
		print "----> Iniciando criação de árvores para o par",v1,v2

		futures.append(executor.submit(montaListas,v1,v2))

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
		futures.append(executor.submit(calculos.calculaDistancia,l[0]['listas'],l[1]['listas'],l[0]['label'],l[1]['label']))

	for f in as_completed(futures):
		res = f.result()
		resultados.append(res)


print "Cálculos terminados."

dadosGrafico = {}
for r in resultados:
	if((r[1],r[2]) not in dadosGrafico):
		dadosGrafico[r[1],r[2]] = {}
	for k,v in r[0].iteritems():
		dadosGrafico[r[1],r[2]][k] = v

delta_medio = {}
cont = {}
for k,d in dadosGrafico.iteritems():
	for kk,dd in d.iteritems():
		if kk not in delta_medio:
			delta_medio[kk] = 0.0
		delta_medio[kk] += dd

		if(kk not in cont):
			cont[kk] = 0
		cont[kk] += 1

for k,v in delta_medio.iteritems():
	dM = delta_medio[k] / cont[k]
	print "Delta médio para k = ",k,":",dM

graficoParVertices = {}
for k,v in dadosGrafico.iteritems():
	graficoParVertices[k[0],k[1]] = {}
	graficoParVertices[k[0],k[1]]['xs'] = []
	graficoParVertices[k[0],k[1]]['ys'] = []
	v = sorted(v.items())
	for vv in v:
		if(vv[1] != -1):
			graficoParVertices[k[0],k[1]]['xs'].append(vv[0])
			graficoParVertices[k[0],k[1]]['ys'].append(vv[1])

t1 = time()
print ('Calculos realizados em {}m'.format((t1-t0)/60))

print " - Gerando gráfico..."
graficos.plotaGrafico(graficoParVertices,averageDistance,diameter)











