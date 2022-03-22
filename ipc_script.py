import pandas as pd
import numpy as np
import pickle
import random
import time

def ipc_scr(test_indices, train_indices, indices_dict):
    d_iter = pd.read_csv("../patent_databases/ipcr.tsv", sep="\t",
                    usecols=["patent_id", "section"],
                    chunksize=250000, low_memory=False)


    ipc_nda = np.zeros(shape=(len(indices_dict.keys()), 8), dtype=int)
    print("Creating label matrix...")
    i = -1
    for chunk in d_iter:
        for row in chunk["section"]:
            i = i + 1
            tmp_index = chunk["patent_id"][i]
            if tmp_index in indices_dict.keys():
                if (row == "A"):
                    ipc_nda[indices_dict[tmp_index]][0] = 1
                elif (row == "B"):
                    ipc_nda[indices_dict[tmp_index]][1] = 1
                elif (row == "C"):
                    ipc_nda[indices_dict[tmp_index]][2] = 1
                elif (row == "D"):
                    ipc_nda[indices_dict[tmp_index]][3] = 1
                elif (row == "E"):
                    ipc_nda[indices_dict[tmp_index]][4] = 1
                elif (row == "F"):
                    ipc_nda[indices_dict[tmp_index]][5] = 1
                elif (row == "G"):
                    ipc_nda[indices_dict[tmp_index]][6] = 1
                elif (row == "H"):
                    ipc_nda[indices_dict[tmp_index]][7] = 1

        print("check_i", i)



    print(len(ipc_nda))
    print(type(ipc_nda))

    #test_indices = random.sample(range(7814196), k=3907098) # half
    #train_indices = random.sample(test_indices, k=390709) # 5%

    all_pickled = open("../generated_data/ind.ptcdb.ally","wb")
    pickle.dump(ipc_nda, all_pickled)
    all_pickled.close()

    y_pickled = open("../generated_data/ind.ptcdb.y","wb")
    train = ipc_nda[train_indices, :]
    pickle.dump(train, y_pickled)
    y_pickled.close()

    ty_pickled = open("../generated_data/ind.ptcdb.ty","wb")
    test = ipc_nda[test_indices, :]
    pickle.dump(test, ty_pickled)
    ty_pickled.close()

# IndexError: index 11049786 is out of bounds for axis 0 with size 11049786

