# -*- coding: utf-8 -*-
"""
@author: Sakshi
"""
import math
import os
import pandas as pd
from Bio.Seq import Seq
import random
from collections import OrderedDict
os.chdir(r"") #location of the appended file
fname="final_dnaN_results.xlsx" #put file with all apeended results files for genes, 16s, ITS, etc.
df = pd.read_excel (fname)
defold = df["Def Line"].tolist()
lig = df["Extension Arm"].tolist()
#ext = df["Extension Arm"].tolist()
ndef=[]
count=0

for j in defold:
    j=str(count)+"**"+j
    ndef.append(j)
    count+=1

defold=ndef
lenofligfin=len(lig)
def mipscore(fmip,countmip,lig,ext,defold):
    #MIP comparison code
    import os
    import pandas as pd
    from Bio.Seq import Seq
    ligarm = lig
    extarm = ext
    defline = defold
    cntmip=countmip
    newdef=[]
    count=0
    for i in defline:
        i=i.strip()
        newi=str(i)+" arm_"+str(count)+"|index_"+str(cntmip)
        newdef.append(newi)
        count+=1
    MIPtest=fmip
    MIPtest=Seq(MIPtest)
    #take complement of first MIP to check for what it can bind to
    compMIP=MIPtest.complement()
    l10=input("How many basepairs would you like to check against?")
    all_scores=[]
    last10test=[]
    last10testext=[]
    last10org=[]
    all_scores_ext=[]
    defn=[]
    defcounts=0
    compared_mip=[]
    querymip=[]
    score=[]
    for i in ligarm:
        scr = 0
        set_string1 = list(compMIP)
        tenorg=set_string1[-l10:]
        set_string2 = list(i)
        tentest=set_string2[-l10:]
        iter1 = 1
        for org, test in zip(tenorg, tentest):
            if org == test:
                scr = scr + iter1
            iter1 = iter1 + 1       
        
        last10org.append(str(tenorg))
        last10test.append(tentest)
        querymip.append(compMIP)
        compared_mip.append(i)
        if scr >= 6:
            score.append(newdef[defcounts])
        else:
            score.append('None')
        defcounts+=1
    queryind=[]
    for i in newdef:
        queryind.append(newdef[cntmip])
    df=pd.DataFrame({"Query Index":pd.Series(queryind),"Index":pd.Series(newdef),"Query MIP":pd.Series(querymip), "Compared Basepairs(Ligation)": pd.Series(last10test), "Compared Basepairs(Query)": pd.Series(last10org), "Extension Arm Score": pd.Series(score)})
    df.to_excel("CHECK"+str(countmip)+".xlsx",index=False)
    return df
    
final_dict=OrderedDict()
list_of_ind=[]
cnt=0
countmip=0
finalmiplist=[]
finaldef=[]
failmip=[]
faildef=[]
failig=[]
finalig=[]

outputfilecompmip=[]
outputfileindexes=[]
outputfilerandmip=[]
no_match=[]
no_match_def=[]

for i in lig:
    vals=[]
    indexval=[]
    df2=mipscore(i,countmip,lig,ext,defold)
    lsc = df2["Extension Arm Score"].tolist()
    lsc = [x for x in lsc if str(x) != 'nan']
    query1 = df2["Query Index"].tolist()
    q1=query1[0]
    outputfilecompmip.append(q1)
    final_dict[q1] = df2
    for n in lsc:
        if n == "None" or n == 'nan':
            continue
        else:
            vals.append(n)    
    queryval=q1.split("arm_")
    queryval=queryval[1].split("|")
    indexval.append(int(queryval[0]))
    for j in vals:
        j=str(j)
        valstring=j.split("arm_")
        valstring=valstring[1].split("|")
        indexval.append(int(valstring[0]))
    indexforout=indexval
    ranelem=random.choice(indexval)
    lc=indexval.index(ranelem)
    indexval.pop(lc)
    indexval=sorted(indexval)
    for ele in sorted(indexval, reverse=True):
        del defold[ele]
        del lig[ele]
    countmip+=1
    cnt+=1
allkey=[]
allvalues=[]
for keys,values in final_dict.items(): 
    allkey.append(keys)
    allvalues.append(values)
lastdf=allvalues[-1]
leftover = lastdf["Index"].tolist()
fin_df=pd.DataFrame()
column_names=["Def Line","Main Sequence","Target region","Extension Arm","TM 1","GC content 1","Continuous stretch","Ligation Arm","TM 2","GC content 2","Continuous stretch 2","Organism"]
fin_df=pd.DataFrame(columns = column_names)
df_org = pd.read_excel (fname)
for i in leftover:
    stringind1=i.split("**")
    finind=int(stringind1[0])
    if finind==len(df_org):
        break
    entry = df_org.loc[finind]
    fin_df=fin_df.append(entry)
fin_df.to_excel("Final List.xlsx",index=False)
