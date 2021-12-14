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
    

    def detect_language(self, document_profile='document6.txt'):
        dist = []
        doc = open(document_profile.replace('.', '_profile.'), 'r').readlines()

        for f in TRAINING:
            error = self.measure_profile_distance(open(f.replace('.', '_profile.'), 'r').readlines(), doc)
            dist.append(error)

        return self.find_minimum_distance(dist)


def generate_language_profiles(detector, training=True):
    if training:
        dataset = TRAINING
    else:
        dataset = TEST

    for data in dataset:
        detector.generate_profile(data)
    return


def main(detector):
    languages = ['english', 'german', 'norwegian', 'russian', 'turkish', 'ukrainian']

    document_languages = {} #filename as keys, language as values

    for doc in TEST:
        document_languages[doc] = languages[detector.detect_language(doc)]

    with open('./document_languages.csv', 'w') as fp:
        fp.writelines([f'{document},{lang}\n' for document,lang in document_languages.items()])

if __name__ == "__main__":
    # create detector object
    detector = LanguageDetection()

    # generate profiles for training and testing data
    generate_language_profiles(detector)
    generate_language_profiles(detector, training=False)
    
    # evaluate on test data
    main(detector)
    
