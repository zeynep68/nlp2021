# No external (non-standard library) packages except numpy
import numpy as np

NUMBERS = [str(0), str(1), str(2), str(3), str(4), str(5), str(6), str(7), str(8), str(9)]

def split_by(tokens, t, c1, c2=None):
    a = t.split(c1)
    a.insert(-1, c1)

    if c2 is not None:
        a.insert(-1, c2)
        a[-1] = a[-1].replace("'", '')
    while '' in a:
        a.remove('')
    if 'http:' in t:
        del a[-1]

    tokens += a

    return tokens


def tokenize(s):
    tokens = []

    for t in s.split(' '):
        if "\n" in t:
            t = t.replace("\n", "")
        
        if '.' in t:
            if t.startswith('$'):
                tokens.append(t[0])
                t = t[1:]

            idx = t.index('.')
            if '[' in t:
                tokens = split_by(tokens, t, '[')
            
            elif (idx+1 < len(t)) and (t[idx+1] in NUMBERS):
                tokens.append(t[:-1])
                tokens.append('.')

            elif ".'" in t:
                tokens = split_by(tokens, t, '.', "'") 
                
            elif ')' in t:
                tokens = split_by(tokens, t, ')') 

            else:
                tokens = split_by(tokens, t, '.') 

        elif ',' in t:
            if (t.endswith(',')) and ('(' not in t):
                tokens = split_by(tokens, t, ',')

            elif '$' in t:
                tokens = split_by(tokens, t, '$')

            elif '(' in t:
                tokens = split_by(tokens, t, t[t.index('(')+1])
            else:
                tokens.append(t)

        elif ';' in t:
            tokens = split_by(tokens, t, ';') 

        elif '?' in t:
            tokens = split_by(tokens, t, '?') 

        elif "''" in t:
            tokens = split_by(tokens, t, "''") 

        elif '%' in t:
            tokens = split_by(tokens, t, '%') 

        elif '"' in t:
            tokens = split_by(tokens, t, '"') 

        elif '!' in t:
            tokens = split_by(tokens, t, '!') 

        elif ')' in t:
            tokens = split_by(tokens, t, ')') 

        elif '(' in t:
            tokens = split_by(tokens, t, '(') 

        elif '—' in t:
            tokens = split_by(tokens, t, '—') 

        else:
            tokens.append(t)

    return tokens
