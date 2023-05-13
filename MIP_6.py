#MIP ligation arm code
import os
import pandas as pd
from bs4 import BeautifulSoup
 
fd = open('Resultsall_extarm.xml', 'r')
 
xml_file = fd.read()
 
soup = BeautifulSoup(xml_file, 'lxml')
alltext=soup.get_text()
file1 = open("soup_text_all.txt","a")
file1.write(alltext)
cnt=1
textblck=[]

with open("soup_text_all.txt", "r") as a_file:
    for line in a_file:
        stripped_line = line.strip()
        textblck.append(stripped_line)
nohit=[]
result=[]
for i in textblck:
    if i == "No hits found":
        index1=textblck.index(i)-15
        nohit.append(textblck[index1])
        result.append("No Hits")
        textblck.pop(textblck.index(i))
df=pd.DataFrame({"Definition Line":pd.Series(nohit), "Hit":pd.Series(result)})
df.to_excel("Extension Arm Results(No Matches).xlsx", index=False)
file1.close()