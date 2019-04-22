import os
import re
import nltk
import pandas as pd
from collections import defaultdict
from collections import OrderedDict
import time
import json




directory = r"C:\Users\PCS\Desktop\ir-assignment\ShortStories"
directory2= r"C:\Users\PCS\Desktop\ir-assignment"
pathpositional = r"C:/Users/PCS/Desktop/ir-assignment/positional.txt"
pathinverted = r"C:/Users/PCS/Desktop/ir-assignment/inverted.txt"

stoplist = dict()
       
#storing stopwords file in dictionary 
#with open('list.txt','r') as readl:
 #     stoplist = readl.read() 

stoplist = "a is the of all and to can be as once for at am are has have had up his her in on no we do"

stoplist=nltk.word_tokenize(stoplist)

x=1
dictionary = {}
positionalindex ={}

##converting all documents and files in dictionary



x=1
dictionary = {}

for filename in (os.listdir(directory)):
    #print(filename)
    f = os.fsdecode(filename)
    if f.endswith(".txt"):
        story = open(r'C:\Users\PCS\Desktop\ir-assignment\ShortStories\\' + filename)
        stripslash = '.txt'
        filename = ''.join(char for char in filename if char not in stripslash)
        c=int(filename)
        x=c
        dictionary[c]= story.read()
        #print(c , dictionary[c])
        dictionary[c]= dictionary[c].lower()
            
        #removing stop words
        
    for k in range(len(stoplist)):
        r = stoplist[k]
    # print(r)
    dictionary[x] = re.sub( r"\s+" + stoplist[k] + "\s"," ",dictionary[x] )
   
        #removing all unnecessary punctutations , keeping the word clean
   
    dictionary[x] = re.sub(r"'","",dictionary[x] )
    dictionary[x] = re.sub(r"_"," ",dictionary[x] )
    dictionary[x] = re.sub(r";","",dictionary[x] )
    dictionary[x] = re.sub(r"\?","",dictionary[x] )
    dictionary[x] = re.sub(r","," ",dictionary[x] )
    
    dictionary[x] = re.sub(r"\W"," ",dictionary[x] )
    dictionary[x] = re.sub(r"\d"," ",dictionary[x] )
    dictionary[x] = re.sub(r"\s+"," ",dictionary[x])  
        
    x +=1;
        

##creating an positional index

for i in range(1,51):        
    positionalindex[i] = nltk.word_tokenize(dictionary[i])
    

if os.stat(directory2).st_size != 0:
    
    invertedindex = defaultdict(list)
    a=1
    s=0
    for keys,values in sorted(positionalindex.items()):
        for value in values:
            if value not in stoplist:
                if value not in invertedindex:
                    invertedindex[keys].append(value)                #x = 'document: {}'.format(keys)

    positionalindex = invertedindex    
    
    
    with open(pathpositional, 'w') as outfile:
        json.dump(positionalindex, outfile)
else:
    with open(pathpositional, 'r') as f:
        positionalindex = json.load(f)  
          
    
######### CREATING INVERTED INDEX

invertedindex = defaultdict(list)

    
if os.stat(directory2).st_size != 0:
    a=1
    s=0
    for keys,values in sorted(positionalindex.items()):
        for value in values:
            if value not in stoplist:
                if value not in invertedindex:
                    
                    x= keys
                    l = [x]
                    invertedindex[value]=l
                # print("------------------------------------")
                #print ("value:            " , value)
                #print("key:            " , keys)
                #print("values*********:            " , values)
                    a=a+1
                #print("\n\n\n")
                else :
                
               
                    k = invertedindex.get(value)
                    x= keys
                    l.append(x)
                    l = (list(OrderedDict.fromkeys(k)))
                
                    l = pd.unique(l).tolist()
                    
                    if len(l) == 2:
                        if l[0] == l[1]:
                            l.pop(1)
                    
                    invertedindex[value]=l
                
    with open(pathinverted, 'w') as outfile:
        json.dump(positionalindex, outfile)
else:
    with open(pathinverted, 'r') as f:
        positionalindex = json.load(f)  
          
    


query = input("Enter Query:    ")
start = time. time()

pquery=nltk.word_tokenize(query)

#print("pquery:        ",pquery)
pq = {} #query list
n="not"
a="and"
o="or"
z=0
no=0

###########BOOLEAN QUERY PORTION
if (len(pquery)) == 1:
    
    print("Query:   ", query)
    print("Document: ")
    
    print(invertedindex.get(pquery[0]))
    
    print("Total Document:  ",len(invertedindex.get(pquery[0])))

elif (len(pquery)) == 2:  #only for not query
    i=0;
    if n in pquery:
       # print(pquery[i])
        del pquery[i]
            
        print("Query:   " , query)
        print("Document:  ")
        l=1
        pl=invertedindex.get(pquery[i])
        for i in range(1,x):
            if i not in pl:
                l +=1
                print(i , end =" ")
         
        print("Total Document:  ",l )      
elif (len(pquery)) == 3:
    #print("Entered 3rd query")
    i=0
    pl1=[]
    pl2=[]
    if n in pquery:
        no=0;
        for i in range(i,4):
            if n != pquery[no]:
                no +=1
                       
        del pquery[no]
        #print(pquery)
            
        k=invertedindex.get(pquery[no])
         
        s=0
        l=[]
        for i in range(1,x):
            # if i in k:
            l.append(x)
            l = (list(OrderedDict.fromkeys(k)))
            print(l)
            
        invertedindex[pquery[no]]=pl
        z +=1
    if a in pquery:
        
        pl1 = invertedindex.get(pquery[0])
        pl2 = invertedindex.get(pquery[2])
            #print("i: ", i)
        l=1        
        print("Query:   ",query)
        print("Document:  ")
        for item in pl2:
            if item in pl2:
                l +=1
                print(item , end=" ")
    
        print("Total Document:  ",l)                            
    if o in pquery:
        pl1 = invertedindex.get(pquery[0])
      #  print("pl1:   " ,pl1)
        pl2 = invertedindex.get(pquery[2])
      #  print("pl2:   " ,pl2)
        
        pl1 = pl1+pl2
        pl1 = pd.unique(pl1).tolist()
        
            
        print("Query:   ",query)
        print("Document:  ", pl1)
        print("Total Document:  ",len(pl1))     
        
elif (len(pquery)) >= 5:
    d=[]
    pl1=[]
    pl2=[]
    for r in pquery:
        
        i=0 
        if a in pquery:
            no=0
            pl1 = invertedindex.get(pquery[no])
            del pquery[no]
            del pquery[no]
      
            pl2 = invertedindex.get(pquery[no])
       
            
            
            for x in pl1:
                if x in pl2:
                    d.append(x)
            
       #     pl1 = (list(OrderedDict.fromkeys(pl1)))
            del invertedindex[pquery[no]]
            invertedindex[pquery[no]]=d
                           
            #print("length:   " ,len(pquery))
               
            
            if (len(pquery)) <= 1:
                print("Query:   ",query)
                print("Document:  ", d)
                print("Total Document:  ",len(d))   
       
        if o in pquery:
            no=0
            
            pl1 = invertedindex.get(pquery[no])
            del pquery[no]
            del pquery[no]
            pl2 = invertedindex.get(pquery[no])
       
            pl1 = pl1+pl2
            pl1 = pd.unique(pl1).tolist()
                
            
     
            del invertedindex[pquery[no]]
            invertedindex[pquery[no]]=pl1
       
            
            if (len(pquery)) <= 1:
                print("Query:   ",query)
                print("Document:  ", pl1)
                print("Total Document:  ",len(pl1)) 

end = time. time()
print("The total process by query is",end - start)
               
        
########positional index query
start = time. time()
query = input("Enter Positional Query:    ")
ppquery=query
stripslash = '/'
ppquery = ''.join(char for char in ppquery if char not in stripslash)

ppquery=nltk.word_tokenize(ppquery)
a=2
p=0;
b=ppquery[1]
#print("b:     ",b)
c=ppquery[2]
a = a + int(c)
#print(a)
for k,v in positionalindex.items():    
    i=0
    w=0
    for item in v:
        #print ("Document No:    ", k, " Term:      ", item , "at index:    " , i )
        l={}
        f=0
        d=0
        i+=1
        p = i
        doc = k
        if ppquery[f] == item:
          #  print("d:   ", d , item , ppquery[f])
            l[d]=item
            f+=1
            for y in range(1,a):
                strg = positionalindex[doc][p]
             #   print( "doc: " ,doc , "p:  " ,p,"strg:        " , strg, "ppquery :" ,ppquery[f])
                d=d+1
                l[d]=positionalindex[doc][p]
                p=p+1
            
        if (len(l)) == a :
            if l[len(l)-1] == b:
                print("Query:   " ,query)
                print("Document no: " , doc)
                print(l.values())
            
    
end = time. time()
print("The total process by query is",end - start)


        


    
