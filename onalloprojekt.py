#imports
import pysat
import numpy as np
import matplotlib as plt
import pandas as pd
from pysat.solvers import Glucose3
from pysat.card import *

qin=input("Rank of the finite projective field: ")
q= int(qin)
#dictionaryt kell csinálni
valtozok=dict()
k=1
for i in range(q**2+q+1):
    for j in range(q**2+q+1):
        valtozok[tuple([i, j])]= k
        k=k+1
#print(valtozok)   

ssolver = Glucose3()
normalforma=CNF()

#minden sorban pontosan q+1 db 1-es legyen
maxvaltozo=(q**2+q+1)**2
for i in range(q**2+q+1):
    l1=[]
    for j in range(q**2+q+1):
        l1=l1+[valtozok[(i,j)]]
        
    cnf=CardEnc.equals(lits=l1, bound=q+1, top_id=maxvaltozo)
    for cl in cnf.clauses:
        normalforma.append(cl)
    
    #az abselemek lista tartalmazza az eddig használt változók abszolút értékét
    #a top_id frissítéséhez használom a maxvaltozo-t
    abselemek=[]
    for kloz in normalforma.clauses:
        l2=[abs(elem) for elem in kloz]
        abselemek=abselemek+l2
    maxvaltozo=max(abselemek)
#print(normalforma.clauses)

#minden oszlopban pontosan q+1 db 1-es legyen
for i in range(q**2+q+1):
    l1=[]
    for j in range(q**2+q+1):
        l1=l1+[valtozok[(j,i)]]
        
    cnf=CardEnc.equals(lits=l1, bound=q+1, top_id=maxvaltozo)
    for cl in cnf.clauses:
        normalforma.append(cl)
    
    #az abselemek lista tartalmazza az eddig használt változók abszolút értékét
    #a top_id frissítéséhez használom a maxvaltozo-t
    abselemek=[]
    for kloz in normalforma.clauses:
        l2=[abs(elem) for elem in kloz]
        abselemek=abselemek+l2
    maxvaltozo=max(abselemek)
	
#maxvaltozo
	
	#már csak az kell, hogy ne legyen csupa 1-es négyzet, vagyis i, k sor és j, l oszlop, hogy ij, il, kj, és kl is igaz
for i in range(q**2+q+1):
    for j in range(q**2+q+1):
        for k in range(q**2+q+1):
            for l in range(q**2+q+1):
                x1=valtozok[(i,j)]
                x2=valtozok[(i,l)]
                x3=valtozok[(k,j)]
                x4=valtozok[(k,l)]
                if (x1!=x2 and x1!=x3 and x1!=x4 and x2!=x3 and x2!=x4 and x3!=x4):
                    normalforma.clauses.append([-x1, -x2, -x3, -x4])
					
#beadom a sat-solvernek a normálformát
for kloz in normalforma.clauses:
    ssolver.add_clause(kloz)
    
# megoldás kiszámítása
ssolver.solve()
ans=ssolver.get_model()
print(ans)

#csinálok egy listák listáját a megoldásból, amiben csak a nekünk releváns változók szerepelnek és csak 1-0 elemek vannak

megoldaslista=[]
for i in range(0, (q**2+q+1)**2, q**2+q+1):
    l1=ans[i:i+q**2+q+1]
    l2=[]
    for elem in l1:
        if elem>0:
            l2=l2+[1]
        else:
            l2=l2+[0]
    megoldaslista.append(l2)
        
#kiprintelem a megoldást mátrix alakban

szepmatrix=np.array(megoldaslista)
print(szepmatrix)