import numpy as np

from tokenization import tokenize
from utils import everygram, out_of_order_measure, save_profile, valid_token

PATH = 'datasets/language_detection/'

TRAINING = ['training_english.utf8', 'training_german.utf8', 
            'training_norwegian.utf8', 'training_russian.utf8', 
            'training_turkish.utf8', 'training_ukrainian.utf8']

TEST = ['document1.utf8', 'document2.utf8', 'document3.utf8',
        'document4.utf8', 'document5.utf8', 'document6.utf8']

class LanguageDetection:
    def __init__(self, pad_symbol=' ', top_n=300):
        self.pad_symbol = pad_symbol
        self.top_n = top_n 

    def generate_profile(self, filename):
        # split the text into separate tokens (see tokenize for more details)
        # scan down each token, generating all possible N-grams, for N=1 to 5
        tokens = tokenize(open(PATH+filename, 'r').read())

        done = []
    
        for token in tokens:
            token = token.lower()
            
            if valid_token(token):
                done += everygram(token, 1, 5, " ")

        # count occurence 
        items, counts = np.unique(np.array(done), return_counts=True)

        # hash table with N-gram as keys and their counter as values
        all_ngrams = dict(zip(items, counts))        
        all_ngrams = sorted(all_ngrams, key=all_ngrams.get, reverse=True)

        # save file
        save_profile(filename.replace('.', '_profile.'), all_ngrams[:self.top_n])

        return

    def measure_profile_distance(self, language_profile, document_profile):
        return out_of_order_measure(language_profile, document_profile)

    def find_minimum_distance(self, dist):
        return np.argmin(dist)
    
    def generate_language_profiles(self):
        for f in TRAINING:
            self.generate_profile(f)
        return

    def detect_language(self, document_profile='document6.txt'):
        dist = []
        doc = open(document_profile.replace('.', 'profile.'), 'r').readlines()

        for f in self.training:
            error = self.measure_profile_distance(open(f.replace('.', 'profile.'), 'r').readlines(), doc)
            dist.append(error)

        return self.find_minimum_distance(dist)
