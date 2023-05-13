# -*- coding: utf-8 -*-
"""
@author: Sakshi
"""
import pandas as pd
from Bio.Seq import Seq
df = pd.read_excel (r"Passable MIPs.xlsx")
extarm = df["Extension Arm"].tolist()
accid = df["Def Line"].tolist()
org = df["Organism"].tolist()
fname3="extension_arms"
tag2=[]
tag3=[]
tag4=[]
cnt2=0
#number the sequences and add the organisms to the definition line
for k in accid:
    k=k.rstrip("\n")
    tag4.append(k+" extension arm"+"_"+str(cnt2)+"|"+org[cnt2])
    cnt2+=1
efile = open(fname3+".txt","w")
cnt=0
#create a FASTA file with new definition lines and the arm1+target+arm2 sequence
for i in range(len(accid)):
    earm=Seq(extarm[i])
    efile.write(str(tag4[i])+"|check"+"_"+str(i)+"\n"+str(earm)+"\n")
    cnt+=1
efile.close()