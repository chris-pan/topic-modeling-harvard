#PART 1, PART 2 and PART 3 come later;
import csv
import random
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
from sklearn.linear_model import LogisticRegression

#All files here can be found in Dropbox with the same filename

#NLP dictionary
f555 = open('/Users/christopherpan 1/Desktop/Topic Modeling Project/test_db_dict.txt','r')

dictList = []
for line in f555:
    ll = line.split('|')
    dictList.append([ll[0],ll[1]])
f555.close()

#This example uses Transient Ischemic Attack (TIA) as the main disease

cui_vecs = '/Users/christopherpan 1/Desktop/Topic Modeling Project/tia/tiaTags.csv'
#tags (cosine similarity) relative to TIA's CUI
rows = []
with open(cui_vecs, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    first = True
    for row in reader:
        if first:
            first = False
            continue
        else:
            rows.append(row)
            
rows.sort(key=lambda x: x[2], reverse = True)

#50 samples
for iiiiii in range(0,50):

    sample = []
    indexx = 0
    
    #special cases below used so that data isn't too large, important articles all kept
    for row in rows:
        r = random.random()
        if r <= float(row[2]) and float(row[2]) > 0.4:
            sample.append([row[0],row[2]])
            indexx += 1
        #special case for 0.1-0.4 range: divide cos_sim by 4
        elif float(row[2]) <= 0.4 and float(row[2]) >= 0.1 and r < float(row[2])/4:
            sample.append([row[0],row[2]])
            indexx += 1
        #special case for <0.1 range: divide cos_sim by 2
        elif r <= float(row[2])/2.0 and float(row[2]) < 0.1:
            sample.append([row[0],row[2]])
            indexx += 1
    sample.insert(0,['Filename','Tag'])

    path = '/Users/christopherpan 1/Desktop/Topic Modeling Project/tia_50Samples/' + str(iiiiii) + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    
    #make the sample
    f = open(os.path.join(path,'tiaSample.csv'), 'w')
    with f:
        writer = csv.writer(f)
        writer.writerows(sample)
    f.close()
    
    #these prints were just for me to see where the program is
    #checkpoint0
    print('sample ' + str(iiiiii))
    
    df = pd.read_csv(path + 'tiaSample.csv',sep=",")
    filenames = df['Filename']
    tag = df['Tag']
    tagsList = []
    for i in range(indexx):
        tagsList.append([filenames[i],tag[i]])
    filenamesList = []
    for fi in filenames:
        filenamesList.append(fi.replace('.txt',''))
        
    #YES/NO/UNCLEAR will be removed from actual NLP results and written here
    f = open(os.path.join(path,'NLP_RESULTS.txt'), 'w')
    
    #checkpoint1
    print('results ' + str(iiiiii))
    
    #the sample generated only has filenames, this part gets the CUI counts of only these files (cont.)
    #from the total data file (NLP output data e.g. test_db_res.txt)
    
    with open('/Users/christopherpan 1/Desktop/Topic Modeling Project/test_db_res.txt','r') as file1:
        data = file1.readlines()
        for line in data:
            title = line.split('|')[0]
            if title in filenamesList:
                a = line.replace(':YES','')
                b = a.replace(':NO','')
                c = b.replace(':UNCLEAR','')
                f.write(c)
    
    f.close()
    theTitles = []
    #only get CUIs with >0.1 cos_sim to TIA which are in this file
    with open('/Users/christopherpan 1/Desktop/Topic Modeling Project/tia/tia0.1.txt','r') as file3:
        data1 = file3.readlines()
        for line in data1:
            theTitles.append(line.split(':')[0])
            cuislol = []
    with open('/Users/christopherpan 1/Desktop/Topic Modeling Project/tia/tia0.1.txt','r') as file3:
        data1 = file3.readlines()
        for line in data1:
            cuislol.append([line.split(':')[0],line.split(':')[1].replace('\n','')])
    theDictlist = []

    #this part just makes a table with the counts for all the CUIs in each article
    with open(path + 'NLP_RESULTS.txt','r') as file2:
        data = file2.readlines()
        for line in data:
            l = line.split('|')
            cuis = l[2].split(',')
            for cui in cuis:
                cui = cui.replace('\n','')
                if cui in theDictlist:
                    continue
                elif cui in theTitles:
                    theDictlist.append(cui)
    theDictlist.sort()
    theDictlistCUIs = []
    for d in theDictlist:
        for cu in cuislol:
            if cu[0] == d:
                theDictlistCUIs.append([cu[0],cu[1]])
    res = open(path + 'NLP_RESULTS.txt','r')
    f2 = open(os.path.join(path,'CUICountstia.txt'), 'w')
    results = res.readlines()
    f2.write('filename')
    for d in theDictlistCUIs:
        f2.write(',' + d[0]+'|'+ d[1])
    f2.write('\n')
    for line in results:
        l = line.split('|')
        title = l[0].replace(',','')
        CUIs = l[2].split(',')
        f2.write(title)
        for di in theDictlist:
            count = 0
            for cui in CUIs:
                if cui.replace('\n','') == di:
                    count += 1
            f2.write(',' + str(count))
        f2.write('\n')
    f2.close()
    
    
    #checkpoint2
    print('counts ' + str(iiiiii))
    #table with counts of all CUIs generated
    
    #read table
    df = pd.read_csv(path + 'CUICountstia.txt',sep=",")
    filenamesList = []
    filenames = df['filename']
    for fil in filenames:
        filenamesList.append(fil)
    df2 = pd.read_csv(path + 'tiaSample.csv',sep=",")
    tag = df2['Tag']
    filnames = df2['Filename']
    tagsList = []
    i = 0
    for i in range(indexx):
        tagsList.append([filnames[i],tag[i]])
    tagsList.sort(key=lambda x: x[0])
    tagAppend = []
    for tag in tagsList:
        tagAppend.append(tag[1])
    df.insert(1, 'Cos_Sim', pd.Series(tagAppend))
    df.sort_values('filename')
    df = df.sort_values('Cos_Sim',ascending=False)
    df.to_csv(path + 'tiaData.csv', sep=',',header=True)

    #checkpoint3
    print('data ' + str(iiiiii))
    #tags appended to table
    
    # tag > 0.5 = 1, others are 0
    df['Bin_tag'] = (df['Cos_Sim'] > 0.5)
    df['Bin_tag'] = df['Bin_tag'].astype(object).replace({False:'0',True:'1'})
    clean_frame_train = df.drop(['filename','Cos_Sim'],axis = 1,inplace = False)
    clean_frame_train = clean_frame_train.drop(clean_frame_train.columns[0],axis = 1,inplace = False)
    y = clean_frame_train.Bin_tag
    X_train, X_valid, y_train, y_valid = train_test_split(clean_frame_train, y, test_size=0.20)
    
    #normalize data
    X_tr = normalize(X_tr.as_matrix())
    X_vl = normalize(X_vl.as_matrix())

    y_tr = y_train.as_matrix()
    y_vl = y_valid.as_matrix()
    
    #SGDClassifier allows use of both l1 and l2 penalty, in my earlier attempt (cont.)
    #I used sklearn's LogisticRegression where I only used l1 penalty
    regr = linear_model.SGDClassifier(loss='log', penalty='elasticnet', alpha=.001, l1_ratio=0.15)
    regr.fit(X_tr,y_tr)

    #checkpoint4
    print('regression ' + str(iiiiii))
    
    #get coefficients
    coefficients = regr.coef_[0]
    clean_frame_train_2 = clean_frame_train.drop(['Bin_tag'], axis = 1,inplace=False)
    pd.Series(coefficients, index=clean_frame_train_2.columns)
    coefficientList = pd.Series(coefficients, index=clean_frame_train_2.columns)
    llll = len(coefficientList)
    coeffList = []
    for i in range(llll):
        if coefficientList[i] != 0.0:
            coeffList.append([clean_frame_train_2.columns[i],coefficientList[i]])
    coeffList.sort(key=lambda x: abs(float(x[1])), reverse = True)
    f3 = open(path2 + str(iiiiii) + 'tiaWords.txt','w')
    f3.write('Disease:Transient Ischemic Attack\n')
    f3.write('SGDClassifier: alpha = 0.001, l1_ratio = 0.15\n')
    for l in coeffList:
        ll = l[0].split('|')[0]
        for lin in dictList:
            if lin[1] == ll:
                f3.write(l[0] + ',' + str(l[1]) + ' ' + lin[0] + '\n')
                break
    f3.close()

    #checkpoint5
    print('ALL ' + str(iiiiii))


#PART 2
rootdir = '/Users/christopherpan 1/Desktop/Topic Modeling Project/tia_50Samples/'

#get all variables that were selected from each of the 50 attempts

cuiDict = []

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filename=os.path.join(subdir, file)
        filna = os.path.basename(filename)
        if 'tiaWords' in filna:
            with open(filename, 'r') as filen:
                data = filen.readlines()
                isFirst = True
                isSecond = True
                for line in data:
                    if isFirst:
                        isFirst = False
                        continue
                    elif isSecond:
                        isSecond = False
                        continue
                    else:
                        l = line.split(',')
                        cui = l[0]
                        if cui in cuiDict:
                            continue
                        else:
                            cuiDict.append(cui)
            print("Done for: "+filna)
cuiDict.sort()


#PART 3
rootdir = '/Users/christopherpan 1/Desktop/Topic Modeling Project/tia_50Samples/'

#creates table: each column is a CUI/variable, each row is one of the 50 samples
#each cell is the coefficient of that CUI in that sample or 0 if it did not appear

f = open('/Users/christopherpan 1/Desktop/tiaCUIs.txt','w')
f.write('Sample')
for cui in cuiDict:
    f.write(',' + cui)
f.write('\n')
count = 0
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filename=os.path.join(subdir, file)
        filna = os.path.basename(filename)
        if 'tiaWords' in filna:
            with open(filename, 'r') as filen:
                data = filen.readlines()
                f.write(filna)
                for cu in cuiDict:
                    isFirst = True
                    isSecond = True
                    notfound = True
                    for line in data:
                        if isFirst:
                            isFirst = False
                            continue
                        elif isSecond:
                            isSecond = False
                            continue
                        else:
                            l = line.split(',')
                            cui = l[0]
                            coef = l[1][0:l[1].index(' ')]
                            if cui == cu:
                                f.write(',' + coef)
                                notfound = False
                    if notfound:
                        f.write(',' + str(0))   
            f.write('\n')
            print("Done for: "+filna)
f.close()
