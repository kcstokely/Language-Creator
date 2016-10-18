# -*- coding: latin-1 -*-

### imports

import numpy
import random

import os
from subprocess import call

### helpers

def flatten(k):
    return [i for j in k for i in j]

def pick_from_weights(input_list):
    return (random.choice([i for i in range(len(input_list)) for j in range(input_list[i])]))

def string_form(word, rep, cap):
    if not cap:
        k = rep.tex[word[0]]
    else:
        k = rep.TEX[word[0]]
    if len(word) > 1: 
        k = k+("".join([rep.tex[i] for i in word[1:]]))
    return k

### classes (though lists pretty much would have been fine)

class Representation:
    def __init__(self):
        self.num = 33
        self.uni = ['a',u'ä',u'á','e',u'ë',u'é','o',u'ö',u'ó','u',u'ü',u'ú',
                'p','t','k','b','d','g',
                'f','th','sh','s','v','dh','zh','z',
                'm','l','n','ng','r','w','y']
        self.tex = ['a','\\"{a}',"\\'{a}",'e','\\"{e}',"\\'{e}",'o','\\"{o}',"\\'{o}",'u','\\"{u}',"\\'{u}",
                'p','t','k','b','d','g',
                'f','th','sh','s','v','dh','zh','z',
                'm','l','n','ng','r','w','y']
        self.TEX = ['A','\\"{A}',"\\'{A}",'E','\\"{E}',"\\'{E}",'O','\\"{O}',"\\'{O}",'U','\\"{U}',"\\'{U}",
                'P','T','K','B','D','G',
                'F','Th','Sh','S','V','Dh','Zh','Z',
                'M','L','N','Ng','R','W','Y']
    def imp(self, filename):
        with open(filename, "r") as fp:
            self.num = 0
            for line in fp.readlines():
                self.tex[i] = line.split()[0]
                self.TEX[i] = line.split()[1]
                self.num += 1
    def exp(self, filename):
        with open(filename, "w") as fp:
            for i in range(self.num):
                fp.write(self.tex[i]+" "+self.TEX[i]+"\n")
    
class SoundSpace:
    def __init__(self):
        x = [5, 0, 0] * 4
        x.extend([1] * 21)
        nx = numpy.array(x, dtype=int)
        ny = numpy.zeros((33,33), dtype=int)
        for i in range(33):
            for j in range(33):
                if i == j:
                    ny[i][j] = 0
                else:
                    ny[i][j] = nx[i] * nx[j]
        self.numv = 12
        self.numn = 33
        self.voca = [1, 1]
        self.vocb = [[1, 1], [1,1]]
        self.vocc = [[1, 1], [1,1]]
        self.a    = nx
        self.b    = ny
        self.c    = ny
    def imp(self, filename):
        with open(filename, "r") as fp:
            line = fp.readline().split()
            self.numv = int(line[0])
            self.numn = int(line[1])
            line = fp.readline().split()
            self.voca = [int(i) for i in line]
            line = fp.readline.split()
            self.vocb[0] = [int(i) for i in line[:2]]
            self.vocb[1] = [int(i) for i in line[2:]]
            line = fp.readline().split()
            self.vocc[0] = [int(i) for i in line[:2]]
            self.vocc[1] = [int(i) for i in line[2:]]
            line = fp.readline().split()
            self.a = [int(i) for i in line]
            for i in range(self.numn):
                line = fp.readline().split()
                self.b[i] = [int(i) for i in line]
            for i in range(self.numn):
                line = fp.readline().split()
                self.c[i] = [int(i) for i in line]
    def exp(self, filename):
        with open(filename, "w") as fp:
            csv.writer(fp).writerow([self.numv, self.numn])
            csv.writer(fp).writerow(self.voca)
            csv.writer(fp).writerow(self.voca)
            csv.writer(fp).writerow(self.voca)
            csv.writer(fp).writerows(self.a)
            for i in range(self.numn):
                csv.writer(fp).writerow(self.vocb[i])
            for i in range(self.numn):
                csv.writer(fp).writerow(self.vocc[i])
    def scan(self, filename):
        with open(filename) as fp:
            for line in fp.readlines():
                chars = list(line)
                sndspc.a[chars[0]] += 1
                for i in range(1,len(chars)-1):
                    sndspc.b[chars[i-1]][chars[i]] += 1
                sndspc.c[chars[len(chars)-2]][chars[len(chars)-1]] += 1

class Lexicon:
    types = ['sbj','obj']
    def gen_word(self, soundspace, length):
        vvv = soundspace.numv
        # step 1: generate pattern in v=0, c=1
        pattern = [pick_from_weights(soundspace.voca)]
        pattern.extend([pick_from_weights(soundspace.vocb[pattern[0]])])
        for i in range(2,length-1):
            if pattern[i-1]==pattern[i-2]:
                if pattern[i-1]==0:
                    pattern.extend([1])
                else:
                    pattern.extend([0])
            else:
                pattern.extend([pick_from_weights(soundspace.vocb[pattern[i-1]])])
        if pattern[length-2]==pattern[length-3]:
            if pattern[length-2]==0:
                pattern.extend([1])
            else:
                pattern.extend([0])
        else:
            pattern.extend([pick_from_weights(soundspace.vocc[pattern[length-2]])])    
        # step 2: fill in first sound
        if not pattern[0]:
            word = [pick_from_weights(soundspace.a[:vvv])]
        else:
            word = [vvv + pick_from_weights(soundspace.a[vvv:])]
        # step 3: fill in middle sounds
        for i in range(1,length-1):
            if not pattern[i]:
                word.extend([pick_from_weights(soundspace.b[word[i-1]][:vvv])])
            else:
                word.extend([vvv + pick_from_weights(soundspace.b[word[i-1]][vvv:])])
        # step 4: fill in final sound
        if not pattern[length-1]:
            word.extend([pick_from_weights(soundspace.c[word[length-2]][:vvv])])
        else:
            word.extend([vvv + pick_from_weights(soundspace.c[word[length-2]][vvv:])])
        #step 5: return
        return word    
    def gen_words(self, len_min, len_med, len_std, soundspace, number):
        words = []
        for w in range(number):
            length = int(max(len_min,numpy.random.normal(len_med,len_std)))
            words.extend([self.gen_word(soundspace,length)])
        return words
    def __init__(self, soundspace):
        self.sbj = self.gen_words(1, 2, 1, soundspace, 6)
        self.obj = self.gen_words(2, 3, 1, soundspace, 6)
        self.log = self.gen_words(1, 2, 1, soundspace, 4)
        self.rel = self.gen_words(2, 2, 1, soundspace, 6)
        self.hyp = self.gen_words(2, 3, 2, soundspace, 6)
        self.adj = self.gen_words(2, 3, 3, soundspace, 72)
        self.adv = self.gen_words(2, 3, 2, soundspace, 36)
        self.vrb = self.gen_words(2, 3, 2, soundspace, 18)
        self.tns = self.gen_words(1, 2, 1, soundspace, 6)
    def imp(self, fname):
        pass
    def exp(self, fname):
        pass
        
### page creation
###     (uses types: sbj, obj, vrb, tns, hyp)
###     (fix to also use: log, etc.)

def generate_sentence(lex):
    s = []
    def generate_clause():
        s.append(random.choice(lex.sbj))
        s.append(flatten([random.choice(lex.vrb),random.choice(lex.tns)]))
        if not random.randint(0,6):
            s.append(random.choice(lex.obj))
        return None
    h = random.randint(0,3)
    if not h:
        s.append(random.choice(lex.hyp))
    generate_clause()
    if not h:
        s.append(random.choice(lex.hyp))
        generate_clause()
    return s

def conjure_page(lex, rep):
    infile = open("story_.tex","w+")
    # print head
    infile.write("\\documentclass[11pt]{article}\n")
    infile.write("\\usepackage{geometry}\n")
    infile.write("\\usepackage{lmodern}\n")
    infile.write("\\usepackage[T1]{fontenc}\n")
    infile.write("\\usepackage[utf8]{inputenc}\n")
    infile.write("\\setlength{\parskip}{11pt}\n")
    infile.write("\\begin{document}\n")
    # print body
    num_t = random.randint(2,5)
    for t in range(num_t):
        for p in range(random.randint(3,7)):
            for s in range(random.randint(4,9)):
                g = generate_sentence(lex)
                h = string_form(g[0], rep, True)+" "
                h = h+" ".join([string_form(x, rep, False) for x in g[1:]])
                h = h+".  "
                infile.write(h)
            infile.write("\n")
        if t != num_t-1:
            infile.write("\n\\noindent\\hfil\\rule{0.5\\textwidth}{.4pt}\\hfil\n\n")
    # print tail
    infile.write("\\end{document}\n")
    infile.close()
    return None

def create_story(lex, rep):
    conjure_page(lex, rep)
    fnull = open(os.devnull,'w')
    call(["pdflatex","story_.tex"], stdout=fnull)
    call(["pdflatex","story_.tex"], stdout=fnull)
    return None

    
    
    
    
    
    
        
        
        
        
        
        
        
        
        
        
        
        