chars = [', ', '$', '?', '(', ')', '"', '—', '!', ';', "''", '%', ".'"]


def tokenize(s):
    tokens = []

    for c in chars:
        s = s.replace(c, ' ' + c + ' ')

    # special cases
    for t in s.split(): 
        if '[http' in t:
            tokens.append(t[0])
        elif t == ".'":
            tokens.append(t[0])
            tokens.append(t[1])
        elif t.endswith('.'):
            tokens.append(t[:-1])
            tokens.append(t[-1])
        else:
            tokens.append(t)
   
    return [t for t in tokens if t != '']
