# -*- coding: utf-8 -*-
"""
@author: Sakshi
"""
from Bio.SeqUtils import GC
from Bio import SeqIO
from Bio.SeqUtils import MeltingTemp as mt
from Bio.Seq import Seq
import re
import pandas as pd
import os
import sys
import configparser
fname = sys.argv[1]
#read in the length of the target region and the length of the extension and ligation arms
config = configparser.ConfigParser()
config.read_file(open(r'config.txt'))
rep = config.get('My Section', 'Number of repeats',fallback='No Value Entered')
armlengthel = config.get('My Section', 'length of MIP ext and lig arm',fallback='No Value Entered')
targetlen = config.get('My Section', 'length of target region',fallback='No Value Entered')

alllen=int(targetlen)+int(armlengthel)+int(armlengthel)


#check definiton line for organism from excel file Organism Dictionary
#following this if organism not found ask for user input to identify the Organism
#full scientific name of the organism should be entered. Ex. Streptomyces lavendulae

df=pd.read_excel('Organism Dictionary.xlsx', index_col=None) 
org=df['Organism'].tolist()
accid=[]
seqs=[]

#Read in the sequences and definition lines from the FASTA file
with open(fname+".fasta") as fh:
    for line in fh:
        if line.startswith(">"):
            accid.append(line)
fasta_sequences = SeqIO.parse(open(fname+".fasta"),'fasta')
for fasta in fasta_sequences:
    name, sequence = fasta.id, str(fasta.seq)
    seqs.append(sequence)
bad_chars = [';', ':', '!', "*", '_']
cnt=0
cntno=0
org_notfound=[]
organism=[]
#Search for the organism against the dictionary file
for i in accid:
    for a in bad_chars:
        i=i.replace(a," ")
    #check for any special characters and remove them
    if any(o in i for o in org):
        matched = [o for o in org if o in i]
        organism.append(matched[0])
        cnt+=1
    else:
        cntno+=1
        org_notfound.append(i)
if cntno != 0:
    for i in org_notfound:
        print("An organism could not be detected in the following definition line:")
        print(i)
        print("Please enter the full scientific name of the organism:")
        org1=input()
        organism.append(org1)


arm1=[]
arm2=[]
v4seq=[]
temp=[]
gccontent=[]
temp1=[]
gccontent1=[]
stretch=[]
stretch1=[]
target=[]
mseq=[]
accid2=[]
organism2=[]

#generate arms
for s in seqs:
    indi=seqs.index(s)
    seqmain=s
    acid=accid[indi]
    org2=organism[indi]
    out =[s[i: j] for i in range(len(s)) for j in range(i + 1, len(s) + 1) if len(s[i:j]) == alllen]
    lenarm=int(armlengthel)
    for g in out:
        organism2.append(org2)
        accid2.append(acid)
        mseq.append(seqmain)
        a1=Seq(g[:lenarm])
        a2=Seq(g[-lenarm:])
        arm1.append(a1)
        arm2.append(a2)
        target.append(g[lenarm:-lenarm])
        
#get temperature, gc content, and check for polyNs
for a in arm1:
    myseq = a
    inn=arm1.index(a)
    temp.append('%0.2f' % mt.Tm_NN(myseq, nn_table=mt.DNA_NN2))
    gccontent.append(GC(myseq))
    a=str(a)
    if re.search(r"G{rep,}", a) or re.search(r"A{rep,}", a) or re.search(r"C{rep,}", a) or re.search(r"T{rep,}", a):
        stretch.append('yes')
    else:
        stretch.append('no')
for b in arm2:    
    myseq = b
    temp1.append('%0.2f' % mt.Tm_NN(myseq, nn_table=mt.DNA_NN2))
    gccontent1.append(GC(myseq))
    b=str(b)
    if re.search(r"G{rep,}", b) or re.search(r"A{rep,}", b) or re.search(r"C{rep,}", b) or re.search(r"T{rep,}", b):
        stretch1.append('yes')
    else:
        stretch1.append('no')

#output all MIPs possible for the FASTA file input by the user
df=pd.DataFrame({"Def Line":pd.Series(accid2), "Main Sequence":pd.Series(mseq),"Target region":pd.Series(target),"Extension Arm":pd.Series(arm1),"TM 1":pd.Series(temp),"GC content 1":pd.Series(gccontent),"Continuous stretch":pd.Series(stretch),"Ligation Arm":pd.Series(arm2),"TM 2":pd.Series(temp1),"GC content 2":pd.Series(gccontent1),"Continuous stretch 2":pd.Series(stretch1),"Organism":pd.Series(organism2)})

df.to_excel(fname+" MIPs.xlsx", index=False)