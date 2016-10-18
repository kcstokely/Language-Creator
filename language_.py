import random
import language_functions_ as lang

### create shells

current_rep = lang.Representation()
current_spc = lang.SoundSpace()
current_lex = lang.Lexicon(current_spc)

### Helps

def help_representation():
    print "    A REPRESENTATION is a map from the list of sounds to the list of characters."
    print "    "
    print "        So really, it is just a list of characters."
    print "    "
    print "        The canonical sounds are these 12 vowels and 21 consonants:"
    print "    "
    print "            a, a, a, e, e, e, o, o, o, u, u, u,"
    print "            p, t, k, b, d, g, f, th, s, sh, v, dh, z, zh,"
    print "            m, l, n, ng, r, w, y."
    print "    "
    print "        (The vowel sounds correspond to the English words: [TEXT MISSING])"
    print "    "
    print "        The default representation is as seen there, though the unicode is likely"
    print "        not showing up properly in your terminal."
    print "    "
    print "        If you would like to upload a representation, it should be an ascii file,"
    print "        with the latex code for the nth sound on the nth line,"
    print "        lower then uppercase, separated by whitespace."
    print "    "
    return None
    
def help_soundspace():
    print "    A SOUND-SPACE is essentially the list of rules from which words are created."
    print "    "
    print "        It consists of lists of frequencies of vowel or consonant sounds"
    print "        for the beginning, middle, and end of words, and..."
    print "    "
    print "        lists of frequencies for each sound for the beginning of a word,"
    print "        and of sound-sound pairs for the middle and end of words."
    print "    "
    print "        If you would like to upload a sound-space, it should be a text file"
    print "        with a specific format."
    print "    "
    return None
    
def help_lexicon():    
    print "    A LEXICON is a group of words generated from a sound-space."
    print "    "
    print "        There are several parts of speech: verbs and tenses,"
    print "        subject and object pronouns, nouns, logics, conjunctions, and etc."
    print "    "
    print "        If you would like to upload a lexicon, it should be a text file"
    print "        with a specific format."
    print "    "
    return None
    
def help_story():
    print "    A STORY is a bunch of semantically coherent sentences, randomly generated"
    print "    with words chosen from a given lexicon."
    print "    "
    return None

def help_ask():
    print "    Please choose your topic:"
    print "    "
    print "        1) Representations"
    print "        2) Sound-spaces"
    print "        3) Lexicons"
    print "        4) Stories"
    print "        5) Exit"
    print "    "
    print "    "
    return None

def help_choose():
    choice = raw_input("    Your command:  ")
    print "    "
    if choice is '1':
        help_representation()
        help_ask()
        help_choose()
    elif choice is '2':
        help_soundspace()
        help_ask()
        help_choose()
    elif choice is '3':
        help_lexicon()
        help_ask()
        help_choose()
    elif choice is '4':
        help_story()
        help_ask()
        help_choose()
    elif choice is '5':
        print "    "
        print "    "
        return None
    else:
        help_choose()

### menus

def fill():
    print "    Sorry, that is not implemented yet."
    return None

def ask():
    print "    "
    print "    "
    print "    What would you like to do..."
    print "    "
    print "        1) Import a Representation from a file"
    print "        2) Export a Representation to a file"
    print "        3) Mutate a Representation"
    print "    "
    print "        4) Create a Soundspace by uploading a list of words"
    print "        5) Create a Soundspace by typing a bunch of words"
    print "        6) Import a Soundspace from a file"
    print "        7) Export a Soundspace to a file"
    print "        8) Mutate a Soundspace"
    print "    "
    print "         9) Import a Lexicon from a file"
    print "        10) Export a Lexicon to a file"
    print "        11) Create a Lexicon"
    print "    "
    print "        12) Create a Random Story from a Lexicon"
    print "    "
    if random.choice([0,1]):
        print "        13) Browse a Semi-Help File"
    else:
        print "        13) Peruse a Semi-Help File"
    print "    "
    print "        14) Exit"
    print "    "
    print "    "
    return None
    
def choose():
    global current_rep, current_spc, current_lex
    choice = raw_input("    Your choice:  ")
    print "    "
    if choice == '1':
        fname = raw_input("Filename: ")
        current_rep.imp(fname)
        print "    "+fname+" imported!"
        ask()
        choose()
    elif choice == '2':
        fname = raw_input("Filename: ")
        current_rep.exp(fname)
        print "    "+fname+" exported!"
        ask()
        choose()
    elif choice == '3':
        fill()
        ask()
        choose()
    elif choice == '4':
        fill()
        ask()
        choose()
    elif choice == '5':
        fname = raw_input("Filename: ")
        current_spc.scanin(fname)
        print "    "+fname+" scanned!"
        ask()
        choose()
    elif choice == '6':
        fname = raw_input("Filename: ")
        current_spc.imp(fname)
        print "    "+fname+" imported!"
        ask()
        choose()
    elif choice == '7':
        fname = raw_input("Filename: ")
        current_spc.exp(fname)
        print "    "+fname+" exported!"
        ask()
        choose()
    elif choice == '8':
        fill()
        ask()
        choose()
    elif choice == '9':
        fname = raw_input("Filename: ")
        current_lex.imp(fname)
        print "    "+fname+" imported!"
        ask()
        choose()
    elif choice == '10':
        fname = raw_input("Filename: ")
        current_lex.exp(fname)
        print "    "+fname+" exported!"
        ask()
        choose()
    elif choice == '11':
        current_lex = Lexicon(current_spc)
        print "    Lexicon created!"
        ask()
        choose()
    elif choice == '12':
        lang.create_story(current_lex, current_rep)
        print "    story_.pdf created!"
        ask()
        choose()
    elif choice == '13':
        print "    This is SEMI-HELPFUL."
        print "    "
        help_ask()
        help_choose()
        print "    "
        print "    "
        ask()
        choose()
    elif choice == '14':
        print "    Good-bye!"
        print "    "
        print "    "
        exit()
    else:
        choose()

### actual call
        
print "    "
print "    "
print "    Welcome to Interactive Language Generator!"
ask()
choose()

### things:

    # yo make sure one word words are vowels
    # conjugation
    # hyp pairs
    # memory
    # translation instead of conjuration
    
    
    
    
    
    
    
    
    

