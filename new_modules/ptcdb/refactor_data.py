import random
import time
import numpy as np
from read_pickle import data_reader

class data_refactorizer:
    def __init__(self, filelist):
        picks = data_reader(filelist).get_picks()
        self.cite_graph = picks[0]
        self.tfidf_sparse_matrix = picks[1]
        self.patent_classification_np_array = picks[2]
        print(type(self.cite_graph))
        print(type(self.tfidf_sparse_matrix))
        print(type(self.patent_classification_np_array))


    def generate_content_file():
        return 0
        # @todo
    def generate_cites_data():
        return 0
        # @todo:

