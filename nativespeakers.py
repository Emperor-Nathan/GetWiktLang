from bs4 import BeautifulSoup
from requests import get

langlist = []

allfile = open('all.txt', 'r')
t = '*'
la = ''
mode = 1
rr = ''
while t:
    t = allfile.read(1)
    if t == '\n':
        langlist.append(la)
        mode = 1
        nu = ''
        la = ''
    elif t == '&':
        mode = 2
    else:
        if mode == 1:
            la += t
        elif mode == 2:
            if t == '#':
                rr = ''
            elif t == ';':
                la += chr(int(rr))
                rr = ''
                mode = 1
            else:
                rr += t

langfile = open('nativespeakers.txt', 'w')
m = 0
print('Total:', len(langlist))
for a in langlist:
    m += 1
    print(m)
    if a[:6] == 'Proto-':
        continue
    ls = a
    if ls[(len(ls)-9):] != ' Language':
        ls += ' language'
    wtpage = BeautifulSoup(get('https://en.wiktionary.org/wiki/Category:'+ls).content, 'html.parser')
    ex = wtpage.find('a', {'title': 'extinct language'})
    if ex != None:
        continue
    try:
        datakey = wtpage.find('table', {'class':'wikitable language-category-info'}).find_all('a', {'class':'external text'})[1].getText()
    except AttributeError:
        continue
    except IndexError:
        continue
    datapage = BeautifulSoup(get('https://www.wikidata.org/wiki/'+datakey).content, 'html.parser')
    speakerdiv1 = datapage.find('div', {'id':'P1098'})
    try:
        speakerdiv2 = speakerdiv1.find_all('div', {'class':'wikibase-statementview-mainsnak-container'})
    except AttributeError:
        continue
    maxyear = 0
    best = 0
    n = 0
    found = False
    while n < len(speakerdiv2):
        properties = speakerdiv2[n].find_all('div', {'class':'wikibase-snaklistview-listview'})
        year = 0
        native = False
        juris = False
        for b in properties:
            propname = b.find('div', {'class':'wikibase-snakview-property'}).find('a')
            if propname['title'] == 'Property:P585':
                try:
                    ytext = b.find('div', {'class':'wikibase-snakview-value wikibase-snakview-variation-valuesnak'}).getText()
                    if ytext[len(ytext) - 1] == 's':
                        year = int(ytext[:4])
                    elif ytext[(len(ytext) - 7):] == 'century':
                        year = int(ytext[:2]) * 100 - 99
                    elif ytext[len(ytext) - 5] == ' ':
                        year = int(ytext[(len(ytext) - 4):])
                    else:
                        year = int(ytext)
                except AttributeError:
                    year = 0
            elif propname['title'] == 'Property:P518':
                if b.find('div', {'class':'wikibase-snakview-value wikibase-snakview-variation-valuesnak'}).find('a')['title'] == 'Q36870':
                    native = True
            elif propname['title'] == 'Property:P1001':
                juris = True
        if year > maxyear and native and not juris:
            found = True
            maxyear = year
            best = n
        n += 1
    if not found:
        while n < len(speakerdiv2):
            properties = speakerdiv2[n].find_all('div', {'class':'wikibase-snaklistview-listview'})
            year = 0
            second = False
            juris = False
            for b in properties:
                propname = b.find('div', {'class':'wikibase-snakview-property'}).find('a')
                if propname['title'] == 'Property:P585':
                    try:
                        ytext = b.find('div', {'class':'wikibase-snakview-value wikibase-snakview-variation-valuesnak'}).getText()
                        if ytext[len(ytext) - 1] == 's':
                            year = int(ytext[:4])
                        elif ytext[(len(ytext) - 7):] == 'century':
                            year = int(ytext[:2]) * 100 - 99
                        else:
                            year = int(ytext)
                    except AttributeError:
                        year = 0
                elif propname['title'] == 'Property:P518':
                    if b.find('div', {'class':'wikibase-snakview-value wikibase-snakview-variation-valuesnak'}).find('a')['title'] == 'Q125421':
                        second = True
                elif propname['title'] == 'Property:P1001':
                    juris = True
            if year > maxyear and not second and not juris:
                found = True
                maxyear = year
                best = n
            n += 1
    try:
        speakerdiv = speakerdiv2[best].find('div', {'class':'wikibase-snakview-value wikibase-snakview-variation-valuesnak'}).getText()
    except AttributeError:
        continue
    strn = ''
    for b in speakerdiv:
        if b in '0123456789':
            strn += b
        elif b != ',':
            break
    c = ''
    for e in a:
        if ord(e) < 128:
            c += e
        else:
            c += '&#' + str(ord(e)) + ';'
    langfile.write(c + '\t' + strn + '\n')
langfile.close()
