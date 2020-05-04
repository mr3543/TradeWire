#topics 
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
import numpy as np
from gensim.corpora import Dictionary
from gensim.models import LdaMulticore
from scipy.special import kl_div
from scipy.stats import entropy
from scipy.spatial.distance import jensenshannon
from Reader import Reader
from Processor import Processor


def topic_to_arr(doc_topic,num_topics):
    arr = np.zeros(num_topics)
    for tup in doc_topic:
        arr[tup[0]] = tup[1]
    return arr

def arr_to_topics(article_arr):
    topics = []
    for i,top in enumerate(article_arr):
        if top > 0.03:
            topics.append((i,top))
    return topics
    
class Topics:
    def __init__(self,model,reader,processor,num_topics):
        self.model      = model
        self.reader     = reader
        self.com_list   = self.reader.com_list
        self.num_topics = num_topics
        self.processor  = processor
        self.cutoff     = 5
        self.epsilon    = 0.0001
    
    def score_docs(self):
        topic_mat = np.zeros([len(self.reader),self.num_topics])
        for i,doc in enumerate(self.reader):
            doc_topic = model[doc]
            topic_mat[i] = topic_to_arr(doc_topic,self.num_topics)
            
        self.topic_mat = topic_mat + self.epsilon
    
    def get_article_topics(self,text):
        article_topics = self._get_topics(text)
        article_arr  = topic_to_arr(article_topics,self.num_topics)
        arr_sorted   = np.argsort(-article_arr)
        to_discard   = arr_sorted[self.cutoff:]
        article_arr[to_discard] = self.epsilon
        article_arr /= np.sum(article_arr)
        return arr_to_topics(article_arr)
        
    def _get_topics(self,text):
        lemmas = self.processor.process(text)
        bow    = self.reader.dct.doc2bow(lemmas.split(' '))
        topics = self.model[bow]
        return topics
        
    def get_top_companies(self,article_text):
        article_topics = self._get_topics(article_text)
        article_arr    = topic_to_arr(article_topics,self.num_topics)
        to_discard     = np.argsort(-article_arr)[self.cutoff:]
        article_arr[to_discard] = self.epsilon
        #article_arr /= np.sum(article_arr)
        #article_arr    += 0.01
        
        distances = []
        for doc in self.topic_mat:
            doc_to_discard = np.argsort(-doc)[self.cutoff:]
            doc[doc_to_discard] = self.epsilon
            ent = jensenshannon(article_arr,doc)
            #ent = np.linalg.norm(article_arr-doc)
            distances.append(ent)
        distance_inds = np.argsort(distances)
        #print(distances)
        return [self.com_list[i] for i in distance_inds[:10]]
    

