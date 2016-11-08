# -*- coding: latin-1 -*-

### imports ###############################################################################################################################

import numpy
import random

import os
from subprocess import call

### helpers ###############################################################################################################################

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

### classes ###############################################################################################################################

class Representation:
    def __init__(self):
        self.name = 'Default'
        self.num = 0
        self.asc = []
        self.uni = []
        self.tex = []
        self.TEX = []
        self.imp("representation_.dat")
    def imp(self, filename):
        with open(filename, "r") as fp:
            self.num = 0
            for line in fp.readlines():
                tokes = line.split()
                self.asc.append(tokes[0])
                self.uni.append(tokes[1])
                self.tex.append(tokes[2])
                self.TEX.append(tokes[3])
                self.num += 1
    def exp(self, filename):
        with open(filename, "w") as fp:
            for i in range(self.num):
                fp.write(self.asc[i]+" "+self.uni[i]+" "+self.tex[i]+" "+self.TEX[i]+"\n")



'''
    self.fa: allowed transitions on the rising part of a syllable
                (here rising also includes the vowel sounds)
    
            - self.fa[c][v] = 1
            - self.fa[v][v] = 0, unless specified as allowed in transitions_.dat
            - self.fa[v][c] = 1
            - self.fa[c][c] = as specified in transitions_.dat
    
    self.fb: allowed transitions on the falling part of a syllable
    
            - self.fb[v][v] = 0
            - self.fb[v][c] = 1
            - self.fb[c][v] = 0
            - self.fb[c][c] = as specified in transitions_.dat
'''                
             
class SoundSpace:
    def __init__(self):
        self.name = 'Default'
        self.numv = 11
        self.numc = 22
        self.numn = self.numv + self.numc
        self.voca = [1,1]
        self.vocb = [1,1]
        self.x = [3] * self.numv
        self.x.extend([1] * self.numc)
        self.fa = numpy.zeros((self.numn,self.numn), dtype=int)
        self.fb = numpy.zeros((self.numn,self.numn), dtype=int)
        for c in range(self.numv,self.numn):
            for v in range(self.numv):
                self.fa[c][v] = 1
                self.fa[v][c] = 1
                self.fb[c][v] = 1
        with open("transitions_.dat","r") as fp:
            numd = 0
            read = 0
            for line in fp:
                line = line.strip().split()
                if line and '#' not in line[0]:
                    if read == 0:
                        numd = int(line[0])
                        read += 1
                    elif read <= numd:
                        self.fa[int(line[1])][int(line[2])] = int(line[3])
                        self.fb[int(line[1])][int(line[2])] = int(line[4])
                        read += 1
                    else:
                        self.fa[self.numv+int(line[1])][self.numv+int(line[2])] = int(line[3])
                        self.fb[self.numv+int(line[1])][self.numv+int(line[2])] = int(line[4])
                        read += 1
    def imp(self, filename):
        with open(filename, "r") as fp:
            line = fp.readline().split()
            self.numv = int(line[0])
            self.numc = int(line[1])
            self.numn = int(line[2])
            for i in range(self.numn):
                line = fp.readline().split()
                self.x[i] = int(i)
    def exp(self, filename):
        with open(filename, "w") as fp:
            csv.writer(fp).writerow([self.numv, self.numc, self.numn])
            for i in range(self.numn):
                csv.writer(fp).writerow(self.x[i])
    def scan(self, filename):
        with open(filename) as fp:
            for line in fp.readlines():
                pass

class Lexicon:
    types = []
    def gen_word(self, soundspace, length):
        ### constants
        numv = soundspace.numv
        numc = soundspace.numc
        numn = soundspace.numn
        ### variables
        syl_num = 0
        syl_rising = True
        ### get started
        word = []
        if pick_from_weights(soundspace.voca):
            sound = pick_from_weights(soundspace.x[:numv])
        else:
            sound = numv + pick_from_weights(soundspace.x[numv:])
        word.append(sound)
        ### loop
        while syl_num < length:
            # rising
            if syl_rising:
                filter = soundspace.fa[word[-1]]
                flist = [filter[i]*soundspace.x[i] for i in range(numn)]
                sound = pick_from_weights(flist)
                if sound < numv:
                    syl_rising = False
            # falling
            else:
                filter = [0]*numv
                filter.extend([1]*numc)
                flist = [filter[i]*soundspace.x[i] for i in range(numn)]
                sound = pick_from_weights(flist)
                check = soundspace.fb[word[-1]]
                if check[sound] == 0:                    
                        syl_num += 1
                        syl_rising = True
            word.append(sound)
        ### possible trim
        if(pick_from_weights(soundspace.vocb)):
            while word[-1] > numv:
                del word[-1]
        ### return 
        print syl_num
        return word
    def gen_words(self, len_min, len_med, len_std, soundspace, number):
        words = []
        for w in range(number):
            length = int(max(len_min,numpy.random.normal(len_med,len_std)))
            words.append(self.gen_word(soundspace,length))
        return words    
    def __init__(self, soundspace):
        self.name = 'Default'
        # word types
        self.sbj = self.gen_words(1, 1.5, 1, soundspace, 6)
        self.obj = self.gen_words(2, 2.5, 1, soundspace, 6)
        self.log = self.gen_words(1, 1.5, 1, soundspace, 4)
        self.rel = self.gen_words(2, 2, 1, soundspace, 6)
        self.hyp = self.gen_words(2, 2.5, 1.5, soundspace, 6)
        self.adj = self.gen_words(2, 2.5, 2, soundspace, 72)
        self.adv = self.gen_words(2, 2.5, 1.5, soundspace, 36)
        self.vrb = self.gen_words(2, 2.5, 1, soundspace, 18)
        self.tns = self.gen_words(1, 1.5, 1, soundspace, 6)
    def imp(self, fname):
        pass
    def exp(self, fname):
        pass
        
### page creation #########################################################################################################################
### uses types: sbj, obj, vrb, tns, hyp --- fix to also use: log, etc.

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

def create_story(lex, rep):
    conjure_page(lex, rep)
    fnull = open(os.devnull,'w')
    call(["pdflatex","story_.tex"], stdout=fnull)
    call(["pdflatex","story_.tex"], stdout=fnull)

###########################################################################################################################################
    
    
    
    
    
        
        
        
        
        
        
        
        
        
        
        
