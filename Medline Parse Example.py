from bs4 import BeautifulSoup
#Use BeautifulSoup to clean up html files
#BeautifulSoup documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

html_doc = '/Users/christopherpan 1/Desktop/TOPIC MODELING PROJECT/OLD/medlineplus.gov/ency/article/000423.htm'

data = ''
with open(html_doc, 'r') as f:
    data = f.read().replace('\n', '') 
#New lines appear as \n in the html file so this removes all of them
    
soup = BeautifulSoup(data, 'html.parser')
#Create "soup" to work on

#print(soup.prettify) prints what the "soup" looks like

def get_plain_text(soup):
    for el in soup.find_all('li'):
        el.insert(0, '123456')
        el.append('123456')
    for el in soup.find_all('p'):
        el.insert(0, '123456')
        el.append('123456')
    for el in soup.find_all('h2'):
        el.insert(0, '123456')
        el.append('123456')
    #123456's are inserted and then replaced later on by \n so that the final text file looks like the actual page
    elements1 = soup.find_all('div', id = 'section-Ref')
    for element in elements1:
        element.decompose()
    elements2 = soup.find_all('div', id = 'section-version')
    for element in elements2:
        element.decompose()
    elements3 = soup.find_all(class_ = 'adam-info')
    for element in elements3:
        element.decompose()
    elements4 = soup.find_all(class_ = 'videobox')
    for element in elements4:
        element.decompose()
    elements5 = soup.find_all(class_ = 'section img-thumb')
    for element in elements5:
        element.decompose()
    #element.decompose() removes unnecessary elements
    #For example, all elements with the tag 'videobox' are videos 
    #You have to look through the page source (or soup.prettify) to find the tags of unnecessary elements
    plain_text = ''
    #For Medline articles, class_ = 'main-single' contains the content of the text
    for el in soup.find_all(class_ = 'main-single'):
        plain_text += el.get_text()
    plain_text = plain_text.replace(u'\xa0', ' ')
    final_text = ''
    if 'References' in plain_text:
        i = 0
        while i < (plain_text.index('References')):
            final_text += plain_text[i]
            i += 1
    #In Medline, I did not want the References part of the text so I removed it
    else:
        final_text = plain_text
    return final_text

print(soup.title.string)
#Title of the article

a = (repr(get_plain_text(soup)).replace('\\','')) #repr turns it into a string
#Replaces are specific to Medline
b = a.replace('.', '. ')
c = b.replace('123456', '\n')
d = c.replace('123456', '\n')
print(d[1:len(d)-1]) #Remove ' at beginning and end of string



#After running ^ on all files, run this on all text files to remove all empty lines or white spaces at the beginning of the line (This is separate code)
import os

with open('/Users/christopherpan 1/Desktop/TOPIC MODELING PROJECT/FINAL DATA/Medline/000001.htm.txt', 'r') as filen:
    complete = os.path.join('/Users/christopherpan 1/Desktop/TOPIC MODELING PROJECT/', 'test.txt') 
    f = open(complete, 'w')
    for i in filen.readlines():
        if not i.strip():
            continue
        f.write(i)
