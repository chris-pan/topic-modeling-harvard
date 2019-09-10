from scipy import spatial
import csv
import os

#Vector file
cui_vecs = '/Users/christopherpan 1/Desktop/TOPIC MODELING PROJECT/cui_vecs_500.csv'
count = 0
with open(cui_vecs, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        count += 1

stroke = []

with open(cui_vecs, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        #C0553692 = hemorrhagic stroke
        #C0948008 = ischemic stroke
        #C0007787 = TIA
        #C0344315 = Depression
        #C0010068 = Coronary artery disease
        #C0003873 = Rheumatoid arthritis
        if row[0] == 'C0553692':
            stroke = row[1:len(row)]
            stroke = list(map(float, stroke))
count = 0

StrokeCUIs = []
with open(cui_vecs, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    first_row = True
    for row in reader:
        if first_row:
            first_row = False
            continue
        else:
            test_row = row[1:len(row)]
            test_row = list(map(float, test_row))
            cos_sim = 1 - spatial.distance.cosine(stroke, test_row)
            StrokeCUIs.append([row[0], cos_sim])
            count += 1
StrokeCUIs.sort(key=lambda x: x[1], reverse=True)
f = open(os.path.join('/Users/christopherpan 1/Desktop','StrokeCOS_SIM.txt'), 'w')
for CUI in StrokeCUIs:
	f.write(CUI[0] + ':' + str(CUI[1]) + '\n')
f.close()