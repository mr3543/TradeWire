import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
import numpy as np
from gensim.corpora import Dictionary


class Processor:
    def __init__(self):
        # placeholder for now, if we want to use spacy preprocessing
        # we will store spacy nlp obj here
        pass
    
    def process(self,rawtext:str):
        """
        Parameters
        ------------

        converts string of raw text to string of lemmas separated by
        single whitespace

        rawtext: str, text to be processed
        """

        tokenizer = RegexpTokenizer(r'\w+')
        rawtext   = rawtext.lower()
        rawtext   = tokenizer.tokenize(rawtext)
        lemmas    = []

        for token in rawtext:
            if any(char.isdigit() for char in token) or \
               len(token) <= 1: continue
            lemmas.append(token)

        lemmatizer = WordNetLemmatizer()
        lemmas = [lemmatizer.lemmatize(token) for token in lemmas]
        output = ' '.join(lemmas)

        return output

