from bs4 import BeautifulSoup
from requests import get
import csv

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

langfile = open('langfamilies.csv', 'w')
ritari = csv.writer(langfile, delimiter = ',')
ritari.writerow(['Language', 'Family'])
subfamilies = {'Kipchak-Bulgar': 'Turkic'}
m = 0
print('Total:', len(langlist))
for a in langlist:
    m += 1
    print(m)
    if len(a) == 0:
        continue
    ls = a
    if ls[(len(ls)-9):] != ' Language':
        ls += ' language'
    wtpage = BeautifulSoup(get('https://en.wiktionary.org/wiki/Category:'+ls).content, 'html.parser')
    n = 0
    try:
        t = wtpage.find_all('table')[2].find_all('tr')
    except IndexError:
        continue
    famlink = ''
    while True:
        fam1 = t[n]
        try:
            if fam1.find('th').find('a')['href'] == '/wiki/Wiktionary:Families':
                famlink = fam1.find_all('a')[1]
                break
        except TypeError:
            pass
        except IndexError:
            famlink = ' '
            ritari.writerow([a, 'unclassified'])
            break
        if len(famlink) > 0:
            break
        n += 1
    if famlink == ' ':
        continue
    sname = famlink.getText()
    if sname == 'language isolate':
        ritari.writerow([a, 'isolate'])
        continue
    if sname == 'constructed language':
        ritari.writerow([a, 'constructed'])
        continue
    if sname == 'sign language':
        ritari.writerow([a, 'sign language'])
        continue
    if sname == 'mixed language':
        ritari.writerow([a, 'mixed'])
        continue
    f = False
    try:
        if len(subfamilies[sname]) == 0:
            ritari.writerow[a, sname]
        else:
            g = subfamilies[sname]
            ritari.writerow([a, g])
        f = True
        continue
    except KeyError:
        pass
    except TypeError:
        pass
    if f:
        continue
    fampage = BeautifulSoup(get('https://en.wiktionary.org' + famlink['href']).content, 'html.parser')
    n = 0
    try:
        t = fampage.find_all('table')[1].find_all('tr')
    except IndexError:
        print(a)
        continue
    fam = ''
    while True:
        fam1 = t[n]
        try:
            x = fam1.find('th').find('a').getText()
            if x == 'Parent family' or x == 'Parent families':
                try:
                    fam = fam1.find('li').find('a').getText()
                except AttributeError:
                    fam = sname
                break
        except TypeError:
            pass
        except AttributeError:
            pass
        if len(fam) > 0:
            break
        n += 1
    if fam == sname:
        subfamilies[fam] = ''
    else:
        subfamilies[sname] = fam
    ritari.writerow([a, fam])
langfile.close()
