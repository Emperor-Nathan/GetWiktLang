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
    ar = ''
    for b in a:
        if ord(b) > 127:
            ar += '&#' + str(ord(b)) + ';'
        else:
            ar += b
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
            ritari.writerow([ar, 'unclassified'])
            break
        if len(famlink) > 0:
            break
        n += 1
    if famlink == ' ':
        continue
    sname = famlink.getText()
    if sname == 'language isolate':
        ritari.writerow([ar, 'isolate'])
        continue
    if sname == 'constructed language':
        ritari.writerow([ar, 'constructed'])
        continue
    if sname == 'sign language':
        ritari.writerow([ar, 'sign language'])
        continue
    if sname == 'mixed language':
        ritari.writerow([ar, 'mixed'])
        continue
    snafn = ''
    for b in sname:
        if ord(b) > 127:
            snafn += '&#' + str(ord(b)) + ';'
        else:
            snafn += b
    f = False
    try:
        if len(subfamilies[snafn]) == 0:
            ritari.writerow[ar, snafn]
        else:
            g = subfamilies[snafn]
            ritari.writerow([ar, g])
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
    fi = ''
    for b in fam:
        if ord(b) > 127:
            fi += '&#' + str(ord(b)) + ';'
        else:
            fi += b
    if fam == snafn:
        subfamilies[fi] = ''
    else:
        subfamilies[snafn] = fi
    ritari.writerow([ar, fi])
langfile.close()
