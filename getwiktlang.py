from bs4 import BeautifulSoup
from requests import get
from tkinter import *
import math, sys, csv#, langmap

size = [0, 0]
sizefile = open('size.csv', 'r')
rdr = csv.reader(sizefile, delimiter = ',')
for row in rdr:
    if row[0].lower() == 'width':
        size[0] = int(row[1])
    elif row[0].lower() == 'height':
        size[1] = int(row[1])
sizefile.close()
if size[0] < 350:
    print('Error: width must be at least 350.')
if size[1] < 40:
    print('Error: height must be at least 40.')
tnum = int((size[1] - 30) / 15)

lemmas = {}

webpage = BeautifulSoup(get('https://en.wiktionary.org/wiki/Category:Lemmas_by_language').content, 'html.parser')
done = False
while not done:
    for div in webpage.find_all('div', {'id':'catlinks'}):
        div.decompose()
    for div in webpage.find_all('div', {'id':'mw-navigation'}):
        div.decompose()
    for div in webpage.find_all('div', {'id':'footer'}):
        div.decompose()
    done = True
    for a in webpage.find_all('a'):
        if 'next page' in a.getText():
            done = False
            new_url = 'https://en.wiktionary.org' + a['href']
    l3 = webpage.find_all('ul')
    l2 = []
    for a in l3:
        for b in a.find_all('li'):
            l2.append(b)
    if l2[0] == 'Lemmas subcategories by language':
        del l2[0]
    l = []
    lx = []
    for a in l2:
        try:
            if 'footer' in a['id']:
                continue
        except KeyError:
            z = 0
        try:
            q = a.find_all('span')
            p = a.find('a').getText()
            s = ''
            n = 0
            while n < len(p) - 7: #Change for different categories
                s += p[n]
                n += 1
            l.append(s)
            r = q[len(q)-1].getText()
            x = ''
            y = 0
            while r[y] != ',':
                y += 1
            y += 2
            while r[y] != ' ':
                x += r[y]
                y += 1
            lx.append(int(x))
        except AttributeError:
            z = 0
        except IndexError:
            break
    n = 0
    while n < len(l):
        try:
            lemmas[l[n]] = lx[n]
        except IndexError:
            z = 0
        n += 1
    if not done:
        webpage = BeautifulSoup(get(new_url).content, 'html.parser')

tk = Tk()
c = Canvas(tk, width = size[0], height = size[1])
c.pack()


min_words = 1 #Change this
max_words = 1e6 #Change this
sl = [['',max_words+1]]

for a in lemmas:
    if lemmas[a] >= min_words and lemmas[a] <= max_words:
        sl.append([a, lemmas[a]])

n = len(sl)
while n >= 1:
    newn = 0
    i = 1
    while i < n:
        if sl[i-1][1] < sl[i][1]:
            temp = sl[i-1]
            sl[i-1] = sl[i]
            sl[i] = temp
            newn = i
        i += 1
    n = newn

pnu = 1
while sl[pnu][0] != 'English':
    pnu += 1
proportion = sl[1][1]/(size[0] - 300)

nativespeakers = {}

nativefile = open('nativespeakers.csv', 'r')
nsreader = csv.reader(nativefile, delimiter = ',')
for a in nsreader:
    if a[0].lower() == 'language':
        continue
    s = ''
    r = ''
    mode = 1
    for b in a[0]:
        if b == '&':
            mode = 2
        elif b == '#' and mode == 2:
            r = ''
        elif b == ';' and mode == 2:
            s += chr(int(r))
            mode = 1
        elif mode == 2:
            r += b
        else:
            s += b
    nativespeakers[s] = int(a[1])
nativefile.close()

def drawWindow(tk, c, j):
    oj = j
    c.create_line(40, 0, 40, (tnum + 1)*15)
    for a in sl:
        if a[1] >= min_words and a[1] <= max_words and j < len(sl):
            c.create_text(40, (j+.25)*15, anchor='e', text = str(j) + ' ')
            c.create_rectangle(40, j * 15, 40 + a[1]/proportion, (j+.25)*15, fill='black')
            if a[0] in nativespeakers:
                c.create_rectangle(40, (j+.25)*15, 40 + (nativespeakers[a[0]] * sl[pnu][1] / nativespeakers['English'])/proportion, (j+.5)*15, fill = 'orange', outline = 'orange')
            c.create_text(40 + a[1]/proportion, (j+.25)*15, text = ' '+a[0], anchor = W)
            j += 1
        if j < len(sl) - 1 and sl[j][1] == sl[j+1][1] and j < tnum: # Language below has same number
            c.create_rectangle(40, (j+.5)*15, 40 + sl[j][1]/proportion, (j+1) * 15, fill='black')
        if j > tnum:
            break
    #lines
    z = 10**math.floor(math.log10(sl[1][1]))
    z1 = z
    while z <= sl[1][1]:
        c.create_line(40+z/proportion, 0, 40+z/proportion, (tnum + 1)*15)
        c.create_text(40+z/proportion, (tnum + 1)*15, anchor='n', text=str(int(z/z1))+'e'+str(int(math.log10(z))))
        z += z1
    tk.update()
    return oj

j = drawWindow(tk, c, 1)

def sort(a):
    n = len(a)
    while n > 1:
        newn = 0
        i = 1
        while i < n:
            if a[i-1][1] < a[i][1]:
                temp = a[i-1]
                a[i-1] = a[i]
                a[i] = temp
                newn = i
            i += 1
        n = newn
    return a

def sortDiff():
    diff = []
    for a in sl:
        if a[0] in nativespeakers:
            diff.append([a[0], a[1] - (nativespeakers[a[0]] * sl[pnu][1] / nativespeakers['English'])])
    for a in sort(diff):
        print(a[0], a[1], sep='\t')

def createList():
    allfile = open('all.txt', 'w')
    for a in sl:
        c = ''
        for e in a[0]:
            if ord(e) < 128:
                c += e
            else:
                c += '&#' + str(ord(e)) + ';'
        allfile.write(c + '\n')
    allfile.close()

def scrollUp(event):
    global j
    c.delete('all')
    if j > 1:
        j -= 1
    jtemp = j
    m = tnum + j
    proportion = sl[j][1]/(size[0] - 300)
    while jtemp < m:
        if sl[jtemp][1] >= min_words and sl[jtemp][1] <= max_words and jtemp < len(sl):
            c.create_text(40, (jtemp-j+1.25)*15, anchor='e', text = str(jtemp) + ' ')
            c.create_rectangle(40, (jtemp-j+1) * 15, 40 + sl[jtemp][1]/proportion, (jtemp-j+1.25)*15, fill='black')
            if sl[jtemp][0] in nativespeakers:
                c.create_rectangle(40, (jtemp-j+1.25)*15, 40 + (nativespeakers[sl[jtemp][0]] * sl[pnu][1] / nativespeakers['English'])/proportion, (jtemp-j+1.5)*15, fill = 'orange', outline = 'orange')
            c.create_text(40 + sl[jtemp][1]/proportion, (jtemp-j+1.25)*15, text = ' '+sl[jtemp][0], anchor = W)
        if jtemp < len(sl) - 1 and sl[jtemp][1] == sl[jtemp+1][1] and jtemp < m - 1:
            c.create_rectangle(40, (jtemp-j+1.5)*15, 40 + sl[jtemp][1]/proportion, (jtemp-j+2) * 15, fill='black')
        jtemp += 1
    j = m - tnum
    z = 10**math.floor(math.log10(sl[j][1]))
    z1 = z
    c.create_line(40, 0, 40, (tnum + 1)*15)
    while z <= sl[j][1]:
        c.create_line(40+z/proportion, 0, 40+z/proportion, (tnum + 1)*15)
        c.create_text(40+z/proportion, (tnum + 1)*15, anchor='n', text=str(int(z/z1))+'e'+str(int(math.log10(z))))
        z += z1
    tk.update()

def scrollDown(event):
    global j
    c.delete('all')
    if j < len(sl) - tnum:
        j += 1
    jtemp = j
    m = tnum + j
    proportion = sl[j][1]/(size[0] - 300)
    while jtemp < m:
        if sl[jtemp][1] >= min_words and sl[jtemp][1] <= max_words and jtemp < len(sl):
            c.create_text(40, (jtemp-j+1.25)*15, anchor='e', text = str(jtemp) + ' ')
            c.create_rectangle(40, (jtemp-j+1) * 15, 40 + sl[jtemp][1]/proportion, (jtemp-j+1.25)*15, fill='black')
            if sl[jtemp][0] in nativespeakers:
                c.create_rectangle(40, (jtemp-j+1.25)*15, 40 + (nativespeakers[sl[jtemp][0]] * sl[pnu][1] / nativespeakers['English'])/proportion, (jtemp-j+1.5)*15, fill = 'orange', outline = 'orange')
            c.create_text(40 + sl[jtemp][1]/proportion, (jtemp-j+1.25)*15, text = ' '+sl[jtemp][0], anchor = W)
        if jtemp < len(sl) - 1 and sl[jtemp][1] == sl[jtemp+1][1] and jtemp < m - 1:
            c.create_rectangle(40, (jtemp-j+1.5)*15, 40 + sl[jtemp][1]/proportion, (jtemp-j+2) * 15, fill='black')
        jtemp += 1
    j = m - tnum
    z = 10**math.floor(math.log10(sl[j][1]))
    z1 = z
    c.create_line(40, 0, 40, (tnum + 1)*15)
    while z <= sl[j][1]:
        c.create_line(40+z/proportion, 0, 40+z/proportion, (tnum + 1)*15)
        c.create_text(40+z/proportion, (tnum + 1)*15, anchor='n', text=str(int(z/z1))+'e'+str(int(math.log10(z))))
        z += z1
    tk.update()

"""
def scrollDown(event):
    global j
    c.delete('all')
    if j < len(sl) - tnum:
        j = drawWindow(tk, c, j + 1)
"""

c.bind_all('<KeyPress-Down>',scrollDown)
c.bind_all('<KeyPress-Up>',scrollUp)

try:
    if sys.argv[1] == 'diff':
        sortDiff()
except IndexError:
    zz = 0

def quickList():
    ql = []
    ql_file = open('quicklist.txt')
    lines = ql_file.readlines()
    for a in lines:
        mode = 1
        la = ''
        rr = ''
        for t in a:
            if t == '&':
                mode = 2
            else:
                if mode == 1:
                    if t != '\n':
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
        ql.append(la)
    ql_file.close()
    fl = []
    for a in ql:
        if len(a) == 0:
            continue
        n = 0
        while n < len(sl):
            if sl[n][0] == a:
                break
            n += 1
        try:
            b = sl[n]
        except IndexError:
            print('ERROR', a)
            continue
        s = b[0]
        while len(s) < 17:
            s += ' '
        try:
            fl.append([s, int(b[1] - (nativespeakers[b[0]] * sl[pnu][1] /
                                         nativespeakers['English']))])
        except KeyError:
            continue
    n = 0
    ml = 0
    while n < len(fl):
        t = str(fl[n][1])
        if fl[n][1] > 0:
            t = '+' + t
        if ml < len(t):
            ml = len(t)
        fl[n].append(t)
        n += 1
    for a in sort(fl):
        u = a[2]
        while len(u) < ml:
            u = ' ' + u
        print(a[0], u, sep='\t')

def byFamily():
    lbf = {}
    familyfile = open('langfamilies.csv', 'r')
    nsreader = csv.reader(familyfile, delimiter = ',')
    for a in nsreader:
        if a[0].lower() == 'language':
            continue
        s = ''
        r = ''
        mode = 1
        for b in a[0]:
            if b == '&':
                mode = 2
            elif b == '#' and mode == 2:
                r = ''
            elif b == ';' and mode == 2:
                s += chr(int(r))
                mode = 1
            elif mode == 2:
                r += b
            else:
                s += b
        s2 = ''
        r = ''
        for b in a[1]:
            if b == '&':
                mode = 2
            elif b == '#' and mode == 2:
                r = ''
            elif b == ';' and mode == 2:
                s2 += chr(int(r))
                mode = 1
            elif mode == 2:
                r += b
            else:
                s2 += b
        mode = 1
        lbf[s] = s2
    familyfile.close()
    families = {}
    for a in sl:
        if len(a[0]) == 0:
            continue
        try:
            families[lbf[a[0]]] += int(a[1] - (nativespeakers[a[0]] * sl[pnu][1] /
                                         nativespeakers['English']))
        except KeyError:
            try:
                families[lbf[a[0]]] = int(a[1] - (nativespeakers[a[0]] * sl[pnu][1] /
                                         nativespeakers['English']))
            except KeyError:
                pass
    flist = []
    for a in families:
        flist.append([a, families[a]])
    for a in sort(flist):
        s = a[0]
        while len(s) < 17:
            s += ' '
        print(s, a[1], sep = '\t')

def createMap(overlay):
    if overlay:
        tc = langmap.map_main_overlay()
    else:
        tc = langmap.map_main()
    for a in sl:
        try:
            if a[1] < (nativespeakers[a[0]] * sl[pnu][1] / nativespeakers['English']):
                langmap.changeColor(langmap.nameRecog[a[0]], 'red', tc[1])
            else:
                langmap.changeColor(langmap.nameRecog[a[0]], 'black', tc[1])
        except IndexError:
            #print('Index', a)
            continue
        except KeyError:
            #print('Key', a)
            continue
    tc[0].update()
