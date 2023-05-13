from Bio.Blast import NCBIXML

import pandas as pd
import os
path=os.getcwd()
files = os.listdir(path)
trial_3=pd.DataFrame()

alignments=[]
start=[]
end=[]
linker=[]
matched_indexes=[]
qid=[]           
allq=[]
defn=[]
accid=[]
seqlist=[]
s=[]
f=open("extension_arms.txt","r")
ksj=1
#get ext arm sequence
for line in f.readlines():
        if ksj % 2 == 0 :
            seqlist.append(line.rstrip())
        ksj += 1
#get definition lines
with open("extension_arms.txt") as fh:
    for line in fh:
        if line.startswith(">"):
            accid.append(line)

ks=0
trialdf=pd.DataFrame()
trial_2=pd.DataFrame()
trialdfh=pd.DataFrame()
trial_2h=pd.DataFrame()
count=0
toff=0
numdds=0
human_match=[]
for i in files:
    if "Resultsall_extarm.xml" in i:
        result=open(i,"r")
        records= NCBIXML.parse(result)
        item=records
        a=0
        for record in records:
            toff+=1
            k=0
            if a==0:
                ks=0
            else:
                ks+=1
            allq.append(record.query)

            for alignment in record.alignments:

                numdds+=1
                
                start=[]
                if alignment.hit_def:
                    
                    start.append(accid[ks])
                for hsp in alignment.hsps:
                    #only first hsp is taken for each hit, this is the hsp with the best score
                    qcov=(hsp.query_end - hsp.query_start + 1)/(record.query_length)
                    start.append(hsp.query_start)
                    start.append(hsp.query_end)
                    start.append(alignment.hit_def)
                    ident=(hsp.identities/ hsp.align_length)*100
                    evalue=hsp.expect

                    start.append(ident)
                    start.append(evalue)
                    start.append(qcov)
                    accidfin=alignment.accession
                    start.append(accidfin)
                    allq.append('')
                    trialdf=pd.DataFrame({"Def Line":pd.Series(start[0]),"Start":pd.Series(start[1]),"End":pd.Series(start[2]),"Alignment Definition":pd.Series(start[3]),"Ident":pd.Series(start[4]), "Eval":pd.Series(start[5]), "Query coverage":pd.Series(start[6]), "Alignment Accession":pd.Series(start[7])})
                    break
                trial_2=pd.concat([trial_2,trialdf], axis=0)
                a+=1

ks=ks+1
trial_2.to_excel('MIP parsed all.xlsx', index=False)
