#read query def and alignment plus query and match then score them
import os
import pandas as pd
from Bio.Blast import NCBIXML
import collections
import configparser
config = configparser.ConfigParser()
config.read_file(open(r'config.txt'))
armlengthel = config.get('My Section', 'length of MIP ext and lig arm',fallback='No Value Entered')


result=open("Resultshuman_extarm.xml","r")
records= NCBIXML.parse(result)
item=records
dict1 = {}
key=[]
vals=[]
dicts = {}
arm11=0
armlen1=int(armlengthel)+1
#EDIT HERE
while arm11 < 11:
    key.append(arm11)
    arm11+=1
    armlen1=armlen1-1
    vals.append(armlen1)

for i in key:
        dicts[i] = vals[i]   
gaplist=[]

for record in records:
    for alignment in record.alignments:
        for hsp in alignment.hsps:
                gaplist.append(hsp.gaps)
                stringn=record.query
                stringn=stringn.split("|")
                stringn=stringn[2].split("_")
                stringn=stringn[1]
                counter1=dicts.get(int(stringn))
                f = open("extarm_out.txt", "a")
                stringhsp=str(hsp.query_start)+":"+str(hsp.query_end)
                print(record.query,file=f)
                print(stringhsp,file=f)
                print(hsp.align_length,file=f)
                print(counter1,file=f)
                
                      
#only first hsp is taken for each hit, this is the hsp with the best score
f.close()
defn=[]
st_en=[]
al_len=[]
que=[]
cnt=0

with open("extarm_out.txt", "r") as a_file:
    for line in a_file:
        stripped_line = line.strip()
        if cnt == 0: 
            defn.append(stripped_line)
            cnt+=1
        elif cnt == 1:
            st_en.append(stripped_line)
            cnt+=1
        elif cnt == 2:
            al_len.append(stripped_line)
            cnt+=1
        elif cnt == 3:
            que.append(stripped_line)
            cnt=0
posit=[]
totsco=[]
listlen=[]
highsco=armlengthel

for i in range(len(al_len)):
    #EDIT FROM HERE
    send=st_en[i].split(":")
    gaps1=gaplist[i]
    qlen=que[i]
    al=((int(send[1])-int(send[0]))+1)-int(gaps1)
    if int(al) <= 0.75*20:
        totsco.append("Pass")
    else:
        totsco.append("Fail")
duplist=[item for item, count in collections.Counter(defn).items() if count > 1]
norlist=[item for item, count in collections.Counter(defn).items() if count == 1]
findef=[]
finsco=[]
for a in duplist:
    indices=[]
    #not getting the ones which aren't duplicates
    indices = [index for index, element in enumerate(defn) if element == a]
    dupscores=[]
    alldefn=[]
    for n in indices:
        alldefn.append(defn[n])
        dupscores.append(totsco[n])
    if "Fail" in dupscores:
        findef.append(alldefn[0])
        finsco.append("Fail")
    else:
        findef.append(alldefn[0])
        finsco.append("Pass")
for i in norlist:
    index1 = [index for index, element in enumerate(defn) if element == i]
    for j in index1:
        finsco.append(totsco[j])
        findef.append(i)      

df=pd.DataFrame({"Definition Line":pd.Series(findef), "Score": pd.Series(finsco)})
df.to_excel("Extension Arm Results(Human Alignment Scored).xlsx", index=False)    