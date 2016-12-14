#!/usr/bin/env python
# -*- coding: utf-8 -*-

### arquivos utilizados
import graph, editDistance2, algoritmos, graficos, utilitarios
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

def montaBolas(v1,v2,kMax,arestasUC):

	futures = []
	with ProcessPoolExecutor() as executor:

		if(arestasUC):
			futures.append(executor.submit(algoritmos.montaBolasComArestasUltimaCamada, dictG, v1, kMax))
			futures.append(executor.submit(algoritmos.montaBolasComArestasUltimaCamada, dictG, v2, kMax))
			
	resultados = []
	for f in as_completed(futures):
		res = f.result()
		resultados.append(res)

	resultadosConsolidados = {}
	for r in resultados:
		if(r[1] not in resultadosConsolidados):
			resultadosConsolidados[r[1]] = {}
		resultadosConsolidados[r[1]] = r[0]

	bsV1 = {}
	bsV2 = {}
	for kVertice,bolasVertice in resultadosConsolidados.iteritems():
		#print kVertice
		if(kVertice == v1):
			bs = bsV1
		else:
			bs = bsV2
		for kBola,bolaVertice in bolasVertice.iteritems():
			#print "-",kBola
			bs[kBola] = bolaVertice

	bolas = {}
	bolas[v1,v2] = {}
	k = 0
	while(k <= kMax):
		bV1 = bsV1[k]
		bV2 = bsV2[k]
		bolas[v1,v2][k] = {'bolaV1':bV1, 'bolaV2':bV2}
		k += 1
	
	return bolas

rand=random.Random()

parser = argparse.ArgumentParser(description='Criar bolas por vértices.')
parser.add_argument('--grafo', nargs='?', required=True,
                      help='Input graph file')
parser.add_argument('--k', default=2, type=int, required=False,
                      help='Max: bola de tamanho k')
parser.add_argument('--qtdPares', default=2, type=int, required=True,
                      help='Quantidade de pares')
parser.add_argument('--arestasUltimaCamada', default=2, type=bool, required=True,
                      help='Arestas entre vizinhos da última camada?')

args = parser.parse_args()

print " - Carregando matriz de adjacência para Grafo (na memória)..."
G = graph.load_adjacencylist(args.grafo,undirected=True)
print " - Convertendo grafo para Dict (na memória)..."
dictG = G.gToDict()

print " - Criando arquivo .dot temporário..."
utilitarios.criaArquivoDot(G)

print " - Carregando arquivo .dot para o GraphTools..."
GGT = gt.load_graph("temp.dot")
#GGT = utilitarios.graphToGraphTool(G)
diameter, averageDistance = utilitarios.getDiameterAndAverageDistance(GGT)
del GGT

#diameter = 5
#averageDistance = 5
#gt.graph_draw(GGT,vertex_text=GGT.vp.vertex_name,font_size=14,pen_width=0,output="rede.png")
#k = args.k
k = int(math.ceil(diameter))

print " - Gerando bolas..."
t0 = time()

bolas = []
futures = []
with ProcessPoolExecutor() as executor:
	for qtd in range(0, args.qtdPares):
		print "----> Iniciando criação de bolas para o par",qtd
		v1,v2 = escolhaDoisVertices()

		futures.append(executor.submit(montaBolas,v1,v2,k,args.arestasUltimaCamada))

resultados = []
for f in as_completed(futures):
	res = f.result()
	resultados.append(res)

for r in resultados:
	if(not r in bolas):
		bolas.append(r)

del G
del dictG
	
t1 = time()
print ('Bolas geradas em {}m'.format((t1-t0)/60))


print " - Calculando degreeSequenceEditDistance..."
t0 = time()

futures = []
with ProcessPoolExecutor() as executor:
	for bolasV1V2 in bolas:
		for kB,vB in bolasV1V2.iteritems():
			for k,v in vB.iteritems():
				#print "Executando cálculo de degreeSequenceEditDistance para os vértices",kB[0],kB[1],"com bolas de tamanho",k

				# Mudar para calcular de uma vez, é possível?
				futures.append(executor.submit(editDistance2.degreeSequenceEditDistance,v['bolaV1'],v['bolaV2'],kB[0],kB[1],k))
				del v
				
resultados = []
for f in as_completed(futures):
	res = f.result()
	resultados.append(res)

print "Cálculos terminados."

dadosGrafico = {}
for r in resultados:
	if((r[1],r[2]) not in dadosGrafico):
		dadosGrafico[r[1],r[2]] = {}
	dadosGrafico[r[1],r[2]][r[3]] = r[0]

graficoParVertices = {}
for k,v in dadosGrafico.iteritems():
	graficoParVertices[k[0],k[1]] = {}
	graficoParVertices[k[0],k[1]]['xs'] = []
	graficoParVertices[k[0],k[1]]['ys'] = []
	v = sorted(v.items())
	for vv in v:
		graficoParVertices[k[0],k[1]]['xs'].append(vv[0])
		graficoParVertices[k[0],k[1]]['ys'].append(vv[1])

t1 = time()
print ('Calculos realizados em {}m'.format((t1-t0)/60))

print " - Gerando gráfico..."
graficos.plotaGrafico(graficoParVertices,averageDistance,diameter)











