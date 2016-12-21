#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
import sys
import sqlite3
import datetime


def criaArvoresDisco(g, root, maxDepth):

    nomeBD = criaTabelasSQLite(maxDepth,root)

    cont_id = 0

    arvore = {}

    bola = {}
    bola[root] = []

    visited, queue = [], [root]
    visited.append(root)
    
    depth = 0

    dados_vertices = []
    dados_filhos = []
    
    cont_id = criaNo(root,depth,cont_id,dados_vertices)

    pendingDepthIncrease = 0
    
    timeToDepthIncrease = 1


    while queue:
        vertex = queue.pop(0)

        id_no = procuraPrimeiroNoComLabel(vertex,depth,dados_vertices)

        bola[vertex] = g[vertex]

        timeToDepthIncrease -= 1
        l = list(set(g[vertex]) - set(visited))
        pendingDepthIncrease += len(l)

        cont_id = criaNos(g[vertex],id_no,depth + 1,cont_id,dados_vertices,dados_filhos)
        #print "cont_id",cont_id



        visited, queue = adicionaVizinhos(g[vertex],visited,queue)

        if(timeToDepthIncrease == 0):

            consolidaDados(bola,depth,nomeBD,dados_vertices,dados_filhos)

            depth += 1

            #print "depth",depth,"maxDepth",maxDepth

            if(depth == (maxDepth + 1)):
                return nomeBD,depth

            timeToDepthIncrease = pendingDepthIncrease
            pendingDepthIncrease = 0

    consolidaDados(bola,depth,nomeBD,dados_vertices,dados_filhos)
    return nomeBD,depth


def criaArvoresComRetornosDisco(g, root,maxDepth):
    nomeDB,depth = criaArvoresDisco(g, root, maxDepth)
    completaArvoreDisco(nomeDB,depth,maxDepth)
    print "Terminei de criar as árvores do nó",root
    return nomeDB,root


def completaArvoreDisco(nomeDB,depth,maxDepth):
    conn = sqlite3.connect(nomeDB)
    cursor = conn.cursor()
    #print "depth",depth,"maxDepth",maxDepth
    cont = depth + 1
    while(cont <= maxDepth):
        cursor.execute("""
        INSERT INTO vertices_arvore_"""+str(cont)+""" SELECT * FROM vertices_arvore_"""+str(depth)+""";
        """)
        cursor.execute("""
        INSERT INTO filhos_arvore_"""+str(cont)+""" SELECT * FROM filhos_arvore_"""+str(depth)+""";
        """)
        cont += 1
    conn.commit()

    cursor.close()
    conn.close()


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


def limitaArvore(arvore,b,camada):

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

def criaTabelasSQLite(qtdk,nomeVertice):
    a=datetime.datetime.now()
    t = "%s-%s-%s-%s-%s-%s" % (a.year,a.month,a.day,a.hour, a.minute, a.microsecond)
    nomeBD = "arvores/arvores-"+str(nomeVertice)+"-"+t+".db"
    conn = sqlite3.connect(nomeBD)

    cursor = conn.cursor()

    cursor.execute('''SELECT tbl_name FROM sqlite_master WHERE type="table" 
        AND (tbl_name like "vertices%" OR tbl_name like "filhos%") ;''')

    for linha in cursor.fetchall():
        l = str(linha[0])
        cursor.execute("DROP TABLE IF EXISTS "+l+" ;")

    cursor.execute('''CREATE TABLE vertices
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        label INTEGER NOT NULL,
        camada INTEGER NOT NULL,
        qtdFilhos INTEGER NOT NULL);''')

    cursor.execute('''CREATE TABLE filhos
            (id_pai INTEGER NOT NULL,
            id_filho INTEGER NOT NULL);''')

    for k in range(0,qtdk+1):

        cursor.execute('''CREATE TABLE vertices_arvore_'''+str(k)+'''
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                label INTEGER NOT NULL,
                camada INTEGER NOT NULL,
                qtdFilhos INTEGER NOT NULL);''')

        cursor.execute('''CREATE TABLE filhos_arvore_'''+str(k)+'''
                (id_pai INTEGER NOT NULL,
                id_filho INTEGER NOT NULL);''')

    conn.commit()

    cursor.close()
    conn.close()

    return nomeBD

def criaNo(label,camada,cont_id,dados_vertices):
    d = {}
    id_inserido = cont_id
    d['id'] = cont_id
    d['label'] = label
    d['camada'] = camada
    d['qtdFilhos'] = 0
    dados_vertices.append(d)
    cont_id += 1
    
    return cont_id

def procuraPrimeiroNoComLabel(label,depth,dados_vertices):
    #print "label",label,"depth",depth
    for v in dados_vertices:
        if(v['label'] == label and v['camada'] == depth):
            return v['id']

def consolidaNos(dados_nos,nomeBD):

    #print "inserindo",len(dados_nos),"nos..."

    conn = sqlite3.connect(nomeBD)
    cursor = conn.cursor()

    data = [{"id": d['id'],
            "label": d['label'],
            "camada": d['camada'],
            "qtdFilhos": d['qtdFilhos']} for d in dados_nos]

    cursor.execute("DELETE FROM vertices; ")

    cursor.executemany("""
    INSERT INTO
        vertices
        (id,label, camada, qtdFilhos)
    VALUES
        (:id, :label, :camada, :qtdFilhos)""", data)


    conn.commit()

    cursor.close()
    conn.close()

    #print len(dados_nos),"nos inseridos."

def consolidaFilhos(dados_filhos,nomeBD):

    conn = sqlite3.connect(nomeBD)
    cursor = conn.cursor()

    data = [{"id_pai": d['id_pai'],
            "id_filho": d['id_filho']} for d in dados_filhos]

    cursor.execute("DELETE FROM filhos; ")

    cursor.executemany("""
    INSERT INTO
        filhos
        (id_pai, id_filho)
    VALUES
        (:id_pai, :id_filho)""", data)

    conn.commit()

    cursor.close()
    conn.close()


def criaNos(filhos,pai,camada,cont_id,dados_vertices,dados_filhos):

    #print "criando",len(filhos),"no disco para o nó",pai

    ids_inseridos = []

    for f in filhos:
        d = {}
        d['id'] = cont_id
        d['label'] = f
        d['camada'] = camada
        d['qtdFilhos'] = len(filhos)
        ids_inseridos.append(cont_id)
        dados_vertices.append(d)
        cont_id += 1


    for i in ids_inseridos:
        d = {}
        d['id_pai'] = pai
        d['id_filho'] = i
        dados_filhos.append(d)


    #print "criado para o no",pai

    return cont_id

def consolidaDados(bb,depth,nomeBD,dados_vertices,dados_filhos):

    b = limitaBola(bb)

    consolidaNos(dados_vertices,nomeBD)
    consolidaFilhos(dados_filhos,nomeBD)


    limitaArvoreDisco(b,depth,nomeBD)


def limitaArvoreDisco(b,depth,nomeBD):
    #print "Prof:",depth
    conn = sqlite3.connect(nomeBD)
    cursor = conn.cursor()

    cursor.execute('''SELECT count(tbl_name) FROM sqlite_master WHERE type="table" 
        AND (tbl_name like "vertices_arvore_'''+str(depth)+'''") ;''')
    result = cursor.fetchone()
    qtdArvores = result[0] 
    if(qtdArvores == 0):
        return

    
    
    vertices = listaVerticesBola(b)
    vertices = list(vertices)

    #print "Vértices"
    #print vertices
    #print "--"



    verticesN = []
    verticesN.append(depth)
    verticesN.extend(vertices)

    cursor.execute(""" SELECT id,label,camada,qtdFilhos FROM vertices WHERE 
     label IN (%s) """ % ','.join('?'*len(vertices)), vertices)

    linhas_selecionadas_v = cursor.fetchall()

    #print "linhas_selecionadas_v",linhas_selecionadas_v

    vertices2 = []
    vertices2.extend(vertices)
    vertices2.extend(vertices)
    #print vertices2

    cursor.execute("""
    SELECT f.id_pai,f.id_filho,v1.label,v2.label FROM filhos f, vertices v1, vertices v2 
    WHERE f.id_pai = v1.id 
    AND f.id_filho = v2.id 
    AND v1.label IN (%s)
    AND v2.label IN (%s)
    """ % (','.join('?'*len(vertices)) , ','.join('?'*len(vertices))), (vertices2))

    linhas_selecionadas_f = cursor.fetchall()

    #print "linhas_selecionadas_f",linhas_selecionadas_f

    cursor.execute("DELETE FROM vertices_arvore_"+str(depth)+"; ")

    ## Insere na nova tabela

    data = [{   "id": v[0],
                "label": v[1],
                "camada": v[2],
                "qtdFilhos": v[3]} for v in linhas_selecionadas_v]

    

    cursor.executemany("""
    INSERT INTO
        vertices_arvore_"""+str(depth)+"""
        (id,label, camada, qtdFilhos)
    VALUES
        (:id, :label, :camada, :qtdFilhos)""", data)

    data = [{   "id_pai": v[0],
                "id_filho": v[1]} for v in linhas_selecionadas_f]

    cursor.executemany("""
    INSERT INTO
        filhos_arvore_"""+str(depth)+"""
        (id_pai,id_filho)
    VALUES
        (:id_pai, :id_filho)""", data)

    cursor.execute("""
    UPDATE vertices_arvore_"""+str(depth)+""" SET
        qtdFilhos = (SELECT count(f.id_filho) FROM filhos_arvore_"""+str(depth)+""" f 
        where vertices_arvore_"""+str(depth)+""".id = f.id_pai)
    """)


    conn.commit()

    cursor.close()
    conn.close()


def printArvoresDisco(nomeBD,k):

    conn = sqlite3.connect(nomeBD)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vertices_arvore_"+str(k)+";")

    for v in cursor.fetchall():
        printNoDisco(v,nomeBD,k)
    print "--"

    cursor.close()
    conn.close()

def printNoDisco(no,nomeBD,k):
    print "Id:",no[0],"Label:",no[1],"Camada:",no[2],"Qtd Filhos:",no[3]
    printFilhosDados(no,nomeBD,k)
    
def printFilhosDados(no,nomeBD,k):
    conn = sqlite3.connect(nomeBD)
    cursor = conn.cursor()

    cursor.execute(""" SELECT v.* FROM 
        filhos_arvore_"""+str(k)+""" f,
        vertices_arvore_"""+str(k)+""" v 
        WHERE f.id_filho = v.id AND f.id_pai = ? ;""", (no[0],))
    filhos = cursor.fetchall()
    if(filhos):
        print "Filhos:",
        for v in filhos:
            print "( Id:",v[0],"Label:",v[1],"Camada:",v[2],") ",
        print ""

    cursor.close()
    conn.close()


def grausPorCamada(nomeBD,k,camada):
    conn = sqlite3.connect(nomeBD)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT qtdFilhos FROM vertices_arvore_"""+str(k)+"""
    WHERE camada = ?
    """,(camada,))

    graus = {}
    for q in cursor.fetchall():
        grau = q[0]
        if(grau not in graus):
            graus[grau] = 0
        graus[grau] += 1

    cursor.close()
    conn.close()

    return graus


def grausPorVertice(nomeBD):
    conn = sqlite3.connect(nomeBD)
    cursor = conn.cursor()

    cursor.execute('''SELECT count(tbl_name) FROM sqlite_master WHERE type="table" 
        AND (tbl_name like "vertices_%") ;''')
    result = cursor.fetchone()
    qtdArvores = result[0]

    graus = {}

    for k in range(0,qtdArvores):
        graus['arv_tam'+str(k)] = {}

        maxCamada = getMaximaCamada(nomeBD,k)
        for camada in range(0,maxCamada+1):
            graus['arv_tam'+str(k)][camada] = grausPorCamada(nomeBD,k,camada)

    return graus
            

def getMaximaCamada(nomeBD,k):
    conn = sqlite3.connect(nomeBD)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT max(camada) FROM vertices_arvore_"""+str(k)+"""
    """)

    result = cursor.fetchone()
    maxCamada = result[0] 

    cursor.close()
    conn.close()

    return maxCamada
    
















