#imports
import pysat
import numpy as np
import matplotlib as plt
import pandas as pd
from pysat.solvers import Glucose3
from pysat.card import *
import time
import datetime

q = int(input("Search for finite projective field with order q=? "))
#dictionaryt kell csinálni
valtozok=dict()
k=1
for i in range(q**2+q+1):
    for j in range(q**2+q+1):
        valtozok[tuple([i, j])]= k
        k=k+1
		
ssolver = Glucose3()
normalforma=CNF()

#beleírom a plusz feltevéseket, amiket a megoldások szimmetriája miatt feltehetünk
#az első sor első q+1 eleme 1, a többi 0
for i in range(q+1):
    normalforma.clauses.append([valtozok[0, i]])
for i in range(q+1, q**2+q+1, 1):
    normalforma.clauses.append([-valtozok[0, i]])
    
#az első oszlop 2. elemétől a q+1-edik oszlop utolsó eleméig felírom a feltételeket, i lesz az oszlopindex, j a sorindex
for i in range(q+1):
    for j in range(1, q**2+q+1, 1):
        if (j >= i*q+1 and j<(i+1)*q+1):
            normalforma.clauses.append([valtozok[j,i]])
        else:
            normalforma.clauses.append([-valtozok[j, i]])

#a q+2-edik oszlop formáját is elő lehet írni
for i in range(1, q**2+q+1, 1):
    if i%q==1:
        normalforma.clauses.append([valtozok[i, q+1]])
    else:
        normalforma.clauses.append([-valtozok[i, q+1]])
		
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
					
#módosítom a sorfeltételeket, miután lefixáltam néhány változó igazságértékét
#minden sorban pontosan q-1 db 1-es legyen még a lefixáltakon kívül
maxvaltozo=(q**2+q+1)**2
for i in range(1, q**2+q+1, 1):
    l1=[]
    for j in range(q+2, q**2+q+1, 1):
        l1=l1+[valtozok[(i,j)]]
        
    cnf=CardEnc.equals(lits=l1, bound=q-1, top_id=maxvaltozo)
    for cl in cnf.clauses:
        normalforma.append(cl)
    
    #az abselemek lista tartalmazza az eddig használt változók abszolút értékét
    #a top_id frissítéséhez használom a maxvaltozo-t
    abselemek=[]
    for kloz in normalforma.clauses:
        l2=[abs(elem) for elem in kloz]
        abselemek=abselemek+l2
    maxvaltozo=max(abselemek)
	
print("Maxvaltozo a sorfelteltelek utan: "+str(maxvaltozo))

#minden oszlopban pontosan q+1 db 1-es legyen
for i in range(q+2, q**2+q+1, 1):
    l1=[]
    for j in range(1, q**2+q+1, 1):
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
	
print("Maxvaltozo az oszlopfeltetelek utan: "+ str(maxvaltozo))

#beadom a sat-solvernek a normálformát
for kloz in normalforma.clauses:
    ssolver.add_clause(kloz)
    
# megoldás kiszámítása
ssolver.solve()
ans=ssolver.get_model()
print(ans)