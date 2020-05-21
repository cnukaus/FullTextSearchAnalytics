This script will search within a folder, find all files containing a keyword, and return all results (the line containing it, and the file name)

# FullTextSearchAnalytics


@@ usage 
@@ python path+searchcode.py FolderToScan Keyword ResultFile+path


python "SearchCode.py" "folderPath" "keyword CaseInsensitive" "e:\result.csv"


Search2addr.py is to search a xdag address list


Here I have ini config reader, or
#from .utils import read_yaml

or:with open("redlogin.txt","r") as f:
    mylist = f.read().splitlines() #remove line feed otherwise system won't like
    userprod,passwordprod,key1,sec1=mylist  

try not use global variable as will have hidden implication spagetti, instead, use tuple or class objects:
https://www.geeksforgeeks.org/g-fact-41-multiple-return-values-in-python/

f"string" to do quick replacement
f"a{var}b"
"a"+var+"b"

