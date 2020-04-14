from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html=urlopen('https://en.wikipedia.org/wiki/List_of_UFC_events')
bs=BeautifulSoup(html, 'html.parser')


"""
for link in bs.find('table', {'id':'Past_events'}).find_all(
        'a', title=re.compile('^(UFC|The Ultimate)')):
    if 'href' in link.attrs:
        print(link.attrs['href'])
        
        

"""

links = bs.find('table', {'id':'Past_events'}).find_all(
        'a', title=re.compile('^(UFC|The Ultimate)'))

"""
for link in links:
    print(link)
    print()
    print()
"""
    
print("Links[0]")
print(links[0].attrs['title'])


def getBody(articleURL, eventName):
    html= urlopen('http://en.wikipedia.org{}'.format(articleURL))    
    bs = BeautifulSoup(html.read(), 'html.parser')
    p_all = bs.find_all('table', {'class':'toccolours'})
    file = open(f'fight-page-table-dump/{eventName}', 'w')
    file.write(str(str(p_all).encode("utf-8")))
    file.close()
    return(p_all)
    





def getSaneFilename(filename):
    filename = filename.replace(" ", "_")
    keepcharacters = ('_')
    filename = "".join(c for c in filename if c
                       .isalnum() or c in keepcharacters).rstrip()
    return(filename + "_table")


#print(getSaneFilename(links[0].attrs['title']))


#temp_p = getBody(links[0].attrs['href'], getSaneFilename(links[0]
#                                                         .attrs['title']))

#print(temp_p)


for link in links:
    getBody(link.attrs['href'], getSaneFilename(link.attrs['title']))



"""
html = urlopen('https://en.wikipedia.org/wiki/UFC_137')
bs = BeautifulSoup(html.read(), 'html.parser')
p_all = bs.find_all('p')

"""
    