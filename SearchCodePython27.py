import os
import sys
import subprocess
import collections
import pandas as pd
import string

rootdir = sys.argv[1]
print rootdir
singlekeyword = sys.argv[2]
ExtractDir = sys.argv[3]

all_filename=[]
all_fileext=[]
all_filewords=[]

df3=pd.DataFrame(columns=['cnt','dataname','filesource'])

for folder, subs, files in os.walk(rootdir):

        for filename in files:
            if ".ext" in filename or "sql" in filename:
                  #print filename

                  a=open(os.path.join(folder, filename),"r"); b=a.read(); rows=b.split('\n')
                  p=set([])

                  for x in rows:
                   if string.find(x.upper(),singlekeyword.upper())>=0 :
                 
                        p.add(x)
                        #print x
                        all_fileext.append(x)
                   #print (p)

                  
                  counter=collections.Counter(all_fileext)

                  df=pd.DataFrame([counter.values(),counter.keys()])
                  df2=df.transpose()
                  df2.columns=['cnt','dataname']
                  df2['filesource']=filename
                  df3=df3.append(df2)
                  #cols = df2.columns.tolist()
                  #cols=cols[-1:] + cols[:-1]
               

                  

                  all_fileext=[]

                  #ax = sns.barplot(x="fname", y="cnt", data=df3)
                  #sns.plt.show()



df3.to_csv(ExtractDir,index=False)