# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 18:18:33 2021

@author: Asus
"""

# Filter for organism
import pandas as pd
import os
import re

name1="Resultsall_extarm.xml"

path=os.getcwd()
files = os.listdir(path)

#open the results file


trial_3=pd.DataFrame()

accid=[]
organisms=[]
abb=[]
df2=pd.read_excel('Organism Dictionary.xlsx', index_col=None)
orglist=df2['Organism'].tolist()
syno=df2['Synonyms'].tolist()
abbr=df2['Abbreviations'].tolist()
df=pd.read_excel('MIP parsed all.xlsx', index_col=None) 
defline=df['Alignment Definition'].tolist()
accid=df['Def Line'].tolist()
syn=[]


#>Akkermansia_muciniphila beta sliding clamp whole region_0|Akkermansia muciniphila
#>Akkermansia_muciniphila beta sliding clamp extension arm_0|Akkermansia muciniphila|check_0
#>coaE [Akkermansia muciniphila] extension arm_0|Akkermansia muciniphila|check_0
for s in accid:
    s=s.strip()
    pattern = "\|(.*?)\|"
    val = re.search(pattern, s).group(1)
    organisms.append(val)
    for a in orglist:
        if a.lower() == val.lower():
            indexli=orglist.index(a)
            st=syno[indexli]
            at=abbr[indexli]
            syn.append(st)
            abb.append(at)
            break

freqs=[]
for i in accid:
    freqs.append(accid.count(i))

presentorg=[]
cnt=1
new=[]
for i in range(len(defline)):
    aldef=defline[i]
    org=organisms[i]
    freqcnt=freqs[i]
    synonym=syn[i]
    abbrevi=abb[i]
    if org in aldef:
        new.append('yes')
    elif str(synonym) in aldef:
        new.append('yes'+str(synonym))
    elif str(abbrevi) in aldef:
        new.append('yes'+str(abbrevi))
    else:
        new.append('no')
    if len(new) == freqcnt:
        if 'no' in new:
            for h in range(freqcnt):
                presentorg.append("Different Organism Found")
            
        else:
            for h in range(freqcnt):
                presentorg.append("Perfect Match Found") 
    
    cnt+=1
    if len(new)==freqcnt:
        new=[]
        cnt=0       

df["Organism Check"]=presentorg

df.to_excel('BLAST Organism Check.xlsx', index=False)
df = df[~df['Organism Check'].isin(['Different Organism Found'])]
df.to_excel('BLAST Organism Check(Only perfect).xlsx', index=False)
#Everything works until here