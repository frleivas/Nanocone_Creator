#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 14:49:47 2024

@author: frleivas
"""
import numpy as np
import math as mt
import matplotlib.pyplot as plt
import matplotlib.style as style 
from random import seed
seed(8)

style.use('seaborn-poster')
dr = 0.142                #distancia entre átomos
phi = 60*mt.pi/180        #ângulo do pentagono
theta = 300*mt.pi/180     #ângulo disclinação
apx = 19.2*mt.pi/180      #ângulo apice


L = 10                    #tamanho folha de grafeno para o cone
Lg = 4                    #tamanho folha de grafeno para pistão

no = 343                  #numero de oxigênios

n = int((L+0.1)/(2*dr*mt.sin(phi)))
m = int((L+0.1)/(dr*mt.cos(phi)+2*dr))
N = 4*m*n                 #número total de átomos da folha de grafeno

# Constroi folha de grafeno por linhas

x = []
y = []
dy = (2*dr*mt.cos(phi)+2*dr)
drsin = dr*mt.sin(phi)
drcos = dr*mt.cos(phi)
for j in range (0, m):
    for i in range (0,n):
        x.append(2*drsin*i)
        y.append(j*dy)
    for i in range (0,n):
        x.append(x[i] + drsin)
        y.append(j*dy + drcos)
    for i in range (0,n):
        x.append(x[i] + drsin)
        y.append(j*dy + (drcos+dr))
    for i in range (0,n):
        x.append(x[i])
        y.append(j*dy + (2*drcos+dr))
            
# Tornando grafeno redondo
xr = []
yr = []

Nr=0
for i in range (0,N):
    if ( mt.sqrt((x[i]-(L/2))*(x[i]-(L/2))+(y[i]-(L/2))*(y[i]-(L/2))) <= (L)/2):
        xr.append(x[i]- L/2)
        yr.append(y[i]- L/2)
        Nr+=1
        
# Cortando ângulo de disclinação

xf = []
yf = []

ang = 2*mt.pi - theta
Nf=0  
if (theta > mt.pi):    
    for i in range (0,Nr):
        xi=xr[i] ; yi=yr[i]
        r = mt.sqrt(xi*xi + yi*yi) 
        if( (yi > 0) and (xi > 0) and (r > 0.5)  and np.arccos(xi/r) < ang):
            xf.append(xi)
            yf.append(yi)
            Nf+=1
           
# Troca de coordenadas para torcer q folha
alpha = []
l = []
X = []
Y = []
Z = []

for i in range (0,Nf):
        l.append(mt.sqrt((xf[i])*(xf[i]) + (yf[i])*(yf[i])))
        alpha.append(np.arcsin((yf[i])/l[i]))
        X.append(((l[i]*ang)/(2*mt.pi))*mt.cos((alpha[i]*2*mt.pi)/ang))
        Y.append(((l[i]*ang)/(2*mt.pi)) * mt.sin((alpha[i]*2*mt.pi)/ang))
        Z.append(-l[i]* mt.sqrt(1 - ang/(2*mt.pi)))

# Plotando átomos e suas ligações (2D e 3d)

p = np.zeros( (Nf, Nf) )
fig = plt.figure()
ax = plt.axes(projection='3d')
for j in range (0,Nf):
    for i in range (0,Nf): 
        xi = X[i] ; yi = Y[i] ; zi = Z[i] 
        xj = X[j] ; yj = Y[j] ; zj = Z[j] 
        rr = mt.sqrt((xi-xj)*(xi-xj)+(yi-yj)*(yi-yj)+(zi-zj)*(zi-zj))
        if(abs(rr-dr) < 0.03): 
            #distm.write(str(rr-dr)+'  '+str(rr)+'  '+'\n')
            p[i][j]=1.
            ax.plot3D([X[i],X[j]], [Y[i],Y[j]], [Z[i],Z[j]], 'cornflowerblue');
