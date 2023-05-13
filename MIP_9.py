import pandas as pd
import os
import re
import sys
name1="Extension Arm Results(No Matches)"
name1=name1+".xlsx"
name2="BLAST Organism Check(Only perfect)"
name2=name2+".xlsx"
name3="Extension Arm Results(Human Alignment Scored).xlsx"
name4="Extension Arm Results(No Human Matches).xlsx"
output = sys.argv[1]
number=[]
orgdef=[]

df=pd.read_excel(name1, index_col=None)
df2=pd.read_excel(name2, index_col=None)
df3=pd.read_excel(name3, index_col=None)
df4=pd.read_excel(name4, index_col=None)
nohit_hum=df4['Definition Line'].tolist()
defn_hum=df3['Definition Line'].tolist()
score_hum=df3['Score'].tolist()
nohit_def=df['Definition Line'].tolist()
orgcheck=df2['Organism Check'].tolist()
defline_perf=df2['Def Line'].tolist()
defline_perf = list(set(defline_perf))
perfdef=[]
hum_pass=[]
hum_fail=[]

for a in range(len(defn_hum)):
    if score_hum[a]=="Pass":
        hum_pass.append(defn_hum[a])
    else:
        hum_fail.append(defn_hum[a])
        continue
for j in nohit_hum:
    hum_pass.append(j)

hum_pass=list(set(hum_pass))
#obtain all the MIPs which passed for human alignment
for a in defline_perf:
    a=a.strip()
    perfdef.append(a)
    val = a.rpartition("|")
    orgdef.append(val[0])

cnt=0
test=[]
stripped_perf = list(map(str.strip, defline_perf))
stripped_hit = []
for i in nohit_def:
    i=i.strip()
    i=">"+i
    stripped_hit.append(i)

allcheck=[]
all_humcheck=[]
cnt=0
test=[]
pass_hum=[]
hum_final=[]
for a in hum_pass:
    nstry=">"+a
    pass_hum.append(nstry)

for i in range(len(orgdef)):
    org1=orgdef[i]
    cnt1=0
    cnt1=org1.split("_")
    cnt=cnt1[1].split("|")
    stringn=str(org1)+"|check_"+str(cnt[0])
    test=[]
    if stringn in pass_hum:
        test.append(stringn)
        val = test[0].rpartition("|")
        hum_final.append(val[0])

cnt=0
test=[]
final=[]
for i in range(len(orgdef)):
    org1=orgdef[i]
    cnt1=0
    cnt1=org1.split("_")
    cnt=cnt1[1].split("|")
    stringn=str(org1)+"|check_"+str(cnt[0])
    test=[]
    if stringn in stripped_hit:
        test.append(stringn)
    if stringn in stripped_perf:
        test.append(stringn)
    else:
        continue
    val = test[0].rpartition("|")
    final.append(val[0])
#done until here
finfin=[]
for i in final:
    if i in hum_final:
        finfin.append(i)
finfin=list(set(finfin))
column_names=["Def Line","Main Sequence","Target region","Extension Arm","TM 1","GC content 1","Continuous stretch","Ligation Arm","TM 2","GC content 2","Continuous stretch 2","Organism"]
df_fin=pd.DataFrame(columns = column_names)
df_org=pd.read_excel('Passable MIPs.xlsx', index_col=None)
index=[]
for i in finfin:
    string_index=i.split("_")
    string_index=string_index[1].split("|")
    index.append(string_index[0])
for ind in index:
    ind=int(ind)
    if ind==len(df_org):
        break
    entry = df_org.loc[ind]
    df_fin = df_fin.append(df_org.iloc[ind])
df_fin.to_excel(output+".xlsx", index=False)