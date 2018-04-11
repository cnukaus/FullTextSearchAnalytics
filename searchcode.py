import os
import sys
import subprocess
import collections
import pandas as pd
import string

rootdir = sys.argv[1]
print(rootdir)
singlekeyword = sys.argv[2]
ExtractDir = sys.argv[3]

all_filename=[]
all_fileext=[]
all_filewords=[]

df3=pd.DataFrame(columns=['cnt','dataname','filesource'])

for folder, subs, files in os.walk(rootdir):

        for filename in files:
            try:#if  #".ext" in filename or "sql" in filename:
                  #print filename

                  a=open(os.path.join(folder, filename),"r"); b=a.read(); rows=b.split('\n')
                  p=set([])

                  for x in rows:
                   if x.upper().find(singlekeyword.upper())>=0 :
                   
                        p.add(x)
                        #print x
                        all_fileext.append(x[:1000])
                   #print (p)

                  
                  counter=collections.Counter(all_fileext)

                  df=pd.DataFrame([list(counter.values()),list(counter.keys())])
                  df2=df.transpose()
                  df2.columns=['cnt','dataname']
                  df2['filesource']=filename
                  df3=df3.append(df2)

                  all_fileext=[]

            except:
                  pass#sys.logging("Error")  



df3.to_csv(ExtractDir,index=False)