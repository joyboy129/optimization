# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# This is a sample Python script.


# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pulp
from pulp import *
import pandas as pd
import numpy as np
import openpyxl

#Input


def dict(a,b):
    my={}
    for i in range(len(a)):
        my[a[i]]=b[i]
    return my
def getting(i,l):
    m=[]
    for k in l:
        m.append(k[i])
    return m
def concat_list(a,b):
    m=[]
    for i in range(len(a)):
        m.append(a[i]+"_"+b[i])
    return m

def making_recette(a,b,c):
    m={}
    n=len(b[0])
    for i in range(len(a)):
        m[a[i]]=dict(c,b[i][2:])
    return m
def elim_zero(l):
    m=[]
    for i in l:
        if i !=0 and i!="0":
            m.append(i)
    return m
def making_dict(a,b):
    m={}
    for i in range(len(a)):
        m[a[i]]=b[i]
    return m
def com_possible(a,b):
    m=[]
    for i in a:
        for j in b:
            m.append(i+"_"+str(j))
    return m
def making_pourc(df,l,MP):
    m={}
    for i in range(len(l)):
        p={}
        for j in range(len(MP)):
            p[MP[j]]=df[i][j+2]
        m[l[i]]=p
    return m
Cout_de_stockage_MP=10
Cout_de_stockage_Engrais=10
Cout_blending=120
Cout_smart_blending=260
blending_min=500
stockage_min=100
Big_M=100000000
Cout_stockage_building=10
Big_n=range(1,10)
url1="venv/Structure_Modele_Actuelle - small data set.xlsx"
url2="venv/Structure_Modele_Actuelle - all data set.xlsx"
url=url2
OCP=["OCP Jorf","OCP SAFI","OCP Port Casablanca","OCP Port Tanger","OCP Port Nador"]
df_Options = pd.read_excel (url, sheet_name='Options')
df_Options=df_Options.to_numpy()
Cout_blender=10000000
Cout_sblender=100000
temps=[2,3,4,1]


#Lecture des excels
df_MP = pd.read_excel (url, sheet_name='MP')
df_MP=df_MP.to_numpy()
df_Stockage = pd.read_excel (url, sheet_name='Stockage')
df_Stockage=df_Stockage.to_numpy()
df_Blenders = pd.read_excel (url, sheet_name='Blenders')
df_Blenders=df_Blenders.to_numpy()
df_Recette = pd.read_excel (url, sheet_name='Recettes')
df_Recette=df_Recette.to_numpy()
df_Demande = pd.read_excel (url, sheet_name='Demande')
df_Demande=df_Demande.to_numpy()
df_transportAmont=pd.read_excel (url, sheet_name='Cout de transport  Amont')
df_transportAmont=df_transportAmont.to_numpy()
df_transportAval=pd.read_excel (url, sheet_name='Cout de transport aval')
df_transportAval=df_transportAval.to_numpy()
df_Capacite_source=pd.read_excel (url, sheet_name='Capacité source')
df_Capacite_source=df_Capacite_source.to_numpy()

#Blenders=[province,1]
SBlenders=[]
Blenders=[]
for i in range(len(df_Blenders)):
    for j in range(df_Blenders[i][1]):
        Blenders.append(df_Blenders[i][0]+"_"+str(j))
for i in range(len(df_Blenders)):
    for j in range(df_Blenders[i][2]):
        SBlenders.append(df_Blenders[i][0]+"_"+str(j))







#Initiation du probleme
prob = LpProblem("The OCP Problem", LpMinimize)


#Process de calcul des constantes
Province_1=getting(0,df_Recette)
Filieres=getting(1,df_Recette)



#Constantes
MP=getting(0,df_MP)
Prix_MP=getting(1,df_MP)
Province=getting(0,df_Stockage)
Stock=getting(0,df_Stockage)
Capacite_Stockage=getting(1,df_Stockage)
OCP=["OCP Jorf","OCP SAFI","OCP Port Casablanca","OCP Port Tanger","OCP Port Nador"]
Capacite_Blender=elim_zero(getting(3,df_Blenders))
Capacite_SBlender=elim_zero(getting(4,df_Blenders))
Blenderplus=com_possible(Province,Big_n)
SBlenderplus=com_possible(Province,Big_n)
n=len(Blenderplus)
ToutBlenderplus=Blenderplus+SBlenderplus
Capacite_Blenderplus=[12000 for i in range(n)]
Capacite_SBlenderplus=[3000 for i in range(n)]
Capacite_TBlender=Capacite_Blender+Capacite_SBlender
Capacite_TBlenderplus=Capacite_Blenderplus+Capacite_SBlenderplus
Recette=concat_list(Province_1,Filieres)
Recette_avec_ing=making_recette(Recette,df_Recette,MP)
demande={}
for t in range(len(temps)):
    demande[temps[t]]=making_dict(concat_list(getting(0,df_Demande),getting(1,df_Demande)),getting(t+2,df_Demande))
ToutBlender=Blenders+SBlenders
zone=getting(0,df_transportAmont)
Stockplus=com_possible(Province,Big_n)
Capacite_Stockageplus=[3500 for i in range(len(Stockplus))]
AllBlender=ToutBlender+ToutBlenderplus
coa={}

for i in range(len(zone)):
    m={}
    for j in range(len(OCP)):
        m[OCP[j]]=df_transportAmont[i][j+1]
    coa[zone[i]]=m

cod={}
for i in range(len(zone)):
    m={}
    for j in range(len(zone)):
        m[zone[j]]=df_transportAval[i][j+1]
    cod[zone[i]]=m
def contrainte_min(prob,X,MP,OCP,ToutBlender,W_X,Big_M,blending_min,temps):
    for i in MP:
        for j in OCP:
            for k in ToutBlender:
                for t in temps:
                    prob += X[i][j][k][t] <= W_X[i][j][k][t] * Big_M
                    prob += X[i][j][k][t] >= W_X[i][j][k][t] * blending_min





def cont_activation(prob,Cplus,W_Xplus,MP,OCP,ToutBlenderplus,temps):
    for i in MP:
        for j in OCP:
            for k in ToutBlenderplus:
                for t in temps:
                    prob += Cplus[k][t] >= W_Xplus[i][j][k][t]

def cont_activation1(prob,Splus,W_Rplus_2,Recette,Stockplus,ToutBlenderplus):
    for i in Recette:
        for j in Stockplus:
            for k in ToutBlenderplus:
                prob += Splus[j] >= W_Rplus_2[i][j][k]
#A revoir
#Déclaration des variables


X=pulp.LpVariable.dicts("X",(MP,OCP,ToutBlender,temps),lowBound=0,cat="Continuous")
Xplus=pulp.LpVariable.dicts("Xplus",(MP,OCP,ToutBlenderplus,temps),lowBound=0,cat="Continuous")
R=pulp.LpVariable.dicts("R",(MP,Stock,ToutBlender,temps),lowBound=0,cat="Continuous")
Rplus_0=pulp.LpVariable.dicts("Rplus_0",(MP,Stock,ToutBlenderplus,temps),lowBound=0,cat="Continuous")
Rplus_1=pulp.LpVariable.dicts("Rplus_1",(MP,Stockplus,ToutBlender,temps),lowBound=0,cat="Continuous")
Rplus_2=pulp.LpVariable.dicts("Rplus_2",(MP,Stockplus,ToutBlenderplus,temps),lowBound=0,cat="Continuous")
Y=pulp.LpVariable.dicts("Y",(Recette,ToutBlender,Province,temps),lowBound=0,cat="Continuous")
Yplus=pulp.LpVariable.dicts("Yplus",(Recette,ToutBlenderplus,Province,temps),lowBound=0,cat="Continuous")
A=pulp.LpVariable.dicts("A",(MP,OCP,Stock,temps),lowBound=0,cat="Continuous")
Aplus=pulp.LpVariable.dicts("Aplus",(MP,OCP,Stockplus,temps),lowBound=0,cat="Continuous")
B=pulp.LpVariable.dicts("B",(Recette,ToutBlender,Stock,temps),lowBound=0,cat="Continuous")
Bplus_0=pulp.LpVariable.dicts("Bplus_0",(Recette,ToutBlenderplus,Stock,temps),lowBound=0,cat="Continuous")
Bplus_1=pulp.LpVariable.dicts("Bplus_1",(Recette,ToutBlender,Stockplus,temps),lowBound=0,cat="Continuous")
Bplus_2=pulp.LpVariable.dicts("Bplus_2",(Recette,ToutBlenderplus,Stockplus,temps),lowBound=0,cat="Continuous")
P=pulp.LpVariable.dicts("P",(Recette,Stock,Province,temps),lowBound=0,cat="Continuous")
Pplus=pulp.LpVariable.dicts("Pplus",(Recette,Stockplus,Province,temps),lowBound=0,cat="Continuous")
W_X= LpVariable.dicts("W_X", (MP,OCP,ToutBlender,temps), lowBound=0, upBound=1, cat='Binary')
W_A= LpVariable.dicts("W_A", (MP,OCP,Stock,temps), lowBound=0, upBound=1, cat='Binary')
W_B= LpVariable.dicts("W_B", (Recette,ToutBlender,Stock,temps), lowBound=0, upBound=1, cat='Binary')
W_Xplus= LpVariable.dicts("W_X", (MP,OCP,ToutBlenderplus,temps), lowBound=0, upBound=1, cat='Binary')
W_Aplus= LpVariable.dicts("W_A", (MP,OCP,Stockplus,temps), lowBound=0, upBound=1, cat='Binary')
W_Rplus_0=pulp.LpVariable.dicts("W_Rplus_0",(MP,Stock,ToutBlenderplus,temps),lowBound=0, upBound=1, cat='Binary')
W_Rplus_1=pulp.LpVariable.dicts("W_Rplus_1",(MP,Stockplus,ToutBlender,temps),lowBound=0, upBound=1, cat='Binary')
W_Rplus_2=pulp.LpVariable.dicts("W_Rplus_2",(MP,Stockplus,ToutBlenderplus,temps),lowBound=0, upBound=1, cat='Binary')
W_Yplus=pulp.LpVariable.dicts("W_Yplus",(Recette,ToutBlenderplus,Province,temps),lowBound=0, upBound=1, cat='Binary')
W_Bplus_0=pulp.LpVariable.dicts("W_Bplus_0",(Recette,ToutBlenderplus,Stock,temps),lowBound=0, upBound=1, cat='Binary')
W_Bplus_1=pulp.LpVariable.dicts("W_Bplus_1",(Recette,ToutBlender,Stockplus,temps),lowBound=0, upBound=1, cat='Binary')
W_Bplus_2=pulp.LpVariable.dicts("W_Bplus_2",(Recette,ToutBlenderplus,Stockplus,temps),lowBound=0, upBound=1, cat='Binary')
W_R= LpVariable.dicts("W_R", (MP,Stock,ToutBlender,temps), lowBound=0, upBound=1, cat='Binary')
Cplus=pulp.LpVariable.dicts("Cplus",(ToutBlenderplus,temps),lowBound=0, upBound=1, cat='Binary')
Splus=pulp.LpVariable.dicts("Splus",(Stockplus,temps),lowBound=0, upBound=1, cat='Binary')
res_MP=pulp.LpVariable.dicts("res_MP",(MP,Stock,temps),lowBound=0,cat="Continuous")
res_PF=pulp.LpVariable.dicts("res_PF",(Recette,Stock,temps),lowBound=0,cat="Continuous")
res_MP_plus=pulp.LpVariable.dicts("res_MP_plus",(MP,Stockplus,temps),lowBound=0,cat="Continuous")
res_PF_plus=pulp.LpVariable.dicts("res_PF_plus",(Recette,Stockplus,temps),lowBound=0,cat="Continuous")
CplusF=pulp.LpVariable.dicts("Cplus",(ToutBlenderplus),lowBound=0, upBound=1, cat='Binary')
SplusF=pulp.LpVariable.dicts("Splus",(Stockplus),lowBound=0, upBound=1, cat='Binary')


#Contraintes

for i in ToutBlenderplus:
    for t in temps:
        prob+=CplusF[i]>=Cplus[i][t]

for i in Stockplus:
    for t in temps:
        prob+=SplusF[i]>=Splus[i][t]




cont_activation(prob,Cplus,W_Xplus,MP,OCP,ToutBlenderplus,temps)
cont_activation(prob,Cplus,W_Rplus_0,MP,Stock,ToutBlenderplus,temps)
cont_activation(prob,Cplus,W_Rplus_2,MP,Stockplus,ToutBlenderplus,temps)
cont_activation(prob,Splus,W_Aplus,MP,OCP,Stockplus,temps)
cont_activation(prob,Splus,W_Bplus_1,Recette,ToutBlender,Stockplus,temps)
cont_activation(prob,Splus,W_Bplus_2,Recette,ToutBlenderplus,Stockplus,temps)



#Contrainte mini
contrainte_min(prob,R,MP,Stock,ToutBlender,W_R,Big_M,blending_min,temps)
contrainte_min(prob,X,MP,OCP,ToutBlender,W_X,Big_M,blending_min,temps)
contrainte_min(prob,Xplus,MP,OCP,ToutBlenderplus,W_Xplus,Big_M,blending_min,temps)
contrainte_min(prob,A,MP,OCP,Stock,W_A,Big_M,stockage_min,temps)
contrainte_min(prob,Aplus,MP,OCP,Stockplus,W_Aplus,Big_M,stockage_min,temps)
contrainte_min(prob,B,Recette,ToutBlender,Stock,W_B,Big_M,stockage_min,temps)
contrainte_min(prob,Bplus_1,Recette,ToutBlender,Stockplus,W_Bplus_1,Big_M,stockage_min,temps)
contrainte_min(prob,Bplus_0,Recette,ToutBlenderplus,Stock,W_Bplus_0,Big_M,stockage_min,temps)
contrainte_min(prob,Bplus_2,Recette,ToutBlenderplus,Stockplus,W_Bplus_2,Big_M,stockage_min,temps)
contrainte_min(prob,Yplus,Recette,ToutBlenderplus,Province,W_Yplus,Big_M,0,temps)
contrainte_min(prob,Rplus_0,MP,Stock,ToutBlenderplus,W_Rplus_0,Big_M,0,temps)
contrainte_min(prob,Rplus_1,MP,Stockplus,ToutBlender,W_Rplus_1,Big_M,0,temps)
contrainte_min(prob,Rplus_2,MP,Stockplus,ToutBlenderplus,W_Rplus_2,Big_M,0,temps)







for k in range(len(ToutBlender)):
    prob += pulp.lpSum([X[i][j][ToutBlender[k]][t] for t in temps for i in MP for j in OCP])+pulp.lpSum([R[i][j][ToutBlender[k]][t] for t in temps for i in MP for j in Stock])+pulp.lpSum([Rplus_1[i][j][ToutBlender[k]][t] for t in temps for i in MP for j in Stockplus]) <= Capacite_TBlender[k], "capacite blender "+str(k)

for k in range(len(Stock)):
    prob += pulp.lpSum([A[i][j][Stock[k]][t] for t in temps for i in MP for j in OCP])+pulp.lpSum([B[i][j][Stock[k]][t] for t in temps for i in Recette for j in ToutBlender])+pulp.lpSum([Bplus_0[i][j][Stock[k]][t] for t in temps for i in Recette for j in ToutBlenderplus]) <= Capacite_Stockage[k]

for k in range(len(ToutBlender)):
    prob += pulp.lpSum([X[i][j][ToutBlender[k]][t] for t in temps for i in MP for j in OCP])+pulp.lpSum([R[i][j][ToutBlender[k]][t] for t in temps for i in MP for j in Stock])+pulp.lpSum([Rplus_1[i][j][ToutBlender[k]][t] for t in temps for i in MP for j in Stockplus]) == pulp.lpSum([Y[i][ToutBlender[k]][j][t] for t in temps for i in Recette for j in Province])+pulp.lpSum([B[i][ToutBlender[k]][j][t] for t in temps for i in Recette for j in Stock])+pulp.lpSum([Bplus_1[i][ToutBlender[k]][j][t] for t in temps for i in Recette for j in Stockplus])

for k in range(len(ToutBlenderplus)):
    prob += pulp.lpSum([Xplus[i][j][ToutBlenderplus[k]][t] for t in temps for i in MP for j in OCP])+pulp.lpSum([Rplus_0[i][j][ToutBlenderplus[k]][t] for t in temps for i in MP for j in Stock])+pulp.lpSum([Rplus_2[i][j][ToutBlenderplus[k]][t] for t in temps for i in MP for j in Stockplus]) == pulp.lpSum([Yplus[i][ToutBlenderplus[k]][j][t] for t in temps for i in Recette for j in Province])+pulp.lpSum([Bplus_0[i][ToutBlenderplus[k]][j][t] for t in temps for i in Recette for j in Stock])+pulp.lpSum([Bplus_2[i][ToutBlenderplus[k]][j][t] for t in temps for i in Recette for j in Stockplus])


for k in range(len(ToutBlenderplus)):
    prob += pulp.lpSum([Xplus[i][j][ToutBlenderplus[k]][t] for t in temps for i in MP for j in OCP])+pulp.lpSum([Rplus_0[i][j][ToutBlenderplus[k]][t] for t in temps for i in MP for j in Stock])+pulp.lpSum([Rplus_2[i][j][ToutBlenderplus[k]][t] for t in temps for i in MP for j in Stockplus]) <= Capacite_TBlenderplus[k]


#demande satistfaite:
for i in Recette:
    for k in Province:
        for t in temps:
            if i.split("_")[0] == k:
                prob += pulp.lpSum([Y[i][j][k][t] for j in ToutBlender]) + pulp.lpSum(
                    [Yplus[i][j][k][t] for j in ToutBlenderplus]) + pulp.lpSum([P[i][j][k][t] for j in Stock]) + pulp.lpSum(
                    [Pplus[i][j][k][t] for j in Stockplus]) == demande[t][i]

#Les blenders doivent recevoir de quoi faire les recettes
for i in MP:
    for k in ToutBlender:
        for t in temps:
            prob += pulp.lpSum([X[i][j][k][t] for j in OCP]) + pulp.lpSum([R[i][j][k][t] for j in Stock]) + pulp.lpSum(
                [Rplus_1[i][j][k][t] for j in Stockplus]) == pulp.lpSum(
                [Recette_avec_ing[a][i] * Y[a][k][j][t] for j in Province for a in Recette]) + pulp.lpSum(
                [Recette_avec_ing[a][i] * B[a][k][j][t] for j in Stock for a in Recette]) + pulp.lpSum(
                [Recette_avec_ing[a][i] * Bplus_1[a][k][j][t] for j in Stockplus for a in Recette])

for i in MP:
    for k in ToutBlenderplus:
        for t in temps:
            prob += pulp.lpSum([Xplus[i][j][k][t] for j in OCP]) + pulp.lpSum(
                [Rplus_0[i][j][k][t] for j in Stock]) == pulp.lpSum(
                [Recette_avec_ing[a][i] * Yplus[a][k][j][t] for j in Province for a in Recette]) + pulp.lpSum(
                [Recette_avec_ing[a][i] * Bplus_0[a][k][j][t] for j in Stock for a in Recette]) + pulp.lpSum(
                [Recette_avec_ing[a][i] * Bplus_2[a][k][j][t] for j in Stockplus for a in Recette])



#Les stocks ne creent rien
for i in MP:
    for j in Stock:
        for t in temps:
            prob += pulp.lpSum([R[i][j][k][t] for k in ToutBlender]) + pulp.lpSum(
                [Rplus_0[i][j][k][t] for k in ToutBlenderplus]) == pulp.lpSum([A[i][k][j][t] for k in OCP]) + \
                    res_MP[i][j][t]

for i in MP:
    for j in Stockplus:
        for t in temps:
            prob += pulp.lpSum([Rplus_1[i][j][k][t] for k in ToutBlender]) + pulp.lpSum(
                [Rplus_2[i][j][k][t] for k in ToutBlenderplus]) == pulp.lpSum([Aplus[i][k][j][t] for k in OCP])\
                    +res_MP_plus[i][j][t]


for i in Recette:
    for j in Stock:
        for t in temps:
            prob += pulp.lpSum([P[i][j][k][t] for k in Province]) == pulp.lpSum(
                [B[i][k][j][t] for k in ToutBlender]) + pulp.lpSum([Bplus_0[i][k][j][t] for k in ToutBlenderplus])+res_PF[i][j][t]

for i in Recette:
    for j in Stockplus:
        for t in temps:
            prob += pulp.lpSum([Pplus[i][j][k][t] for k in Province]) == pulp.lpSum(
                [Bplus_2[i][k][j][t] for k in ToutBlenderplus]) + pulp.lpSum([Bplus_1[i][k][j][t] for k in ToutBlender])\
                    +res_PF_plus[i][j][t]

#Contrainte de supply:
for i in range(len(MP)):
    for j in range(len(OCP)):
        for t in temps:
            prob += pulp.lpSum([X[MP[i]][OCP[j]][k][t] for k in ToutBlender]) + pulp.lpSum(
                [Xplus[MP[i]][OCP[j]][k][t] for k in ToutBlenderplus]) + pulp.lpSum(
                [A[MP[i]][OCP[j]][k][t] for k in Stock]) \
                    + pulp.lpSum([Aplus[MP[i]][OCP[j]][k][t] for k in Stockplus]) <= \
                    df_Capacite_source[i][j + 1]

#Step 3 residus:

for i in MP:
    for j in Stock:
        prob+=res_MP[i][j][2]==0
        for t in range(1,len(temps)):
            prob += res_MP[i][j][temps[t]] == res_MP[i][j][temps[t-1]]\
                    +pulp.lpSum([A[i][k][j][t] for k in OCP])\
                    -pulp.lpSum([R[i][j][k][t] for k in ToutBlender])\
                    -pulp.lpSum([Rplus_0[i][j][k][t] for k in ToutBlenderplus])
    for j in Stockplus:
        prob += res_MP_plus[i][j][2] == 0
        for t in range(1, len(temps)):
            prob += res_MP_plus[i][j][temps[t]] == res_MP_plus[i][j][temps[t - 1]] \
                    + pulp.lpSum([Aplus[i][k][j][t] for k in OCP]) \
                    - pulp.lpSum([Rplus_1[i][j][k][t] for k in ToutBlender]) \
                    - pulp.lpSum([Rplus_2[i][j][k][t] for k in ToutBlenderplus])

for i in Recette:
    for j in Stock:
        prob+=res_PF[i][j][2]==0
        for t in range(1,len(temps)):
            prob += res_PF[i][j][temps[t]] == res_PF[i][j][temps[t-1]]\
                    +pulp.lpSum([B[i][k][j][t] for k in ToutBlender])\
                    +pulp.lpSum([Bplus_0[i][k][j][t] for k in ToutBlenderplus])\
                    -pulp.lpSum([P[i][j][k][t] for k in Province])
    for j in Stockplus:
        prob += res_PF_plus[i][j][2] == 0
        for t in range(1, len(temps)):
            prob += res_PF_plus[i][j][temps[t]] == res_PF_plus[i][j][temps[t - 1]] \
                    + pulp.lpSum([Bplus_1[i][k][j][t] for k in ToutBlender]) \
                    + pulp.lpSum([Bplus_2[i][k][j][t] for k in ToutBlenderplus]) \
                    - pulp.lpSum([Pplus[i][j][k][t] for k in Province])



#Objective function

prob+=(pulp.lpSum([coa[k.split("_")[0]][j]*X[i][j][k][t] for t in temps for l in Stock for i in MP for j in OCP for k in ToutBlender])
       +pulp.lpSum([coa[k.split("_")[0]][j]*Xplus[i][j][k][t] for t in temps for l in Stock for i in MP for j in OCP for k in ToutBlenderplus])
       +pulp.lpSum([cod[k][j.split("_")[0]]*Y[i][j][k][t] for t in temps for i in Recette for j in ToutBlender for k in Province])
       +pulp.lpSum([cod[k][j.split("_")[0]]*Yplus[i][j][k][t] for t in temps for i in Recette for j in ToutBlenderplus for k in Province])
       +pulp.lpSum([cod[k][j.split("_")[0]]*B[i][j][k][t] for t in temps for i in Recette for j in ToutBlender for k in Stock])
       +pulp.lpSum([cod[k][j.split("_")[0]]*Bplus_0[i][j][k][t] for t in temps for i in Recette for j in ToutBlenderplus for k in Stock])
       +pulp.lpSum([cod[k.split("_")[0]][j.split("_")[0]]*Bplus_1[i][j][k][t] for t in temps for i in Recette for j in ToutBlender for k in Stockplus])
       +pulp.lpSum([cod[k.split("_")[0]][j.split("_")[0]]*Bplus_2[i][j][k][t] for t in temps for i in Recette for j in ToutBlenderplus for k in Stockplus])
       +pulp.lpSum([coa[k.split("_")[0]][j]*A[i][j][k][t] for t in temps for i in MP for j in OCP for k in Stock])
       +pulp.lpSum([coa[k.split("_")[0]][j]*Aplus[i][j][k][t] for t in temps for i in MP for j in OCP for k in Stockplus])
       +pulp.lpSum([Cout_blending*X[i][j][k][t] for t in temps for i in MP for j in OCP for k in Blenders])
       +pulp.lpSum([Cout_blending*Xplus[i][j][k][t] for t in temps for i in MP for j in OCP for k in Blenderplus])
       +pulp.lpSum([Cout_smart_blending*X[i][j][k][t] for t in temps for i in MP for j in OCP for k in SBlenders])
       +pulp.lpSum([Cout_smart_blending*Xplus[i][j][k][t] for t in temps for i in MP for j in OCP for k in SBlenderplus])
       +pulp.lpSum([Cout_blending*R[i][j][k][t] for t in temps for i in MP for j in Stock for k in Blenders])
       +pulp.lpSum([Cout_blending*Rplus_0[i][j][k][t] for t in temps for i in MP for j in Stock for k in Blenderplus])
       +pulp.lpSum([Cout_blending*Rplus_1[i][j][k][t] for t in temps for i in MP for j in Stockplus for k in Blenders])
       +pulp.lpSum([Cout_blending*Rplus_2[i][j][k][t] for t in temps for i in MP for j in Stockplus for k in Blenderplus])
       +pulp.lpSum([Cout_smart_blending*R[i][j][k][t] for t in temps for i in MP for j in Stock for k in SBlenders])
       +pulp.lpSum([Cout_smart_blending*Rplus_0[i][j][k][t] for t in temps for i in MP for j in Stock for k in SBlenderplus])
       +pulp.lpSum([Cout_smart_blending*Rplus_1[i][j][k][t] for t in temps for i in MP for j in Stockplus for k in SBlenders])
       +pulp.lpSum([Cout_smart_blending*Rplus_2[i][j][k][t] for t in temps for i in MP for j in Stockplus for k in SBlenderplus])
       +pulp.lpSum([Cout_de_stockage_MP*A[i][j][k][t] for t in temps for i in MP for j in OCP for k in Stock])
       +pulp.lpSum([Cout_de_stockage_MP*Aplus[i][j][k][t] for t in temps for i in MP for j in OCP for k in Stockplus])
       +pulp.lpSum([Cout_de_stockage_Engrais*B[i][j][k][t] for t in temps for i in Recette for j in ToutBlender for k in Stock])
       +pulp.lpSum([Cout_de_stockage_Engrais*Bplus_0[i][j][k][t] for t in temps for i in Recette for j in ToutBlenderplus for k in Stock])
       +pulp.lpSum([Cout_de_stockage_Engrais*Bplus_1[i][j][k][t] for t in temps for i in Recette for j in ToutBlender for k in Stockplus])
       +pulp.lpSum([Cout_de_stockage_Engrais*Bplus_2[i][j][k][t] for t in temps for i in Recette for j in ToutBlenderplus for k in Stockplus]))\
      +pulp.lpSum([Cout_blender*CplusF[k] for k in Blenderplus])\
      +pulp.lpSum([Cout_sblender*CplusF[k] for k in SBlenderplus])\
      +pulp.lpSum([Cout_stockage_building*SplusF[k] for k in Stockplus])



prob.solve()
