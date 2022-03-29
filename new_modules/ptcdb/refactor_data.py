import random
import time
import numpy as np
from read_pickle import data_reader


class data_refactorizer:

    def __init__(self, filelist):
        picks = data_reader(filelist).get_picks()

        self.id_list = []
        self.cite_graph = picks[0] # citation dict of lists
        self.tfidf_sparse_matrix = picks[1] # tfidf sparse matrix, may be in need of refactoring
        self.patent_classification_np_array = picks[2] # ipc classifications array

        self.generate_cites_data()

        print(type(self.cite_graph))
        print(type(self.tfidf_sparse_matrix))
        print(type(self.patent_classification_np_array))

    def generate_content_file(self):
        mtx = self.tfidf_sparse_matrix
        arr = self.patent_classification_np_array
        # @todo
        # need to generate as this format:
        # <paper_id> <word_attributes>+ <class_label>
        # for key in id list:
        #   get feature matrix by either regenerating data from db, or using the data in hand
        #   get class_label by iterating through array in 2d and appending classes "a,b,c..."


    def generate_cites_data(self):
        lines = [] # lines list
        keys = self.cite_graph.keys() # keys list

        for key in keys:
            self.id_list.append(key) # may be needed
            for cite in self.cite_graph[key]:
                string = str(cite) + "	" + str(key) # create the line as string
                lines.append(string) # append to lines

        random.shuffle(lines) # can be omitted
        cites_file = open("ptcdb.cites", "w")

        for line in lines:
            print(line, file=cites_file)

    # we may need to go one level down in abstraction and create new objects for each patent in db,
    # may be easier to realize than regenerating data from database to prune the graph.
