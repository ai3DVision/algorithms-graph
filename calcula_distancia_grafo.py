#!/usr/bin/env python
# -*- coding: utf-8 -*-

### arquivos utilizados
import graph, editDistance2, algoritmos, graficos, utilitarios

######
import argparse,random,math
import graph_tool.all as gt

def escolhaDoisVertices():
	v1 = rand.choice(G.keys())
	v2 = rand.choice(G.keys())
	while v1 == v2:
		v2 = rand.choice(G.keys())
	return v1,v2

def montaBolas(v1,v2,kMax,arestasUC):
	bolas = {}
	for k in range(0, kMax+1):

		if(arestasUC):
			bV1 = algoritmos.montaBolaComArestasUltimaCamada(G, v1, k)
			bV2 = algoritmos.montaBolaComArestasUltimaCamada(G, v2, k)
		else:
			bV1 = algoritmos.montaBolaSemArestasUltimaCamada(G, v1, k)
			bV2 = algoritmos.montaBolaSemArestasUltimaCamada(G, v2, k)

		if((v1,v2) not in bolas):
			bolas[v1,v2] = {}
		bolas[v1,v2][k] = {'bolaV1':bV1, 'bolaV2':bV2}
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


G = graph.load_adjacencylist(args.grafo,undirected=True)

GGT = utilitarios.graphToGraphTool(G)
diameter, averageDistance = utilitarios.getDiameterAndAverageDistance(GGT)
#gt.graph_draw(GGT,vertex_text=GGT.vp.vertex_name,font_size=14,pen_width=0,output="rede.png")

#k = args.k
k = int(math.ceil(diameter))

print " - Gerando bolas..."
bolas = []
for qtd in range(0, args.qtdPares):
	v1,v2 = escolhaDoisVertices()
	bolasV1V2 = montaBolas(v1,v2,k,args.arestasUltimaCamada)
	bolas.append(bolasV1V2)


print " - Calculando degreeSequenceEditDistance..."
graficoParVertices = {}

for bolasV1V2 in bolas:
	for kB,vB in bolasV1V2.iteritems():
		#print "------------------------------------"
		#print "entre os vértices:",kB[0],"-",kB[1]
		graficoParVertices[kB[0],kB[1]] = {}
		xs = []
		ys = []
		for k,v in vB.iteritems():
			xs.append(k)
			#print "Bola de",kB[0]
			#v['bolaV1'].printAdjList()
			#print "Bola de",kB[1]
			#v['bolaV2'].printAdjList()
			e = editDistance2.degreeSequenceEditDistance(v['bolaV1'],v['bolaV2'])
			ys.append(e)
			#print "bola de tamanho:",k, "DegreeSequenceEditDistance:",e 

		graficoParVertices[kB[0],kB[1]]['xs'] = xs
		graficoParVertices[kB[0],kB[1]]['ys'] = ys

		#print "------------------------------------"



print " - Gerando gráfico..."
graficos.plotaGrafico(graficoParVertices,averageDistance,diameter)











