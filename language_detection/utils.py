import numpy as np


def add_padding(s, n, pad_symbol):
    return pad_symbol * (n-1) + s + pad_symbol * (n-1)


def ngram(sequence, n=3, pad_symbol=None, everygram=False, max_n=3):
    if pad_symbol == None:
        pad_symbol = ""

    if everygram:
        padded_sequence = add_padding(sequence, max_n, pad_symbol)
    else:
        padded_sequence = add_padding(sequence, n, pad_symbol)
    
    count = 0
    ngrams = []

    while count < len(padded_sequence)-(n-1):
        ngrams.append(padded_sequence[count:count+n])
        count += 1
   
    return ngrams


def everygram(sequence, min_n, max_n, pad_symbol=None):
    everygrams = []

    for i in range(min_n, max_n+1):
        everygrams += ngram(sequence=sequence, n=i, pad_symbol=pad_symbol, everygram=True, max_n=max_n)

    return everygrams


def out_of_order_measure(language_profile, document_profile):
    error = 0

    for count, item in enumerate(document_profile):
        if item in language_profile:
            error += np.abs(language_profile.index(item) - count)
        else: # maximum distance if item not in language profile
            error += len(document_profile) - 1

    return error


def save_profile(filename, items):
    textfile = open(filename, "w")
    textfile.writelines(["%s\n" % item  for item in items])
    textfile.close()


def valid_token(m):
    if (m.count("'") <= 1):
        if m.count("'") == 1:
            m =m.replace("'", "")
        if m.count("-") >= 0: 
            m = m.replace("-", "")
        if m.isalpha():
            return True
    return False

